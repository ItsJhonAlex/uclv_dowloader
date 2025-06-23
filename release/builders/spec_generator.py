"""
PyInstaller Spec File Generator
"""


class SpecGenerator:
    """Generates PyInstaller .spec files with custom configuration"""
    
    def __init__(self, app_name: str = 'ucvl-downloader', main_file: str = 'main.py'):
        self.app_name = app_name
        self.main_file = main_file
        self.spec_filename = f'{app_name}.spec'
    
    def create_spec_file(self) -> str:
        """Crea archivo .spec personalizado para PyInstaller"""
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{self.main_file}'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'requests',
        'bs4',
        'tqdm',
        'urllib3'
    ],
    hookspath=[],
    hooksconfig={{}},
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
    name='{self.app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None
)
'''
        
        with open(self.spec_filename, 'w') as f:
            f.write(spec_content)
        
        print(f"📝 Archivo {self.spec_filename} creado")
        return self.spec_filename
    
    def add_hidden_import(self, module: str):
        """Add a hidden import to the spec file"""
        # This would modify the spec file to add the import
        # For now, it's just a placeholder
        pass
    
    def set_console_mode(self, console: bool):
        """Set console mode for the executable"""
        # This would modify the spec file
        # For now, it's just a placeholder
        pass
    
    def set_icon(self, icon_path: str):
        """Set icon for the executable"""
        # This would modify the spec file to include the icon
        # For now, it's just a placeholder
        pass 