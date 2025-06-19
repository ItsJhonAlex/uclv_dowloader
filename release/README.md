# 🏗️ Release Tools

Esta carpeta contiene todas las herramientas necesarias para compilar y crear releases del UCLV Downloader.

## 📁 Archivos

### Scripts de Compilación

- **`build.py`** - Script principal de compilación con PyInstaller
- **`create_release.py`** - Creador de paquetes de distribución
- **`build_and_release.sh`** - Script automático que ejecuta todo el proceso

### Uso

#### 🚀 Método Automático (Recomendado)

Ejecuta todo el proceso de una vez:

```bash
# Desde el directorio raíz del proyecto
./release/build_and_release.sh
```

#### 🔧 Método Manual

Si prefieres ejecutar paso a paso:

```bash
# 1. Compilar ejecutable
uv run python release/build.py

# 2. Crear paquetes de distribución  
uv run python release/create_release.py
```

## 📦 Salida Generada

Todos los scripts generan archivos en el directorio raíz del proyecto:

```
ucvl_dowloader/
├── dist/
│   ├── ucvl-downloader           # Ejecutable standalone
│   └── INSTALACION.md            # Instrucciones de instalación
├── ucvl-downloader-v1.0.0-linux-x64.tar.gz    # Paquete comprimido
├── ucvl-downloader-v1.0.0-linux-x64.zip       # Paquete ZIP
└── ucvl-downloader.spec          # Archivo de configuración PyInstaller
```

## 🔄 Proceso de Build

### build.py

1. **Limpia** builds anteriores (dist/, build/, *.spec)
2. **Crea** archivo .spec personalizado para PyInstaller
3. **Compila** el ejecutable usando `uv run pyinstaller`
4. **Prueba** el ejecutable generado
5. **Crea** documentación de instalación

### create_release.py

1. **Verifica** que el ejecutable existe
2. **Crea** carpeta temporal con todos los archivos necesarios
3. **Genera** archivo RELEASE-INFO.md con información del release
4. **Comprime** en formatos .tar.gz y .zip
5. **Limpia** archivos temporales

### build_and_release.sh

1. **Sincroniza** dependencias con UV
2. **Ejecuta** build.py
3. **Ejecuta** create_release.py  
4. **Muestra** resumen de archivos generados

## ⚙️ Requisitos

- **UV** instalado y configurado
- **PyInstaller** como dependencia de desarrollo
- **Python 3.8+**
- **Permisos de ejecución** para scripts .sh

## 🐛 Solución de Problemas

### Error "PyInstaller not found"
```bash
uv add --dev pyinstaller
```

### Error "Permission denied" en .sh
```bash
chmod +x release/build_and_release.sh
```

### Error "main.py not found"
Asegúrate de ejecutar los scripts desde el directorio raíz del proyecto, o usa el script automático que maneja las rutas correctamente.

## 📏 Configuración

### Modificar Versión

Edita la variable `version` en `create_release.py`:
```python
version = "1.0.0"  # Cambiar aquí
```

### Modificar Nombre del Ejecutable

Edita el `name` en la configuración .spec en `build.py`:
```python
name='ucvl-downloader',  # Cambiar aquí
```

### Agregar Archivos al Release

Modifica la lista `files_to_copy` en `create_release.py`:
```python
files_to_copy = [
    ("dist/ucvl-downloader", "ucvl-downloader"),
    ("dist/INSTALACION.md", "INSTALACION.md"),
    ("README.md", "README.md"),
    ("CHANGELOG.md", "CHANGELOG.md"),
    # ("nuevo_archivo.txt", "nuevo_archivo.txt"),  # Agregar aquí
]
```

## ✨ Características

- ✅ **Compilación automática** con configuración optimizada
- ✅ **Detección de dependencias** automática
- ✅ **Testing del ejecutable** post-compilación
- ✅ **Paquetes multiplataforma** (.tar.gz y .zip)
- ✅ **Documentación automática** incluida en releases
- ✅ **Limpieza automática** de archivos temporales
- ✅ **Gestión de versiones** centralizada 