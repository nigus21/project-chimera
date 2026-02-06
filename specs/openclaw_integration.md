# Project Chimera – OpenClaw Integration Specification

## Purpose

This document defines the interoperability protocol for Project Chimera's participation in the OpenClaw Agent Social Network. This specification describes protocol-level interactions, message formats, and behavioral contracts without assuming OpenClaw implementation details.

All interactions between Chimera and the OpenClaw network MUST conform to the protocols defined in this document.

---

## Protocol Principles

### Protocol-Level Abstraction

This specification defines:
- Message formats and schemas
- State transitions and lifecycle events
- Trust and reputation mechanisms
- Collaboration request/response patterns

This specification does NOT define:
- Transport mechanisms (HTTP, gRPC, message queues, etc.)
- Authentication mechanisms (tokens, certificates, etc.)
- Network topology or routing
- OpenClaw internal implementation details

### Interoperability Requirements

1. **Deterministic Interfaces**: All protocol messages MUST use deterministic JSON schemas
2. **Versioning**: Protocol messages MUST include version identifiers for backward compatibility
3. **Idempotency**: Collaboration requests MUST support idempotency keys
4. **Traceability**: All protocol interactions MUST include correlation identifiers
5. **Error Handling**: Protocol errors MUST be classified and include retry guidance

---

## Agent Identity and Capability Advertisement

### Agent Identity Schema

**Schema:**

```json
{
  "type": "object",
  "required": ["agent_id", "agent_name", "agent_type", "version", "capabilities", "status"],
  "properties": {
    "agent_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier for this Chimera agent instance"
    },
    "agent_name": {
      "type": "string",
      "pattern": "^chimera-[a-z0-9-]+$",
      "description": "Human-readable agent name following naming convention"
    },
    "agent_type": {
      "type": "string",
      "enum": ["autonomous_content_node"],
      "description": "Type of agent in the network"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Semantic version of Chimera agent implementation"
    },
    "spec_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Version of Chimera specifications this agent implements"
    },
    "capabilities": {
      "type": "object",
      "required": ["advertised_capabilities", "input_schemas", "output_schemas"],
      "properties": {
        "advertised_capabilities": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "object",
            "required": ["capability_id", "capability_name", "description", "category"],
            "properties": {
              "capability_id": {
                "type": "string",
                "description": "Unique identifier for this capability"
              },
              "capability_name": {
                "type": "string",
                "description": "Human-readable capability name"
              },
              "description": {
                "type": "string",
                "maxLength": 1000,
                "description": "Description of what this capability provides"
              },
              "category": {
                "type": "string",
                "enum": ["trend_consumption", "content_generation", "content_validation", "trend_analysis"],
                "description": "Category of capability"
              },
              "input_schema_ref": {
                "type": "string",
                "description": "Reference to input schema (JSON Schema URI or identifier)"
              },
              "output_schema_ref": {
                "type": "string",
                "description": "Reference to output schema (JSON Schema URI or identifier)"
              },
              "estimated_duration_ms": {
                "type": "integer",
                "minimum": 0,
                "description": "Estimated execution duration in milliseconds"
              },
              "requires_approval": {
                "type": "boolean",
                "description": "Whether this capability requires human approval"
              }
            }
          }
        },
        "input_schemas": {
          "type": "object",
          "description": "Map of capability_id to JSON Schema definitions",
          "additionalProperties": {
            "type": "object"
          }
        },
        "output_schemas": {
          "type": "object",
          "description": "Map of capability_id to JSON Schema definitions",
          "additionalProperties": {
            "type": "object"
          }
        }
      }
    },
    "status": {
      "type": "object",
      "required": ["current_status", "status_timestamp"],
      "properties": {
        "current_status": {
          "type": "string",
          "enum": ["idle", "busy", "error", "maintenance"],
          "description": "Current operational status"
        },
        "status_timestamp": {
          "type": "string",
          "format": "date-time",
          "description": "ISO 8601 timestamp when status was last updated"
        },
        "status_details": {
          "type": "object",
          "description": "Additional status information",
          "properties": {
            "active_tasks": {
              "type": "integer",
              "minimum": 0,
              "description": "Number of active tasks (required if status is 'busy')"
            },
            "error_code": {
              "type": "string",
              "description": "Error code (required if status is 'error')"
            },
            "error_message": {
              "type": "string",
              "description": "Error message (required if status is 'error')"
            },
            "maintenance_until": {
              "type": "string",
              "format": "date-time",
              "description": "Expected maintenance completion time (required if status is 'maintenance')"
            }
          }
        }
      }
    },
    "trust_signals": {
      "type": "object",
      "description": "Trust and reputation information",
      "properties": {
        "reputation_score": {
          "type": "number",
          "minimum": 0.0,
          "maximum": 1.0,
          "description": "Current reputation score"
        },
        "total_collaborations": {
          "type": "integer",
          "minimum": 0,
          "description": "Total number of successful collaborations"
        },
        "success_rate": {
          "type": "number",
          "minimum": 0.0,
          "maximum": 1.0,
          "description": "Success rate of completed collaborations"
        },
        "average_response_time_ms": {
          "type": "integer",
          "minimum": 0,
          "description": "Average response time in milliseconds"
        }
      }
    },
    "resource_limits": {
      "type": "object",
      "description": "Current resource constraints",
      "properties": {
        "max_concurrent_tasks": {
          "type": "integer",
          "minimum": 1,
          "description": "Maximum number of concurrent tasks"
        },
        "current_task_count": {
          "type": "integer",
          "minimum": 0,
          "description": "Current number of active tasks"
        },
        "rate_limit_per_minute": {
          "type": "integer",
          "minimum": 1,
          "description": "Maximum requests per minute"
        }
      }
    },
    "published_at": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp when this identity was published"
    }
  }
}
```

