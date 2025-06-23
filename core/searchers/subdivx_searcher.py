"""
SubDivX.com searcher implementation
"""

from typing import List, Dict, Any
from .base_searcher import BaseSubtitleSearcher


class SubDivXSearcher(BaseSubtitleSearcher):
    """SubDivX Spanish subtitle searcher"""
    
    def get_source_name(self) -> str:
        return "SubDivX.com"
    
    def search_subtitles(self, video_name: str, language: str = 'spanish') -> List[Dict[str, Any]]:
        """Mock search for SubDivX (demo implementation)"""
        clean_name = self.clean_video_name(video_name)
        
        if not clean_name or language != 'spanish':
            return []
        
        # For demo purposes, return mock results
        results = [
            {
                'title': f"{clean_name} - Español Latino",
                'source': 'SubDivX.com',
                'language': 'Spanish (Latin)',
                'downloads': '2100',
                'rating': '9.2/10',
                'confidence': 85,
                'download_url': f'https://example.com/subdl1.srt',
                'format': 'srt'
            }
        ]
        
        return results