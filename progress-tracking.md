---
title: Progress Tracking
description: Session-level completion state tracking with stage indicators, percentage estimates, and active progress reporting
version: "2.0.0"
module_id: progress-tracking
category: system
depends_on: ["05-log-memory"]
inputs:
  - field: module_completion
    description: "Module completion events from any lifecycle stage"
    required: false
  - field: blockers
    description: "Current blocking items"
    required: false
outputs:
  - field: progress_snapshot
    description: "Overall completion state with stage statuses"
    schema: "{overall_percentage: number, stages: [{id: string, status: 'complete'|'in_progress'|'skipped'|'pending', completed_at?: string}], blockers: [string], next_milestone: string}"
gates:
  - condition: "progress_snapshot.overall_percentage <= 100"
    description: "Percentage must be within valid range"
    on_fail: warn
---

# Progress Tracking

## Positioning

Long projects span multiple conversations and stages. Users may lose track of what is done, what is in progress, and what remains. This module maintains a lightweight progress state that is updated silently and reported on request or at meaningful boundaries.

## Trigger Conditions

Captures state silently at:
- Every stage transition
- Every checkpoint marker
- Every module completion (including degraded)

Reports state actively when:
- A new conversation starts on an existing project
- The user asks "what's the status?", "where are we?", "what's left?"
- A major milestone is reached
- A blocker is resolved

## Progress State Structure

Maintained as a simple data structure, persisted to the implementation log:

```
[Progress Snapshot — YYYY-MM-DD HH:MM]

Project: <name>
Overall: <percentage>% complete

Stages:
  Requirements Analysis:    [COMPLETE]   — <date completed>
  Technical Design:         [COMPLETE]   — <date completed>
  Skill Dictionary:         [SKIPPED]    — <reason>
  Code Generation:          [IN PROGRESS] — <current file/module being written>
  Testing Strategy:         [PENDING]
  Code Review:              [PENDING]
  Security Review:          [PENDING]
  Post-Deployment:          [PENDING]
  Evaluation:               [PENDING]

Blockers: <list of blocking items or "None">
Next Milestone: <next major deliverable>
```

## Percentage Estimation

Percentages are heuristic estimates, not precise measurements:

| Milestone | Cumulative % |
|-----------|-------------|
| Requirements Analysis complete | 15% |
| Technical Design complete | 30% |
| First working prototype (core functionality) | 50% |
| All modules implemented | 70% |
| Tests written and passing | 80% |
| Code review complete, issues resolved | 90% |
| Security review passed | 95% |
| Evaluation feedback incorporated | 100% |

These are defaults. For projects that skip stages, percentages are recalculated proportionally.

## Active Reporting Triggers

Report progress to the user at these moments:

1. **Conversation start**: Brief restoration summary (not full progress report unless user asks)
2. **Stage completion**: "Requirements analysis complete. Design stage next. Overall: 15%."
3. **Blocker resolution**: "Blocker resolved. Resuming implementation. Overall: 50%."
4. **Milestone reached**: "First prototype working. 4 of 8 modules functional. Overall: 50%. Next: remaining modules."
5. **On request**: Full progress snapshot when user asks

## Integration with Other Modules

- **Error Recovery**: Recovery updates the progress state to reflect actual completion.
- **Context Management**: Progress snapshot is included in auto-summarization at 40+ turns.
- **Log System**: Progress snapshots are written to the implementation log.
- **Evaluation System**: Evaluation notes which stages have been reviewed and which still need attention.
