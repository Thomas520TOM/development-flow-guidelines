---
title: Skill Guidance Dictionary
description: Learning and explanation system for implementation methods before coding, with built-in technology selection matrices
version: "2.0.0"
module_id: 02-skill-dictionary
category: lifecycle
depends_on: []
inputs:
  - field: user_question
    description: "Specific implementation question or technology choice the user needs help with"
    required: true
  - field: tech_stack
    description: "Existing technology choices if already decided"
    from: "02-technical-design"
    required: false
outputs:
  - field: selected_approach
    description: "User-chosen implementation direction with rationale"
  - field: explanation
    description: "Detailed explanation of the selected approach"
  - field: code_example
    description: "Runnable code segment demonstrating the approach"
gates:
  - condition: "user_selection_confirmed"
    description: "User must select or acknowledge an approach before proceeding"
    on_fail: warn
---

# Skill Guidance Dictionary

## Positioning

Sits between project setup and code generation. After project setup produces concrete functional requirements, interface signatures, and constraints, this module provides learning guidance on implementation approaches, then hands off to the code generation module for execution.

The granularity focuses at the function or code-segment level.

## Trigger Conditions

- Triggered when the user has a question about a specific feature implementation and **actively asks**.
- Does not auto-populate or run alongside code generation.
- Only used for high-complexity scenarios or technologies unfamiliar to the user. Simple implementations go directly to code generation without passing through the dictionary.

## Processing Flow

### Round One: Direction Enumeration

- Briefly list several feasible implementation approaches for the requirement (selectable algorithms, selectable libraries/frameworks, different architectural ideas).
- Provide a high-level overview for each approach (one-sentence summary, pros and cons, applicable scenarios).
- Do not go into detail; only provide directional choices.

### User Selection

- After the user selects a direction, proceed to round two.
- The process may also end here without further depth (indicating the user already understands).

### Round Two: Detailed Explanation

Based on the selected approach, provide a thorough explanation:

- **Library/Framework**: Introduce which specific functions and interfaces will be used, calling conventions, notes, and common pitfalls.
- **Algorithm**: Clearly explain the principles and implementation process, supplemented with pseudocode or brief examples as needed.

### Depth Control

- The user decides when they have "understood enough."
- When the user indicates "got it, understood" or "let's start implementing," the explanation concludes and the system switches to code generation.

## Output Artifacts

- The explanation process naturally produces text notes (explanations, code snippet examples).
- After the explanation concludes, generate a directly runnable code segment based on the explained content.
- In principle, explanation and code generation happen in separate conversations to avoid ambiguity from "explaining while coding."

## Technology Selection Matrices

When users face technology decisions without clear preferences, present a curated comparison using these pre-built matrices. Each matrix covers the dominant options in a category with decision factors.

### Frontend Framework

| Factor | React | Vue | Svelte | Solid |
|--------|-------|-----|--------|-------|
| Ecosystem maturity | Excellent — largest community | Strong — Vue-specific ecosystem | Growing — fewer third-party libs | Small — emerging ecosystem |
| Learning curve | Moderate — JSX, hooks mental model | Gentle — template syntax, reactive data | Gentle — compiles away, less boilerplate | Moderate — signals, fine-grained reactivity |
| Performance (runtime) | Good — virtual DOM diffing | Good — virtual DOM | Excellent — no virtual DOM, compiled | Excellent — no virtual DOM, signals |
| Bundle size (baseline) | ~40KB gzipped | ~20KB gzipped | ~2KB gzipped | ~5KB gzipped |
| TypeScript support | Good — gradual adoption | Good — composition API | Good — built-in | Good — built-in |
| Best for | Large teams, rich ecosystem needs | Balanced DX, progressive adoption | Performance-critical, smaller bundles | Fine-grained reactivity, performance |

### State Management

| Factor | Zustand | Redux Toolkit | Jotai | Pinia (Vue) | Context + useReducer |
|--------|---------|---------------|-------|-------------|---------------------|
| Boilerplate | Minimal | Moderate (RTK reduces from classic Redux) | Minimal | Minimal | Minimal |
| Learning curve | Low | Moderate | Low | Low | Low |
| DevTools | Yes (middleware) | Excellent (Redux DevTools) | Yes | Excellent (Vue DevTools) | None (manual logging) |
| Scalability | Good — stores are independent | Excellent — designed for large apps | Good — atomic model | Good | Poor — re-render cascading |
| TypeScript | Excellent | Excellent | Good | Excellent | OK |
| Bundle size | ~1KB | ~12KB | ~2KB | ~2KB | 0 (built-in) |
| Best for | Small-medium apps, independent stores | Large apps, complex state logic | React apps with atomic state needs | Vue apps | Simple global state (theme, auth) |

### CSS Approach

