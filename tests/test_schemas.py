"""Tests for Pydantic schemas."""

import pytest
from app.schemas import (
    Decision,
    ActionItem,
    Risk,
    FollowUp,
    MeetingAnalysis,
    MeetingAnalysisRequest,
    MeetingAnalysisResponse,
)


class TestDecision:
    """Test Decision schema."""

    def test_decision_creation(self):
        """Test creating a decision."""
        decision = Decision(
            decision="Prioritize authentication",
            owner="Alice",
            confidence=0.95,
        )
        assert decision.decision == "Prioritize authentication"
        assert decision.owner == "Alice"
        assert decision.confidence == 0.95

    def test_decision_confidence_validation(self):
        """Test confidence score validation."""
        with pytest.raises(ValueError):
            Decision(decision="Test", confidence=1.5)

        with pytest.raises(ValueError):
            Decision(decision="Test", confidence=-0.1)


class TestActionItem:
    """Test ActionItem schema."""

    def test_action_item_creation(self):
        """Test creating an action item."""
        item = ActionItem(
            task="Prepare authentication spec",
            owner="Bob",
            due_date="2026-08-23",
            priority="high",
        )
        assert item.task == "Prepare authentication spec"
        assert item.owner == "Bob"
        assert item.priority == "high"

    def test_action_item_default_priority(self):
        """Test default priority."""
        item = ActionItem(task="Do something")
        assert item.priority == "medium"

    def test_action_item_priority_validation(self):
        """Test priority validation."""
        with pytest.raises(ValueError):
            ActionItem(task="Test", priority="urgent")


class TestRisk:
    """Test Risk schema."""

    def test_risk_creation(self):
        """Test creating a risk."""
        risk = Risk(
            risk="Timeline pressure",
            severity="medium",
            mitigation="Allocate additional resources",
        )
        assert risk.risk == "Timeline pressure"
        assert risk.severity == "medium"


class TestMeetingAnalysisRequest:
    """Test MeetingAnalysisRequest schema."""

    def test_request_creation(self):
        """Test creating a request."""
        request = MeetingAnalysisRequest(
            transcript="Meeting transcript here",
            meeting_title="Test Meeting",
            participants=["Alice", "Bob"],
        )
        assert request.transcript == "Meeting transcript here"
        assert request.meeting_title == "Test Meeting"
        assert len(request.participants) == 2

    def test_request_empty_transcript_validation(self):
        """Empty transcript should still be valid at schema level."""
        # Schema validation allows empty, business logic validates later
        request = MeetingAnalysisRequest(
            transcript="",
            meeting_title="Test",
        )
        assert request.transcript == ""


class TestMeetingAnalysis:
    """Test MeetingAnalysis schema."""

    def test_full_analysis_creation(self):
        """Test creating complete analysis."""
        analysis = MeetingAnalysis(
            summary="Q3 planning review",
            decisions=[
                Decision(decision="Prioritize auth", confidence=0.95)
            ],
            action_items=[
                ActionItem(
                    task="Prepare spec",
                    owner="Bob",
                    priority="high",
                )
            ],
            topics=["Planning", "Resources"],
        )
        assert analysis.summary == "Q3 planning review"
        assert len(analysis.decisions) == 1
        assert len(analysis.action_items) == 1
        assert len(analysis.topics) == 2

    def test_analysis_default_fields(self):
        """Test default values."""
        analysis = MeetingAnalysis(summary="Test")
        assert analysis.summary == "Test"
        assert analysis.decisions == []
        assert analysis.action_items == []
        assert analysis.topics == []
