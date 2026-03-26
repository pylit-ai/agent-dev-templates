# Agentic-devkit: common dev and release tasks. Uses uv for Python/version.
# Usage: make [target]. Default: make help.

.PHONY: help sync sync-templates sync-greenfield sync-overlay test verify version bump-patch bump-minor bump-major tag release-patch release-minor release-major clean

# Default target
help:
	@echo "Targets:"
	@echo "  make sync          - uv sync (install deps)"
	@echo "  make sync-templates - copy both greenfield and brownfield template bundles into src/agentic_devkit/templates"
	@echo "  make sync-greenfield - copy templates/greenfield-dev-os into src/agentic_devkit/templates (bundled greenfield)"
	@echo "  make sync-overlay  - copy templates/brownfield-dev-overlay into src/agentic_devkit/templates (bundled overlay)"
	@echo "  make test          - run pytest"
	@echo "  make verify        - governance + template copy checks (CI-style)"
	@echo "  make version       - show current version from pyproject.toml"
	@echo "  make bump-patch    - bump patch version (0.x.y -> 0.x.y+1)"
	@echo "  make bump-minor    - bump minor version (0.x.y -> 0.x+1.0)"
	@echo "  make bump-major    - bump major version (x.y.z -> x+1.0.0)"
	@echo "  make tag           - create git tag v<VERSION> from current version"
	@echo "  make release-patch - bump patch, commit, tag, push (tag push triggers PyPI); optional: gh release create"
	@echo "  make release-minor - bump minor, commit, tag, push"
	@echo "  make release-major - bump major, commit, tag, push"
	@echo "  make clean         - remove dist, build, .egg-info, __pycache__"

sync:
	uv sync

sync-templates: sync-greenfield sync-overlay

sync-greenfield:
	@rm -rf src/agentic_devkit/templates/greenfield-dev-os
	@cp -R templates/greenfield-dev-os src/agentic_devkit/templates/
	@echo "Synced templates/greenfield-dev-os -> src/agentic_devkit/templates/greenfield-dev-os"

sync-overlay:
	@rm -rf src/agentic_devkit/templates/brownfield-dev-overlay
	@cp -R templates/brownfield-dev-overlay src/agentic_devkit/templates/
	@echo "Synced templates/brownfield-dev-overlay -> src/agentic_devkit/templates/brownfield-dev-overlay"

test:
	uv run pytest tests/ -v

verify: sync
	./scripts/check-governance
	./scripts/verify-template greenfield-dev-os
	./scripts/verify-template brownfield-dev-overlay

version:
	@uv version 2>/dev/null || grep '^version' pyproject.toml | sed 's/.*= *"\(.*\)".*/\1/'

bump-patch:
	uv version --bump patch

bump-minor:
	uv version --bump minor

bump-major:
	uv version --bump major

# VERSION is the current version from pyproject (e.g. 0.1.2)
VERSION := $(shell grep '^version' pyproject.toml | sed 's/.*= *"\(.*\)".*/\1/')

tag:
	@if [ -z "$(VERSION)" ]; then echo "Could not read version from pyproject.toml"; exit 1; fi
	git tag -a v$(VERSION) -m "Release v$(VERSION)"
	@echo "Created tag v$(VERSION). Push with: git push origin v$(VERSION)"

release-patch: sync test verify
	@if [ -n "$$(git status --porcelain)" ]; then echo "Working tree not clean; commit or stash first."; exit 1; fi
	uv version --bump patch
	@V=$$(grep '^version' pyproject.toml | sed 's/.*= *"\(.*\)".*/\1/'); \
	git add pyproject.toml uv.lock; \
	git commit -m "chore(release): v$$V"; \
	git tag -a v$$V -m "Release v$$V"; \
	git push origin main; \
	git push origin v$$V; \
	if command -v gh >/dev/null 2>&1; then gh release create v$$V --notes "Release v$$V"; else echo "Pushed v$$V. PyPI publish runs on tag push. Install 'gh' to also create a GitHub Release."; fi

release-minor: sync test verify
	@if [ -n "$$(git status --porcelain)" ]; then echo "Working tree not clean; commit or stash first."; exit 1; fi
	uv version --bump minor
	@V=$$(grep '^version' pyproject.toml | sed 's/.*= *"\(.*\)".*/\1/'); \
	git add pyproject.toml uv.lock; \
	git commit -m "chore(release): v$$V"; \
	git tag -a v$$V -m "Release v$$V"; \
	git push origin main; \
	git push origin v$$V; \
	if command -v gh >/dev/null 2>&1; then gh release create v$$V --notes "Release v$$V"; else echo "Pushed v$$V. PyPI publish runs on tag push."; fi

release-major: sync test verify
	@if [ -n "$$(git status --porcelain)" ]; then echo "Working tree not clean; commit or stash first."; exit 1; fi
	uv version --bump major
	@V=$$(grep '^version' pyproject.toml | sed 's/.*= *"\(.*\)".*/\1/'); \
	git add pyproject.toml uv.lock; \
	git commit -m "chore(release): v$$V"; \
	git tag -a v$$V -m "Release v$$V"; \
	git push origin main; \
	git push origin v$$V; \
	if command -v gh >/dev/null 2>&1; then gh release create v$$V --notes "Release v$$V"; else echo "Pushed v$$V. PyPI publish runs on tag push."; fi

clean:
	rm -rf dist/ build/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
