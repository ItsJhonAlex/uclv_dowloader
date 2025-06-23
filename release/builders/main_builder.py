"""
Main Builder that coordinates all build steps
"""

import time
from typing import Dict, Any
from pathlib import Path

from .build_cleaner import BuildCleaner
from .spec_generator import SpecGenerator
from .executable_builder import ExecutableBuilder
from .build_tester import BuildTester


class MainBuilder:
    """Main build coordinator using modular components"""
    
    def __init__(self):
        self.cleaner = BuildCleaner()
        self.spec_generator = SpecGenerator()
        self.executable_builder = ExecutableBuilder()
        self.build_tester = BuildTester()
        
        self.start_time = None
    
    def build_all(self) -> Dict[str, Any]:
        """Execute all build steps and return results"""
        self.start_time = time.time()
        
        # Define build steps with their descriptions
        steps = [
            ("Limpiar builds anteriores", self.cleaner.clean_build),
            ("Crear archivo .spec", self.spec_generator.create_spec_file),
            ("Compilar ejecutable", self.executable_builder.build_executable),
            ("Probar ejecutable", self.build_tester.test_executable),
            ("Crear información de instalación", self._create_installation_info)
        ]
        
        completed_steps = 0
        failed_steps = []
        
        try:
            for step_name, step_func in steps:
                print(f"\n🔄 {step_name}...")
                
                try:
                    # Some steps return boolean, others don't
                    if step_func in [self.executable_builder.build_executable, self.build_tester.test_executable]:
                        if not step_func():
                            failed_steps.append(step_name)
                            break
                    else:
                        step_func()
                    
                    completed_steps += 1
                    
                except Exception as e:
                    print(f"❌ Error en {step_name}: {e}")
                    failed_steps.append(step_name)
                    break
            
            # Calculate results
            total_steps = len(steps)
            success = completed_steps == total_steps
            duration = time.time() - self.start_time
            
            return {
                'success': success,
                'completed': completed_steps,
                'total': total_steps,
                'failed_steps': failed_steps,
                'duration': duration,
                'message': 'Build completed successfully' if success else f'Build failed at step: {failed_steps[-1] if failed_steps else "unknown"}'
            }
            
        except KeyboardInterrupt:
            return {
                'success': False,
                'completed': completed_steps,
                'total': len(steps),
                'failed_steps': failed_steps + ['Interrupted by user'],
                'duration': time.time() - self.start_time,
                'message': 'Build interrupted by user'
            }
    
    def _create_installation_info(self):
        """Create installation information file"""
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
        
        # Ensure dist directory exists
        Path('dist').mkdir(exist_ok=True)
        
        with open('dist/INSTALACION.md', 'w') as f:
            f.write(install_info)
        print("📋 Información de instalación creada en dist/INSTALACION.md")
    
    def get_build_summary(self) -> Dict[str, Any]:
        """Get summary of available build tools"""
        return {
            'cleaner': 'Limpia archivos de builds anteriores',
            'spec_generator': 'Genera archivo .spec para PyInstaller',
            'executable_builder': 'Compila el ejecutable usando PyInstaller',
            'build_tester': 'Prueba el ejecutable generado',
            'installation_info': 'Crea documentación de instalación'
        } 