# Project Chimera – Tooling Strategy

## Purpose

This document defines the developer tooling strategy for Project Chimera. It explains the distinction between development-time MCP tools and runtime agent capabilities, justifies tooling choices, and describes how tooling supports the project's traceability and auditability requirements.

This document focuses on strategy and justification, not implementation details or runtime logic.

---

## MCP Developer Tools vs Runtime Agent Skills

### Fundamental Distinction

**MCP Developer Tools** are development-time utilities that assist human developers and AI coding assistants (like Cursor) in building, testing, and maintaining the Chimera system. These tools operate **outside** the runtime system and have no direct impact on agent behavior.

**Runtime Agent Skills** are capabilities that Chimera's agents (Planner, Worker, Governor) use during system operation. These are defined in specifications, implemented as code, and executed by agents to accomplish their tasks.

### MCP Developer Tools

**Purpose:** Enhance developer productivity and ensure specification compliance during development.

**Characteristics:**
- Used by developers and AI coding assistants (Cursor)
- Operate at development time, not runtime
- Provide capabilities like file system access, git operations, code search
- Enable traceability of development activities
- Do not execute as part of the Chimera runtime system

**Examples:**
- Git MCP server: Commit code, view history, create branches
- Filesystem MCP server: Read/write files, navigate directories
- Telemetry MCP server: Track development metrics, code changes

**Governance:** Developer tools are governed by development workflows, not runtime governance policies. However, their usage is logged for auditability.

### Runtime Agent Skills

**Purpose:** Provide executable capabilities that agents use to accomplish their assigned tasks.

**Characteristics:**
- Defined in `specs/functional.md` and `specs/technical.md`
- Implemented as code that agents invoke
- Execute within the Chimera runtime system
- Subject to governance policies and boundary enforcement
- Logged to `skill_invocations` table for auditability

**Examples:**
- `fetch_trends_from_openclaw`: Worker Agent skill for retrieving trend data
- `draft_content_from_trends`: Worker Agent skill for content generation
- `validate_output`: Governor Agent skill for policy validation

**Governance:** Skills are governed by runtime policies, capability boundaries, and approval workflows as defined in `specs/_meta.md`.

### Why This Distinction Matters

1. **Separation of Concerns:** Development tooling and runtime capabilities serve different purposes and operate in different contexts.

2. **Security Boundaries:** Developer tools may have broader access (e.g., full repository access) than runtime skills, which operate within strict capability boundaries.

3. **Traceability Requirements:** Development activities and runtime activities require different traceability mechanisms. Developer tool usage is tracked for development auditability; runtime skill invocations are tracked for operational auditability.

4. **Specification Authority:** Runtime skills MUST be defined in specifications before implementation. Developer tools are infrastructure choices that support the development process but are not themselves specified as system capabilities.

---

## Development MCP Servers

### Git MCP Server

**Purpose:** Enable version control operations during development.

**Capabilities:**
- Commit code changes
- View git history and diffs
- Create and manage branches
- Tag releases
- View repository status

**Justification:**
- **Specification Conformance:** `specs/_meta.md` requires that "Governance policies, agent specifications, and system configurations MUST be version-controlled and traceable to specific deployments." Git MCP enables this requirement.

- **Traceability:** Git commits provide immutable history of specification and code changes. Each commit can be traced to specific specification versions.

- **Collaboration:** Enables multiple developers and AI assistants to work on the same codebase with conflict resolution and history tracking.

- **Auditability:** Git history provides audit trail of who changed what and when, supporting governance requirements for traceability.

**Usage Context:** Used by developers and AI coding assistants when making code changes. Not used by runtime agents.

### Filesystem MCP Server

**Purpose:** Enable file system operations during development.

**Capabilities:**
- Read specification files
- Write code files
- Navigate directory structure
- Search file contents
- Create and delete files

**Justification:**
- **Specification Access:** Developers and AI assistants need to read specifications before implementing code, per the Prime Directive in `.cursor/rules/agent.mdc`.

- **Code Generation:** Enables writing implementation code that conforms to specifications.

- **Specification Updates:** When specifications need updates, filesystem access enables modifying spec files before code changes.

