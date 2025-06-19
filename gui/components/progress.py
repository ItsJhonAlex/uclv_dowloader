"""
Progress component for UCLV Downloader GUI
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional
from .styles import ModernStyles


class ProgressComponent:
    """Modern progress component with progress bar and status"""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.LabelFrame(parent, text="📊 Progreso de descarga", 
                                   style='Section.TLabelframe', 
                                   padding=ModernStyles.get_spacing('lg'))
        
        # State variables
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Listo para descargar")
        self.current_file_var = tk.StringVar(value="")
        self.stats_var = tk.StringVar(value="")
        
        # UI components
        self.progress_bar = None
        self.status_label = None
        self.current_file_label = None
        self.stats_label = None
        self.eta_label = None
        
        self._setup_component()
    
    def _setup_component(self):
        """Setup the progress component"""
        # Main container
        container = ttk.Frame(self.frame)
        container.pack(fill=tk.X)
        container.columnconfigure(0, weight=1)
        
        # Progress bar section
        self._create_progress_section(container)
        
        # Status section
        self._create_status_section(container)
        
        # Current file section
        self._create_current_file_section(container)
        
        # Statistics section
        self._create_stats_section(container)
    
    def _create_progress_section(self, parent):
        """Create progress bar section"""
        progress_frame = ttk.Frame(parent)
        progress_frame.grid(row=0, column=0, sticky=(tk.W, tk.E),
                           pady=(0, ModernStyles.get_spacing('md')))
        progress_frame.columnconfigure(0, weight=1)
        
        # Progress bar with reduced length for better fit
        self.progress_bar = ttk.Progressbar(progress_frame, 
                                           variable=self.progress_var,
                                           maximum=100,
                                           style='Modern.Horizontal.TProgressbar',
                                           length=300)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E),
                              pady=(0, ModernStyles.get_spacing('sm')))
        
        # Progress percentage
        self.progress_percent_label = ttk.Label(progress_frame, text="0%",
                                               style='Heading.TLabel')
        self.progress_percent_label.grid(row=0, column=1, sticky=tk.E,
                                        padx=(ModernStyles.get_spacing('md'), 0))
    
    def _create_status_section(self, parent):
        """Create status section"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E),
                         pady=(0, ModernStyles.get_spacing('sm')))
        
        # Status icon and text
        status_container = ttk.Frame(status_frame)
        status_container.pack(anchor=tk.W)
        
        self.status_icon_label = ttk.Label(status_container, text="⏳",
                                          style='Heading.TLabel')
        self.status_icon_label.pack(side=tk.LEFT,
                                   padx=(0, ModernStyles.get_spacing('sm')))
        
        self.status_label = ttk.Label(status_container, textvariable=self.status_var,
                                     style='Status.TLabel')
        self.status_label.pack(side=tk.LEFT)
    
    def _create_current_file_section(self, parent):
        """Create current file section"""
        current_file_frame = ttk.Frame(parent)
        current_file_frame.grid(row=2, column=0, sticky=(tk.W, tk.E),
                               pady=(0, ModernStyles.get_spacing('sm')))
        current_file_frame.columnconfigure(1, weight=1)
        
        # Current file label
        ttk.Label(current_file_frame, text="📄 Archivo actual:",
                 style='Caption.TLabel').grid(row=0, column=0, sticky=tk.W,
                                            padx=(0, ModernStyles.get_spacing('sm')))
        
        # Current file name (with scrolling for long names)
        self.current_file_label = ttk.Label(current_file_frame, 
                                           textvariable=self.current_file_var,
                                           style='Body.TLabel')
        self.current_file_label.grid(row=0, column=1, sticky=(tk.W, tk.E))
    
    def _create_stats_section(self, parent):
        """Create statistics section"""
        stats_frame = ttk.Frame(parent)
        stats_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        # Statistics grid
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill=tk.X)
        
        # Configure grid columns
        for i in range(4):
            stats_grid.columnconfigure(i, weight=1)
        
        # Downloaded files
        self.downloaded_label = ttk.Label(stats_grid, text="📥 Descargados: 0",
                                         style='Caption.TLabel')
        self.downloaded_label.grid(row=0, column=0, sticky=tk.W)
        
        # Total files
        self.total_label = ttk.Label(stats_grid, text="📋 Total: 0",
                                    style='Caption.TLabel')
        self.total_label.grid(row=0, column=1, sticky=tk.W)
        
        # Download speed
        self.speed_label = ttk.Label(stats_grid, text="⚡ Velocidad: --",
                                    style='Caption.TLabel')
        self.speed_label.grid(row=0, column=2, sticky=tk.W)
        
        # ETA
        self.eta_label = ttk.Label(stats_grid, text="⏰ Tiempo restante: --",
                                  style='Caption.TLabel')
        self.eta_label.grid(row=0, column=3, sticky=tk.W)
        
        # Errors (if any)
        self.errors_label = ttk.Label(stats_grid, text="",
                                     style='Error.TLabel')
        self.errors_label.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E),
                              pady=(ModernStyles.get_spacing('xs'), 0))
    
    def set_progress(self, percentage: float):
        """Set progress percentage (0-100)"""
        self.progress_var.set(percentage)
        self.progress_percent_label.config(text=f"{percentage:.1f}%")
    
    def set_status(self, status: str, status_type: str = 'normal'):
        """Set status message with type"""
        self.status_var.set(status)
        
        # Update icon and style based on status type
        icons = {
            'normal': '⏳',
            'downloading': '⬇️',
            'success': '✅',
            'error': '❌',
            'warning': '⚠️',
            'paused': '⏸️',
            'cancelled': '❌'
        }
        
        styles = {
            'normal': 'Status.TLabel',
            'downloading': 'Status.TLabel',
            'success': 'Success.TLabel',
            'error': 'Error.TLabel',
            'warning': 'Warning.TLabel',
            'paused': 'Warning.TLabel',
            'cancelled': 'Error.TLabel'
        }
        
        icon = icons.get(status_type, '⏳')
        style = styles.get(status_type, 'Status.TLabel')
        
        self.status_icon_label.config(text=icon)
        self.status_label.config(style=style)
    
    def set_current_file(self, filename: str):
        """Set current file being downloaded"""
        # Truncate long filenames for display
        if len(filename) > 50:
            display_name = filename[:47] + "..."
        else:
            display_name = filename
        
        self.current_file_var.set(display_name)
    
    def update_stats(self, downloaded: int = 0, total: int = 0, 
                    speed: str = "--", eta: str = "--", errors: int = 0):
        """Update download statistics"""
        self.downloaded_label.config(text=f"📥 Descargados: {downloaded}")
        self.total_label.config(text=f"📋 Total: {total}")
        self.speed_label.config(text=f"⚡ Velocidad: {speed}")
        self.eta_label.config(text=f"⏰ Tiempo restante: {eta}")
        
        # Show errors if any
        if errors > 0:
            self.errors_label.config(text=f"⚠️ Errores: {errors}")
        else:
            self.errors_label.config(text="")
    
    def reset_progress(self):
        """Reset progress to initial state"""
        self.set_progress(0)
        self.set_status("Listo para descargar", 'normal')
        self.set_current_file("")
        self.update_stats()
    
    def set_indeterminate(self, active: bool = True):
        """Set progress bar to indeterminate mode"""
        if active:
            self.progress_bar.config(mode='indeterminate')
            self.progress_bar.start(10)  # 10ms interval
            self.progress_percent_label.config(text="...")
        else:
            self.progress_bar.stop()
            self.progress_bar.config(mode='determinate')
    
    def animate_success(self):
        """Animate success completion"""
        self.set_progress(100)
        self.set_status("✅ Descarga completada exitosamente", 'success')
        
        # Brief animation
        original_color = ModernStyles.get_color('success')
        # Could add color animation here if needed
    
    def show_error(self, error_message: str):
        """Show error state"""
        self.set_status(f"❌ Error: {error_message}", 'error')
        self.set_indeterminate(False)
    
    def pack(self, **kwargs):
        """Pack the component"""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the component"""
        self.frame.grid(**kwargs)
    
    def place(self, **kwargs):
        """Place the component"""
        self.frame.place(**kwargs) 