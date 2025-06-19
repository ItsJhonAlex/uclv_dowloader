#!/bin/bash

# UCVL Downloader - Script de Build y Release Automático
# Este script compila el proyecto y crea los paquetes de distribución

set -e  # Salir si hay algún error

echo "🚀 UCVL Downloader - Build y Release Automático"
echo "==============================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar mensajes
print_step() {
    echo -e "${BLUE}🔄 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Cambiar al directorio raíz del proyecto
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Verificar que estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    print_error "No se encontró main.py. Asegúrate de que la estructura del proyecto sea correcta."
    exit 1
fi

# Verificar que UV está instalado
if ! command -v uv &> /dev/null; then
    print_error "UV no está instalado. Instálalo desde https://docs.astral.sh/uv/"
    exit 1
fi

# Paso 1: Sincronizar dependencias
print_step "Sincronizando dependencias con UV..."
uv sync
print_success "Dependencias sincronizadas"

# Paso 2: Ejecutar build
print_step "Compilando ejecutable con PyInstaller..."
uv run python release/build.py
if [ $? -eq 0 ]; then
    print_success "Compilación exitosa"
else
    print_error "Error en la compilación"
    exit 1
fi

# Paso 3: Crear paquetes de release
print_step "Creando paquetes de distribución..."
uv run python release/create_release.py
if [ $? -eq 0 ]; then
    print_success "Paquetes de release creados"
else
    print_error "Error al crear paquetes de release"
    exit 1
fi

# Paso 4: Mostrar información final
echo ""
echo "🎉 ¡Build y Release completados exitosamente!"
echo "=============================================="

# Mostrar archivos generados
echo ""
echo "📁 Archivos generados:"
ls -lh dist/ucvl-downloader 2>/dev/null && echo "   - dist/ucvl-downloader (ejecutable)"
ls -lh *.tar.gz 2>/dev/null && echo "   - $(ls *.tar.gz)"
ls -lh *.zip 2>/dev/null && echo "   - $(ls *.zip)"

echo ""
echo "🚀 Para distribuir:"
echo "   1. Sube los archivos .tar.gz o .zip a GitHub Releases"
echo "   2. O comparte directamente con usuarios finales"
echo "   3. Los usuarios solo necesitan descomprimir y ejecutar"

echo ""
echo "🧪 Para probar localmente:"
echo "   ./dist/ucvl-downloader --help"
echo "   ./dist/ucvl-downloader --cli"
echo "   ./dist/ucvl-downloader  (GUI)"

# Mostrar tamaños
if [ -f "dist/ucvl-downloader" ]; then
    SIZE=$(du -h dist/ucvl-downloader | cut -f1)
    echo ""
    echo "📏 Tamaño del ejecutable: $SIZE"
fi

print_success "¡Todo listo para distribución!" 