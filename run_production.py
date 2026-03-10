#!/usr/bin/env python3
"""
Production deployment script for the portfolio application.
This script sets up the production environment and starts the server.
"""

import os
import sys
from pathlib import Path

def main():
    # Set environment variables for production
    os.environ.setdefault('FLASK_CONFIG', 'production')
    
    # Add current directory to Python path
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    # Import and create the app
    from app import create_app
    
    app = create_app('production')
    
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    print(f"Starting production server on port {port}")
    print("Press Ctrl+C to stop the server")
    
    try:
        # Use Gunicorn if available, otherwise use Flask's built-in server
        try:
            import gunicorn.app.base
            
            class StandaloneApplication(gunicorn.app.base.BaseApplication):
                def __init__(self, app, options=None):
                    self.options = options or {}
                    self.application = app
                    super().__init__()
                
                def load_config(self):
                    config = {key: value for key, value in self.options.items()
                            if key in self.cfg.settings and value is not None}
                    for key, value in config.items():
                        self.cfg.set(key.lower(), value)
                
                def load(self):
                    return self.application
            
            options = {
                'bind': f'0.0.0.0:{port}',
                'workers': 4,
                'worker_class': 'sync',
                'worker_connections': 1000,
                'timeout': 30,
                'keepalive': 2,
                'max_requests': 1000,
                'max_requests_jitter': 100,
                'preload_app': True,
            }
            
            StandaloneApplication(app, options).run()
            
        except ImportError:
            print("Gunicorn not found, using Flask development server")
            print("For production, install gunicorn: pip install gunicorn")
            app.run(host='0.0.0.0', port=port)
            
    except KeyboardInterrupt:
        print("\nServer stopped")

if __name__ == '__main__':
    main()
