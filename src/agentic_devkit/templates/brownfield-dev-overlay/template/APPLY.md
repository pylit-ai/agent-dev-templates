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

## Run intake

**repo-os-brownfield-intake** is a skill you run by **prompting your agent** (Cursor or Claude) in this repo — not a CLI. The agent reads AGENTS.md and `.agents/skills/repo-os-brownfield-intake/SKILL.md`, runs the repo census, drafts CURRENT_STATE.md, proposes NORTHSTAR/PRD deltas, and creates the first spec bundle. If you chose not to overwrite some files when applying the overlay, they may not mention the intake skill or canonical docs; the prompt below still works. See **"If you kept your existing files"** for what to add to each file you skipped.

**Copy-paste prompt** (use in a chat where the agent has this repo open):

```
Run the repo-os-brownfield-intake skill: read AGENTS.md and .agents/skills/repo-os-brownfield-intake/SKILL.md. Run the repo census script, draft CURRENT_STATE.md using the brownfield rubric, propose (don't overwrite) NORTHSTAR/PRD deltas, create the first spec bundle in specs/ and register it. Run scripts/check-governance if present. Give me a short handoff summary.
```

Review the drafted CURRENT_STATE.md and confirm (or edit) before making large edits. The agent will propose changes to NORTHSTAR/PRD for your approval instead of overwriting.

## If you kept your existing files (didn't overwrite)

When Copier asks "Overwrite X?" and you choose **No**, that file won't contain the overlay's content. You can still run the intake prompt above (the agent reads `.agents/skills/repo-os-brownfield-intake/SKILL.md`). For each file you skipped, add or merge as below so agents and maintainers can find the brownfield docs and the intake skill.

### Adapter files (point agents at canonical docs)

| File | What to add |
|------|-------------|
| **AGENTS.md** | Append a **Skills** section so the intake skill is discoverable. See snippet below. Optionally merge the overlay's "If touching legacy code" read order and "Core docs" list from the template. |
| **CLAUDE.md** | Append so Claude reads the canonical entrypoint and governance: `@AGENTS.md` and `@docs/governance/DOCS_SYSTEM.md`. |
| **.cursor/rules/00-router.mdc** | Append or ensure these rules: Read `AGENTS.md` first; for docs/structure changes read `docs/governance/DOCS_SYSTEM.md` and `CONSTITUTION.md`; for legacy code read `CURRENT_STATE.md` and `MIGRATION_GUARDRAILS.md` before editing; for feature work read the active spec bundle; do not duplicate policy from canonical docs. |
| **.github/copilot-instructions.md** | Append: Follow `AGENTS.md`. For repo structure/docs read `docs/governance/DOCS_SYSTEM.md` and `CONSTITUTION.md`. For legacy code read `CURRENT_STATE.md` and `MIGRATION_GUARDRAILS.md` first. For features read the active spec bundle. Do not introduce policy not in canonical docs. |
| **opencode.json** | Ensure `instructions` includes `"AGENTS.md"` and `"docs/governance/DOCS_SYSTEM.md"`. Merge with any existing entries; keep the `$schema` if you use it. |

**AGENTS.md — append this block:**

```markdown
## Skills (on-demand, explicit only)
- **repo-os-brownfield-intake** — Run only when explicitly requested: draft CURRENT_STATE, create first migration spec, handoff summary. Copy-paste prompt and full steps: see **APPLY.md** section "Run intake" and `.agents/skills/repo-os-brownfield-intake/SKILL.md`. Claude: `.claude/commands/intake-brownfield.md`. Do not invoke implicitly.
```

### This file (APPLY.md)

If you skipped **APPLY.md**, you won't have the "Run intake" prompt or this section. Copy `APPLY.md` from the overlay template (e.g. from the agentic-devkit package source or run the overlay again and choose to overwrite only APPLY.md), or keep this file open from the template repo so you can use the copy-paste prompt and the table above.

### Canonical and governance docs

| File | What to do |
|------|------------|
| **NORTHSTAR.md**, **CONSTITUTION.md**, **PRD.md** | No snippet required. When you run brownfield intake, the agent will **propose** additions or changes for your approval instead of overwriting. Merge as you see fit. Full template versions are in the overlay if you want to copy sections (e.g. CONSTITUTION articles, PRD structure). |
| **CURRENT_STATE.md** | No snippet required. The intake skill will draft or propose content; review and confirm before large edits. |
| **MIGRATION_GUARDRAILS.md** | If you kept your own file, append or merge the overlay rules: prefer strangler/adapter over rewrites; add characterization tests before refactoring fragile code; separate cleanup from behavior changes; preserve public contracts unless a spec authorizes a break; record durable changes as ADRs. Required workflow: read CURRENT_STATE → identify touched surfaces → add/confirm characterization tests → write spec/plan/tasks → implement smallest slice → verify no drift. See template `MIGRATION_GUARDRAILS.md` for full text. |
| **docs/governance/DOCS_SYSTEM.md** | Ensure your docs define the hierarchy and that `CURRENT_STATE.md` and `MIGRATION_GUARDRAILS.md` own legacy reality. Merge the overlay's "Canonical homes" and "Read order by task type" if helpful. See template for full file. |
| **docs/governance/context-registry.yaml** | If you had an existing registry, merge the overlay's schema (e.g. `canonical_entrypoint`, `owners`, `documents` with `CURRENT_STATE.md` and `MIGRATION_GUARDRAILS.md`). See template for full structure. |
| **specs/registry.yaml** | If you had existing specs, merge the overlay's `version`, `statuses` (proposed, active, blocked, implemented, superseded, archived), and `rules` (no two active specs touch same surface without dependency; superseded names replacement; etc.). Keep your existing spec entries; add new ones in the same format. See template for full file. |

## After applying

1. Fill **CURRENT_STATE.md** with an honest picture of the repo.
2. Keep **MIGRATION_GUARDRAILS.md** and **AGENTS.md** as the source of truth for agent behavior.
3. Use **specs/** for every non-trivial change; register each spec in `specs/registry.yaml`.
4. Do not duplicate policy in adapter files; they should only point at canonical docs.

## Design principle

**One canonical truth layer, thin tool adapters, zero duplicated policy.**
