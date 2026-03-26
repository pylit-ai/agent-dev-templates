from pathlib import Path

from agentic_devkit import cli


def test_cmd_init_uses_bundled_source_when_available(monkeypatch):
    monkeypatch.delenv("AGENTIC_DEV_GREENFIELD_SOURCE", raising=False)
    monkeypatch.setattr(cli, "_bundled_greenfield_path", lambda: Path("/tmp/bundled-greenfield"))

    seen = {}

    def _fake_run_copier(source: str, dest: Path) -> int:
        seen["source"] = source
        seen["dest"] = dest
        return 0

    monkeypatch.setattr(cli.Path, "is_dir", lambda _: True)
    monkeypatch.setattr(cli, "_run_copier", _fake_run_copier)

    rc = cli.cmd_init("demo-app")

    assert rc == 0
    assert seen["source"] == "/tmp/bundled-greenfield"
    assert seen["dest"] == Path("demo-app").resolve()


def test_cmd_init_rejects_placeholder_source(monkeypatch, capsys):
    monkeypatch.delenv("AGENTIC_DEV_GREENFIELD_SOURCE", raising=False)
    monkeypatch.setattr(cli, "_bundled_greenfield_path", lambda: Path("/tmp/missing-greenfield"))
    monkeypatch.setattr(cli.Path, "is_dir", lambda _: False)

    called = {"ran": False}

    def _fake_run_copier(source: str, dest: Path) -> int:
        called["ran"] = True
        return 0

    monkeypatch.setattr(cli, "_run_copier", _fake_run_copier)

    rc = cli.cmd_init("demo-app")
    out = capsys.readouterr()

    assert rc == 2
    assert called["ran"] is False
    assert "no usable greenfield template source found" in out.err.lower()
    assert "AGENTIC_DEV_GREENFIELD_SOURCE" in out.err


def test_cmd_init_uses_configured_source(monkeypatch):
    source = "gh:acme/agentic-dev-greenfield"
    monkeypatch.setenv("AGENTIC_DEV_GREENFIELD_SOURCE", source)

    seen = {}

    def _fake_run_copier(run_source: str, run_dest: Path) -> int:
        seen["source"] = run_source
        seen["dest"] = run_dest
        return 0

    monkeypatch.setattr(cli, "_run_copier", _fake_run_copier)

    rc = cli.cmd_init("demo-app")

    assert rc == 0
    assert seen["source"] == source
    assert seen["dest"] == Path("demo-app").resolve()
