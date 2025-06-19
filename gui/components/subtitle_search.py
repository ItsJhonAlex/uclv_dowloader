"""
Subtitle Search component for UCLV Downloader GUI
Allows users to search and select subtitles from external sources
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from typing import Dict, List, Any, Optional, Callable
from .styles import ModernStyles


class SubtitleSearchComponent:
    """Component for searching and selecting external subtitles"""
    
    def __init__(self, parent, on_subtitles_selected: Optional[Callable] = None):
        self.parent = parent
        self.on_subtitles_selected = on_subtitles_selected
        self.frame = ttk.LabelFrame(parent, text="🔍 Búsqueda de subtítulos externos", 
                                   style='Section.TLabelframe', 
                                   padding=ModernStyles.get_spacing('lg'))
        
        # Data storage
        self.videos_without_subtitles = []
        self.subtitle_search_results = {}  # video_name -> list of subtitle options
        self.selected_subtitles = {}       # video_name -> selected subtitle info
        self.subtitle_vars = {}            # For radio buttons
        
        # UI components
        self.search_button = None
        self.status_label = None
        self.results_notebook = None
        self.is_searching = False
        
        # Initially hidden
        self.is_visible = False
        
        self._setup_component()
    
    def _setup_component(self):
        """Setup the subtitle search component"""
        # Initially hide the component
        self.frame.pack_forget()
        
        # Main container
        container = ttk.Frame(self.frame)
        container.pack(fill=tk.BOTH, expand=True)
        container.rowconfigure(2, weight=1)
        container.columnconfigure(0, weight=1)
        
        # Header section
        self._create_header_section(container)
        
        # Control buttons section
        self._create_controls_section(container)
        
        # Results section (notebook with tabs for each video)
        self._create_results_section(container)
    
    def _create_header_section(self, parent):
        """Create header with info about subtitle search"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E),
                         pady=(0, ModernStyles.get_spacing('md')))
        
        # Info text
        info_text = ("Se detectaron videos sin subtítulos. Puedes buscar subtítulos automáticamente "
                    "desde YouTube y OpenSubtitles.com para descargarlos junto con los videos.")
        
        info_label = ttk.Label(header_frame, text=info_text,
                              style='Caption.TLabel', wraplength=600)
        info_label.pack(anchor=tk.W)
        
        # Status label
        self.status_label = ttk.Label(header_frame, text="",
                                     style='Status.TLabel')
        self.status_label.pack(anchor=tk.W, pady=(ModernStyles.get_spacing('xs'), 0))
    
    def _create_controls_section(self, parent):
        """Create control buttons section"""
        controls_frame = ttk.Frame(parent)
        controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E),
                           pady=(0, ModernStyles.get_spacing('md')))
        
        # Search button
        self.search_button = ttk.Button(controls_frame, text="🔍 Buscar subtítulos",
                                       style='Primary.TButton',
                                       command=self._start_subtitle_search)
        self.search_button.pack(side=tk.LEFT, padx=(0, ModernStyles.get_spacing('sm')))
        
        # Skip button
        skip_button = ttk.Button(controls_frame, text="⏭️ Continuar sin subtítulos",
                                style='Secondary.TButton',
                                command=self._skip_subtitle_search)
        skip_button.pack(side=tk.LEFT, padx=(0, ModernStyles.get_spacing('sm')))
        
        # Confirm selection button
        confirm_button = ttk.Button(controls_frame, text="✅ Confirmar selección",
                                   style='Success.TButton',
                                   command=self._confirm_selection)
        confirm_button.pack(side=tk.LEFT, padx=(0, ModernStyles.get_spacing('sm')))
        
        # Clear results button
        clear_button = ttk.Button(controls_frame, text="🗑️ Limpiar resultados",
                                 style='Secondary.TButton',
                                 command=self._clear_results)
        clear_button.pack(side=tk.LEFT)
    
    def _create_results_section(self, parent):
        """Create results section with tabs for each video"""
        results_frame = ttk.Frame(parent)
        results_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.rowconfigure(0, weight=1)
        results_frame.columnconfigure(0, weight=1)
        
        # Notebook for tabs
        self.results_notebook = ttk.Notebook(results_frame)
        self.results_notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def show_for_videos(self, videos_without_subtitles: List[tuple]):
        """Show the component for videos that don't have subtitles"""
        self.videos_without_subtitles = videos_without_subtitles
        
        if not videos_without_subtitles:
            self.hide()
            return
        
        # Update status
        video_count = len(videos_without_subtitles)
        video_names = [video[0] for video in videos_without_subtitles]
        
        self.status_label.config(
            text=f"📹 {video_count} video{'s' if video_count > 1 else ''} sin subtítulos detectado{'s' if video_count > 1 else ''}",
            style='Warning.TLabel'
        )
        
        # Show the component
        self.frame.pack(fill=tk.BOTH, expand=True, 
                       pady=(0, ModernStyles.get_spacing('md')))
        self.is_visible = True
        
        # Clear previous results
        self._clear_results()
    
    def hide(self):
        """Hide the component"""
        self.frame.pack_forget()
        self.is_visible = False
    
    def _start_subtitle_search(self):
        """Start searching for subtitles in background"""
        if self.is_searching:
            return
        
        if not self.videos_without_subtitles:
            messagebox.showwarning("Sin videos", "No hay videos sin subtítulos para buscar.")
            return
        
        self.is_searching = True
        self._update_search_state(True)
        
        # Start search in background thread
        search_thread = threading.Thread(
            target=self._search_worker,
            daemon=True
        )
        search_thread.start()
    
    def _search_worker(self):
        """Background worker for subtitle search"""
        try:
            # Import here to avoid circular imports
            from core.subtitle_search import SubtitleSearchManager
            
            search_manager = SubtitleSearchManager()
            
            # Update status
            self.parent.after(0, lambda: self.status_label.config(
                text="🔍 Buscando subtítulos en YouTube y OpenSubtitles...", 
                style='Status.TLabel'))
            
            # Search subtitles
            results = search_manager.search_subtitles_for_videos(
                self.videos_without_subtitles, language='es'
            )
            
            # Update UI in main thread
            self.parent.after(0, lambda: self._display_search_results(results))
            
        except Exception as e:
            # Handle error in main thread
            self.parent.after(0, lambda: self._handle_search_error(str(e)))
        finally:
            # Reset state in main thread
            self.parent.after(0, lambda: self._update_search_state(False))
    
    def _display_search_results(self, results: Dict[str, List[Dict[str, Any]]]):
        """Display search results in the notebook"""
        self.subtitle_search_results = results
        
        # Clear existing tabs
        for tab in self.results_notebook.tabs():
            self.results_notebook.forget(tab)
        
        # Create tab for each video with results
        videos_with_results = 0
        total_subtitles = 0
        
        for video_name, subtitle_options in results.items():
            if subtitle_options:
                self._create_video_tab(video_name, subtitle_options)
                videos_with_results += 1
                total_subtitles += len(subtitle_options)
        
        # Update status
        if videos_with_results == 0:
            self.status_label.config(
                text="😞 No se encontraron subtítulos para ningún video",
                style='Error.TLabel'
            )
        else:
            self.status_label.config(
                text=f"🎉 Encontrados subtítulos para {videos_with_results} video{'s' if videos_with_results > 1 else ''} ({total_subtitles} opciones)",
                style='Success.TLabel'
            )
    
    def _create_video_tab(self, video_name: str, subtitle_options: List[Dict[str, Any]]):
        """Create a tab for a video with its subtitle options"""
        # Create tab frame
        tab_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(tab_frame, text=f"📹 {video_name[:20]}...")
        
        # Container with scrollbar
        canvas = tk.Canvas(tab_frame, height=200)
        scrollbar = ttk.Scrollbar(tab_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Radio button variable for this video
        var = tk.StringVar()
        self.subtitle_vars[video_name] = var
        
        # None option (no subtitle)
        none_frame = ttk.Frame(scrollable_frame)
        none_frame.pack(fill=tk.X, pady=(0, ModernStyles.get_spacing('xs')))
        
        none_radio = ttk.Radiobutton(none_frame, text="❌ No descargar subtítulo",
                                    variable=var, value="none",
                                    style='Modern.TRadiobutton')
        none_radio.pack(anchor=tk.W)
        var.set("none")  # Default to no subtitle
        
        # Separator
        separator = ttk.Separator(scrollable_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=ModernStyles.get_spacing('xs'))
        
        # Subtitle options
        for i, subtitle in enumerate(subtitle_options):
            self._create_subtitle_option(scrollable_frame, video_name, subtitle, var, i)
    
    def _create_subtitle_option(self, parent, video_name: str, subtitle: Dict[str, Any], 
                               var: tk.StringVar, index: int):
        """Create a subtitle option widget"""
        option_frame = ttk.Frame(parent)
        option_frame.pack(fill=tk.X, pady=(0, ModernStyles.get_spacing('sm')))
        
        # Main radio button
        radio_text = f"🌐 {subtitle.get('source', 'Unknown')} - {subtitle.get('title', 'Unknown')}"
        radio = ttk.Radiobutton(option_frame, text=radio_text,
                               variable=var, value=str(index),
                               style='Modern.TRadiobutton')
        radio.pack(anchor=tk.W)
        
        # Details frame
        details_frame = ttk.Frame(option_frame)
        details_frame.pack(fill=tk.X, padx=(ModernStyles.get_spacing('lg'), 0))
        
        # Confidence and additional info
        confidence = subtitle.get('confidence', 0)
        rating = subtitle.get('rating', 0)
        downloads = subtitle.get('download_count', 0)
        
        details_text = f"📊 Similitud: {confidence:.1%}"
        if rating > 0:
            details_text += f" | ⭐ Calificación: {rating:.1f}"
        if downloads > 0:
            details_text += f" | ⬇️ Descargas: {downloads:,}"
        
        details_label = ttk.Label(details_frame, text=details_text,
                                 style='Caption.TLabel')
        details_label.pack(anchor=tk.W)
    
    def _update_search_state(self, searching: bool):
        """Update UI state during search"""
        self.is_searching = searching
        
        if searching:
            self.search_button.config(text="🔄 Buscando...", state=tk.DISABLED)
        else:
            self.search_button.config(text="🔍 Buscar subtítulos", state=tk.NORMAL)
    
    def _handle_search_error(self, error_msg: str):
        """Handle search error"""
        self.status_label.config(
            text=f"❌ Error en la búsqueda: {error_msg}",
            style='Error.TLabel'
        )
        messagebox.showerror("Error de búsqueda", f"Error al buscar subtítulos:\n{error_msg}")
    
    def _skip_subtitle_search(self):
        """Skip subtitle search and continue with download"""
        if self.on_subtitles_selected:
            self.on_subtitles_selected({})  # Empty selection
        self.hide()
    
    def _clear_results(self):
        """Clear search results"""
        self.subtitle_search_results = {}
        self.selected_subtitles = {}
        self.subtitle_vars = {}
        
        # Clear notebook tabs
        for tab in self.results_notebook.tabs():
            self.results_notebook.forget(tab)
        
        self.status_label.config(text="Resultados limpiados", style='Status.TLabel')
    
    def get_selected_subtitles(self) -> Dict[str, Dict[str, Any]]:
        """Get user-selected subtitles"""
        selected = {}
        
        for video_name, var in self.subtitle_vars.items():
            selection = var.get()
            
            if selection != "none" and selection.isdigit():
                index = int(selection)
                subtitle_options = self.subtitle_search_results.get(video_name, [])
                
                if 0 <= index < len(subtitle_options):
                    selected[video_name] = subtitle_options[index]
        
        return selected
    
    def _confirm_selection(self):
        """Handle confirm selection button click"""
        self.confirm_selection()
    
    def confirm_selection(self) -> bool:
        """Show confirmation dialog and return selected subtitles"""
        selected = self.get_selected_subtitles()
        
        if not selected:
            if messagebox.askyesno("Sin subtítulos", 
                                 "No has seleccionado ningún subtítulo. ¿Continuar sin subtítulos externos?"):
                if self.on_subtitles_selected:
                    self.on_subtitles_selected({})
                self.hide()
                return True
            return False
        
        # Show confirmation
        subtitle_count = len(selected)
        video_list = "\n".join([f"• {video}: {info.get('source', 'Unknown')}" 
                               for video, info in selected.items()])
        
        confirm_msg = f"¿Descargar {subtitle_count} subtítulo{'s' if subtitle_count > 1 else ''}?\n\n{video_list}"
        
        if messagebox.askyesno("Confirmar selección de subtítulos", confirm_msg):
            if self.on_subtitles_selected:
                self.on_subtitles_selected(selected)
            self.hide()
            return True
        
        return False
    
    def pack(self, **kwargs):
        """Pack the component"""
        if self.is_visible:
            self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the component"""
        if self.is_visible:
            self.frame.grid(**kwargs)
    
    def place(self, **kwargs):
        """Place the component"""
        if self.is_visible:
            self.frame.place(**kwargs) 