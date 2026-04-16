"""Local requirement-evidence graph compiler."""
from __future__ import annotations

import json
import re
import sqlite3
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REQ_ID_RE = re.compile(r"\bREQ-[A-Za-z0-9][A-Za-z0-9_.:-]*\b")
TASK_RE = re.compile(r"^-\s*\[(?P<done>[ xX])\]\s*(?P<id>[A-Za-z]+-\d+|[A-Za-z]+\d+)?:?\s*(?P<body>.*)$")
PATH_RE = re.compile(r"`([^`]+)`")
CODE_SUFFIXES = {
    ".c",
    ".cc",
    ".cpp",
    ".cs",
    ".go",
    ".java",
    ".js",
    ".jsx",
    ".kt",
    ".php",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".swift",
    ".ts",
    ".tsx",
}
SKIP_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "generated",
    "node_modules",
}


@dataclass(frozen=True)
class CompileResult:
    graph_path: Path
    index_path: Path
    coverage_path: Path
    ledger_path: Path
    drift_report_path: Path
    forgotten_report_path: Path
    graph: dict[str, Any]


def compile_traceability(repo: str | Path = ".", output_dir: str | Path | None = None) -> CompileResult:
    """Compile repository-local specs and evidence into generated traceability artifacts."""
    repo_path = Path(repo).resolve()
    out_dir = Path(output_dir).resolve() if output_dir else repo_path / "generated" / "traceability"
    out_dir.mkdir(parents=True, exist_ok=True)

    requirements = _collect_requirements(repo_path)
    _link_tasks(repo_path, requirements)
    _link_file_evidence(repo_path, requirements)
    _derive_statuses(requirements)

    graph = {
        "metadata": {
            "repo": str(repo_path),
            "branch": _git_value(repo_path, ["branch", "--show-current"]) or "unknown",
            "commit": _git_value(repo_path, ["rev-parse", "--short", "HEAD"]) or "unknown",
            "generated": True,
            "canonical": False,
        },
        "requirements": requirements,
        "edges": _build_edges(requirements),
    }

    graph_path = out_dir / "graph.json"
    index_path = out_dir / "index.sqlite"
    coverage_path = out_dir / "coverage.md"
    ledger_path = out_dir / "verification-ledger.json"
    drift_report_path = out_dir / "drift-report.md"
    forgotten_report_path = out_dir / "forgotten-requirements.md"

    graph_path.write_text(json.dumps(graph, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_index(index_path, requirements)
    coverage_path.write_text(_coverage_markdown(requirements), encoding="utf-8")
    ledger_path.write_text(json.dumps(_verification_ledger(requirements), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    drift_report_path.write_text(_drift_markdown(requirements), encoding="utf-8")
    forgotten_report_path.write_text(_forgotten_markdown(requirements), encoding="utf-8")

    return CompileResult(
        graph_path=graph_path,
        index_path=index_path,
        coverage_path=coverage_path,
        ledger_path=ledger_path,
        drift_report_path=drift_report_path,
        forgotten_report_path=forgotten_report_path,
        graph=graph,
    )


def load_requirement(requirement_id: str, repo: str | Path = ".") -> dict[str, Any] | None:
    index_path = Path(repo).resolve() / "generated" / "traceability" / "index.sqlite"
    if not index_path.exists():
        return None
    with sqlite3.connect(index_path) as conn:
        row = conn.execute(
            "select payload from requirements where id = ?",
            (requirement_id,),
        ).fetchone()
    if row is None:
        return None
    return json.loads(row[0])


def load_all_requirements(repo: str | Path = ".") -> list[dict[str, Any]]:
    index_path = Path(repo).resolve() / "generated" / "traceability" / "index.sqlite"
    if not index_path.exists():
        return []
    with sqlite3.connect(index_path) as conn:
        rows = conn.execute("select payload from requirements order by id").fetchall()
    return [json.loads(row[0]) for row in rows]


def diagnostics(repo: str | Path = ".") -> list[str]:
    messages: list[str] = []
    for req in load_all_requirements(repo):
        missing = req.get("missing") or []
        if missing:
            messages.append(f"{req['id']}: " + "; ".join(missing))
    return messages


def _collect_requirements(repo: Path) -> dict[str, dict[str, Any]]:
    requirements: dict[str, dict[str, Any]] = {}
    specs_root = repo / "specs"
    for spec_id in _active_spec_ids(specs_root):
        spec_path = specs_root / spec_id / "spec.md"
        if not spec_path.exists():
            continue
        for req_id, text, line_no in _parse_requirements(spec_path):
            requirements[req_id] = {
                "id": req_id,
                "text": text,
                "source": _rel(repo, spec_path),
                "line": line_no,
                "spec": spec_id,
                "tasks": [],
                "code_entities": [],
                "verifiers": [],
                "verifier_strategy": _verifier_strategy(spec_path, specs_root / spec_id / "plan.md"),
                "status": "planned",
                "missing": [],
            }
    return dict(sorted(requirements.items()))


def _active_spec_ids(specs_root: Path) -> list[str]:
    registry = specs_root / "registry.yaml"
    ids: list[str] = []
    if registry.exists():
        current_id: str | None = None
        current_status: str | None = None
        for raw in registry.read_text(encoding="utf-8").splitlines() + ["- id:"]:
            line = raw.strip()
            if line.startswith("- id:"):
                if current_id and current_status == "active":
                    ids.append(current_id)
                current_id = line.split(":", 1)[1].strip().strip("'\"") or None
                current_status = None
            elif line.startswith("status:"):
                current_status = line.split(":", 1)[1].strip().strip("'\"")
        return ids
    if not specs_root.exists():
        return []
    return sorted(path.name for path in specs_root.iterdir() if (path / "spec.md").exists())


def _parse_requirements(spec_path: Path) -> list[tuple[str, str, int]]:
    parsed: list[tuple[str, str, int]] = []
    for line_no, raw in enumerate(spec_path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = raw.strip()
        if stripped.startswith("### Requirement:"):
            ids = REQ_ID_RE.findall(stripped)
            if ids:
                text = REQ_ID_RE.sub("", stripped.split(":", 1)[1]).strip(" []:-")
                parsed.append((ids[0], text, line_no))
            continue
        if stripped.startswith("- ["):
            ids = REQ_ID_RE.findall(stripped)
            if ids:
                text = REQ_ID_RE.sub("", stripped).strip()
                text = re.sub(r"^-\s*\[[ xX]\]\s*", "", text).strip(" :-")
                parsed.append((ids[0], text, line_no))
    return parsed


def _verifier_strategy(spec_path: Path, plan_path: Path) -> list[str]:
    strategies: list[str] = []
    for path in (spec_path, plan_path):
        if not path.exists():
            continue
        in_section = False
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if line.startswith("## "):
                heading = line.lower()
                in_section = "verifier" in heading or "verification" in heading or "evidence" in heading
                continue
            if in_section and line.startswith("-"):
                strategies.append(line.lstrip("- ").strip())
    return sorted(set(strategies))


def _link_tasks(repo: Path, requirements: dict[str, dict[str, Any]]) -> None:
    for tasks_path in sorted((repo / "specs").glob("*/tasks.md")):
        for raw in tasks_path.read_text(encoding="utf-8").splitlines():
            match = TASK_RE.match(raw.strip())
            if not match:
                continue
            body = match.group("body")
            req_ids = REQ_ID_RE.findall(body)
            if not req_ids:
                continue
            task = {
                "id": match.group("id") or "task",
                "done": match.group("done").lower() == "x",
                "text": body,
                "source": _rel(repo, tasks_path),
                "paths": PATH_RE.findall(body),
            }
            for req_id in req_ids:
                if req_id in requirements:
                    requirements[req_id]["tasks"].append(task)
                    if task["done"]:
                        for raw_path in task["paths"]:
                            evidence_path = (repo / raw_path).resolve()
                            if evidence_path.exists() and _is_code_file(evidence_path) and not _is_test_file(evidence_path):
                                _append_unique(requirements[req_id]["code_entities"], _rel(repo, evidence_path))


def _link_file_evidence(repo: Path, requirements: dict[str, dict[str, Any]]) -> None:
    if not requirements:
        return
    ids = set(requirements)
    for path in sorted(_walk_evidence_files(repo)):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        present = ids.intersection(REQ_ID_RE.findall(text))
        if not present:
            continue
        rel = _rel(repo, path)
        for req_id in present:
            if _is_test_file(path):
                _append_unique(requirements[req_id]["verifiers"], rel)
            elif _is_code_file(path):
                _append_unique(requirements[req_id]["code_entities"], rel)


def _derive_statuses(requirements: dict[str, dict[str, Any]]) -> None:
    for req in requirements.values():
        missing: list[str] = []
        if not req["verifier_strategy"]:
            missing.append("missing verifier strategy")
        if not req["code_entities"]:
            missing.append("missing implementation evidence")
        if not req["verifiers"]:
            missing.append("missing verifier evidence")
        req["missing"] = missing
        if req["code_entities"] and req["verifiers"]:
            req["status"] = "verified"
        elif req["code_entities"]:
            req["status"] = "implemented"
        elif missing:
            req["status"] = "forgotten"
        else:
            req["status"] = "planned"


def _build_edges(requirements: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    for req in requirements.values():
        for task in req["tasks"]:
            edges.append({"from": req["id"], "to": task["id"], "type": "ADDRESSED_BY"})
        for path in req["code_entities"]:
            edges.append({"from": req["id"], "to": path, "type": "IMPLEMENTED_BY"})
        for path in req["verifiers"]:
            edges.append({"from": req["id"], "to": path, "type": "VERIFIED_BY"})
    return sorted(edges, key=lambda edge: (edge["from"], edge["type"], edge["to"]))


def _write_index(index_path: Path, requirements: dict[str, dict[str, Any]]) -> None:
    if index_path.exists():
        index_path.unlink()
    with sqlite3.connect(index_path) as conn:
        conn.execute("create table requirements (id text primary key, status text not null, payload text not null)")
        conn.execute("create table diagnostics (requirement_id text not null, message text not null)")
        for req_id, req in requirements.items():
            conn.execute(
                "insert into requirements (id, status, payload) values (?, ?, ?)",
                (req_id, req["status"], json.dumps(req, sort_keys=True)),
            )
            for message in req["missing"]:
                conn.execute(
                    "insert into diagnostics (requirement_id, message) values (?, ?)",
                    (req_id, message),
                )


def _coverage_markdown(requirements: dict[str, dict[str, Any]]) -> str:
    lines = [
        "# Traceability Coverage",
        "",
        "Generated artifact. Canonical requirements remain in `specs/<id>/spec.md`.",
        "",
        "| Requirement | Status | Implementation | Verifiers |",
        "| --- | --- | --- | --- |",
    ]
    for req in requirements.values():
        code = ", ".join(req["code_entities"]) or "-"
        verifiers = ", ".join(req["verifiers"]) or "-"
        lines.append(f"| {req['id']} | {req['status']} | {code} | {verifiers} |")
    return "\n".join(lines) + "\n"


def _verification_ledger(requirements: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        req_id: {
            "status": req["status"],
            "verified": req["status"] == "verified",
            "verifiers": req["verifiers"],
            "missing": req["missing"],
        }
        for req_id, req in requirements.items()
    }


def _drift_markdown(requirements: dict[str, dict[str, Any]]) -> str:
    lines = ["# Traceability Drift", "", "Generated artifact. Review missing evidence before merge.", ""]
    drifting = [req for req in requirements.values() if req["status"] not in {"verified", "planned"}]
    if not drifting:
        lines.append("No drift detected.")
    for req in drifting:
        lines.append(f"- {req['id']}: {', '.join(req['missing'])}")
    return "\n".join(lines) + "\n"


def _forgotten_markdown(requirements: dict[str, dict[str, Any]]) -> str:
    lines = ["# Forgotten Requirements", "", "Generated artifact. Requirements listed here need evidence links.", ""]
    forgotten = [req for req in requirements.values() if req["status"] == "forgotten"]
    if not forgotten:
        lines.append("No forgotten requirements detected.")
    for req in forgotten:
        lines.append(f"- {req['id']}: {', '.join(req['missing'])}")
    return "\n".join(lines) + "\n"


def _walk_evidence_files(repo: Path) -> list[Path]:
    files: list[Path] = []
    for path in repo.rglob("*"):
        if not path.is_file():
            continue
        if SKIP_DIRS.intersection(path.relative_to(repo).parts):
            continue
        if path.suffix in CODE_SUFFIXES or _is_test_file(path):
            files.append(path)
    return files


def _is_test_file(path: Path) -> bool:
    parts = set(path.parts)
    return "tests" in parts or path.name.startswith("test_") or path.name.endswith("_test.py")


def _is_code_file(path: Path) -> bool:
    return path.suffix in CODE_SUFFIXES


def _append_unique(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)
        values.sort()


def _rel(repo: Path, path: Path) -> str:
    return path.resolve().relative_to(repo).as_posix()


def _git_value(repo: Path, args: list[str]) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=repo, text=True, stderr=subprocess.DEVNULL).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""
