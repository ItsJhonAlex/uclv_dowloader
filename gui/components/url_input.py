"""
URL Input component for UCLV Downloader GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from typing import Callable, Optional
from .styles import ModernStyles
from core import URLUtils


class URLInputComponent:
    """Modern URL input component with validation and analysis"""
    
    def __init__(self, parent, on_analysis_complete: Optional[Callable] = None):
        self.parent = parent
        self.on_analysis_complete = on_analysis_complete
        self.frame = ttk.LabelFrame(parent, text="🔗 URL de la carpeta", 
                                   style='Section.TLabelframe', padding=ModernStyles.get_spacing('lg'))
        
        # State variables
        self.url_var = tk.StringVar()
        self.is_analyzing = False
        
        # UI components
        self.url_entry = None
        self.analyze_btn = None
        self.status_label = None
        self.validation_label = None
        
        self._setup_component()
        self._setup_bindings()
    
    def _setup_component(self):
        """Setup the URL input component"""
        # Main container
        container = ttk.Frame(self.frame)
        container.pack(fill=tk.X)
        container.columnconfigure(1, weight=1)
        
        # URL input row
        input_frame = ttk.Frame(container)
        input_frame.pack(fill=tk.X, pady=(0, ModernStyles.get_spacing('sm')))
        input_frame.columnconfigure(1, weight=1)
        
        # URL label
        url_label = ttk.Label(input_frame, text="URL:",
                             style='Heading.TLabel')
        url_label.grid(row=0, column=0, sticky=tk.W, 
                      padx=(0, ModernStyles.get_spacing('md')))
        
        # URL entry
        self.url_entry = ttk.Entry(input_frame, textvariable=self.url_var,
                                  style='Modern.TEntry', font=ModernStyles.get_font('body'))
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E),
                           padx=(0, ModernStyles.get_spacing('md')))
        
        # Analyze button
        self.analyze_btn = ttk.Button(input_frame, text="🔍 Analizar",
                                     style='Primary.TButton',
                                     command=self._on_analyze_clicked)
        self.analyze_btn.grid(row=0, column=2, sticky=tk.E)
        
        # Validation feedback
        validation_frame = ttk.Frame(container)
        validation_frame.pack(fill=tk.X, pady=(ModernStyles.get_spacing('xs'), 0))
        
        self.validation_label = ttk.Label(validation_frame, text="",
                                         style='Caption.TLabel')
        self.validation_label.pack(anchor=tk.W)
        
        # Status row
        status_frame = ttk.Frame(container)
        status_frame.pack(fill=tk.X, pady=(ModernStyles.get_spacing('sm'), 0))
        
        self.status_label = ttk.Label(status_frame, text="Ingresa la URL de una carpeta de visuales.ucv.cu",
                                     style='Status.TLabel')
        self.status_label.pack(anchor=tk.W)
        
        # Examples section (collapsible)
        self._create_examples_section(container)
    
    def _create_examples_section(self, parent):
        """Create examples section"""
        examples_frame = ttk.Frame(parent)
        examples_frame.pack(fill=tk.X, pady=(ModernStyles.get_spacing('md'), 0))
        
        # Examples toggle button
        self.examples_visible = False
        self.toggle_btn = ttk.Button(examples_frame, text="💡 Ver ejemplos",
                                    style='Secondary.TButton',
                                    command=self._toggle_examples)
        self.toggle_btn.pack(anchor=tk.W)
        
        # Examples content (initially hidden)
        self.examples_content = ttk.Frame(examples_frame)
        
        examples_text = """Ejemplos de URLs válidas:
