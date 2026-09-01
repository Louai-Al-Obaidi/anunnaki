# Changelog

All notable changes to this project are documented here.

## [Unreleased]

## [0.1.3] - 2026-09-01

### Added

- Namespaced release tags (`anunnaki-vX.Y.Z`) and a Windows release workflow
  that publishes executable, portable ZIP, and SHA256 checksums.
- A single authoritative Anunnaki version module, release verification, roadmap,
  screenshot/demo asset location, and expanded project documentation.

### Changed

- Pinned the tested Microsoft MarkItDown dependency to 0.1.7.
- Renamed the Anunnaki PyInstaller specification and added immediate splash-screen
  feedback during a cold application launch.

### Security

- Documented checksum verification, unsigned-binary guidance, and private GitHub
  Security Advisory reporting.

## [0.1.2] - 2026-09-01 (legacy tag: `v0.1.2`)

- Bundled Magika's file-identification model in Windows builds, fixing the
  `model dir not found` conversion error.
- Made the portable one-folder Windows package the preferred user download for
  faster startup.
- Moved the desktop application to the standard `src/` layout and consolidated
  project documentation and GitHub Actions workflows.

## [0.1.1] - 2026-08-31 (legacy tag: `v0.1.1`)

- Made the Anunnaki logo explicit in the Windows taskbar and application title bar.
- Simplified the end-user release path around a self-contained Windows executable with no separate Python installation.

## [0.1.0] - 2026-08-31 (legacy tag: `v0.1.0`)

- First independent Anunnaki desktop release, based on Microsoft MarkItDown.
- Added a dark-friendly PySide6 Windows GUI for drag-and-drop and multi-file Markdown conversion.
- Added local conversion queues, per-file progress and errors, cancellation, and safe existing-output handling.
- Added per-source output by default (`report.pdf` becomes `report.md` beside it), with an optional shared output folder.
- Added PyInstaller packaging for `Anunnaki.exe`, application branding, tests, and Windows build automation.
