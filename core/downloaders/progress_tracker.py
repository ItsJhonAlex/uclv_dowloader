"""
Progress Tracker for download operations
"""

import time
from typing import List, Callable


class DownloadProgress:
    """Class to track download progress and statistics"""
    
    def __init__(self):
        self.total_files = 0
        self.completed_files = 0
        self.failed_files = 0
        self.current_file = ""
        self.current_progress = 0
        self.total_bytes = 0
        self.downloaded_bytes = 0
        self.start_time = None
        self.callbacks: List[Callable] = []
    
    def add_callback(self, callback: Callable):
        """Add progress callback function"""
        self.callbacks.append(callback)
    
    def update(self, **kwargs):
        """Update progress data and notify callbacks"""
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        for callback in self.callbacks:
            callback(self)
    
    def get_progress_percentage(self) -> float:
        """Get overall progress percentage"""
        if self.total_files == 0:
            return 0.0
        return (self.completed_files / self.total_files) * 100
    
    def get_current_file_percentage(self) -> float:
        """Get current file download percentage"""
        if self.total_bytes == 0:
            return 0.0
        return (self.downloaded_bytes / self.total_bytes) * 100
    
    def get_elapsed_time(self) -> float:
        """Get elapsed time since start"""
        if self.start_time is None:
            return 0.0
        return time.time() - self.start_time
    
    def get_estimated_time_remaining(self) -> float:
        """Estimate remaining time based on current progress"""
        if self.total_files == 0 or self.completed_files == 0:
            return 0.0
        
        elapsed = self.get_elapsed_time()
        progress = self.get_progress_percentage() / 100.0
        
        if progress <= 0:
            return 0.0
        
        estimated_total = elapsed / progress
        return estimated_total - elapsed
    
    def reset(self):
        """Reset progress tracking"""
        self.total_files = 0
        self.completed_files = 0
        self.failed_files = 0
        self.current_file = ""
        self.current_progress = 0
        self.total_bytes = 0
        self.downloaded_bytes = 0
        self.start_time = time.time() 