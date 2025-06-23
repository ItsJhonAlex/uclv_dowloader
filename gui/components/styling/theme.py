"""
Theme Management for UCLV Downloader GUI
"""

import tkinter as tk
from tkinter import ttk
from .colors import ColorPalette
from .fonts import FontSystem
from .spacing import SpacingSystem


class ThemeManager:
    """Advanced theme management with style configuration"""
    
    def __init__(self):
        self.colors = ColorPalette()
        self.fonts = FontSystem()
        self.spacing = SpacingSystem()
    
    def setup_theme(self, root: tk.Tk) -> ttk.Style:
        """Setup modern theme for the application"""
        style = ttk.Style()
        
        # Use clam as base theme
        style.theme_use('clam')
        
        # Configure all component styles
        self._configure_general_styles(style)
        self._configure_button_styles(style)
        self._configure_frame_styles(style)
        self._configure_entry_styles(style)
        self._configure_label_styles(style)
        self._configure_treeview_styles(style)
        self._configure_progressbar_styles(style)
        self._configure_checkbutton_styles(style)
        self._configure_radiobutton_styles(style)
        
        return style
    
    def _configure_general_styles(self, style: ttk.Style):
        """Configure general application styles"""
        style.configure('TLabel', 
                       background=self.colors.BG_PRIMARY,
                       foreground=self.colors.TEXT_PRIMARY,
                       font=self.fonts.get_font('body'))
        
        style.configure('TFrame',
                       background=self.colors.BG_PRIMARY,
                       relief='flat')
    
    def _configure_button_styles(self, style: ttk.Style):
        """Configure button styles"""
        # Primary button
        style.configure('Primary.TButton',
                       background=self.colors.PRIMARY,
                       foreground=self.colors.TEXT_INVERSE,
                       font=self.fonts.get_font('body_bold'),
                       padding=self.spacing.get_padding('md'),
                       relief='flat')
        
        style.map('Primary.TButton',
                 background=[('active', self.colors.PRIMARY_DARK),
                           ('pressed', self.colors.PRIMARY_DARK)])
        
        # Secondary button
        style.configure('Secondary.TButton',
                       background=self.colors.BG_SECONDARY,
                       foreground=self.colors.TEXT_PRIMARY,
                       font=self.fonts.get_font('body'),
                       padding=self.spacing.get_padding('md'),
                       relief='flat')
        
        style.map('Secondary.TButton',
                 background=[('active', self.colors.BG_HOVER),
                           ('pressed', self.colors.BG_HOVER)])
        
        # Status buttons
        for button_type, color in [
            ('Success', self.colors.SUCCESS),
            ('Warning', self.colors.WARNING),
            ('Error', self.colors.ERROR)
        ]:
            style.configure(f'{button_type}.TButton',
                           background=color,
                           foreground=self.colors.TEXT_INVERSE,
                           font=self.fonts.get_font('body_bold'),
                           padding=self.spacing.get_padding('md'),
                           relief='flat')
    
    def _configure_frame_styles(self, style: ttk.Style):
        """Configure frame styles"""
        # Card frame
        style.configure('Card.TFrame',
                       background=self.colors.BG_CARD,
                       relief='solid',
                       borderwidth=1)
        
        # Section frame
        style.configure('Section.TLabelframe',
                       background=self.colors.BG_PRIMARY,
                       foreground=self.colors.TEXT_PRIMARY,
                       font=self.fonts.get_font('heading'),
                       relief='flat',
                       borderwidth=1)
        
        style.configure('Section.TLabelframe.Label',
                       background=self.colors.BG_PRIMARY,
                       foreground=self.colors.TEXT_PRIMARY,
                       font=self.fonts.get_font('heading'))
    
    def _configure_entry_styles(self, style: ttk.Style):
        """Configure entry styles"""
        style.configure('Modern.TEntry',
                       fieldbackground=self.colors.BG_PRIMARY,
                       borderwidth=1,
                       relief='solid',
                       font=self.fonts.get_font('body'),
                       padding=self.spacing.get_spacing('sm'))
        
        style.map('Modern.TEntry',
                 focuscolor=[('!focus', self.colors.BORDER),
                           ('focus', self.colors.BORDER_FOCUS)],
                 bordercolor=[('!focus', self.colors.BORDER),
                            ('focus', self.colors.BORDER_FOCUS)])
    
    def _configure_label_styles(self, style: ttk.Style):
        """Configure label styles"""
        label_configs = [
            ('Title', 'title', self.colors.TEXT_PRIMARY),
            ('Subtitle', 'subtitle', self.colors.TEXT_PRIMARY),
            ('Heading', 'heading', self.colors.TEXT_PRIMARY),
            ('Caption', 'caption', self.colors.TEXT_SECONDARY),
            ('Status', 'body', self.colors.TEXT_SECONDARY),
            ('Success', 'body_bold', self.colors.SUCCESS),
            ('Error', 'body_bold', self.colors.ERROR),
        ]
        
        for label_type, font_name, color in label_configs:
            style.configure(f'{label_type}.TLabel',
                           background=self.colors.BG_PRIMARY,
                           foreground=color,
                           font=self.fonts.get_font(font_name))
    
    def _configure_treeview_styles(self, style: ttk.Style):
        """Configure treeview styles"""
        style.configure('Modern.Treeview',
                       background=self.colors.BG_PRIMARY,
                       foreground=self.colors.TEXT_PRIMARY,
                       font=self.fonts.get_font('body'),
                       fieldbackground=self.colors.BG_PRIMARY,
                       borderwidth=1,
                       relief='solid')
        
        style.configure('Modern.Treeview.Heading',
                       background=self.colors.BG_SECONDARY,
                       foreground=self.colors.TEXT_PRIMARY,
                       font=self.fonts.get_font('body_bold'),
                       relief='flat')
        
        style.map('Modern.Treeview',
                 background=[('selected', self.colors.PRIMARY_LIGHT)],
                 foreground=[('selected', self.colors.TEXT_INVERSE)])
    
    def _configure_progressbar_styles(self, style: ttk.Style):
        """Configure progressbar styles"""
        style.configure('Modern.Horizontal.TProgressbar',
                       background=self.colors.PRIMARY,
                       troughcolor=self.colors.BG_SECONDARY,
                       borderwidth=0,
                       lightcolor=self.colors.PRIMARY,
                       darkcolor=self.colors.PRIMARY)
    
    def _configure_checkbutton_styles(self, style: ttk.Style):
        """Configure checkbutton styles"""
        style.configure('Modern.TCheckbutton',
                       background=self.colors.BG_PRIMARY,
                       foreground=self.colors.TEXT_PRIMARY,
                       font=self.fonts.get_font('body'),
                       focuscolor='none')
        
        style.map('Modern.TCheckbutton',
                 background=[('active', self.colors.BG_HOVER)])
    
    def _configure_radiobutton_styles(self, style: ttk.Style):
        """Configure radiobutton styles"""
        style.configure('Modern.TRadiobutton',
                       background=self.colors.BG_PRIMARY,
                       foreground=self.colors.TEXT_PRIMARY,
                       font=self.fonts.get_font('body'),
                       focuscolor='none')
        
        style.map('Modern.TRadiobutton',
                 background=[('active', self.colors.BG_HOVER)]) 