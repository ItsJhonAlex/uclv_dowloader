#!/usr/bin/env python3
"""
Script para crear un release distributable de UCLV Downloader
"""

import os
import shutil
import tarfile
import zipfile
from datetime import datetime
from pathlib import Path

def create_release_package():
    """Crea un paquete de release listo para distribuir"""
    
    version = "1.0.0"
    date = datetime.now().strftime("%Y%m%d")
    
    # Nombres de los paquetes
    tar_name = f"ucvl-downloader-v{version}-linux-x64.tar.gz"
    zip_name = f"ucvl-downloader-v{version}-linux-x64.zip"
    
    # Verificar que el ejecutable existe
    exe_path = Path("dist/ucvl-downloader")
    if not exe_path.exists():
        print("❌ Error: No se encontró el ejecutable en dist/")
        print("   Ejecuta primero: release/build.py")
        return False
    
    # Crear carpeta temporal de release
    release_dir = Path(f"ucvl-downloader-v{version}")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    
    release_dir.mkdir()
    
    print(f"📦 Creando paquete de release v{version}...")
    
    # Copiar archivos necesarios
    files_to_copy = [
        ("dist/ucvl-downloader", "ucvl-downloader"),
        ("dist/INSTALACION.md", "INSTALACION.md"),
        ("README.md", "README.md"),
        ("CHANGELOG.md", "CHANGELOG.md")
    ]
    
    for src, dst in files_to_copy:
        src_path = Path(src)
        dst_path = release_dir / dst
        
        if src_path.exists():
            shutil.copy2(src_path, dst_path)
            print(f"✅ Copiado: {src} -> {dst}")
        else:
            print(f"⚠️  No encontrado: {src}")
    
    # Crear archivo de información de release
    release_info = f"""# UCLV Downloader v{version} - Release Linux x64

🎬 **Descargador de Videos y Subtítulos para visuales.ucv.cu**

## 📊 Información del Release

- **Versión**: {version}
- **Fecha de compilación**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Plataforma**: Linux x86_64
- **Compatibilidad**: Ubuntu 18.04+, Debian 10+, Linux Mint 19+

## 🚀 Instalación Rápida

1. **Descomprime** el archivo donde quieras instalar el programa
2. **Da permisos de ejecución** al archivo:
   ```bash
   chmod +x ucvl-downloader
   ```
3. **Ejecuta** el programa:
   ```bash
   ./ucvl-downloader
   ```

## 🎮 Uso

### Interfaz Gráfica (Recomendado)
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

## 📋 Archivos Incluidos

- `ucvl-downloader` - Ejecutable principal (14MB)
- `INSTALACION.md` - Instrucciones detalladas de instalación
- `README.md` - Documentación completa del proyecto
- `CHANGELOG.md` - Historial de versiones y cambios
- `RELEASE-INFO.md` - Este archivo

## 🔧 Requisitos del Sistema

- **SO**: Ubuntu 18.04+ / Debian 10+ / Linux Mint 19+
- **Arquitectura**: x86_64 (64-bit)
- **RAM**: 512MB mínimo
- **Espacio**: 50MB libres
- **Dependencias**: Ninguna (ejecutable standalone)

## 🌐 Sitios Soportados

- **visuales.ucv.cu** - Universidad Central de Venezuela

## 🐛 Solución de Problemas

### Error "Permission denied"
```bash
chmod +x ucvl-downloader
```

### Error "No such file or directory" 
Asegúrate de estar en la carpeta donde descargaste y descomprimiste el programa.

### Error de librerías en sistemas muy antiguos
```bash
sudo apt update
sudo apt install libc6 libgcc-s1
```

## 📞 Soporte

- **Repositorio**: https://github.com/tu-usuario/ucvl-downloader
- **Issues**: Reporta bugs y solicita funcionalidades
- **Documentación**: Ver README.md incluido

## ⭐ Características v{version}

- ✅ Descarga selectiva por tipo de archivo
- ✅ Interfaz gráfica moderna con tkinter
- ✅ Interfaz de línea de comandos interactiva
- ✅ Progreso en tiempo real
- ✅ Reintentos automáticos
- ✅ Arquitectura modular
- ✅ Sin dependencias externas

¡Gracias por usar UCLV Downloader! 🎉
"""
    
    with open(release_dir / "RELEASE-INFO.md", 'w') as f:
        f.write(release_info)
    
    # Crear archivo .tar.gz
    print(f"\n📦 Creando {tar_name}...")
    with tarfile.open(tar_name, "w:gz") as tar:
        tar.add(release_dir, arcname=release_dir.name)
    
    # Crear archivo .zip
    print(f"📦 Creando {zip_name}...")
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in release_dir.rglob('*'):
            if file_path.is_file():
                arc_name = file_path.relative_to(release_dir.parent)
                zip_file.write(file_path, arc_name)
    
    # Información de archivos creados
    tar_size = Path(tar_name).stat().st_size / (1024 * 1024)
    zip_size = Path(zip_name).stat().st_size / (1024 * 1024)
    
    print(f"\n🎉 ¡Release creado exitosamente!")
    print(f"📁 Archivos generados:")
    print(f"   - {tar_name} ({tar_size:.1f} MB)")
    print(f"   - {zip_name} ({zip_size:.1f} MB)")
    print(f"   - {release_dir}/ (carpeta temporal)")
    
    print(f"\n🚀 Para distribuir:")
    print(f"   - Sube {tar_name} o {zip_name} a GitHub Releases")
    print(f"   - O comparte directamente el archivo con usuarios")
    
    # Limpiar carpeta temporal
    shutil.rmtree(release_dir)
    print(f"🧹 Carpeta temporal eliminada")
    
    return True

def main():
    """Función principal"""
    print("📦 UCLV Downloader - Creador de Release")
    print("=" * 45)
    
    # Cambiar al directorio raíz del proyecto
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    # Verificar que estamos en el directorio correcto
    if not Path("dist/ucvl-downloader").exists():
        print("❌ Error: No se encontró dist/ucvl-downloader")
        print("   Ejecuta primero: release/build.py")
        return
    
    if create_release_package():
        print("\n✅ Release listo para distribución!")
    else:
        print("\n❌ Error al crear el release")

if __name__ == '__main__':
    main() 