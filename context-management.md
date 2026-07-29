---
title: Context Management
description: Long-conversation handling via auto-summarization, key decision persistence, and context window optimization
version: "2.0.0"
module_id: context-management
category: system
depends_on: ["05-log-memory"]
inputs:
  - field: turn_count
    description: "Current conversation turn count"
    required: true
  - field: log_entries
    description: "Recent log entries for summarization"
    from: "05-log-memory"
    required: false
outputs:
  - field: context_snapshot
    description: "Compressed summary of decisions, open questions, blockers, next steps"
    schema: "{stage: string, decisions: [string], open_questions: [string], blockers: [string], next_steps: [string]}"
gates:
  - condition: "turn_count >= 20"
    description: "Summarization triggers at 20+ turns"
    on_fail: skip
  - condition: "context_snapshot.summary_length <= 500"
    description: "Snapshot must be compact"
    on_fail: warn
---

# Context Management

## Positioning

As conversations stretch beyond 20 turns, context accumulates and the AI may lose track of early decisions or drift from the original plan. This module defines when and how to compress context without losing critical information.

## Trigger Conditions

Activated when:
- Conversation exceeds 20 turns (check after each user response)
- A major stage transition occurs (requirements → design → implementation)
- The conversation topic has shifted significantly and prior context is no longer relevant

## Auto-Summarization

### When to Summarize

| Trigger | Action |
|---------|--------|
| 20 turns reached | Generate a lightweight summary, silently append to log |
| 40 turns reached | Generate a full context snapshot, inform user briefly: "Summarized conversation state for continuity." |
| Stage transition | Summarize the completed stage's decisions before entering the next stage |
| Topic shift | Summarize the previous topic if it contained decisions worth preserving |

### Summary Format

```
[Context Snapshot — YYYY-MM-DD HH:MM]

Active Stage: <requirements|design|implementation|maintenance|review>
Project: <project name>

Decisions Made:
  - <decision 1 with brief rationale>
  - <decision 2 with brief rationale>

Open Questions:
  - <unresolved question>
  - <unresolved question>

Current Blockers: <none or description>

Next Steps:
  1. <immediate next action>
  2. <subsequent action>
```

### What to Preserve vs. Discard

**Always preserve:**
- Confirmed requirements and scope boundaries
- Architecture decisions with rationale
- Technology choices and versions
- Known issues and their status
- User preferences and constraints

**May discard:**
- Exploratory discussion that led nowhere
- Rejected alternatives (unless the user may revisit)
- Minor clarifications and rephrasing
- Implementation details already captured in code
- Repeated information

### Write Destination

Summaries are appended to the appropriate log file:
- Stage completion summary → corresponding stage log
- General conversation summary → implementation log

## Key Decision Persistence

For high-impact decisions, create a persistent record beyond the conversation log:

```
[Decision Record — YYYY-MM-DD]

Decision: <one-line summary>
Context: <what problem this solves>
Alternatives Considered: <options and why rejected>
Consequences: <what changes because of this decision>
Reversible: <yes/no and how to reverse>
```

These records are written to the architecture log and serve as project memory for future conversations.

## Context Restoration

At the start of a new conversation:

1. Read the most recent log entries (last 20 lines from each log file)
2. If a context snapshot exists within the last 3 log entries, present a concise restoration summary:
   ```
   Resuming [project name]. Last stage: [stage]. Key decisions: [list].
   Open items: [list]. Ready to continue?
   ```
3. Do not replay the entire conversation history — the logs are the authoritative record

## Token Budget Awareness

- Summaries should be compact (under 500 characters when possible)
- Do not repeat information already present in log files
- When loading context, prioritize most recent entries first
