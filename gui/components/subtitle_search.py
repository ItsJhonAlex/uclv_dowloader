"""
Subtitle Search Component - Simplified interface using widget system
"""

import tkinter as tk
from tkinter import messagebox
from typing import Dict, List, Any, Optional, Callable
from .widgets import SubtitleSearchWidget, SubtitleSearchManager
from .styling import ModernStyles


class SubtitleSearchComponent:
    """Simplified subtitle search component using widget architecture"""
    
    def __init__(self, parent, on_subtitles_selected: Optional[Callable] = None):
        self.parent = parent
        self.on_subtitles_selected = on_subtitles_selected
        
        # Initialize managers and widgets
        self.manager = SubtitleSearchManager()
        self.widget = SubtitleSearchWidget(parent, self.manager)
        
        # Store current videos for search
        self.videos_without_subtitles = []
        
        # Connect widget callbacks
        self._setup_callbacks()
    
    def _setup_callbacks(self):
        """Setup callbacks between widget and main component"""
        # Override widget's search button callback
        self.widget.search_button.configure(command=self._start_subtitle_search)
        
        # Add additional control buttons
        self._add_control_buttons()
    
    def _add_control_buttons(self):
        """Add additional control buttons to the widget"""
        controls_frame = self.widget.search_button.master
        
        # Skip button
        skip_button = tk.Button(controls_frame, text="⏭️ Continuar sin subtítulos",
                               style='Secondary.TButton',
                               command=self._skip_subtitle_search)
        skip_button.pack(side=tk.LEFT, padx=(0, ModernStyles.get_spacing('sm')))
        
        # Confirm selection button
        confirm_button = tk.Button(controls_frame, text="✅ Confirmar selección",
                                  style='Success.TButton',
                                  command=self._confirm_selection)
        confirm_button.pack(side=tk.LEFT, padx=(0, ModernStyles.get_spacing('sm')))
        
        # Clear results button
        clear_button = tk.Button(controls_frame, text="🗑️ Limpiar resultados",
                                style='Secondary.TButton',
                                command=self.widget.clear_results)
        clear_button.pack(side=tk.LEFT)
    
    def show_for_videos(self, videos_without_subtitles: List[tuple]):
        """Show the component for videos that don't have subtitles"""
        self.videos_without_subtitles = videos_without_subtitles
        self.widget.show_for_videos(videos_without_subtitles)
    
    def hide(self):
        """Hide the component"""
        self.widget.hide()
    
    def _start_subtitle_search(self):
        """Start searching for subtitles"""
        if not self.videos_without_subtitles:
            messagebox.showwarning("Sin videos", "No hay videos sin subtítulos para buscar.")
            return
        
        # Update widget state
        self.widget.update_search_state(True)
        
        # Start search using manager
        success = self.manager.start_search(
            self.videos_without_subtitles,
            language='spanish',
            status_callback=lambda msg: self.widget.set_status(msg, 'normal'),
            results_callback=self._handle_search_results,
            error_callback=self._handle_search_error
        )
        
        if not success:
            self.widget.update_search_state(False)
    
    def _handle_search_results(self, results: Dict[str, List[Dict[str, Any]]]):
        """Handle search results from manager"""
        self.widget.update_search_state(False)
        self.widget.display_search_results(results)
    
    def _handle_search_error(self, error_msg: str):
        """Handle search error"""
        self.widget.update_search_state(False)
        self.widget.set_status(f"❌ Error en la búsqueda: {error_msg}", 'error')
        messagebox.showerror("Error de búsqueda", f"Error al buscar subtítulos:\n{error_msg}")
    
    def _skip_subtitle_search(self):
        """Skip subtitle search and continue with download"""
        if self.on_subtitles_selected:
            self.on_subtitles_selected({})  # Empty selection
        self.hide()
    
    def _confirm_selection(self):
        """Handle confirm selection button click"""
        selected = self.manager.get_selected_subtitles()
        
        if not selected:
            if messagebox.askyesno("Sin subtítulos", 
                                 "No has seleccionado ningún subtítulo. ¿Continuar sin subtítulos externos?"):
                if self.on_subtitles_selected:
                    self.on_subtitles_selected({})
                self.hide()
            return
        
        # Show confirmation
        subtitle_count = len(selected)
        video_list = "\n".join([f"• {video}: {info.get('source', 'Unknown')}" 
                               for video, info in selected.items()])
        
        confirm_msg = f"¿Descargar {subtitle_count} subtítulo{'s' if subtitle_count > 1 else ''}?\n\n{video_list}"
        
        if messagebox.askyesno("Confirmar selección de subtítulos", confirm_msg):
            if self.on_subtitles_selected:
                self.on_subtitles_selected(selected)
            self.hide()
    
    def get_selected_subtitles(self) -> Dict[str, Dict[str, Any]]:
        """Get user-selected subtitles"""
        return self.manager.get_selected_subtitles()
    
    def pack(self, **kwargs):
        """Pack the component"""
        self.widget.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the component"""
        self.widget.grid(**kwargs)
    
    def place(self, **kwargs):
        """Place the component"""
        self.widget.place(**kwargs)