- **Test File Management:** Enables creating and managing test files that verify specification conformance.

**Usage Context:** Used extensively during development for reading specs, writing code, and managing test files. Not used by runtime agents.

### Telemetry MCP Server

**Purpose:** Track development metrics and code changes for analysis.

**Capabilities:**
- Track code change frequency
- Monitor specification update patterns
- Measure development velocity
- Analyze test coverage trends
- Track AI assistant usage patterns

**Justification:**
- **Process Improvement:** Telemetry enables understanding of development patterns, identifying bottlenecks, and improving the spec-driven development workflow.

- **Quality Metrics:** Tracks metrics like time between spec updates and implementation, test coverage growth, and specification compliance rates.

- **Resource Planning:** Provides data for planning development resources and identifying areas needing more specification clarity.

**Usage Context:** Passive monitoring during development. Does not interfere with development workflow. Not used by runtime agents.

---

## MCP Sense: Mandatory Traceability Layer

### What is MCP Sense

MCP Sense (Tenx MCP Sense) is a telemetry and traceability system that operates as a "black box" recorder of development activities. It captures development-time events without requiring explicit instrumentation in code.

### Why MCP Sense is Mandatory

#### 1. Specification-Driven Development Compliance

**Requirement:** The Prime Directive in `.cursor/rules/agent.mdc` requires that code never be written without first checking specifications. MCP Sense provides independent verification that this requirement is being followed.

**Mechanism:** MCP Sense tracks file access patterns, enabling verification that specification files were read before code files were modified.

**Justification:** Without independent verification, there is no way to ensure that developers and AI assistants are following the mandatory specification review workflow. MCP Sense provides this verification layer.

#### 2. Traceability Requirements

**Requirement:** `specs/_meta.md` states: "All agent decisions, content generation requests, and governance actions MUST be logged with sufficient context for audit and debugging."

**Development Context:** While runtime activities are logged to the database, development activities (specification updates, code changes, test creation) also require traceability for:
- Understanding why specifications changed
- Tracing code changes back to specification requirements
- Auditing development decisions

**Mechanism:** MCP Sense captures development events (file reads, writes, git operations) with timestamps and context, providing an immutable audit trail.

**Justification:** Development traceability is necessary to understand the evolution of the system and verify that all code changes are properly justified by specification updates.

#### 3. Governance Verification

**Requirement:** `specs/_meta.md` requires: "Code implementations MUST be verifiable against their corresponding specifications through automated tests or formal verification."

**Development Context:** Governance requires that:
- Specification changes precede code changes
- Code changes reference specific specification sections
- Tests verify specification conformance

**Mechanism:** MCP Sense enables post-hoc analysis of development patterns to verify governance compliance. It can detect patterns like:
- Code changes without preceding spec reads
- Spec changes without corresponding test updates
- Implementation patterns that deviate from specifications

**Justification:** Governance requirements cannot be enforced solely through runtime checks. Development-time governance requires independent monitoring, which MCP Sense provides.

#### 4. Black Box Recording

**Principle:** MCP Sense operates as a "black box" recorder, meaning it captures events without requiring developers to explicitly log them.

**Advantages:**
- **Non-Intrusive:** Does not require code changes or explicit logging statements
- **Comprehensive:** Captures all development activities automatically
- **Impartial:** Provides objective record of what actually happened, not what developers intended
- **Retrospective Analysis:** Enables analysis of development patterns after the fact

**Justification:** Explicit logging of development activities would be burdensome and error-prone. Black box recording ensures complete traceability without developer overhead.

#### 5. Audit Trail for Compliance

**Requirement:** Project Chimera must demonstrate compliance with specification-driven development principles for governance and quality assurance.

**Mechanism:** MCP Sense provides an audit trail that can be reviewed to verify:
- That specifications were consulted before code changes
- That code changes align with specification updates
- That development follows defined workflows

**Justification:** External stakeholders, auditors, or governance bodies may require evidence of development practices. MCP Sense provides this evidence without requiring manual documentation.

---

## Tooling Support for Traceability and Auditability

### Development-Time Traceability

