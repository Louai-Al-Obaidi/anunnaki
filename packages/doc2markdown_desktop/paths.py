"""Safe filesystem operations used by the conversion pipeline."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path


def open_in_file_manager(path: Path) -> None:
    """Open *path* in the operating system's file manager."""
    if sys.platform == "win32":
        os.startfile(path)  # type: ignore[attr-defined]  # noqa: S606
    elif sys.platform == "darwin":
        subprocess.Popen(["open", str(path)])  # noqa: S603
    else:
        subprocess.Popen(["xdg-open", str(path)])  # noqa: S603


def write_text_atomically(path: Path, content: str) -> None:
    """Write UTF-8 text to *path* without leaving a partial final file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.stem}.", suffix=".tmp", dir=path.parent, text=True
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
        Path(temporary_name).replace(path)
    except BaseException:
        Path(temporary_name).unlink(missing_ok=True)
        raise
