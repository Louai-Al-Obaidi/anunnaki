# Anunnaki roadmap

This roadmap describes intentions, not promises. Priorities are guided by safe, local-first document conversion on Windows.

## Next release

- Continue UI polish and improve error explanations.
- Add focused tests for supported conversion formats and queue edge cases.
- Add a conversion summary that can be copied or saved.
- Evaluate folder conversion and optional recursive folder conversion without changing the safe default output behavior.

## Future candidates

- Markdown preview and copy-to-clipboard.
- Open a generated Markdown file after conversion.
- Retry failed queue items and a lightweight local conversion history.
- Preserve source folder hierarchy during folder conversion.
- Dark/light theme refinements.
- A signed Windows installer or MSIX option, once a trustworthy signing process is available.
- A reversible Windows Explorer context-menu integration with a documented uninstaller.
- Version update checking that does not upload document content.
- Investigation of macOS/Linux support if packaging and testing can be maintained responsibly.

## Windows Explorer integration

“Convert to Markdown with Anunnaki” could be implemented through a per-user registry entry that invokes the installed executable with a selected path. It is deferred because any integration must be opt-in, reversible, documented, and accompanied by an uninstaller. Anunnaki does not modify the Windows registry today.
