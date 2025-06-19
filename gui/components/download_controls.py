"""
Download Controls component for UCLV Downloader GUI
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Callable, Optional
from .styles import ModernStyles


class DownloadControlsComponent:
    """Modern download controls component with path selection and action buttons"""
    
    def __init__(self, parent, on_download: Optional[Callable] = None, 
                 on_cancel: Optional[Callable] = None):
        self.parent = parent
        self.on_download = on_download
        self.on_cancel = on_cancel
        self.frame = ttk.LabelFrame(parent, text="💾 Controles de descarga", 
                                   style='Section.TLabelframe', 
                                   padding=ModernStyles.get_spacing('lg'))
        
        # State variables
        self.download_path_var = tk.StringVar(value="./descarga")
        self.is_downloading = False
        
        # UI components
        self.path_entry = None
        self.download_btn = None
        self.cancel_btn = None
        self.about_btn = None
        
        self._setup_component()
    
    def _setup_component(self):
        """Setup the download controls component"""
        # Main container
        container = ttk.Frame(self.frame)
        container.pack(fill=tk.X)
        container.columnconfigure(1, weight=1)
        
        # Download path section
        self._create_path_section(container)
        
        # Control buttons section
        self._create_buttons_section(container)
    
    def _create_path_section(self, parent):
        """Create download path selection section"""
        path_frame = ttk.Frame(parent)
        path_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E),
                       pady=(0, ModernStyles.get_spacing('lg')))
        path_frame.columnconfigure(1, weight=1)
        
        # Path label
        ttk.Label(path_frame, text="📁 Carpeta de descarga:",
                 style='Heading.TLabel').grid(row=0, column=0, sticky=tk.W,
                                            padx=(0, ModernStyles.get_spacing('md')))
        
        # Path entry
        self.path_entry = ttk.Entry(path_frame, textvariable=self.download_path_var,
                                   style='Modern.TEntry', font=ModernStyles.get_font('body'))
        self.path_entry.grid(row=0, column=1, sticky=(tk.W, tk.E),
                            padx=(0, ModernStyles.get_spacing('sm')))
        
        # Browse button
        browse_btn = ttk.Button(path_frame, text="📂 Explorar",
                               style='Secondary.TButton',
                               command=self._browse_download_path)
        browse_btn.grid(row=0, column=2)
        
        # Path info
        path_info_frame = ttk.Frame(path_frame)
        path_info_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E),
                            pady=(ModernStyles.get_spacing('sm'), 0))
        
        self.path_info_label = ttk.Label(path_info_frame, text="",
                                        style='Caption.TLabel')
        self.path_info_label.pack(anchor=tk.W)
        
        # Update path info initially
        self._update_path_info()
        
        # Bind path changes
        self.download_path_var.trace('w', lambda *args: self._update_path_info())
    
    def _create_buttons_section(self, parent):
        """Create control buttons section"""
        buttons_frame = ttk.Frame(parent)
        buttons_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Main action buttons (left side)
        main_buttons_frame = ttk.Frame(buttons_frame)
        main_buttons_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Download button
        self.download_btn = ttk.Button(main_buttons_frame, text="⬇️ Iniciar descarga",
                                      style='Primary.TButton',
                                      command=self._on_download_clicked,
                                      state=tk.DISABLED)
        self.download_btn.pack(side=tk.LEFT, padx=(0, ModernStyles.get_spacing('sm')))
        
        # Cancel button
        self.cancel_btn = ttk.Button(main_buttons_frame, text="❌ Cancelar descarga",
                                    style='Error.TButton',
                                    command=self._on_cancel_clicked,
                                    state=tk.DISABLED)
        self.cancel_btn.pack(side=tk.LEFT, padx=(0, ModernStyles.get_spacing('sm')))
        
        # Pause/Resume button (for future enhancement)
        self.pause_btn = ttk.Button(main_buttons_frame, text="⏸️ Pausar",
                                   style='Warning.TButton',
                                   command=self._on_pause_clicked,
                                   state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=(0, ModernStyles.get_spacing('sm')))
        
        # Secondary buttons (right side)
        secondary_buttons_frame = ttk.Frame(buttons_frame)
        secondary_buttons_frame.pack(side=tk.RIGHT)
        
        # About button
        self.about_btn = ttk.Button(secondary_buttons_frame, text="ℹ️ Acerca de",
                                   style='Secondary.TButton',
                                   command=self._show_about)
        self.about_btn.pack(side=tk.LEFT, padx=(0, ModernStyles.get_spacing('sm')))
        
        # Settings button (for future enhancement)
        settings_btn = ttk.Button(secondary_buttons_frame, text="⚙️ Configuración",
                                 style='Secondary.TButton',
                                 command=self._show_settings)
        settings_btn.pack(side=tk.LEFT)
    
    def _browse_download_path(self):
        """Browse for download directory"""
        current_path = self.download_path_var.get()
        
        # Use current path as initial directory if it exists
        initial_dir = current_path if Path(current_path).exists() else str(Path.home())
        
        selected_path = filedialog.askdirectory(
            title="Seleccionar carpeta de descarga",
            initialdir=initial_dir
        )
        
        if selected_path:
            self.download_path_var.set(selected_path)
    
    def _update_path_info(self):
        """Update path information display"""
        path = self.download_path_var.get()
        
        if not path:
            self.path_info_label.config(text="⚠️ Por favor selecciona una carpeta")
            return
        
        path_obj = Path(path)
        
        try:
            if path_obj.exists():
                if path_obj.is_dir():
                    # Get directory info
                    try:
                        files_count = len(list(path_obj.iterdir()))
                        self.path_info_label.config(text=f"✅ Carpeta válida ({files_count} elementos)")
                    except PermissionError:
                        self.path_info_label.config(text="⚠️ Sin permisos para leer la carpeta")
                else:
                    self.path_info_label.config(text="❌ La ruta no es una carpeta")
            else:
                # Check if parent directory exists for creation
                if path_obj.parent.exists():
                    self.path_info_label.config(text="💡 La carpeta se creará automáticamente")
                else:
                    self.path_info_label.config(text="❌ La ruta padre no existe")
        except Exception as e:
            self.path_info_label.config(text=f"❌ Error: {str(e)}")
    
    def _on_download_clicked(self):
        """Handle download button click"""
        path = self.download_path_var.get().strip()
        
        if not path:
            messagebox.showerror("Error", "Por favor selecciona una carpeta de descarga")
            return
        
        # Validate path
        path_obj = Path(path)
        try:
            # Create directory if it doesn't exist
            if not path_obj.exists():
                path_obj.mkdir(parents=True, exist_ok=True)
                
            if not path_obj.is_dir():
                messagebox.showerror("Error", "La ruta especificada no es una carpeta válida")
                return
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la carpeta: {e}")
            return
        
        # Call download callback
        if self.on_download:
            self.on_download(path)
    
    def _on_cancel_clicked(self):
        """Handle cancel button click"""
        if self.on_cancel:
            self.on_cancel()
    
    def _on_pause_clicked(self):
        """Handle pause/resume button click"""
        # Future enhancement for pause/resume functionality
        pass
    
    def _show_about(self):
        """Show about dialog"""
        about_text = """🎬 UCLV Downloader v1.0.0

