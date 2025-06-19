"""
GUI module for UCLV Downloader

This module provides modern graphical user interface components and main interface.
Uses modular component architecture for better maintainability and design.
"""

from .interface import ModernGUIInterface, main
from .components import (
    HeaderComponent,
    URLInputComponent,
    FileTypeComponent, 
    FileListComponent,
    DownloadControlsComponent,
    ProgressComponent,
    ModernStyles
)

# Backward compatibility alias
GUIInterface = ModernGUIInterface

__all__ = [
    'ModernGUIInterface',
    'GUIInterface',  # For backward compatibility
    'main',
    'HeaderComponent',
    'URLInputComponent',
    'FileTypeComponent',
    'FileListComponent', 
    'DownloadControlsComponent',
    'ProgressComponent',
    'ModernStyles'
]
