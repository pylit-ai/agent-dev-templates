# plan.md — <change-id>

## Summary
Implement <change> using <approach> while preserving constraints in `CONSTITUTION.md` and `MIGRATION_GUARDRAILS.md`.

## Legacy surfaces touched
- <surface>
- <surface>

## Characterization tests
- <suite or test> — must remain passing

## Evidence sources
- implementation: <legacy files, seams, or new code paths that will cite requirement IDs>
- verifier: <characterization tests, regression tests, checks, or manual records that will cite requirement IDs>
- runtime signals: <logs, metrics, traces, or operational checks used as evidence>
- generated artifacts: `generated/traceability/graph.json`, `generated/traceability/verification-ledger.json`, and reports

## Architecture impact
- touched components: <list>
- unchanged components: <list>

## Rollout
1. <step>
2. <step>

## Rollback
1. <step>
2. <step>

## Verification plan
- run existing characterization tests
- run: `make verify` (or repo equivalent)
- manual checks: <list>
