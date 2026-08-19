"""LLM-based meeting transcript analyzer."""

import json
import logging
import time
from typing import Optional

from openai import OpenAI, APIError, RateLimitError

from app.schemas import MeetingAnalysis, MeetingAnalysisRequest, MeetingAnalysisResponse
from app.prompts import get_analysis_prompt
from app.config import settings

logger = logging.getLogger(__name__)


class MeetingAnalyzer:
    """Analyzes meeting transcripts using OpenAI LLMs."""

    def __init__(self):
        """Initialize the analyzer with OpenAI client."""
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    def analyze(self, request: MeetingAnalysisRequest) -> MeetingAnalysisResponse:
        """Analyze a meeting transcript and extract structured intelligence.

        Args:
            request: Meeting analysis request with transcript and metadata

        Returns:
            MeetingAnalysisResponse with structured analysis

        Raises:
            ValueError: If transcript is empty or analysis fails
            APIError: If OpenAI API call fails
        """
        if not request.transcript or not request.transcript.strip():
            raise ValueError("Transcript cannot be empty")

        start_time = time.time()

        try:
            # Generate prompts
            system_prompt, user_prompt = get_analysis_prompt(
                transcript=request.transcript,
                meeting_title=request.meeting_title,
                participants=request.participants,
            )

            # Call LLM with structured output
            logger.info(f"Analyzing meeting with model {self.model}")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,  # Lower temperature for more consistent extraction
                max_tokens=4096,
            )

            # Extract response content
            response_content = response.choices[0].message.content
            logger.debug(f"LLM Response: {response_content[:200]}...")

            # Parse JSON response
            analysis_data = self._parse_response(response_content)

            # Create MeetingAnalysis object
            analysis = MeetingAnalysis(**analysis_data)

            # Calculate metrics
            processing_time = time.time() - start_time
            transcript_tokens = self._estimate_tokens(request.transcript)

            logger.info(
                f"Meeting analysis completed in {processing_time:.2f}s, "
                f"tokens: {transcript_tokens}"
            )

            return MeetingAnalysisResponse(
                analysis=analysis,
                processing_time_seconds=processing_time,
                model_used=self.model,
                transcript_tokens=transcript_tokens,
            )

        except RateLimitError as e:
            logger.error(f"OpenAI rate limit exceeded: {e}")
            raise ValueError("API rate limit exceeded. Please try again later.") from e
        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise ValueError(f"Failed to analyze meeting: {str(e)}") from e
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            raise ValueError(
                "LLM response was not valid JSON. Please try again."
            ) from e
        except Exception as e:
            logger.error(f"Unexpected error during analysis: {e}")
            raise ValueError(f"Unexpected error: {str(e)}") from e

    def _parse_response(self, response_text: str) -> dict:
        """Parse JSON response from LLM.

        Args:
            response_text: Raw text response from LLM

        Returns:
            Parsed JSON as dictionary

        Raises:
            json.JSONDecodeError: If response is not valid JSON
        """
        # Try to extract JSON from markdown code blocks
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            if end > start:
                response_text = response_text[start:end].strip()
        elif "```" in response_text:
            start = response_text.find("```") + 3
            end = response_text.find("```", start)
            if end > start:
                response_text = response_text[start:end].strip()

        return json.loads(response_text)

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        """Estimate token count for text.

        Uses a simple approximation: ~4 characters per token.
        For production, use tiktoken library for exact counts.

        Args:
            text: Text to estimate tokens for

        Returns:
            Estimated token count
        """
        return len(text) // 4


def create_analyzer() -> MeetingAnalyzer:
    """Factory function to create a MeetingAnalyzer instance.

    Returns:
        Configured MeetingAnalyzer instance
    """
    return MeetingAnalyzer()
