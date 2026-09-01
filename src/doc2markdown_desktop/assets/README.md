# Anunnaki assets

`logo.png` is the canonical Anunnaki brand image. The application resolves it
through `branding.py`, so the same asset is used by the GUI and included in
the packaged executable.

`anunnaki.ico` is the Windows multi-resolution icon used for the executable,
window title bar, and taskbar. Keep both files in this directory when building
with PyInstaller.
