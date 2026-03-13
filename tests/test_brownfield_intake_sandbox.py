"""
Test brownfield intake behavior in a sandbox where CURRENT_STATE, NORTHSTAR, PRD already exist.

Contract: intake must not overwrite those docs without user confirmation; it must
stop and ask / propose deltas. See .agents/skills/repo-os-brownfield-intake/SKILL.md.
"""
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

# Census logic (same as skill script); use package if available
try:
    from agentic_devkit.census import census
except ImportError:
    # Fallback when running from repo root without install: run census script in-process
    import importlib.util
    _script = REPO_ROOT / ".agents/skills/repo-os-brownfield-intake/scripts/repo_census.py"
    _spec = importlib.util.spec_from_file_location("repo_census", _script)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    census = _mod.census

SANDBOX = REPO_ROOT / "sandbox" / "brownfield-intake-test"
SKILL_MD = REPO_ROOT / ".agents" / "skills" / "repo-os-brownfield-intake" / "SKILL.md"

PROTECTED_DOCS = ("CURRENT_STATE.md", "NORTHSTAR.md", "PRD.md")


def test_sandbox_has_existing_docs():
    """Sandbox must contain the three protected docs so we can test no-overwrite behavior."""
    for name in PROTECTED_DOCS:
        path = SANDBOX / name
        assert path.exists(), f"Sandbox missing {name}; intake test requires pre-existing docs."
        content = path.read_text()
        assert "pre-existing" in content or "placeholder" in content.lower(), (
            f"{name} should contain placeholder content to detect overwrites."
        )


def test_census_runs_in_sandbox():
    """Repo census runs against sandbox and detects structure (e.g. pyproject.toml)."""
    data = census(SANDBOX)
    assert "manifests" in data
    assert "pyproject.toml" in data["manifests"], "Sandbox has pyproject.toml; census should find it."
    assert data["manifests"]  # at least one manifest


def test_skill_requires_stop_before_overwrite():
    """Skill must document: stop and ask before overwriting existing CURRENT_STATE, NORTHSTAR, PRD."""
    assert SKILL_MD.exists(), "Brownfield intake skill must exist."
    text = SKILL_MD.read_text()
    assert "Stop and ask before overwriting" in text, (
        "Skill must require stopping before overwriting existing docs."
    )
    assert "CURRENT_STATE.md" in text and "NORTHSTAR.md" in text and "PRD.md" in text, (
        "Skill must name the protected doc files."
    )
    assert "Do not overwrite" in text or "do not overwrite" in text, (
        "Skill must explicitly say do not overwrite (without confirmation)."
    )


def test_intake_policy_when_docs_exist():
    """
    When all three protected docs exist in a repo, intake policy must be 'propose delta / ask',
    not 'overwrite'. We encode this by: (1) sandbox has the docs, (2) skill says stop and ask.
    """
    for name in PROTECTED_DOCS:
        assert (SANDBOX / name).exists()
    policy = SKILL_MD.read_text()
    assert "propose" in policy.lower() or "ask" in policy.lower() or "confirmation" in policy.lower()
    # Ensure we would not overwrite: skill says "drafted (or delta proposed)"
    assert "delta" in policy.lower() or "propose" in policy.lower()
