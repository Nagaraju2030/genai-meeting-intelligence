"""Command-line interface for meeting analysis."""

import json
import logging
import sys
from pathlib import Path

from app.analyzer import create_analyzer
from app.schemas import MeetingAnalysisRequest

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def load_transcript(file_path: str) -> str:
    """Load meeting transcript from file.

    Args:
        file_path: Path to transcript file

    Returns:
        Transcript text

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Transcript file not found: {file_path}")

    logger.info(f"Loading transcript from {file_path}")
    return path.read_text(encoding="utf-8")


def analyze_transcript_cli(
    transcript_path: str,
    meeting_title: str = None,
    participants: list = None,
    output_file: str = None,
):
    """Analyze a meeting transcript from the command line.

    Args:
        transcript_path: Path to the transcript file
        meeting_title: Optional title of the meeting
        participants: Optional list of participants
        output_file: Optional file to save results to
    """
    try:
        # Load transcript
        transcript = load_transcript(transcript_path)

        # Create request
        request = MeetingAnalysisRequest(
            transcript=transcript,
            meeting_title=meeting_title or Path(transcript_path).stem,
            participants=participants or [],
        )

        # Analyze
        logger.info("Starting analysis...")
        analyzer = create_analyzer()
        response = analyzer.analyze(request)

        # Format output
        result = {
            "meeting_title": request.meeting_title,
            "processing_time_seconds": response.processing_time_seconds,
            "model_used": response.model_used,
            "transcript_tokens": response.transcript_tokens,
            "analysis": response.analysis.model_dump(),
        }

        # Output results
        output_json = json.dumps(result, indent=2, default=str)

        if output_file:
            Path(output_file).write_text(output_json)
            logger.info(f"Results saved to {output_file}")
        else:
            print("\n" + "=" * 80)
            print("MEETING ANALYSIS RESULTS")
            print("=" * 80 + "\n")
            print(output_json)

        logger.info(f"Analysis completed in {response.processing_time_seconds:.2f}s")

    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze meeting transcripts using GenAI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m app.cli sample_data/meeting.txt
  python -m app.cli transcript.txt --title "Q3 Planning" --output results.json
  python -m app.cli meeting.txt --participants "Alice" "Bob" "Charlie"
        """,
    )

    parser.add_argument("transcript", help="Path to transcript file")
    parser.add_argument(
        "--title", help="Meeting title (defaults to filename)", default=None
    )
    parser.add_argument(
        "--participants",
        nargs="+",
        help="List of participants",
        default=[],
    )
    parser.add_argument(
        "--output", help="Output file for results (JSON)", default=None
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    analyze_transcript_cli(
        transcript_path=args.transcript,
        meeting_title=args.title,
        participants=args.participants,
        output_file=args.output,
    )
