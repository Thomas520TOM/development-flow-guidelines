---
title: Error Recovery and Checkpoint Resume
description: Failure handling with checkpoint markers, automatic breakpoint detection, and graceful degradation across module boundaries
version: "2.0.0"
module_id: error-recovery
category: system
depends_on: ["05-log-memory"]
inputs:
  - field: module_failure
    description: "Failed module execution with error details"
    required: true
  - field: log_entries
    description: "Recent log entries to find last checkpoint"
    from: "05-log-memory"
    required: false
outputs:
  - field: checkpoint_marker
    description: "Progress marker written to log on checkpoint or failure"
  - field: recovery_strategy
    description: "Resume point and strategy"
    schema: "{resume_from: string, strategy: 'retry'|'alternative'|'skip'|'escalate', reason: string}"
gates:
  - condition: "retry_count < 3"
    description: "Auto-retry at most twice before escalating"
    on_fail: warn
  - condition: "checkpoint_marker != null"
    description: "Checkpoint must be written on every module boundary"
    on_fail: warn
---

# Error Recovery and Checkpoint Resume

## Positioning

Development work is inherently iterative. Modules may fail mid-execution (user interrupts, external tools error, network timeout). This module ensures the system can recover gracefully from interruptions without losing progress or repeating completed work.

## Trigger Conditions

- Any module execution is interrupted or fails
- The user says "continue", "resume", "pick up where we left off"
- A new conversation starts on an existing project with an in-progress module

## Checkpoint System

### Checkpoint Granularity

Checkpoints are set at module boundaries and within modules at sub-step boundaries:

| Module | Internal Checkpoints |
|--------|---------------------|
| Requirements Analysis | After step 2 (module discovery), after step 4 (blind spot annotation) |
| Technical Design | After step 2 (architecture layering), after step 4 (data flow design) |
| Code Generation | After each file or logical unit is generated and confirmed |
| Testing | After test plan definition, after each test unit completion |
| Code Review | After each dimension review |
| Security Review | After each dimension review |
| Maintenance | After step 3 (modification plan), after step 4 (modifications complete) |

### Checkpoint Marker Format

Appended to implementation log when a checkpoint is reached:

```
[YYYY-MM-DD HH:MM] Checkpoint <module> — <sub-step description>
Status: Complete. Next: <next step description>.
```

### Breakpoint Detection

When resuming after interruption:

1. Read the implementation log and find the most recent `Checkpoint` entry
2. If a checkpoint exists: resume from the `Next:` step
3. If no checkpoint exists but log entries indicate partial progress: resume from the first incomplete step
4. If no log entries at all for this stage: start from the beginning

## Recovery Strategies

### User Interruption

If the user stops mid-flow (changes topic, closes conversation):
- Immediately write a checkpoint marker with current progress
- Log any partial outputs that should be preserved

### External Tool Failure

If a tool command fails (build error, test failure, API timeout):
- Log the failure with the attempted command and error message
- Propose a recovery strategy before retrying
- Do not silently retry more than twice
- After 3 failures, escalate: "This operation has failed 3 times. Options: [a] try alternative approach X, [b] skip and revisit later, [c] investigate root cause."

### Module Rollback

If a module's output is found to be incorrect later in the process:
- Revert affected downstream artifacts only (not upstream)
- Mark the reverted module's checkpoint as `Status: Rolled back. Reason: <reason>.`
- Re-execute the module and all downstream modules affected

## Graceful Degradation

When a module cannot be fully executed (missing information, dependencies unavailable):

1. Execute what is possible and log a degraded completion
2. Record what was skipped and why:
   ```
   [YYYY-MM-DD HH:MM] Degraded <module> completed
   Completed: <what was done>.
   Skipped: <what was skipped> — <reason>.
   Required to proceed: <blocking dependency>.
   ```
3. Allow downstream modules to proceed on a best-effort basis if the degradation is non-blocking

## Integration with Other Modules

- **Log System**: All checkpoint markers and recovery actions are written to the implementation log.
- **Context Management**: After recovery, generate a context snapshot so the next conversation can resume cleanly.
- **Progress Tracking**: Recovery status updates the progress tracker to reflect actual completion state.
