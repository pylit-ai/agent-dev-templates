# Repo bootstrapper (Claude subagent adapter)

Follow the same workflow and artifacts defined by the canonical repo docs and the **.agents/skills/repo-os-greenfield-bootstrap** skill.

1. Read NORTHSTAR.md, PRD.md, docs/architecture/overview.md, specs/001-bootstrap/*, and .copier-answers.agentic-greenfield.yml if present.
2. Fill placeholders in those files using .agents/skills/repo-os-greenfield-bootstrap/references/rubric.md.
3. Align AGENTS.md Commands with the repo's real commands (Makefile, package.json, pyproject.toml).
4. Update specs/registry.yaml for 001-bootstrap.
5. Run scripts/check-governance if present.

Do not treat this file as source of truth. Canonical: NORTHSTAR.md, CONSTITUTION.md, AGENTS.md, specs.
