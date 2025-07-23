# uefi_editor.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],  # 替换为你的Python脚本文件名
    pathex=[],
    binaries=[
        ('UEFIExtract.exe', '.'),  # 添加所有依赖的exe文件
        ('ifrextractor.exe', '.'),
        ('findver.exe', '.'),
        ('cecho.exe', '.'),
        ('UEFIReplace.exe', '.')
    ],
    datas=[
        ('manifest.xml', '.'),  # 添加权限清单文件
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='UE-assist',  # 输出的exe文件名
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 隐藏命令行窗口
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    manifest='manifest.xml'  # 指定权限清单文件
)