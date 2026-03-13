"""agentic-dev CLI: init, overlay, intake."""
import os
import subprocess
import sys
from pathlib import Path

from . import __version__
from .census import write_census_yaml

DEFAULT_GREENFIELD = "gh:your-org/agentic-dev-greenfield"
DEFAULT_BROWNFIELD = "gh:your-org/agentic-dev-brownfield-overlay"


def _greenfield_source() -> str:
    return os.environ.get("AGENTIC_DEV_GREENFIELD_SOURCE", DEFAULT_GREENFIELD)


def _brownfield_source() -> str:
    return os.environ.get("AGENTIC_DEV_BROWNFIELD_SOURCE", DEFAULT_BROWNFIELD)


def _run_copier(source: str, dest: Path) -> int:
    dest_str = str(dest.resolve())
    return subprocess.call([sys.executable, "-m", "copier", "copy", source, dest_str])


def cmd_init(dest: str) -> int:
    """Create a new greenfield repo from template."""
    source = _greenfield_source()
    dest_path = Path(dest).resolve()
    print(f"Running: copier copy {source} {dest_path}")
    return _run_copier(source, dest_path)


def cmd_overlay(path: str, intake: bool) -> int:
    """Apply brownfield overlay to an existing repo. With --intake, run census first."""
    path = Path(path).resolve()
    if not path.is_dir():
        print(f"Error: not a directory: {path}", file=sys.stderr)
        return 1
    if intake:
        out_path = write_census_yaml(path)
        print(f"Wrote {out_path}")
    source = _brownfield_source()
    print(f"Running: copier copy {source} {path}")
    return _run_copier(source, path)


def cmd_intake(path: str) -> int:
    """Print next-step instructions for brownfield intake (no Copier run)."""
    path = Path(path).resolve()
    if not path.is_dir():
        print(f"Error: not a directory: {path}", file=sys.stderr)
        return 1
    print("Brownfield intake — next steps:")
    print()
    print("1. Run preflight census (writes .agentic-bootstrap.yml):")
    print(f"   uvx agentic-devkit overlay {path} --intake")
    print("   or, after overlay: python .agents/skills/repo-os-brownfield-intake/scripts/repo_census.py . --format yaml -o .agentic-bootstrap.yml")
    print()
    print("2. Apply the overlay if you have not yet:")
    print(f"   uvx agentic-devkit overlay {path}")
    print()
    print("3. Run the repo-os-brownfield-intake skill (explicit only) to draft CURRENT_STATE.md and create the first spec.")
    print("   Use your agent's skill or .claude/commands/intake-brownfield.md.")
    return 0


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(
        prog="agentic-dev",
        description="Init, overlay, or intake for the agentic documentation OS templates.",
    )
    ap.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = ap.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Create a new repo from greenfield template")
    p_init.add_argument("dest", help="Destination path (e.g. my-new-repo)")
    p_init.set_defaults(func=lambda a: cmd_init(a.dest))

    p_overlay = sub.add_parser("overlay", help="Apply brownfield overlay to an existing repo")
    p_overlay.add_argument("path", nargs="?", default=".", help="Repo path (default: .)")
    p_overlay.add_argument("--intake", action="store_true", help="Run repo census first and write .agentic-bootstrap.yml")
    p_overlay.set_defaults(func=lambda a: cmd_overlay(a.path, a.intake))

    p_intake = sub.add_parser("intake", help="Show brownfield intake next-step instructions")
    p_intake.add_argument("path", nargs="?", default=".", help="Repo path (default: .)")
    p_intake.set_defaults(func=lambda a: cmd_intake(a.path))

    args = ap.parse_args()
    return args.func(args)
