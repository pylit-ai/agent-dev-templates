# Sandbox

## brownfield-intake-test

Used by `tests/test_brownfield_intake_sandbox.py` to verify brownfield intake behavior when **CURRENT_STATE.md**, **NORTHSTAR.md**, **CONSTITUTION.md**, and **PRD.md** already exist.

- Intake must **not** overwrite these files without user confirmation.
- The skill requires: stop and ask / propose deltas.
- Census runs against this dir; tests assert the skill’s no-overwrite contract.

Do not remove or overwrite the placeholder content in the four doc files; tests rely on it.
