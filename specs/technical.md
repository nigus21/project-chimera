# Project Chimera – Technical Specification

## Purpose

This document defines the technical implementation contracts for Project Chimera. All API interfaces, data structures, and system behaviors MUST conform to the specifications defined herein. This specification is designed to be executable by AI agents without ambiguity or interpretation.

---

## API Contracts

### Trend Fetch Results

#### Schema Definition

**Endpoint:** Internal API (Skill output)  
**Method:** N/A (Skill return value)  
**Content-Type:** `application/json`

**Schema:**

```json
{
  "type": "object",
  "required": ["request_id", "timestamp", "status", "trends"],
  "properties": {
    "request_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier for this trend fetch request"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp when trends were fetched"
    },
    "status": {
      "type": "string",
      "enum": ["success", "partial", "failed"],
      "description": "Overall status of the trend fetch operation"
    },
    "trends": {
      "type": "array",
      "minItems": 0,
      "items": {
        "type": "object",
        "required": ["trend_id", "title", "source", "relevance_score", "observed_at"],
        "properties": {
          "trend_id": {
            "type": "string",
            "format": "uuid",
            "description": "Unique identifier for this trend"
          },
          "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 500,
            "description": "Human-readable title of the trend"
          },
          "description": {
            "type": "string",
            "maxLength": 5000,
            "description": "Optional detailed description of the trend"
          },
          "source": {
            "type": "string",
            "enum": ["openclaw", "social_platform", "aggregator", "manual"],
            "description": "Origin of the trend data"
          },
          "source_agent_id": {
            "type": "string",
            "format": "uuid",
            "description": "Identifier of the agent that provided this trend (required if source is 'openclaw')"
          },
          "relevance_score": {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0,
            "description": "Relevance score between 0.0 and 1.0"
          },
          "observed_at": {
            "type": "string",
            "format": "date-time",
            "description": "ISO 8601 timestamp when trend was first observed"
          },
          "metadata": {
            "type": "object",
            "description": "Optional additional metadata about the trend",
            "additionalProperties": true
          }
        }
      }
    },
    "error": {
      "type": "object",
      "description": "Error details (required if status is 'failed')",
      "required": ["code", "message"],
      "properties": {
        "code": {
          "type": "string",
          "description": "Machine-readable error code"
        },
        "message": {
          "type": "string",
          "description": "Human-readable error message"
        },
        "details": {
          "type": "object",
          "description": "Optional additional error context",
          "additionalProperties": true
        }
      }
    },
    "partial_results_reason": {
      "type": "string",
      "description": "Explanation for partial results (required if status is 'partial')"
    }
  }
}
```

**Example - Success:**

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-02-06T14:30:00Z",
  "status": "success",
  "trends": [
    {
      "trend_id": "660e8400-e29b-41d4-a716-446655440001",
      "title": "AI Agent Collaboration Protocols",
      "description": "Growing discussion about standardized protocols for agent-to-agent communication",
      "source": "openclaw",
      "source_agent_id": "770e8400-e29b-41d4-a716-446655440002",
      "relevance_score": 0.85,
      "observed_at": "2026-02-06T12:00:00Z",
      "metadata": {
        "category": "technology",
        "engagement_count": 1250
      }
    }
  ]
}
```

**Example - Partial:**

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-02-06T14:30:00Z",
  "status": "partial",
  "trends": [
    {
      "trend_id": "660e8400-e29b-41d4-a716-446655440001",
      "title": "AI Agent Collaboration Protocols",
      "source": "openclaw",
      "source_agent_id": "770e8400-e29b-41d4-a716-446655440002",
      "relevance_score": 0.85,
      "observed_at": "2026-02-06T12:00:00Z"
    }
  ],
  "partial_results_reason": "Rate limit reached after fetching 1 of 3 requested sources"
}
```

