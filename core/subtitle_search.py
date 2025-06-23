"""
Subtitle Search module for UCLV Downloader - Refactored to use searcher architecture
"""

import time
from typing import List, Dict, Any, Tuple
from pathlib import Path
from .searchers import SimpleSubtitleSearcher


class SubtitleSearchManager:
    """Manager for searching and downloading subtitles using the new searcher architecture"""
    
    def __init__(self):
        self.searcher = SimpleSubtitleSearcher()
    
    def search_subtitles_for_videos(self, videos_without_subtitles: List[Tuple[str, str, str]], 
                                   language: str = 'spanish') -> Dict[str, List[Dict[str, Any]]]:
        """
        Search subtitles for multiple videos
        Returns: Dict mapping video filename to list of subtitle options
        """
        results = {}
        
        for video_filename, video_url, video_type in videos_without_subtitles:
            if video_type != 'video':
                continue
                
            print(f"🔍 Buscando subtítulos para: {video_filename}")
            
            try:
                video_results = self.searcher.search_subtitles(video_filename, language)
                results[video_filename] = video_results
                
                if video_results:
                    print(f"✅ Encontrados {len(video_results)} resultados para {video_filename}")
                else:
                    print(f"❌ No se encontraron subtítulos para {video_filename}")
                
                # Rate limiting
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Error buscando subtítulos para {video_filename}: {e}")
                results[video_filename] = []
        
        return results
    
    def download_selected_subtitles(self, selected_subtitles: Dict[str, Dict[str, Any]], 
                                   output_directory: Path) -> Dict[str, bool]:
        """
        Download selected subtitles
        Returns: Dict mapping video filename to download success
        """
        results = {}
        
        for video_filename, subtitle_info in selected_subtitles.items():
            try:
                # Generate subtitle filename
                video_stem = Path(video_filename).stem
                subtitle_filename = f"{video_stem}.srt"
                subtitle_path = output_directory / subtitle_filename
                
                # Download subtitle using searcher
                success = self.searcher.download_subtitle(subtitle_info, subtitle_path)
                results[video_filename] = success
                
                if success:
                    print(f"✅ Subtítulo descargado: {subtitle_filename}")
                else:
                    print(f"❌ Error descargando subtítulo para: {video_filename}")
                    
            except Exception as e:
                print(f"❌ Error descargando subtítulo para {video_filename}: {e}")
                results[video_filename] = False
        
        return results


# Backward compatibility alias
SimpleSubtitleSearcher = SimpleSubtitleSearcher 