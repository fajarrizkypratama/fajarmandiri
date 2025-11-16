#!/usr/bin/env python3
"""
Fajar Mandiri Store - Wedding Invitation & CV Generator
Server entry point optimized for Ubuntu server / Virtualmin
"""

import os
import sys
from datetime import datetime

# Tambahkan folder project ke sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Set secret key (untuk Flask)
os.environ.setdefault('FLASK_SECRET_KEY', 'dev-secret-key-change-in-prod')

# Import Flask app & SocketIO
try:
    from app import app, socketio, init_db, USER_DOCS
    print("✓ Successfully imported Flask app and SocketIO")
except ImportError as e:
    print(f"❌ Error importing app components: {e}")
    sys.exit(1)

# -------------------------------
# Setup environment & directories
# -------------------------------
def setup_environment():
    """Setup folders and initialize database"""
    try:
        print("🔧 Initializing database...")
        init_db()
        print("✓ Database initialized")
    except Exception as e:
        print(f"❌ Database init error: {e}")

    directories = [
        USER_DOCS,
        os.path.join(USER_DOCS, 'cv_templates'),
        os.path.join(USER_DOCS, 'wedding_templates'),
        os.path.join(USER_DOCS, 'music'),
        os.path.join(USER_DOCS, 'prewedding_photos'),
        os.path.join(USER_DOCS, 'thumbnails'),
        os.path.join(BASE_DIR, 'static/images'),
        os.path.join(BASE_DIR, 'static/images/templates'),
        os.path.join(BASE_DIR, 'static/images/wedding_templates')
    ]

    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
        except Exception as e:
            print(f"⚠️  Could not create directory {directory}: {e}")

    print("✓ Directory structure ready")

# -------------------------------
# Main server entry point
# -------------------------------
def main():
    print("🌸 Starting Fajar Mandiri Store")
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Setup environment
    setup_environment()

    # Gunakan port default 5000 (bisa override dari environment)
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'

    print(f"🚀 Server running on {host}:{port}")

    try:
        # Jalankan server dengan SocketIO jika tersedia
        if hasattr(socketio, 'run') and callable(socketio.run):
            print("📡 Using SocketIO")
            socketio.run(
                app,
                host=host,
                port=port,
                debug=False,
                use_reloader=False,
                allow_unsafe_werkzeug=True
            )
        else:
            print("📡 Using Flask only")
            app.run(host=host, port=port, debug=False, use_reloader=False)
    except Exception as e:
        print(f"❌ Server startup error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
