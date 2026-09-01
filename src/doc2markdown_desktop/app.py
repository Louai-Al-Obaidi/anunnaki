"""Executable entry point for Anunnaki."""

from __future__ import annotations

import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from doc2markdown_desktop.branding import APP_NAME, application_icon_path
from doc2markdown_desktop.main_window import MainWindow


def configure_windows_app_id() -> None:
    """Associate the running process with Anunnaki's Windows taskbar identity."""
    if sys.platform == "win32":
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(  # type: ignore[attr-defined]
            "LouaiAlObaidi.Anunnaki.0.1.1"
        )


def main() -> int:
    """Start the Qt application and return its exit code."""
    configure_windows_app_id()
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    icon = application_icon_path()
    if icon:
        app.setWindowIcon(QIcon(str(icon)))
    window = MainWindow()
    if icon:
        window.setWindowIcon(QIcon(str(icon)))
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
