"""
Main downloader class for UCLV Downloader - Simplified to use modular components
"""

# Import the new modular components  
from .downloaders import UCLVDownloader, DownloadProgress

# Backward compatibility - re-export main classes
__all__ = ['UCLVDownloader', 'DownloadProgress'] 