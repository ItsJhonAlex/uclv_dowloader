"""
Simplified Modern Styles for UCLV Downloader GUI
Backward compatibility wrapper for the refactored styling system
"""

import tkinter as tk
from tkinter import ttk
from .colors import ColorPalette
from .fonts import FontSystem
from .spacing import SpacingSystem
from .theme import ThemeManager


class ModernStyles:
    """Simplified modern styling system with backward compatibility"""
    
    _theme_manager = None
    _colors = ColorPalette()
    _fonts = FontSystem()
    _spacing = SpacingSystem()
    
    @classmethod
    def setup_theme(cls, root: tk.Tk) -> ttk.Style:
        """Setup modern theme for the application"""
        if cls._theme_manager is None:
            cls._theme_manager = ThemeManager()
        
        return cls._theme_manager.setup_theme(root)
    
    @classmethod
    def get_color(cls, name: str) -> str:
        """Get color by name"""
        return cls._colors.get_color(name)
    
    @classmethod
    def get_font(cls, name: str) -> tuple:
        """Get font by name"""
        return cls._fonts.get_font(name)
    
    @classmethod
    def get_spacing(cls, name: str) -> int:
        """Get spacing by name"""
        return cls._spacing.get_spacing(name)
    
    # Backward compatibility properties
    @classmethod
    def get_colors_dict(cls) -> dict:
        """Get all colors (backward compatibility)"""
        return cls._colors.get_colors_dict()
    
    @classmethod
    def get_fonts_dict(cls) -> dict:
        """Get all fonts (backward compatibility)"""
        return cls._fonts.get_fonts_dict()
    
    @classmethod
    def get_spacing_dict(cls) -> dict:
        """Get all spacing values (backward compatibility)"""
        return cls._spacing.get_spacing_dict()
    
    # Legacy constants for backward compatibility
    COLORS = property(lambda self: self._colors.get_colors_dict())
    FONTS = property(lambda self: self._fonts.get_fonts_dict())
    SPACING = property(lambda self: self._spacing.get_spacing_dict()) 