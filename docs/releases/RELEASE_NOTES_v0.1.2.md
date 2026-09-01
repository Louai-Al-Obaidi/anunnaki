# Anunnaki v0.1.2

## Installation

Download `Anunnaki-Windows-x64-portable.zip`, extract it, and run
`Anunnaki.exe` from the extracted folder. No separate Python installation is
required.

## Fixed

- The Windows package now includes Magika's model files, fixing the
  `model dir not found` error during document conversion.
- The portable package is the recommended download because it starts faster
  than the optional self-extracting one-file executable.

## Project maintenance

- The desktop application now uses a standard `src/` layout.
- Documentation and release notes are organized under `docs/`.
- GitHub Actions workflows were consolidated around the desktop application.
