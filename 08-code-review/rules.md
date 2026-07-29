---
title: Code Review
description: Structured code review with multi-dimensional checklist covering functionality, design, readability, security, and performance
version: "2.0.0"
module_id: 08-code-review
category: lifecycle
depends_on: ["01-code-generation", "07-testing-strategy"]
inputs:
  - field: implementation_code
    description: "Code to be reviewed (files, diff, or PR)"
    from: "01-code-generation"
    required: true
  - field: test_plan
    description: "Test plan to verify test existence and quality"
    from: "07-testing-strategy"
    required: false
outputs:
  - field: review_report
    description: "Severity-ranked findings across 6 dimensions"
    schema: "{findings: [{severity: 'critical'|'high'|'medium'|'low', dimension: string, file: string, line: number, description: string, suggestion: string}], assessment: 'approve'|'approve_with_comments'|'request_changes'}"
gates:
  - condition: "review_report.dimensions_covered >= 6"
    description: "All 6 dimensions must be reviewed"
    on_fail: block
  - condition: "review_report.assessment != null"
    description: "Overall assessment must be provided"
    on_fail: block
  - condition: "review_report.findings.filter(f => f.severity == 'critical').length == 0"
    description: "No critical issues on final approval"
    on_fail: block
---

# Code Review

## Positioning

Code review is a systematic quality gate, not a subjective opinion exchange. This module provides a structured checklist that ensures every review covers the same dimensions with the same rigor, regardless of who or what is conducting the review.

## Trigger Conditions

Triggered when:
- The user says "review this code", "check my code", "any issues with this?"
- A feature implementation is completed
- Before committing or merging code
- The evaluation system flags a need for deeper review

## Review Process

### Step 1: Scope Declaration

Before reviewing, clarify what is being reviewed:
- Full feature or specific files?
- New code only or including modified existing code?
- Any specific concerns the user wants prioritized?

### Step 2: Multi-Dimensional Review

Apply each dimension below. Flag issues by severity:

| Severity | Meaning | Action |
|----------|---------|--------|
| **Critical** | Security vulnerability, data loss risk, system crash | Must fix before merge |
| **High** | Logic bug, incorrect behavior, broken contract | Fix before merge |
| **Medium** | Design smell, readability issue, missing test | Fix before or file follow-up task |
| **Low** | Style inconsistency, naming suggestion, minor optimization | Optional fix |

### Dimension 1: Functionality and Correctness

- Does the code implement the stated requirements completely?
- Is the core logic correct? Any off-by-one, inverted conditions, or missing branches?
- Are edge cases handled: null/empty input, zero/negative values, boundary values, concurrent access?
- Does this change break any existing functionality?

### Dimension 2: Design and Architecture

- Does each function/class/module have a single responsibility?
- Is the abstraction level appropriate? Any over-engineering or under-engineering?
- Is there unnecessary code duplication (DRY violation)?
- Is the new code tightly coupled to other modules? Would changes here cascade?
- Can this design accommodate foreseeable future requirements without restructuring?

### Dimension 3: Readability and Maintainability

- Are names clear, accurate, and meaningful? Avoid `data`, `temp`, `result`, `a`, `b`.
- Can the same functionality be expressed more simply?
- Are there necessary comments explaining "why" (not "what")?
- Are there stale, misleading, or redundant comments?
- Are there very long functions (>50 lines), deep nesting (>3 levels), or huge classes?

### Dimension 4: Testing and Robustness

- Do tests exist for the new/modified behavior?
- Are the tests meaningful (testing behavior, not implementation details)?
- Do edge cases have corresponding test coverage?
- Is error handling present for all fallible operations (I/O, network, parsing)?
- Are error messages user-friendly and actionable?

### Dimension 5: Security

- Is user input validated and sanitized before use?
- Are there SQL injection, XSS, command injection, or path traversal vectors?
- Are secrets (API keys, tokens, passwords) hardcoded in the source?
- Are authorization checks present on sensitive operations?
- Is sensitive data logged, exposed in error messages, or transmitted insecurely?

### Dimension 6: Performance

- Are there database queries inside loops (N+1 problem)?
- Are there unnecessary full table scans, large in-memory collections, or unbounded buffers?
- Is there obvious redundant computation or I/O?
- For frontend: unnecessary re-renders, large bundle additions, blocking operations on the main thread?

### Step 3: Severity-Ordered Report

Present findings grouped by severity, not by dimension:

```
[Critical]
  file:line — Issue description + suggested fix
[High]
  file:line — Issue description + suggested fix
[Medium]
  file:line — Issue description + suggested fix
[Low]
  file:line — Issue description + suggested fix
```

### Step 4: Overall Assessment

One of:

- **Approve**: No critical or high issues. Ready to merge.
- **Approve with Comments**: Medium issues only. Merge at discretion, file follow-ups.
- **Request Changes**: Critical or high issues present. Fix and re-submit for review.

## Review Principles

- **Review the code, not the author**: Focus on the artifact, not who wrote it.
- **Be specific**: "This could be simpler" is unhelpful. "Extract lines 45-60 into a separate function `validateInput` to reduce nesting" is helpful.
- **Explain why**: Every issue should include a brief "why this matters."
- **Acknowledge what works**: Call out well-designed sections, not just problems.
- **One review is enough**: Do not nitpick style if the project has a linter/formatter handling it. Focus on substance.

## Integration with Other Modules

- **Code Generation**: Review naturally follows after code generation completes.
- **Post-Deployment Maintenance**: Modified code in maintenance mode must pass review before merging.
- **Testing Strategy**: Reviewers verify that tests exist and cover the changes.
- **Evaluation System**: The evaluation system may trigger a full review for deeper issues flagged during evaluation.
- **Log System**: Review findings (summary) are appended to the implementation log.
