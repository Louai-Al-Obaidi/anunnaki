# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller specification for the standalone Anunnaki Windows executable."""

from pathlib import Path

from PyInstaller.utils.hooks import collect_all

project_root = Path(SPECPATH).parents[2]
icon_path = project_root / "src" / "doc2markdown_desktop" / "assets" / "anunnaki.ico"
logo_path = project_root / "src" / "doc2markdown_desktop" / "assets" / "logo.png"
markitdown_datas, markitdown_binaries, markitdown_hiddenimports = collect_all("markitdown")
magika_datas, magika_binaries, magika_hiddenimports = collect_all("magika")
datas = markitdown_datas + magika_datas
binaries = markitdown_binaries + magika_binaries
hiddenimports = markitdown_hiddenimports + magika_hiddenimports
datas.append((str(icon_path), "doc2markdown_desktop/assets"))
datas.append((str(logo_path), "doc2markdown_desktop/assets"))

a = Analysis(
    [str(project_root / "src" / "doc2markdown_desktop" / "app.py")],
    pathex=[str(project_root / "src")],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    excludes=["tkinter"],
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="Anunnaki",
    icon=str(icon_path),
    console=False,
    debug=False,
    upx=False,
)
coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, name="Anunnaki")
