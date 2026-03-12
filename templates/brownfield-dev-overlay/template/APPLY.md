# Brownfield overlay — how to use

This overlay adds the agentic documentation operating system to an **existing** repository.

## Prerequisites

- Clean working tree (commit or stash changes)
- Git-managed repo
- [Copier](https://copier.readthedocs.io/) installed (`pip install copier` or `uv add copier`)

## Apply once

From the **parent** of your repo (e.g. `~/src`):

```bash
copier copy path/to/agentic-dev-brownfield-overlay my-existing-repo
```

Or from a published template URL:

```bash
copier copy gh:org/agentic-dev-brownfield-overlay ./my-existing-repo
```

Answer the prompts. Files are written into the repo; existing files are not overwritten by default (Copier will ask or skip). Review diffs before committing.

## Update later

After applying, Copier stores answers in **`.copier-answers.agentic-brownfield.yml`** (so this overlay can coexist with other Copier templates). To pull template updates:

```bash
cd my-existing-repo
copier update --answers-file .copier-answers.agentic-brownfield.yml
```

## What this overlay adds

- **CURRENT_STATE.md** — describe the repo as it really is (legacy, debt, fragile areas).
- **MIGRATION_GUARDRAILS.md** — rules for changing legacy safely.
- **AGENTS.md** — brownfield read order (current state first) and approval boundaries.
- **docs/governance/** — DOCS_SYSTEM.md, context-registry.yaml.
- **specs/** — registry, archive, and a starter spec folder (e.g. `2026-03-12-legacy-change`).
- **NORTHSTAR.md**, **CONSTITUTION.md**, **PRD.md** — minimal placeholders; fill or merge with existing.
- **Adapters** — CLAUDE.md, .github/copilot-instructions.md, .cursor/rules/00-router.mdc, opencode.json.

## After applying

1. Fill **CURRENT_STATE.md** with an honest picture of the repo.
2. Keep **MIGRATION_GUARDRAILS.md** and **AGENTS.md** as the source of truth for agent behavior.
3. Use **specs/** for every non-trivial change; register each spec in `specs/registry.yaml`.
4. Do not duplicate policy in adapter files; they should only point at canonical docs.

## Design principle

**One canonical truth layer, thin tool adapters, zero duplicated policy.**
