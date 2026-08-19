# 📞 GenAI Meeting Intelligence

A schema-driven **Generative AI application** that transforms unstructured meeting transcripts into structured operational intelligence.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-blue.svg)](https://docs.pydantic.dev/)

---

## 🎯 Overview

Automatically extract structured intelligence from meeting transcripts using LLMs with validated schema output.

**Perfect for:** Corporate meetings, project reviews, client calls, sprint planning, board meetings, team sync-ups.

---

## ✨ Key Features

✅ **Structured Output** - Pydantic models ensure typed, validated data  
✅ **Multi-Level Extraction** - Summaries, decisions, action items, risks  
✅ **Owner & Priority Assignment** - Action items with accountability  
✅ **Risk Identification** - Automatic blocker detection  
✅ **Topic Detection** - What was discussed  
✅ **Downstream Integration** - Ready for Jira, Slack, Teams, email  
✅ **Interview-Ready** - Shows schema-driven LLM output discipline  

---

## 📊 Output

The API extracts:

- **Executive Summary** - High-level overview for stakeholders
- **Key Decisions** - What was decided and by whom
- **Action Items** - Tasks with owner, due date, and priority
- **Risks and Blockers** - Identified concerns and impediments
- **Follow-up Questions** - Remaining open items
- **Detected Topics** - What was discussed

---

## 🏗️ Architecture

```
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

---

## 🚀 Quick Start

### Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY=...
uvicorn app.api:app --reload
```

### CLI Usage

```bash
python -m app.cli sample_data/meeting.txt
```

### API Usage

**POST /analyze** through Swagger UI at `http://127.0.0.1:8000/docs`

---

## 📝 Example Response

```json
{
  "summary": "Q3 planning review covered roadmap priorities, resource constraints, and hiring plans",
  "decisions": [
    {
      "decision": "Prioritize authentication over analytics",
      "owner": "Alice (PM)",
      "confidence": 0.95
    }
  ],
  "action_items": [
    {
      "task": "Prepare authentication spec",
      "owner": "Bob",
      "due_date": "2026-08-23",
      "priority": "high"
    }
  ],
  "risks": [
    {
      "risk": "Timeline pressure on authentication module",
      "severity": "medium",
      "mitigation": "Allocate additional resources"
    }
  ],
  "follow_ups": [
    {
      "item": "Share roadmap with stakeholders",
      "owner": "Alice"
    }
  ]
}
```

---

## 💡 Why This Is More Than a Prompt Demo

The LLM output is mapped to explicit **Pydantic models** so downstream systems receive typed data instead of unpredictable free-form text. This makes integration with Jira, Slack, Teams reliable and maintainable.

---

## 🧪 Testing

```bash
python -m pytest tests/ -v
```

---

## 📂 Project Structure

```
genai-meeting-intelligence/
├── app/
│   ├── api.py              # FastAPI application
│   ├── cli.py              # CLI interface
│   ├── analyzer.py         # LLM-based analysis
│   ├── prompts.py          # System prompts
│   └── schemas.py          # Pydantic models
├── sample_data/
│   └── meeting.txt
├── tests/
│   └── test_api.py
├── requirements.txt
└── README.md
```

---

## 🚀 Production Improvements

- Async processing for large transcripts
- Speaker diarization (who said what)
- Audio transcription from mp3/wav
- Jira/Teams/Slack integrations
- Confidence and provenance fields per extraction
- Prompt versioning and A/B testing
- PII redaction
- Token and cost tracking
- Human review workflow for high-impact actions
- Meeting recording transcription API support

---

## 📊 Interview Talking Points

- Benefits of schema-driven LLM output over free-form text
- How to handle hallucinations and validation failures
- Streaming vs. structured output trade-offs
- Cost optimization strategies
- Confidence scoring and reliability

---

## 🤝 Contributing

Contributions welcome! Please fork, create a feature branch, and submit a PR.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙋 Support

- **Issues:** [GitHub Issues](https://github.com/Nagaraju2030/genai-meeting-intelligence/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Nagaraju2030/genai-meeting-intelligence/discussions)

---

<div align="center">

**⭐ Transform your meetings into intelligence!**

Built for structured GenAI applications

</div>