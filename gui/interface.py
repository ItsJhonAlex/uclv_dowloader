"""
Modern Modular GUI Interface for UCLV Downloader using Components
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any

from core import UCLVDownloader, URLUtils, FileUtils
from .components import (
    HeaderComponent,
    URLInputComponent, 
    FileTypeComponent,
    FileListComponent,
    DownloadControlsComponent,
    ProgressComponent,
    SubtitleSearchComponent,
    ModernStyles
)


class ModernGUIInterface:
    """Modern modular GUI interface for UCLV Downloader"""
    
    def __init__(self):
        # Core components
        self.downloader = UCLVDownloader()
        self.download_thread: Optional[threading.Thread] = None
        self.is_downloading = False
        
        # Create main window
        self.root = self._create_main_window()
        
        # Setup modern theme
        self.style = ModernStyles.setup_theme(self.root)
        
        # Initialize components
        self._setup_components()
        
        # Layout components
        self._setup_layout()
        
        # Setup event bindings
        self._setup_bindings()
    
    def _create_main_window(self) -> tk.Tk:
        """Create and configure the main window"""
        root = tk.Tk()
        root.title("🎬 UCLV Downloader")
        root.geometry("950x800")  # Aumentado para mejor visualización
        root.minsize(800, 600)
        root.resizable(True, True)
        
        # Set window icon (if available)
        # root.iconbitmap("icon.ico")  # Uncomment if you have an icon
        
        # Configure main window background
        root.configure(bg=ModernStyles.get_color('bg_primary'))
        
        # Center window on screen
        self._center_window(root)
        
        return root
    
    def _center_window(self, window):
        """Center window on screen"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def _setup_components(self):
        """Initialize all GUI components with scrollable container"""
        # Create main scrollable frame
        self._create_scrollable_container()
        
        # Create components inside scrollable area
        self.header = HeaderComponent(self.scrollable_frame)
        
        self.url_input = URLInputComponent(self.scrollable_frame, 
                                          on_analysis_complete=self._on_url_analysis)
        
        self.file_types = FileTypeComponent(self.scrollable_frame,
                                           on_selection_changed=self._on_file_type_changed)
        
        self.file_list = FileListComponent(self.scrollable_frame,
                                          on_selection_changed=self._on_file_selection_changed)
        
        self.subtitle_search = SubtitleSearchComponent(self.scrollable_frame,
                                                      on_subtitles_selected=self._on_subtitles_selected)
        
        self.download_controls = DownloadControlsComponent(self.scrollable_frame,
                                                          on_download=self._on_download_started,
                                                          on_cancel=self._on_download_cancelled)
        
        self.progress = ProgressComponent(self.scrollable_frame)
    
    def _create_scrollable_container(self):
        """Create a scrollable container for all components"""
        # Main container frame (fills the window)
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, 
                                padx=ModernStyles.get_spacing('md'),
                                pady=ModernStyles.get_spacing('md'))
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self.main_container, 
                               bg=ModernStyles.get_color('bg_primary'),
                               highlightthickness=0)
        
        self.v_scrollbar = ttk.Scrollbar(self.main_container, 
                                        orient=tk.VERTICAL, 
                                        command=self.canvas.yview)
        
        # Configure scrollbar
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)
        
        # Create scrollable frame inside canvas
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Add scrollable frame to canvas
        self.canvas_frame = self.canvas.create_window(
            (0, 0), 
            window=self.scrollable_frame, 
            anchor="nw"
        )
        
        # Pack canvas and scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind mouse wheel to canvas
        self._bind_mousewheel()
        
        # Bind canvas resize to update scroll region
        self.canvas.bind("<Configure>", self._on_canvas_configure)
    
    def _bind_mousewheel(self):
        """Bind mouse wheel events for scrolling"""
        def _on_mousewheel(event):
            if self.canvas.winfo_exists():
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            if self.canvas.winfo_exists():
                self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            if self.canvas.winfo_exists():
                self.canvas.unbind_all("<MouseWheel>")
        
        # Bind mouse wheel when entering the canvas
        self.canvas.bind('<Enter>', _bind_to_mousewheel)
        self.canvas.bind('<Leave>', _unbind_from_mousewheel)
        
        # For Linux systems (additional binding)
        def _on_mousewheel_linux(event):
            if self.canvas.winfo_exists():
                if event.num == 4:
                    self.canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    self.canvas.yview_scroll(1, "units")
        
        self.canvas.bind("<Button-4>", _on_mousewheel_linux)
        self.canvas.bind("<Button-5>", _on_mousewheel_linux)
    
    def _on_canvas_configure(self, event):
        """Handle canvas resize to update scrollable frame width"""
        # Update the scrollable frame width to match canvas width
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)
    
    def _setup_layout(self):
        """Setup component layout in scrollable container"""
        # All components now use pack with proper spacing
        self.header.pack(fill=tk.X, pady=(0, ModernStyles.get_spacing('lg')))
        
        self.url_input.pack(fill=tk.X, pady=(0, ModernStyles.get_spacing('md')))
        
        self.file_types.pack(fill=tk.X, pady=(0, ModernStyles.get_spacing('md')))
        
        # File list with fixed height to prevent excessive expansion
        self.file_list.pack(fill=tk.X, pady=(0, ModernStyles.get_spacing('md')))
        
        # Subtitle search component (initially hidden)
        # Will be shown conditionally when needed
        
        self.download_controls.pack(fill=tk.X, 
                                   pady=(0, ModernStyles.get_spacing('md')))
        
        self.progress.pack(fill=tk.X, pady=(0, ModernStyles.get_spacing('lg')))
        
        # Force canvas to update scroll region after layout
        self.root.after(100, self._update_scroll_region)
    
    def _update_scroll_region(self):
        """Update the scroll region to encompass all widgets"""
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _setup_bindings(self):
        """Setup event bindings"""
        # Window close event
        self.root.protocol("WM_DELETE_WINDOW", self._on_window_closing)
        
        # Keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.url_input.url_entry.focus())
        self.root.bind('<Control-d>', lambda e: self._on_download_started(
            self.download_controls.get_download_path()) if not self.is_downloading else None)
        self.root.bind('<F5>', lambda e: self._refresh_file_list())
        self.root.bind('<Escape>', lambda e: self._on_download_cancelled() if self.is_downloading else None)
    
    def _on_url_analysis(self, url: str):
        """Handle URL analysis completion"""
        try:
            # Configure downloader based on file type selections
            selected_types = self.file_types.get_selected_types()
            self.downloader.configure_downloads(
                videos=selected_types.get('videos', False),
                subtitles=selected_types.get('subtitles', False),
                images=selected_types.get('images', False),
                info=selected_types.get('info', False)
            )
            
            # Get file list
            files = self.downloader.get_file_list(url)
            
            # Update file list component
            self.file_list.set_files(files)
            
            # Enable download if files found
            if files:
                self.download_controls.enable_download(True)
                self.url_input.set_status(f"✅ Encontrados {len(files)} archivos", 'success')
            else:
                self.download_controls.enable_download(False)
                self.url_input.set_status("⚠️ No se encontraron archivos del tipo seleccionado", 'warning')
            
        except Exception as e:
            # Handle analysis error
            self.file_list.clear_files()
            self.download_controls.enable_download(False)
            self.url_input.set_status(f"❌ Error: {str(e)}", 'error')
            messagebox.showerror("Error de análisis", f"Error al analizar URL:\n{e}")
    
    def _on_file_type_changed(self, selected_types):
        """Handle file type selection changes"""
        # Re-analyze if URL is present
        url = self.url_input.get_url()
        if url and URLUtils.is_valid_url(url):
            # Trigger re-analysis with new file types
            self._on_url_analysis(url)
    
    def _on_file_selection_changed(self, selected_files):
        """Handle individual file selection changes"""
        # Update download button state based on selection
        has_selection = len(selected_files) > 0
        self.download_controls.enable_download(has_selection)
        
        # Check for videos without subtitles
        self._check_for_videos_without_subtitles(selected_files)
        
        # Update status
        if len(selected_files) == 0:
            self.url_input.set_status("⚠️ Selecciona al menos un archivo para descargar", 'warning')
        else:
            self.url_input.set_status(f"✅ {len(selected_files)} archivos seleccionados para descarga", 'success')
    
    def _on_download_started(self, download_path: str):
        """Handle download start"""
        if self.is_downloading:
            return
        
        # Validate we have files to download
        if self.file_list.get_file_count() == 0:
            messagebox.showwarning("Sin archivos", "No hay archivos para descargar. Analiza una URL primero.")
            return
        
        # Validate individual file selection
        selected_files = self.file_list.get_selected_files()
        if not selected_files:
            messagebox.showwarning("Sin selección", "Selecciona al menos un archivo para descargar.")
            return
        
        # Show confirmation dialog with selection summary
        file_count = len(selected_files)
        type_counts = {}
        for _, _, file_type in selected_files:
            type_counts[file_type] = type_counts.get(file_type, 0) + 1
        
        type_summary = ", ".join([f"{count} {file_type}{'s' if count > 1 else ''}" 
                                 for file_type, count in type_counts.items()])
        
        confirm_msg = f"¿Descargar {file_count} archivo{'s' if file_count > 1 else ''}?\n\n{type_summary}\n\nCarpeta: {download_path}"
        
        if not messagebox.askyesno("Confirmar descarga", confirm_msg):
            return
        
        # Check if we need external subtitles before starting download
        videos_without_subtitles = self._get_videos_without_subtitles(selected_files)
        
        if videos_without_subtitles:
            # Show subtitle search component instead of starting download immediately
            self.subtitle_search.show_for_videos(videos_without_subtitles)
            return
        
        # Start download in background thread
        self.is_downloading = True
        self._update_ui_for_download_state(True)
        
        self.download_thread = threading.Thread(
            target=self._download_worker,
            args=(download_path, selected_files, {}),  # Empty external subtitles
            daemon=True
        )
        self.download_thread.start()
    
    def _check_for_videos_without_subtitles(self, selected_files: List[Tuple[str, str, str]]):
        """Check if there are videos without corresponding subtitles"""
        videos_without_subtitles = self._get_videos_without_subtitles(selected_files)
        
        if videos_without_subtitles:
            # Show a subtle hint that external subtitles can be searched
            video_count = len(videos_without_subtitles)
            self.url_input.set_status(
                f"💡 {video_count} video{'s' if video_count > 1 else ''} sin subtítulos - puedes buscar subtítulos externos al descargar", 
                'normal'
            )
        else:
            # Hide subtitle search component if no videos need subtitles
            self.subtitle_search.hide()
    
    def _get_videos_without_subtitles(self, selected_files: List[Tuple[str, str, str]]) -> List[Tuple[str, str, str]]:
        """Get list of videos that don't have corresponding subtitle files"""
        from pathlib import Path
        
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
    
    def _on_subtitles_selected(self, selected_subtitles: Dict[str, Dict[str, Any]]):
        """Handle subtitle selection from the search component"""
        # Get current download configuration
        download_path = self.download_controls.get_download_path()
        selected_files = self.file_list.get_selected_files()
        
        if not selected_files:
            messagebox.showwarning("Sin archivos", "No hay archivos seleccionados para descargar.")
            return
        
        # Start download with external subtitles
        self.is_downloading = True
        self._update_ui_for_download_state(True)
        
        self.download_thread = threading.Thread(
            target=self._download_worker,
            args=(download_path, selected_files, selected_subtitles),
            daemon=True
        )
        self.download_thread.start()
    
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
                self.root.after(0, lambda: self.progress.set_progress(file_progress))
                self.root.after(0, lambda: self.progress.set_current_file(filename))
                self.root.after(0, lambda: self.progress.update_stats(
                    downloaded=self._completed_files, 
                    total=self._total_files
                ))
                self.root.after(0, lambda: self.progress.set_status(
                    f"Descargando archivo {self._completed_files + 1} de {self._total_files}: {filename}", 'downloading'))
            
            # Start download with selected files
            url = self.url_input.get_url()
            result = self.downloader.download_selected_files(selected_files, url, download_path, progress_callback)
            
            # Download external subtitles if any were selected
            if external_subtitles:
                self.root.after(0, lambda: self.progress.set_status("Descargando subtítulos externos...", 'downloading'))
                
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
            self.root.after(0, lambda: self._download_completed(result))
            
        except Exception as e:
            # Handle error in main thread
            self.root.after(0, lambda: self._download_error(str(e)))
    
    def _download_completed(self, result):
        """Handle download completion"""
        self.is_downloading = False
        self._update_ui_for_download_state(False)
        
        # Update progress
        if result.get('success', False):
            self.progress.animate_success()
        
        # Show completion message
        completed = result.get('completed', 0)
        failed_list = result.get('failed', [])
        failed_count = len(failed_list)
        total = result.get('total', 0)
        
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
        self._update_ui_for_download_state(False)
        
        # Update progress
        self.progress.show_error(error_msg)
        
        # Show error message
        messagebox.showerror("Error de descarga", f"Error durante la descarga:\n{error_msg}")
    
    def _on_download_cancelled(self):
        """Handle download cancellation"""
        if not self.is_downloading:
            return
        
        # Ask for confirmation
        if messagebox.askyesno("Cancelar descarga", "¿Estás seguro de que quieres cancelar la descarga?"):
            # Note: The actual cancellation would need to be implemented in the downloader
            self.is_downloading = False
            self._update_ui_for_download_state(False)
            
            # Update progress
            self.progress.set_status("❌ Descarga cancelada", 'cancelled')
            
            messagebox.showinfo("Cancelado", "Descarga cancelada por el usuario")
    
    def _update_ui_for_download_state(self, downloading: bool):
        """Update UI state for downloading"""
        # Update download controls
        self.download_controls.set_download_state(downloading)
        
        # Update progress
        if downloading:
            self.progress.set_status("Iniciando descarga...", 'downloading')
            self.progress.set_progress(0)
        else:
            if not self.is_downloading:  # Only reset if not actually downloading
                self.progress.reset_progress()
    
    def _refresh_file_list(self):
        """Refresh file list"""
        url = self.url_input.get_url()
        if url and URLUtils.is_valid_url(url):
            self._on_url_analysis(url)
    
    def _on_window_closing(self):
        """Handle window closing"""
        if self.is_downloading:
            if messagebox.askyesno("Cerrar aplicación", 
                                 "Hay una descarga en progreso. ¿Quieres cerrar la aplicación?"):
                self.is_downloading = False
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """Run the GUI application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Aplicación interrumpida por el usuario")
        except Exception as e:
            print(f"Error inesperado: {e}")
            messagebox.showerror("Error", f"Error inesperado: {e}")
        finally:
            if self.root:
                self.root.destroy()


def main():
    """Main entry point for GUI"""
    try:
        app = ModernGUIInterface()
        app.run()
    except ImportError as e:
        if 'tkinter' in str(e):
            print("❌ Error: tkinter no está disponible")
            print("En Ubuntu/Debian, instala: sudo apt install python3-tk")
            print("En otros sistemas, consulta la documentación de Python")
        else:
            print(f"❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error al inicializar la interfaz gráfica: {e}")
        return False
    
    return True


if __name__ == "__main__":
    main()
