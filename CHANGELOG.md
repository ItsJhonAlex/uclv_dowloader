# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto se adhiere al [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [No publicado]

### Por agregar
- Descargas paralelas para múltiples archivos simultáneos
- Funcionalidad de reanudar descargas interrumpidas
- Temas para la GUI (modo oscuro/claro)
- Sistema de notificaciones de finalización
- Cola de descargas para múltiples URLs
- Organización inteligente por serie/temporada
- Configuración persistente de preferencias del usuario
- Sistema de plugins para nuevos sitios
- Modo de descarga programada
- Integración con gestores de descarga externos

## [1.0.0] - 2025-06-19

### 🎉 Lanzamiento inicial

Esta es la primera versión estable del UCVL Downloader con arquitectura modular completa.

### ✨ Agregado

#### Funcionalidades Core
- **Descarga selectiva de archivos** por tipo:
  - Videos (.mp4, .avi, .mkv, .mov, .wmv, .flv, .webm)
  - Subtítulos (.srt, .sub, .vtt, .ass, .ssa)
  - Imágenes (.jpg, .jpeg, .png, .gif, .bmp)
  - Archivos de información (.nfo, .txt)
- **Sistema de reintentos** automáticos para descargas fallidas
- **Progreso en tiempo real** con barras de progreso y estadísticas
- **Validación de URLs** y manejo robusto de errores
- **Detección automática** de tipos de archivo y tamaños

#### Interfaces de Usuario
- **Interfaz Gráfica (GUI)** completa con tkinter:
  - Campo de entrada de URL con validación
  - Análisis de archivos disponibles con vista previa
  - Checkboxes para selección de tipos de archivo
  - Treeview con lista detallada de archivos (nombre, tipo, tamaño)
  - Selector de carpeta de destino
  - Barra de progreso y estado en tiempo real
  - Operaciones en hilos separados para evitar bloqueos de UI
- **Interfaz de Línea de Comandos (CLI)** interactiva:
  - Configuración paso a paso de tipos de descarga
  - Vista previa categorizada de archivos disponibles
  - Progreso con barras de tqdm y emojis
  - Confirmaciones y estadísticas detalladas

#### Arquitectura Modular
- **Módulo Core** (`core/`):
  - `UCVLDownloader`: Clase principal con filtros configurables
  - `FileUtils`: Utilidades para detección de tipos y formateo
  - `URLUtils`: Manipulación y validación de URLs
- **Módulo CLI** (`cli/interface.py`): Interfaz de línea de comandos completa
- **Módulo GUI** (`gui/interface.py`): Interfaz gráfica con tkinter
- **Launcher principal** (`main.py`): Selector automático de interfaz

#### Sistema de Gestión
- **Gestión con UV**: Configuración completa con pyproject.toml
- **Dependencias optimizadas**: requests, beautifulsoup4, tqdm, urllib3
- **Detección automática de tkinter**: Fallback graceful si no está disponible
- **Argumentos de línea de comandos**: --cli, --gui, --help, --version

#### Características Técnicas
- **Descarga secuencial**: Un archivo a la vez para no sobrecargar el servidor
- **Callbacks de progreso**: Sistema extensible para actualización de UI
- **Manejo de archivos existentes**: Verificación y omisión inteligente
- **Limpieza automática**: Eliminación de archivos parciales en caso de error
- **Logging comprehensivo**: Registro detallado de operaciones y errores

#### Documentación y Configuración
- **README.md completo**: Documentación técnica y de usuario
- **Estructura modular documentada**: Explicación de cada componente
- **Ejemplos de uso**: Tanto para CLI como GUI
- **Gitignore completo**: Archivos Python, UV, temporales e IDE
- **Pyproject.toml optimizado**: Configuración UV con metadatos del proyecto

### 🔧 Características Técnicas Destacadas

#### Robustez
- Manejo de excepciones HTTP y de red
- Validación de URLs y parámetros de entrada
- Recuperación automática de errores transitorios
- Verificación de integridad de archivos descargados

#### Performance
- Requests con timeout configurable
- Reutilización de sesiones HTTP
- Buffering optimizado para descargas grandes
- Uso eficiente de memoria para archivos grandes

#### Usabilidad
- Interfaz intuitiva con feedback visual
- Mensajes de error descriptivos y amigables
- Progreso detallado con tiempo estimado
- Configuración flexible por tipo de archivo

#### Compatibilidad
- Compatible con Python 3.8+
- Funciona en Linux, macOS y Windows
- Detección automática de dependencias de sistema
- Fallback graceful entre interfaces

### 🎯 Casos de Uso Soportados

- **Estudiantes**: Descarga de material educativo de visuales.ucv.cu
- **Archivistas**: Backup de contenido con organización automática
- **Desarrolladores**: Base modular para extensión con otros sitios
- **Usuarios casuales**: Interfaz simple para descargas ocasionales
- **Power users**: CLI avanzado con control granular

### 📊 Estadísticas del Proyecto

- **Líneas de código**: ~800+ líneas distribuidas modularmente
- **Archivos de código**: 8 archivos Python organizados
- **Dependencias**: 4 dependencias externas mínimas
- **Interfaces**: 2 interfaces completas (CLI y GUI)
- **Tipos de archivo**: 4 categorías con 15+ extensiones soportadas

### 🚀 Mejoras de Rendimiento

- Arquitectura modular que facilita mantenimiento
- Separación clara de responsabilidades
- Código reutilizable entre interfaces
- Estructura preparada para funcionalidades futuras
- Testing framework listo para implementar

---

## Formato de Versiones

Este proyecto utiliza [Semantic Versioning](https://semver.org/):

- **MAJOR**: Cambios incompatibles en la API
- **MINOR**: Funcionalidad nueva compatible con versiones anteriores  
- **PATCH**: Correcciones de bugs compatibles

## Tipos de Cambios

- **Added** - para nuevas funcionalidades
- **Changed** - para cambios en funcionalidades existentes
- **Deprecated** - para funcionalidades que se eliminarán pronto
- **Removed** - para funcionalidades eliminadas
- **Fixed** - para corrección de bugs
- **Security** - para mejoras de seguridad 