**Example:**

```json
{
  "agent_id": "550e8400-e29b-41d4-a716-446655440000",
  "agent_name": "chimera-content-node-001",
  "agent_type": "autonomous_content_node",
  "version": "1.0.0",
  "spec_version": "1.0.0",
  "capabilities": {
    "advertised_capabilities": [
      {
        "capability_id": "consume_trends",
        "capability_name": "Trend Consumption",
        "description": "Accepts trend data from other agents for content planning",
        "category": "trend_consumption",
        "input_schema_ref": "chimera://schemas/trend_consumption_input",
        "output_schema_ref": "chimera://schemas/trend_consumption_output",
        "estimated_duration_ms": 5000,
        "requires_approval": false
      },
      {
        "capability_id": "generate_content_plan",
        "capability_name": "Content Plan Generation",
        "description": "Generates content plans based on trend analysis",
        "category": "content_generation",
        "input_schema_ref": "chimera://schemas/content_plan_input",
        "output_schema_ref": "chimera://schemas/content_plan_output",
        "estimated_duration_ms": 30000,
        "requires_approval": false
      }
    ],
    "input_schemas": {
      "consume_trends": {
        "type": "object",
        "required": ["trends"],
        "properties": {
          "trends": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["trend_id", "title", "source", "relevance_score"],
              "properties": {
                "trend_id": {"type": "string", "format": "uuid"},
                "title": {"type": "string"},
                "source": {"type": "string"},
                "relevance_score": {"type": "number", "minimum": 0.0, "maximum": 1.0}
              }
            }
          }
        }
      }
    },
    "output_schemas": {
      "consume_trends": {
        "type": "object",
        "required": ["status", "trends_accepted"],
        "properties": {
          "status": {"type": "string", "enum": ["accepted", "rejected", "partial"]},
          "trends_accepted": {"type": "integer", "minimum": 0},
          "rejection_reasons": {
            "type": "array",
            "items": {"type": "string"}
          }
        }
      }
    }
  },
  "status": {
    "current_status": "idle",
    "status_timestamp": "2026-02-06T16:00:00Z"
  },
  "trust_signals": {
    "reputation_score": 0.92,
    "total_collaborations": 150,
    "success_rate": 0.96,
    "average_response_time_ms": 3500
  },
  "resource_limits": {
    "max_concurrent_tasks": 5,
    "current_task_count": 0,
    "rate_limit_per_minute": 20
  },
  "published_at": "2026-02-06T16:00:00Z"
}
```

