---
title: Post-Deployment Maintenance
description: Incremental modifications, bug investigation, and regression protection for existing projects
version: "2.0.0"
module_id: 04-maintenance
category: lifecycle
depends_on: []
inputs:
  - field: bug_description
    description: "User-reported issue: symptoms, conditions, reproduction steps"
    required: true
  - field: existing_code
    description: "Affected codebase for investigation"
    required: true
outputs:
  - field: diagnosis
    description: "Root cause confirmed by user"
  - field: modification_plan
    description: "Scope and approach for the fix"
  - field: modified_code
    description: "Applied fix with regression verification"
gates:
  - condition: "diagnosis.confirmed_by_user"
    description: "Root cause must be diagnosed and confirmed before modifying code"
    on_fail: block
  - condition: "modification_plan.scope_declared"
    description: "Change scope must be declared before execution"
    on_fail: block
---

# Post-Deployment Maintenance

## Positioning

Post-deployment maintenance is not rewriting the project; it is performing precise, surgical modifications on the existing codebase. The goal of maintenance is to resolve the current problem at minimal cost without introducing new issues.

## Modification Principles

- **Minimal changes**: Do not modify code outside the target scope. Follow the "precise change scope" rules from the code generation section.
- **Understand before acting**: Before modifying, read and understand the affected code blocks and their context, then formulate a modification plan.
- **Change implementation, not interfaces**: Unless necessary, prefer modifying internal module implementations rather than inter-module interface definitions.

## Maintenance Flow

### Step 1: Locate the Problem

After the user describes the problem, the AI first helps locate the root cause rather than directly modifying code:

- Confirm the specific symptom ("What error occurs? Under what conditions is it triggered?")
- Cross-reference code and logs to trace the root cause
- Eliminate possible causes, narrowing down to the most likely candidates
- Present the diagnosis for user confirmation before proceeding with modifications

### Step 2: Assess Impact Scope

Determine the scope of changes needed, and explain which modules will be affected:

- In which module and which function does the change occur?
- Which places call this function?
- Do other files need to be updated after the change?

### Step 3: Formulate Modification Plan

Before making changes, explain the planned approach:

- What to change and how
- What not to change (clear boundaries to avoid unintended modifications)
- How to verify the change works correctly after completion

### Step 4: Execute Modifications

- Modify one file at a time according to the plan, confirming each after completion
- Verify affected functionality after each modification
- If rollback is needed, roll back only the current change, not other files

### Step 5: Regression Testing

- After modifications are complete, verify affected functionality
- Also check whether the changes impacted unrelated functionality
- The user provides final confirmation that everything works correctly

## Bug Investigation Flow

When the user reports a bug, systematically investigate through the following layers rather than guessing blindly:

1. **Surface check**: Are there obvious typos? Variable names, spelling, bracket matching, etc.
2. **Type check**: Do parameter types match? Is the return value handled correctly?
3. **Logic check**: Are there missing branches in conditional statements? Could loops cause index out-of-bounds?
4. **State check**: Are there implicit state dependencies? Is state consistent across different paths?
5. **Boundary check**: Null values, empty lists, boundary inputs, concurrent scenarios.
6. **Environment check**: Runtime environment differences, dependency versions, configuration issues.

After investigating one layer without finding the issue, proceed to the next layer.

## Scenario Coverage Testing

Beyond code-level investigation, the AI should also perform scenario-based testing from a functional perspective, simulating user operations under different conditions to discover hidden issues:

### Common Scenario Types

- **Happy path scenarios**: The user's complete operation path under ideal conditions
- **Invalid input scenarios**: The user enters invalid values, empty values, overly long data, etc.
- **Interruption scenarios**: Operations are interrupted mid-way (network disconnection, page refresh, unexpected exit)
- **Boundary condition scenarios**: Behavior when system limits are reached (maximum concurrency, maximum data volume)
- **Permission scenarios**: Different roles / unauthenticated users attempting unauthorized operations
- **State jump scenarios**: The user skips certain prerequisite steps and directly operates downstream features

### Operation Method

- The AI describes hypothetical scenarios and expected behavior rather than directly executing code
- Lists for each scenario: input conditions, expected output, and actual observed behavior
- The user can perform actual test verification based on this

## Rollback Protection

- Maintenance-stage modifications should use small commits where possible (confirm after changing one function).
- Use git or other version control tools for fine-grained rollback.
- If the AI assists with rollback, it should specify the rollback scope: only roll back the current modification, not unrelated files.
- Before modifying, inform the user whether the current code has been committed, and suggest committing unsaved changes before starting modifications.

## User Psychology Protection

- Understand that users may lack motivation to re-familiarize themselves with an existing project.
- During maintenance, the AI should proactively take on more context restoration work: reading logs, explaining code structure, proposing minimal change plans.
- The goal is to reduce the user's psychological burden, not to add new steps to the maintenance process.
- If the change scope is large, it can be completed across multiple conversations, doing only a small portion each time.

## Log System Integration

- After modifications are complete, append a modification record to the implementation path log.
- Record: which module was changed, why it was changed, a summary of the changes, and a recovery point (git commit hash, etc.).
- This facilitates future maintainers (including the future self) understanding the change history.
