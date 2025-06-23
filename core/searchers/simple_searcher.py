"""
Simple Subtitle Searcher that aggregates multiple sources
"""

from typing import List, Dict, Any
from .base_searcher import BaseSubtitleSearcher
from .opensubtitles_searcher import OpenSubtitlesSearcher
from .subdivx_searcher import SubDivXSearcher  
from .podnapisi_searcher import PodnapisiSearcher


class SimpleSubtitleSearcher(BaseSubtitleSearcher):
    """Simple subtitle searcher that works without complex APIs"""
    
    def __init__(self):
        super().__init__()
        self.searchers = [
            OpenSubtitlesSearcher(),
            SubDivXSearcher(),
            PodnapisiSearcher()
        ]
    
    def get_source_name(self) -> str:
        return "Multiple Sources"
    
    def search_subtitles(self, video_name: str, language: str = 'spanish') -> List[Dict[str, Any]]:
        """Search for subtitles using multiple simple methods"""
        results = []
        
        # Clean video name for search
        clean_name = self.clean_video_name(video_name)
        
        # Search using all available searchers
        for searcher in self.searchers:
            try:
                searcher_results = searcher.search_subtitles(clean_name, language)
                results.extend(searcher_results)
            except Exception as e:
                print(f"{searcher.get_source_name()} search failed: {e}")
        
        # Sort by confidence and return top results
        results.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        return results[:10]  # Top 10 results 