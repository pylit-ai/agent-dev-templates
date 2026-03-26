"""Agentic dev CLI — init, overlay, and intake for agentic documentation OS templates."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("agentic-devkit")
except PackageNotFoundError:
    __version__ = "0+unknown"
