# Publish workflow (maintainers)

This catalog holds the source of truth. Distribution is **one repo per consumable template** so Copier’s update semantics and GitHub template repos work correctly.

## Recommended setup

1. **This repo** (`agent-dev-templates`) = catalog with:
   - `templates/greenfield-dev-os/`
   - `templates/brownfield-dev-overlay/`
   - shared docs, scripts, and notepads

2. **Distribution repos** (separate repos, e.g. under your org):
   - `agentic-dev-greenfield` — contents of `templates/greenfield-dev-os/` (optional: GitHub template repo)
   - `agentic-dev-brownfield-overlay` — contents of `templates/brownfield-dev-overlay/`

## Publish steps

1. Copy template payload into the distribution repo:
   - For greenfield: copy `templates/greenfield-dev-os/` (including `copier.yml` and `template/`) to the root of `agentic-dev-greenfield`.
   - For brownfield: copy `templates/brownfield-dev-overlay/` to the root of `agentic-dev-brownfield-overlay`.

2. In each distribution repo, ensure:
   - `copier.yml` is at repo root.
   - `_subdirectory: template` so the template files live under `template/`.
   - A tag (e.g. `v0.1.0`) for versioned `copier update`.

3. Optional: In GitHub, set **Settings → General → Template repository** for the greenfield repo so users get “Use this template”.

## Script idea

A small script could:

- Read `templates/greenfield-dev-os/` and rsync/copy to a clone of `agentic-dev-greenfield`.
- Same for brownfield.
- Optionally run `copier copy` in a temp dir to validate rendering.

No script is committed here; add one under `scripts/` when needed.

## Tagging

Tag an explicit **v0.1.0** only after the hardening in `notepads/apply/review.md` is done (answers-file strategy, CI, governance checks). After that, distribution repos can use tags for `copier update` versioning.
