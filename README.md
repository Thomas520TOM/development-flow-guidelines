# development-flow-guidelines

Open-source guidance for AI-assisted coding work across multiple editors and agents.

<table>
    <tr>
        <td width="58%" valign="top">
            <p><strong>development-flow-guidelines</strong> packages a full lifecycle system for code-related tasks: requirements analysis, technical design, skill lookup, testing strategy, code generation, code review, security review, maintenance, evaluation, logging, context recovery, and extensibility.</p>
            <p align="left">
                <a href="https://github.com/Thomas520TOM/development-flow-guidelines" aria-label="GitHub repository">
                    <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub logo" width="28" height="28" style="vertical-align: middle; margin-right: 8px;">
                </a>
                <a href="https://github.com/Thomas520TOM/development-flow-guidelines/actions/workflows/validate.yml">
                    <img src="https://img.shields.io/github/actions/workflow/status/Thomas520TOM/development-flow-guidelines/validate.yml?branch=main&logo=githubactions&label=CI" alt="CI status" style="vertical-align: middle; margin-right: 6px;">
                </a>
                <a href="scripts/validate.py">
                    <img src="https://img.shields.io/badge/validation-passing-brightgreen" alt="Validation passing" style="vertical-align: middle; margin-right: 6px;">
                </a>
                <a href="LICENSE">
                    <img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT license" style="vertical-align: middle; margin-right: 6px;">
                </a>
                <a href="platforms/">
                    <img src="https://img.shields.io/badge/platforms-Codex%20%7C%20Claude%20Code%20%7C%20opencode%20%7C%20Cursor%20%7C%20Copilot-6a5acd" alt="Supported platforms" style="vertical-align: middle;">
                </a>
            </p>
            <p><strong>Why It Matters</strong></p>
            <ul>
                <li>Enough structure to keep the assistant consistent.</li>
                <li>Enough modularity to load only what is needed.</li>
                <li>Enough validation to keep the repository trustworthy.</li>
            </ul>
        </td>
        <td width="42%" valign="top">
            <img src="assets/development-flow-cover-dark.svg" alt="development-flow-guidelines dark cover" />
        </td>
    </tr>
</table>

## Highlights

<table>
  <tr>
    <td width="33%" valign="top"><strong>Lifecycle aware</strong><br>Work flows from idea to implementation through explicit stages, gates, and validation.</td>
    <td width="33%" valign="top"><strong>Multi-platform</strong><br>Codex, Claude Code, opencode, Cursor, and GitHub Copilot all have first-class adapters.</td>
    <td width="33%" valign="top"><strong>Modular and auditable</strong><br>Every module has frontmatter, dependencies, outputs, and gate checks.</td>
  </tr>
</table>

<table>
  <tr>
    <td width="33%" valign="top"><strong>Release ready</strong><br>Validation covers reference reachability, dependency closure, token budgets, and lifecycle coverage.</td>
    <td width="33%" valign="top"><strong>Template friendly</strong><br>The repo works as a reusable instruction system, not a one-off prompt dump.</td>
    <td width="33%" valign="top"><strong>Recovery built in</strong><br>Context management, error recovery, and progress tracking are part of the system.</td>
  </tr>
</table>

## What You Get

| Area | What It Covers |
|------|----------------|
| Stage routing | A single entry point in [SKILL.md](SKILL.md) and a standard development flow |
| Decision support | A skill dictionary with technology selection matrices |
| Quality gates | Testing strategy, code review, and security review before work is considered complete |
| Recovery | Context management, error recovery, and progress tracking |
| Extensibility | A documented extension interface and hook model |
| Platform support | Dedicated adapters for the supported coding environments |

## How It Works

```mermaid
flowchart LR
    A[Requirements Analysis] --> B[Technical Design]
    B --> C[Skill Dictionary]
    C --> D[Testing Strategy]
    D --> E[Code Generation]
    E --> F[Code Review]
    E --> G[Security Review]
    F --> H[Evaluation]
    G --> H
    E --> I[Maintenance]
```

The system separates three layers:

1. Discovery: lightweight metadata for intent detection.
2. Activation: the full rule set for the active module.
3. Execution: deeper references, checklists, and platform-specific guidance.

## Supported Platforms

| Platform | Adapter | Notes |
|----------|---------|-------|
| Codex | `agents/openai.yaml` | Root skill package support |
| Claude Code | `platforms/claude-code/` | Project-level or user-level install |
| opencode | `platforms/opencode/` | Uses `AGENTS.md` as discovery |
| Cursor | `platforms/cursor/rules/` | Always-on and glob-based rule loading |
| GitHub Copilot | `platforms/github-copilot/instructions.md` | Single-file instructions |

## Quick Start

If you want to use the repository as a skill package:

```powershell
Expand-Archive -Path ".\development-flow-guidelines.zip" -DestinationPath "C:\Users\<username>\.codex\skills\development-flow-guidelines" -Force
```

For Claude Code:

```bash
cp -r . ~/.claude/skills/development-flow-guidelines/
cp platforms/claude-code/CLAUDE.md <project-root>/CLAUDE.md
```

For opencode:

```bash
cp platforms/opencode/SKILL.md ~/.config/opencode/skills/development-flow-guidelines/SKILL.md
mkdir -p .opencode/skills/development-flow-guidelines
cp platforms/opencode/SKILL.md .opencode/skills/development-flow-guidelines/SKILL.md
```

## Validation

Run the repository validator before publishing changes:

```powershell
python scripts/validate.py
```

It checks:

- frontmatter completeness
- reference reachability
- gate closure
- circular dependencies
- token budget consistency
- lifecycle coverage
- release surface presence

## Repository Map

| Path | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Entry point and stage router |
| [02-skill-dictionary/index.md](02-skill-dictionary/index.md) | Technology selection matrices and implementation guidance |
| [03-project-setup/](03-project-setup/) | Requirements analysis and technical design |
| [05-log-memory/](05-log-memory/) | Append-only logs and templates |
| [07-testing-strategy/rules.md](07-testing-strategy/rules.md) | TDD and coverage gate |
| [08-code-review/rules.md](08-code-review/rules.md) | Structured code review rubric |
| [09-security-review/rules.md](09-security-review/rules.md) | Security review rubric |
| [platforms/](platforms/) | Platform adapters |
| [scripts/validate.py](scripts/validate.py) | Repository validation script |
| [AGENTS.md](AGENTS.md) | opencode discovery layer |

## Contributing

When adding or changing a module:

1. Keep the module frontmatter complete.
2. Update the relevant platform adapter if behavior changes.
3. Run `python scripts/validate.py`.
4. Keep the README and module index aligned with the actual file tree.

## Notes

- Discovery, activation, and execution are intentionally separate.
- Dynamic project logs belong in instance directories, not inside the template itself.
- The `scripts/` folder is reserved for repository automation and validation.

## License

MIT License. See [LICENSE](LICENSE).
