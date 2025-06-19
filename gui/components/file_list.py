"""
File List component for UCLV Downloader GUI with Individual File Selection
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Tuple, Callable, Optional, Dict
from .styles import ModernStyles


class FileListComponent:
    """Modern file list component with individual file selection"""
    
    def __init__(self, parent, on_selection_changed: Optional[Callable] = None):
        self.parent = parent
        self.on_selection_changed = on_selection_changed
        self.frame = ttk.LabelFrame(parent, text="📋 Seleccionar archivos a descargar", 
                                   style='Section.TLabelframe', 
                                   padding=ModernStyles.get_spacing('lg'))
        
        # Data storage
        self.files_data = []  # List of (filename, file_url, file_type)
        self.file_vars = {}   # Dict of {index: BooleanVar} for checkboxes
        self.file_info = {}   # Dict of {index: file_info} for additional data
        
        # UI components
        self.tree = None
        self.stats_label = None
        self.selection_stats_label = None
        
        self._setup_component()
    
    def _setup_component(self):
        """Setup the file list component"""
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
        
        # Selection buttons
        ttk.Button(controls_frame, text="✅ Seleccionar todos",
                  style='Secondary.TButton',
                  command=self._select_all).pack(side=tk.LEFT, 
                                               padx=(0, ModernStyles.get_spacing('sm')))
        
        ttk.Button(controls_frame, text="❌ Deseleccionar todos",
                  style='Secondary.TButton',
                  command=self._deselect_all).pack(side=tk.LEFT,
                                                 padx=(0, ModernStyles.get_spacing('sm')))
        
        ttk.Button(controls_frame, text="🔄 Invertir selección",
                  style='Secondary.TButton',
                  command=self._invert_selection).pack(side=tk.LEFT,
                                                     padx=(0, ModernStyles.get_spacing('sm')))
        
        # Type-based selection buttons
        ttk.Button(controls_frame, text="🎬 Solo videos",
                  style='Secondary.TButton',
                  command=self._select_videos_only).pack(side=tk.LEFT,
                                                        padx=(0, ModernStyles.get_spacing('sm')))
        
        ttk.Button(controls_frame, text="📝 Solo subtítulos",
                  style='Secondary.TButton',
                  command=self._select_subtitles_only).pack(side=tk.LEFT)
    
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
        
        # Bind double-click to toggle selection
        self.tree.bind('<Double-1>', self._on_tree_double_click)
        self.tree.bind('<Button-1>', self._on_tree_click)
    
    def set_files(self, files: List[Tuple[str, str, str]]):
        """Set files to display with individual selection"""
        self.files_data = files
        self.file_vars = {}
        self.file_info = {}
        
        # Create BooleanVar for each file (all selected by default)
        for i in range(len(files)):
            var = tk.BooleanVar(value=True)
            var.trace('w', lambda *args, idx=i: self._on_selection_changed_internal(idx))
            self.file_vars[i] = var
        
        self._update_display()
        self._update_selection_stats()
    
    def _update_display(self):
        """Update treeview display with checkboxes"""
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
        for i, (filename, file_url, file_type) in enumerate(self.files_data):
            icon = icons.get(file_type, '📄')
            selected = self.file_vars[i].get()
            checkbox_icon = "☑️" if selected else "☐"
            
            # Insert item with data
            item_id = self.tree.insert('', tk.END,
                                      text=f"{icon} {filename}",
                                      values=(checkbox_icon, file_type.title(), 'Calculando...'),
                                      tags=(str(i),))
            
            # Store item mapping for click handling
            self.file_info[i] = {'item_id': item_id, 'filename': filename, 'url': file_url, 'type': file_type}
        
        # Update general stats
        count = len(self.files_data)
        if count == 0:
            self.stats_label.config(text="No hay archivos cargados")
        else:
            # Count by type
            type_counts = {}
            for _, _, file_type in self.files_data:
                type_counts[file_type] = type_counts.get(file_type, 0) + 1
            
            type_summary = []
            for file_type, count in type_counts.items():
                icon = icons.get(file_type, '📄')
                type_summary.append(f"{icon} {count}")
            
            self.stats_label.config(text=f"📊 {count} archivos encontrados: {' | '.join(type_summary)}")
    
    def _on_tree_click(self, event):
        """Handle tree click to toggle checkboxes"""
        item = self.tree.identify('item', event.x, event.y)
        column = self.tree.identify('column', event.x, event.y)
        
        if item and column == '#2':  # Clicked on 'Seleccionar' column
            # Get file index from tags
            tags = self.tree.item(item, 'tags')
            if tags:
                file_index = int(tags[0])
                # Toggle selection
                current_value = self.file_vars[file_index].get()
                self.file_vars[file_index].set(not current_value)
    
    def _on_tree_double_click(self, event):
        """Handle double-click to toggle selection"""
        item = self.tree.identify('item', event.x, event.y)
        if item:
            # Get file index from tags
            tags = self.tree.item(item, 'tags')
            if tags:
                file_index = int(tags[0])
                # Toggle selection
                current_value = self.file_vars[file_index].get()
                self.file_vars[file_index].set(not current_value)
    
    def _on_selection_changed_internal(self, file_index: int):
        """Handle individual file selection change"""
        # Update checkbox display
        if file_index in self.file_info:
            item_id = self.file_info[file_index]['item_id']
            selected = self.file_vars[file_index].get()
            checkbox_icon = "☑️" if selected else "☐"
            
            # Update the treeview item
            current_values = list(self.tree.item(item_id, 'values'))
            current_values[0] = checkbox_icon
            self.tree.item(item_id, values=current_values)
        
        # Update selection stats
        self._update_selection_stats()
        
        # Notify parent component
        if self.on_selection_changed:
            self.on_selection_changed(self.get_selected_files())
    
    def _update_selection_stats(self):
        """Update selection statistics"""
        if not self.file_vars:
            self.selection_stats_label.config(text="")
            return
        
        selected_count = sum(1 for var in self.file_vars.values() if var.get())
        total_count = len(self.file_vars)
        
        if selected_count == 0:
            self.selection_stats_label.config(text="❌ Ninguno seleccionado", 
                                             style='Error.TLabel')
        elif selected_count == total_count:
            self.selection_stats_label.config(text=f"✅ Todos seleccionados ({selected_count})", 
                                             style='Success.TLabel')
        else:
            self.selection_stats_label.config(text=f"📊 {selected_count} de {total_count} seleccionados", 
                                             style='Heading.TLabel')
    
    def _select_all(self):
        """Select all files"""
        for var in self.file_vars.values():
            var.set(True)
    
    def _deselect_all(self):
        """Deselect all files"""
        for var in self.file_vars.values():
            var.set(False)
    
    def _invert_selection(self):
        """Invert current selection"""
        for var in self.file_vars.values():
            var.set(not var.get())
    
    def _select_videos_only(self):
        """Select only video files"""
        for i, (_, _, file_type) in enumerate(self.files_data):
            self.file_vars[i].set(file_type == 'video')
    
    def _select_subtitles_only(self):
        """Select only subtitle files"""
        for i, (_, _, file_type) in enumerate(self.files_data):
            self.file_vars[i].set(file_type == 'subtitle')
    
    def get_selected_files(self) -> List[Tuple[str, str, str]]:
        """Get list of selected files"""
        selected_files = []
        for i, (filename, file_url, file_type) in enumerate(self.files_data):
            if self.file_vars.get(i, tk.BooleanVar()).get():
                selected_files.append((filename, file_url, file_type))
        return selected_files
    
    def get_selected_count(self) -> int:
        """Get count of selected files"""
        return len(self.get_selected_files())
    
    def has_selection(self) -> bool:
        """Check if any files are selected"""
        return self.get_selected_count() > 0
    
    def get_file_count(self) -> int:
        """Get total file count"""
        return len(self.files_data)
    
    def set_file_selection(self, index: int, selected: bool):
        """Set selection state for a specific file"""
        if index in self.file_vars:
            self.file_vars[index].set(selected)
    
    def clear_files(self):
        """Clear all files"""
        self.files_data = []
        self.file_vars = {}
        self.file_info = {}
        self._update_display()
        self._update_selection_stats()
    
    def pack(self, **kwargs):
        """Pack the component"""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the component"""
        self.frame.grid(**kwargs)
    
    def place(self, **kwargs):
        """Place the component"""
        self.frame.place(**kwargs) 