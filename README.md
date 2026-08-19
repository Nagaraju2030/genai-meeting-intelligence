# GenAI Meeting Intelligence

A schema-driven Generative AI application that turns unstructured meeting transcripts into structured operational intelligence.

## Output

The API extracts:

- executive summary
- key decisions
- action items with owner, due date and priority
- risks and blockers
- follow-up questions
- detected topics

## Why this is more than a prompt demo

The LLM output is mapped to explicit Pydantic models so downstream systems receive typed data instead of unpredictable free-form text. This makes the project suitable for integrations with Jira, Slack, email, CRM or project-management systems.

## Architecture

```text
Meeting Transcript
       |
       v
Input Validation
       |
       v
Prompt + Structured Output Schema
       |
       v
       LLM
       |
       v
Pydantic Parsed Result
       |
       +--> Summary
       +--> Decisions
       +--> Action Items
       +--> Risks
       +--> Follow-ups
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY=...
uvicorn app.api:app --reload
```

## Try it

```bash
python -m app.cli sample_data/meeting.txt
```

Or use `POST /analyze` through Swagger UI.

## Production improvements

- async processing for large transcripts
- speaker diarization
- audio transcription
- Jira/Teams/Slack integrations
- confidence and provenance fields
- prompt/evaluation versioning
- PII redaction
- token and cost tracking
- human review for high-impact action creation