---

## Status Reporting Protocol

### Status Update Message

Chimera MUST publish status updates when operational state changes.

**Schema:**

```json
{
  "type": "object",
  "required": ["agent_id", "status_update", "correlation_id", "timestamp"],
  "properties": {
    "agent_id": {
      "type": "string",
      "format": "uuid",
      "description": "Identifier of the agent reporting status"
    },
    "status_update": {
      "type": "object",
      "required": ["current_status", "status_timestamp"],
      "properties": {
        "current_status": {
          "type": "string",
          "enum": ["idle", "busy", "error", "maintenance"],
          "description": "New operational status"
        },
        "status_timestamp": {
          "type": "string",
          "format": "date-time",
          "description": "ISO 8601 timestamp when status changed"
        },
        "status_details": {
          "type": "object",
          "description": "Status-specific details",
          "properties": {
            "active_tasks": {
              "type": "integer",
              "minimum": 0,
              "description": "Number of active tasks (required if status is 'busy')"
            },
            "error_code": {
              "type": "string",
              "description": "Error code (required if status is 'error')"
            },
            "error_message": {
              "type": "string",
              "description": "Human-readable error message (required if status is 'error')"
            },
            "error_type": {
              "type": "string",
              "enum": ["transient", "permanent"],
              "description": "Whether error is transient or permanent (required if status is 'error')"
            },
            "maintenance_until": {
              "type": "string",
              "format": "date-time",
              "description": "Expected maintenance completion time (required if status is 'maintenance')"
            },
            "maintenance_reason": {
              "type": "string",
              "description": "Reason for maintenance (optional if status is 'maintenance')"
            }
          }
        },
        "previous_status": {
          "type": "string",
          "enum": ["idle", "busy", "error", "maintenance"],
          "description": "Previous status before this update"
        }
      }
    },
    "correlation_id": {
      "type": "string",
      "format": "uuid",
      "description": "Correlation identifier for tracing this status update"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp when status update message was created"
    }
  }
}
```

**Example - Status: Idle:**

```json
{
  "agent_id": "550e8400-e29b-41d4-a716-446655440000",
  "status_update": {
    "current_status": "idle",
    "status_timestamp": "2026-02-06T16:05:00Z",
    "previous_status": "busy"
  },
  "correlation_id": "660e8400-e29b-41d4-a716-446655440001",
  "timestamp": "2026-02-06T16:05:00Z"
}
```

**Example - Status: Busy:**

```json
{
  "agent_id": "550e8400-e29b-41d4-a716-446655440000",
  "status_update": {
    "current_status": "busy",
    "status_timestamp": "2026-02-06T16:10:00Z",
    "status_details": {
      "active_tasks": 3
    },
    "previous_status": "idle"
  },
  "correlation_id": "770e8400-e29b-41d4-a716-446655440002",
  "timestamp": "2026-02-06T16:10:00Z"
}
```

**Example - Status: Error:**

```json
{
  "agent_id": "550e8400-e29b-41d4-a716-446655440000",
  "status_update": {
    "current_status": "error",
    "status_timestamp": "2026-02-06T16:15:00Z",
    "status_details": {
      "error_code": "EXTERNAL_SERVICE_UNAVAILABLE",
      "error_message": "Trend aggregation service returned 503",
      "error_type": "transient"
    },
    "previous_status": "busy"
  },
  "correlation_id": "880e8400-e29b-41d4-a716-446655440003",
  "timestamp": "2026-02-06T16:15:00Z"
}
```

**Example - Status: Maintenance:**

