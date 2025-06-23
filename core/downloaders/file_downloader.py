"""
Single File Downloader component
"""

import time
import requests
from pathlib import Path
from typing import Optional, Callable, Dict, Any
from tqdm import tqdm

from ..utils import FileUtils


class FileDownloader:
    """Handles downloading of individual files with retry logic"""
    
    def __init__(self, session: Optional[requests.Session] = None, max_retries: int = 3):
        self.session = session or requests.Session()
        self.max_retries = max_retries
        
        # Set default headers if session doesn't have them
        if 'User-Agent' not in self.session.headers:
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
    
    def get_file_info(self, url: str) -> Dict[str, Any]:
        """Get file information without downloading"""
        try:
            response = self.session.head(url, timeout=10)
            response.raise_for_status()
            
            size = int(response.headers.get('content-length', 0))
            content_type = response.headers.get('content-type', 'unknown')
            
            return {
                'size': size,
                'size_formatted': FileUtils.format_file_size(size),
                'content_type': content_type,
                'url': url
            }
        except requests.RequestException:
            return {'size': 0, 'size_formatted': '0 B', 'content_type': 'unknown', 'url': url}
    
    def download_file(self, filename: str, url: str, download_path: Path, 
                     progress_callback: Optional[Callable] = None) -> bool:
        """Download a single file with retry logic and progress tracking"""
        file_path = download_path / filename
        
        # Check if file already exists
        if file_path.exists():
            print(f"✅ Archivo ya existe: {filename}")
            return True
        
        # Create directory if it doesn't exist
        download_path.mkdir(parents=True, exist_ok=True)
        
        for attempt in range(self.max_retries):
            try:
                return self._download_file_attempt(filename, url, file_path, progress_callback)
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    print(f"❌ Falló descarga después de {self.max_retries} intentos: {filename}")
                    raise Exception(f"Failed to download {filename} after {self.max_retries} attempts: {e}")
                else:
                    print(f"⚠️  Intento {attempt + 1} falló para {filename}, reintentando...")
                    time.sleep(1)  # Wait before retry
        
        return False
    
    def _download_file_attempt(self, filename: str, url: str, file_path: Path,
                              progress_callback: Optional[Callable] = None) -> bool:
        """Single download attempt"""
        response = self.session.get(url, stream=True, timeout=30)
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
                desc=filename[:50],
                leave=False
            ) as pbar:
                with open(file_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                            pbar.update(len(chunk))
        
        print(f"✅ Descargado: {filename}")
        return True 