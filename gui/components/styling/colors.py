"""
Color Palette for UCLV Downloader GUI
"""


class ColorPalette:
    """Centralized color palette management"""
    
    # Primary colors
    PRIMARY = '#2563eb'      # Blue
    PRIMARY_DARK = '#1d4ed8'
    PRIMARY_LIGHT = '#3b82f6'
    
    # Secondary colors  
    SECONDARY = '#64748b'    # Slate
    SECONDARY_DARK = '#475569'
    SECONDARY_LIGHT = '#94a3b8'
    
    # Accent colors
    ACCENT = '#10b981'       # Green
    ACCENT_DARK = '#059669'
    WARNING = '#f59e0b'      # Amber
    ERROR = '#ef4444'        # Red
    SUCCESS = '#22c55e'      # Green
    
    # Background colors
    BG_PRIMARY = '#ffffff'   # White
    BG_SECONDARY = '#f8fafc' # Light gray
    BG_CARD = '#ffffff'      # Card background
    BG_HOVER = '#f1f5f9'     # Hover state
    
    # Text colors
    TEXT_PRIMARY = '#1e293b'   # Dark slate
    TEXT_SECONDARY = '#64748b' # Medium slate  
    TEXT_MUTED = '#94a3b8'     # Light slate
    TEXT_INVERSE = '#ffffff'   # White
    
    # Border colors
    BORDER = '#e2e8f0'       # Light border
    BORDER_FOCUS = '#3b82f6' # Focus border
    BORDER_ERROR = '#ef4444'  # Error border
    
    @classmethod
    def get_colors_dict(cls) -> dict:
        """Get all colors as a dictionary"""
        return {
            # Primary colors
            'primary': cls.PRIMARY,
            'primary_dark': cls.PRIMARY_DARK,
            'primary_light': cls.PRIMARY_LIGHT,
            
            # Secondary colors  
            'secondary': cls.SECONDARY,
            'secondary_dark': cls.SECONDARY_DARK,
            'secondary_light': cls.SECONDARY_LIGHT,
            
            # Accent colors
            'accent': cls.ACCENT,
            'accent_dark': cls.ACCENT_DARK,
            'warning': cls.WARNING,
            'error': cls.ERROR,
            'success': cls.SUCCESS,
            
            # Background colors
            'bg_primary': cls.BG_PRIMARY,
            'bg_secondary': cls.BG_SECONDARY,
            'bg_card': cls.BG_CARD,
            'bg_hover': cls.BG_HOVER,
            
            # Text colors
            'text_primary': cls.TEXT_PRIMARY,
            'text_secondary': cls.TEXT_SECONDARY,
            'text_muted': cls.TEXT_MUTED,
            'text_inverse': cls.TEXT_INVERSE,
            
            # Border colors
            'border': cls.BORDER,
            'border_focus': cls.BORDER_FOCUS,
            'border_error': cls.BORDER_ERROR,
        }
    
    @classmethod
    def get_color(cls, name: str) -> str:
        """Get color by name"""
        colors = cls.get_colors_dict()
        return colors.get(name, cls.TEXT_PRIMARY) 