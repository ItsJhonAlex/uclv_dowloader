"""
Build Cleaner component
"""

import os
import shutil
from pathlib import Path


class BuildCleaner:
    """Handles cleaning of build directories and files"""
    
    def __init__(self):
        self.dirs_to_clean = ['build', 'dist', '__pycache__']
        self.patterns_to_clean = ['*.spec']
    
    def clean_build(self):
        """Limpia directorios de build anteriores"""
        print("🧹 Limpiando archivos de build anteriores...")
        
        # Clean directories
        for dir_name in self.dirs_to_clean:
            if os.path.exists(dir_name):
                print(f"   🗑️  Eliminando {dir_name}/")
                shutil.rmtree(dir_name)
        
        # Clean spec files
        for pattern in self.patterns_to_clean:
            for file_path in Path('.').glob(pattern):
                print(f"   🗑️  Eliminando {file_path}")
                file_path.unlink()
        
        print("✅ Limpieza completada")
    
    def clean_temp_files(self):
        """Clean temporary files"""
        temp_patterns = ['*.pyc', '__pycache__', '.pytest_cache', '*.egg-info']
        
        for pattern in temp_patterns:
            for file_path in Path('.').rglob(pattern):
                if file_path.is_file():
                    file_path.unlink()
                elif file_path.is_dir():
                    shutil.rmtree(file_path)
    
    def get_cleanup_size(self) -> int:
        """Get size of files that would be cleaned"""
        total_size = 0
        
        for dir_name in self.dirs_to_clean:
            if os.path.exists(dir_name):
                for root, dirs, files in os.walk(dir_name):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if os.path.exists(file_path):
                            total_size += os.path.getsize(file_path)
        
        return total_size 