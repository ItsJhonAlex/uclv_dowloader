"""
Utility classes for UCLV Downloader
"""

import re
import urllib.parse
from pathlib import Path
from typing import Set


class URLUtils:
    """Utilities for URL manipulation and validation"""
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Validate if URL is properly formatted"""
        return url.startswith(('http://', 'https://'))
    
    @staticmethod
    def extract_folder_name(url: str) -> str:
        """Extract folder name from URL"""
        parsed = urllib.parse.urlparse(url)
        path_parts = [part for part in parsed.path.split('/') if part]
        
        if path_parts:
            # Decodificar URL encoding (como %20 por espacios)
            folder_name = urllib.parse.unquote(path_parts[-1])
            # Limpiar caracteres que no son válidos para nombres de carpeta
            folder_name = re.sub(r'[<>:"/\\|?*]', '_', folder_name)
            return folder_name
        
        return "descarga_ucvl"
    
    @staticmethod
    def build_full_url(base_url: str, href: str) -> str:
        """Build complete URL from base and relative href"""
        if href.startswith('http'):
            return href
        return urllib.parse.urljoin(base_url, href)


class FileUtils:
    """Utilities for file operations and validation"""
    
    # Extensiones soportadas
    VIDEO_EXTENSIONS: Set[str] = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'}
    SUBTITLE_EXTENSIONS: Set[str] = {'.srt', '.sub', '.vtt', '.ass', '.ssa'}
    IMAGE_EXTENSIONS: Set[str] = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    INFO_EXTENSIONS: Set[str] = {'.nfo', '.txt', '.info'}
    
    @classmethod
    def get_all_extensions(cls) -> Set[str]:
        """Get all supported file extensions"""
        return cls.VIDEO_EXTENSIONS | cls.SUBTITLE_EXTENSIONS | cls.IMAGE_EXTENSIONS | cls.INFO_EXTENSIONS
    
    @staticmethod
    def is_video_file(filename: str) -> bool:
        """Check if file is a video"""
        return Path(filename).suffix.lower() in FileUtils.VIDEO_EXTENSIONS
    
    @staticmethod
    def is_subtitle_file(filename: str) -> bool:
        """Check if file is a subtitle"""
        return Path(filename).suffix.lower() in FileUtils.SUBTITLE_EXTENSIONS
    
    @staticmethod
    def is_image_file(filename: str) -> bool:
        """Check if file is an image"""
        return Path(filename).suffix.lower() in FileUtils.IMAGE_EXTENSIONS
    
    @staticmethod
    def is_info_file(filename: str) -> bool:
        """Check if file is an info file"""
        return Path(filename).suffix.lower() in FileUtils.INFO_EXTENSIONS
    
    @staticmethod
    def get_file_type(filename: str) -> str:
        """Get file type category"""
        if FileUtils.is_video_file(filename):
            return "video"
        elif FileUtils.is_subtitle_file(filename):
            return "subtitle"
        elif FileUtils.is_image_file(filename):
            return "image"
        elif FileUtils.is_info_file(filename):
            return "info"
        else:
            return "other"
    
    @staticmethod
    def clean_filename(filename: str) -> str:
        """Clean filename for safe filesystem usage"""
        # Decodificar URL encoding
        filename = urllib.parse.unquote(filename)
        # Limpiar caracteres problemáticos
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        return filename
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        size = float(size_bytes)
        
        while size >= 1024.0 and i < len(size_names) - 1:
            size /= 1024.0
            i += 1
        
        return f"{size:.1f} {size_names[i]}" 