# Optional app bundle: ./build-macos-arm64.sh --app
import sys
from pathlib import Path

if sys.platform != 'darwin':
    raise SystemExit('This spec requires macOS. Use main.spec for Windows.')

root = Path(SPECPATH)
a = Analysis(
    [str(root / 'main.py')],
    pathex=[str(root)],
    binaries=[],
    datas=[(str(root / 'assets'), 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, [],
    exclude_binaries=True,
    name='SecretCouncil',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    target_arch='arm64',
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe, a.binaries, a.datas,
    strip=False,
    upx=False,
    name='SecretCouncil',
)
app = BUNDLE(
    coll,
    name='SecretCouncil.app',
    icon=str(root / 'assets/icons/SecretCouncil.icns'),
    bundle_identifier='org.secretcouncil.game',
    info_plist={
        'CFBundleDisplayName': 'Secret Council',
        'NSHighResolutionCapable': True,
    },
)
