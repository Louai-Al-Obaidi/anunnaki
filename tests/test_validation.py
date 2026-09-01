"""Tests for safe file validation and output conflict policies."""

from pathlib import Path

import pytest
from doc2markdown_desktop.validation import (
    OutputPolicy,
    ValidationError,
    auto_renamed_path,
    markdown_output_path,
    resolve_output_path,
    validate_input_path,
)


def test_output_path_preserves_base_filename(tmp_path: Path) -> None:
    assert markdown_output_path(tmp_path / "report.final.pdf") == tmp_path / "report.final.md"


def test_custom_output_directory_is_used(tmp_path: Path) -> None:
    output = tmp_path / "markdown"
    assert markdown_output_path(tmp_path / "report.pdf", output) == output / "report.md"


def test_auto_rename_finds_next_available_name(tmp_path: Path) -> None:
    original = tmp_path / "report.md"
    original.touch()
    (tmp_path / "report (1).md").touch()
    assert auto_renamed_path(original) == tmp_path / "report (2).md"


@pytest.mark.parametrize(
    ("policy", "expected"),
    [
        (OutputPolicy.OVERWRITE, "report.md"),
        (OutputPolicy.SKIP, None),
        (OutputPolicy.AUTO_RENAME, "report (1).md"),
    ],
)
def test_existing_output_policy(tmp_path: Path, policy: OutputPolicy, expected: str | None) -> None:
    output = tmp_path / "report.md"
    output.touch()
    result = resolve_output_path(output, policy)
    assert result is None if expected is None else result.name == expected


def test_missing_file_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(ValidationError, match="no longer exists"):
        validate_input_path(tmp_path / "missing.pdf")


def test_directory_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(ValidationError, match="not a folder"):
        validate_input_path(tmp_path)
