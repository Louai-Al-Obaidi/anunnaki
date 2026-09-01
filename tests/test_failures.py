"""Failure-path tests for conversion and input validation."""

from pathlib import Path

import pytest
from doc2markdown_desktop.conversion import ConversionError, convert_file
from doc2markdown_desktop.validation import ValidationError, validate_input_path


def test_missing_input_is_rejected_before_worker_conversion(tmp_path: Path) -> None:
    with pytest.raises(ValidationError, match="no longer exists"):
        validate_input_path(tmp_path / "missing.docx")


def test_conversion_service_wraps_engine_errors(tmp_path: Path) -> None:
    with pytest.raises(ConversionError):
        convert_file(tmp_path / "missing.txt", tmp_path / "output.md")