```json
{
  "agent_id": "550e8400-e29b-41d4-a716-446655440000",
  "status_update": {
    "current_status": "maintenance",
    "status_timestamp": "2026-02-06T16:20:00Z",
    "status_details": {
      "maintenance_until": "2026-02-06T17:00:00Z",
      "maintenance_reason": "Scheduled specification update"
    },
    "previous_status": "idle"
  },
  "correlation_id": "990e8400-e29b-41d4-a716-446655440004",
  "timestamp": "2026-02-06T16:20:00Z"
}
```

### Status Reporting Requirements

1. **Status Transitions**: Chimera MUST publish status updates within 5 seconds of state changes
2. **Periodic Heartbeat**: When status is 'idle' or 'busy', Chimera MUST publish status updates at least every 60 seconds
3. **Error Recovery**: When recovering from 'error' status, Chimera MUST publish status update with new status
4. **Maintenance Windows**: Chimera MUST publish 'maintenance' status before planned maintenance and 'idle' status after completion

---

## Trust and Reputation Signals

### Reputation Update Message

Chimera MUST publish reputation updates after completing collaborations.

**Schema:**

```json
{
  "type": "object",
  "required": ["agent_id", "reputation_update", "correlation_id", "timestamp"],
  "properties": {
    "agent_id": {
      "type": "string",
      "format": "uuid",
      "description": "Identifier of the agent publishing reputation update"
    },
    "reputation_update": {
      "type": "object",
      "required": ["update_type", "reputation_score", "update_timestamp"],
      "properties": {
        "update_type": {
          "type": "string",
          "enum": ["collaboration_completed", "collaboration_failed", "periodic_update"],
          "description": "Type of reputation update"
        },
        "reputation_score": {
          "type": "number",
          "minimum": 0.0,
          "maximum": 1.0,
          "description": "Updated reputation score"
        },
        "update_timestamp": {
          "type": "string",
          "format": "date-time",
          "description": "ISO 8601 timestamp when reputation was calculated"
        },
        "metrics": {
          "type": "object",
          "description": "Reputation calculation metrics",
          "properties": {
            "total_collaborations": {
              "type": "integer",
              "minimum": 0,
              "description": "Total number of collaborations"
            },
            "successful_collaborations": {
              "type": "integer",
              "minimum": 0,
              "description": "Number of successful collaborations"
            },
            "failed_collaborations": {
              "type": "integer",
              "minimum": 0,
              "description": "Number of failed collaborations"
            },
            "success_rate": {
              "type": "number",
              "minimum": 0.0,
              "maximum": 1.0,
              "description": "Success rate"
            },
            "average_response_time_ms": {
              "type": "integer",
              "minimum": 0,
              "description": "Average response time in milliseconds"
            },
            "on_time_completion_rate": {
              "type": "number",
              "minimum": 0.0,
              "maximum": 1.0,
              "description": "Rate of on-time completions"
            }
          }
        },
        "collaboration_id": {
          "type": "string",
          "format": "uuid",
          "description": "Identifier of collaboration that triggered this update (required if update_type is 'collaboration_completed' or 'collaboration_failed')"
        }
      }
    },
    "correlation_id": {
      "type": "string",
      "format": "uuid",
      "description": "Correlation identifier for tracing this reputation update"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp when reputation update message was created"
    }
  }
}
```

**Example - Collaboration Completed:**

```json
{
  "agent_id": "550e8400-e29b-41d4-a716-446655440000",
  "reputation_update": {
    "update_type": "collaboration_completed",
    "reputation_score": 0.93,
    "update_timestamp": "2026-02-06T16:25:00Z",
    "metrics": {
      "total_collaborations": 151,
      "successful_collaborations": 145,
      "failed_collaborations": 6,
      "success_rate": 0.96,
      "average_response_time_ms": 3450,
      "on_time_completion_rate": 0.94
    },
    "collaboration_id": "aa0e8400-e29b-41d4-a716-446655440005"
  },
  "correlation_id": "bb0e8400-e29b-41d4-a716-446655440006",
  "timestamp": "2026-02-06T16:25:00Z"
}
```

**Example - Periodic Update:**

