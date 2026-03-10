#!/usr/bin/env python3
"""
Static Site Generator for Flask Portfolio
Converts Flask application to static HTML files for Netlify deployment
"""

import os
import shutil
from datetime import datetime
from flask import Flask
from app import create_app

def generate_static_site():
    """Generate static HTML files from Flask application"""
    print("🚀 Generating static site for Netlify deployment...")
    
    # Create Flask app with test configuration
    app = create_app('development')
    
    # Set secret key for CSRF (required for form generation)
    app.config['SECRET_KEY'] = 'static-generator-secret-key'
    
    with app.app_context():
        # Clean and create build directory
        build_dir = 'build'
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)
        os.makedirs(build_dir)
        
        # Copy static files
        print("📁 Copying static files...")
        if os.path.exists('static'):
            shutil.copytree('static', os.path.join(build_dir, 'static'))
        
        # Generate HTML files for all routes
        routes = [
            ('/', 'index.html'),
            ('/about', 'about.html'),
            ('/projects', 'projects.html'),
            ('/achievements', 'achievements.html'),
            ('/certifications', 'certifications.html'),
            ('/resume', 'resume.html'),
            ('/gallery', 'gallery.html')
        ]
        
        # Handle contact page separately (use static version)
        print("📄 Generating HTML files...")
        for route, filename in routes:
            try:
                with app.test_client() as client:
                    response = client.get(route)
                    if response.status_code == 200:
                        filepath = os.path.join(build_dir, filename)
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(response.get_data(as_text=True))
                        print(f"   ✅ Generated {filename}")
                    else:
                        print(f"   ❌ Failed to generate {filename} (Status: {response.status_code})")
            except Exception as e:
                print(f"   ⚠️  Error generating {filename}: {e}")
                # Create a basic error page
                error_content = f"""<!DOCTYPE html>
<html>
<head><title>{filename} - Generation Error</title></head>
<body>
    <h1>Page Generation Failed</h1>
    <p>Could not generate {filename} from route {route}</p>
    <p>Error: {e}</p>
</body>
</html>"""
                filepath = os.path.join(build_dir, filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(error_content)
                print(f"   🔄 Created error page for {filename}")
        
        # Generate static contact page
        print("📄 Generating static contact page...")
        try:
            with app.app_context():
                from flask import render_template
                contact_html = render_template('contact_static.html')
                with open(os.path.join(build_dir, 'contact.html'), 'w', encoding='utf-8') as f:
                    f.write(contact_html)
                print("   ✅ Generated contact.html (Netlify Forms version)")
        except Exception as e:
            print(f"   ⚠️  Could not generate contact_static.html: {e}")
            print("   🔄 Using original contact page instead...")
            # Fallback to original contact page
            with app.test_client() as client:
                response = client.get('/contact')
                if response.status_code == 200:
                    with open(os.path.join(build_dir, 'contact.html'), 'w', encoding='utf-8') as f:
                        f.write(response.get_data(as_text=True))
                    print("   ✅ Generated contact.html (original version)")
        
        # Create error pages
        print("📄 Generating error pages...")
        for error_code, filename in [(404, '404.html'), (500, '500.html')]:
            with app.test_client() as client:
                response = client.get(f'/error/{error_code}', follow_redirects=True)
                if response.status_code == 200:
                    filepath = os.path.join(build_dir, filename)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(response.get_data(as_text=True))
                    print(f"   ✅ Generated {filename}")
        
        # Create _redirects file for Netlify
        print("🔧 Creating Netlify configuration...")
        redirects_content = """# Netlify redirects
/api/* /.netlify/functions/:splat 200
/contact /.netlify/functions/contact 200
/subscribe /.netlify/functions/subscribe 200
/download-resume /static/files/Srinivasa_Rao_Talari_Resume.docx 200

# SPA fallback (if needed)
/* /index.html 200
"""
        
        with open(os.path.join(build_dir, '_redirects'), 'w') as f:
            f.write(redirects_content)
        
        # Create netlify.toml
        netlify_toml = """[build]
  publish = "build"
  command = "python static_generator.py"

[build.environment]
  PYTHON_VERSION = "3.11"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"

[[headers]]
  for = "/static/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
"""
        
        with open('netlify.toml', 'w') as f:
            f.write(netlify_toml)
        
        print(f"\n🎉 Static site generated successfully!")
        print(f"📂 Build directory: {build_dir}")
        print(f"🌐 Ready for Netlify deployment!")
        print(f"\n📝 Next steps:")
        print(f"   1. Run: python static_generator.py")
        print(f"   2. Upload 'build' folder to Netlify")
        print(f"   3. Set build command: python static_generator.py")
        print(f"   4. Set publish directory: build")

if __name__ == '__main__':
    generate_static_site()
