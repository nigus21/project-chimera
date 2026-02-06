# Skill: Trend Fetcher

## Purpose
The Trend Fetcher skill is responsible for retrieving trending topics, keywords, or media signals
from external platforms (e.g., social media APIs, analytics services).

This skill provides structured, normalized trend data to downstream agents
(e.g., Planner Agent) for content ideation.

---

## Input Contract (JSON)

```json
{
  "platform": "string",
  "region": "string",
  "category": "string",
  "time_window_hours": "integer"
}