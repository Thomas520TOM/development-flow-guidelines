---
title: Gate Chain Specification
description: Formal dependency chain with verifiable input/output contracts and gate conditions
version: "2.0.0"
module_id: gate-chain
category: meta
---

# Gate Chain Specification

This document defines the formal dependency graph and verification rules for the development-flow-guidelines module system. All module contracts in their YAML frontmatter must satisfy the closure rules defined here.

## Module Dependency Graph

```
[user_input]
    │
    ▼
01-requirements-analysis ─────────────────────────────────────────────┐
    │ outputs: module_list, boundaries, blind_spots                    │
    ▼                                                                 │
02-technical-design ──────────────────────────────────────────────┐   │
    │ outputs: architecture_design, tech_stack, data_flow          │   │
    │                                                              │   │
    ├──► 02-skill-dictionary (on demand)                           │   │
    │    outputs: selected_approach, explanation                   │   │
    │                                                              │   │
    ▼                                                              │   │
07-testing-strategy ◄── module_list ──────────────────────────────┘   │
    │                                      (from requirements)         │
    │ outputs: test_plan, coverage_targets                             │
    │ gate: test_plan.length > 0 [BLOCK]                               │
    │                                                                  │
    ▼                                                                  │
01-code-generation ◄── test_plan ─────────────────────────────────┐   │
    │ gate: test_plan exists [BLOCK]                                │   │
    │ gate: change_plan declared & confirmed [BLOCK]                │   │
    │ outputs: implementation_code                                  │   │
    │                                                               │   │
    ├──► 08-code-review ◄── implementation_code ───────────────────┘   │
    │    gate: all 6 dimensions covered [BLOCK]                         │
    │    gate: no critical findings [BLOCK]                             │
    │    outputs: review_report                                        │
    │                                                                  │
    ├──► 09-security-review ◄── implementation_code                    │
    │    gate: all 7 dimensions covered [BLOCK]                         │
    │    gate: no critical vulnerabilities [BLOCK]                      │
    │    outputs: security_report                                       │
    │                                                                  │
    ▼                                                                  │
06-evaluation ◄── any stage output ────────────────────────────────────┘
    gate: issues <= 3 [WARN]
    outputs: evaluation_report

[Independent Entry Points]

04-maintenance ◄── bug_description
    gate: diagnosis confirmed [BLOCK]
    gate: modification scope declared [BLOCK]
    outputs: diagnosis, modification_plan, modified_code

[Cross-Cutting Systems]

05-log-memory ◄── any module_output
    gate: append_only (never modify existing) [BLOCK]
    gate: single entry <= 500 chars [WARN]
    outputs: log_entries, context_snapshot

context-management ◄── turn_count >= 20
    gate: snapshot <= 500 chars [WARN]
    outputs: context_snapshot

error-recovery ◄── module_failure
    gate: retry_count < 3 [WARN]
    outputs: checkpoint_marker, recovery_strategy

progress-tracking ◄── module_completion events
    outputs: progress_snapshot
```

## Gate Closure Rules

### Rule 1: Input Consumption

Every `input` field declared in a module's frontmatter that has a `from` reference must be produced as an `output` by the referenced module.

```
for each module.input where input.from exists:
    assert input.from in all_module_ids
    assert input.field in referenced_module.outputs
```

### Rule 2: Output Production

Every `output` field declared by an upstream module that feeds a gate condition must be consumed by at least one downstream module.

```
for each module.output:
    if module.id in ['system-router', 'extension-interface']:
        skip  // meta modules
    assert exists downstream where downstream.input.from == module.id
```

### Rule 3: Full Lifecycle Coverage

The standard flow from requirements to evaluation must be traceable without gaps:

```
trace: 01-requirements → 02-design → 07-testing → 01-codegen → 08-review → 09-security → 06-evaluation
entry points: 01-requirements, 04-maintenance, 02-skill-dictionary
exit point: 06-evaluation
```

### Rule 4: Gate Enforcement Levels

| Level | Behavior |
|-------|----------|
| `block` | Module execution must not proceed. Halt and report violation. |
| `warn` | Execution may proceed, but violation must be logged and visible to user. |
| `skip` | Condition not met means module is not applicable in current context. |

### Rule 5: Frontmatter Completeness

Every module file must declare all of these in its YAML frontmatter:

| Field | Required | Type |
|-------|----------|------|
| `title` or `name` | yes | string |
| `description` | yes | string |
| `version` | yes | semver string |
| `module_id` | yes | unique string |
| `category` | yes | `lifecycle` \| `system` \| `meta` |
| `depends_on` | yes | string[] (empty if none) |
| `inputs` | yes | array of input specs |
| `outputs` | yes | array of output specs |
| `gates` | yes | array of gate specs |

## Validation Script

Run `scripts/validate.py` to check all rules above. A clean run means the module system is production-ready.
