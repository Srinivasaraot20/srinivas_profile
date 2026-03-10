#!/usr/bin/env python3
"""
Test script to verify the production-ready Flask application.
This script tests the application configuration and basic functionality.
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test that all modules can be imported."""
    try:
        from app import create_app
        from config import config
        from forms import ContactForm
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_app_creation():
    """Test that the app can be created with different configurations."""
    try:
        from app import create_app
        
        # Test development config
        dev_app = create_app('development')
        print("✓ Development app created successfully")
        
        # Test production config
        prod_app = create_app('production')
        print("✓ Production app created successfully")
        
        # Test default config
        default_app = create_app()
        print("✓ Default app created successfully")
        
        return True
    except Exception as e:
        print(f"✗ App creation error: {e}")
        return False

def test_config_paths():
    """Test that configuration paths are properly set."""
    try:
        from config import Config
        
        # Test that paths are Path objects
        assert isinstance(Config.BASE_DIR, Path)
        assert isinstance(Config.STATIC_FOLDER, Path)
        assert isinstance(Config.FILES_FOLDER, Path)
        
        # Test that paths exist
        assert Config.BASE_DIR.exists()
        assert Config.STATIC_FOLDER.exists()
        
        print("✓ Configuration paths are valid")
        return True
    except Exception as e:
        print(f"✗ Configuration path error: {e}")
        return False

def test_routes():
    """Test that all routes are properly registered."""
    try:
        from app import create_app
        
        app = create_app('testing')
        
        with app.test_client() as client:
            # Test main routes
            routes = ['/', '/about', '/projects', '/achievements', 
                     '/certifications', '/resume', '/gallery']
            
            for route in routes:
                response = client.get(route)
                assert response.status_code in [200, 302], f"Route {route} failed"
            
            print("✓ All routes are accessible")
            return True
    except Exception as e:
        print(f"✗ Route testing error: {e}")
        return False

def test_file_handling():
    """Test that file handling works without hardcoded paths."""
    try:
        from app import create_app
        from config import Config
        
        # Test that FILES_FOLDER is properly configured
        files_folder = Config.FILES_FOLDER
        assert files_folder.exists(), "Files folder should exist"
        
        # Test resume file path handling
        resume_filename = os.environ.get('RESUME_FILENAME', 'Srinivasa Rao Talari_Computer Programmer_20250513.docx')
        resume_path = files_folder / resume_filename
        
        print(f"✓ File handling configured correctly")
        print(f"  Files folder: {files_folder}")
        print(f"  Resume file: {resume_path} {'(exists)' if resume_path.exists() else '(missing)'}")
        
        return True
    except Exception as e:
        print(f"✗ File handling error: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing Production-Ready Flask Application")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_app_creation,
        test_config_paths,
        test_routes,
        test_file_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The application is production-ready.")
        return 0
    else:
        print("❌ Some tests failed. Please check the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
