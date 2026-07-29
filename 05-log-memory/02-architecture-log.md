# Architecture Design Log

Log entry format:
```
[YYYY-MM-DD HH:MM] <Entry Type> <Summary>

<Detailed Content (max 5 lines)>
```

---

## Examples

```
[2026-07-26 10:15] Decision Chose PostgreSQL as primary database
Selected PostgreSQL for relational data integrity. Considered SQLite (single-server
limitation) and MongoDB (schema enforcement needed). Version: PostgreSQL 16.
```

```
[2026-07-26 10:45] Addition Defined API contract for /users endpoint
GET /users/:id — returns UserProfile, 404 if not found.
POST /users — creates user, returns 201 + UserProfile.
PUT /users/:id — updates user fields, returns 200 + updated UserProfile.
DELETE /users/:id — soft-deletes user, returns 204.
```

```
[2026-07-26 11:00] Change Switched from Express to Fastify
Replaced Express with Fastify for built-in schema validation, better TypeScript
support, and ~2x throughput. Migration cost: 2 hours, surface area matched 95%.
```

---

## Log Entries
