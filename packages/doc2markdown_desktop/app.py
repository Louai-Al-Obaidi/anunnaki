"""Executable entry point for Anunnaki."""

from __future__ import annotations

import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from doc2markdown_desktop.branding import APP_NAME, application_icon_path
from doc2markdown_desktop.main_window import MainWindow


def main() -> int:
    """Start the Qt application and return its exit code."""
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    icon = application_icon_path()
    if icon:
        app.setWindowIcon(QIcon(str(icon)))
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