• https://visuales.ucv.cu/Series/Ingles/Breaking%20Bad/Breaking%20Bad%20x%201/
• https://visuales.ucv.cu/Peliculas/Accion/Matrix/
• https://visuales.ucv.cu/Documentales/Ciencia/Cosmos/"""
        
        examples_label = ttk.Label(self.examples_content, text=examples_text,
                                  style='Caption.TLabel', justify=tk.LEFT)
        examples_label.pack(anchor=tk.W, pady=(ModernStyles.get_spacing('sm'), 0))
    
    def _setup_bindings(self):
        """Setup event bindings"""
        # URL validation on typing
        self.url_var.trace('w', self._on_url_changed)
        
        # Enter key to analyze
        self.url_entry.bind('<Return>', lambda e: self._on_analyze_clicked())
        
        # Paste event
        self.url_entry.bind('<Control-v>', self._on_paste)
    
    def _on_url_changed(self, *args):
        """Handle URL text changes for real-time validation"""
        url = self.url_var.get().strip()
        
        if not url:
            self.validation_label.config(text="", style='Caption.TLabel')
            self.analyze_btn.config(state=tk.DISABLED)
            return
        
        # Basic validation
        if URLUtils.is_valid_url(url):
            if 'visuales.ucv.cu' in url:
                self.validation_label.config(text="✅ URL válida", 
                                           style='Success.TLabel')
                self.analyze_btn.config(state=tk.NORMAL)
            else:
                self.validation_label.config(text="⚠️ URL válida pero no es de visuales.ucv.cu", 
                                           style='Warning.TLabel')
                self.analyze_btn.config(state=tk.NORMAL)
        else:
            self.validation_label.config(text="❌ URL inválida", 
                                       style='Error.TLabel')
            self.analyze_btn.config(state=tk.DISABLED)
    
    def _on_paste(self, event):
        """Handle paste event for better UX"""
        # Small delay to let the paste complete
        self.url_entry.after(10, self._on_url_changed)
    
    def _toggle_examples(self):
        """Toggle examples visibility"""
        if self.examples_visible:
            self.examples_content.pack_forget()
            self.toggle_btn.config(text="💡 Ver ejemplos")
            self.examples_visible = False
        else:
            self.examples_content.pack(fill=tk.X, pady=(ModernStyles.get_spacing('sm'), 0))
            self.toggle_btn.config(text="🔼 Ocultar ejemplos")
            self.examples_visible = True
    
    def _on_analyze_clicked(self):
        """Handle analyze button click"""
        url = self.url_var.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Por favor ingresa una URL")
            return
        
        if not URLUtils.is_valid_url(url):
            messagebox.showerror("Error", "URL inválida. Debe comenzar con http:// o https://")
            return
        
        self._start_analysis(url)
    
    def _start_analysis(self, url: str):
        """Start URL analysis in background thread"""
        if self.is_analyzing:
            return
        
        self.is_analyzing = True
        self._update_analyzing_state(True)
        
        def analyze_thread():
            try:
                # Call the analysis callback if provided
                if self.on_analysis_complete:
                    self.on_analysis_complete(url)
                
            except Exception as e:
                # Handle error in main thread
                self.parent.after(0, lambda: self._handle_analysis_error(str(e)))
            finally:
                # Reset state in main thread
                self.parent.after(0, lambda: self._update_analyzing_state(False))
        
        threading.Thread(target=analyze_thread, daemon=True).start()
    
    def _update_analyzing_state(self, analyzing: bool):
        """Update UI state during analysis"""
        self.is_analyzing = analyzing
        
        if analyzing:
            self.analyze_btn.config(text="🔄 Analizando...", state=tk.DISABLED)
            self.status_label.config(text="🔍 Analizando URL y obteniendo lista de archivos...",
                                   style='Status.TLabel')
            self.url_entry.config(state=tk.DISABLED)
        else:
            self.analyze_btn.config(text="🔍 Analizar", state=tk.NORMAL)
            self.status_label.config(text="Análisis completado",
                                   style='Success.TLabel')
            self.url_entry.config(state=tk.NORMAL)
    
    def _handle_analysis_error(self, error_msg: str):
        """Handle analysis error"""
        self.status_label.config(text=f"❌ Error: {error_msg}",
                               style='Error.TLabel')
        messagebox.showerror("Error de análisis", f"Error al analizar URL:\n{error_msg}")
    
    def get_url(self) -> str:
        """Get the current URL"""
        return self.url_var.get().strip()
    
    def set_url(self, url: str):
        """Set the URL programmatically"""
        self.url_var.set(url)
    
    def clear_url(self):
        """Clear the URL field"""
        self.url_var.set("")
    
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
    
    def pack(self, **kwargs):
        """Pack the component"""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the component"""
        self.frame.grid(**kwargs)
    
    def place(self, **kwargs):
        """Place the component"""
        self.frame.place(**kwargs) 