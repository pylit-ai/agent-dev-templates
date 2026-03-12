---
name: Brownfield intake
description: >-
  Runs repo census, drafts CURRENT_STATE.md, and creates the first brownfield spec
  per AGENTS.md and the repo-os-brownfield-intake skill. Use when explicitly asked.
---

# Brownfield intake (GitHub Copilot custom agent)

This agent is a thin adapter. **Canonical truth** lives in AGENTS.md, CURRENT_STATE.md, MIGRATION_GUARDRAILS.md, and `.agents/skills/repo-os-brownfield-intake`.

## What to do

1. Run repo census: `python .agents/skills/repo-os-brownfield-intake/scripts/repo_census.py .` (optionally `--output .agentic-bootstrap.yml`).
2. Draft **CURRENT_STATE.md** using `.agents/skills/repo-os-brownfield-intake/references/brownfield-rubric.md`.
3. Propose deltas for NORTHSTAR and PRD; do not overwrite without confirmation.
4. Create first brownfield spec bundle in `specs/<id>/` and register in `specs/registry.yaml`.
5. Run **scripts/check-governance** if present.
6. Emit handoff summary: inferred, uncertain, next steps.

Do not treat this file as source of truth. Follow the skill and canonical docs above.
