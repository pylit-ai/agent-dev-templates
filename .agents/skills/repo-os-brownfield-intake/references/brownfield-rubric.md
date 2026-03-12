# Brownfield intake rubric

Use this when drafting CURRENT_STATE and first migration spec.

## CURRENT_STATE.md
- Current architecture: list components and what they do; note dependencies.
- Known mismatches: where docs or intent diverge from code.
- Fragile areas: path or module + brief reason.
- Characterization tests: test suite or file that must keep passing.
- Unsafe assumptions: e.g. "naming is not consistent," "dead code is not safe to remove without dependency search."

## First migration spec (specs/registry + one spec bundle)
- Choose one high-leverage, bounded change (e.g. add tests for one module, or one API boundary).
- spec.md: legacy context, why now, in/out of scope, acceptance criteria, blast radius.
- plan.md: characterization tests to add or confirm, rollout/rollback.
- Register in specs/registry.yaml with status active and touched_surfaces.

## Handoff summary
- What was inferred (stack, CI, docs).
- What is uncertain (needs human confirmation).
- What still needs to be done (e.g. "Fill CURRENT_STATE section X after reviewing module Y").
