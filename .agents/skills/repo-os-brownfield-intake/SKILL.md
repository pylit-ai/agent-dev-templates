---
name: repo-os-brownfield-intake
description: >-
  Inventories repo structure, CI, manifests, and tests; drafts CURRENT_STATE.md;
  proposes deltas for NORTHSTAR/PRD; creates the first brownfield spec bundle and
  registry entry; runs governance checks; produces a handoff summary. Use only
  when the user explicitly requests brownfield intake or "draft CURRENT_STATE."
  Never invoke implicitly.
---

# Repo OS brownfield intake

Run **only when explicitly requested** after applying the brownfield overlay to an existing repo. Canonical truth stays in CURRENT_STATE.md, MIGRATION_GUARDRAILS.md, and specs; this skill is the execution layer.

## When to use

- User explicitly asks for "brownfield intake," "draft CURRENT_STATE," or "run repo census and create first migration spec."

## When not to use

- Do **not** run on "legacy" or "refactor" alone. Requires explicit request.
- Do not overwrite existing CURRENT_STATE or NORTHSTAR without user confirmation.

## Steps

1. **Run repo census**
   - Run `python .agents/skills/repo-os-brownfield-intake/scripts/repo_census.py .` (or from catalog equivalent). Optionally write `.agentic-bootstrap.yml` for reuse: `--format yaml --output .agentic-bootstrap.yml`. If this file exists when applying the brownfield overlay, Copier uses it as `_external_data.census` to prefill an "Inferred stack" section in CURRENT_STATE.md.
   - Scan repo root: manifests (package.json, pyproject.toml, etc.), CI (e.g. `.github/workflows`), lockfiles, test dirs, existing docs.

2. **Draft CURRENT_STATE.md**
   - Fill Current architecture, Known mismatches, Fragile areas, Characterization tests that must keep passing, Unsafe assumptions. Use [references/brownfield-rubric.md](references/brownfield-rubric.md).

3. **Propose deltas for NORTHSTAR and PRD**
   - Do not overwrite. Propose additions or changes (e.g. "Add to Non-goals: …") and ask for confirmation before applying.

4. **Create first brownfield spec bundle**
   - Pick one high-leverage, bounded change. Create `specs/<id>/spec.md`, `plan.md`, `tasks.md` (e.g. id like `2026-03-12-first-slice`).
   - Register in `specs/registry.yaml` with status active and touched_surfaces.

5. **Run governance checks**
   - Run `scripts/check-governance` if present; fix failures.

6. **Handoff summary**
   - Emit: what was inferred, what is uncertain, what still needs human confirmation.

## Stop conditions

- Stop if repo has no clear structure or no Git.
- Stop and ask before overwriting any existing CURRENT_STATE.md, NORTHSTAR.md, or PRD.md.

## Output

- CURRENT_STATE.md drafted (or delta proposed).
- First spec bundle and registry entry created.
- Short handoff: inferred, uncertain, next steps.

## References

- [references/brownfield-rubric.md](references/brownfield-rubric.md) — format for CURRENT_STATE and first spec.
