"""
Event Manager - Handles all GUI event bindings and callbacks
"""

from typing import List, Tuple, Dict, Any
from tkinter import messagebox

from core import URLUtils


class EventManager:
    """Manages GUI events and callbacks"""
    
    def __init__(self, gui_interface):
        self.gui = gui_interface
    
    def setup_bindings(self):
        """Setup event bindings"""
        # Window close event
        self.gui.root.protocol("WM_DELETE_WINDOW", self._on_window_closing)
        
        # Keyboard shortcuts
        self.gui.root.bind('<Control-o>', lambda e: self.gui.url_input.url_entry.focus())
        self.gui.root.bind('<Control-d>', lambda e: self._handle_download_shortcut())
        self.gui.root.bind('<F5>', lambda e: self._refresh_file_list())
        self.gui.root.bind('<Escape>', lambda e: self._handle_escape_key())
    
    def _handle_download_shortcut(self):
        """Handle Ctrl+D shortcut for download"""
        if not self.gui.download_manager.is_downloading:
            download_path = self.gui.download_controls.get_download_path()
            self.on_download_started(download_path)
    
    def _handle_escape_key(self):
        """Handle Escape key - cancel download if active"""
        if self.gui.download_manager.is_downloading:
            self.on_download_cancelled()
    
    def on_url_analysis(self, url: str):
        """Handle URL analysis completion"""
        try:
            # Configure downloader based on file type selections
            selected_types = self.gui.file_types.get_selected_types()
            self.gui.download_manager.configure_downloader(selected_types)
            
            # Get file list
            files = self.gui.download_manager.get_file_list(url)
            
            # Update file list component
            self.gui.file_list.set_files(files)
            
            # Enable download if files found
            if files:
                self.gui.download_controls.enable_download(True)
                self.gui.url_input.set_status(f"✅ Encontrados {len(files)} archivos", 'success')
            else:
                self.gui.download_controls.enable_download(False)
                self.gui.url_input.set_status("⚠️ No se encontraron archivos del tipo seleccionado", 'warning')
            
        except Exception as e:
            # Handle analysis error
            self.gui.file_list.clear_files()
            self.gui.download_controls.enable_download(False)
            self.gui.url_input.set_status(f"❌ Error: {str(e)}", 'error')
            messagebox.showerror("Error de análisis", f"Error al analizar URL:\n{e}")
    
    def on_file_type_changed(self, selected_types):
        """Handle file type selection changes"""
        # Re-analyze if URL is present
        url = self.gui.url_input.get_url()
        if url and URLUtils.is_valid_url(url):
            # Trigger re-analysis with new file types
            self.on_url_analysis(url)
    
    def on_file_selection_changed(self, selected_files):
        """Handle individual file selection changes"""
        # Update download button state based on selection
        has_selection = len(selected_files) > 0
        self.gui.download_controls.enable_download(has_selection)
        
        # Check for videos without subtitles
        self._check_for_videos_without_subtitles(selected_files)
        
        # Update status
        if len(selected_files) == 0:
            self.gui.url_input.set_status("⚠️ Selecciona al menos un archivo para descargar", 'warning')
        else:
            self.gui.url_input.set_status(f"✅ {len(selected_files)} archivos seleccionados para descarga", 'success')
    
    def on_download_started(self, download_path: str):
        """Handle download start"""
        if self.gui.download_manager.is_downloading:
            return
        
        # Validate we have files to download
        if self.gui.file_list.get_file_count() == 0:
            messagebox.showwarning("Sin archivos", "No hay archivos para descargar. Analiza una URL primero.")
            return
        
        # Validate individual file selection
        selected_files = self.gui.file_list.get_selected_files()
        if not selected_files:
            messagebox.showwarning("Sin selección", "Selecciona al menos un archivo para descargar.")
            return
        
        # Show confirmation dialog with selection summary
        if not self._show_download_confirmation(selected_files, download_path):
            return
        
        # Check if we need external subtitles before starting download
        videos_without_subtitles = self.gui.download_manager.get_videos_without_subtitles(selected_files)
        
        if videos_without_subtitles:
            # Show subtitle search component instead of starting download immediately
            self.gui.subtitle_search.show_for_videos(videos_without_subtitles)
            return
        
        # Start download
        self.gui.download_manager.start_download(download_path, selected_files)
    
    def on_download_cancelled(self):
        """Handle download cancellation"""
        self.gui.download_manager.cancel_download()
    
    def on_subtitles_selected(self, selected_subtitles: Dict[str, Dict[str, Any]]):
        """Handle subtitle selection from the search component"""
        # Get current download configuration
        download_path = self.gui.download_controls.get_download_path()
        selected_files = self.gui.file_list.get_selected_files()
        
        if not selected_files:
            messagebox.showwarning("Sin archivos", "No hay archivos seleccionados para descargar.")
            return
        
        # Start download with external subtitles
        self.gui.download_manager.start_download(download_path, selected_files, selected_subtitles)
    
    def _show_download_confirmation(self, selected_files: List[Tuple[str, str, str]], download_path: str) -> bool:
        """Show download confirmation dialog"""
        file_count = len(selected_files)
        type_counts = {}
        for _, _, file_type in selected_files:
            type_counts[file_type] = type_counts.get(file_type, 0) + 1
        
        type_summary = ", ".join([f"{count} {file_type}{'s' if count > 1 else ''}" 
                                 for file_type, count in type_counts.items()])
        
        confirm_msg = f"¿Descargar {file_count} archivo{'s' if file_count > 1 else ''}?\n\n{type_summary}\n\nCarpeta: {download_path}"
        
        return messagebox.askyesno("Confirmar descarga", confirm_msg)
    
    def _check_for_videos_without_subtitles(self, selected_files: List[Tuple[str, str, str]]):
        """Check if there are videos without corresponding subtitles"""
        videos_without_subtitles = self.gui.download_manager.get_videos_without_subtitles(selected_files)
        
        if videos_without_subtitles:
            # Show a subtle hint that external subtitles can be searched
            video_count = len(videos_without_subtitles)
            self.gui.url_input.set_status(
                f"💡 {video_count} video{'s' if video_count > 1 else ''} sin subtítulos - puedes buscar subtítulos externos al descargar", 
                'normal'
            )
        else:
            # Hide subtitle search component if no videos need subtitles
            self.gui.subtitle_search.hide()
    
    def _refresh_file_list(self):
        """Refresh file list"""
        url = self.gui.url_input.get_url()
        if url and URLUtils.is_valid_url(url):
            self.on_url_analysis(url)
    
    def _on_window_closing(self):
        """Handle window closing"""
        if self.gui.download_manager.is_downloading:
            if messagebox.askyesno("Cerrar aplicación", 
                                 "Hay una descarga en progreso. ¿Quieres cerrar la aplicación?"):
                self.gui.download_manager.is_downloading = False
                self.gui.root.destroy()
        else:
            self.gui.root.destroy() 