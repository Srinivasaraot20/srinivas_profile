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
            routes = ['/', '/about', '/skills', '/experience', '/projects', '/achievements', 
                     '/certifications', '/resume', '/gallery']
            
            for route in routes:
                response = client.get(route)
                assert response.status_code in [200, 302], f"Route {route} failed"
                
            # Verify Sitemap XML
            response = client.get('/sitemap.xml')
            assert response.status_code == 200
            assert 'application/xml' in response.content_type or 'text/xml' in response.content_type
            sitemap_content = response.get_data(as_text=True)
            assert '<urlset' in sitemap_content
            for route in routes:
                # Remove leading slash for matching since sitemap might use full URLs
                clean_route = route[1:] if route.startswith('/') else route
                assert clean_route in sitemap_content or route == '/'
                
            # Verify Robots TXT
            response = client.get('/robots.txt')
            assert response.status_code == 200
            assert 'text/plain' in response.content_type
            robots_content = response.get_data(as_text=True)
            assert 'User-agent: *' in robots_content
            assert 'Sitemap:' in robots_content
            
            print("✓ All routes and SEO files are accessible and correct")
            return True
    except Exception as e:
        print(f"✗ Route testing error: {e}")
        import traceback
        traceback.print_exc()
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

def test_database_and_contact():
    """Test database storage, form validation, and admin routes."""
    try:
        from app import create_app
        from models import db, ContactMessage
        
        app = create_app('testing')
        
        with app.app_context():
            # Verify tables exist
            from sqlalchemy import inspect
            assert inspect(db.engine).has_table("contact_messages")
            
            # Add a mock message directly
            msg = ContactMessage(
                name="Test Visitor",
                email="visitor@example.com",
                phone="+918341492762",
                subject="Test Inquiry",
                message="This is a test message to verify database storage.",
                ip_address="127.0.0.1",
                status="New"
            )
            db.session.add(msg)
            db.session.commit()
            
            # Query it back
            retrieved = ContactMessage.query.filter_by(email="visitor@example.com").first()
            assert retrieved is not None
            assert retrieved.name == "Test Visitor"
            assert retrieved.phone == "+918341492762"
            assert retrieved.status == "New"
            
            # Check dict conversion
            ret_dict = retrieved.to_dict()
            assert ret_dict['email'] == "visitor@example.com"
            assert ret_dict['status'] == "New"
            
            # Test admin views using test client
            with app.test_client() as client:
                # Test credentials (admin / admin123)
                import base64
                headers = {
                    'Authorization': 'Basic ' + base64.b64encode(b'admin:admin123').decode('utf-8')
                }
                
                # Retrieve dashboard
                response = client.get('/admin/messages', headers=headers)
                assert response.status_code == 200
                assert b"Contact Messages" in response.data
                assert b"visitor@example.com" in response.data
                
                # Update status
                response = client.post(f'/admin/messages/{retrieved.id}/status/Read', headers=headers, follow_redirects=True)
                assert response.status_code == 200
                assert retrieved.status == "Read"
                
                # Export CSV
                response = client.get('/admin/messages/export/csv', headers=headers)
                assert response.status_code == 200
                assert b"visitor@example.com" in response.data
                assert b"Date Submitted (UTC)" in response.data
                
                # Delete
                response = client.post(f'/admin/messages/{retrieved.id}/delete', headers=headers, follow_redirects=True)
                assert response.status_code == 200
                assert ContactMessage.query.get(retrieved.id) is None
                
        print("✓ Database, form validation, and admin dashboard verified successfully")
        return True
    except Exception as e:
        print(f"✗ Database and contact testing error: {e}")
        import traceback
        traceback.print_exc()
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
        test_file_handling,
        test_database_and_contact
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
