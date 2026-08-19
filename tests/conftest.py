"""Pytest configuration and fixtures."""

import os
import pytest
from unittest.mock import Mock, patch


@pytest.fixture
def mock_openai_api_key():
    """Set mock OpenAI API key for testing."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test-key"}):
        yield


@pytest.fixture
def sample_transcript():
    """Sample meeting transcript for testing."""
    return """
    Meeting: Q3 Planning Review
    Date: 2026-08-19
    Participants: Alice (PM), Bob (Engineering), Charlie (Design)

    Alice: Good morning everyone. Let's start with Q3 planning. We need to finalize our roadmap priorities.

    Bob: I've reviewed the engineering capacity. We can handle the authentication module as top priority.

    Alice: Great. I propose we prioritize authentication over analytics for Q3. Any objections?

    Charlie: I agree. Authentication is more critical for user trust.

    Alice: Perfect. Alice will coordinate with Bob to prepare the authentication spec by August 23rd.

    Bob: I can have the initial spec ready by then. We might need two developers full-time though.

    Alice: Let's schedule a separate meeting to discuss resource allocation. That's a follow-up item.

    Charlie: One concern - if we commit heavy resources to auth, the design system work might suffer.

    Alice: That's a valid risk. We need to plan mitigation carefully. Charlie, can you document the design impact?

    Charlie: I'll prepare a document outlining the timeline impact if resources are shared.

    Alice: Excellent. Let's wrap up with action items:
    1. Bob: Prepare authentication spec (due 2026-08-23, high priority)
    2. Charlie: Document design system impact (medium priority)
    3. Alice: Schedule resource allocation meeting

    We'll reconvene next week to review progress. Thanks everyone.
    """


@pytest.fixture
def sample_analysis_request(sample_transcript):
    """Create a sample analysis request."""
    from app.schemas import MeetingAnalysisRequest

    return MeetingAnalysisRequest(
        transcript=sample_transcript,
        meeting_title="Q3 Planning Review",
        participants=["Alice", "Bob", "Charlie"],
    )
