"""The main window for selecting, queuing, and converting files."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, QThread, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .branding import APP_NAME, application_logo_path
from .drop_area import DropArea
from .paths import open_in_file_manager
from .style import APP_STYLESHEET
from .validation import (
    OutputPolicy,
    ValidationError,
    validate_input_path,
    validate_output_directory,
)
from .worker import ConversionRequest, ConversionWorker


class MainWindow(QMainWindow):
    """Top-level GUI for the Anunnaki conversion workflow."""

    def __init__(self) -> None:
        super().__init__()
        self._requests: list[ConversionRequest] = []
        self._thread: QThread | None = None
        self._worker: ConversionWorker | None = None
        self._last_output_folder: Path | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        self.setWindowTitle(f"{APP_NAME} — File to Markdown")
        self.resize(900, 650)
        self.setStyleSheet(APP_STYLESHEET)
        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(28, 24, 28, 24)
        heading_row = QHBoxLayout()
        logo_path = application_logo_path()
        if logo_path:
            logo = QLabel()
            logo.setPixmap(
                QPixmap(str(logo_path)).scaled(
                    64,
                    64,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
            heading_row.addWidget(logo)
        heading = QLabel(APP_NAME)
        heading.setStyleSheet("font-size: 25pt; font-weight: 700;")
        heading_row.addWidget(heading)
        heading_row.addStretch(1)
        layout.addLayout(heading_row)
        subtitle = QLabel(
            "Convert files to Markdown locally. Your files never leave this computer."
        )
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)

        self.drop_area = DropArea()
        self.drop_area.files_dropped.connect(self.add_paths)
        layout.addWidget(self.drop_area)
        choose = QPushButton("Choose files")
        choose.clicked.connect(self.choose_files)
        layout.addWidget(choose, alignment=Qt.AlignmentFlag.AlignHCenter)

        folder_row = QHBoxLayout()
        self.source_folder_checkbox = QCheckBox("Save next to each source file")
        self.source_folder_checkbox.setChecked(True)
        self.source_folder_checkbox.setToolTip(
            "Creates report.md beside report.pdf and preserves the base filename."
        )
        self.source_folder_checkbox.toggled.connect(self.on_source_folder_toggled)
        folder_row.addWidget(self.source_folder_checkbox)
        self.folder_label = QLabel("Output: Each input file’s folder")
        folder_row.addWidget(self.folder_label, 1)
        self.output_button = QPushButton("Choose output folder")
        self.output_button.setEnabled(False)
        self.output_button.clicked.connect(self.choose_output_folder)
        folder_row.addWidget(self.output_button)
        layout.addLayout(folder_row)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["File", "Status", "Details"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table, 1)
        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)
        self.message = QLabel("Add files to begin.")
        self.message.setObjectName("message")
        layout.addWidget(self.message)
        controls = QHBoxLayout()
        self.convert_button = QPushButton("Convert queue")
        self.convert_button.clicked.connect(self.start_conversion)
        controls.addWidget(self.convert_button)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setEnabled(False)
        self.cancel_button.clicked.connect(self.cancel_conversion)
        controls.addWidget(self.cancel_button)
        clear_button = QPushButton("Clear queue")
        clear_button.clicked.connect(self.clear_queue)
        controls.addWidget(clear_button)
        controls.addStretch(1)
        self.open_folder_button = QPushButton("Open output folder")
        self.open_folder_button.setEnabled(False)
        self.open_folder_button.clicked.connect(self.open_output_folder)
        controls.addWidget(self.open_folder_button)
        layout.addLayout(controls)
        self.setCentralWidget(root)

    @Slot()
    def choose_files(self) -> None:
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Choose files to convert", "", "All files (*.*)"
        )
        self.add_paths(paths)

    @Slot(list)
    def add_paths(self, paths: list[str]) -> None:
        existing = {request.source for request in self._requests}
        added = 0
        errors: list[str] = []
        for raw_path in paths:
            try:
                source = validate_input_path(Path(raw_path))
                if source in existing:
                    continue
                self._requests.append(ConversionRequest(source, self._last_output_folder))
                existing.add(source)
                self._add_row(source)
                added += 1
            except ValidationError as error:
                errors.append(f"{Path(raw_path).name}: {error}")
        self.message.setText(
            f"Added {added} file(s)."
            if not errors
            else "Some files could not be added: " + "; ".join(errors)
        )

    def _add_row(self, source: Path) -> None:
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(source.name))
        self.table.setItem(row, 1, QTableWidgetItem("Queued"))
        self.table.setItem(row, 2, QTableWidgetItem(str(source)))

    @Slot()
    def choose_output_folder(self) -> None:
        selected = QFileDialog.getExistingDirectory(self, "Choose output folder")
        if not selected:
            return
        try:
            self._last_output_folder = validate_output_directory(Path(selected))
        except ValidationError as error:
            QMessageBox.warning(self, APP_NAME, str(error))
            return
        self.folder_label.setText(f"Output: {self._last_output_folder}")
        self._requests = [
            ConversionRequest(item.source, self._last_output_folder) for item in self._requests
        ]

    @Slot()
    def on_source_folder_toggled(self, enabled: bool) -> None:
        """Switch between per-source output folders and one shared folder."""
        self.output_button.setEnabled(not enabled)
        if enabled:
            self._last_output_folder = None
            self.folder_label.setText("Output: Each input file’s folder")
            self._requests = [ConversionRequest(item.source) for item in self._requests]
        elif self._last_output_folder is None:
            self.folder_label.setText("Output: Choose a shared output folder")
        else:
            self.folder_label.setText(f"Output: {self._last_output_folder}")

    @Slot()
    def clear_queue(self) -> None:
        if self._thread is not None:
            return
        self._requests.clear()
        self.table.setRowCount(0)
        self.progress.setValue(0)
        self.message.setText("Queue cleared.")

    def _choose_conflict_policy(self) -> OutputPolicy | None:
        conflicts = []
        for request in self._requests:
            folder = request.output_directory or request.source.parent
            if (folder / f"{request.source.stem}.md").exists():
                conflicts.append(request.source.name)
        if not conflicts:
            # A file can appear after this scan; auto-renaming keeps the
            # no-overwrite guarantee even in that narrow race window.
            return OutputPolicy.AUTO_RENAME
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Existing Markdown files")
        dialog.setText(f"{len(conflicts)} output file(s) already exist. Choose how to handle them.")
        overwrite = dialog.addButton("Overwrite", QMessageBox.ButtonRole.DestructiveRole)
        rename = dialog.addButton("Auto-rename", QMessageBox.ButtonRole.AcceptRole)
        skip = dialog.addButton("Skip existing", QMessageBox.ButtonRole.ActionRole)
        dialog.addButton(QMessageBox.StandardButton.Cancel)
        dialog.exec()
        clicked = dialog.clickedButton()
        if clicked == overwrite:
            return OutputPolicy.OVERWRITE
        if clicked == rename:
            return OutputPolicy.AUTO_RENAME
        if clicked == skip:
            return OutputPolicy.SKIP
        return None

    @Slot()
    def start_conversion(self) -> None:
        if not self._requests:
            self.message.setText("Add one or more files before converting.")
            return
        if not self.source_folder_checkbox.isChecked() and self._last_output_folder is None:
            QMessageBox.information(
                self, APP_NAME, "Choose a shared output folder before converting."
            )
            return
        policy = self._choose_conflict_policy()
        if policy is None:
            return
        self.progress.setRange(0, len(self._requests))
        self.progress.setValue(0)
        self.convert_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self._thread = QThread(self)
        self._worker = ConversionWorker(self._requests, policy)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.item_started.connect(self.on_item_started)
        self._worker.item_finished.connect(self.on_item_finished)
        self._worker.progress.connect(self.on_progress)
        self._worker.finished.connect(self.on_finished)
        self._worker.finished.connect(self._thread.quit)
        self._thread.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._cleanup_thread)
        self._thread.start()

    @Slot()
    def cancel_conversion(self) -> None:
        if self._worker:
            self._worker.cancel()
            self.message.setText("Cancelling after the current file finishes…")
            self.cancel_button.setEnabled(False)

    @Slot(int, str)
    def on_item_started(self, index: int, status: str) -> None:
        self.table.item(index, 1).setText(status)

    @Slot(int, str, str)
    def on_item_finished(self, index: int, status: str, detail: str) -> None:
        self.table.item(index, 1).setText(status)
        self.table.item(index, 2).setText(detail)
        if status == "Complete":
            self._last_output_folder = Path(detail).parent
            self.open_folder_button.setEnabled(True)

    @Slot(int, int)
    def on_progress(self, current: int, total: int) -> None:
        self.progress.setRange(0, total)
        self.progress.setValue(current)

    @Slot(bool)
    def on_finished(self, cancelled: bool) -> None:
        completed = sum(
            self.table.item(row, 1).text() == "Complete" for row in range(self.table.rowCount())
        )
        failed = sum(
            self.table.item(row, 1).text() == "Failed" for row in range(self.table.rowCount())
        )
        prefix = "Conversion cancelled." if cancelled else "Conversion complete."
        self.message.setText(f"{prefix} {completed} succeeded, {failed} failed.")

    @Slot()
    def _cleanup_thread(self) -> None:
        self.convert_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self._worker = None
        if self._thread:
            self._thread.deleteLater()
        self._thread = None

    @Slot()
    def open_output_folder(self) -> None:
        if self._last_output_folder:
            open_in_file_manager(self._last_output_folder)

    def closeEvent(self, event: object) -> None:  # type: ignore[override]
        if self._thread and self._thread.isRunning():
            QMessageBox.information(
                self, APP_NAME, "Please wait for the active conversion to finish."
            )
            event.ignore()
            return
        event.accept()
