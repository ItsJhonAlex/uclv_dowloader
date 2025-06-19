"""
CLI Interface for UCLV Downloader
"""

import sys
from pathlib import Path
from typing import Optional

from core import UCLVDownloader, URLUtils, FileUtils


class CLIInterface:
    """Command Line Interface for UCLV Downloader"""
    
    def __init__(self):
        self.downloader = UCLVDownloader()
        
    def print_banner(self):
        """Print application banner"""
        print("🎬 UCLV Downloader - Descargador de Videos y Subtítulos")
        print("=" * 60)
        
    def get_url_from_user(self) -> str:
        """Get URL from user input with validation"""
        while True:
            url = input("\n📎 Ingresa la URL de la carpeta a descargar: ").strip()
            
            if not url:
                print("❌ Por favor ingresa una URL válida")
                continue
                
            if not URLUtils.is_valid_url(url):
                print("❌ La URL debe comenzar con http:// o https://")
                continue
                
            return url
    
    def configure_download_options(self):
        """Configure download options interactively"""
        print("\n🔧 Configuración de descarga:")
        print("¿Qué tipos de archivos quieres descargar?")
        
        videos = self._ask_yes_no("📹 ¿Descargar videos?", default=True)
        subtitles = self._ask_yes_no("📝 ¿Descargar subtítulos?", default=True)
        images = self._ask_yes_no("🖼️ ¿Descargar imágenes?", default=False)
        info = self._ask_yes_no("📄 ¿Descargar archivos de información (.nfo)?", default=False)
        
        self.downloader.configure_downloads(
            videos=videos,
            subtitles=subtitles,
            images=images,
            info=info
        )
        
        # Show summary
        enabled_types = []
        if videos: enabled_types.append("Videos")
        if subtitles: enabled_types.append("Subtítulos")
        if images: enabled_types.append("Imágenes")
        if info: enabled_types.append("Info")
        
        print(f"\n✅ Configuración: {', '.join(enabled_types)}")
    
    def _ask_yes_no(self, question: str, default: bool = True) -> bool:
        """Ask yes/no question with default"""
        default_str = "S/n" if default else "s/N"
        response = input(f"{question} [{default_str}]: ").strip().lower()
        
        if not response:
            return default
        
        return response in ['s', 'si', 'sí', 'y', 'yes']
    
    def preview_files(self, url: str) -> bool:
        """Preview files before downloading"""
        try:
            print("\n🔍 Analizando URL...")
            files = self.downloader.get_file_list(url)
            
            if not files:
                print("❌ No se encontraron archivos para descargar")
                return False
            
            # Group by type
            file_types = {}
            for filename, _, file_type in files:
                if file_type not in file_types:
                    file_types[file_type] = []
                file_types[file_type].append(filename)
            
            print(f"\n📊 Archivos encontrados ({len(files)} total):")
            for file_type, filenames in file_types.items():
                icon = self._get_type_icon(file_type)
                print(f"{icon} {file_type.title()}: {len(filenames)}")
                
                # Show first few files as preview
                preview_count = min(3, len(filenames))
                for i in range(preview_count):
                    print(f"   • {filenames[i]}")
                
                if len(filenames) > preview_count:
                    print(f"   ... y {len(filenames) - preview_count} más")
                print()
            
            # Ask for confirmation
            return self._ask_yes_no("¿Continuar con la descarga?", default=True)
            
        except Exception as e:
            print(f"❌ Error al analizar la URL: {e}")
            return False
    
    def _get_type_icon(self, file_type: str) -> str:
        """Get icon for file type"""
        icons = {
            'video': '📹',
            'subtitle': '📝',
            'image': '🖼️',
            'info': '📄',
            'other': '📄'
        }
        return icons.get(file_type, '📄')
    
    def show_download_progress(self, result: dict):
        """Show download results"""
        print("\n" + "=" * 60)
        
        if result['success']:
            print("✅ Descarga completada exitosamente!")
        else:
            print("⚠️ Descarga completada con errores")
        
        print(f"📊 Estadísticas:")
        print(f"   • Total: {result['total']} archivos")
        print(f"   • Exitosos: {result['completed']}")
        print(f"   • Fallidos: {len(result.get('failed', []))}")
        print(f"   • Duración: {result.get('duration', 0):.1f} segundos")
        print(f"📂 Archivos guardados en: {result['download_path']}")
        
        # Show file type statistics
        if 'file_stats' in result:
            print(f"\n📈 Por tipo de archivo:")
            for file_type, count in result['file_stats'].items():
                if count > 0:
                    icon = self._get_type_icon(file_type)
                    print(f"   {icon} {file_type.title()}: {count}")
        
        # Show failed files if any
        if result.get('failed'):
            print(f"\n❌ Archivos que fallaron:")
            for failed in result['failed'][:5]:  # Show first 5
                print(f"   • {failed}")
            if len(result['failed']) > 5:
                print(f"   ... y {len(result['failed']) - 5} más")
    
    def run(self):
        """Main CLI loop"""
        try:
            self.print_banner()
            
            # Get URL
            url = self.get_url_from_user()
            
            # Configure options
            self.configure_download_options()
            
            # Preview files
            if not self.preview_files(url):
                print("\n👋 Descarga cancelada")
                return
            
            # Start download
            print("\n🚀 Iniciando descarga...")
            result = self.downloader.download_from_url(url)
            
            # Show results
            self.show_download_progress(result)
            
        except KeyboardInterrupt:
            print("\n\n⏹️ Programa interrumpido por el usuario")
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
        finally:
            print("\n🎯 ¡Gracias por usar UCLV Downloader!")


def main():
    """Entry point for CLI interface"""
    cli = CLIInterface()
    cli.run()


if __name__ == "__main__":
    main()