**Example - Failed:**

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-02-06T14:30:00Z",
  "status": "failed",
  "trends": [],
  "error": {
    "code": "EXTERNAL_SERVICE_UNAVAILABLE",
    "message": "Trend aggregation service returned 503",
    "details": {
      "service": "openclaw_trend_api",
      "retry_after_seconds": 60
    }
  }
}
```

---

### Content Plan Output

#### Schema Definition

**Endpoint:** Planner Agent output  
**Method:** N/A (Agent output)  
**Content-Type:** `application/json`

**Schema:**

```json
{
  "type": "object",
  "required": ["plan_id", "objective_id", "created_at", "spec_version", "tasks"],
  "properties": {
    "plan_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier for this content plan"
    },
    "objective_id": {
      "type": "string",
      "format": "uuid",
      "description": "Identifier of the objective this plan addresses"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp when plan was created"
    },
    "spec_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Semantic version of specifications used to generate this plan"
    },
    "tasks": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["task_id", "task_type", "required_skill", "input_parameters", "success_criteria", "status"],
        "properties": {
          "task_id": {
            "type": "string",
            "format": "uuid",
            "description": "Unique identifier for this task"
          },
          "task_type": {
            "type": "string",
            "enum": ["trend_fetch", "content_draft", "content_review", "approval_request", "publish"],
            "description": "Type of task to be executed"
          },
          "required_skill": {
            "type": "string",
            "description": "Identifier of the Skill required to execute this task"
          },
          "input_parameters": {
            "type": "object",
            "description": "Input parameters for the Skill invocation",
            "additionalProperties": true
          },
          "success_criteria": {
            "type": "object",
            "required": ["validation_schema"],
            "properties": {
              "validation_schema": {
                "type": "string",
                "description": "JSON Schema reference for validating task output"
              },
              "required_fields": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "List of fields that must be present in output"
              }
            }
          },
          "depends_on": {
            "type": "array",
            "items": {
              "type": "string",
              "format": "uuid"
            },
            "description": "Array of task_id values that must complete before this task can execute"
          },
          "status": {
            "type": "string",
            "enum": ["pending", "assigned", "in_progress", "completed", "failed", "cancelled"],
            "description": "Current status of the task"
          },
          "priority": {
            "type": "integer",
            "minimum": 1,
            "maximum": 10,
            "description": "Task priority (1 = highest, 10 = lowest)"
          }
        }
      }
    },
    "metadata": {
      "type": "object",
      "description": "Optional plan metadata",
      "additionalProperties": true
    }
  }
}
```

**Example:**

```json
{
  "plan_id": "880e8400-e29b-41d4-a716-446655440000",
  "objective_id": "990e8400-e29b-41d4-a716-446655440001",
  "created_at": "2026-02-06T15:00:00Z",
  "spec_version": "1.0.0",
  "tasks": [
    {
      "task_id": "aa0e8400-e29b-41d4-a716-446655440002",
      "task_type": "trend_fetch",
      "required_skill": "fetch_trends_from_openclaw",
      "input_parameters": {
        "sources": ["openclaw"],
        "max_results": 10,
        "min_relevance": 0.7
      },
      "success_criteria": {
        "validation_schema": "trend_fetch_result_schema",
        "required_fields": ["trends", "status"]
      },
      "depends_on": [],
      "status": "pending",
      "priority": 1
    },
    {
      "task_id": "bb0e8400-e29b-41d4-a716-446655440003",
      "task_type": "content_draft",
      "required_skill": "draft_content_from_trends",
      "input_parameters": {
        "trend_ids": ["{{task:aa0e8400-e29b-41d4-a716-446655440002:trends[0].trend_id}}"],
        "content_type": "post",
        "platform": "twitter"
      },
      "success_criteria": {
        "validation_schema": "content_draft_schema",
        "required_fields": ["content_id", "draft_text", "metadata"]
      },
      "depends_on": ["aa0e8400-e29b-41d4-a716-446655440002"],
      "status": "pending",
      "priority": 2
    }
  ],
  "metadata": {
    "estimated_completion": "2026-02-06T16:00:00Z"
  }
}
```

---

### Skill Invocation Input/Output

#### Input Schema

**Schema:**

```json
{
  "type": "object",
  "required": ["invocation_id", "skill_id", "agent_id", "input_parameters"],
  "properties": {
    "invocation_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier for this Skill invocation"
    },
    "skill_id": {
      "type": "string",
      "description": "Identifier of the Skill to invoke"
    },
    "agent_id": {
      "type": "string",
      "format": "uuid",
      "description": "Identifier of the agent making this invocation"
    },
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "Identifier of the task this invocation is part of (optional)"
    },
    "input_parameters": {
      "type": "object",
      "description": "Skill-specific input parameters",
      "additionalProperties": true
    },
    "idempotency_key": {
      "type": "string",
      "description": "Optional idempotency key for retry-safe invocations"
    }
  }
}
```

**Example:**

```json
{
  "invocation_id": "cc0e8400-e29b-41d4-a716-446655440004",
  "skill_id": "fetch_trends_from_openclaw",
  "agent_id": "dd0e8400-e29b-41d4-a716-446655440005",
  "task_id": "aa0e8400-e29b-41d4-a716-446655440002",
  "input_parameters": {
    "sources": ["openclaw"],
    "max_results": 10,
    "min_relevance": 0.7
  },
  "idempotency_key": "trend_fetch_2026-02-06_15:00:00"
}
```

#### Output Schema

**Schema:**

```json
{
  "type": "object",
  "required": ["invocation_id", "status", "completed_at"],
  "properties": {
    "invocation_id": {
      "type": "string",
      "format": "uuid",
      "description": "Identifier matching the input invocation_id"
    },
    "status": {
      "type": "string",
      "enum": ["success", "failed", "timeout"],
      "description": "Status of the Skill invocation"
    },
    "completed_at": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp when invocation completed"
    },
    "output": {
      "type": "object",
      "description": "Skill output data (required if status is 'success')",
      "additionalProperties": true
    },
    "error": {
      "type": "object",
      "description": "Error details (required if status is 'failed' or 'timeout')",
      "required": ["code", "message"],
      "properties": {
        "code": {
          "type": "string",
          "description": "Machine-readable error code"
        },
        "message": {
          "type": "string",
          "description": "Human-readable error message"
        },
        "error_type": {
          "type": "string",
          "enum": ["skill_error", "validation_error", "resource_error", "external_service_error"],
          "description": "Classification of the error"
        },
        "details": {
          "type": "object",
          "description": "Optional additional error context",
          "additionalProperties": true
        },
        "retryable": {
          "type": "boolean",
          "description": "Whether this error is retryable"
        }
      }
    },
    "execution_duration_ms": {
      "type": "integer",
      "minimum": 0,
      "description": "Execution duration in milliseconds"
    },
    "resource_usage": {
      "type": "object",
      "description": "Optional resource usage metrics",
      "properties": {
        "api_calls": {
          "type": "integer",
          "minimum": 0
        },
        "tokens_used": {
          "type": "integer",
          "minimum": 0
        }
      }
    }
  }
}
```

**Example - Success:**

```json
{
  "invocation_id": "cc0e8400-e29b-41d4-a716-446655440004",
  "status": "success",
  "completed_at": "2026-02-06T15:05:00Z",
  "output": {
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2026-02-06T15:05:00Z",
    "status": "success",
    "trends": [
      {
        "trend_id": "660e8400-e29b-41d4-a716-446655440001",
        "title": "AI Agent Collaboration Protocols",
        "source": "openclaw",
        "source_agent_id": "770e8400-e29b-41d4-a716-446655440002",
        "relevance_score": 0.85,
        "observed_at": "2026-02-06T12:00:00Z"
      }
    ]
  },
  "execution_duration_ms": 1250,
  "resource_usage": {
    "api_calls": 1,
    "tokens_used": 450
  }
}
```

**Example - Failed:**

```json
{
  "invocation_id": "cc0e8400-e29b-41d4-a716-446655440004",
  "status": "failed",
  "completed_at": "2026-02-06T15:05:00Z",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Input parameter 'sources' must be a non-empty array",
    "error_type": "validation_error",
    "details": {
      "parameter": "sources",
      "received_type": "string",
      "expected_type": "array"
    },
    "retryable": false
  },
  "execution_duration_ms": 15
}
```

---

## Database Schema

### Overview

**Database System:** PostgreSQL 14+  
**Character Encoding:** UTF-8  
**Time Zone:** UTC (all timestamps stored in UTC)

### Tables

#### objectives

Stores high-level objectives that Planner Agents decompose into tasks.

| Column Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| objective_id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the objective |
| objective_type | VARCHAR(50) | NOT NULL | Type of objective (e.g., 'content_creation', 'trend_analysis') |
| objective_data | JSONB | NOT NULL | Objective parameters and context |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | Current status: 'pending', 'planning', 'executing', 'completed', 'failed', 'cancelled' |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | When objective was created |
| updated_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | When objective was last updated |
| completed_at | TIMESTAMP WITH TIME ZONE | NULL | When objective was completed or failed |
| spec_version | VARCHAR(20) | NOT NULL | Specification version used for this objective |

**Indexes:**
- `idx_objectives_status` ON `objectives(status)`
- `idx_objectives_created_at` ON `objectives(created_at)`
- `idx_objectives_spec_version` ON `objectives(spec_version)`

**Relationships:**
- One-to-many with `plans` (objective_id)

---

#### plans

Stores content plans generated by Planner Agents.

| Column Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| plan_id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the plan |
| objective_id | UUID | FOREIGN KEY(objectives.objective_id), NOT NULL | Objective this plan addresses |
| plan_data | JSONB | NOT NULL | Complete plan structure (tasks, dependencies, etc.) |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | Current status: 'pending', 'executing', 'completed', 'failed', 'cancelled' |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | When plan was created |
| updated_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | When plan was last updated |
| completed_at | TIMESTAMP WITH TIME ZONE | NULL | When plan was completed or failed |
| spec_version | VARCHAR(20) | NOT NULL | Specification version used for this plan |

**Indexes:**
- `idx_plans_objective_id` ON `plans(objective_id)`
- `idx_plans_status` ON `plans(status)`
- `idx_plans_created_at` ON `plans(created_at)`

**Relationships:**
- Many-to-one with `objectives` (objective_id)
- One-to-many with `tasks` (plan_id)

---

#### tasks

Stores individual tasks within plans.

| Column Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| task_id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the task |
| plan_id | UUID | FOREIGN KEY(plans.plan_id), NOT NULL | Plan this task belongs to |
| task_type | VARCHAR(50) | NOT NULL | Type of task (e.g., 'trend_fetch', 'content_draft') |
| required_skill | VARCHAR(100) | NOT NULL | Skill identifier required to execute this task |
| input_parameters | JSONB | NOT NULL | Input parameters for Skill invocation |
| success_criteria | JSONB | NOT NULL | Criteria for task success |
| depends_on | UUID[] | NULL | Array of task_id values this task depends on |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | Current status: 'pending', 'assigned', 'in_progress', 'completed', 'failed', 'cancelled' |
| assigned_agent_id | UUID | NULL | Agent assigned to execute this task |
| priority | INTEGER | NOT NULL, DEFAULT 5, CHECK (priority >= 1 AND priority <= 10) | Task priority (1 = highest) |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | When task was created |
| started_at | TIMESTAMP WITH TIME ZONE | NULL | When task execution started |
| completed_at | TIMESTAMP WITH TIME ZONE | NULL | When task was completed or failed |
| output_data | JSONB | NULL | Task output data (if completed successfully) |
| error_data | JSONB | NULL | Error details (if failed) |

**Indexes:**
- `idx_tasks_plan_id` ON `tasks(plan_id)`
- `idx_tasks_status` ON `tasks(status)`
- `idx_tasks_assigned_agent_id` ON `tasks(assigned_agent_id)`
- `idx_tasks_priority` ON `tasks(priority)`
- `idx_tasks_depends_on` ON `tasks USING GIN(depends_on)`

**Relationships:**
- Many-to-one with `plans` (plan_id)
- One-to-many with `skill_invocations` (task_id)

---

#### skill_invocations

Stores records of all Skill invocations.

| Column Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| invocation_id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the invocation |
| task_id | UUID | FOREIGN KEY(tasks.task_id), NULL | Task this invocation is part of (optional) |
| skill_id | VARCHAR(100) | NOT NULL | Skill that was invoked |
| agent_id | UUID | NOT NULL | Agent that made this invocation |
| input_parameters | JSONB | NOT NULL | Input parameters passed to Skill |
| output_data | JSONB | NULL | Output data returned by Skill |
| status | VARCHAR(20) | NOT NULL | Invocation status: 'success', 'failed', 'timeout' |
| error_data | JSONB | NULL | Error details (if failed or timeout) |
| execution_duration_ms | INTEGER | NOT NULL, DEFAULT 0, CHECK (execution_duration_ms >= 0) | Execution duration in milliseconds |
| resource_usage | JSONB | NULL | Resource usage metrics |
| idempotency_key | VARCHAR(255) | NULL, UNIQUE | Idempotency key for retry-safe invocations |
| invoked_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | When invocation was made |
| completed_at | TIMESTAMP WITH TIME ZONE | NOT NULL | When invocation completed |

**Indexes:**
- `idx_skill_invocations_task_id` ON `skill_invocations(task_id)`
- `idx_skill_invocations_skill_id` ON `skill_invocations(skill_id)`
- `idx_skill_invocations_agent_id` ON `skill_invocations(agent_id)`
- `idx_skill_invocations_status` ON `skill_invocations(status)`
- `idx_skill_invocations_invoked_at` ON `skill_invocations(invoked_at)`
- `idx_skill_invocations_idempotency_key` ON `skill_invocations(idempotency_key)` WHERE `idempotency_key IS NOT NULL`

**Relationships:**
- Many-to-one with `tasks` (task_id)

---

#### trends

Stores trend data fetched from various sources.

| Column Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| trend_id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the trend |
| title | VARCHAR(500) | NOT NULL | Trend title |
| description | TEXT | NULL | Optional trend description |
| source | VARCHAR(50) | NOT NULL | Source of trend: 'openclaw', 'social_platform', 'aggregator', 'manual' |
| source_agent_id | UUID | NULL | Agent that provided this trend (if source is 'openclaw') |
| relevance_score | DECIMAL(3,2) | NOT NULL, CHECK (relevance_score >= 0.0 AND relevance_score <= 1.0) | Relevance score |
| observed_at | TIMESTAMP WITH TIME ZONE | NOT NULL | When trend was first observed |
| metadata | JSONB | NULL | Additional trend metadata |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | When trend was stored in database |
| updated_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | When trend was last updated |

**Indexes:**
- `idx_trends_source` ON `trends(source)`
- `idx_trends_source_agent_id` ON `trends(source_agent_id)` WHERE `source_agent_id IS NOT NULL`
- `idx_trends_relevance_score` ON `trends(relevance_score)`
- `idx_trends_observed_at` ON `trends(observed_at)`
- `idx_trends_created_at` ON `trends(created_at)`

**Relationships:**
- None (standalone reference data)

---

#### approval_requests

Stores approval requests for governed actions.

| Column Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| approval_request_id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the approval request |
| action_type | VARCHAR(50) | NOT NULL | Type of action requiring approval (e.g., 'content_publication') |
| action_data | JSONB | NOT NULL | Details of the action requiring approval |
| requester_agent_id | UUID | NOT NULL | Agent requesting approval |
| workflow_type | VARCHAR(50) | NOT NULL | Type of approval workflow |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | Current status: 'pending', 'approved', 'denied', 'expired' |
| policy_references | TEXT[] | NOT NULL | Array of policy identifiers that triggered this approval |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | When approval request was created |
| reviewed_at | TIMESTAMP WITH TIME ZONE | NULL | When approval was reviewed |
| reviewed_by | VARCHAR(255) | NULL | Identifier of human reviewer |
| review_decision | VARCHAR(20) | NULL | Decision: 'approved', 'denied' |
| review_notes | TEXT | NULL | Optional notes from reviewer |
| expires_at | TIMESTAMP WITH TIME ZONE | NULL | When approval request expires |

**Indexes:**
- `idx_approval_requests_status` ON `approval_requests(status)`
- `idx_approval_requests_requester_agent_id` ON `approval_requests(requester_agent_id)`
- `idx_approval_requests_created_at` ON `approval_requests(created_at)`
- `idx_approval_requests_expires_at` ON `approval_requests(expires_at)` WHERE `expires_at IS NOT NULL`

**Relationships:**
- None (standalone workflow table)

---

#### audit_logs

Stores immutable audit records for all governance decisions and system events.

| Column Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| audit_log_id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the audit log entry |
| event_type | VARCHAR(50) | NOT NULL | Type of event: 'policy_evaluation', 'approval_workflow', 'boundary_enforcement', 'output_validation' |
| agent_id | UUID | NULL | Agent involved in this event |
| action_type | VARCHAR(50) | NULL | Type of action that triggered this event |
| action_data | JSONB | NULL | Details of the action |
| policy_references | TEXT[] | NULL | Policy identifiers relevant to this event |
| decision_outcome | VARCHAR(20) | NOT NULL | Outcome: 'approved', 'rejected', 'deferred', 'error' |
| decision_rationale | TEXT | NOT NULL | Explanation of the decision |
| event_timestamp | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | When event occurred |
| metadata | JSONB | NULL | Additional event metadata |

**Indexes:**
- `idx_audit_logs_event_type` ON `audit_logs(event_type)`
- `idx_audit_logs_agent_id` ON `audit_logs(agent_id)` WHERE `agent_id IS NOT NULL`
- `idx_audit_logs_action_type` ON `audit_logs(action_type)` WHERE `action_type IS NOT NULL`
- `idx_audit_logs_decision_outcome` ON `audit_logs(decision_outcome)`
- `idx_audit_logs_event_timestamp` ON `audit_logs(event_timestamp)`

**Relationships:**
- None (immutable audit trail)

---

#### agent_executions

Stores execution records for agent operations.

| Column Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| execution_id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the execution record |
| agent_id | UUID | NOT NULL | Agent that performed this execution |
| agent_type | VARCHAR(20) | NOT NULL | Type of agent: 'planner', 'worker', 'governor' |
| execution_type | VARCHAR(50) | NOT NULL | Type of execution: 'task_decomposition', 'task_execution', 'policy_evaluation', etc. |
| input_data | JSONB | NULL | Input data for the execution |
| output_data | JSONB | NULL | Output data from the execution |
| status | VARCHAR(20) | NOT NULL | Execution status: 'success', 'failed', 'timeout' |
| error_data | JSONB | NULL | Error details (if failed) |
| execution_duration_ms | INTEGER | NOT NULL, DEFAULT 0, CHECK (execution_duration_ms >= 0) | Execution duration in milliseconds |
| resource_usage | JSONB | NULL | Resource usage metrics |
| started_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | When execution started |
| completed_at | TIMESTAMP WITH TIME ZONE | NULL | When execution completed |

**Indexes:**
- `idx_agent_executions_agent_id` ON `agent_executions(agent_id)`
- `idx_agent_executions_agent_type` ON `agent_executions(agent_type)`
- `idx_agent_executions_execution_type` ON `agent_executions(execution_type)`
- `idx_agent_executions_status` ON `agent_executions(status)`
- `idx_agent_executions_started_at` ON `agent_executions(started_at)`

**Relationships:**
- None (execution history)

---

## Non-Functional Requirements

### Idempotency

#### Requirement IDM-001: Skill Invocation Idempotency

**Requirement:** All Skill invocations MUST be idempotent when an `idempotency_key` is provided.

**Specification:**
- When a Skill invocation request includes an `idempotency_key`, the system MUST check for existing invocations with the same key
- If an existing invocation with the same `idempotency_key` exists and completed successfully, the system MUST return the cached result without re-executing the Skill
- If an existing invocation with the same `idempotency_key` exists and is currently in progress, the system MUST return the in-progress invocation identifier without creating a duplicate
- If an existing invocation with the same `idempotency_key` exists and failed, the system MAY retry (based on retry policy) or return the cached error
- Idempotency keys MUST be unique per agent within a 24-hour window
- Idempotency key lookups MUST use database indexes for performance

**Implementation Contract:**
- Idempotency keys are stored in `skill_invocations.idempotency_key` column with UNIQUE constraint
- Lookup query: `SELECT * FROM skill_invocations WHERE idempotency_key = $1 AND agent_id = $2 AND invoked_at > NOW() - INTERVAL '24 hours' ORDER BY invoked_at DESC LIMIT 1`
- Cache duration: 24 hours from invocation time

---

#### Requirement IDM-002: Task Assignment Idempotency

**Requirement:** Task assignments MUST be idempotent to prevent duplicate execution.

**Specification:**
- When a Planner Agent assigns a task to a Worker Agent, the assignment MUST be atomic
- If a task is already assigned, subsequent assignment requests MUST return the existing assignment without creating duplicates
- Task status transitions MUST be atomic: 'pending' → 'assigned' → 'in_progress' → 'completed'/'failed'
- Concurrent assignment attempts MUST be handled using database-level locking or optimistic concurrency control

**Implementation Contract:**
- Task assignment uses database transaction with row-level locking: `SELECT * FROM tasks WHERE task_id = $1 FOR UPDATE`
- Status update: `UPDATE tasks SET status = 'assigned', assigned_agent_id = $2, updated_at = NOW() WHERE task_id = $1 AND status = 'pending'`
- Assignment succeeds only if update affects exactly one row

---

### Logging

#### Requirement LOG-001: Structured Logging Format

**Requirement:** All system logs MUST use structured JSON format with required fields.

**Specification:**
- Log entries MUST be JSON objects
- All log entries MUST include: `timestamp` (ISO 8601), `level` (enum: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'), `component` (string), `message` (string)
- Log entries SHOULD include: `agent_id` (if applicable), `task_id` (if applicable), `invocation_id` (if applicable), `correlation_id` (for request tracing)
- Log entries MUST NOT include sensitive information (credentials, API keys, personal data)
- Log entries MUST be written to stdout/stderr for containerized deployments

**Log Entry Schema:**

```json
{
  "timestamp": "2026-02-06T15:30:00.123Z",
  "level": "INFO",
  "component": "planner_agent",
  "message": "Task decomposition completed",
  "agent_id": "dd0e8400-e29b-41d4-a716-446655440005",
  "task_id": "aa0e8400-e29b-41d4-a716-446655440002",
  "correlation_id": "ee0e8400-e29b-41d4-a716-446655440006",
  "metadata": {
    "tasks_created": 5,
    "execution_time_ms": 250
  }
}
```

---

#### Requirement LOG-002: Audit Log Persistence

**Requirement:** All governance decisions and critical system events MUST be persisted to `audit_logs` table.

**Specification:**
- Audit log entries MUST be written synchronously before action execution proceeds
- Audit log entries MUST be immutable once written
- Audit log entries MUST include sufficient context to reconstruct decision-making process
- Audit log writes MUST NOT fail silently; failures MUST be treated as critical errors

**Implementation Contract:**
- Audit log writes use database transactions
- If audit log write fails, the associated action MUST be rejected
- Audit log entries are never updated or deleted

---

#### Requirement LOG-003: Execution Logging

**Requirement:** All agent executions MUST be logged to `agent_executions` table.

**Specification:**
- Execution records MUST be created when execution starts
- Execution records MUST be updated when execution completes (success or failure)
- Execution records MUST include input/output data (within size limits)
- Execution records MUST include execution duration and resource usage metrics

**Implementation Contract:**
- Execution record creation: `INSERT INTO agent_executions (...) VALUES (...)`
- Execution record update: `UPDATE agent_executions SET status = $1, output_data = $2, completed_at = NOW(), execution_duration_ms = $3 WHERE execution_id = $4`
- Large input/output data (> 1MB) MAY be truncated or stored separately

---

### Error Handling

#### Requirement ERR-001: Error Classification

**Requirement:** All errors MUST be classified into defined error types.

**Specification:**
- Error types: `skill_error`, `validation_error`, `resource_error`, `external_service_error`, `policy_violation_error`, `system_error`
- Each error MUST include: `code` (machine-readable), `message` (human-readable), `error_type` (classification)
- Errors MAY include: `details` (object), `retryable` (boolean), `retry_after_seconds` (integer)

**Error Schema:**

```json
{
  "code": "VALIDATION_ERROR",
  "message": "Input parameter 'sources' must be a non-empty array",
  "error_type": "validation_error",
  "details": {
    "parameter": "sources",
    "received_type": "string",
    "expected_type": "array"
  },
  "retryable": false
}
```

---

#### Requirement ERR-002: Error Propagation

**Requirement:** Errors MUST propagate through the system with context preservation.

**Specification:**
- When a Worker Agent fails, the error MUST be propagated to the Planner Agent with full context
- When a Skill invocation fails, the error MUST be included in task failure reports
- Error context MUST include: original error, agent chain (which agents handled the request), and timestamp chain
- Errors MUST NOT expose internal system details (file paths, stack traces) to external interfaces

**Error Context Schema:**

```json
{
  "error": {
    "code": "EXTERNAL_SERVICE_ERROR",
    "message": "Trend API returned 503",
    "error_type": "external_service_error",
    "retryable": true,
    "retry_after_seconds": 60
  },
  "context": {
    "agent_chain": ["worker_agent_001", "planner_agent_001"],
    "timestamps": {
      "initial_failure": "2026-02-06T15:30:00Z",
      "propagated_at": "2026-02-06T15:30:01Z"
    },
    "task_id": "aa0e8400-e29b-41d4-a716-446655440002"
  }
}
```

---

#### Requirement ERR-003: Retry Policy

**Requirement:** Retryable errors MUST be handled according to defined retry policies.

**Specification:**
- Only errors with `retryable: true` MAY be retried
- Maximum retry attempts: 3
- Retry backoff strategy: exponential backoff with jitter
  - First retry: after 1 second ± 0.2 seconds
  - Second retry: after 2 seconds ± 0.4 seconds
  - Third retry: after 4 seconds ± 0.8 seconds
- Retry attempts MUST be logged with attempt number and delay
- After maximum retries, error MUST be treated as permanent failure

**Implementation Contract:**
- Retry logic MUST check `error.retryable` field
- Retry delays MUST respect `error.retry_after_seconds` if present
- Retry attempts MUST use idempotency keys to prevent duplicate execution

---

#### Requirement ERR-004: Error Logging

**Requirement:** All errors MUST be logged with sufficient detail for debugging.

**Specification:**
- Error log entries MUST include: error code, message, error type, stack trace (for system errors), and full error context
- Error log entries MUST be written at ERROR level
- Error log entries MUST be persisted to `agent_executions` table with `status = 'failed'` and `error_data` populated
- Critical errors (system errors, policy violations) MUST trigger alerts

**Implementation Contract:**
- Error logging: `INSERT INTO agent_executions (..., status, error_data) VALUES (..., 'failed', $error_json)`
- Stack traces included only for `system_error` type
- Alerts triggered for errors with `error_type = 'system_error'` or `error_type = 'policy_violation_error'`

---

## Conformance Requirements

All implementations MUST:

1. Validate all inputs against the JSON schemas defined in this document
2. Produce outputs conforming to the JSON schemas defined in this document
3. Use the database schema exactly as specified (no additional columns, no missing columns, no type modifications)
4. Implement idempotency, logging, and error handling according to the non-functional requirements
5. Reject any inputs that do not conform to schemas with `validation_error` type errors
6. Never modify audit logs or execution records after creation (immutability)

Deviations from this specification MUST be documented as specification updates before implementation.
