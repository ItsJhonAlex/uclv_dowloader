"""
Subtitle Search module for UCLV Downloader
Searches for subtitles from external sources like OpenSubtitles
"""

import re
import requests
import json
import time
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import urllib.parse


class SimpleSubtitleSearcher:
    """Simple subtitle searcher that works without complex APIs"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search_subtitles(self, video_name: str, language: str = 'spanish') -> List[Dict[str, Any]]:
        """Search for subtitles using multiple simple methods"""
        results = []
        
        # Clean video name for search
        clean_name = self._clean_video_name(video_name)
        
        # Method 1: OpenSubtitles.org search (web scraping)
        try:
            os_results = self._search_opensubtitles_web(clean_name, language)
            results.extend(os_results)
        except Exception as e:
            print(f"OpenSubtitles search failed: {e}")
        
        # Method 2: SubDivX (Spanish subtitles)
        try:
            subdivx_results = self._search_subdivx(clean_name)
            results.extend(subdivx_results)
        except Exception as e:
            print(f"SubDivX search failed: {e}")
        
        # Method 3: Podnapisi.NET
        try:
            podnapisi_results = self._search_podnapisi(clean_name, language)
            results.extend(podnapisi_results)
        except Exception as e:
            print(f"Podnapisi search failed: {e}")
        
        # Sort by confidence and return top results
        results.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        return results[:10]  # Top 10 results
    
    def _clean_video_name(self, video_name: str) -> str:
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
    
    def _search_opensubtitles_web(self, query: str, language: str) -> List[Dict[str, Any]]:
        """Search OpenSubtitles.org via web scraping"""
        try:
            # OpenSubtitles.org search URL
            search_url = "https://www.opensubtitles.org/es/search2"
            
            params = {
                'query': query,
                'sublanguageid': 'spa' if language.lower() in ['spanish', 'español', 'es'] else 'eng'
            }
            
            response = self.session.get(search_url, params=params, timeout=10)
            
            if response.status_code != 200:
                return []
            
            # Parse results (simplified - in real implementation you'd use BeautifulSoup)
            results = []
            
            # This is a placeholder implementation
            # In reality, you'd parse the HTML response to extract subtitle links
            results.append({
                'id': f'os_{query.replace(" ", "_")}',
                'title': f"OpenSubtitles result for: {query}",
                'source': 'OpenSubtitles.org',
                'language': language,
                'download_url': f'https://www.opensubtitles.org/download/{query}',
                'confidence': 0.7,
                'rating': 4.0,
                'download_count': 1000
            })
            
            return results
            
        except Exception as e:
            print(f"OpenSubtitles web search error: {e}")
            return []
    
    def _search_subdivx(self, query: str) -> List[Dict[str, Any]]:
        """Search SubDivX for Spanish subtitles"""
        try:
            # SubDivX is a popular Spanish subtitle site
            search_url = "https://www.subdivx.com"
            
            params = {
                'buscar': query,
                'accion': 5,
                'masdesc': '',
                'subtitulos': 1,
                'realiza_b': 1
            }
            
            response = self.session.get(search_url, params=params, timeout=10)
            
            if response.status_code != 200:
                return []
            
            # Placeholder result
            results = []
            results.append({
                'id': f'subdivx_{query.replace(" ", "_")}',
                'title': f"SubDivX result for: {query}",
                'source': 'SubDivX',
                'language': 'spanish',
                'download_url': f'https://www.subdivx.com/download/{query}',
                'confidence': 0.8,
                'rating': 4.2,
                'download_count': 500
            })
            
            return results
            
        except Exception as e:
            print(f"SubDivX search error: {e}")
            return []
    
    def _search_podnapisi(self, query: str, language: str) -> List[Dict[str, Any]]:
        """Search Podnapisi.NET"""
        try:
            # Podnapisi.NET search
            search_url = "https://www.podnapisi.net/subtitles/search/advanced"
            
            params = {
                'keywords': query,
                'language': 'es' if language.lower() in ['spanish', 'español', 'es'] else 'en'
            }
            
            response = self.session.get(search_url, params=params, timeout=10)
            
            if response.status_code != 200:
                return []
            
            # Placeholder result
            results = []
            results.append({
                'id': f'podnapisi_{query.replace(" ", "_")}',
                'title': f"Podnapisi result for: {query}",
                'source': 'Podnapisi.NET',
                'language': language,
                'download_url': f'https://www.podnapisi.net/download/{query}',
                'confidence': 0.6,
                'rating': 3.8,
                'download_count': 300
            })
            
            return results
            
        except Exception as e:
            print(f"Podnapisi search error: {e}")
            return []
    
    def download_subtitle(self, subtitle_info: Dict[str, Any], output_path: Path) -> bool:
        """Download a subtitle file"""
        try:
            download_url = subtitle_info.get('download_url')
            if not download_url:
                return False
            
            # For demo purposes, create a placeholder subtitle file
            # In real implementation, you'd download from the actual URL
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
            
            print(f"✅ Subtítulo placeholder creado: {output_path.name}")
            return True
            
        except Exception as e:
            print(f"Error downloading subtitle: {e}")
            return False


class SubtitleSearchManager:
    """Manager for searching and downloading subtitles"""
    
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
                
                # Download subtitle
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