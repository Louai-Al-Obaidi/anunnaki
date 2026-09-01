"""Offline smoke tests for common document conversions using upstream fixtures."""

from pathlib import Path

import pytest
from doc2markdown_desktop.conversion import convert_file


@pytest.mark.parametrize("extension", ["pdf", "docx", "xlsx", "pptx"])
def test_common_document_fixture_converts_to_markdown(tmp_path: Path, extension: str) -> None:
    project_root = Path(__file__).resolve().parents[1]
    source = project_root / "packages" / "markitdown" / "tests" / "test_files" / f"test.{extension}"
    destination = tmp_path / f"converted-{extension}.md"

    convert_file(source, destination)

    assert destination.exists()
    assert destination.read_text(encoding="utf-8").strip()
