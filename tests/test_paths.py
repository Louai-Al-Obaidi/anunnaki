"""Tests for filesystem writing used by conversions."""

from pathlib import Path

from doc2markdown_desktop.branding import application_icon_path, application_logo_path
from doc2markdown_desktop.paths import write_text_atomically
from doc2markdown_desktop.version import __version__


def test_atomic_writer_creates_parent_and_writes_utf8(tmp_path: Path) -> None:
    destination = tmp_path / "nested" / "report.md"
    write_text_atomically(destination, "# Hello\n")
    assert destination.read_text(encoding="utf-8") == "# Hello\n"


def test_branding_finds_assets_in_a_pyinstaller_bundle(tmp_path: Path, monkeypatch) -> None:
    """Assets are stored beneath the package directory in the frozen app."""
    assets = tmp_path / "doc2markdown_desktop" / "assets"
    assets.mkdir(parents=True)
    (assets / "anunnaki.ico").touch()
    (assets / "logo.png").touch()
    monkeypatch.setattr("sys._MEIPASS", str(tmp_path), raising=False)

    assert application_icon_path() == assets / "anunnaki.ico"
    assert application_logo_path() == assets / "logo.png"


def test_application_version_uses_semantic_versioning() -> None:
    assert __version__.count(".") == 2
