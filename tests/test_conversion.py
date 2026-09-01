"""Small end-to-end conversion smoke tests using the pinned MarkItDown engine."""

from pathlib import Path

from doc2markdown_desktop.conversion import convert_file


def test_plain_text_file_converts_to_markdown(tmp_path: Path) -> None:
    source = tmp_path / "notes.txt"
    destination = tmp_path / "notes.md"
    source.write_text("Anunnaki conversion smoke test", encoding="utf-8")

    convert_file(source, destination)

    assert destination.exists()
    assert "Anunnaki conversion smoke test" in destination.read_text(encoding="utf-8")
