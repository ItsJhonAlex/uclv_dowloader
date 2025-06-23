"""
Subtitle Search Manager - Business logic for subtitle searching
"""

import threading
import time
from typing import Dict, List, Any, Optional, Tuple, Callable


class SubtitleSearchManager:
    """Manages subtitle search operations and state"""
    
    def __init__(self):
        self.is_searching = False
        self.search_results = {}
        self.selected_subtitles = {}
        self.subtitle_vars = {}
        
    def start_search(self, videos_without_subtitles: List[Tuple[str, str, str]], 
                     language: str = 'spanish', 
                     status_callback: Optional[Callable] = None,
                     results_callback: Optional[Callable] = None,
                     error_callback: Optional[Callable] = None) -> bool:
        """Start subtitle search in background thread"""
        
        if self.is_searching:
            return False
        
        if not videos_without_subtitles:
            if error_callback:
                error_callback("No hay videos sin subtítulos para buscar.")
            return False
        
        self.is_searching = True
        
        def search_worker():
            try:
                # Import here to avoid circular imports
                from core.subtitle_search import SubtitleSearchManager as CoreManager
                
                search_manager = CoreManager()
                
                # Update status
                if status_callback:
                    status_callback("🔍 Buscando subtítulos en YouTube y OpenSubtitles...")
                
                # Search subtitles
                results = search_manager.search_subtitles_for_videos(
                    videos_without_subtitles, language=language
                )
                
                self.search_results = results
                
                # Update results
                if results_callback:
                    results_callback(results)
                
            except Exception as e:
                # Handle error
                if error_callback:
                    error_callback(str(e))
            finally:
                # Reset state
                self.is_searching = False
        
        # Start search in background thread
        search_thread = threading.Thread(target=search_worker, daemon=True)
        search_thread.start()
        
        return True
    
    def process_search_results(self, results: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Process and analyze search results"""
        videos_with_results = 0
        total_subtitles = 0
        
        for video_name, subtitle_options in results.items():
            if subtitle_options:
                videos_with_results += 1
                total_subtitles += len(subtitle_options)
        
        return {
            'videos_with_results': videos_with_results,
            'total_subtitles': total_subtitles,
            'has_results': videos_with_results > 0
        }
    
    def get_selected_subtitles(self) -> Dict[str, Dict[str, Any]]:
        """Get user-selected subtitles from UI variables"""
        selected = {}
        
        for video_name, var in self.subtitle_vars.items():
            if hasattr(var, 'get'):
                selection = var.get()
                
                if selection != "none" and selection.isdigit():
                    index = int(selection)
                    subtitle_options = self.search_results.get(video_name, [])
                    
                    if 0 <= index < len(subtitle_options):
                        selected[video_name] = subtitle_options[index]
        
        return selected
    
    def register_subtitle_variable(self, video_name: str, variable):
        """Register a UI variable for subtitle selection"""
        self.subtitle_vars[video_name] = variable
    
    def clear_results(self):
        """Clear search results and selections"""
        self.search_results = {}
        self.selected_subtitles = {}
        self.subtitle_vars = {}
    
    def get_videos_without_subtitles_info(self, videos: List[Tuple[str, str, str]]) -> Dict[str, Any]:
        """Get information about videos without subtitles"""
        video_count = len(videos)
        video_names = [video[0] for video in videos]
        
        return {
            'count': video_count,
            'names': video_names,
            'plural': video_count > 1
        } 