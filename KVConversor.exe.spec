# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['KVConversor.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['pywin32'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['config'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='KVConversor.exe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir='.',
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