| Factor | Tailwind CSS | CSS Modules | Styled Components | Vanilla Extract | Panda CSS |
|--------|-------------|-------------|-------------------|-----------------|-----------|
| Learning curve | Moderate — utility-first is a mind shift | Low — standard CSS syntax | Low — CSS-in-JS familiar | Moderate — build-time CSS | Moderate — new syntax |
| Runtime cost | Zero — compiled at build | Zero — CSS file output | Runtime — ~12KB + per-component | Zero — compiled at build | Zero — compiled at build |
| Type safety | Config-based, partial | None | Via theme typing | Full TypeScript | Full TypeScript |
| Component co-location | In markup (className) | Co-located .module.css file | In JS file (template literal) | Separate .css.ts file | Separate file or co-located |
| Theming | Config-based design tokens | CSS custom properties | ThemeProvider + props | createTheme + contract | Preset + conditions |
| Bundle output | Tiny (only used classes) | One CSS file per module | Runtime injection | Static CSS file | Static CSS + atomic |
| Best for | Rapid prototyping, consistent design | Standard CSS, no tool lock-in | Dynamic styling, React ecosystem | Type-safe, zero-runtime | Atomic CSS with type safety |

### Backend Framework

| Factor | Express | Fastify | Hono | Elysia (Bun) | NestJS |
|--------|---------|---------|------|-------------|--------|
| Performance | Moderate | High | High | Very high | Moderate |
| Ecosystem | Vast — most middleware available | Growing — fastify plugins | Growing — web standard | Small — Bun ecosystem | Large — Nest modules |
| TypeScript | Manual setup | Good | Excellent (built-in) | Excellent (built-in) | Excellent (built-in) |
| Learning curve | Low | Low | Low | Moderate | High — Angular-style architecture |
| Bundle/startup | Light | Light | Very light | Very light | Heavy — reflection, decorators |
| Validation | Manual or zod | Built-in schema | Built-in (zod integration) | Built-in (typebox) | class-validator + DTOs |
| Best for | Legacy, max ecosystem | High-performance APIs | Edge, serverless, small APIs | Bun-first, max performance | Enterprise, large teams |

### Database / ORM

| Factor | Prisma | Drizzle | Knex | Raw SQL |
|--------|--------|---------|------|---------|
| Type safety | Excellent — generated types | Excellent — inferred types | Partial | None |
| Migration tool | Built-in, declarative | Built-in, SQL-first | Built-in | Manual (or external tool) |
| Query flexibility | Good — Prisma Client covers common cases | Excellent — SQL-like API, raw SQL escape hatch | Excellent — query builder | Maximum |
| Performance | Good — Data Proxy for edge | Excellent — minimal overhead | Good | Maximum (no ORM overhead) |
| Learning curve | Moderate — own schema language | Low — SQL-like syntax | Low — chainable | Depends on SQL knowledge |
| Bundle/size | Large — generated client | Small | Moderate | None |
| Best for | Teams wanting type-safe DB access | SQL power with type safety | Users preferring query builders over ORMs | Maximum control, complex queries |

### Testing Framework

| Factor | Vitest | Jest | Playwright (E2E) | Cypress (E2E) |
|--------|--------|------|-----------------|---------------|
| Runtime | Vite-native, fast | Node, slower startup | Browser-based, realistic | Browser-based, real-time |
| API compatibility | Jest-compatible | — | Custom (web-first) | Custom (chainable) |
| Parallel execution | Yes, per-file | Yes, per-file (workers) | Yes, per-worker | Paid feature |
| Watch mode | Excellent (HMR-aware) | Good | No | No |
| UI mode | Yes (built-in) | Via third-party reporter | Yes (trace viewer) | Yes (built-in) |
| Component testing | Yes (via @vitest/ui) | Via @testing-library | Via @playwright/experimental-ct | Via @cypress/mount-utils |
| TypeScript | Zero config with Vite | Requires ts-jest config | Zero config | Zero config |
| Best for | Vite projects, unit + integration | Non-Vite or legacy projects | Browser E2E, cross-browser testing | Component-level integration, visual testing |

### Package Manager

| Factor | pnpm | npm | yarn | bun |
|--------|------|-----|------|-----|
| Disk usage | Content-addressable, efficient | Flat node_modules, duplicates | Pluggable (PnP or node_modules) | Fast, disk efficient |
| Install speed | Fast (hard links) | Moderate | Moderate (PnP adds time) | Very fast (Zig-based) |
| Strictness | Strict — undeclared deps error | Lenient — hoisted flat | Configurable | Strict (similar to pnpm) |
| Monorepo support | Excellent — workspaces, filters, catalog | Good — workspaces | Good — workspaces | Good — workspaces |
| Lockfile | pnpm-lock.yaml | package-lock.json | yarn.lock | bun.lockb (binary) |
| Best for | Monorepos, disk-conscious | Default, no extra install | Existing Yarn projects | Speed, all-in-one runtime |

## How to Use These Matrices

1. Identify the decision category from the user's question
2. Present a condensed version: show the top 2-3 candidate factors most relevant to the user's specific context, not the full matrix
3. Ask clarifying questions to narrow down: "What matters most — ecosystem maturity, learning curve, or performance?"
4. Recommend a specific option with reasoning, but leave the final decision to the user
5. Log the decision to the architecture log after user confirmation
