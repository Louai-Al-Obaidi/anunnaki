"""Application identity and packaged-resource helpers."""

from __future__ import annotations

import sys
from pathlib import Path

APP_NAME = "Anunnaki"
__version__ = "0.1.0"


def resource_path(*parts: str) -> Path:
    """Return a path to an application resource in source or frozen mode."""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base.joinpath(*parts)


def application_icon_path() -> Path | None:
    """Return the optional application icon path when it is bundled."""
    icon = resource_path("assets", "anunnaki.ico")
    return icon if icon.is_file() else None


def application_logo_path() -> Path | None:
    """Return the bundled PNG logo path when it is available."""
    logo = resource_path("assets", "logo.png")
    return logo if logo.is_file() else None
