"""
Main downloader class for UCLV Downloader - Refactored version
"""

import requests
from pathlib import Path
from typing import List, Tuple, Optional, Callable, Dict, Any
from bs4 import BeautifulSoup

from ..utils import URLUtils, FileUtils
from .batch_downloader import BatchDownloader
from .file_downloader import FileDownloader


class UCLVDownloader:
    """Main downloader class with improved modularity using components"""
    
    def __init__(self, download_delay: float = 0.5, max_retries: int = 3):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Initialize components
        self.batch_downloader = BatchDownloader(download_delay, max_retries)
        self.file_downloader = FileDownloader(self.session, max_retries)
        
        # Filtros configurables
        self.download_videos = True
        self.download_subtitles = True
        self.download_images = False
        self.download_info = False
    
    def configure_downloads(self, videos=True, subtitles=True, images=False, info=False):
        """Configure which file types to download"""
        self.download_videos = videos
        self.download_subtitles = subtitles
        self.download_images = images
        self.download_info = info
    
    def get_file_list(self, url: str) -> List[Tuple[str, str, str]]:
        """
        Get list of files from the webpage
        Returns: List of (filename, full_url, file_type)
        """
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Error accessing URL: {e}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        files = []
        
        # Buscar todos los enlaces de archivos
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if not href or href.startswith('?') or href == '../':
                continue
            
            # Obtener información del archivo
            filename = FileUtils.clean_filename(href)
            file_type = FileUtils.get_file_type(filename)
            
            # Aplicar filtros
            if not self._should_download_file_type(file_type):
                continue
            
            # Construir URL completa
            full_url = URLUtils.build_full_url(url, href)
            files.append((filename, full_url, file_type))
        
        return files
    
    def _should_download_file_type(self, file_type: str) -> bool:
        """Check if file type should be downloaded based on configuration"""
        return {
            "video": self.download_videos,
            "subtitle": self.download_subtitles,
            "image": self.download_images,
            "info": self.download_info
        }.get(file_type, False)
    
    def get_file_info(self, url: str) -> Dict[str, Any]:
        """Get file information without downloading"""
        return self.file_downloader.get_file_info(url)
    
    def download_from_url(self, url: str, download_path: Optional[Path] = None,
                         progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Main download function
        Returns: Dictionary with download statistics
        """
        if not URLUtils.is_valid_url(url):
            raise ValueError("Invalid URL provided")
        
        # Get file list
        files = self.get_file_list(url)
        if not files:
            return {'success': False, 'message': 'No files found to download'}
        
        return self.download_selected_files(files, url, download_path, progress_callback)
    
    def download_selected_files(self, selected_files: List[Tuple[str, str, str]], 
                               url: str, download_path: Optional[Path] = None,
                               progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Download specific selected files using batch downloader
        """
        if not selected_files:
            return {'success': False, 'message': 'No files selected for download'}
        
        # Create download directory
        if download_path is None:
            folder_name = URLUtils.extract_folder_name(url)
            download_path = Path("descarga") / folder_name
        elif isinstance(download_path, str):
            download_path = Path(download_path)
        
        # Use batch downloader for the actual downloading
        result = self.batch_downloader.download_files(
            selected_files, download_path, progress_callback
        )
        
        # Add file statistics
        result['file_stats'] = self.batch_downloader.get_file_statistics(selected_files)
        
        return result
    
    def add_progress_callback(self, callback: Callable):
        """Add progress callback to batch downloader"""
        self.batch_downloader.add_progress_callback(callback)
    
    @property
    def progress(self):
        """Get progress tracker from batch downloader"""
        return self.batch_downloader.progress 