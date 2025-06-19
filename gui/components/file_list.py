"""
File List component for UCLV Downloader GUI
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Tuple, Callable, Optional
from .styles import ModernStyles


class FileListComponent:
    """Modern file list component with treeview"""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.LabelFrame(parent, text="📋 Archivos encontrados", 
                                   style='Section.TLabelframe', 
                                   padding=ModernStyles.get_spacing('lg'))
        
        # Data storage
        self.files_data = []
        
        # UI components
        self.tree = None
        self.stats_label = None
        
        self._setup_component()
    
    def _setup_component(self):
        """Setup the file list component"""
        container = ttk.Frame(self.frame)
        container.pack(fill=tk.BOTH, expand=True)
        container.rowconfigure(1, weight=1)
        container.columnconfigure(0, weight=1)
        
        # Statistics
        self.stats_label = ttk.Label(container, text="No hay archivos cargados",
                                    style='Caption.TLabel')
        self.stats_label.grid(row=0, column=0, sticky=tk.W, 
                             pady=(0, ModernStyles.get_spacing('sm')))
        
        # Treeview container
        tree_frame = ttk.Frame(container)
        tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        
        # Treeview with reduced height for better fit
        columns = ('Tipo', 'Tamaño')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='tree headings',
                                style='Modern.Treeview', height=6)
        
        # Headers
        self.tree.heading('#0', text='📄 Nombre del archivo')
        self.tree.heading('Tipo', text='🏷️ Tipo')
        self.tree.heading('Tamaño', text='📏 Tamaño')
        
        # Column widths
        self.tree.column('#0', width=400, minwidth=200)
        self.tree.column('Tipo', width=100, minwidth=80)
        self.tree.column('Tamaño', width=100, minwidth=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    
    def set_files(self, files: List[Tuple[str, str, str]]):
        """Set files to display"""
        self.files_data = files
        self._update_display()
    
    def _update_display(self):
        """Update treeview display"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # File type icons
        icons = {
            'video': '🎬',
            'subtitle': '📝', 
            'image': '🖼️',
            'info': '📄'
        }
        
        # Add files
        for filename, file_url, file_type in self.files_data:
            icon = icons.get(file_type, '📄')
            self.tree.insert('', tk.END,
                           text=f"{icon} {filename}",
                           values=(file_type.title(), 'Desconocido'))
        
        # Update stats
        count = len(self.files_data)
        if count == 0:
            self.stats_label.config(text="No hay archivos cargados")
        else:
            self.stats_label.config(text=f"📊 {count} archivos encontrados")
    
    def clear_files(self):
        """Clear all files"""
        self.files_data = []
        self._update_display()
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs) 