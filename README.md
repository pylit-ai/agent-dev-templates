# Agentic dev templates

Catalog of Copier-based templates for the **agentic documentation operating system**: layered docs, spec-driven development, thin `AGENTS.md` router, and governance so multiple agents (Cursor, Claude Code, Codex, Copilot, OpenCode) share one canonical truth.

Design principle: **one canonical truth layer, thin tool adapters, zero duplicated policy.**

## Templates

| Template | Use case |
|----------|----------|
| **greenfield-dev-os** | New repo: NORTHSTAR, CONSTITUTION, AGENTS, PRD, docs governance, specs, adapters (Claude, Copilot, Cursor, OpenCode), and **repo-os-greenfield-bootstrap** skill. |
| **brownfield-dev-overlay** | Existing repo: add CURRENT_STATE, MIGRATION_GUARDRAILS, brownfield AGENTS.md, governance, spec discipline, and **repo-os-brownfield-intake** skill (explicit-only). |

## Quick start

### Greenfield (new repo)

```bash
# From this catalog (clone or path)
copier copy ./templates/greenfield-dev-os ./my-new-repo
cd my-new-repo
# Fill NORTHSTAR.md, PRD.md, specs/001-bootstrap; run make setup / make verify when you add real commands
```

Or use a published distribution repo (if you maintain one):

```bash
copier copy gh:org/agentic-dev-greenfield ./my-new-repo
```

**Optional:** Mark the distribution repo as a [GitHub template repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template) for “Use this template” one-click create. For **updateable** lineage, use Copier; answers are stored in `.copier-answers.agentic-greenfield.yml` so you can run `copier update` later (and coexist with other templates).

### Brownfield (existing repo)

```bash
# From this catalog
copier copy ./templates/brownfield-dev-overlay /path/to/existing-repo
cd /path/to/existing-repo
# Fill CURRENT_STATE.md, then use specs/ for each non-trivial change
```

See `templates/brownfield-dev-overlay/template/APPLY.md` for full instructions.

## Layout (greenfield)

```
repo/
├── NORTHSTAR.md
├── CONSTITUTION.md
├── AGENTS.md
├── PRD.md
├── CLAUDE.md
├── opencode.json
├── docs/
│   ├── governance/
│   │   ├── DOCS_SYSTEM.md
│   │   └── context-registry.yaml
│   ├── architecture/
│   │   └── overview.md
│   ├── adr/
│   │   └── ADR-000-template.md
│   └── mcp/
│       └── servers.md
├── specs/
│   ├── registry.yaml
│   ├── 001-bootstrap/
│   │   ├── spec.md
│   │   ├── plan.md
│   │   └── tasks.md
│   └── archive/
├── .github/
│   ├── copilot-instructions.md
│   └── instructions/
│       └── backend.instructions.md
├── .cursor/
│   └── rules/
│       └── 00-router.mdc
├── .agents/
│   └── skills/
│       └── repo-os-greenfield-bootstrap/
│           ├── SKILL.md
│           ├── scripts/
│           ├── references/
│           └── agents/
├── .claude/
│   ├── agents/
│   │   └── repo-bootstrapper.md
│   └── commands/
│       └── bootstrap-repo.md
└── skills/
    └── README.md   # points to .agents/skills
```

## Requirements

- [Copier](https://copier.readthedocs.io/) — use the catalog’s dev env: `uv sync --extra dev` then `uv run copier ...`, or install globally: `pip install copier`

## Publishing (maintainers)

To publish each template as its own repo for `copier copy gh:org/repo` and optional GitHub template UX:

1. Sync `templates/greenfield-dev-os` → `agentic-dev-greenfield` repo (e.g. via script).
2. Sync `templates/brownfield-dev-overlay` → `agentic-dev-brownfield-overlay` repo.
3. Tag releases in each distribution repo so `copier update` works.

See this repo's `notepads/apply/templates.md` (catalog only; not in the generated tree) for the full design rationale, decision matrix, and governance details.

**Scope (v1):** GitHub custom agents (`.github/agents/*.agent.md`) are out of scope; can be added in a later release.
