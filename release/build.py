"""
Build script para generar ejecutable standalone de UCLV Downloader - Refactored
"""

import os
import sys
import subprocess
from pathlib import Path
from .builders import MainBuilder

def main():
    """Función principal del script de build usando el sistema refactorizado"""
    print("🏗️  UCLV Downloader - Script de Compilación (Refactorizado)")
    print("=" * 60)
    
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
    
    # Crear y usar el main builder
    builder = MainBuilder()
    
    try:
        result = builder.build_all()
        
        if result['success']:
            print("\n" + "=" * 60)
            print("🎉 ¡Compilación completada exitosamente!")
            print(f"\n📊 Resultados: {result['completed']}/{result['total']} pasos completados")
            print("\n📁 Archivos generados:")
            print("   - dist/ucvl-downloader (ejecutable)")
            print("   - dist/INSTALACION.md (instrucciones)")
            print(f"\n⏱️  Tiempo total: {result['duration']:.1f} segundos")
            print("\n🚀 Para distribuir, comprime la carpeta 'dist/' o solo el ejecutable")
        else:
            print(f"\n❌ Compilación falló: {result['message']}")
            if 'failed_steps' in result:
                print("Pasos fallidos:")
                for step in result['failed_steps']:
                    print(f"   - {step}")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error inesperado durante la compilación: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()