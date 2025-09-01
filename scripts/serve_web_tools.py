#!/usr/bin/env python3
"""
Simple web server to serve the Power BI web tools locally
Run this script and open http://localhost:8080 in your browser
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

def main():
    # Change to the web-import directory
    web_dir = Path(__file__).parent.parent / "powerbi" / "web-import"
    os.chdir(web_dir)
    
    PORT = 8080
    
    class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🚀 Bevco Dashboard Web Tools Server")
        print(f"📍 Serving at: http://localhost:{PORT}")
        print(f"📁 Directory: {web_dir}")
        print(f"\n🌐 Available Tools:")
        print(f"   • Implementation Guide: http://localhost:{PORT}/index.html")
        print(f"   • Online Converter: http://localhost:{PORT}/online-converter.html")
        print(f"\n💡 Press Ctrl+C to stop the server")
        
        # Try to open browser automatically
        try:
            webbrowser.open(f'http://localhost:{PORT}/index.html')
            print(f"🌍 Opening browser automatically...")
        except:
            print(f"🌍 Please open http://localhost:{PORT}/index.html in your browser")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n👋 Server stopped. Thanks for using Bevco Dashboard tools!")

if __name__ == "__main__":
    main()