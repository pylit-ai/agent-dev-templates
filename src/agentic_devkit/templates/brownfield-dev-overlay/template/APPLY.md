# Brownfield overlay — how to use

This overlay adds the agentic documentation operating system to an **existing** repository.

## Prerequisites

- Clean working tree (commit or stash changes)
- Git-managed repo

## Apply once (no clone required)

**Preferred:** use the wrapper CLI or remote Copier source. No need to clone the template repo.

From **inside** your existing repo root:

```bash
# Easiest: wrapper (runs census optionally, then Copier)
uvx agentic-devkit overlay .
# With preflight census to prefill CURRENT_STATE:
uvx agentic-devkit overlay . --intake
```

Or with Copier directly:

```bash
uvx copier copy gh:your-org/agentic-dev-brownfield-overlay .
```

With pipx: `pipx run copier copy gh:your-org/agentic-dev-brownfield-overlay .`

**Fallback** (local template path):

```bash
copier copy path/to/agentic-dev-brownfield-overlay .
```

Answer the prompts. Files are written into the repo; existing files are not overwritten by default (Copier will ask or skip). Review diffs before committing.

## Optional: preflight census

To let the overlay prefill **CURRENT_STATE** from repo structure (manifests, CI, lockfiles, test/docs dirs), run the census and write the result **before** applying:

```bash
cd my-existing-repo
python .agents/skills/repo-os-brownfield-intake/scripts/repo_census.py . --format yaml --output .agentic-bootstrap.yml
```

Then apply the overlay. Copier loads `.agentic-bootstrap.yml` as `_external_data.census` and the template will add an "Inferred stack" section to CURRENT_STATE.md. Or use `uvx agentic-devkit overlay . --intake` to do both.

## Update later

After applying, Copier stores answers in **`.copier-answers.agentic-brownfield.yml`** (so this overlay can coexist with other Copier templates). To pull template updates:

```bash
cd my-existing-repo
copier update --answers-file .copier-answers.agentic-brownfield.yml
```

(Requires Copier installed: `uv sync` in a repo that depends on this template, or `pip install copier` / `uv tool install copier`.)

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
