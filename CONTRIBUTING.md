# Contributing to Anunnaki

Thanks for contributing to the Anunnaki desktop experience. This project is an independent derivative of Microsoft MarkItDown; changes to the GUI and packaging should remain clearly separated from upstream conversion-engine behavior.

Use Python 3.11+ and install the development dependencies:

```powershell
python -m pip install -e ".[dev]"
```

Before opening a pull request, run:

```powershell
ruff check packages tests
ruff format --check packages tests
pytest
pre-commit run --all-files
```

Keep pull requests focused, add tests for behavior changes, and preserve the local-only default: document content must not be sent over the network without an explicit user choice. Do not commit `.env` files, credentials, private certificates, personal documents, or generated executables.

For updates to the MarkItDown engine, first compare with `upstream` and explain the compatibility impact in the pull request.
