#!/usr/bin/env python3
"""
Mac Web Server for Bevco Dashboard Import
Serves the web-based import tool optimized for Mac users
"""

import http.server
import socketserver
import os
import webbrowser
import sys
from pathlib import Path

def main():
    # Change to the web-import directory
    web_dir = Path(__file__).parent.parent / "web-import"
    
    if not web_dir.exists():
        print("❌ Web import directory not found!")
        print(f"Expected: {web_dir}")
        return 1
    
    os.chdir(web_dir)
    
    PORT = 8080
    
    class MacHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            # Add CORS headers for better compatibility
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            # Add Mac-specific headers
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('X-Frame-Options', 'SAMEORIGIN')
            super().end_headers()
        
        def log_message(self, format, *args):
            # Custom logging for Mac
            print(f"🍎 {self.address_string()} - {format % args}")
    
    try:
        with socketserver.TCPServer(("", PORT), MacHTTPRequestHandler) as httpd:
            print("🍎 Bevco Dashboard - Mac Web Import Server")
            print("=" * 50)
            print(f"🌐 Server running at: http://localhost:{PORT}")
            print(f"📁 Serving from: {web_dir}")
            print()
            print("🚀 Features Available:")
            print("   • Generate sample data (36,400+ transactions)")
            print("   • Convert CSV files to Excel format")
            print("   • Step-by-step Power BI upload guide")
            print("   • Mac-optimized interface and shortcuts")
            print()
            print("💡 Mac Tips:")
            print("   • Use Safari for best performance")
            print("   • Files download to ~/Downloads by default")
            print("   • Use ⌘+Click for multi-file selection")
            print()
            print("🛑 Press Ctrl+C to stop the server")
            
            # Try to open browser automatically
            try:
                webbrowser.open(f'http://localhost:{PORT}')
                print(f"🌍 Opening in your default browser...")
            except Exception as e:
                print(f"🌍 Please open http://localhost:{PORT} in your browser")
                print(f"   (Auto-open failed: {e})")
            
            print()
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print(f"\n👋 Server stopped. Thanks for using Bevco Dashboard!")
                return 0
                
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {PORT} is already in use!")
            print("💡 Try closing other applications or use a different port")
            
            # Try alternative ports
            for alt_port in [8081, 8082, 8083, 3000, 5000]:
                try:
                    with socketserver.TCPServer(("", alt_port), MacHTTPRequestHandler) as httpd:
                        print(f"✅ Using alternative port: {alt_port}")
                        print(f"🌐 Server running at: http://localhost:{alt_port}")
                        webbrowser.open(f'http://localhost:{alt_port}')
                        httpd.serve_forever()
                        break
                except OSError:
                    continue
            else:
                print("❌ No available ports found. Please close other applications and try again.")
                return 1
        else:
            print(f"❌ Server error: {e}")
            return 1

if __name__ == "__main__":
    sys.exit(main())