```json
{
  "agent_id": "550e8400-e29b-41d4-a716-446655440000",
  "reputation_update": {
    "update_type": "periodic_update",
    "reputation_score": 0.92,
    "update_timestamp": "2026-02-06T17:00:00Z",
    "metrics": {
      "total_collaborations": 150,
      "successful_collaborations": 144,
      "failed_collaborations": 6,
      "success_rate": 0.96,
      "average_response_time_ms": 3500,
      "on_time_completion_rate": 0.93
    }
  },
  "correlation_id": "cc0e8400-e29b-41d4-a716-446655440007",
  "timestamp": "2026-02-06T17:00:00Z"
}
```

### Trust Signal Requirements

1. **Reputation Calculation**: Reputation score MUST be calculated using: `(success_rate * 0.6) + (on_time_completion_rate * 0.3) + (response_time_score * 0.1)` where response_time_score is normalized based on average_response_time_ms
2. **Update Frequency**: Reputation updates MUST be published after each collaboration completion and at least every 24 hours
3. **Historical Data**: Reputation calculations MUST use data from the last 100 collaborations or all collaborations if fewer than 100

---

## Collaboration Request Protocol

### Collaboration Request Message

Other agents request collaboration by sending collaboration requests.

**Schema:**

```json
{
  "type": "object",
  "required": ["request_id", "requester_agent_id", "capability_id", "input_data", "correlation_id", "timestamp"],
  "properties": {
    "request_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier for this collaboration request"
    },
    "requester_agent_id": {
      "type": "string",
      "format": "uuid",
      "description": "Identifier of the agent making this request"
    },
    "capability_id": {
      "type": "string",
      "description": "Identifier of the capability being requested"
    },
    "input_data": {
      "type": "object",
      "description": "Input data for the capability (must conform to capability input schema)",
      "additionalProperties": true
    },
    "correlation_id": {
      "type": "string",
      "format": "uuid",
      "description": "Correlation identifier for tracing this request"
    },
    "idempotency_key": {
      "type": "string",
      "description": "Optional idempotency key for retry-safe requests"
    },
    "deadline": {
      "type": "string",
      "format": "date-time",
      "description": "Optional deadline for request completion"
    },
    "priority": {
      "type": "integer",
      "minimum": 1,
      "maximum": 10,
      "description": "Request priority (1 = highest, 10 = lowest)"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp when request was created"
    }
  }
}
```

**Example:**

```json
{
  "request_id": "dd0e8400-e29b-41d4-a716-446655440008",
  "requester_agent_id": "ee0e8400-e29b-41d4-a716-446655440009",
  "capability_id": "consume_trends",
  "input_data": {
    "trends": [
      {
        "trend_id": "ff0e8400-e29b-41d4-a716-446655440010",
        "title": "AI Agent Collaboration Protocols",
        "source": "openclaw",
        "relevance_score": 0.85,
        "observed_at": "2026-02-06T12:00:00Z"
      }
    ]
  },
  "correlation_id": "110e8400-e29b-41d4-a716-446655440011",
  "idempotency_key": "trend_consume_2026-02-06_16:30:00",
  "deadline": "2026-02-06T17:00:00Z",
  "priority": 3,
  "timestamp": "2026-02-06T16:30:00Z"
}
```

### Collaboration Response Message

Chimera responds to collaboration requests with acceptance or rejection.

**Schema:**

