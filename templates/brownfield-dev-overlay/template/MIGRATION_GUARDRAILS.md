# MIGRATION_GUARDRAILS

## Rules
1. Prefer strangler or adapter patterns over rewrites.
2. Add characterization tests before refactoring fragile code.
3. Separate cleanup from behavior changes unless the active spec explicitly combines them.
4. Preserve public contracts unless a spec explicitly authorizes a break.
5. Record durable architecture changes as ADRs.

## Required workflow
1. Read `CURRENT_STATE.md`
2. Identify touched legacy surfaces
3. Add or confirm characterization tests
4. Write spec / plan / tasks
5. Implement smallest viable slice
6. Verify no unintended drift
