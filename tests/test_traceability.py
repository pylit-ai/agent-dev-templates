import json
from pathlib import Path

from agentic_devkit import cli
from agentic_devkit.traceability import compile_traceability


def _write_repo(root: Path) -> None:
    spec_dir = root / "specs" / "001-login"
    spec_dir.mkdir(parents=True)
    (root / "specs" / "registry.yaml").write_text(
        """version: 1
specs:
  - id: 001-login
    status: active
    owner: test
""",
        encoding="utf-8",
    )
    (spec_dir / "spec.md").write_text(
        """# spec.md - 001-login

## Acceptance criteria
- [ ] [REQ-login-001] Users can sign in with a valid token.
- [ ] [REQ-login-002] Invalid tokens are rejected.

## Required verifiers
- unit tests: `tests/test_login.py`
""",
        encoding="utf-8",
    )
    (spec_dir / "plan.md").write_text(
        """# plan.md - 001-login

## Evidence sources
- implementation: `src/login.py`
- verifier: `tests/test_login.py`

## Verification plan
- run: `pytest tests/test_login.py`
""",
        encoding="utf-8",
    )
    (spec_dir / "tasks.md").write_text(
        """# tasks.md - 001-login

## Tasks
- [x] T1 [REQ-login-001] Implement valid-token login in `src/login.py`
- [ ] T2 [REQ-login-002] Reject invalid tokens in `src/login.py`
""",
        encoding="utf-8",
    )
    (root / "src").mkdir()
    (root / "src" / "login.py").write_text(
        "# REQ-login-001\nVALID_TOKEN = 'ok'\n",
        encoding="utf-8",
    )
    (root / "tests").mkdir()
    (root / "tests" / "test_login.py").write_text(
        "# REQ-login-001\n\ndef test_valid_token_login():\n    assert True\n",
        encoding="utf-8",
    )


def test_compile_traceability_writes_graph_index_and_reports(tmp_path):
    _write_repo(tmp_path)

    result = compile_traceability(tmp_path)

    out_dir = tmp_path / "generated" / "traceability"
    assert result.graph_path == out_dir / "graph.json"
    assert (out_dir / "index.sqlite").exists()
    assert (out_dir / "coverage.md").exists()
    assert (out_dir / "verification-ledger.json").exists()
    assert (out_dir / "drift-report.md").exists()
    assert (out_dir / "forgotten-requirements.md").exists()

    graph = json.loads((out_dir / "graph.json").read_text(encoding="utf-8"))
    assert graph["metadata"]["branch"]
    assert graph["metadata"]["commit"]
    assert graph["requirements"]["REQ-login-001"]["status"] == "verified"
    assert graph["requirements"]["REQ-login-002"]["status"] == "forgotten"
    assert graph["requirements"]["REQ-login-001"]["tasks"][0]["id"] == "T1"


def test_cli_trace_inspect_reads_local_index(tmp_path, capsys):
    _write_repo(tmp_path)
    compile_traceability(tmp_path)

    rc = cli.cmd_trace_inspect("REQ-login-001", repo=tmp_path)
    out = capsys.readouterr()

    assert rc == 0
    assert "REQ-login-001" in out.out
    assert "verified" in out.out
    assert "tests/test_login.py" in out.out


def test_cli_trace_check_fails_for_missing_verifier_evidence(tmp_path, capsys):
    _write_repo(tmp_path)
    compile_traceability(tmp_path)

    rc = cli.cmd_trace_check(repo=tmp_path)
    out = capsys.readouterr()

    assert rc == 1
    assert "REQ-login-002" in out.err
    assert "missing implementation evidence" in out.err
    assert "missing verifier evidence" in out.err


def test_compile_respects_empty_registry_as_no_active_specs(tmp_path):
    spec_dir = tmp_path / "specs" / "001-draft"
    spec_dir.mkdir(parents=True)
    (tmp_path / "specs" / "registry.yaml").write_text(
        "version: 1\nspecs: []\n",
        encoding="utf-8",
    )
    (spec_dir / "spec.md").write_text(
        "- [ ] [REQ-draft-001] Draft requirement.\n",
        encoding="utf-8",
    )

    result = compile_traceability(tmp_path)

    assert result.graph["requirements"] == {}
