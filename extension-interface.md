---
title: Extension Interface
description: Module registration specification for custom modules, plugin architecture, and third-party extension injection
version: "2.0.0"
module_id: extension-interface
category: meta
depends_on: []
inputs:
  - field: custom_module_spec
    description: "Module definition following the registration contract"
    required: false
outputs:
  - field: registration_spec
    description: "The formal contract that all modules (built-in and custom) must satisfy"
    schema: "{required_fields: [string], optional_fields: [string], hook_points: [string]}"
gates:
  - condition: "module.required_fields.all(f => f in module.frontmatter)"
    description: "All required fields must be present in frontmatter"
    on_fail: block
---

# Extension Interface

## Positioning

The development-flow-guidelines system is designed to be extended. Users and third-party developers can create custom modules that integrate with the routing system, log system, and inter-module workflow. This document defines the contract for module registration.

## Module Registration Specification

### Required Frontmatter

Every module file must include YAML frontmatter with the following fields:

```yaml
---
title: <Module Title>
description: <One-line description of what the module does>
version: "1.0.0"
module_id: <unique-identifier>       # e.g., "07-testing-strategy"
category: <core|extension|utility>    # core = lifecycle stage, extension = added capability, utility = tool/helper
depends_on: []                        # List of upstream module_ids this module depends on
inputs: []                            # Declared inputs, including optional from/alias bindings
outputs: []                           # Declared outputs used by downstream modules
gates: []                             # Gate conditions enforced before execution
---
```

Optional extension metadata such as `triggers` and `hooks` may be added when the module participates in routing or lifecycle interception, but they are not required by the core validator.

### File Naming Convention

```
<NN>-<module-category>/rules.md     # For lifecycle modules (NN = stage number)
<feature-name>.md                   # For extension/utility modules (at skill root)
```

### Integration Points

A module may integrate with the system at three levels:

**Level 1: Trigger-Only Module**
- Defined in SKILL.md trigger conditions section
- When triggered, loaded and executed independently
- No log integration required
- Example: context-management.md

**Level 2: Stage Module (with log integration)**
- Participates in the lifecycle flow
- Has defined position in the standard flow
- Writes to and reads from log files
- Has checkpoint support
- Example: 07-testing-strategy/rules.md

**Level 3: System-Wide Module**
- Intercepts or wraps other modules
- May modify system behavior globally
- Requires explicit dependency declaration
- Example: error-recovery.md (intercepts failures across modules)

### Registering a New Module

1. Create the module file following the naming convention
2. Add the required frontmatter
3. Add the module to the Sub-Module Index in SKILL.md
4. If it is a Stage Module, add its position to the Standard Flow diagram in SKILL.md
5. Add trigger conditions to the Intent Inference section if applicable
6. Define checkpoint points if applicable (for error-recovery integration)
7. Document in README.md module table

## Hook Points

The system provides these hook points for extension modules to intercept or enhance behavior:

| Hook | When Called | Signature |
|------|-----------|-----------|
| `pre_stage_enter` | Before entering any stage module | `(stage_id: string, context: ConversationContext) → void` |
| `post_stage_exit` | After completing any stage module | `(stage_id: string, output: StageOutput) → void` |
| `on_decision` | When user confirms a technology choice or design decision | `(decision: Decision) → void` |
| `on_checkpoint` | When a checkpoint marker is written | `(checkpoint: Checkpoint) → void` |
| `on_error` | When any module execution fails or degrades | `(error: ModuleError) → RecoveryStrategy` |

Hook handlers are registered by declaring the hook in the module's frontmatter:

```yaml
hooks:
  - pre_stage_enter
  - on_decision
```

## Inter-Module Communication

Modules communicate through the log system, not direct function calls:

1. **Upstream → Downstream**: Stage modules write outputs to log files; downstream modules read those logs.
2. **Peer Modules**: Modules at the same level do not directly communicate. They read the shared log state.
3. **System → Module**: SKILL.md routes execution; error-recovery intercepts failures; context-management injects summaries.

## Custom Module Example

A user-created module for API documentation generation:

```yaml
---
title: API Documentation Generator
description: Auto-generates OpenAPI specs from implemented endpoints
version: "1.0.0"
module_id: "custom-api-docs"
category: extension
depends_on: ["03-project-setup", "08-code-review"]
triggers: ["generate docs", "create API docs", "write documentation"]
hooks:
  - post_stage_exit
---
```

This module would:
- Trigger when the user requests documentation
- Hook into `post_stage_exit` after code review to auto-suggest documentation generation
- Read architecture logs for API contracts
- Generate OpenAPI specification file as output
