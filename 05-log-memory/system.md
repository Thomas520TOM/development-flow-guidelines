---
title: Log Memory System
description: An append-only logging system that dynamically records requirements, architecture, and implementation paths in conversation order
version: "2.0.0"
module_id: 05-log-memory
category: system
depends_on: []
inputs:
  - field: module_output
    description: "Output from any lifecycle module to record"
    required: false
  - field: decision
    description: "Technology or design decision to persist"
    required: false
outputs:
  - field: log_entries
    description: "Append-only log records in instance directory"
    schema: "[{timestamp: string, type: string, summary: string, detail: string}]"
  - field: context_snapshot
    description: "Restorable project state for new conversations"
gates:
  - condition: "log_entry.detail.length <= 500"
    description: "Single log entry detail must not exceed 500 characters"
    on_fail: warn
  - condition: "log_entry.type in valid_types"
    description: "Entry type must be from the defined set"
    on_fail: warn
  - condition: "append_only"
    description: "Existing entries must never be modified"
    on_fail: block
---

# Log Memory System

## Positioning

Similar to a database's append-only log, this system dynamically records key information in chronological order during development, enabling cross-conversation context continuity.

## Instantiation Mechanism

This skill uses a template-instance architecture. Log files are the core data of instances; each project has its own independent set.

When the AI determines that a new project has started, it should create copies of three log files in the instance directory:

```
instance-directory/
├── 01-requirements-log.md
├── 02-architecture-log.md
└── 03-implementation-log.md
```

The instance directory's naming and location are determined by the AI upon creation (e.g., `C:\Users\<username>\Documents\Codex\instances\<project-name>\` or under the project root directory). All subsequent log append operations in future conversations target files in the instance directory; the template is not modified.

## File Structure

Template log rule files:

```
05-log-memory/
└── system.md                    # This rule file (template, shared by all instances)
```

Instance log data files (one set per project, generated when creating the instance):

```
<instance-directory>/
├── 01-requirements-log.md       # Requirements analysis log
├── 02-architecture-log.md       # Architecture design log
└── 03-implementation-log.md     # Implementation path log
```

## Recording Method

- **Append-only writes**: Previously written historical entries are never modified; only new records are appended. Similar to a database's WAL (Write-Ahead Log).
- **In conversation order**: Logs are arranged in the actual chronological order of conversations, forming a traceable timeline.
- **Silent writes**: The AI appends to logs in real-time without needing to inform the user.
- **Cross-conversation continuity**: At the start of a new conversation, existing logs are loaded to restore context, and appending continues from there.

## Write Timing

Logs are automatically written at the following moments:

1. **Module transitions**: When the current development stage changes, switch to the corresponding log file
    - Requirements analysis ↔ structure design ↔ implementation path ↔ code generation
2. **Topic changes**: When the conversation content clearly shifts to another topic
3. **Key decision confirmations**: The user confirms a technology choice, design decision, or requirements change

## Log File Assignment Rules

Which log file to write to is determined by the current development stage:

| Current Stage | Log File | Example Content |
|---|---|---|
| Requirements Analysis | 01-requirements-log.md | New requirements, requirement changes, boundary definitions |
| Structure Design | 02-architecture-log.md | Module breakdown, interface agreements, data flow design |
| Implementation Path | 03-implementation-log.md | Algorithm choices, library usage, implementation status |
| Testing | 03-implementation-log.md | Test plan summary, coverage results, regression notes |
| Code Review | 03-implementation-log.md | Review findings summary, severity distribution |
| Security Review | 03-implementation-log.md | Security issues found and resolved |
| Maintenance | 03-implementation-log.md | Bug fixes, modification records, rollback points |

If a piece of information pertains to multiple stages simultaneously, it is written to the log file of the currently active stage; the other module needing this information is noted via cross-file reference.

## Log Entry Format

Each log entry follows a uniform format:

```
[YYYY-MM-DD HH:MM] <Entry Type> <Summary>

<Detailed Content>
```

- Date and time reflect when the record was written
- Entry type marks the nature of this log entry (addition, change, deprecation, decision, status update, etc.)
- Summary is a one-sentence overview
- Detailed content provides supplementary explanation

## Log Granularity Standards

To maintain useful logs without bloat:

- **Single entry max length**: 5 lines of detailed content. If more detail is needed, summarize and reference the conversation.
- **Entry frequency**: One entry per significant decision or stage transition. Do not log every minor exchange.
- **What to log**: Decisions and their rationale, confirmed requirements, architecture choices, resolved issues.
- **What not to log**: Code snippets (read from source), trivial clarifications, repeated information, interim exploration that was abandoned.
- **Granularity examples**:

```
CORRECT — Records the decision with rationale:
[2026-07-26 14:30] Decision Chose PostgreSQL over MongoDB
Selected PostgreSQL for the user data store. Rationale: users have relational data
(reviews, orders, profiles need JOINs). MongoDB considered but schema enforcement
requirement favored PostgreSQL.

INCORRECT — Too vague:
[2026-07-26 14:30] Status Update Database chosen

INCORRECT — Too verbose, duplicates code:
[2026-07-26 14:30] Implementation Wrote user controller
Created UserController with the following methods:
async create(req: Request, res: Response) {
  const { name, email } = req.body;
  const user = await db.insert(users).values({ name, email });
  return res.json(user);
}
... (20 more lines)
```

## Integration with Other Modules

- **Evaluation system**: Reads previous critique points from logs to track progress.
- **Project setup**: Loads requirements logs at the start of a new conversation to quickly restore project context.
- **Post-deployment maintenance**: Understands the code evolution history through implementation path logs.
- **Testing strategy**: Test plans and coverage results are recorded in the implementation log.
- **Code review**: Review findings summary is appended to the implementation log.
