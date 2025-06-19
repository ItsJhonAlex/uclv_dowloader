"""
Modern styles and theming for UCLV Downloader GUI
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any


class ModernStyles:
    """Modern styling system for the GUI"""
    
    # Color palette
    COLORS = {
        # Primary colors
        'primary': '#2563eb',      # Blue
        'primary_dark': '#1d4ed8',
        'primary_light': '#3b82f6',
        
        # Secondary colors  
        'secondary': '#64748b',    # Slate
        'secondary_dark': '#475569',
        'secondary_light': '#94a3b8',
        
        # Accent colors
        'accent': '#10b981',       # Green
        'accent_dark': '#059669',
        'warning': '#f59e0b',      # Amber
        'error': '#ef4444',        # Red
        'success': '#22c55e',      # Green
        
        # Background colors
        'bg_primary': '#ffffff',   # White
        'bg_secondary': '#f8fafc', # Light gray
        'bg_card': '#ffffff',      # Card background
        'bg_hover': '#f1f5f9',     # Hover state
        
        # Text colors
        'text_primary': '#1e293b',   # Dark slate
        'text_secondary': '#64748b', # Medium slate  
        'text_muted': '#94a3b8',     # Light slate
        'text_inverse': '#ffffff',   # White
        
        # Border colors
        'border': '#e2e8f0',       # Light border
        'border_focus': '#3b82f6', # Focus border
        'border_error': '#ef4444',  # Error border
    }
    
    # Typography
    FONTS = {
        'title': ('Segoe UI', 20, 'bold'),
        'subtitle': ('Segoe UI', 16, 'bold'),
        'heading': ('Segoe UI', 14, 'bold'),
        'body': ('Segoe UI', 10, 'normal'),
        'body_bold': ('Segoe UI', 10, 'bold'),
        'caption': ('Segoe UI', 9, 'normal'),
        'monospace': ('Consolas', 10, 'normal'),
    }
    
    # Spacing
    SPACING = {
        'xs': 4,
        'sm': 8,
        'md': 12,
        'lg': 16,
        'xl': 20,
        'xxl': 24,
        'xxxl': 32,
    }
    
    # Component specific styles
    COMPONENTS = {
        'card': {
            'relief': 'flat',
            'borderwidth': 1,
            'background': COLORS['bg_card'],
        },
        'button_primary': {
            'background': COLORS['primary'],
            'foreground': COLORS['text_inverse'],
            'font': FONTS['body_bold'],
        },
        'button_secondary': {
            'background': COLORS['bg_secondary'],
            'foreground': COLORS['text_primary'],
            'font': FONTS['body'],
        },
        'entry': {
            'fieldbackground': COLORS['bg_primary'],
            'borderwidth': 1,
            'focuscolor': COLORS['border_focus'],
        }
    }
    
    @classmethod
    def setup_theme(cls, root: tk.Tk) -> ttk.Style:
        """Setup modern theme for the application"""
        style = ttk.Style()
        
        # Use clam as base theme
        style.theme_use('clam')
        
        # Configure general styles
        cls._configure_general_styles(style)
        cls._configure_button_styles(style)
        cls._configure_frame_styles(style)
        cls._configure_entry_styles(style)
        cls._configure_label_styles(style)
        cls._configure_treeview_styles(style)
        cls._configure_progressbar_styles(style)
        cls._configure_checkbutton_styles(style)
        
        return style
    
    @classmethod
    def _configure_general_styles(cls, style: ttk.Style):
        """Configure general application styles"""
        style.configure('TLabel', 
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body'])
        
        style.configure('TFrame',
                       background=cls.COLORS['bg_primary'],
                       relief='flat')
        
    @classmethod
    def _configure_button_styles(cls, style: ttk.Style):
        """Configure button styles"""
        # Primary button
        style.configure('Primary.TButton',
                       background=cls.COLORS['primary'],
                       foreground=cls.COLORS['text_inverse'],
                       font=cls.FONTS['body_bold'],
                       padding=(cls.SPACING['md'], cls.SPACING['sm']),
                       relief='flat')
        
        style.map('Primary.TButton',
                 background=[('active', cls.COLORS['primary_dark']),
                           ('pressed', cls.COLORS['primary_dark'])])
        
        # Secondary button
        style.configure('Secondary.TButton',
                       background=cls.COLORS['bg_secondary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body'],
                       padding=(cls.SPACING['md'], cls.SPACING['sm']),
                       relief='flat')
        
        style.map('Secondary.TButton',
                 background=[('active', cls.COLORS['bg_hover']),
                           ('pressed', cls.COLORS['bg_hover'])])
        
        # Success button
        style.configure('Success.TButton',
                       background=cls.COLORS['success'],
                       foreground=cls.COLORS['text_inverse'],
                       font=cls.FONTS['body_bold'],
                       padding=(cls.SPACING['md'], cls.SPACING['sm']),
                       relief='flat')
        
        # Warning button  
        style.configure('Warning.TButton',
                       background=cls.COLORS['warning'],
                       foreground=cls.COLORS['text_inverse'],
                       font=cls.FONTS['body_bold'],
                       padding=(cls.SPACING['md'], cls.SPACING['sm']),
                       relief='flat')
        
        # Error button
        style.configure('Error.TButton',
                       background=cls.COLORS['error'],
                       foreground=cls.COLORS['text_inverse'],
                       font=cls.FONTS['body_bold'],
                       padding=(cls.SPACING['md'], cls.SPACING['sm']),
                       relief='flat')
    
    @classmethod
    def _configure_frame_styles(cls, style: ttk.Style):
        """Configure frame styles"""
        # Card frame
        style.configure('Card.TFrame',
                       background=cls.COLORS['bg_card'],
                       relief='solid',
                       borderwidth=1)
        
        # Section frame
        style.configure('Section.TLabelframe',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['heading'],
                       relief='flat',
                       borderwidth=1)
        
        style.configure('Section.TLabelframe.Label',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['heading'])
    
    @classmethod
    def _configure_entry_styles(cls, style: ttk.Style):
        """Configure entry styles"""
        style.configure('Modern.TEntry',
                       fieldbackground=cls.COLORS['bg_primary'],
                       borderwidth=1,
                       relief='solid',
                       font=cls.FONTS['body'],
                       padding=cls.SPACING['sm'])
        
        style.map('Modern.TEntry',
                 focuscolor=[('!focus', cls.COLORS['border']),
                           ('focus', cls.COLORS['border_focus'])],
                 bordercolor=[('!focus', cls.COLORS['border']),
                            ('focus', cls.COLORS['border_focus'])])
    
    @classmethod
    def _configure_label_styles(cls, style: ttk.Style):
        """Configure label styles"""
        # Title labels
        style.configure('Title.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['title'])
        
        # Subtitle labels  
        style.configure('Subtitle.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['subtitle'])
        
        # Heading labels
        style.configure('Heading.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['heading'])
        
        # Caption labels
        style.configure('Caption.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_secondary'],
                       font=cls.FONTS['caption'])
        
        # Status labels
        style.configure('Status.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_secondary'],
                       font=cls.FONTS['body'])
        
        # Success status
        style.configure('Success.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['success'],
                       font=cls.FONTS['body_bold'])
        
        # Error status
        style.configure('Error.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['error'],
                       font=cls.FONTS['body_bold'])
    
    @classmethod
    def _configure_treeview_styles(cls, style: ttk.Style):
        """Configure treeview styles"""
        style.configure('Modern.Treeview',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body'],
                       fieldbackground=cls.COLORS['bg_primary'],
                       borderwidth=1,
                       relief='solid')
        
        style.configure('Modern.Treeview.Heading',
                       background=cls.COLORS['bg_secondary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body_bold'],
                       relief='flat')
        
        style.map('Modern.Treeview',
                 background=[('selected', cls.COLORS['primary_light'])],
                 foreground=[('selected', cls.COLORS['text_inverse'])])
    
    @classmethod
    def _configure_progressbar_styles(cls, style: ttk.Style):
        """Configure progressbar styles"""
        style.configure('Modern.Horizontal.TProgressbar',
                       background=cls.COLORS['primary'],
                       troughcolor=cls.COLORS['bg_secondary'],
                       borderwidth=0,
                       lightcolor=cls.COLORS['primary'],
                       darkcolor=cls.COLORS['primary'])
    
    @classmethod
    def _configure_checkbutton_styles(cls, style: ttk.Style):
        """Configure checkbutton styles"""
        style.configure('Modern.TCheckbutton',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body'],
                       focuscolor='none')
        
        style.map('Modern.TCheckbutton',
                 background=[('active', cls.COLORS['bg_hover'])])
    
    @classmethod
    def get_color(cls, name: str) -> str:
        """Get color by name"""
        return cls.COLORS.get(name, cls.COLORS['text_primary'])
    
    @classmethod
    def get_font(cls, name: str) -> tuple:
        """Get font by name"""
        return cls.FONTS.get(name, cls.FONTS['body'])
    
    @classmethod
    def get_spacing(cls, name: str) -> int:
        """Get spacing by name"""
        return cls.SPACING.get(name, cls.SPACING['md']) 