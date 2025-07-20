#!/usr/bin/env python3
"""
Test script to validate the installation and dependencies
"""

import sys
import subprocess
import importlib

def test_python_version():
    """Test if Python version is compatible"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 6:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} is too old. Need Python 3.6+")
        return False

def test_system_commands():
    """Test if required system commands are available"""
    commands = ['showmount']
    all_good = True
    
    for cmd in commands:
        try:
            result = subprocess.run(['which', cmd], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ {cmd} command is available")
            else:
                print(f"✗ {cmd} command not found. Install nfs-common package.")
                all_good = False
        except Exception as e:
            print(f"✗ Error checking {cmd}: {e}")
            all_good = False
    
    return all_good

def test_python_packages():
    """Test if required Python packages are installed"""
    packages = [
        ('smb.SMBConnection', 'pysmb'),
        ('csv', 'built-in'),
        ('socket', 'built-in'),
        ('datetime', 'built-in'),
        ('pathlib', 'built-in'),
        ('getpass', 'built-in'),
        ('ipaddress', 'built-in')
    ]
    
    all_good = True
    
    for module_name, package_name in packages:
        try:
            importlib.import_module(module_name.split('.')[0])
            print(f"✓ {module_name} ({package_name}) is available")
        except ImportError:
            print(f"✗ {module_name} ({package_name}) is not available")
            all_good = False
    
    return all_good

def main():
    """Run all tests"""
    print("=== NAS Share Lister Installation Test ===\n")
    
    tests = [
        ("Python Version", test_python_version),
        ("System Commands", test_system_commands),
        ("Python Packages", test_python_packages)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"Testing {test_name}:")
        result = test_func()
        all_passed = all_passed and result
        print()
    
    if all_passed:
        print("🎉 All tests passed! The NAS Share Lister should work correctly.")
        print("Run './run.sh' or 'python3 nas_share_lister.py' to start the tool.")
    else:
        print("⚠️  Some tests failed. Please install missing dependencies.")
        print("Run './setup.sh' to install required packages.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
