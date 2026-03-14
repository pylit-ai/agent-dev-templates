#!/usr/bin/env python3
"""
Write a minimal repo census for Copier _external_data or skill input.
Scans repo root for manifests, CI, lockfiles, and doc paths. Uses stdlib only.

Usage:
  python repo_census.py [REPO_PATH]              # print JSON to stdout
  python repo_census.py [REPO_PATH] --format yaml # print YAML to stdout
  python repo_census.py [REPO_PATH] --output .agentic-bootstrap.yml  # write YAML file

For Copier: run before applying the brownfield overlay so the template can use
_external_data.census to prefill inferred stack (e.g. in CURRENT_STATE).
"""
from pathlib import Path
import argparse
import json


def census(root: Path) -> dict:
    root = Path(root).resolve()
    out = {
        "manifests": [],
        "ci": [],
        "lockfiles": [],
        "has_makefile": (root / "Makefile").exists(),
        "test_dirs": [],
        "docs_dirs": [],
    }
    for p in root.iterdir():
        if p.is_file():
            if p.name in (
                "package.json",
                "pyproject.toml",
                "Cargo.toml",
                "go.mod",
                "requirements.txt",
            ):
                out["manifests"].append(p.name)
            if p.name in (
                "uv.lock",
                "package-lock.json",
                "yarn.lock",
                "Cargo.lock",
                "poetry.lock",
            ):
                out["lockfiles"].append(p.name)
        elif p.is_dir() and not p.name.startswith("."):
            if p.name in ("tests", "test", "__tests__", "spec"):
                out["test_dirs"].append(p.name)
            if p.name == "docs":
                out["docs_dirs"].append(p.name)
    ci = root / ".github" / "workflows"
    if ci.exists():
        out["ci"].extend(
            f.name for f in ci.iterdir() if f.suffix in (".yml", ".yaml")
        )
    return out


def to_yaml(obj, indent=0):
    """Minimal YAML dump (stdlib only). Handles dict, list, bool, str, int."""
    spaces = "  " * indent
    if isinstance(obj, dict):
        lines = []
        for k, v in obj.items():
            if isinstance(v, (dict, list)) and v:
                lines.append(f"{spaces}{k}:")
                lines.append(to_yaml(v, indent + 1))
            else:
                if v is True:
                    v = "true"
                elif v is False:
                    v = "false"
                elif isinstance(v, str) and (":" in v or "\n" in v or v == ""):
                    v = repr(v)
                lines.append(f"{spaces}{k}: {v}")
        return "\n".join(lines)
    if isinstance(obj, list):
        if not obj:
            return f"{spaces}[]"
        lines = []
        for item in obj:
            lines.append(f"{spaces}- {item}")
        return "\n".join(lines)
    return str(obj)


def main():
    ap = argparse.ArgumentParser(description="Repo census for agentic bootstrap")
    ap.add_argument("repo", nargs="?", default=".", help="Repo root path")
    ap.add_argument(
        "--format",
        choices=("json", "yaml"),
        default="json",
        help="Output format (default: json)",
    )
    ap.add_argument(
        "--output",
        "-o",
        metavar="FILE",
        help="Write output to FILE (default: stdout)",
    )
    args = ap.parse_args()
    data = census(args.repo)
    if args.format == "yaml":
        out = to_yaml(data)
    else:
        out = json.dumps(data, indent=2)
    if args.output:
        Path(args.output).write_text(out)
    else:
        print(out)


if __name__ == "__main__":
    main()
