"""Input validation and predictable Markdown output naming."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path


class OutputPolicy(StrEnum):
    """How to handle an output file that already exists."""

    OVERWRITE = "overwrite"
    SKIP = "skip"
    AUTO_RENAME = "auto_rename"


class ValidationError(ValueError):
    """Raised when an input or output path is unsuitable for conversion."""


def validate_input_path(path: Path) -> Path:
    """Validate and return an absolute regular-file path."""
    candidate = path.expanduser()
    if not candidate.exists():
        raise ValidationError("The file no longer exists.")
    if not candidate.is_file():
        raise ValidationError("Please select a file, not a folder.")
    try:
        with candidate.open("rb"):
            pass
    except OSError as error:
        raise ValidationError(f"The file cannot be read: {error}") from error
    return candidate.resolve()


def validate_output_directory(directory: Path) -> Path:
    """Validate an existing writable output directory."""
    candidate = directory.expanduser()
    if not candidate.exists() or not candidate.is_dir():
        raise ValidationError("The output folder does not exist.")
    if not candidate.exists():  # Kept explicit for clear future extension.
        raise ValidationError("The output folder does not exist.")
    return candidate.resolve()


def markdown_output_path(source: Path, output_directory: Path | None = None) -> Path:
    """Return the normal `.md` output path for *source*."""
    folder = output_directory if output_directory is not None else source.parent
    return folder / f"{source.stem}.md"


def auto_renamed_path(path: Path) -> Path:
    """Return the first available `name (N).md` path."""
    if not path.exists():
        return path
    index = 1
    while True:
        candidate = path.with_name(f"{path.stem} ({index}){path.suffix}")
        if not candidate.exists():
            return candidate
        index += 1


def resolve_output_path(path: Path, policy: OutputPolicy) -> Path | None:
    """Resolve an existing output using *policy*; `None` means skip."""
    if not path.exists() or policy is OutputPolicy.OVERWRITE:
        return path
    if policy is OutputPolicy.SKIP:
        return None
    return auto_renamed_path(path)
