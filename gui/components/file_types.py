"""
File Types Selection component for UCLV Downloader GUI
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Callable, Optional
from .styles import ModernStyles


class FileTypeComponent:
    """Modern file type selection component with checkboxes"""
    
    def __init__(self, parent, on_selection_changed: Optional[Callable] = None):
        self.parent = parent
        self.on_selection_changed = on_selection_changed
        self.frame = ttk.LabelFrame(parent, text="🎯 Tipos de archivo a descargar", 
                                   style='Section.TLabelframe', padding=ModernStyles.get_spacing('lg'))
        
        # File type variables
        self.file_types = {
            'videos': {'var': tk.BooleanVar(value=True), 'icon': '🎬', 'label': 'Videos'},
            'subtitles': {'var': tk.BooleanVar(value=True), 'icon': '📝', 'label': 'Subtítulos'},
            'images': {'var': tk.BooleanVar(value=False), 'icon': '🖼️', 'label': 'Imágenes'},
            'info': {'var': tk.BooleanVar(value=False), 'icon': '📄', 'label': 'Info'}
        }
        
        # File extensions info
        self.extensions_info = {
            'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
            'subtitles': ['.srt', '.sub', '.vtt', '.ass', '.ssa'],
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
            'info': ['.nfo', '.txt']
        }
        
        self._setup_component()
        self._setup_bindings()
    
    def _setup_component(self):
        """Setup the file types component"""
        # Main container
        container = ttk.Frame(self.frame)
        container.pack(fill=tk.X)
        
        # File types grid
        types_frame = ttk.Frame(container)
        types_frame.pack(fill=tk.X, pady=(0, ModernStyles.get_spacing('md')))
        
        # Configure grid for responsive layout
        for i in range(4):
            types_frame.columnconfigure(i, weight=1)
        
        # Create checkboxes for each file type
        for i, (key, data) in enumerate(self.file_types.items()):
            self._create_file_type_checkbox(types_frame, key, data, i)
        
        # Quick actions
        self._create_quick_actions(container)
        
        # Extensions info (expandable)
        self._create_extensions_info(container)
    
    def _create_file_type_checkbox(self, parent, key: str, data: dict, column: int):
        """Create a checkbox for a file type"""
        # Container for each checkbox
        check_frame = ttk.Frame(parent)
        check_frame.grid(row=0, column=column, sticky=(tk.W, tk.E), 
                        padx=ModernStyles.get_spacing('sm'))
        
        # Checkbox with icon and label
        checkbox = ttk.Checkbutton(
            check_frame,
            text=f"{data['icon']} {data['label']}",
            variable=data['var'],
            style='Modern.TCheckbutton'
        )
        checkbox.pack(anchor=tk.W)
        
        # Extensions hint
        extensions = ', '.join(self.extensions_info[key][:3])
        if len(self.extensions_info[key]) > 3:
            extensions += f" (+{len(self.extensions_info[key]) - 3} más)"
        
        hint_label = ttk.Label(check_frame, text=extensions,
                              style='Caption.TLabel')
        hint_label.pack(anchor=tk.W, pady=(ModernStyles.get_spacing('xs'), 0))
    
    def _create_quick_actions(self, parent):
        """Create quick action buttons"""
        actions_frame = ttk.Frame(parent)
        actions_frame.pack(fill=tk.X, pady=(0, ModernStyles.get_spacing('md')))
        
        # Quick action buttons
        ttk.Button(actions_frame, text="✅ Seleccionar todo",
                  style='Secondary.TButton',
                  command=self._select_all).pack(side=tk.LEFT, 
                                               padx=(0, ModernStyles.get_spacing('sm')))
        
        ttk.Button(actions_frame, text="❌ Deseleccionar todo",
                  style='Secondary.TButton',
                  command=self._deselect_all).pack(side=tk.LEFT,
                                                 padx=(0, ModernStyles.get_spacing('sm')))
        
        ttk.Button(actions_frame, text="🎬 Solo videos",
                  style='Secondary.TButton',
                  command=self._videos_only).pack(side=tk.LEFT,
                                                 padx=(0, ModernStyles.get_spacing('sm')))
        
        ttk.Button(actions_frame, text="📝 Videos + Subtítulos",
                  style='Secondary.TButton',
                  command=self._videos_and_subtitles).pack(side=tk.LEFT)
    
    def _create_extensions_info(self, parent):
        """Create expandable extensions info"""
        info_frame = ttk.Frame(parent)
        info_frame.pack(fill=tk.X)
        
        # Toggle button for extensions
        self.extensions_visible = False
        self.extensions_toggle_btn = ttk.Button(info_frame, text="ℹ️ Ver extensiones soportadas",
                                               style='Secondary.TButton',
                                               command=self._toggle_extensions_info)
        self.extensions_toggle_btn.pack(anchor=tk.W)
        
        # Extensions content (initially hidden)
        self.extensions_content = ttk.Frame(info_frame)
        
        for file_type, extensions in self.extensions_info.items():
            type_data = self.file_types[file_type]
            
            type_frame = ttk.Frame(self.extensions_content)
            type_frame.pack(fill=tk.X, pady=(ModernStyles.get_spacing('sm'), 0))
            
            # Type label
            type_label = ttk.Label(type_frame, 
                                  text=f"{type_data['icon']} {type_data['label']}:",
                                  style='Body.TLabel')
            type_label.pack(anchor=tk.W)
            
            # Extensions
            ext_text = ', '.join(extensions)
            ext_label = ttk.Label(type_frame, text=ext_text,
                                 style='Caption.TLabel')
            ext_label.pack(anchor=tk.W, padx=(ModernStyles.get_spacing('lg'), 0))
    
    def _setup_bindings(self):
        """Setup event bindings"""
        # Bind selection change events
        for key, data in self.file_types.items():
            data['var'].trace('w', self._on_selection_changed_internal)
    
    def _on_selection_changed_internal(self, *args):
        """Handle internal selection changes"""
        if self.on_selection_changed:
            self.on_selection_changed(self.get_selected_types())
    
    def _select_all(self):
        """Select all file types"""
        for data in self.file_types.values():
            data['var'].set(True)
    
    def _deselect_all(self):
        """Deselect all file types"""
        for data in self.file_types.values():
            data['var'].set(False)
    
    def _videos_only(self):
        """Select only videos"""
        self._deselect_all()
        self.file_types['videos']['var'].set(True)
    
    def _videos_and_subtitles(self):
        """Select videos and subtitles"""
        self._deselect_all()
        self.file_types['videos']['var'].set(True)
        self.file_types['subtitles']['var'].set(True)
    
    def _toggle_extensions_info(self):
        """Toggle extensions info visibility"""
        if self.extensions_visible:
            self.extensions_content.pack_forget()
            self.extensions_toggle_btn.config(text="ℹ️ Ver extensiones soportadas")
            self.extensions_visible = False
        else:
            self.extensions_content.pack(fill=tk.X, pady=(ModernStyles.get_spacing('sm'), 0))
            self.extensions_toggle_btn.config(text="🔼 Ocultar extensiones")
            self.extensions_visible = True
    
    def get_selected_types(self) -> Dict[str, bool]:
        """Get selected file types"""
        return {
            key: data['var'].get()
            for key, data in self.file_types.items()
        }
    
    def set_selected_types(self, selections: Dict[str, bool]):
        """Set selected file types"""
        for key, selected in selections.items():
            if key in self.file_types:
                self.file_types[key]['var'].set(selected)
    
    def get_selection_summary(self) -> str:
        """Get a summary of selected types"""
        selected = [
            self.file_types[key]['label']
            for key, data in self.file_types.items()
            if data['var'].get()
        ]
        
        if not selected:
            return "Ningún tipo seleccionado"
        elif len(selected) == 1:
            return f"Solo {selected[0].lower()}"
        elif len(selected) == len(self.file_types):
            return "Todos los tipos"
        else:
            return f"{', '.join(selected[:-1])} y {selected[-1]}"
    
    def has_selection(self) -> bool:
        """Check if at least one type is selected"""
        return any(data['var'].get() for data in self.file_types.values())
    
    def pack(self, **kwargs):
        """Pack the component"""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the component"""
        self.frame.grid(**kwargs)
    
    def place(self, **kwargs):
        """Place the component"""
        self.frame.place(**kwargs) 