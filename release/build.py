"""
Build script para generar ejecutable standalone de UCLV Downloader
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def clean_build():
    """Limpia directorios de build anteriores"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"🧹 Limpiando {dir_name}/")
            shutil.rmtree(dir_name)
    
    # Limpiar archivos .spec
    for spec_file in Path('.').glob('*.spec'):
        print(f"🧹 Eliminando {spec_file}")
        spec_file.unlink()

def create_spec_file():
    """Crea archivo .spec personalizado para PyInstaller"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
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
    name='ucvl-downloader',
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
    
    with open('ucvl-downloader.spec', 'w') as f:
        f.write(spec_content)
    print("📝 Archivo .spec creado")

def build_executable():
    """Compila el ejecutable usando PyInstaller"""
    print("🚀 Iniciando compilación con PyInstaller...")
    
    try:
        # Compilar usando el archivo .spec con uv run
        cmd = ['uv', 'run', 'pyinstaller', '--clean', 'ucvl-downloader.spec']
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("✅ Compilación exitosa!")
        print("\n📦 Ejecutable generado en: dist/ucvl-downloader")
        
        # Mostrar tamaño del ejecutable
        exe_path = Path('dist/ucvl-downloader')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📏 Tamaño del ejecutable: {size_mb:.1f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error durante la compilación:")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def test_executable():
    """Prueba el ejecutable generado"""
    exe_path = Path('dist/ucvl-downloader')
    
    if not exe_path.exists():
        print("❌ No se encontró el ejecutable generado")
        return False
    
    print("🧪 Probando el ejecutable...")
    
    try:
        # Probar con --version
        result = subprocess.run([str(exe_path), '--version'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Ejecutable funciona correctamente!")
            print(f"Versión: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ El ejecutable falló: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Timeout al probar el ejecutable")
        return False
    except Exception as e:
        print(f"❌ Error al probar el ejecutable: {e}")
        return False

def create_installation_info():
    """Crea información de instalación"""
    install_info = """# UCLV Downloader - Ejecutable Linux

## 📦 Instalación

1. Descarga el archivo `ucvl-downloader`
2. Dale permisos de ejecución:
   ```bash
   chmod +x ucvl-downloader
   ```
3. Ejecuta el programa:
   ```bash
   ./ucvl-downloader
   ```

## 🖥️ Uso

### Interfaz Gráfica (por defecto)
```bash
./ucvl-downloader
```

### Interfaz de Línea de Comandos
```bash
./ucvl-downloader --cli
```

### Ayuda
```bash
./ucvl-downloader --help
```

## 📋 Requisitos del Sistema

- Ubuntu 18.04+ / Linux Mint 19+ / Debian 10+
- Arquitectura x86_64
- ~50MB de espacio libre

## 🔧 Solución de Problemas

Si obtienes error de "Permission denied":
```bash
chmod +x ucvl-downloader
```

Si obtienes error de librerías faltantes en sistemas muy antiguos:
```bash
sudo apt update
sudo apt install libc6 libgcc-s1
```

## 🌐 Sitio Web Soportado

- visuales.ucv.cu (Universidad Central de Venezuela)

## 📞 Soporte

Para reportar bugs o solicitar nuevas funcionalidades, abre un issue en el repositorio.
"""
    
    with open('dist/INSTALACION.md', 'w') as f:
        f.write(install_info)
    print("📋 Información de instalación creada en dist/INSTALACION.md")

def main():
    """Función principal del script de build"""
    print("🏗️  UCLV Downloader - Script de Compilación")
    print("=" * 50)
    
    # Cambiar al directorio raíz del proyecto
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    # Verificar que estamos en el directorio correcto
    if not Path('main.py').exists():
        print("❌ Error: No se encontró main.py")
        print("   Asegúrate de ejecutar este script desde el directorio del proyecto")
        sys.exit(1)
    
    # Verificar que PyInstaller está instalado
    try:
        subprocess.run(['uv', 'run', 'pyinstaller', '--version'], 
                      capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print("❌ Error: PyInstaller no está instalado")
        print("   Ejecuta: uv add --dev pyinstaller")
        sys.exit(1)
    
    # Pasos de compilación
    steps = [
        ("Limpiar builds anteriores", clean_build),
        ("Crear archivo .spec", create_spec_file),
        ("Compilar ejecutable", build_executable),
        ("Probar ejecutable", test_executable),
        ("Crear información de instalación", create_installation_info)
    ]
    
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        try:
            if step_func == build_executable or step_func == test_executable:
                if not step_func():
                    print(f"❌ Falló: {step_name}")
                    sys.exit(1)
            else:
                step_func()
        except Exception as e:
            print(f"❌ Error en {step_name}: {e}")
            sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 ¡Compilación completada exitosamente!")
    print("\n📁 Archivos generados:")
    print("   - dist/ucvl-downloader (ejecutable)")
    print("   - dist/INSTALACION.md (instrucciones)")
    print("\n🚀 Para distribuir, comprime la carpeta 'dist/' o solo el ejecutable")

if __name__ == '__main__':
    main()