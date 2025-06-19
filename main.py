#!/usr/bin/env python3
"""
UCLV Downloader - Main launcher
Allows choosing between CLI and GUI interfaces
"""

import sys
import argparse
from pathlib import Path


def main():
    """Main launcher that chooses between CLI and GUI"""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="🎬 UCLV Downloader - Descargador de Videos y Subtítulos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python main.py                    # Lanzar GUI por defecto
  python main.py --cli             # Usar interfaz de línea de comandos
  python main.py --gui             # Usar interfaz gráfica (explícito)
  python main.py --help            # Mostrar esta ayuda
        """
    )
    
    interface_group = parser.add_mutually_exclusive_group()
    interface_group.add_argument(
        '--cli', 
        action='store_true',
        help='Usar interfaz de línea de comandos'
    )
    interface_group.add_argument(
        '--gui', 
        action='store_true',
        help='Usar interfaz gráfica (por defecto)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='UCLV Downloader v1.4.0'
    )
    
    args = parser.parse_args()
    
    # Determine which interface to use
    use_gui = not args.cli  # Default to GUI unless CLI is explicitly requested
    
    try:
        if use_gui:
            print("🚀 Iniciando interfaz gráfica...")
            try:
                from gui import GUIInterface
                gui = GUIInterface()
                gui.run()
            except ImportError as e:
                print(f"❌ Error importando GUI: {e}")
                print("🔄 Cambiando a interfaz CLI...")
                launch_cli()
            except Exception as e:
                print(f"❌ Error en GUI: {e}")
                print("🔄 Cambiando a interfaz CLI...")
                launch_cli()
        else:
            launch_cli()
            
    except KeyboardInterrupt:
        print("\n\n👋 Programa terminado por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()


def launch_cli():
    """Launch CLI interface"""
    print("🚀 Iniciando interfaz de línea de comandos...")
    try:
        from cli import CLIInterface
        cli = CLIInterface()
        cli.run()
    except ImportError as e:
        print(f"❌ Error importando CLI: {e}")
        print("💡 Asegúrate de que todas las dependencias estén instaladas:")
        print("   uv sync")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error en CLI: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def show_banner():
    """Show application banner"""
    banner = """
╔══════════════════════════════════════════════════════════╗
║                🎬 UCLV Downloader v1.0                  ║
║          Descargador de Videos y Subtítulos              ║
║                                                          ║
║  Un descargador modular para visuales.ucv.cu            ║
║                                                          ║
║  🖥️  Interfaz gráfica disponible                        ║
║  💻 Interfaz de línea de comandos                       ║
║  ⚙️  Configuración flexible                             ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


if __name__ == "__main__":
    # Only show banner if no arguments or help is not being shown
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] in ['--gui']):
        show_banner()
    
    main() 