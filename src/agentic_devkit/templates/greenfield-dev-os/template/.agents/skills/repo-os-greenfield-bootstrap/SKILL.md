---
name: repo-os-greenfield-bootstrap
description: >-
  Fills NORTHSTAR, NORTHSTAR_METRICS, PRD, docs/architecture, and specs/001-bootstrap placeholders and aligns
  AGENTS.md commands after a greenfield repo was created with copier. Use when the user
  just ran copier copy from the agentic greenfield template or asks to bootstrap or
  fill placeholders in a new repo.
---

# Repo OS greenfield bootstrap

Run **after** `copier copy` into a new repo. Do not treat this skill as the source of truth; canonical truth stays in `NORTHSTAR.md`, `NORTHSTAR_METRICS.md`, `CONSTITUTION.md`, and specs.

## When to use

- User just created a repo from the agentic greenfield template.
- User asks to "bootstrap," "fill placeholders," or "finish setup" in a new repo.

## When not to use

- Repo already has filled NORTHSTAR/NORTHSTAR_METRICS/PRD and a completed 001-bootstrap spec.
- Task is a one-off edit (use normal editing).

## Steps

1. **Read context**
   - `NORTHSTAR.md`, `NORTHSTAR_METRICS.md`, `PRD.md`, `docs/architecture/overview.md`
   - `specs/001-bootstrap/spec.md`, `plan.md`, `tasks.md`
   - `.copier-answers.agentic-greenfield.yml` if present (project name, etc.)
   - Existing Makefile or package manifests to infer real commands

2. **Fill placeholders**
   - Replace `<product-name>`, `<primary user>`, `<core outcome>`, etc. in `NORTHSTAR.md` and `PRD.md` using rubric in [references/rubric.md](references/rubric.md).
   - Fill `NORTHSTAR_METRICS.md` so the headline metric, hard gates, diagnostics, stopping rules, and assumptions are concrete and consistent with `NORTHSTAR.md`, `PRD.md`, and repo evidence.
   - Fill `docs/architecture/overview.md` with at least high-level components and boundaries.
   - Fill `specs/001-bootstrap/*` so in-scope, acceptance criteria, and verifiers are concrete and match the PRD.

3. **Align AGENTS.md commands**
   - Set Commands section to the repo's real commands (e.g. `make setup`, `npm run dev`, or `uv run dev`). Do not leave stub text if the repo already has a Makefile or package scripts.

4. **Update specs/registry.yaml**
   - Ensure `001-bootstrap` has correct `title`, `status: active`, and `touched_surfaces` if you changed anything.

5. **Run governance checks**
   - If the repo has `scripts/check-governance`, run it and fix any failures before finishing.

## Stop conditions

- Stop and ask if project name or primary user is ambiguous.
- Stop if the repo has no clear stack (no Makefile, no package.json, no pyproject.toml) and ask how the user runs setup/test.

## Output

- All placeholders in `NORTHSTAR.md`, `NORTHSTAR_METRICS.md`, `PRD.md`, `docs/architecture/overview.md`, and `specs/001-bootstrap/*` filled with concrete, consistent text.
- AGENTS.md commands matching the repo.
- Handoff: "Bootstrap complete. Run `make verify` (or your equivalent) and review specs/001-bootstrap before implementing."

## References

- [references/rubric.md](references/rubric.md) — format and consistency for filled content.
