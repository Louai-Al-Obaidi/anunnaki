"""Background Qt worker that converts each queue item independently."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from threading import Event

from PySide6.QtCore import QObject, Signal, Slot

from .conversion import ConversionError, convert_file
from .validation import OutputPolicy, markdown_output_path, resolve_output_path, validate_input_path


@dataclass(frozen=True)
class ConversionRequest:
    """A source item and the output folder selected for its conversion."""

    source: Path
    output_directory: Path | None = None


class ConversionWorker(QObject):
    """Convert requests sequentially in a worker thread and report every outcome."""

    item_started = Signal(int, str)
    item_finished = Signal(int, str, str)
    progress = Signal(int, int)
    finished = Signal(bool)

    def __init__(self, requests: list[ConversionRequest], policy: OutputPolicy) -> None:
        super().__init__()
        self._requests = requests
        self._policy = policy
        self._cancel = Event()

    @Slot()
    def run(self) -> None:
        """Run conversions, preserving failures as per-file results."""
        for index, request in enumerate(self._requests):
            if self._cancel.is_set():
                self.item_finished.emit(index, "Cancelled", "Conversion cancelled")
                self.progress.emit(index + 1, len(self._requests))
                continue
            self.item_started.emit(index, "Converting")
            try:
                source = validate_input_path(request.source)
                destination = markdown_output_path(source, request.output_directory)
                destination = resolve_output_path(destination, self._policy)
                if destination is None:
                    self.item_finished.emit(index, "Skipped", "Output already exists")
                else:
                    convert_file(source, destination)
                    self.item_finished.emit(index, "Complete", str(destination))
            except (OSError, ConversionError, ValueError) as error:
                self.item_finished.emit(index, "Failed", str(error))
            self.progress.emit(index + 1, len(self._requests))
        self.finished.emit(self._cancel.is_set())

    @Slot()
    def cancel(self) -> None:
        """Request cancellation after the currently active conversion completes."""
        self._cancel.set()
