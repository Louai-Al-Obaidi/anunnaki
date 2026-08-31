"""Drag-and-drop target for one or more local files."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class DropArea(QFrame):
    """A large drop target that emits accepted local file paths."""

    files_dropped = Signal(list)

    def __init__(self, parent: object | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("dropArea")
        self.setAcceptDrops(True)
        self.setMinimumHeight(180)
        layout = QVBoxLayout(self)
        label = QLabel(
            "Drop files here\n<span>PDF, Office documents, spreadsheets, images, and more</span>"
        )
        label.setObjectName("dropLabel")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

    def dragEnterEvent(self, event: object) -> None:  # type: ignore[override]
        mime = event.mimeData()
        if mime.hasUrls() and any(url.isLocalFile() for url in mime.urls()):
            event.acceptProposedAction()

    def dropEvent(self, event: object) -> None:  # type: ignore[override]
        paths = [url.toLocalFile() for url in event.mimeData().urls() if url.isLocalFile()]
        if paths:
            self.files_dropped.emit(paths)
            event.acceptProposedAction()
