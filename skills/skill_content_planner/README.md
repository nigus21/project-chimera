# Skill: Content Planner

## Purpose
The Content Planner skill converts validated trend data into a structured
content plan suitable for downstream media generation and publishing.

This skill defines *intent*, not final content.
It does not generate text, audio, or video assets.

---

## Input Contract (JSON)

```json
{
  "trends": [
    {
      "topic": "string",
      "confidence_score": "float"
    }
  ],
  "platform": "string",
  "constraints": {
    "max_duration_seconds": "integer",
    "tone": "string",
    "language": "string"
  }
}