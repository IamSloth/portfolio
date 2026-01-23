import http.server
import socketserver
import os
import urllib.parse

PORT = 8080
ALLOWED_FILES = ["1_resume.html", "2_essay_free.html", "3_essay_required.html"]

class EditorRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == '/save':
            # Parse query parameters
            query_params = urllib.parse.parse_qs(parsed_path.query)
            filename = query_params.get('file', [ALLOWED_FILES[0]])[0]
            
            # Security check: only allow saving specific files in current directory
            if filename not in ALLOWED_FILES:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"Forbidden: Cannot save to this file")
                print(f"Attempted to save unauthorized file: {filename}")
                return

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Save the file
            try:
                # Ensure we are writing text, assuming UTF-8
                content = post_data.decode('utf-8')
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"Saved {filename} successfully".encode('utf-8'))
                print(f"Successfully saved {filename}")
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
                print(f"Error saving file: {e}")
        else:
            self.send_error(404, "File not found")

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Allow address reuse to prevent "Address already in use" errors on quick restarts
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), EditorRequestHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        print("Available files:")
        for f in ALLOWED_FILES:
            print(f" - http://localhost:{PORT}/{f}")
        httpd.serve_forever()
