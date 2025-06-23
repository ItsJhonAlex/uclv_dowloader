"""
Scroll Manager - Handles scrollable container functionality
"""

import tkinter as tk
from tkinter import ttk
from ..components import ModernStyles


class ScrollManager:
    """Manages scrollable container for GUI components"""
    
    def __init__(self, parent_widget):
        self.parent = parent_widget
        self.canvas = None
        self.v_scrollbar = None
        self.scrollable_frame = None
        self.canvas_frame = None
        self.main_container = None
        
    def create_scrollable_container(self):
        """Create a scrollable container for all components"""
        # Main container frame (fills the window)
        self.main_container = ttk.Frame(self.parent)
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
        
        return self.scrollable_frame
    
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
    
    def update_scroll_region(self):
        """Update the scroll region to encompass all widgets"""
        if self.canvas:
            self.canvas.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all")) 