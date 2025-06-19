# UCLV Downloader 🎬

Un downloader moderno y eficiente para descargar videos y subtítulos desde el sitio `visuales.ucv.cu`. Construido con Python y UV, ofrece tanto interfaz de línea de comandos (CLI) como interfaz gráfica (GUI).

## ✨ Características

- 🎯 **Descarga selectiva**: Videos (.mp4), subtítulos (.srt), imágenes (.jpg) y archivos de información (.nfo)
- 🖥️ **Doble interfaz**: CLI interactivo y GUI con tkinter
- 📊 **Progreso en tiempo real**: Barras de progreso y estadísticas detalladas
- 🔄 **Reintentos automáticos**: Lógica de reintento para descargas fallidas
- 🎨 **Interfaz moderna**: GUI intuitiva con selección de tipos de archivo
- 📁 **Organización inteligente**: Estructura modular y mantenible
- ⚡ **Descarga secuencial**: Descarga archivo por archivo con control total

## 🚀 Instalación

### Requisitos previos

- Python 3.8+
- UV (Ultra-fast Python package installer)
- tkinter (para GUI en Linux: `sudo apt install python3-tk`)

### Instalación de UV

```bash
# En Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# En Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Configuración del proyecto

```bash
# Clonar el repositorio
git clone <repository-url>
cd ucvl_dowloader

# Instalar dependencias
uv sync
```

## 📖 Uso

### Interfaz Gráfica (por defecto)

```bash
python main.py
# o simplemente
python main.py --gui
```

### Interfaz de Línea de Comandos

```bash
python main.py --cli
```

### Opciones adicionales

```bash
python main.py --help     # Mostrar ayuda
python main.py --version  # Mostrar versión
```

## 🏗️ Estructura del Proyecto

```
ucvl_dowloader/
├── core/
│   ├── __init__.py
│   ├── downloader.py     # Lógica principal de descarga
│   └── utils.py          # Utilidades para URLs y archivos
├── cli/
│   ├── __init__.py
│   └── interface.py      # Interfaz de línea de comandos
├── gui/
│   ├── __init__.py
│   └── interface.py      # Interfaz gráfica con tkinter
├── release/
│   ├── build.py          # Script de compilación
│   ├── create_release.py # Creador de paquetes
│   ├── build_and_release.sh # Script automático
│   └── README.md         # Documentación de herramientas
├── main.py               # Launcher principal
├── pyproject.toml        # Configuración UV y dependencias
├── CHANGELOG.md          # Historial de versiones
├── .gitignore           # Archivos ignorados por git
└── README.md            # Este archivo
```

## 🎮 Modo de Uso

### GUI (Interfaz Gráfica)

1. **Ingresa la URL**: Pega la URL de la carpeta de visuales.ucv.cu
2. **Analizar**: Haz clic en "Analizar URL" para obtener la lista de archivos
3. **Seleccionar tipos**: Marca/desmarca los tipos de archivo a descargar:
   - ☑️ Videos (.mp4)
   - ☑️ Subtítulos (.srt)
   - ☐ Imágenes (.jpg)
   - ☐ Info (.nfo)
4. **Elegir carpeta**: Selecciona dónde guardar los archivos
5. **Descargar**: Haz clic en "Iniciar Descarga" y observa el progreso

### CLI (Línea de Comandos)

1. **Ingresa la URL** cuando se solicite
2. **Configura tipos de archivo** a descargar
3. **Previsualiza archivos** disponibles antes de descargar
4. **Confirma la descarga** y observa el progreso

## 🔧 Características Técnicas

### Core Module (`core/`)

- **UCLVDownloader**: Clase principal con filtros configurables
- **Reintentos**: Lógica de reintento para descargas fallidas
- **Callbacks**: Sistema de callbacks para actualización de progreso
- **Estadísticas**: Tracking detallado de descargas y errores

### Utilidades (`core/utils.py`)

- **FileUtils**: Detección de tipos de archivo y formateo de tamaños
- **URLUtils**: Manipulación y validación de URLs

### Interfaces

- **CLI**: Interfaz interactiva con emojis y formato claro
- **GUI**: Interfaz completa con tkinter, threading para operaciones no bloqueantes

## 📦 Dependencias

- **requests**: Para realizar peticiones HTTP
- **beautifulsoup4**: Para parsing de HTML
- **tqdm**: Para barras de progreso en CLI
- **urllib3**: Para manejo avanzado de URLs
- **tkinter**: Para la interfaz gráfica (incluido en Python estándar)

## 📦 Compilación (Ejecutables Standalone)

### Build automático

Para crear un ejecutable que funcione en distribuciones Debian/Ubuntu sin dependencias:

```bash
# Script automático que hace todo el proceso
./release/build_and_release.sh
```

### Build manual paso a paso

```bash
# 1. Instalar PyInstaller
uv add --dev pyinstaller

# 2. Compilar ejecutable
uv run python release/build.py

# 3. Crear paquetes de distribución
uv run python release/create_release.py
```

### Archivos generados

- `dist/ucvl-downloader` - Ejecutable standalone (14MB)
- `ucvl-downloader-v1.0.0-linux-x64.tar.gz` - Paquete comprimido
- `ucvl-downloader-v1.0.0-linux-x64.zip` - Paquete ZIP

### Distribución

Los usuarios finales solo necesitan:
1. Descargar el archivo `.tar.gz` o `.zip`
2. Descomprimir en cualquier carpeta
3. Dar permisos: `chmod +x ucvl-downloader`
4. Ejecutar: `./ucvl-downloader`

## 🛠️ Desarrollo

### Estructura modular

El proyecto está diseñado con una arquitectura modular que facilita:

- ✅ Mantenimiento y testing
- ✅ Extensión con nuevas funcionalidades
- ✅ Reutilización de componentes
- ✅ Separación clara de responsabilidades

### Próximas mejoras planeadas

- 🔄 **Descargas paralelas**: Múltiples archivos simultáneos
- ⏸️ **Resumir descargas**: Continuar descargas interrumpidas
- 🎨 **Temas**: Modo oscuro/claro para la GUI
- 🔔 **Notificaciones**: Alertas de finalización
- 📋 **Cola de descargas**: Gestión de múltiples URLs
- 🗂️ **Organización inteligente**: Clasificación automática por serie/temporada
- 💾 **Configuración persistente**: Guardar preferencias del usuario

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una branch para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🐛 Reportar Bugs

Si encuentras algún bug, por favor abre un issue en el repositorio con:

- Descripción del problema
- Pasos para reproducir
- Sistema operativo y versión de Python
- Logs de error si están disponibles

## 🙏 Agradecimientos

- A la comunidad de Python por las excelentes librerías
- A los contribuidores que han ayudado a mejorar este proyecto 