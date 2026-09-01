"""Executable entry point for Anunnaki."""

from __future__ import annotations

import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen

from doc2markdown_desktop.branding import APP_NAME, application_icon_path, application_logo_path
from doc2markdown_desktop.version import __version__


def configure_windows_app_id() -> None:
    """Associate the running process with Anunnaki's Windows taskbar identity."""
    if sys.platform == "win32":
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(  # type: ignore[attr-defined]
            f"LouaiAlObaidi.Anunnaki.{__version__}"
        )


def main() -> int:
    """Start the Qt application and return its exit code."""
    configure_windows_app_id()
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    icon = application_icon_path()
    if icon:
        app.setWindowIcon(QIcon(str(icon)))

    # Load the heavier UI after an event loop iteration so a cold start gives
    # visible feedback instead of looking like a failed launch.
    logo = application_logo_path()
    splash = QSplashScreen(QPixmap(str(logo)) if logo else QPixmap())
    splash.showMessage(
        "Starting Anunnaki…",
        Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
    )
    splash.show()
    app.processEvents()

    def show_main_window() -> None:
        from doc2markdown_desktop.main_window import MainWindow

        window = MainWindow()
        if icon:
            window.setWindowIcon(QIcon(str(icon)))
        app.main_window = window  # type: ignore[attr-defined]
        window.show()
        splash.finish(window)

    QTimer.singleShot(0, show_main_window)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