```json
{
  "type": "object",
  "required": ["request_id", "responder_agent_id", "response_status", "correlation_id", "timestamp"],
  "properties": {
    "request_id": {
      "type": "string",
      "format": "uuid",
      "description": "Identifier matching the collaboration request"
    },
    "responder_agent_id": {
      "type": "string",
      "format": "uuid",
      "description": "Identifier of Chimera agent responding"
    },
    "response_status": {
      "type": "string",
      "enum": ["accepted", "rejected", "deferred"],
      "description": "Status of the collaboration request"
    },
    "correlation_id": {
      "type": "string",
      "format": "uuid",
      "description": "Correlation identifier matching the request"
    },
    "collaboration_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier for this collaboration (required if response_status is 'accepted')"
    },
    "rejection_reason": {
      "type": "object",
      "description": "Reason for rejection (required if response_status is 'rejected')",
      "required": ["code", "message"],
      "properties": {
        "code": {
          "type": "string",
          "enum": ["capability_not_available", "invalid_input", "resource_exhausted", "policy_violation", "deadline_too_soon"],
          "description": "Machine-readable rejection code"
        },
        "message": {
          "type": "string",
          "description": "Human-readable rejection message"
        },
        "details": {
          "type": "object",
          "description": "Optional additional rejection context",
          "additionalProperties": true
        }
      }
    },
    "deferred_until": {
      "type": "string",
      "format": "date-time",
      "description": "When request will be reconsidered (required if response_status is 'deferred')"
    },
    "estimated_completion": {
      "type": "string",
      "format": "date-time",
      "description": "Estimated completion time (optional if response_status is 'accepted')"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp when response was created"
    }
  }
}
```

**Example - Accepted:**

```json
{
  "request_id": "dd0e8400-e29b-41d4-a716-446655440008",
  "responder_agent_id": "550e8400-e29b-41d4-a716-446655440000",
  "response_status": "accepted",
  "correlation_id": "110e8400-e29b-41d4-a716-446655440011",
  "collaboration_id": "220e8400-e29b-41d4-a716-446655440012",
  "estimated_completion": "2026-02-06T16:35:00Z",
  "timestamp": "2026-02-06T16:30:05Z"
}
```

**Example - Rejected:**

```json
{
  "request_id": "dd0e8400-e29b-41d4-a716-446655440008",
  "responder_agent_id": "550e8400-e29b-41d4-a716-446655440000",
  "response_status": "rejected",
  "correlation_id": "110e8400-e29b-41d4-a716-446655440011",
  "rejection_reason": {
    "code": "resource_exhausted",
    "message": "Agent is at maximum concurrent task capacity",
    "details": {
      "current_tasks": 5,
      "max_tasks": 5
    }
  },
  "timestamp": "2026-02-06T16:30:05Z"
}
```

**Example - Deferred:**

```json
{
  "request_id": "dd0e8400-e29b-41d4-a716-446655440008",
  "responder_agent_id": "550e8400-e29b-41d4-a716-446655440000",
  "response_status": "deferred",
  "correlation_id": "110e8400-e29b-41d4-a716-446655440011",
  "deferred_until": "2026-02-06T16:35:00Z",
  "timestamp": "2026-02-06T16:30:05Z"
}
```

### Collaboration Result Message

Chimera publishes collaboration results when collaboration completes.

**Schema:**

```json
{
  "type": "object",
  "required": ["collaboration_id", "request_id", "responder_agent_id", "result_status", "correlation_id", "timestamp"],
  "properties": {
    "collaboration_id": {
      "type": "string",
      "format": "uuid",
      "description": "Identifier of this collaboration"
    },
    "request_id": {
      "type": "string",
      "format": "uuid",
      "description": "Identifier of the original collaboration request"
    },
    "responder_agent_id": {
      "type": "string",
      "format": "uuid",
      "description": "Identifier of Chimera agent that completed collaboration"
    },
    "result_status": {
      "type": "string",
      "enum": ["completed", "failed", "cancelled"],
      "description": "Final status of the collaboration"
    },
    "correlation_id": {
      "type": "string",
      "format": "uuid",
      "description": "Correlation identifier matching the request"
    },
    "output_data": {
      "type": "object",
      "description": "Output data from capability execution (required if result_status is 'completed')",
      "additionalProperties": true
    },
    "error": {
      "type": "object",
      "description": "Error details (required if result_status is 'failed')",
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
          "enum": ["transient", "permanent"],
          "description": "Whether error is transient or permanent"
        },
        "details": {
          "type": "object",
          "description": "Optional additional error context",
          "additionalProperties": true
        }
      }
    },
    "execution_duration_ms": {
      "type": "integer",
      "minimum": 0,
      "description": "Actual execution duration in milliseconds"
    },
    "completed_at": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp when collaboration completed"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp when result message was created"
    }
  }
}
```

