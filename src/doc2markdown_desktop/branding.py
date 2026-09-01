"""Application identity and packaged-resource helpers."""

from __future__ import annotations

import sys
from pathlib import Path

APP_NAME = "Anunnaki"
__version__ = "0.1.1"


def resource_path(*parts: str) -> Path:
    """Return a path to an application resource in source or frozen mode."""
    # PyInstaller preserves the destination supplied in the spec file.  The
    # bundled assets therefore live below ``doc2markdown_desktop`` inside
    # ``_MEIPASS``, while in source mode they are beside this module.
    if hasattr(sys, "_MEIPASS"):
        base = Path(sys._MEIPASS) / "doc2markdown_desktop"  # type: ignore[attr-defined]
    else:
        base = Path(__file__).resolve().parent
    return base.joinpath(*parts)


def application_icon_path() -> Path | None:
    """Return the optional application icon path when it is bundled."""
    icon = resource_path("assets", "anunnaki.ico")
    return icon if icon.is_file() else None


def application_logo_path() -> Path | None:
    """Return the bundled PNG logo path when it is available."""
    logo = resource_path("assets", "logo.png")
    return logo if logo.is_file() else None
