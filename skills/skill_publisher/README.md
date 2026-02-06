
---

# 📁 `skills/skill_publisher/README.md`  

```md
# Skill: Publisher

## Purpose
The Publisher skill executes approved publishing actions
on external content platforms.

This skill represents a **controlled execution boundary**.
It may only operate with explicit authorization.

---

## Input Contract (JSON)

```json
{
  "content_id": "string",
  "platform": "string",
  "media_asset_url": "string",
  "publish_metadata": {
    "title": "string",
    "description": "string",
    "tags": ["string"]
  },
  "approval_token": "string"
}