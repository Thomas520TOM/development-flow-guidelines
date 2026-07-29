---
name: coding-guidelines
description: Full development lifecycle guidance covering requirements, design, implementation, testing, code review, security audit, and maintenance. Activates on any programming task — the AI infers your current stage from natural conversation and loads the appropriate rules on demand.
allowed-tools: ["Bash", "Read", "Write", "Edit", "Glob", "Grep"]
---

# Coding Work Guidance

## Overview

This is a comprehensive development methodology system. It is NOT loaded all at once — the AI detects which stage you are in (requirements, design, learning, coding, reviewing, debugging) and applies only the relevant rules. All modules are located in the skill root directory.

## Core Principles (Always Active)

These apply regardless of which module is active:

- **Present options, do not decide unilaterally**: When recommending technology or approaches, show multiple options with pros/cons and let the user choose.
- **Explain the why**: For key decisions, provide brief reasoning. Do not lecture unless asked.
- **Precise change scope**: Before modifying code, declare what will change and the impact scope. Get confirmation before executing.
- **Conversational tone**: Communicate as an experienced colleague, not a bureaucratic report generator.
- **Respect thinking space**: Leave room for the user to add their own thoughts and adjustments.

## Workflow

The standard lifecycle flow, with each module loaded on demand based on the user's natural language:

1. **Requirements Analysis** (`03-project-setup/01-requirements-analysis.md`) — When user describes vague ideas or "want to build X". Outputs: module list, boundaries, blind spots.

2. **Technical Design** (`03-project-setup/02-technical-design.md`) — When user discusses technology choices, architecture, or "how to structure this". Outputs: architecture, function list, data flow design.

3. **Skill Dictionary** (`02-skill-dictionary/index.md`) — When user asks "how to implement" or "best approach for X". Contains pre-built technology selection matrices (frameworks, state management, CSS, backend, databases, testing tools, package managers).

4. **Testing Strategy** (`07-testing-strategy/rules.md`) — A gate before code generation. Defines test plans, coverage standards (80%+ lines, 75%+ branches), and test type selection (unit/integration/E2E). RED-GREEN-REFACTOR cycle enforced.

5. **Code Generation** (`01-code-generation/rules.md`) — When user says "implement it" or "write the code". Step-by-step execution with confirmation gates. Readability standards, error handling, edge case requirements.

6. **Code Review** (`08-code-review/rules.md`) — Structured 6-dimension review: functionality, design, readability, testing, security, performance. Severity-ranked findings (Critical/High/Medium/Low).

7. **Security Review** (`09-security-review/rules.md`) — 7-dimension audit: input validation, injection prevention, authentication, authorization, data protection, dependency security, configuration security.

8. **Post-Deployment Maintenance** (`04-maintenance/rules.md`) — 6-layer bug investigation system (surface/type/logic/state/boundary/environment). Minimal changes principle, rollback protection.

9. **Evaluation** (`06-evaluation/system.md`) — Senior-engineer mentoring perspective. 2-3 issues per session, affirm-then-critique structure.

## Cross-Cutting Modules

- **Log Memory** (`05-log-memory/system.md`) — Append-only logging for cross-conversation context. Decision-focused entries (max 5 lines). Checkpoints for resumability.
- **Context Management** (`context-management.md`) — Auto-summarizes at 20+ turns. Preserves decisions, discards exploration.
- **Error Recovery** (`error-recovery.md`) — Checkpoint system, breakpoint detection, graceful degradation on failure.
- **Progress Tracking** (`progress-tracking.md`) — Percentage estimates, milestone reporting, stage completion status.
- **Extension Interface** (`extension-interface.md`) — Spec for registering custom modules with hook points.

## Behavior When Uncertain

If the AI cannot determine the current stage:
- New project, no logs → start from requirements analysis
- Existing project with logs → read logs and continue from last recorded stage
- Direct code request with clear requirements → go straight to code generation (testing gate still applies)

## Non-Standard Flows

- Skip ahead: user can write code directly without going through preceding stages
- Mid-session learning: switch to skill dictionary, then return to coding
- Review anytime: trigger code review or evaluation at any point
- Fix only: existing project issues → maintenance module directly
- Audit only: security review on existing code without other stages
