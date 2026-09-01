# Contributing to Anunnaki

Thanks for contributing to the Anunnaki desktop experience. This project is an independent derivative of Microsoft MarkItDown; changes to the GUI and packaging should remain clearly separated from upstream conversion-engine behavior.

Use Python 3.11+ and install the development dependencies. Anunnaki is tested
with Microsoft MarkItDown 0.1.7.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Run the desktop app with `anunnaki`. Build the portable Windows package with:

```powershell
pyinstaller --noconfirm --clean --distpath dist --workpath build src\doc2markdown_desktop\packaging\Anunnaki.spec
```

Before opening a pull request, run:

```powershell
ruff check src tests
ruff format --check src tests
pytest
pre-commit run --all-files
```

Keep pull requests focused, add tests for behavior changes, and preserve the local-only default: document content must not be sent over the network without an explicit user choice. Do not commit `.env` files, credentials, private certificates, personal documents, or generated executables.

Use `anunnaki-vX.Y.Z` only for Anunnaki release tags. Do not create generic
`vX.Y.Z` tags: inherited Microsoft MarkItDown history uses that namespace.

For updates to the MarkItDown engine, first compare with `upstream` and explain the compatibility impact in the pull request.
