---
title: Testing Strategy
description: TDD workflow, test type selection, and coverage standards for any feature or bug fix
version: "2.0.0"
module_id: 07-testing-strategy
category: lifecycle
depends_on: ["01-requirements-analysis", "02-technical-design"]
inputs:
  - field: module_list
    description: "Decomposed feature units from requirements analysis output"
    from: "01-requirements-analysis"
    alias: feature_units
    required: true
  - field: architecture_design
    description: "Module boundaries and interfaces for integration test planning"
    from: "02-technical-design"
    required: false
outputs:
  - field: test_plan
    description: "Per-unit test definitions: input, expected output, edge cases"
    schema: "[{unit: string, input: any, expected: any, edge_cases: [string]}]"
  - field: coverage_targets
    description: "Specific coverage targets for this feature"
    schema: "{lines: number, branches: number, functions: number}"
gates:
  - condition: "test_plan.length > 0"
    description: "At least one testable unit must be defined"
    on_fail: block
  - condition: "test_plan.all(u => u.edge_cases.length > 0)"
    description: "Every unit must have edge cases listed"
    on_fail: warn
---

# Testing Strategy

## Positioning

Tests are not an afterthought. This module enforces test-first thinking across the entire development lifecycle. It sits alongside code generation: before writing any implementation code, the test strategy is defined first.

## Trigger Conditions

Triggered whenever:
- A new feature is about to be implemented
- A bug is reported and needs fixing
- The user explicitly asks about testing
- Code generation is about to begin on a non-trivial implementation

Does not trigger for:
- Purely conversational/informational requests
- Configuration file changes
- Documentation-only changes

## TDD Workflow

### Phase 1: Test Planning

Before writing a single line of implementation, define:

1. **What to test**: Decompose the feature into testable units. Each unit should be a discrete behavior, not a method.
2. **Expected behavior**: For each unit, specify the input, expected output, and side effects.
3. **Edge cases**: List boundary conditions, error paths, and edge inputs.

Output format (conversational, not a template dump):

```
Test Plan for [feature/component]:

Unit: [behavior description]
  Input: [representative input]
  Expected: [expected output/behavior]

Edge Cases:
  - [edge case]: [expected behavior]
```

### Phase 2: Test-First Implementation

Write the test before the implementation, following RED-GREEN-REFACTOR:

1. **RED**: Write a failing test that captures the expected behavior
2. **GREEN**: Write the minimum implementation to pass the test
3. **REFACTOR**: Clean up both test and implementation code
4. **REPEAT**: Move to the next testable unit

When writing tests, follow these conventions:
- One assertion per test where possible (one behavior, one test)
- Test names describe the scenario and expected outcome
- Tests are independent and can run in any order
- Use the project's existing test framework (do not introduce a new one)

### Phase 3: Regression Guard

After all units pass, verify that existing functionality is intact:
- Run the full test suite
- If any existing test breaks, fix the regression before continuing

## Test Type Selection Guide

Choose the appropriate test type based on what is being tested:

| What to Test | Test Type | Characteristics |
|-------------|-----------|----------------|
| Pure logic, algorithms, data transformations | Unit Test | Fast, no I/O, no network, no database |
| Module interactions, component composition | Integration Test | Tests interfaces between units |
| User-facing workflows, UI flows | End-to-End Test | Tests complete user scenarios |
| API endpoints, response handling | API Test | HTTP request/response validation |
| Cross-cutting concerns (auth, rate limiting) | Smoke Test | Quick sanity check before full suite |
| Performance regression | Benchmark | Timed execution, resource measurement |

Decision flow:
1. Is the behavior pure logic with no side effects? → Unit test
2. Does it span multiple modules or touch I/O? → Integration test
3. Is it a complete user journey? → E2E test

## Coverage Standards

Default coverage targets (adjustable per project conventions):

| Metric | New Code | Modified Code | Legacy Code (on first touch) |
|--------|---------|---------------|------------------------------|
| Line coverage | 80%+ | 70%+ on changed lines | 50%+ on touched module |
| Branch coverage | 75%+ | 65%+ | 40%+ |
| Function coverage | 90%+ | 85%+ | 60%+ |

Coverage is a signal, not a target. Do not write meaningless assertions just to hit coverage numbers. If a line is genuinely trivial (getter, constant, delegation), it is acceptable to exclude it with documented reasoning.

## When to Skip Tests

Tests may be skipped in these cases, with explicit justification:
- **Boilerplate/scaffolding**: Project initialization, config files, generated code
- **Throwaway prototypes**: Code explicitly marked as temporary
- **Trivial pass-through**: Pure delegation with no logic

If skipping tests, state the reason in the implementation log.

## Log System Integration

- Append test plan summary to the implementation log when tests are defined
- Record coverage results after test execution
- In maintenance mode, note which existing tests were updated

## Integration with Other Modules

- **Code Generation**: Test plan is a prerequisite gate. No implementation code is written until the test plan is defined.
- **Code Review**: Reviewers verify that tests exist, are meaningful, and pass.
- **Post-Deployment Maintenance**: Bug fixes must include a regression test that reproduces the bug and verifies the fix.
