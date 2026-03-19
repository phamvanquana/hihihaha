# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['..\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('course_parser.py', '.'), ('main_window.py', '.'), ('video_player.py', '.'), ('transcript_viewer.py', '.'), ('content_viewer.py', '.'), ('styles.py', '.')],
    hiddenimports=['PySide6.QtWidgets', 'PySide6.QtCore', 'PySide6.QtGui', 'vlc', 'pysrt', 'chardet'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SAA_Learning_Hub',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SAA_Learning_Hub',
)
