# Changelog

All notable changes to this project are documented here.

## [0.1.0] - 2026-08-31

- First independent Anunnaki desktop release, based on Microsoft MarkItDown.
- Added a dark-friendly PySide6 Windows GUI for drag-and-drop and multi-file Markdown conversion.
- Added local conversion queues, per-file progress and errors, cancellation, and safe existing-output handling.
- Added per-source output by default (`report.pdf` becomes `report.md` beside it), with an optional shared output folder.
- Added PyInstaller packaging for `Anunnaki.exe`, application branding, tests, and Windows build automation.
