"""
GUI Interface for UCVL Downloader using Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
from pathlib import Path
from typing import Optional

from core import UCVLDownloader, URLUtils, FileUtils


class GUIInterface:
    """Graphical User Interface for UCVL Downloader"""
    
    def __init__(self):
        self.downloader = UCVLDownloader()
        self.download_thread: Optional[threading.Thread] = None
        self.is_downloading = False
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("🎬 UCVL Downloader")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🎬 UCVL Downloader", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL input section
        ttk.Label(main_frame, text="📎 URL de la carpeta:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=60)
        self.url_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 5))
        
        self.analyze_btn = ttk.Button(main_frame, text="🔍 Analizar", command=self.analyze_url)
        self.analyze_btn.grid(row=1, column=2, pady=5)
        
        # File type selection
        file_types_frame = ttk.LabelFrame(main_frame, text="🔧 Tipos de archivo a descargar", padding="10")
        file_types_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        file_types_frame.columnconfigure(1, weight=1)
        
        self.videos_var = tk.BooleanVar(value=True)
        self.subtitles_var = tk.BooleanVar(value=True)
        self.images_var = tk.BooleanVar(value=False)
        self.info_var = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(file_types_frame, text="📹 Videos", variable=self.videos_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(file_types_frame, text="📝 Subtítulos", variable=self.subtitles_var).grid(row=0, column=1, sticky=tk.W)
        ttk.Checkbutton(file_types_frame, text="🖼️ Imágenes", variable=self.images_var).grid(row=0, column=2, sticky=tk.W)
        ttk.Checkbutton(file_types_frame, text="📄 Info", variable=self.info_var).grid(row=0, column=3, sticky=tk.W)
        
        # Files preview
        preview_frame = ttk.LabelFrame(main_frame, text="📋 Archivos encontrados", padding="10")
        preview_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
        # Treeview for file list
        columns = ('Nombre', 'Tipo', 'Tamaño')
        self.files_tree = ttk.Treeview(preview_frame, columns=columns, show='headings', height=8)
        
        # Configure columns
        self.files_tree.heading('Nombre', text='📄 Nombre del archivo')
        self.files_tree.heading('Tipo', text='🏷️ Tipo')
        self.files_tree.heading('Tamaño', text='📏 Tamaño')
        
        self.files_tree.column('Nombre', width=400)
        self.files_tree.column('Tipo', width=100)
        self.files_tree.column('Tamaño', width=100)
        
        # Scrollbar for treeview
        tree_scrollbar = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=self.files_tree.yview)
        self.files_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.files_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Download path selection
        path_frame = ttk.Frame(main_frame)
        path_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        path_frame.columnconfigure(1, weight=1)
        
        ttk.Label(path_frame, text="📁 Carpeta de descarga:").grid(row=0, column=0, sticky=tk.W)
        
        self.download_path_var = tk.StringVar(value="./descarga")
        self.path_entry = ttk.Entry(path_frame, textvariable=self.download_path_var, width=50)
        self.path_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5))
        
        ttk.Button(path_frame, text="📂", command=self.select_download_path).grid(row=0, column=2)
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="📊 Progreso", padding="10")
        progress_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.status_var = tk.StringVar(value="Listo para descargar")
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
        # Control buttons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=6, column=0, columnspan=3, pady=20)
        
        self.download_btn = ttk.Button(buttons_frame, text="⬇️ Descargar", 
                                     command=self.start_download, state=tk.DISABLED)
        self.download_btn.pack(side=tk.LEFT, padx=5)
        
        self.cancel_btn = ttk.Button(buttons_frame, text="❌ Cancelar", 
                                   command=self.cancel_download, state=tk.DISABLED)
        self.cancel_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(buttons_frame, text="ℹ️ Acerca de", command=self.show_about).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights for resizing
        main_frame.rowconfigure(3, weight=1)
        
    def analyze_url(self):
        """Analyze URL and populate file list"""
        url = self.url_var.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Por favor ingresa una URL")
            return
            
        if not URLUtils.is_valid_url(url):
            messagebox.showerror("Error", "URL inválida. Debe comenzar con http:// o https://")
            return
        
        # Clear current file list
        for item in self.files_tree.get_children():
            self.files_tree.delete(item)
        
        self.status_var.set("Analizando URL...")
        self.analyze_btn.config(state=tk.DISABLED)
        
        # Run analysis in separate thread
        def analyze_thread():
            try:
                # Configure downloader
                self.downloader.configure_downloads(
                    videos=self.videos_var.get(),
                    subtitles=self.subtitles_var.get(),
                    images=self.images_var.get(),
                    info=self.info_var.get()
                )
                
                files = self.downloader.get_file_list(url)
                
                # Update UI in main thread
                self.root.after(0, self.populate_file_list, files)
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Error al analizar URL: {e}"))
                self.root.after(0, lambda: self.status_var.set("Error al analizar"))
                self.root.after(0, lambda: self.analyze_btn.config(state=tk.NORMAL))
        
        threading.Thread(target=analyze_thread, daemon=True).start()
    
    def populate_file_list(self, files):
        """Populate the file list treeview"""
        self.analyze_btn.config(state=tk.NORMAL)
        
        if not files:
            self.status_var.set("No se encontraron archivos")
            self.download_btn.config(state=tk.DISABLED)
            return
        
        # Populate treeview
        for filename, file_url, file_type in files:
            # Get file info (this could be optimized to run in background)
            file_info = self.downloader.get_file_info(file_url)
            size_formatted = file_info.get('size_formatted', 'Desconocido')
            
            # Insert into treeview
            self.files_tree.insert('', tk.END, values=(filename, file_type.title(), size_formatted))
        
        self.status_var.set(f"Encontrados {len(files)} archivos")
        self.download_btn.config(state=tk.NORMAL)
        
        # Update download path suggestion
        folder_name = URLUtils.extract_folder_name(self.url_var.get())
        suggested_path = Path("./descarga") / folder_name
        self.download_path_var.set(str(suggested_path))
    
    def select_download_path(self):
        """Select download directory"""
        path = filedialog.askdirectory(initialdir=self.download_path_var.get())
        if path:
            self.download_path_var.set(path)
    
    def start_download(self):
        """Start the download process"""
        if self.is_downloading:
            return
        
        url = self.url_var.get().strip()
        download_path = Path(self.download_path_var.get())
        
        if not url:
            messagebox.showerror("Error", "No hay URL para descargar")
            return
        
        # Update UI state
        self.is_downloading = True
        self.download_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.analyze_btn.config(state=tk.DISABLED)
        
        # Configure downloader
        self.downloader.configure_downloads(
            videos=self.videos_var.get(),
            subtitles=self.subtitles_var.get(),
            images=self.images_var.get(),
            info=self.info_var.get()
        )
        
        # Start download thread
        def download_thread():
            try:
                def progress_callback(downloaded, total, filename):
                    if total > 0:
                        percent = (downloaded / total) * 100
                        self.root.after(0, lambda: self.progress_var.set(percent))
                        self.root.after(0, lambda: self.status_var.set(f"Descargando: {filename[:40]}..."))
                
                result = self.downloader.download_from_url(
                    url, 
                    download_path=download_path,
                    progress_callback=progress_callback
                )
                
                # Update UI with results
                self.root.after(0, self.download_completed, result)
                
            except Exception as e:
                error_result = {
                    'success': False,
                    'message': f'Error: {e}',
                    'completed': 0,
                    'failed': [str(e)],
                    'total': 0
                }
                self.root.after(0, self.download_completed, error_result)
        
        self.download_thread = threading.Thread(target=download_thread, daemon=True)
        self.download_thread.start()
    
    def download_completed(self, result):
        """Handle download completion"""
        self.is_downloading = False
        self.download_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
        self.analyze_btn.config(state=tk.NORMAL)
        self.progress_var.set(0)
        
        if result['success']:
            self.status_var.set(f"✅ Descarga completada: {result['completed']} archivos")
            messagebox.showinfo("Completado", 
                               f"Descarga completada exitosamente!\n"
                               f"Archivos descargados: {result['completed']}")
        else:
            self.status_var.set(f"❌ Error en descarga")
            messagebox.showerror("Error", result['message'])
    
    def cancel_download(self):
        """Cancel ongoing download"""
        if self.is_downloading and self.download_thread:
            # Note: This is a simple cancellation. For a more robust solution,
            # you'd need to implement proper cancellation in the download logic
            self.is_downloading = False
            self.status_var.set("Descarga cancelada")
            self.download_btn.config(state=tk.NORMAL)
            self.cancel_btn.config(state=tk.DISABLED)
            self.analyze_btn.config(state=tk.NORMAL)
            self.progress_var.set(0)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """🎬 UCVL Downloader

Un descargador de videos y subtítulos para visuales.ucv.cu

Características:
• Descarga de videos y subtítulos
• Interfaz gráfica y de línea de comandos
• Progreso en tiempo real
• Configuración de tipos de archivo

Versión: 1.0.0
"""
        messagebox.showinfo("Acerca de", about_text)
    
    def run(self):
        """Start the GUI"""
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
        # Start main loop
        self.root.mainloop()


def main():
    """Entry point for GUI interface"""
    try:
        gui = GUIInterface()
        gui.run()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
