from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOTS = [
    REPO_ROOT / "templates" / "greenfield-dev-os" / "template",
    REPO_ROOT / "templates" / "brownfield-dev-overlay" / "template",
    REPO_ROOT / "src" / "agentic_devkit" / "templates" / "greenfield-dev-os" / "template",
    REPO_ROOT / "src" / "agentic_devkit" / "templates" / "brownfield-dev-overlay" / "template",
]


def test_spec_templates_include_atomic_requirement_ids():
    for root in TEMPLATE_ROOTS:
        spec_files = sorted((root / "specs").glob("*/spec.md"))
        assert spec_files, f"{root} must include a spec template"
        text = "\n".join(path.read_text(encoding="utf-8") for path in spec_files)
        assert "REQ-" in text
        assert "Traceability" in text


def test_plan_templates_include_evidence_sources():
    for root in TEMPLATE_ROOTS:
        plan_files = sorted((root / "specs").glob("*/plan.md"))
        assert plan_files, f"{root} must include a plan template"
        text = "\n".join(path.read_text(encoding="utf-8") for path in plan_files)
        assert "## Evidence sources" in text
        assert "verifier" in text.lower()


def test_task_templates_reference_requirement_ids():
    for root in TEMPLATE_ROOTS:
        task_files = sorted((root / "specs").glob("*/tasks.md"))
        assert task_files, f"{root} must include a task template"
        text = "\n".join(path.read_text(encoding="utf-8") for path in task_files)
        assert "[REQ-" in text
        assert "requirement ID" in text


def test_governance_documents_define_generated_traceability_artifacts():
    for root in TEMPLATE_ROOTS:
        text = (root / "docs" / "governance" / "DOCS_SYSTEM.md").read_text(encoding="utf-8")
        assert "generated/traceability/" in text
        assert "non-canonical generated artifacts" in text