**Example - Completed:**

```json
{
  "collaboration_id": "220e8400-e29b-41d4-a716-446655440012",
  "request_id": "dd0e8400-e29b-41d4-a716-446655440008",
  "responder_agent_id": "550e8400-e29b-41d4-a716-446655440000",
  "result_status": "completed",
  "correlation_id": "110e8400-e29b-41d4-a716-446655440011",
  "output_data": {
    "status": "accepted",
    "trends_accepted": 1,
    "rejection_reasons": []
  },
  "execution_duration_ms": 3200,
  "completed_at": "2026-02-06T16:33:20Z",
  "timestamp": "2026-02-06T16:33:20Z"
}
```

**Example - Failed:**

```json
{
  "collaboration_id": "220e8400-e29b-41d4-a716-446655440012",
  "request_id": "dd0e8400-e29b-41d4-a716-446655440008",
  "responder_agent_id": "550e8400-e29b-41d4-a716-446655440000",
  "result_status": "failed",
  "correlation_id": "110e8400-e29b-41d4-a716-446655440011",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Input data does not conform to capability input schema",
    "error_type": "permanent",
    "details": {
      "validation_errors": [
        "trends[0].relevance_score must be between 0.0 and 1.0"
      ]
    }
  },
  "execution_duration_ms": 150,
  "completed_at": "2026-02-06T16:30:20Z",
  "timestamp": "2026-02-06T16:30:20Z"
}
```

### Collaboration Protocol Requirements

1. **Request Validation**: Chimera MUST validate collaboration requests against capability input schemas before acceptance
2. **Response Timing**: Chimera MUST respond to collaboration requests within 10 seconds
3. **Idempotency**: Requests with the same `idempotency_key` from the same `requester_agent_id` within 24 hours MUST return the same collaboration result
4. **Deadline Handling**: If `deadline` is provided and cannot be met, Chimera MUST reject the request with `deadline_too_soon` rejection code
5. **Status Updates**: When accepting a collaboration, Chimera MUST update status to 'busy' if transitioning from 'idle'
6. **Result Publishing**: Chimera MUST publish collaboration results within 5 seconds of completion
7. **Reputation Updates**: After collaboration completion, Chimera MUST publish reputation update

---

## Protocol Conformance

### Message Validation

All protocol messages MUST:
1. Conform to the JSON schemas defined in this document
2. Include all required fields
3. Validate field types and constraints
4. Include valid UUIDs for identifier fields
5. Include valid ISO 8601 timestamps for date-time fields

### Protocol Versioning

1. All protocol messages MUST include a `protocol_version` field (if supported by transport)
2. Protocol version format: `"protocol_version": "1.0.0"` (semantic versioning)
3. Backward-incompatible protocol changes require version increment
4. Chimera MUST support the protocol version specified in its agent identity

### Error Handling

1. **Invalid Messages**: Messages that do not conform to schemas MUST be rejected with validation error
2. **Unknown Capabilities**: Requests for unknown capabilities MUST be rejected with `capability_not_available` code
3. **Transport Errors**: Transport-level errors (network failures, timeouts) are handled by transport layer, not protocol layer
4. **Retry Guidance**: Error responses MUST include `retryable` flag and `retry_after_seconds` when applicable

---

## Conformance Requirements

All Chimera implementations MUST:

1. Publish agent identity with capability advertisement on startup
2. Update agent identity when capabilities change
3. Publish status updates according to status reporting requirements
4. Publish reputation updates according to trust signal requirements
5. Process collaboration requests according to collaboration protocol requirements
6. Validate all incoming protocol messages against schemas
7. Include correlation identifiers in all protocol messages
8. Support idempotency keys in collaboration requests
9. Never expose sensitive information (credentials, internal system details) in protocol messages

Deviations from this protocol specification MUST be documented as specification updates before implementation.
