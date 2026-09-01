"""Regression tests for predictable Markdown output conflict handling."""

from pathlib import Path

from doc2markdown_desktop.validation import OutputPolicy, resolve_output_path


def test_auto_rename_preserves_existing_markdown_files(tmp_path: Path) -> None:
    destination = tmp_path / "report.md"
    destination.write_text("existing", encoding="utf-8")
    (tmp_path / "report (1).md").write_text("existing", encoding="utf-8")

    assert resolve_output_path(destination, OutputPolicy.AUTO_RENAME) == tmp_path / "report (2).md"


def test_overwrite_policy_returns_the_original_destination(tmp_path: Path) -> None:
    destination = tmp_path / "report.md"
    destination.touch()

    assert resolve_output_path(destination, OutputPolicy.OVERWRITE) == destination
