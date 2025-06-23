"""
File List Model - Data management for file list component
"""

import tkinter as tk
from typing import List, Tuple, Dict, Any, Optional


class FileListModel:
    """Data model for file list with selection management"""
    
    def __init__(self):
        # Data storage
        self.files_data = []  # List of (filename, file_url, file_type)
        self.file_vars = {}   # Dict of {index: BooleanVar} for checkboxes
        self.file_info = {}   # Dict of {index: file_info} for additional data
        
    def set_files(self, files: List[Tuple[str, str, str]]):
        """Set files to display with individual selection"""
        self.files_data = files
        self.file_vars = {}
        self.file_info = {}
        
        # Create BooleanVar for each file (all selected by default)
        for i in range(len(files)):
            var = tk.BooleanVar(value=True)
            self.file_vars[i] = var
            
        return self.files_data
    
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
    
    def get_total_count(self) -> int:
        """Get total file count"""
        return len(self.files_data)
    
    def has_selection(self) -> bool:
        """Check if any files are selected"""
        return self.get_selected_count() > 0
    
    def set_file_selection(self, index: int, selected: bool):
        """Set selection state for a specific file"""
        if index in self.file_vars:
            self.file_vars[index].set(selected)
    
    def select_all(self):
        """Select all files"""
        for var in self.file_vars.values():
            var.set(True)
    
    def deselect_all(self):
        """Deselect all files"""
        for var in self.file_vars.values():
            var.set(False)
    
    def invert_selection(self):
        """Invert current selection"""
        for var in self.file_vars.values():
            var.set(not var.get())
    
    def select_by_type(self, file_type: str):
        """Select only files of specific type"""
        for i, (_, _, ftype) in enumerate(self.files_data):
            self.file_vars[i].set(ftype == file_type)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get file statistics"""
        stats = {'video': 0, 'subtitle': 0, 'image': 0, 'info': 0, 'other': 0}
        selected_stats = {'video': 0, 'subtitle': 0, 'image': 0, 'info': 0, 'other': 0}
        
        for i, (_, _, file_type) in enumerate(self.files_data):
            stats[file_type] = stats.get(file_type, 0) + 1
            
            if self.file_vars.get(i, tk.BooleanVar()).get():
                selected_stats[file_type] = selected_stats.get(file_type, 0) + 1
        
        return {
            'total': stats,
            'selected': selected_stats,
            'total_count': sum(stats.values()),
            'selected_count': sum(selected_stats.values())
        }
    
    def clear_files(self):
        """Clear all files"""
        self.files_data = []
        self.file_vars = {}
        self.file_info = {}
    
    def add_selection_callback(self, index: int, callback):
        """Add callback for when a file selection changes"""
        if index in self.file_vars:
            self.file_vars[index].trace('w', callback) 