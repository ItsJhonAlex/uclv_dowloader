"""
File List View - UI components for file list display
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Tuple, Callable, Optional
from ..styling import ModernStyles


class FileListView:
    """View component for file list with tree display"""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.LabelFrame(parent, text="📋 Seleccionar archivos a descargar", 
                                   style='Section.TLabelframe', 
                                   padding=ModernStyles.get_spacing('lg'))
        
        # UI components
        self.tree = None
        self.stats_label = None
        self.selection_stats_label = None
        
        # Event callbacks
        self.on_selection_changed = None
        self.on_tree_click = None
        
        self._setup_view()
    
    def _setup_view(self):
        """Setup the file list view"""
        container = ttk.Frame(self.frame)
        container.pack(fill=tk.BOTH, expand=True)
        container.rowconfigure(2, weight=1)
        container.columnconfigure(0, weight=1)
        
        # Statistics row
        self._create_stats_section(container)
        
        # Selection controls row
        self._create_selection_controls(container)
        
        # Treeview container
        self._create_file_tree(container)
    
    def _create_stats_section(self, parent):
        """Create statistics section"""
        stats_frame = ttk.Frame(parent)
        stats_frame.grid(row=0, column=0, sticky=(tk.W, tk.E),
                        pady=(0, ModernStyles.get_spacing('sm')))
        stats_frame.columnconfigure(1, weight=1)
        
        # Main stats
        self.stats_label = ttk.Label(stats_frame, text="No hay archivos cargados",
                                    style='Caption.TLabel')
        self.stats_label.grid(row=0, column=0, sticky=tk.W)
        
        # Selection stats (right side)
        self.selection_stats_label = ttk.Label(stats_frame, text="",
                                              style='Heading.TLabel')
        self.selection_stats_label.grid(row=0, column=1, sticky=tk.E)
    
    def _create_selection_controls(self, parent):
        """Create selection control buttons"""
        controls_frame = ttk.Frame(parent)
        controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E),
                           pady=(0, ModernStyles.get_spacing('md')))
        
        self.controls_frame = controls_frame  # Store reference for external button additions
    
    def add_control_button(self, text: str, command: Callable, style: str = 'Secondary.TButton'):
        """Add a control button to the controls frame"""
        button = ttk.Button(self.controls_frame, text=text,
                           style=style, command=command)
        button.pack(side=tk.LEFT, padx=(0, ModernStyles.get_spacing('sm')))
        return button
    
    def _create_file_tree(self, parent):
        """Create file tree with checkboxes"""
        tree_frame = ttk.Frame(parent)
        tree_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        
        # Treeview with checkboxes
        columns = ('Seleccionar', 'Tipo', 'Tamaño')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='tree headings',
                                style='Modern.Treeview', height=8)
        
        # Headers
        self.tree.heading('#0', text='📄 Nombre del archivo')
        self.tree.heading('Seleccionar', text='☑️ Seleccionar')
        self.tree.heading('Tipo', text='🏷️ Tipo')
        self.tree.heading('Tamaño', text='📏 Tamaño')
        
        # Column widths
        self.tree.column('#0', width=350, minwidth=200)
        self.tree.column('Seleccionar', width=90, minwidth=80, anchor=tk.CENTER)
        self.tree.column('Tipo', width=100, minwidth=80, anchor=tk.CENTER)
        self.tree.column('Tamaño', width=100, minwidth=80, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind events
        self.tree.bind('<Double-1>', self._on_tree_double_click)
        self.tree.bind('<Button-1>', self._on_tree_click)
    
    def _on_tree_click(self, event):
        """Handle tree click events"""
        if self.on_tree_click:
            item = self.tree.identify('item', event.x, event.y)
            column = self.tree.identify('column', event.x, event.y)
            self.on_tree_click(item, column)
    
    def _on_tree_double_click(self, event):
        """Handle double-click events"""
        item = self.tree.identify('item', event.x, event.y)
        if item and self.on_tree_click:
            self.on_tree_click(item, None, double_click=True)
    
    def update_tree_display(self, files_data: List[Tuple[str, str, str]], file_vars: dict):
        """Update treeview display with files and selection state"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # File type icons
        icons = {
            'video': '🎬',
            'subtitle': '📝', 
            'image': '🖼️',
            'info': '📄',
            'other': '📄'
        }
        
        # Add files with checkboxes
        for i, (filename, file_url, file_type) in enumerate(files_data):
            icon = icons.get(file_type, '📄')
            selected = file_vars[i].get()
            checkbox_icon = "☑️" if selected else "☐"
            
            # Insert item with data
            item_id = self.tree.insert('', tk.END,
                                      text=f"{icon} {filename}",
                                      values=(checkbox_icon, file_type.title(), 'Calculando...'),
                                      tags=(str(i),))
    
    def update_item_selection(self, item_index: int, selected: bool):
        """Update selection display for a specific item"""
        # Find the item with the matching tag
        for item in self.tree.get_children():
            tags = self.tree.item(item, 'tags')
            if tags and int(tags[0]) == item_index:
                checkbox_icon = "☑️" if selected else "☐"
                current_values = list(self.tree.item(item, 'values'))
                current_values[0] = checkbox_icon
                self.tree.item(item, values=current_values)
                break
    
    def update_stats_display(self, stats_text: str):
        """Update main statistics display"""
        self.stats_label.config(text=stats_text)
    
    def update_selection_stats(self, selected_count: int, total_count: int):
        """Update selection statistics"""
        if total_count == 0:
            self.selection_stats_label.config(text="")
            return
        
        if selected_count == 0:
            self.selection_stats_label.config(text="❌ Ninguno seleccionado", 
                                             style='Error.TLabel')
        elif selected_count == total_count:
            self.selection_stats_label.config(text=f"✅ Todos seleccionados ({selected_count})", 
                                             style='Success.TLabel')
        else:
            self.selection_stats_label.config(text=f"📊 {selected_count} de {total_count} seleccionados", 
                                             style='Heading.TLabel')
    
    def set_selection_changed_callback(self, callback: Callable):
        """Set callback for selection changes"""
        self.on_selection_changed = callback
    
    def set_tree_click_callback(self, callback: Callable):
        """Set callback for tree clicks"""
        self.on_tree_click = callback
    
    def pack(self, **kwargs):
        """Pack the view"""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the view"""
        self.frame.grid(**kwargs)
    
    def place(self, **kwargs):
        """Place the view"""
        self.frame.place(**kwargs) 