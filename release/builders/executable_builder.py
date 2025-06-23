"""
Executable Builder component
"""

import subprocess
from pathlib import Path


class ExecutableBuilder:
    """Handles PyInstaller execution and executable building"""
    
    def __init__(self, app_name: str = 'ucvl-downloader'):
        self.app_name = app_name
        self.spec_file = f'{app_name}.spec'
        self.exe_path = Path(f'dist/{app_name}')
    
    def build_executable(self) -> bool:
        """Compila el ejecutable usando PyInstaller"""
        print("🚀 Iniciando compilación con PyInstaller...")
        
        try:
            # Compilar usando el archivo .spec con uv run
            cmd = ['uv', 'run', 'pyinstaller', '--clean', self.spec_file]
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            print("✅ Compilación exitosa!")
            print(f"\n📦 Ejecutable generado en: {self.exe_path}")
            
            # Mostrar tamaño del ejecutable
            if self.exe_path.exists():
                size_mb = self.exe_path.stat().st_size / (1024 * 1024)
                print(f"📏 Tamaño del ejecutable: {size_mb:.1f} MB")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error durante la compilación:")
            print(f"STDOUT: {e.stdout}")
            print(f"STDERR: {e.stderr}")
            return False
    
    def check_pyinstaller_available(self) -> bool:
        """Check if PyInstaller is available"""
        try:
            subprocess.run(['uv', 'run', 'pyinstaller', '--version'], 
                          capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def get_executable_info(self) -> dict:
        """Get information about the built executable"""
        if not self.exe_path.exists():
            return {'exists': False}
        
        stat = self.exe_path.stat()
        return {
            'exists': True,
            'path': str(self.exe_path),
            'size_bytes': stat.st_size,
            'size_mb': stat.st_size / (1024 * 1024),
            'executable': stat.st_mode & 0o111 != 0  # Check if executable bit is set
        } 