Descargador de videos y subtítulos para visuales.ucv.cu

Características:
• Descarga de videos, subtítulos, imágenes e info
• Interfaz gráfica moderna y amigable
• Progreso en tiempo real
• Multiplataforma (Windows, Linux, macOS)

Desarrollado con ❤️ usando Python y Tkinter

© 2025 - Código abierto"""
        
        messagebox.showinfo("Acerca de UCLV Downloader", about_text)
    
    def _show_settings(self):
        """Show settings dialog"""
        # Future enhancement for settings
        messagebox.showinfo("Configuración", "Próximamente: configuración avanzada")
    
    def set_download_state(self, downloading: bool):
        """Update UI state for downloading"""
        self.is_downloading = downloading
        
        if downloading:
            self.download_btn.config(text="🔄 Descargando...", state=tk.DISABLED)
            self.cancel_btn.config(state=tk.NORMAL)
            self.pause_btn.config(state=tk.NORMAL)
            self.path_entry.config(state=tk.DISABLED)
        else:
            self.download_btn.config(text="⬇️ Iniciar descarga", state=tk.NORMAL)
            self.cancel_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.DISABLED, text="⏸️ Pausar")
            self.path_entry.config(state=tk.NORMAL)
    
    def enable_download(self, enabled: bool = True):
        """Enable or disable download button"""
        if not self.is_downloading:
            state = tk.NORMAL if enabled else tk.DISABLED
            self.download_btn.config(state=state)
    
    def get_download_path(self) -> str:
        """Get the selected download path"""
        return self.download_path_var.get().strip()
    
    def set_download_path(self, path: str):
        """Set the download path"""
        self.download_path_var.set(path)
    
    def pack(self, **kwargs):
        """Pack the component"""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the component"""
        self.frame.grid(**kwargs)
    
    def place(self, **kwargs):
        """Place the component"""
        self.frame.place(**kwargs) 