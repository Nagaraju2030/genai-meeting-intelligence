"""FastAPI application for meeting analysis."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.analyzer import create_analyzer
from app.config import settings
from app.schemas import MeetingAnalysisRequest, MeetingAnalysisResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create analyzer instance
analyzer = create_analyzer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    # Startup
    logger.info(f"Starting {settings.app_title} v{settings.app_version}")
    logger.info(f"Using model: {settings.openai_model}")

    yield

    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI app
app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    description=settings.app_description,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.app_title,
        "version": settings.app_version,
    }


@app.post(
    "/analyze",
    response_model=MeetingAnalysisResponse,
    tags=["Meeting Analysis"],
    summary="Analyze Meeting Transcript",
    description="Extract structured intelligence from a meeting transcript",
)
async def analyze_meeting(request: MeetingAnalysisRequest) -> MeetingAnalysisResponse:
    """Analyze a meeting transcript and extract structured intelligence.

    Args:
        request: Meeting analysis request with transcript and metadata

    Returns:
        MeetingAnalysisResponse with structured analysis and metadata

    Raises:
        HTTPException: If analysis fails or input is invalid
    """
    try:
        logger.info(
            f"Received analysis request for meeting: {request.meeting_title or 'Untitled'}"
        )

        # Perform analysis
        response = analyzer.analyze(request)

        logger.info(
            f"Successfully analyzed meeting in {response.processing_time_seconds:.2f}s"
        )
        return response

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error during analysis: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during analysis",
        ) from e


@app.get("/", tags=["Info"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_title,
        "version": settings.app_version,
        "description": settings.app_description,
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "analyze": "/analyze",
        },
    }


@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.api:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
