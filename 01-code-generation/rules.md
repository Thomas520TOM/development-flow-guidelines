---
title: Code Generation Rules
description: Behavioral norms for AI when generating and modifying code
version: "2.0.0"
module_id: 01-code-generation
category: lifecycle
depends_on: ["07-testing-strategy"]
inputs:
  - field: test_plan
    description: "Test plan defining what to test before implementation"
    from: "07-testing-strategy"
    required: true
  - field: architecture_design
    description: "Module structure and interface contracts"
    from: "02-technical-design"
    required: false
outputs:
  - field: implementation_code
    description: "Generated code with passing tests"
  - field: change_plan
    description: "Declared scope of changes before execution"
gates:
  - condition: "test_plan != null && test_plan.length > 0"
    description: "Test plan must exist before writing implementation code"
    on_fail: block
  - condition: "change_plan_declared"
    description: "Change scope must be declared and confirmed by user before execution"
    on_fail: block
---

# Code Generation Rules

## Readability First

- Variable names are not abbreviated: use `user` not `u`, `calculate_total` not `calcTot`.
- Code does not pursue overly concise styles (e.g., nested chaining, multi-level list comprehensions), but is not bloated either.
- Complex logic is broken into clear steps; simple logic is not unnecessarily split — if one step is clear, there is no need to break it further.

## Precise Change Scope

- Before generating/modifying, first identify which files and which parts need to be changed, and report the change plan to the user (what files to change, how to change them).
- Proceed only after user confirmation.
- Generate and modify only what is necessary; do not make broad, sweeping changes.
- Unless the user explicitly agrees, do not opportunistically refactor, rename, or reformat.
- Changes spanning multiple files should be done one file at a time, ensuring consistency between successive modifications.

## Handling Ambiguous Requirements

- When encountering ambiguous requirements, stop and ask the user for clarification.
- At the same time, provide reasonable guesses as reference opinions to help the user decide.

## Comment Standards (Chinese)

- Variables and functions with broad scope must have comments explaining their actual purpose and significance.
- Small-scope temporary variables (e.g., loop counters) may omit comments.
- Function comments are mandatory at the function header, styled like API documentation: describe what the function does, parameter meanings and types, return values, and notes. A reader should be able to call the function after reading the comment alone.
- Comments are written in Chinese.

## Error Handling and Edge Cases

- Do not automatically introduce error handling (e.g., try-catch, error returns) unless the feature itself requires fault tolerance.
- But proactively handle edge cases: empty lists, None, boundary values, invalid inputs, etc.

## Debugging and Test Output

- Self-testing processes may include debug output.
- However, final delivered code must **not** contain residual debug information (print, console.log, etc.).

## Generation Pace

- Default is step-by-step generation: first generate the skeleton, then fill in details, letting the user see progress at each step.
- The specific pace is adjusted according to user requests.
- Cross-file changes: modify one file at a time, complete one before moving to the next.

## Relationship with Existing Project Style

- Skill rules take precedence. Even if the project's existing code follows a different style, newly generated code follows this skill's rules.
- Do not proactively rewrite existing code to conform to these rules; only ensure new outputs comply.
