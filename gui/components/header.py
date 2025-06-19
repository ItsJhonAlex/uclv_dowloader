"""
Header component for UCLV Downloader GUI
"""

import tkinter as tk
from tkinter import ttk
from .styles import ModernStyles


class HeaderComponent:
    """Modern header component with title and branding"""
    
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        
        self._setup_component()
    
    def _setup_component(self):
        """Setup the header component"""
        # Main container with reduced padding for better space usage
        container = ttk.Frame(self.frame)
        container.pack(fill=tk.X, padx=ModernStyles.get_spacing('md'), 
                      pady=(ModernStyles.get_spacing('md'), ModernStyles.get_spacing('sm')))
        
        # Logo and title section
        title_frame = ttk.Frame(container)
        title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Main title with icon
        title_container = ttk.Frame(title_frame)
        title_container.pack(anchor=tk.W)
        
        # App icon (emoji for now, could be replaced with actual icon)
        icon_label = ttk.Label(title_container, text="🎬", 
                              font=('Segoe UI', 24, 'normal'))
        icon_label.pack(side=tk.LEFT, padx=(0, ModernStyles.get_spacing('md')))
        
        # Title text
        title_text_frame = ttk.Frame(title_container)
        title_text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Main title
        title_label = ttk.Label(title_text_frame, text="UCLV Downloader",
                               style='Title.TLabel')
        title_label.pack(anchor=tk.W)
        
        # Subtitle
        subtitle_label = ttk.Label(title_text_frame, 
                                  text="Descargador de videos y subtítulos para visuales.ucv.cu",
                                  style='Caption.TLabel')
        subtitle_label.pack(anchor=tk.W)
        
        # Version info (right side)
        version_frame = ttk.Frame(container)
        version_frame.pack(side=tk.RIGHT)
        
        version_label = ttk.Label(version_frame, text="v1.0.0",
                                 style='Caption.TLabel')
        version_label.pack(anchor=tk.E)
        
        # Separator line
        separator = ttk.Separator(self.frame, orient='horizontal')
        separator.pack(fill=tk.X, padx=ModernStyles.get_spacing('lg'),
                      pady=(ModernStyles.get_spacing('sm'), 0))
    
    def pack(self, **kwargs):
        """Pack the header component"""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the header component"""
        self.frame.grid(**kwargs)
    
    def place(self, **kwargs):
        """Place the header component"""
        self.frame.place(**kwargs)
    
    def update_version(self, version: str):
        """Update the version display"""
        # This could be enhanced to find and update the version label
        pass 