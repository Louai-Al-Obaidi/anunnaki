# Anunnaki v0.1.0

## Highlights

- First public preview of Anunnaki, an independent Windows desktop interface powered by Microsoft MarkItDown.
- Drag-and-drop and multi-file selection for local document-to-Markdown conversion.
- Background queue with per-file progress, completion state, failure details, and cancellation.
- Safe existing-output choices: overwrite, skip, or auto-rename.
- Default same-folder output (`report.pdf` → `report.md`) plus a shared output-folder option.
- Standalone Windows distribution built with PyInstaller; Python is not required for release users.

## Installation

Download and extract the `Anunnaki` Windows ZIP release asset, then run `Anunnaki.exe`. Keep the `_internal` directory next to the executable.

## Supported formats

Format recognition and conversion are provided by the bundled MarkItDown version. Common formats include PDF, DOCX, PPTX, XLSX, CSV, HTML, text, Markdown, and supported images. Some optional format support depends on bundled dependencies.

## Known limitations

- Markdown cannot reproduce every visual aspect of complex office documents or PDFs.
- A conversion error for one file does not stop the remaining queue; inspect the status table for details.
- This preview release targets Windows. Source development requires Python 3.11+.

## Attribution

Anunnaki is an independent derivative of [Microsoft MarkItDown](https://github.com/microsoft/markitdown), is MIT licensed, and is not affiliated with or endorsed by Microsoft. See [NOTICE.md](NOTICE.md).
