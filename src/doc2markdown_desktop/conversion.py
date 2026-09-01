"""Local MarkItDown conversion service."""

from __future__ import annotations

from pathlib import Path

from .paths import write_text_atomically


class ConversionError(RuntimeError):
    """Raised when MarkItDown cannot convert a source file."""


def convert_file(source: Path, destination: Path) -> None:
    """Convert *source* with MarkItDown and save UTF-8 Markdown to *destination*."""
    try:
        from markitdown import MarkItDown

        result = MarkItDown().convert(str(source))
        content = result.text_content
    except Exception as error:
        raise ConversionError(str(error) or error.__class__.__name__) from error
    write_text_atomically(destination, content)
