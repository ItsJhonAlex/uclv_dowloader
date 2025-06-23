"""
Modern Modular GUI Interface for UCLV Downloader using Components and Managers
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

from .components import (
    HeaderComponent,
    URLInputComponent, 
    FileTypeComponent,
    FileListComponent,
    DownloadControlsComponent,
    ProgressComponent,
    SubtitleSearchComponent,
    ModernStyles
)
from .managers import (
    ScrollManager,
    DownloadManager,
    EventManager,
    UIStateManager
)


class ModernGUIInterface:
    """Modern modular GUI interface for UCLV Downloader"""
    
    def __init__(self):
        # Initialize managers
        self.ui_state = UIStateManager(self)
        self.scroll_manager = None
        self.download_manager = None
        self.event_manager = None
        
        # Create main window
        self.root = self.ui_state.create_main_window()
        
        # Setup modern theme
        self.style = ModernStyles.setup_theme(self.root)
        
        # Initialize managers that need GUI reference
        self._initialize_managers()
        
        # Initialize components
        self._setup_components()
        
        # Layout components
        self._setup_layout()
        
        # Setup event bindings
        self.event_manager.setup_bindings()
    
    def _initialize_managers(self):
        """Initialize managers that need the GUI reference"""
        self.scroll_manager = ScrollManager(self.root)
        self.download_manager = DownloadManager(self)
        self.event_manager = EventManager(self)
    
    def _setup_components(self):
        """Initialize all GUI components with scrollable container"""
        # Create main scrollable frame
        self.scrollable_frame = self.scroll_manager.create_scrollable_container()
        
        # Create components inside scrollable area
        self.header = HeaderComponent(self.scrollable_frame)
        
        self.url_input = URLInputComponent(
            self.scrollable_frame, 
            on_analysis_complete=self.event_manager.on_url_analysis
        )
        
        self.file_types = FileTypeComponent(
            self.scrollable_frame,
            on_selection_changed=self.event_manager.on_file_type_changed
        )
        
        self.file_list = FileListComponent(
            self.scrollable_frame,
            on_selection_changed=self.event_manager.on_file_selection_changed
        )
        
        self.subtitle_search = SubtitleSearchComponent(
            self.scrollable_frame,
            on_subtitles_selected=self.event_manager.on_subtitles_selected
        )
        
        self.download_controls = DownloadControlsComponent(
            self.scrollable_frame,
            on_download=self.event_manager.on_download_started,
            on_cancel=self.event_manager.on_download_cancelled
        )
        
        self.progress = ProgressComponent(self.scrollable_frame)
    
    def _setup_layout(self):
        """Setup component layout in scrollable container"""
        # All components now use pack with proper spacing
        self.header.pack(fill=tk.X, pady=(0, ModernStyles.get_spacing('lg')))
        
        self.url_input.pack(fill=tk.X, pady=(0, ModernStyles.get_spacing('md')))
        
        self.file_types.pack(fill=tk.X, pady=(0, ModernStyles.get_spacing('md')))
        
        # File list with fixed height to prevent excessive expansion
        self.file_list.pack(fill=tk.X, pady=(0, ModernStyles.get_spacing('md')))
        
        # Subtitle search component (initially hidden)
        # Will be shown conditionally when needed
        
        self.download_controls.pack(fill=tk.X, 
                                   pady=(0, ModernStyles.get_spacing('md')))
        
        self.progress.pack(fill=tk.X, pady=(0, ModernStyles.get_spacing('lg')))
        
        # Force canvas to update scroll region after layout
        self.root.after(100, self.scroll_manager.update_scroll_region)
    
    def run(self):
        """Run the GUI application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Aplicación interrumpida por el usuario")
        except Exception as e:
            print(f"Error inesperado: {e}")
            messagebox.showerror("Error", f"Error inesperado: {e}")
        finally:
            if self.root:
                self.root.destroy()


# Keep the alias for backward compatibility
GUIInterface = ModernGUIInterface


def main():
    """Main entry point for GUI"""
    try:
        app = ModernGUIInterface()
        app.run()
    except ImportError as e:
        if 'tkinter' in str(e):
            print("❌ Error: tkinter no está disponible")
            print("En Ubuntu/Debian, instala: sudo apt install python3-tk")
            print("En otros sistemas, consulta la documentación de Python")
        else:
            print(f"❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error al inicializar la interfaz gráfica: {e}")
        return False
    
    return True


if __name__ == "__main__":
    main()
