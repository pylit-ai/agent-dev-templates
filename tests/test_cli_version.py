from agentic_devkit import cli


def test_package_version_reads_distribution_metadata(monkeypatch):
    monkeypatch.setattr(cli.importlib.metadata, "version", lambda _: "9.9.9")
    assert cli._package_version() == "9.9.9"


def test_package_version_falls_back_when_distribution_missing(monkeypatch):
    def _raise_not_found(_: str) -> str:
        raise cli.importlib.metadata.PackageNotFoundError

    monkeypatch.setattr(cli.importlib.metadata, "version", _raise_not_found)
    assert cli._package_version() == "0+unknown"
