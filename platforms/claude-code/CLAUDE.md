# CLAUDE.md — Project Instructions for development-flow-guidelines

When this skill is installed as a project-level Claude Code skill, this file serves as the project instruction reference.

## Active Skill

The `development-flow-guidelines` skill is active in this project. It provides full development lifecycle guidance:

- Requirements analysis → Technical design → Skill dictionary → Testing strategy → Code generation → Code review → Security review → Maintenance → Evaluation

## Key Behaviors

- The AI infers the current development stage from natural conversation — no explicit commands needed
- Options are presented with pros/cons; the user makes the final decision
- No implementation code is written until a test plan is defined (TDD gate)
- Code changes are precise and scoped — impact assessment before execution
- Bug investigation follows a 6-layer systematic approach (surface → type → logic → state → boundary → environment)
- Code review uses a 6-dimension severity-ranked checklist
- Security-sensitive code triggers a mandatory 7-dimension security audit
- Logs are written silently in append-only mode for cross-conversation continuity

## Module Loading

Modules are in the skill root directory:
- `01-code-generation/rules.md`
- `02-skill-dictionary/index.md`
- `03-project-setup/01-requirements-analysis.md`
- `03-project-setup/02-technical-design.md`
- `04-maintenance/rules.md`
- `05-log-memory/system.md`
- `06-evaluation/system.md`
- `07-testing-strategy/rules.md`
- `08-code-review/rules.md`
- `09-security-review/rules.md`
- `context-management.md`
- `error-recovery.md`
- `extension-interface.md`
- `progress-tracking.md`

## Technology Selection

When facing technology decisions, consult `02-skill-dictionary/index.md` which contains pre-built comparison matrices for:
- Frontend frameworks (React/Vue/Svelte/Solid)
- State management (Zustand/Redux Toolkit/Jotai/Pinia)
- CSS approaches (Tailwind/CSS Modules/Styled Components/Vanilla Extract)
- Backend frameworks (Express/Fastify/Hono/Elysia/NestJS)
- Database/ORM (Prisma/Drizzle/Knex/Raw SQL)
- Testing frameworks (Vitest/Jest/Playwright/Cypress)
- Package managers (pnpm/npm/yarn/bun)
