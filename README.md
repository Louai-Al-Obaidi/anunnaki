# Anunnaki

> **MarkItDown Desktop for Windows** — convert PDF, Word, Excel, PowerPoint, and other supported documents to Markdown with drag and drop.

[![Windows](https://img.shields.io/badge/platform-Windows-0078D4?logo=windows&logoColor=white)](https://github.com/Louai-Al-Obaidi/anunnaki/releases/latest)
[![Latest release](https://img.shields.io/github/v/release/Louai-Al-Obaidi/anunnaki?label=release)](https://github.com/Louai-Al-Obaidi/anunnaki/releases/latest)
[![Tests](https://github.com/Louai-Al-Obaidi/anunnaki/actions/workflows/tests.yml/badge.svg)](https://github.com/Louai-Al-Obaidi/anunnaki/actions/workflows/tests.yml)
[![License](https://img.shields.io/github/license/Louai-Al-Obaidi/anunnaki)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](CONTRIBUTING.md)
[![Powered by MarkItDown](https://img.shields.io/badge/powered%20by-Microsoft%20MarkItDown-5E5E5E)](https://github.com/microsoft/markitdown)

<p align="center">
  <img src="src/doc2markdown_desktop/assets/logo.png" width="180" alt="Anunnaki logo">
</p>

## Download for Windows

**Normal users only need the release download.** You do not need Python, Docker, Git, or a command line.

1. Open the [latest Anunnaki release](https://github.com/Louai-Al-Obaidi/anunnaki/releases/latest).
2. Download **`Anunnaki-Windows-x64-portable.zip`**.
3. Extract the ZIP completely.
4. Run **`Anunnaki.exe`** from the extracted `Anunnaki` folder.

The ZIP is the recommended portable Windows application. Keep `Anunnaki.exe` beside its `_internal` folder. The optional standalone EXE is also published for convenience but can start more slowly because it unpacks its runtime at launch.

## What it does

Anunnaki is a friendly Windows GUI around [Microsoft MarkItDown](https://github.com/microsoft/markitdown). It makes local document conversion accessible through drag and drop, batch queues, progress reporting, cancellation, and safe output-file handling.

- No Python, Docker, or CLI required for release users
- Drag-and-drop and multi-file conversion queue
- PDF to Markdown, Word/DOCX to Markdown, Excel/XLSX to Markdown, and PowerPoint/PPTX to Markdown
- Also supports text, CSV, HTML, Markdown, images, and other formats provided by the bundled MarkItDown version
- Existing Markdown files can be overwritten, skipped, or safely auto-renamed
- Portable Windows build; no account or Anunnaki cloud backend required

## Why Anunnaki?

Anunnaki complements MarkItDown; it does not replace it. MarkItDown remains the conversion engine, while Anunnaki focuses on a convenient Windows desktop workflow.

| Microsoft MarkItDown | Anunnaki |
| --- | --- |
| Developer-oriented Python and CLI workflows | Friendly Windows GUI |
| Environment setup normally needed for source use | Portable release for ordinary users |
| Terminal commands | Drag and drop and file picker |
| Flexible conversion engine | Batch conversion queue and output controls |

## Privacy and local processing

The Anunnaki GUI sends no selected document content to an Anunnaki service: selected files are passed to the locally installed MarkItDown conversion engine and Markdown is written to your chosen local folder. The application has no account system, Anunnaki cloud backend, or Anunnaki telemetry code.

Some optional MarkItDown integrations and third-party dependencies may use external services if they are explicitly configured or invoked. Review their documentation and configuration before enabling them with sensitive content.

## How it works

```text
Documents
    ↓
Anunnaki GUI (PySide6)
    ↓
Microsoft MarkItDown conversion engine
    ↓
Markdown output on local disk
```

PySide6 provides the Windows interface, Anunnaki manages the conversion queue and safe output behavior, MarkItDown performs conversion, and PyInstaller packages the Windows release.

## Screenshots and demo

Real media is intentionally not fabricated. Add a screenshot at [`docs/assets/anunnaki-screenshot.png`](docs/assets/README.md) and, optionally, a demo at `docs/assets/anunnaki-demo.gif`.

## Verify a download

Every release includes `SHA256SUMS.txt`. In PowerShell, run the following from the downloaded release folder:

```powershell
Get-FileHash .\Anunnaki-Windows-x64.exe -Algorithm SHA256
```

Compare the result with the matching filename in `SHA256SUMS.txt` from the same GitHub Release. Releases are currently unsigned, so Microsoft Defender SmartScreen may warn before a reputation has been established; download only from the official Releases page and verify the checksum.

## For developers and contributors

The source exists for transparency, auditing, and contributions. Release users do not need to build it.

```powershell
git clone https://github.com/Louai-Al-Obaidi/anunnaki.git
cd anunnaki
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
anunnaki
```

Run checks:

```powershell
ruff check .
ruff format --check src/doc2markdown_desktop tests
pytest
```

Build the portable application:

```powershell
pyinstaller --noconfirm --clean --distpath dist --workpath build src\doc2markdown_desktop\packaging\Anunnaki.spec
```

Anunnaki is tested against **Microsoft MarkItDown 0.1.7**. The project uses `src/doc2markdown_desktop` internally as a controlled technical-debt name; the public product name, release assets, and packaging are Anunnaki.

## Versioning and releases

The current Anunnaki application version is **0.1.3**. It has one source of truth: [`src/doc2markdown_desktop/version.py`](src/doc2markdown_desktop/version.py). Git tags are deliberately namespaced as `anunnaki-vX.Y.Z`—for example, `anunnaki-v0.1.3`, `anunnaki-v0.2.0`, and `anunnaki-v1.0.0`—to avoid collisions with inherited Microsoft MarkItDown tags. Only `anunnaki-v*` tags publish releases; generic upstream `v*` tags in history are not Anunnaki releases.

## Attribution, security, and support

Anunnaki is an independent open-source project built around Microsoft MarkItDown. It is not affiliated with, sponsored by, or endorsed by Microsoft. Microsoft-origin material remains subject to the MIT license and notices; Anunnaki-specific additions are maintained by Louai Al Obaidi. See [NOTICE.md](NOTICE.md), [LICENSE](LICENSE), [SECURITY.md](SECURITY.md), [CONTRIBUTING.md](CONTRIBUTING.md), and [ROADMAP.md](ROADMAP.md).
