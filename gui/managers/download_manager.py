"""
Download Manager - Handles all download-related functionality
"""

import threading
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional
from tkinter import messagebox

from core import UCLVDownloader


class DownloadManager:
    """Manages download operations and tracking"""
    
    def __init__(self, gui_interface):
        self.gui = gui_interface
        self.downloader = UCLVDownloader()
        self.download_thread: Optional[threading.Thread] = None
        self.is_downloading = False
        
        # Progress tracking
        self._current_file_index = 0
        self._total_files = 0
        self._completed_files = 0
    
    def configure_downloader(self, selected_types):
        """Configure downloader based on file type selections"""
        self.downloader.configure_downloads(
            videos=selected_types.get('videos', False),
            subtitles=selected_types.get('subtitles', False),
            images=selected_types.get('images', False),
            info=selected_types.get('info', False)
        )
    
    def get_file_list(self, url: str) -> List[Tuple[str, str, str]]:
        """Get file list from URL"""
        return self.downloader.get_file_list(url)
    
    def start_download(self, download_path: str, selected_files: List[Tuple[str, str, str]], 
                      external_subtitles: Dict[str, Dict[str, Any]] = None):
        """Start download process"""
        if self.is_downloading:
            return
        
        if external_subtitles is None:
            external_subtitles = {}
        
        # Start download in background thread
        self.is_downloading = True
        self.gui.ui_state.set_download_state(True)
        
        self.download_thread = threading.Thread(
            target=self._download_worker,
            args=(download_path, selected_files, external_subtitles),
            daemon=True
        )
        self.download_thread.start()
    
    def cancel_download(self):
        """Cancel ongoing download"""
        if not self.is_downloading:
            return
        
        # Ask for confirmation
        if messagebox.askyesno("Cancelar descarga", "¿Estás seguro de que quieres cancelar la descarga?"):
            self.is_downloading = False
            self.gui.ui_state.set_download_state(False)
            
            # Update progress
            self.gui.progress.set_status("❌ Descarga cancelada", 'cancelled')
            messagebox.showinfo("Cancelado", "Descarga cancelada por el usuario")
    
    def _download_worker(self, download_path: str, selected_files: List[Tuple[str, str, str]], 
                        external_subtitles: Dict[str, Dict[str, Any]]):
        """Background download worker with external subtitle support"""
        try:
            # Track progress across files
            self._current_file_index = 0
            total_items = len(selected_files) + len(external_subtitles)
            self._total_files = total_items
            self._completed_files = 0
            
            def progress_callback(downloaded, total, filename):
                # Calculate file progress percentage
                file_progress = (downloaded / total * 100) if total > 0 else 0
                
                # Update UI in main thread
                self.gui.root.after(0, lambda: self.gui.progress.set_progress(file_progress))
                self.gui.root.after(0, lambda: self.gui.progress.set_current_file(filename))
                self.gui.root.after(0, lambda: self.gui.progress.update_stats(
                    downloaded=self._completed_files, 
                    total=self._total_files
                ))
                self.gui.root.after(0, lambda: self.gui.progress.set_status(
                    f"Descargando archivo {self._completed_files + 1} de {self._total_files}: {filename}", 'downloading'))
            
            # Start download with selected files
            url = self.gui.url_input.get_url()
            result = self.downloader.download_selected_files(selected_files, url, download_path, progress_callback)
            
            # Download external subtitles if any were selected
            if external_subtitles:
                self.gui.root.after(0, lambda: self.gui.progress.set_status("Descargando subtítulos externos...", 'downloading'))
                
                from core.subtitle_search import SubtitleSearchManager
                search_manager = SubtitleSearchManager()
                
                subtitle_results = search_manager.download_selected_subtitles(
                    external_subtitles, Path(download_path)
                )
                
                # Add subtitle results to main result
                if not result:
                    result = {'completed': 0, 'failed': [], 'total': 0}
                
                subtitle_success = sum(1 for success in subtitle_results.values() if success)
                subtitle_failed = [f"Subtitle for {video}" for video, success in subtitle_results.items() if not success]
                
                result['completed'] += subtitle_success
                result['failed'].extend(subtitle_failed)
                result['total'] += len(external_subtitles)
            
            # Handle completion in main thread
            self.gui.root.after(0, lambda: self._download_completed(result))
            
        except Exception as e:
            # Handle error in main thread
            self.gui.root.after(0, lambda: self._download_error(str(e)))
    
    def _download_completed(self, result):
        """Handle download completion"""
        self.is_downloading = False
        self.gui.ui_state.set_download_state(False)
        
        # Update progress
        if result.get('success', False):
            self.gui.progress.animate_success()
        
        # Show completion message
        completed = result.get('completed', 0)
        failed_list = result.get('failed', [])
        failed_count = len(failed_list)
        
        if failed_count == 0:
            message = f"🎉 ¡Descarga completada exitosamente!\n\n✅ Archivos descargados: {completed}\n📂 Ubicación: {result.get('download_path', 'Desconocida')}"
            messagebox.showinfo("Descarga completada", message)
        else:
            failed_names = "\n".join([f"• {f}" for f in failed_list[:5]])  # Show first 5 failed files
            if len(failed_list) > 5:
                failed_names += f"\n... y {len(failed_list) - 5} más"
            
            message = f"⚠️ Descarga completada con errores\n\n✅ Descargados: {completed}\n❌ Fallidos: {failed_count}\n📂 Ubicación: {result.get('download_path', 'Desconocida')}\n\nArchivos que fallaron:\n{failed_names}"
            messagebox.showwarning("Descarga con errores", message)
    
    def _download_error(self, error_msg: str):
        """Handle download error"""
        self.is_downloading = False
        self.gui.ui_state.set_download_state(False)
        
        # Update progress
        self.gui.progress.show_error(error_msg)
        
        # Show error message
        messagebox.showerror("Error de descarga", f"Error durante la descarga:\n{error_msg}")
    
    def get_videos_without_subtitles(self, selected_files: List[Tuple[str, str, str]]) -> List[Tuple[str, str, str]]:
        """Get list of videos that don't have corresponding subtitle files"""
        videos = [f for f in selected_files if f[2] == 'video']
        subtitles = [f for f in selected_files if f[2] == 'subtitle']
        
        # Create a set of video names (without extension) that have subtitles
        subtitle_names = set()
        for subtitle_file, _, _ in subtitles:
            subtitle_stem = Path(subtitle_file).stem
            # Remove common subtitle suffixes like .es, .spa, .spanish
            subtitle_stem = subtitle_stem.replace('.es', '').replace('.spa', '').replace('.spanish', '')
            subtitle_names.add(subtitle_stem.lower())
        
        # Find videos without matching subtitles
        videos_without_subtitles = []
        for video_file, video_url, video_type in videos:
            video_stem = Path(video_file).stem.lower()
            if video_stem not in subtitle_names:
                videos_without_subtitles.append((video_file, video_url, video_type))
        
        return videos_without_subtitles 