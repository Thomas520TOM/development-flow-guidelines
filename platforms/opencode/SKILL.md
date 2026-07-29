---
name: development-flow-guidelines
version: "2.0.0"
maturity: stable
tier: core
token_budget: medium
description: Full development lifecycle guidance system. Covers requirements analysis, technical design, technology selection matrices, TDD workflow, code generation rules, structured code review, security audit, 6-layer bug investigation, append-only logging, context management, error recovery, progress tracking, and an extension interface. The AI infers the current stage from natural conversation — no explicit commands needed.
---

# Coding Work Guidance

## Overview

This is a comprehensive development methodology system covering the full lifecycle: requirements → design → learning → testing → implementation → review → security audit → maintenance → evaluation. Modules are loaded on demand based on the AI inferring your current stage from natural conversation.

## Core Principles (Always Active)

- **Present options, do not decide**: Show multiple approaches with pros/cons. User makes the final call.
- **Explain the why**: Brief rationale for key decisions. No unsolicited lectures.
- **Precise change scope**: Declare what changes and impact before executing. Get confirmation.
- **Conversational, not bureaucratic**: Speak as an experienced colleague, not a report generator.
- **Respect thinking space**: Leave room for user input and adjustments.

## Stage Detection (Intent Inference)

The AI detects stage from conversation semantics:

| User says... | Stage | Module |
|-------------|-------|--------|
| "I want to build X", "I have an idea" | Requirements Analysis | `03-project-setup/01-requirements-analysis.md` |
| "What framework?", "How to structure?" | Technical Design | `03-project-setup/02-technical-design.md` |
| "How to implement?", "Best approach?" | Skill Dictionary | `02-skill-dictionary/index.md` |
| "Write the code", "Implement it" | Code Generation (+ TDD gate) | `01-code-generation/rules.md` |
| "Review this", "Any issues?" | Code Review | `08-code-review/rules.md` |
| "Is this secure?", "Audit this" | Security Review | `09-security-review/rules.md` |
| "There's a bug", "This broke" | Maintenance | `04-maintenance/rules.md` |
| "What do you think?", "How did I do?" | Evaluation | `06-evaluation/system.md` |

## Standard Flow

```
Requirements Analysis → Technical Design → Skill Dictionary (on demand)
  → Testing Strategy (gate) → Code Generation → Code Review
  → Security Review (if sensitive) → Evaluation
  → Maintenance (on demand)
```

## Quality Gates (Post-Implementation)

1. **Testing Strategy** (`07-testing-strategy/rules.md`): TDD enforced. 80%+ line coverage, 75%+ branch coverage. RED-GREEN-REFACTOR cycle. Test type selection guide (unit/integration/E2E/API/smoke/benchmark).
2. **Code Review** (`08-code-review/rules.md`): 6 dimensions (functionality, design, readability, testing, security, performance). Severity-ranked findings (Critical/High/Medium/Low). Overall assessment: Approve / Approve with Comments / Request Changes.
3. **Security Review** (`09-security-review/rules.md`): 7 dimensions (input validation, injection, authentication, authorization, data protection, dependencies, configuration). Exploitation scenarios for critical findings.

## Technology Selection

The Skill Dictionary (`02-skill-dictionary/index.md`) provides pre-built comparison matrices:

- Frontend: React vs Vue vs Svelte vs Solid
- State Management: Zustand vs Redux Toolkit vs Jotai vs Pinia vs Context
- CSS: Tailwind vs CSS Modules vs Styled Components vs Vanilla Extract vs Panda CSS
- Backend: Express vs Fastify vs Hono vs Elysia vs NestJS
- Database/ORM: Prisma vs Drizzle vs Knex vs Raw SQL
- Testing: Vitest vs Jest vs Playwright vs Cypress
- Package Manager: pnpm vs npm vs yarn vs bun

Each matrix includes: ecosystem maturity, learning curve, performance, TypeScript support, bundle size, and best-for scenarios.

## System-Wide Modules

- **Log Memory** (`05-log-memory/system.md`): Append-only cross-conversation logging. Decision-focused, max 5 lines per entry. Checkpoint support for resumability. Template files include annotated examples.
- **Context Management** (`context-management.md`): Auto-summarization at 20 and 40 turns. Key decision persistence. Context restoration on new conversations.
- **Error Recovery** (`error-recovery.md`): Checkpoint markers at module boundaries. Breakpoint detection for resume. Graceful degradation. 3-strike escalation.
- **Progress Tracking** (`progress-tracking.md`): Milestone-based percentage estimation. Stage completion status. Active reporting at boundaries and on request.
- **Extension Interface** (`extension-interface.md`): 3-level module spec (trigger-only, stage, system-wide). Hook system. Custom module registration guide.

## Installation

Install as an opencode skill:
```
# Copy to skills directory
cp -r platforms/opencode/SKILL.md ~/.config/opencode/skills/development-flow-guidelines/

# Or as a project skill
cp -r platforms/opencode/SKILL.md .opencode/skills/development-flow-guidelines/
```
