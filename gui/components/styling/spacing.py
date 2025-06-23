"""
Spacing System for UCLV Downloader GUI
"""


class SpacingSystem:
    """Centralized spacing management"""
    
    # Base spacing values
    XS = 4
    SM = 8
    MD = 12
    LG = 16
    XL = 20
    XXL = 24
    XXXL = 32
    
    @classmethod
    def get_spacing_dict(cls) -> dict:
        """Get all spacing values as a dictionary"""
        return {
            'xs': cls.XS,
            'sm': cls.SM,
            'md': cls.MD,
            'lg': cls.LG,
            'xl': cls.XL,
            'xxl': cls.XXL,
            'xxxl': cls.XXXL,
        }
    
    @classmethod
    def get_spacing(cls, name: str) -> int:
        """Get spacing by name"""
        spacing = cls.get_spacing_dict()
        return spacing.get(name, cls.MD)
    
    @classmethod
    def get_padding(cls, size: str) -> tuple:
        """Get padding tuple for tkinter"""
        value = cls.get_spacing(size)
        return (value, value)
    
    @classmethod
    def get_padding_x(cls, size: str) -> tuple:
        """Get horizontal padding tuple"""
        value = cls.get_spacing(size)
        return (value, 0)
    
    @classmethod
    def get_padding_y(cls, size: str) -> tuple:
        """Get vertical padding tuple"""
        value = cls.get_spacing(size)
        return (0, value) 