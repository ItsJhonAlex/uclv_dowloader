"""
Base Searcher class for subtitle searching
"""

import re
import requests
from pathlib import Path
from typing import List, Dict, Any
from abc import ABC, abstractmethod


class BaseSubtitleSearcher(ABC):
    """Base class for subtitle searchers"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def clean_video_name(self, video_name: str) -> str:
        """Clean video name for better search results"""
        # Remove file extension
        name = Path(video_name).stem
        
        # Remove common patterns that hurt search
        patterns_to_remove = [
            r'\b\d{4}\b',  # Years
            r'\b[Ss]\d{2}[Ee]\d{2}\b',  # Season/Episode patterns like S01E01
            r'\bHD\b|\bBD\b|\bBDRip\b|\bDVDRip\b|\bWEBRip\b|\bHDTV\b',  # Quality indicators
            r'\b\d{3,4}p\b',  # Resolution like 720p, 1080p
            r'\b(x264|x265|H264|H265|HEVC)\b',  # Codecs
            r'\[.*?\]|\(.*?\)',  # Remove brackets and parentheses
            r'\b(PROPER|REPACK|EXTENDED|UNRATED|DIRECTORS|CUT)\b',  # Release info
        ]
        
        for pattern in patterns_to_remove:
            name = re.sub(pattern, '', name, flags=re.IGNORECASE)
        
        # Replace dots, underscores, and hyphens with spaces
        name = re.sub(r'[._-]', ' ', name)
        
        # Remove extra spaces and clean up
        name = ' '.join(name.split())
        
        return name.strip()
    
    @abstractmethod
    def search_subtitles(self, video_name: str, language: str = 'spanish') -> List[Dict[str, Any]]:
        """Search for subtitles for a given video"""
        pass
    
    @abstractmethod 
    def get_source_name(self) -> str:
        """Get the name of this subtitle source"""
        pass
    
    def download_subtitle(self, subtitle_info: Dict[str, Any], output_path: Path) -> bool:
        """Download a subtitle file (basic implementation)"""
        try:
            download_url = subtitle_info.get('download_url')
            if not download_url:
                return False
            
            # For demo purposes, create a placeholder subtitle file
            placeholder_content = f"""1
00:00:01,000 --> 00:00:04,000
Subtítulo descargado desde {subtitle_info.get('source', 'Unknown')}

2
00:00:05,000 --> 00:00:08,000
Para el video: {subtitle_info.get('title', 'Unknown')}

3
00:00:09,000 --> 00:00:12,000
Este es un subtítulo de demostración.
"""
            
            # Write placeholder subtitle
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(placeholder_content)
            
            return True
            
        except Exception as e:
            print(f"Error downloading subtitle: {e}")
            return False 