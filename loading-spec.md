---
title: Layered Loading Specification
description: Executable specification for three-tier module loading with token budget enforcement
version: "2.0.0"
module_id: loading-spec
category: meta
---

# Layered Loading Specification

This document defines the concrete loading mechanism that the host platform (Codex, Claude Code, opencode, Cursor, etc.) should implement to load coding-guidelines modules efficiently.

## Three-Tier Architecture

```
Tier 1: DISCOVERY (~2,500 tokens)
  └── Inject name + description + triggers for all core modules
  └── Always in system prompt
  └── Purpose: enable intent inference without loading full content

Tier 2: ACTIVATION (per-module, ~500-5,000 tokens)
  └── Inject full SKILL.md of the active module
  └── Triggered by: intent inference match OR explicit user command
  └── Purpose: provide detailed module rules and workflow

Tier 3: EXECUTION (per-module, on-demand)
  └── Inject references/, matrices, checklists
  └── Triggered by: module requires deep reference data
  └── Purpose: load heavy content only when actually needed
```

## Executable Loading Logic

```python
class LoadingOrchestrator:
    def __init__(self, skill_root: str):
        self.skill_root = Path(skill_root)
        self.modules = self._load_all_frontmatters()
        self.active_module = None
        self.conversation_state = ConversationState()

    # --- DISCOVERY LAYER ---

    def build_discovery_prompt(self) -> str:
        """Build the always-on discovery layer (~2.5K tokens)."""
        entries = []
        for mid, fm in self.modules.items():
            if fm.get("category") == "meta":
                continue  # meta modules not needed in discovery
            triggers = fm.get("triggers", [])
            trigger_text = ", ".join(triggers) if triggers else "on demand"
            entries.append(
                f"| {fm['title'] or fm['name']} | {fm['description']} | {trigger_text} |"
            )
        return "\n".join([
            "## Available Development Stages",
            "| Stage | Purpose | Triggers |",
            "|-------|---------|----------|",
            *entries,
            "",
            "The AI infers the current stage from conversation semantics. ",
            "Load the full stage rules only when the stage is active."
        ])

    # --- ACTIVATION LAYER ---

    def infer_active_module(self, user_message: str) -> str | None:
        """Infer which module should be active based on user input."""
        scored = []
        for mid, fm in self.modules.items():
            triggers = fm.get("triggers", [])
            if not triggers:
                continue
            score = sum(1 for t in triggers if t.lower() in user_message.lower())
            if score > 0:
                scored.append((score, mid))
        scored.sort(reverse=True)
        return scored[0][1] if scored else None

    def activate_module(self, module_id: str) -> str:
        """Load the full SKILL.md for a module."""
        if module_id == self.active_module:
            return ""  # Already active

        self.active_module = module_id
        fm = self.modules[module_id]

        # Gate check before activation
        for gate in fm.get("gates", []):
            if not self._check_gate(fm, gate):
                action = gate.get("on_fail", "warn")
                if action == "block":
                    raise GateBlockedError(
                        f"Gate blocked: {gate.get('description', 'unknown gate')}"
                    )
                elif action == "warn":
                    self._log_gate_warning(gate)

        # Check token budget
        budget = fm.get("token_budget", "medium")
        path = self._find_module_file(module_id)
        size = len(path.read_text()) if path else 0
        if budget == "low" and size > 5000:
            self._log_token_warning(module_id, size, budget)

        return self._load_full_module(module_id)

    def _check_gate(self, fm: dict, gate: dict) -> bool:
        """Evaluate a gate condition against current state."""
        condition = gate.get("condition", "")
        # In a real implementation, this evaluates the condition expression
        # against self.conversation_state
        if condition == "test_plan != null && test_plan.length > 0":
            return bool(self.conversation_state.get("test_plan"))
        if condition == "change_plan_declared":
            return self.conversation_state.get("change_plan_declared", False)
        if condition == "diagnosis.confirmed_by_user":
            return self.conversation_state.get("diagnosis_confirmed", False)
        # ... additional condition evaluators
        return True  # Default pass for text-only conditions

    # --- EXECUTION LAYER ---

    def load_references(self, module_id: str, ref_name: str) -> str | None:
        """Load a specific reference file for a module (Tier 3)."""
        path = self.skill_root / module_id / "references" / f"{ref_name}.md"
        if path.exists():
            return path.read_text()
        return None

    def should_load_references(self, module_id: str) -> bool:
        """Determine if the module's references should be loaded."""
        fm = self.modules.get(module_id)
        if not fm:
            return False
        # References loaded only when:
        # - Module has high token_budget and conversation requires depth
        # - User explicitly requests reference data
        # - Matrix/comparison data is needed
        return fm.get("token_budget") == "high"
```

## Token Budget Enforcement

| Budget | Max Chars | Max Est. Tokens | Loading Tier |
|--------|-----------|-----------------|--------------|
| `low` | 5,000 | ~1,250 | Activation only |
| `medium` | 15,000 | ~3,750 | Activation + limited refs |
| `high` | 50,000 | ~12,500 | Full activation + refs |

If a module's actual file size exceeds its declared budget:
1. Log a warning via `check_token_budget()` in validate.py
2. At load time, truncate to budget limit with `[content truncated — see full module at <path>]`
3. Flag in CI as a size regression

## Platform-Specific Loading

### Claude Code

Claude Code's skill system loads SKILL.md on trigger. The discovery layer is not needed — Claude resolves skills by `/skill-name` command. Optimization: keep the Claude Code SKILL.md under 5,000 chars (token_budget: low).

### opencode

opencode supports three-tier loading natively. The AGENTS.md serves as the discovery layer. SKILL.md files are activation. References are execution. Map directly: AGENTS.md → Discovery, SKILL.md → Activation, references/ → Execution.

### Cursor

Cursor loads `.mdc` files based on globs. Always-apply files are always in context. Globs-based files load when matching files are open. No concept of execution tier. Optimization: split content between always-apply (core principles, security) and globs-based (code gen, testing, review) to minimize context overhead.

### GitHub Copilot

Single-file loading only. The `instructions.md` must be self-contained and compact. Optimization: keep under 3,000 chars. Prioritize always-active rules over stage-specific ones.
