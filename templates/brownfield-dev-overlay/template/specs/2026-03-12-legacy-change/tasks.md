# tasks.md — <change-id>

## Rules
- Execute in order unless marked [P].
- Update this file as work completes.
- Do not mark complete unless the verifier for that item has passed.
- Every implementation task must name the requirement ID it addresses.

## Tasks
- [ ] T1: read `CURRENT_STATE.md`, `MIGRATION_GUARDRAILS.md`, `spec.md`, and `plan.md`
- [ ] T2 [REQ-legacy-change-001][REQ-legacy-change-002]: add or confirm characterization tests for touched surfaces
- [ ] T3 [REQ-legacy-change-003]: implement smallest viable slice
- [ ] T4 [REQ-legacy-change-001][REQ-legacy-change-002]: verify no unintended behavioral drift
- [ ] T5: run full verify
- [ ] T6 [REQ-legacy-change-004]: reconcile implementation against requirement IDs and migration notes

## Completion checklist
- [ ] existing characterization tests still pass
- [ ] no contract regressions
- [ ] migration notes if applicable
