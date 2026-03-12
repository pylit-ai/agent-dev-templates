# Agentic dev templates

Catalog of Copier-based templates for the **agentic documentation operating system**: layered docs, spec-driven development, thin `AGENTS.md` router, and governance so multiple agents (Cursor, Claude Code, Codex, Copilot, OpenCode) share one canonical truth.

Design principle: **one canonical truth layer, thin tool adapters, zero duplicated policy.**

## Templates

| Template | Use case |
|----------|----------|
| **greenfield-dev-os** | New repo: NORTHSTAR, CONSTITUTION, AGENTS, PRD, docs governance, specs, adapters (Claude, Copilot, Cursor, OpenCode), and **repo-os-greenfield-bootstrap** skill. |
| **brownfield-dev-overlay** | Existing repo: add CURRENT_STATE, MIGRATION_GUARDRAILS, brownfield AGENTS.md, governance, spec discipline, and **repo-os-brownfield-intake** skill (explicit-only). |

## Quick start

**No clone required** once the CLI is [published to PyPI](#publishing-maintainers) and template repos are published (see below). Until then, use this catalog locally with `uv run agentic-dev` or the Copier commands.

### 1) Easiest: wrapper CLI (no Copier syntax)

Requires [uv](https://docs.astral.sh/uv/). After the package is on PyPI as `agentic-devkit`, `uvx agentic-devkit` runs it with no install; otherwise run from this repo: `uv run agentic-dev`.

```bash
# New repo
uvx agentic-devkit init my-new-repo

# Existing repo (apply brownfield overlay)
cd my-existing-repo
uvx agentic-devkit overlay .

# Brownfield with preflight census
uvx agentic-devkit overlay . --intake
```

Set `AGENTIC_DEV_GREENFIELD_SOURCE` and `AGENTIC_DEV_BROWNFIELD_SOURCE` if your org’s distribution repos use different names (default: `gh:your-org/agentic-dev-greenfield` and `gh:your-org/agentic-dev-brownfield-overlay`).

### 2) Remote Copier (zero-clone)

```bash
# New repo
uvx copier copy gh:your-org/agentic-dev-greenfield my-new-repo

# Existing repo (run from repo root)
cd my-existing-repo
uvx copier copy gh:your-org/agentic-dev-brownfield-overlay .
```

With pipx: `pipx run copier copy gh:your-org/agentic-dev-greenfield my-new-repo` (same pattern).

### 3) Updates (after you’ve applied once)

```bash
cd my-repo
copier update --answers-file .copier-answers.agentic-greenfield.yml   # greenfield
copier update --answers-file .copier-answers.agentic-brownfield.yml # brownfield
```

### 4) Fallback: local catalog

If you have cloned this catalog:

```bash
copier copy ./templates/greenfield-dev-os ./my-new-repo
copier copy ./templates/brownfield-dev-overlay /path/to/existing-repo
```

Use `uv sync` then `uv run copier ...` (Copier is a dependency of this project).

**Greenfield UX:** For “Use this template” one-click, mark the distribution repo as a [GitHub template repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template). For **updateable** lineage, use Copier; answers are in `.copier-answers.agentic-greenfield.yml` / `.copier-answers.agentic-brownfield.yml`.

See `templates/brownfield-dev-overlay/template/APPLY.md` for brownfield details.

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

- **Remote / wrapper:** [uv](https://docs.astral.sh/uv/) and `uvx` (or `pipx run copier`) — no persistent Copier install.
- **Local catalog:** `uv sync` then `uv run copier ...` or `uv run agentic-dev ...` (Copier is a dependency).

## Publishing (maintainers)

To publish each template as its own repo for `copier copy gh:org/repo` and optional GitHub template UX:

1. Sync `templates/greenfield-dev-os` → `agentic-dev-greenfield` repo (e.g. via script).
2. Sync `templates/brownfield-dev-overlay` → `agentic-dev-brownfield-overlay` repo.
3. Tag releases in each distribution repo so `copier update` works.

**Scope (v1):** GitHub custom agents (`.github/agents/*.agent.md`) are out of scope; can be added in a later release.
