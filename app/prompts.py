"""System prompts for LLM-based meeting analysis."""

MEETING_ANALYSIS_SYSTEM_PROMPT = """You are an expert meeting analyst. Your task is to analyze meeting transcripts and extract structured intelligence.

When analyzing a meeting transcript, you must:

1. **Summary**: Create a concise executive summary (2-3 sentences) capturing the main purpose and outcome
2. **Decisions**: Extract explicit decisions made, who made them, and your confidence
3. **Action Items**: Identify tasks with owners, due dates (if mentioned), and priority levels
4. **Risks**: Identify potential risks, blockers, or concerns with severity levels and mitigation strategies
5. **Follow-ups**: Extract items that need further discussion or clarification
6. **Topics**: List the main topics discussed

Guidelines:
- Be precise and concrete. Extract only what is explicitly stated or clearly implied
- Assign priorities based on urgency and impact mentioned in the meeting
- For risks, focus on genuine blockers and concerns, not minor issues
- Ensure all owners and names are captured accurately
- Maintain objectivity and avoid speculation beyond the transcript
- If information is uncertain, note it in confidence scores or mitigation fields
- Extract dates in YYYY-MM-DD format when possible

Return your analysis in valid JSON format matching the required schema."""

MEETING_ANALYSIS_USER_PROMPT_TEMPLATE = """Analyze the following meeting transcript and extract structured intelligence:

Meeting Title: {meeting_title}
Participants: {participants}

Transcript:
---
{transcript}
---

Provide the analysis in JSON format with the following structure:
{{
    "summary": "Executive summary of the meeting",
    "decisions": [
        {{
            "decision": "What was decided",
            "owner": "Who decided",
            "confidence": 0.95
        }}
    ],
    "action_items": [
        {{
            "task": "What needs to be done",
            "owner": "Who is responsible",
            "due_date": "YYYY-MM-DD or null",
            "priority": "high|medium|low"
        }}
    ],
    "risks": [
        {{
            "risk": "Identified risk",
            "severity": "high|medium|low",
            "mitigation": "How to mitigate"
        }}
    ],
    "follow_ups": [
        {{
            "item": "Follow-up item",
            "owner": "Responsible person or null"
        }}
    ],
    "topics": ["Topic 1", "Topic 2"]
}}"""


def get_analysis_prompt(
    transcript: str, meeting_title: str = None, participants: list = None
) -> tuple[str, str]:
    """Generate system and user prompts for meeting analysis.

    Args:
        transcript: The meeting transcript text
        meeting_title: Optional title of the meeting
        participants: Optional list of participants

    Returns:
        Tuple of (system_prompt, user_prompt)
    """
    participants_str = ", ".join(participants) if participants else "Not specified"
    meeting_title_str = meeting_title or "Untitled Meeting"

    user_prompt = MEETING_ANALYSIS_USER_PROMPT_TEMPLATE.format(
        meeting_title=meeting_title_str, participants=participants_str, transcript=transcript
    )

    return MEETING_ANALYSIS_SYSTEM_PROMPT, user_prompt
