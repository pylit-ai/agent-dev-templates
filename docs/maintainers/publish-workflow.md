# Publish workflow (maintainers)

This catalog holds the source of truth. Distribution is **one repo per consumable template** so Copier’s update semantics and GitHub template repos work correctly.

## Recommended setup

1. **This repo** (`agentic-devkit`) = catalog with:
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

## Publishing the CLI (PyPI)

This repo’s `pyproject.toml` uses **`name = "agentic-devkit"`** so that when you publish to PyPI, `uvx agentic-devkit` runs the CLI (script name remains `agentic-dev`).

### Trusted Publishing (GitHub Actions)

The repo includes **`.github/workflows/publish-pypi.yml`**, which publishes to PyPI on **release published** or **workflow_dispatch**, using OIDC (no stored token).

**When adding the trusted publisher on PyPI**, use:

| PyPI field | Value |
|------------|--------|
| **Workflow name** | `publish-pypi.yml` |
| **Environment name** | `pypi` (optional but recommended) |

- **Workflow name** = filename of the workflow under `.github/workflows/`. Must match exactly.
- **Environment name** = GitHub Actions environment used by the publish job. Use `pypi` so you can add an environment in **Settings → Environments** with protection rules (e.g. required reviewers, or limit who can deploy). Create the `pypi` environment in the repo if you use this.

After adding the trusted publisher on PyPI, create a **GitHub release** (or run the workflow manually); the job will build and run `uv publish` using OIDC.

### PyPI name: hyphens and good names

- **Hyphens are good.** PyPI normalizes project names; we use **`agentic-devkit`**. The *import* name stays `agentic_dev`; we use `[project.scripts] agentic-dev = "agentic_dev.cli:main"` so the installed command is `agentic-dev`.

### Is the name available?

- **Quick check:** Open **https://pypi.org/project/agentic-devkit/** in a browser. If you get a **404**, the name is free.
- **From the shell:** `pip index versions agentic-devkit` — if it errors (no such package), the name is available.

### Where to get a PyPI token (manual publish)

If you publish from the command line instead of Trusted Publishing:

1. **Log in** at [pypi.org](https://pypi.org).
2. Open **Account settings**: [https://pypi.org/manage/account/](https://pypi.org/manage/account/).
3. In the **API tokens** section, click **“Add API token”**.
4. Give it a label (e.g. “Publish agentic-devkit from laptop”), choose scope (entire account or **Project: agentic-devkit**).
5. **Copy the token immediately** (it starts with `pypi-`). You need a **verified email** on the account. See [PyPI: API tokens](https://pypi.org/help/#api-tokens).

### How to publish

1. **Bump version** (optional):  
   `uv version --bump patch`  
   or set it explicitly in `pyproject.toml` and tag: `git tag v0.1.0`.

2. **Build:**  
   `uv build`  
   Artifacts go into `dist/`.

3. **Publish to Test PyPI first (recommended):**  
   - Create an account at [test.pypi.org](https://test.pypi.org) and create an API token there.  
   - Add a [tool.uv.index] for Test PyPI with `publish-url`, or use:  
     `uv publish --index-url https://test.pypi.org/legacy/ --token <test-token>`  
   - Install from Test PyPI to verify:  
     `uv pip install --index-url https://test.pypi.org/simple/ agentic-devkit`.

4. **Publish to PyPI:**  
   `UV_PUBLISH_TOKEN=pypi-xxxx uv publish`  
   or  
   `uv publish --token pypi-xxxx`  
   (PyPI uses username `__token__` and the token as password; `uv publish` does this when you pass `--token`.)

5. **Verify:**  
   `uvx agentic-devkit --version`  
   (after a short delay for the index to update).

References: [uv: Building and publishing](https://docs.astral.sh/uv/guides/package/), [PyPI Help: API tokens](https://pypi.org/help/#api-tokens).
