"""Tests for the single-source Anunnaki version configuration."""

import tomllib
from pathlib import Path

from doc2markdown_desktop.version import __version__


def test_project_version_is_loaded_from_the_application_version_module() -> None:
    project_root = Path(__file__).resolve().parents[1]
    configuration = tomllib.loads((project_root / "pyproject.toml").read_text(encoding="utf-8"))

    assert configuration["project"]["dynamic"] == ["version"]
    assert configuration["tool"]["setuptools"]["dynamic"]["version"] == {
        "attr": "doc2markdown_desktop.version.__version__"
    }


def test_application_version_is_a_three_part_release_version() -> None:
    assert __version__.split(".") == ["0", "1", "3"]
