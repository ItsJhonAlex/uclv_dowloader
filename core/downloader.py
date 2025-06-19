"""
Main downloader class for UCVL Downloader
"""

import time
from pathlib import Path
from typing import List, Tuple, Optional, Callable, Dict, Any
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from .utils import URLUtils, FileUtils


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


class UCVLDownloader:
    """Main downloader class with improved modularity and features"""
    
    def __init__(self, download_delay: float = 0.5, max_retries: int = 3):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        self.download_delay = download_delay
        self.max_retries = max_retries
        self.progress = DownloadProgress()
        
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
            response = self.session.get(url)
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
        if file_type == "video" and self.download_videos:
            return True
        elif file_type == "subtitle" and self.download_subtitles:
            return True
        elif file_type == "image" and self.download_images:
            return True
        elif file_type == "info" and self.download_info:
            return True
        return False
    
    def get_file_info(self, url: str) -> Dict[str, Any]:
        """Get file information without downloading"""
        try:
            response = self.session.head(url)
            response.raise_for_status()
            
            size = int(response.headers.get('content-length', 0))
            content_type = response.headers.get('content-type', 'unknown')
            
            return {
                'size': size,
                'size_formatted': FileUtils.format_file_size(size),
                'content_type': content_type
            }
        except requests.RequestException:
            return {'size': 0, 'size_formatted': '0 B', 'content_type': 'unknown'}
    
    def download_file(self, filename: str, url: str, download_path: Path, 
                     progress_callback: Optional[Callable] = None) -> bool:
        """Download a single file with retry logic and progress tracking"""
        file_path = download_path / filename
        
        # Check if file already exists
        if file_path.exists():
            return True
        
        for attempt in range(self.max_retries):
            try:
                return self._download_file_attempt(filename, url, file_path, progress_callback)
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise Exception(f"Failed to download {filename} after {self.max_retries} attempts: {e}")
                time.sleep(1)  # Wait before retry
        
        return False
    
    def _download_file_attempt(self, filename: str, url: str, file_path: Path,
                              progress_callback: Optional[Callable] = None) -> bool:
        """Single download attempt"""
        response = self.session.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        # Create progress bar for CLI or use callback for GUI
        if progress_callback:
            # GUI mode - use callback
            downloaded = 0
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                        progress_callback(downloaded, total_size, filename)
        else:
            # CLI mode - use tqdm
            with tqdm(
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                desc=filename[:50]
            ) as pbar:
                with open(file_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                            pbar.update(len(chunk))
        
        return True
    
    def download_from_url(self, url: str, download_path: Optional[Path] = None,
                         progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Main download function
        Returns: Dictionary with download statistics
        """
        if not URLUtils.is_valid_url(url):
            raise ValueError("Invalid URL provided")
        
        # Setup progress tracking
        self.progress.start_time = time.time()
        
        # Get file list
        files = self.get_file_list(url)
        if not files:
            return {'success': False, 'message': 'No files found to download'}
        
        # Create download directory
        if download_path is None:
            folder_name = URLUtils.extract_folder_name(url)
            download_path = Path("descarga") / folder_name
        
        download_path.mkdir(parents=True, exist_ok=True)
        
        # Update progress
        self.progress.update(total_files=len(files))
        
        # Group files by type for better organization
        file_stats = self._get_file_statistics(files)
        
        # Download files
        successful_downloads = 0
        failed_downloads = []
        
        try:
            for i, (filename, file_url, file_type) in enumerate(files):
                self.progress.update(current_file=filename, current_progress=i)
                
                try:
                    if self.download_file(filename, file_url, download_path, progress_callback):
                        successful_downloads += 1
                        self.progress.update(completed_files=successful_downloads)
                    else:
                        failed_downloads.append(filename)
                        self.progress.update(failed_files=len(failed_downloads))
                        
                except Exception as e:
                    failed_downloads.append(f"{filename}: {str(e)}")
                    self.progress.update(failed_files=len(failed_downloads))
                
                # Delay between downloads
                if i < len(files) - 1:
                    time.sleep(self.download_delay)
                    
        except KeyboardInterrupt:
            return {
                'success': False,
                'message': 'Download interrupted by user',
                'completed': successful_downloads,
                'failed': failed_downloads,
                'total': len(files)
            }
        
        # Return statistics
        return {
            'success': len(failed_downloads) == 0,
            'message': 'Download completed successfully' if len(failed_downloads) == 0 else 'Download completed with errors',
            'completed': successful_downloads,
            'failed': failed_downloads,
            'total': len(files),
            'download_path': str(download_path.absolute()),
            'file_stats': file_stats,
            'duration': time.time() - self.progress.start_time
        }
    
    def _get_file_statistics(self, files: List[Tuple[str, str, str]]) -> Dict[str, int]:
        """Get statistics about file types"""
        stats = {'video': 0, 'subtitle': 0, 'image': 0, 'info': 0, 'other': 0}
        
        for _, _, file_type in files:
            stats[file_type] = stats.get(file_type, 0) + 1
            
        return stats 