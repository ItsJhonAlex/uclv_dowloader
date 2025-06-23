"""
Subtitle Search Widget - UI components for subtitle search
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Any, Optional, Callable
from ..styling import ModernStyles


class SubtitleSearchWidget:
    """UI widget for subtitle search interface"""
    
    def __init__(self, parent, manager):
        self.parent = parent
        self.manager = manager
        self.frame = ttk.LabelFrame(parent, text="🔍 Búsqueda de subtítulos externos", 
                                   style='Section.TLabelframe', 
                                   padding=ModernStyles.get_spacing('lg'))
        
        # UI components
        self.search_button = None
        self.status_label = None
        self.results_notebook = None
        
        # Initially hidden
        self.is_visible = False
        
        self._setup_widget()
    
    def _setup_widget(self):
        """Setup the subtitle search widget"""
        # Initially hide the widget
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
                                       command=self._on_search_clicked)
        self.search_button.pack(side=tk.LEFT, padx=(0, ModernStyles.get_spacing('sm')))
        
        # Additional buttons can be added here with callbacks
    
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
        """Show the widget for videos that don't have subtitles"""
        if not videos_without_subtitles:
            self.hide()
            return
        
        # Get video info
        video_info = self.manager.get_videos_without_subtitles_info(videos_without_subtitles)
        
        # Update status
        status_text = f"📹 {video_info['count']} video{'s' if video_info['plural'] else ''} sin subtítulos detectado{'s' if video_info['plural'] else ''}"
        self.status_label.config(text=status_text, style='Warning.TLabel')
        
        # Show the widget
        self.frame.pack(fill=tk.BOTH, expand=True, 
                       pady=(0, ModernStyles.get_spacing('md')))
        self.is_visible = True
        
        # Clear previous results
        self.clear_results()
    
    def hide(self):
        """Hide the widget"""
        self.frame.pack_forget()
        self.is_visible = False
    
    def _on_search_clicked(self):
        """Handle search button click"""
        # This would be connected to the main component's search logic
        pass
    
    def update_search_state(self, searching: bool):
        """Update UI state during search"""
        if searching:
            self.search_button.config(text="🔄 Buscando...", state=tk.DISABLED)
        else:
            self.search_button.config(text="🔍 Buscar subtítulos", state=tk.NORMAL)
    
    def set_status(self, message: str, status_type: str = 'normal'):
        """Set status message"""
        style_map = {
            'normal': 'Status.TLabel',
            'success': 'Success.TLabel',
            'error': 'Error.TLabel',
            'warning': 'Warning.TLabel'
        }
        
        style = style_map.get(status_type, 'Status.TLabel')
        self.status_label.config(text=message, style=style)
    
    def display_search_results(self, results: Dict[str, List[Dict[str, Any]]]):
        """Display search results in the notebook"""
        # Clear existing tabs
        for tab in self.results_notebook.tabs():
            self.results_notebook.forget(tab)
        
        # Process results
        result_info = self.manager.process_search_results(results)
        
        # Create tabs for videos with results
        for video_name, subtitle_options in results.items():
            if subtitle_options:
                self._create_video_tab(video_name, subtitle_options)
        
        # Update status
        if not result_info['has_results']:
            self.set_status("😞 No se encontraron subtítulos para ningún video", 'error')
        else:
            videos_count = result_info['videos_with_results']
            subtitles_count = result_info['total_subtitles']
            self.set_status(
                f"🎉 Encontrados subtítulos para {videos_count} video{'s' if videos_count > 1 else ''} ({subtitles_count} opciones)", 
                'success'
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
        self.manager.register_subtitle_variable(video_name, var)
        
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
    
    def clear_results(self):
        """Clear search results"""
        # Clear notebook tabs
        for tab in self.results_notebook.tabs():
            self.results_notebook.forget(tab)
        
        # Clear manager state
        self.manager.clear_results()
        
        self.set_status("Resultados limpiados", 'normal')
    
    def pack(self, **kwargs):
        """Pack the widget"""
        if self.is_visible:
            self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the widget"""
        if self.is_visible:
            self.frame.grid(**kwargs)
    
    def place(self, **kwargs):
        """Place the widget"""
        if self.is_visible:
            self.frame.place(**kwargs) 