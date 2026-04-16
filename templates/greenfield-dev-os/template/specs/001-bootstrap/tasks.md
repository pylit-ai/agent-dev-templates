# tasks.md — 001-bootstrap

## Rules
- Execute in order unless marked [P].
- Update this file as work completes.
- Do not mark complete unless the verifier for that item has passed.
- Every implementation task must name the requirement ID it addresses.

## Tasks
- [ ] T1: read `NORTHSTAR.md`, `CONSTITUTION.md`, `PRD.md`, `spec.md`, and `plan.md`
- [ ] T2 [REQ-001-bootstrap-001]: create or update contracts / schemas
- [ ] T3 [REQ-001-bootstrap-001][REQ-001-bootstrap-002]: implement core domain logic
- [ ] T4 [REQ-001-bootstrap-002]: implement boundary adapters and API handlers
- [ ] T5 [REQ-001-bootstrap-003]: add structured logging and metrics
- [ ] T6 [REQ-001-bootstrap-001][REQ-001-bootstrap-002]: write unit tests
- [ ] T7 [REQ-001-bootstrap-003][REQ-001-bootstrap-004]: write integration tests
- [ ] T8 [REQ-001-bootstrap-005]: update docs impacted by behavior changes
- [ ] T9: run `make verify`
- [ ] T10: reconcile implementation against requirement IDs

## Parallelizable
- [ ] [P] TP1: docs updates that do not affect code behavior
- [ ] [P] TP2: non-overlapping test additions

## Completion checklist
- [ ] all requirement IDs have implementation and verifier evidence
- [ ] no constitution violations
- [ ] rollback path documented
- [ ] observability added
- [ ] tests pass
