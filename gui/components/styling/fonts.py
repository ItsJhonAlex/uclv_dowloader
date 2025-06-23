"""
Font System for UCLV Downloader GUI
"""


class FontSystem:
    """Centralized font management"""
    
    # Base font family
    FONT_FAMILY = 'Segoe UI'
    MONOSPACE_FAMILY = 'Consolas'
    
    # Font sizes
    SIZE_TITLE = 20
    SIZE_SUBTITLE = 16
    SIZE_HEADING = 14
    SIZE_BODY = 10
    SIZE_CAPTION = 9
    
    # Font weights
    WEIGHT_NORMAL = 'normal'
    WEIGHT_BOLD = 'bold'
    
    @classmethod
    def get_fonts_dict(cls) -> dict:
        """Get all fonts as a dictionary"""
        return {
            'title': (cls.FONT_FAMILY, cls.SIZE_TITLE, cls.WEIGHT_BOLD),
            'subtitle': (cls.FONT_FAMILY, cls.SIZE_SUBTITLE, cls.WEIGHT_BOLD),
            'heading': (cls.FONT_FAMILY, cls.SIZE_HEADING, cls.WEIGHT_BOLD),
            'body': (cls.FONT_FAMILY, cls.SIZE_BODY, cls.WEIGHT_NORMAL),
            'body_bold': (cls.FONT_FAMILY, cls.SIZE_BODY, cls.WEIGHT_BOLD),
            'caption': (cls.FONT_FAMILY, cls.SIZE_CAPTION, cls.WEIGHT_NORMAL),
            'monospace': (cls.MONOSPACE_FAMILY, cls.SIZE_BODY, cls.WEIGHT_NORMAL),
        }
    
    @classmethod
    def get_font(cls, name: str) -> tuple:
        """Get font by name"""
        fonts = cls.get_fonts_dict()
        return fonts.get(name, fonts['body'])
    
    @classmethod
    def create_font(cls, family: str = None, size: int = None, weight: str = None) -> tuple:
        """Create custom font tuple"""
        return (
            family or cls.FONT_FAMILY,
            size or cls.SIZE_BODY,
            weight or cls.WEIGHT_NORMAL
        ) 