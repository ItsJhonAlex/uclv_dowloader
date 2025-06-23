"""
UI State Manager - Handles UI state management and updates
"""

import tkinter as tk
from ..components import ModernStyles


class UIStateManager:
    """Manages UI state and updates"""
    
    def __init__(self, gui_interface):
        self.gui = gui_interface
    
    def set_download_state(self, downloading: bool):
        """Update UI state for downloading"""
        # Update download controls
        self.gui.download_controls.set_download_state(downloading)
        
        # Update progress
        if downloading:
            self.gui.progress.set_status("Iniciando descarga...", 'downloading')
            self.gui.progress.set_progress(0)
        else:
            # Only reset if not actually downloading
            self.gui.progress.reset_progress()
    
    def center_window(self, window):
        """Center window on screen"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_main_window(self) -> tk.Tk:
        """Create and configure the main window"""
        root = tk.Tk()
        root.title("🎬 UCLV Downloader")
        root.geometry("950x800")  # Aumentado para mejor visualización
        root.minsize(800, 600)
        root.resizable(True, True)
        
        # Set window icon (if available)
        # root.iconbitmap("icon.ico")  # Uncomment if you have an icon
        
        # Configure main window background
        root.configure(bg=ModernStyles.get_color('bg_primary'))
        
        # Center window on screen
        self.center_window(root)
        
        return root 