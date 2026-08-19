"""Pydantic schemas for meeting analysis output."""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Decision(BaseModel):
    """Represents a decision made during the meeting."""

    decision: str = Field(..., description="The decision that was made")
    owner: Optional[str] = Field(None, description="Person responsible for the decision")
    confidence: float = Field(
        default=0.9, ge=0.0, le=1.0, description="Confidence score (0-1)"
    )


class ActionItem(BaseModel):
    """Represents an action item to be completed."""

    task: str = Field(..., description="Description of the task")
    owner: Optional[str] = Field(None, description="Person assigned to the task")
    due_date: Optional[str] = Field(None, description="Due date for the task (YYYY-MM-DD)")
    priority: str = Field(
        default="medium",
        description="Priority level: high, medium, low",
        pattern="^(high|medium|low)$",
    )


class Risk(BaseModel):
    """Represents an identified risk or blocker."""

    risk: str = Field(..., description="Description of the risk")
    severity: str = Field(
        default="medium",
        description="Severity level: high, medium, low",
        pattern="^(high|medium|low)$",
    )
    mitigation: Optional[str] = Field(None, description="Proposed mitigation strategy")


class FollowUp(BaseModel):
    """Represents a follow-up item."""

    item: str = Field(..., description="Follow-up item description")
    owner: Optional[str] = Field(None, description="Person responsible for follow-up")


class MeetingAnalysis(BaseModel):
    """Complete structured analysis of a meeting transcript."""

    summary: str = Field(..., description="Executive summary of the meeting")
    decisions: List[Decision] = Field(
        default_factory=list, description="Key decisions made"
    )
    action_items: List[ActionItem] = Field(
        default_factory=list, description="Action items with ownership"
    )
    risks: List[Risk] = Field(
        default_factory=list, description="Identified risks and blockers"
    )
    follow_ups: List[FollowUp] = Field(
        default_factory=list, description="Follow-up items"
    )
    topics: List[str] = Field(default_factory=list, description="Topics discussed")
    meeting_duration_minutes: Optional[int] = Field(
        None, description="Duration of the meeting in minutes"
    )
    participants: List[str] = Field(
        default_factory=list, description="Meeting participants"
    )


class MeetingAnalysisRequest(BaseModel):
    """Request payload for meeting analysis."""

    transcript: str = Field(..., description="Meeting transcript text")
    meeting_title: Optional[str] = Field(None, description="Title of the meeting")
    participants: List[str] = Field(
        default_factory=list, description="List of meeting participants"
    )


class MeetingAnalysisResponse(BaseModel):
    """Response payload for meeting analysis."""

    analysis: MeetingAnalysis = Field(..., description="Analyzed meeting data")
    processing_time_seconds: float = Field(
        ..., description="Time taken to process the meeting"
    )
    model_used: str = Field(..., description="LLM model used for analysis")
    transcript_tokens: int = Field(..., description="Tokens in the transcript")
