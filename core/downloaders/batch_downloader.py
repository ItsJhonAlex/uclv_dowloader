"""
Batch Downloader for multiple files
"""

import time
from pathlib import Path
from typing import List, Tuple, Optional, Callable, Dict, Any

from .file_downloader import FileDownloader
from .progress_tracker import DownloadProgress


class BatchDownloader:
    """Handles batch downloading of multiple files"""
    
    def __init__(self, download_delay: float = 0.5, max_retries: int = 3):
        self.download_delay = download_delay
        self.progress = DownloadProgress()
        self.file_downloader = FileDownloader(max_retries=max_retries)
    
    def download_files(self, selected_files: List[Tuple[str, str, str]], 
                      download_path: Path,
                      progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Download multiple files with progress tracking
        Args:
            selected_files: List of (filename, file_url, file_type) tuples
            download_path: Target download directory
            progress_callback: Progress callback function
        Returns: Dictionary with download statistics
        """
        if not selected_files:
            return {'success': False, 'message': 'No files selected for download'}
        
        # Setup progress tracking
        self.progress.reset()
        self.progress.update(total_files=len(selected_files))
        
        # Create download directory
        download_path.mkdir(parents=True, exist_ok=True)
        
        # Download files
        successful_downloads = 0
        failed_downloads = []
        
        try:
            for i, (filename, file_url, file_type) in enumerate(selected_files):
                self.progress.update(current_file=filename, current_progress=i)
                print(f"📥 Descargando ({i+1}/{len(selected_files)}): {filename}")
                
                # Enhanced progress callback for this specific file
                def file_progress_callback(downloaded, total, fname):
                    self.progress.update(
                        downloaded_bytes=downloaded,
                        total_bytes=total
                    )
                    if progress_callback:
                        progress_callback(downloaded, total, fname)
                
                try:
                    if self.file_downloader.download_file(filename, file_url, download_path, file_progress_callback):
                        successful_downloads += 1
                        self.progress.update(completed_files=successful_downloads)
                    else:
                        failed_downloads.append(filename)
                        self.progress.update(failed_files=len(failed_downloads))
                        
                except Exception as e:
                    error_msg = f"{filename}: {str(e)}"
                    failed_downloads.append(error_msg)
                    self.progress.update(failed_files=len(failed_downloads))
                    print(f"❌ Error descargando {filename}: {e}")
                
                # Delay between downloads
                if i < len(selected_files) - 1:
                    time.sleep(self.download_delay)
                    
        except KeyboardInterrupt:
            print("\n⚠️  Descarga interrumpida por el usuario")
            return {
                'success': False,
                'message': 'Download interrupted by user',
                'completed': successful_downloads,
                'failed': failed_downloads,
                'total': len(selected_files),
                'interrupted': True
            }
        
        # Return statistics
        success = len(failed_downloads) == 0
        message = 'Download completed successfully' if success else f'Download completed with {len(failed_downloads)} errors'
        
        print(f"\n🎉 ¡Descarga completada!")
        print(f"✅ Exitosos: {successful_downloads}")
        print(f"❌ Fallidos: {len(failed_downloads)}")
        
        return {
            'success': success,
            'message': message,
            'completed': successful_downloads,
            'failed': failed_downloads,
            'total': len(selected_files),
            'download_path': str(download_path.absolute()),
            'duration': self.progress.get_elapsed_time()
        }
    
    def get_file_statistics(self, files: List[Tuple[str, str, str]]) -> Dict[str, int]:
        """Get statistics about file types"""
        stats = {'video': 0, 'subtitle': 0, 'image': 0, 'info': 0, 'other': 0}
        
        for _, _, file_type in files:
            stats[file_type] = stats.get(file_type, 0) + 1
            
        return stats
    
    def add_progress_callback(self, callback: Callable):
        """Add progress callback to tracker"""
        self.progress.add_callback(callback) 