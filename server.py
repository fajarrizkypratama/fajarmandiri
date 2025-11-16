#!/usr/bin/env python3
"""
server.py - Headless entry point untuk Fajar Mandiri Store
Menjalankan app.py di server (Virtualmin/Webmin) tanpa GUI atau tray
"""

import os
import sys
import time
from pathlib import Path

# Pastikan import app.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from app import app, socketio, init_db
except ImportError as e:
    print(f"❌ Gagal import app.py: {e}")
    sys.exit(1)

# -------------------------------
# Environment dan setup
# -------------------------------
os.environ.setdefault("FLASK_SECRET_KEY", "server-dev-key-change")

BASE_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))

# Inisialisasi database jika ada
if callable(init_db):
    try:
        print("🔧 Initializing database...")
        init_db()
        print("✓ Database initialized")
    except Exception as e:
        print(f"⚠️ Database init error: {e}")

# -------------------------------
# Main server start
# -------------------------------
def main():
    port = int(os.environ.get("PORT", 5001))  # default 5001
    host = "0.0.0.0"  # agar bisa diakses remote

    print(f"🚀 Starting server at {host}:{port}")

    try:
        if socketio and hasattr(socketio, "run"):
            print("📡 Running with SocketIO")
            socketio.run(
                app,
                host=host,
                port=port,
                debug=False,
                use_reloader=False,
                allow_unsafe_werkzeug=True
            )
        else:
            print("📡 Running with Flask only")
            app.run(host=host, port=port, debug=False, use_reloader=False)

    except Exception as e:
        print(f"❌ Server failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
