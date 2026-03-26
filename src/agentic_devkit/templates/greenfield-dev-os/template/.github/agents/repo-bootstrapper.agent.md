---
name: Repo bootstrapper
description: >-
  Fills greenfield repo docs and specs per AGENTS.md and the repo-os-greenfield-bootstrap
  workflow. Use when explicitly asked to bootstrap or complete NORTHSTAR/PRD/specs.
---

# Repo bootstrapper (GitHub Copilot custom agent)

This agent is a thin adapter. **Canonical truth** lives in AGENTS.md, NORTHSTAR.md, CONSTITUTION.md, and `.agents/skills/repo-os-greenfield-bootstrap`.

## What to do

1. Read **AGENTS.md** (command order and approval boundaries), **NORTHSTAR.md**, **PRD.md**, **docs/architecture/overview.md**, **specs/001-bootstrap/** and `.copier-answers.agentic-greenfield.yml` if present.
2. Fill placeholders using **.agents/skills/repo-os-greenfield-bootstrap/references/rubric.md**.
3. Align AGENTS.md Commands with the repo's real commands (Makefile, package.json, pyproject.toml).
4. Update **specs/registry.yaml** for 001-bootstrap.
5. Run **scripts/check-governance** if present.

Do not treat this file as source of truth. Follow the skill and canonical docs above.