**Git MCP Server:**
- **Traceability:** Git commits provide immutable history linking code changes to commits, authors, and timestamps
- **Auditability:** Git history enables auditing who made what changes and when
- **Specification Linking:** Commit messages can reference specification sections, creating traceability between specs and code

**Filesystem MCP Server:**
- **Traceability:** File access patterns tracked by MCP Sense show which specifications were read before code changes
- **Auditability:** File modification timestamps provide chronological record of development activities
- **Specification Compliance:** Enables verification that code files were created/modified after specification files were accessed

**Telemetry MCP Server:**
- **Traceability:** Tracks development metrics over time, showing evolution of codebase and specification compliance
- **Auditability:** Provides quantitative data on development practices (e.g., spec-to-code lag time, test coverage trends)
- **Pattern Detection:** Enables identification of development patterns that may indicate specification drift or non-compliance

**MCP Sense:**
- **Traceability:** Provides comprehensive black box recording of all development activities
- **Auditability:** Independent verification that development workflows are being followed
- **Governance Verification:** Enables post-hoc verification of governance compliance

### Runtime Traceability (Not Tooling, but Context)

While runtime traceability is implemented in code (not tooling), it's important to understand how development tooling supports runtime traceability requirements:

**Database Logging:**
- Runtime activities are logged to database tables (`audit_logs`, `agent_executions`, `skill_invocations`)
- Development tooling enables writing code that implements this logging correctly
- Git history traces when logging code was added/modified

**Specification Compliance:**
- Runtime traceability requirements are defined in `specs/technical.md`
- Development tooling enables reading these specifications and implementing compliant logging
- MCP Sense verifies that logging code was written after specification review

### Auditability Chain

The complete auditability chain spans from development to runtime:

1. **Specification Definition:** Specifications define traceability requirements
2. **Code Implementation:** Developer tools enable writing code that implements traceability
3. **Development Audit:** MCP Sense verifies that development followed specifications
4. **Runtime Execution:** Runtime code implements traceability as specified
5. **Runtime Audit:** Database logs provide runtime traceability records

**Tooling Role:** Developer tools (Git, Filesystem, Telemetry, MCP Sense) support steps 1-3. Runtime code (not tooling) implements steps 4-5, but tooling enables writing that code correctly.

---

## Tooling Selection Principles

### Principle 1: Separation of Development and Runtime

Developer tools operate in development context and do not execute in runtime. This separation ensures that:
- Development tools can have broader capabilities without compromising runtime security
- Runtime agents operate within strict boundaries defined in specifications
- Development activities and runtime activities are traceable separately

### Principle 2: Specification Authority

All tooling choices must support the specification-driven development workflow:
- Tools must enable reading specifications before code changes
- Tools must enable writing code that conforms to specifications
- Tools must enable verification of specification compliance

### Principle 3: Mandatory Traceability

All tooling must support traceability requirements:
- Development activities must be traceable (Git, MCP Sense)
- Tool usage must be auditable (Telemetry, MCP Sense)
- Tool choices must be justifiable (this document)

### Principle 4: Non-Intrusive Monitoring

Tooling should not burden developers:
- MCP Sense operates as black box recorder (no explicit logging required)
- Telemetry is passive (does not interrupt workflow)
- Git and Filesystem tools are standard development utilities

### Principle 5: Governance Support

Tooling must support governance requirements:
- Enable verification of specification-driven development compliance
- Provide audit trails for development decisions
- Support post-hoc analysis of development patterns

---

## Conclusion

The tooling strategy for Project Chimera is designed to support specification-driven development while ensuring traceability and auditability. The distinction between MCP Developer Tools (development-time) and Runtime Agent Skills (runtime) is fundamental to maintaining proper separation of concerns and security boundaries.

MCP Sense is mandatory because it provides independent verification of governance compliance and comprehensive traceability of development activities. Without MCP Sense, there would be no way to verify that the Prime Directive (specification review before code) is being followed, and no independent audit trail of development decisions.

All tooling choices are justified by their support for:
1. Specification-driven development workflow
2. Traceability requirements
3. Governance verification
4. Auditability needs

This tooling strategy enables Project Chimera to maintain its commitment to infrastructure readiness, predictable behavior, and operational safety through proper development practices and comprehensive traceability.
