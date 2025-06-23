"""
Podnapisi.net searcher implementation
"""

from typing import List, Dict, Any
from .base_searcher import BaseSubtitleSearcher


class PodnapisiSearcher(BaseSubtitleSearcher):
    """Podnapisi.net subtitle searcher""" 
    
    def get_source_name(self) -> str:
        return "Podnapisi.net"
    
    def search_subtitles(self, video_name: str, language: str = 'spanish') -> List[Dict[str, Any]]:
        """Mock search for Podnapisi (demo implementation)"""
        clean_name = self.clean_video_name(video_name)
        
        if not clean_name:
            return []
        
        # For demo purposes, return mock results
        results = [
            {
                'title': f"{clean_name} - Spanish",
                'source': 'Podnapisi.net',
                'language': 'Spanish',
                'downloads': '658',
                'rating': '8.1/10',
                'confidence': 70,
                'download_url': f'https://example.com/pod1.srt',
                'format': 'srt'
            }
        ]
        
        return results 