# Changelog

All notable changes to coding-guidelines will be documented in this file.

## [2.0.0] — 2026-07-26

### Added
- **Testing Strategy module** (`07-testing-strategy`): TDD workflow, 6-type test selection guide, coverage standards (80%+ lines, 75%+ branches, 90%+ functions). Acts as a gate before code generation — no implementation code written until test plan is defined.
- **Code Review module** (`08-code-review`): Structured 6-dimension checklist with severity-ranked findings (Critical/High/Medium/Low). Overall assessment: Approve / Approve with Comments / Request Changes.
- **Security Review module** (`09-security-review`): 7-dimension audit covering input validation, injection prevention, authentication, authorization, data protection, dependency security, and configuration security. Includes exploitation scenarios for critical findings.
- **Technology Selection Matrices** in Skill Dictionary: Pre-built comparisons for 7 categories — frontend frameworks, state management, CSS approaches, backend frameworks, database/ORM, testing frameworks, and package managers. Each matrix includes ecosystem maturity, learning curve, performance, TypeScript support, and best-for scenarios.
- **Context Management** (`context-management.md`): Auto-summarization at 20 and 40 turns, key decision persistence, context restoration on new conversations.
- **Error Recovery** (`error-recovery.md`): Checkpoint system at module boundaries, breakpoint detection for resume, graceful degradation, 3-strike escalation policy.
- **Extension Interface** (`extension-interface.md`): 3-level module registration spec, hook system (pre_stage_enter, post_stage_exit, on_decision, on_checkpoint, on_error), custom module development guide.
- **Progress Tracking** (`progress-tracking.md`): Milestone-based percentage estimation, stage completion status, active reporting at boundaries and on request.
- **Gate Chain Specification** (`gate-chain.md`): Formal dependency graph with verifiable input/output contracts and gate conditions.
- **Validation Script** (`scripts/validate.py`): Automated checks for frontmatter completeness, reference reachability, gate closure, circular dependencies, token budget consistency, and lifecycle coverage.
- **Layered Loading Specification** (`loading-spec.md`): Executable pseudo-code for 3-tier loading (Discovery/Activation/Execution) with per-platform optimization notes.
- **Multi-Platform Support**: Platform adapters for Claude Code, opencode, Cursor, and GitHub Copilot, in addition to existing Codex support.
- **Frontmatter Contracts**: All 15 modules now include formal `inputs`, `outputs`, `gates`, `version`, `module_id`, `category`, and `depends_on` fields.

### Changed
- **Log templates enriched**: All log templates include annotated examples and granularity standards (max 5 lines per entry, decision-focused).
- **Log system expanded**: New write timing for testing, code review, security review, maintenance, and checkpoint events.
- **SKILL.md rewritten**: Now covers 9 lifecycle modules and 4 system-wide modules with full gate pipeline.
- **README.md restructured**: Multi-platform installation guide with per-platform commands.
- **agents/openai.yaml**: Translated to English.

### Fixed
- Module dependency chain formalized — all `input.from` references resolve to valid upstream `output` fields.
- Circular dependency check passes for all modules.
- BOM character stripped from all files.
- Token budget declarations match actual file sizes.

### Removed
- Legacy Codex-only architecture replaced with multi-platform approach.

## [1.0.0] — 2026-07-25

### Initial Release
- **6 lifecycle modules**: Code Generation, Skill Dictionary, Requirements Analysis, Technical Design, Post-Deployment Maintenance, Evaluation System.
- **Log Memory System**: Append-only logging with template-instance architecture.
- **Intent Inference Engine**: Natural conversation stage detection without explicit commands.
- **Codex platform support**: Agent configuration and skill registration.
