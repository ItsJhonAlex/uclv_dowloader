"""
Build Tester component
"""

import subprocess
from pathlib import Path


class BuildTester:
    """Handles testing of built executables"""
    
    def __init__(self, app_name: str = 'ucvl-downloader'):
        self.app_name = app_name
        self.exe_path = Path(f'dist/{app_name}')
    
    def test_executable(self) -> bool:
        """Prueba el ejecutable generado"""
        if not self.exe_path.exists():
            print("❌ No se encontró el ejecutable generado")
            return False
        
        print("🧪 Probando el ejecutable...")
        
        # Test 1: Basic execution with --version
        if not self._test_version():
            return False
        
        # Test 2: Help command
        if not self._test_help():
            return False
        
        print("✅ Ejecutable funciona correctamente!")
        return True
    
    def _test_version(self) -> bool:
        """Test --version command"""
        try:
            result = subprocess.run([str(self.exe_path), '--version'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print(f"   ✅ Versión: {result.stdout.strip()}")
                return True
            else:
                print(f"   ❌ Error en --version: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("   ⏰ Timeout al probar --version")
            return False
        except Exception as e:
            print(f"   ❌ Error al probar --version: {e}")
            return False
    
    def _test_help(self) -> bool:
        """Test --help command"""
        try:
            result = subprocess.run([str(self.exe_path), '--help'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("   ✅ Comando --help funciona")
                return True
            else:
                print(f"   ❌ Error en --help: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("   ⏰ Timeout al probar --help")
            return False
        except Exception as e:
            print(f"   ❌ Error al probar --help: {e}")
            return False
    
    def test_basic_import(self) -> bool:
        """Test basic Python import functionality"""
        try:
            # Test basic import by running a minimal command
            result = subprocess.run([str(self.exe_path), '--version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def get_test_summary(self) -> dict:
        """Get summary of test results"""
        tests = {
            'version_test': self._test_version(),
            'help_test': self._test_help(),
            'basic_import': self.test_basic_import()
        }
        
        passed = sum(tests.values())
        total = len(tests)
        
        return {
            'tests': tests,
            'passed': passed,
            'total': total,
            'success_rate': passed / total if total > 0 else 0,
            'all_passed': passed == total
        } 