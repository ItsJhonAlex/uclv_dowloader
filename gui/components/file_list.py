"""
File List component for UCLV Downloader GUI with Individual File Selection
"""

from typing import List, Tuple, Callable, Optional
from .widgets import FileListModel, FileListView


class FileListComponent:
    """Modern file list component using MVC architecture"""
    
    def __init__(self, parent, on_selection_changed: Optional[Callable] = None):
        self.parent = parent
        self.on_selection_changed = on_selection_changed
        
        # Initialize model and view
        self.model = FileListModel()
        self.view = FileListView(parent)
        
        # Store reference to frame for compatibility
        self.frame = self.view.frame
        
        self._setup_component()
    
    def _setup_component(self):
        """Setup the file list component with model-view binding"""
        # Add control buttons to view
        self.view.add_control_button("✅ Seleccionar todos", self._select_all)
        self.view.add_control_button("❌ Deseleccionar todos", self._deselect_all)
        self.view.add_control_button("🔄 Invertir selección", self._invert_selection)
        self.view.add_control_button("🎬 Solo videos", self._select_videos_only)
        self.view.add_control_button("📝 Solo subtítulos", self._select_subtitles_only)
        
        # Setup view callbacks
        self.view.set_tree_click_callback(self._on_tree_click)
        
        # Setup model callbacks for selection changes
        self._setup_model_callbacks()
    
    def _setup_model_callbacks(self):
        """Setup callbacks for model changes"""
        # Add selection change callbacks to all file variables
        for i in range(len(self.model.files_data)):
            if i in self.model.file_vars:
                self.model.add_selection_callback(i, lambda *args, idx=i: self._on_selection_changed_internal(idx))
    
    def set_files(self, files: List[Tuple[str, str, str]]):
        """Set files to display with individual selection"""
        self.model.set_files(files)
        self._setup_model_callbacks()
        self._update_display()
        self._update_selection_stats()
    
    def _update_display(self):
        """Update view display from model"""
        # Update tree display
        self.view.update_tree_display(self.model.files_data, self.model.file_vars)
        
        # Update stats display
        stats = self.model.get_statistics()
        if stats['total_count'] == 0:
            self.view.update_stats_display("No hay archivos cargados")
        else:
            # Generate stats text
            icons = {'video': '🎬', 'subtitle': '📝', 'image': '🖼️', 'info': '📄', 'other': '📄'}
            type_summary = []
            for file_type, count in stats['total'].items():
                if count > 0:
                    icon = icons.get(file_type, '📄')
                    type_summary.append(f"{icon} {count}")
            
            self.view.update_stats_display(f"📊 {stats['total_count']} archivos encontrados: {' | '.join(type_summary)}")
    
    def _on_tree_click(self, item, column, double_click=False):
        """Handle tree click events"""
        if not item:
            return
            
        # Get file index from tags
        tags = self.view.tree.item(item, 'tags')
        if not tags:
            return
            
        file_index = int(tags[0])
        
        # Toggle selection on checkbox column click or double-click
        if column == '#2' or double_click:  # Checkbox column or double-click
            current_value = self.model.file_vars[file_index].get()
            self.model.file_vars[file_index].set(not current_value)
    
    def _on_selection_changed_internal(self, file_index: int):
        """Handle individual file selection change"""
        # Update view
        selected = self.model.file_vars[file_index].get()
        self.view.update_item_selection(file_index, selected)
        
        # Update selection stats
        self._update_selection_stats()
        
        # Notify parent component
        if self.on_selection_changed:
            self.on_selection_changed(self.get_selected_files())
    
    def _update_selection_stats(self):
        """Update selection statistics in view"""
        selected_count = self.model.get_selected_count()
        total_count = self.model.get_total_count()
        self.view.update_selection_stats(selected_count, total_count)
    
    def _select_all(self):
        """Select all files"""
        self.model.select_all()
    
    def _deselect_all(self):
        """Deselect all files"""
        self.model.deselect_all()
    
    def _invert_selection(self):
        """Invert current selection"""
        self.model.invert_selection()
    
    def _select_videos_only(self):
        """Select only video files"""
        self.model.select_by_type('video')
    
    def _select_subtitles_only(self):
        """Select only subtitle files"""
        self.model.select_by_type('subtitle')
    
    def get_selected_files(self) -> List[Tuple[str, str, str]]:
        """Get list of selected files"""
        return self.model.get_selected_files()
    
    def get_selected_count(self) -> int:
        """Get count of selected files"""
        return self.model.get_selected_count()
    
    def has_selection(self) -> bool:
        """Check if any files are selected"""
        return self.model.has_selection()
    
    def get_file_count(self) -> int:
        """Get total file count"""
        return self.model.get_total_count()
    
    def set_file_selection(self, index: int, selected: bool):
        """Set selection state for a specific file"""
        self.model.set_file_selection(index, selected)
    
    def clear_files(self):
        """Clear all files"""
        self.model.clear_files()
        self._update_display()
        self._update_selection_stats()
    
    def pack(self, **kwargs):
        """Pack the component"""
        self.view.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the component"""
        self.view.grid(**kwargs)
    
    def place(self, **kwargs):
        """Place the component"""
        self.view.place(**kwargs) 