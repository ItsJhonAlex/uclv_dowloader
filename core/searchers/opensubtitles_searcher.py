"""
OpenSubtitles.org searcher implementation
"""

from typing import List, Dict, Any
from .base_searcher import BaseSubtitleSearcher


class OpenSubtitlesSearcher(BaseSubtitleSearcher):
    """Simple OpenSubtitles searcher without API requirements"""
    
    def get_source_name(self) -> str:
        return "OpenSubtitles.org"
    
    def search_subtitles(self, video_name: str, language: str = 'spanish') -> List[Dict[str, Any]]:
        """Mock search for OpenSubtitles (demo implementation)"""
        clean_name = self.clean_video_name(video_name)
        
        if not clean_name:
            return []
        
        # For demo purposes, return mock results
        results = [
            {
                'title': f"{clean_name} - Spanish",
                'source': 'OpenSubtitles.org',
                'language': 'Spanish',
                'downloads': '1250',
                'rating': '8.5/10',
                'confidence': 90,
                'download_url': f'https://example.com/subtitle1.srt',
                'format': 'srt'
            },
            {
                'title': f"{clean_name} - Spanish (Alternate)",
                'source': 'OpenSubtitles.org',
                'language': 'Spanish',
                'downloads': '892',
                'rating': '7.8/10',
                'confidence': 75,
                'download_url': f'https://example.com/subtitle2.srt',
                'format': 'srt'
            }
        ]
        
        return results 