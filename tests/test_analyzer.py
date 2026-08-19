"""Tests for the meeting analyzer."""

import json
from unittest.mock import patch, MagicMock
import pytest

from app.analyzer import MeetingAnalyzer, create_analyzer
from app.schemas import MeetingAnalysisRequest


class TestMeetingAnalyzer:
    """Test MeetingAnalyzer class."""

    @patch("app.analyzer.OpenAI")
    def test_analyzer_initialization(self, mock_openai):
        """Test analyzer initialization."""
        analyzer = MeetingAnalyzer()
        assert analyzer.model is not None

    @patch("app.analyzer.OpenAI")
    def test_analyze_success(self, mock_openai, sample_analysis_request):
        """Test successful analysis."""
        # Mock the OpenAI response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = json.dumps({
            "summary": "Q3 planning review",
            "decisions": [],
            "action_items": [],
            "risks": [],
            "follow_ups": [],
            "topics": ["Planning"],
        })

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        analyzer = MeetingAnalyzer()
        result = analyzer.analyze(sample_analysis_request)

        assert result.analysis.summary == "Q3 planning review"
        assert result.model_used is not None
        assert result.processing_time_seconds > 0
        assert result.transcript_tokens > 0

    @patch("app.analyzer.OpenAI")
    def test_analyze_empty_transcript(self, mock_openai):
        """Test with empty transcript."""
        analyzer = MeetingAnalyzer()
        request = MeetingAnalysisRequest(transcript="")

        with pytest.raises(ValueError, match="cannot be empty"):
            analyzer.analyze(request)

    @patch("app.analyzer.OpenAI")
    def test_analyze_invalid_json_response(self, mock_openai, sample_analysis_request):
        """Test handling of invalid JSON response."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "not valid json"

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        analyzer = MeetingAnalyzer()

        with pytest.raises(ValueError):
            analyzer.analyze(sample_analysis_request)

    @patch("app.analyzer.OpenAI")
    def test_parse_response_with_markdown(self, mock_openai):
        """Test parsing JSON from markdown code blocks."""
        analyzer = MeetingAnalyzer()

        response_text = """Here's the analysis:
        ```json
        {"summary": "Test"}
        ```
        """

        result = analyzer._parse_response(response_text)
        assert result["summary"] == "Test"

    @patch("app.analyzer.OpenAI")
    def test_estimate_tokens(self, mock_openai):
        """Test token estimation."""
        analyzer = MeetingAnalyzer()

        text = "Hello world" * 100  # ~1100 characters
        tokens = analyzer._estimate_tokens(text)

        # Should be approximately 1100/4 = 275 tokens
        assert tokens > 200
        assert tokens < 400


class TestCreateAnalyzer:
    """Test factory function."""

    @patch("app.analyzer.OpenAI")
    def test_create_analyzer(self, mock_openai):
        """Test creating analyzer."""
        analyzer = create_analyzer()
        assert isinstance(analyzer, MeetingAnalyzer)
