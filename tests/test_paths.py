"""Tests for filesystem writing used by conversions."""

from pathlib import Path

from doc2markdown_desktop.paths import write_text_atomically


def test_atomic_writer_creates_parent_and_writes_utf8(tmp_path: Path) -> None:
    destination = tmp_path / "nested" / "report.md"
    write_text_atomically(destination, "# Hello\n")
    assert destination.read_text(encoding="utf-8") == "# Hello\n"
