---
title: Security Review
description: Security audit covering authentication, authorization, input validation, secret management, injection prevention, and common vulnerability patterns
version: "2.0.0"
module_id: 09-security-review
category: lifecycle
depends_on: ["01-code-generation"]
inputs:
  - field: implementation_code
    description: "Code to audit for security vulnerabilities"
    from: "01-code-generation"
    required: true
  - field: review_report
    description: "Code review findings that may flag security concerns"
    from: "08-code-review"
    required: false
outputs:
  - field: security_report
    description: "Severity-ranked security findings with exploitation scenarios"
    schema: "{findings: [{severity: string, dimension: string, file: string, issue: string, exploitation_scenario: string, fix: string}], dimensions_covered: number}"
gates:
  - condition: "security_report.dimensions_covered >= 7"
    description: "All 7 security dimensions must be audited"
    on_fail: block
  - condition: "security_report.findings.filter(f => f.severity == 'critical').length == 0"
    description: "No exploitable vulnerabilities on approval"
    on_fail: block
---

# Security Review

## Positioning

Security review is a mandatory gate for code that handles user input, authentication, sensitive data, or external integrations. This module provides a focused security checklist separate from general code review.

## Trigger Conditions

Triggered when:
- User authentication or authorization logic is implemented
- User input is processed (forms, file uploads, API parameters)
- Sensitive data is stored or transmitted (passwords, tokens, PII)
- External APIs or services are integrated
- Database queries are constructed
- The user explicitly requests a security check

## Review Checklist

### 1. Input Validation

All user input must be validated at the boundary:

| Check | Requirement |
|-------|------------|
| Type validation | Input matches expected type (string, number, boolean) |
| Length limits | Strings and collections have maximum length constraints |
| Format validation | Email, URL, phone, and other structured fields match expected patterns |
| Range checks | Numeric values have min/max bounds |
| Whitelist over blacklist | Accept known-good patterns rather than trying to reject known-bad ones |
| Encoding normalization | Handle Unicode normalization to prevent homograph attacks |

### 2. Injection Prevention

| Vector | Mitigation |
|--------|-----------|
| SQL Injection | Use parameterized queries or ORM. Never concatenate user input into SQL strings. |
| Cross-Site Scripting (XSS) | Escape output in HTML context. Use framework-provided escaping (`textContent` over `innerHTML`). Apply Content-Security-Policy headers. |
| Command Injection | Do not pass user input to shell commands. If unavoidable, use argument arrays, not string concatenation. |
| Path Traversal | Validate and sanitize file paths. Reject `../` sequences. Resolve to canonical path and verify it is within allowed directory. |
| Server-Side Request Forgery (SSRF) | Validate and restrict URLs before making outbound requests from the server. Block internal IP ranges. |
| Deserialization | Never deserialize untrusted data without validation. Use safe parsers (JSON over pickle). |

### 3. Authentication

| Check | Requirement |
|-------|------------|
| Password storage | Use bcrypt, argon2, or scrypt. Never store plain-text or use weak hashes (MD5, SHA1). |
| Session management | Sessions have expiry. Tokens are invalidated on logout. Session IDs are cryptographically random. |
| Rate limiting | Login and sensitive endpoints have rate limits. |
| Multi-factor | Recommend MFA for sensitive operations. |
| Credential in code | No hardcoded passwords, API keys, or tokens in source code. Use environment variables or secret management. |

### 4. Authorization

| Check | Requirement |
|-------|------------|
| Default deny | Access is denied by default; explicitly grant permissions. |
| Server-side enforcement | Authorization checks are on the server, not just hidden UI elements on the client. |
| Resource ownership | Users can only access their own resources unless explicitly granted broader access. |
| Role validation | Role/permission checks happen on every request, not just at login. |
| Indirect object references | Use indirect references (UUIDs, random tokens) instead of sequential IDs in URLs. |

### 5. Data Protection

| Check | Requirement |
|-------|------------|
| Encryption in transit | All communication uses TLS. HTTP is redirected to HTTPS. |
| Encryption at rest | Sensitive data in databases and file storage is encrypted. |
| Data minimization | Only collect and store data that is necessary. |
| Logging sensitivity | No passwords, tokens, or PII in log output. |
| Data retention | Define and enforce data retention policies. |

### 6. Dependency Security

- Are all dependencies up to date? Check for known vulnerabilities.
- Are unused dependencies removed?
- Are dependency versions pinned (lock file committed)?

### 7. Configuration Security

- Default credentials are changed (no `admin/admin`).
- Debug mode and verbose error messages are disabled in production.
- Security headers are configured (CSP, HSTS, X-Frame-Options, X-Content-Type-Options).
- CORS is configured restrictively (not `Access-Control-Allow-Origin: *`).

## Reporting Format

Group findings by severity:

```
[Critical] — Immediate fix required. Exploitable vulnerability.
  file:line — Issue + exploitation scenario + fix

[High] — Fix before production deployment.
  file:line — Issue + risk + fix

[Medium] — Fix in current development cycle.
  file:line — Issue + recommendation

[Low] — Best practice improvement.
  file:line — Suggestion
```

## When No Issues Found

If the review finds no security issues, state this explicitly:
```
Security review: No issues found across all seven dimensions.
```
This provides documented assurance that a review was conducted.

## Integration with Other Modules

- **Code Generation**: Trigger after code involving user input, authentication, or sensitive data.
- **Code Review**: The general review includes security as one dimension; this module provides depth when the security surface is large.
- **Post-Deployment Maintenance**: Any code change touching security-sensitive areas must pass this review.
