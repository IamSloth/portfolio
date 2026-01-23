import http.server
import socketserver
import os

PORT = 8080
FILE_TO_SAVE = "1_resume.html"

class EditorRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Save the file
            try:
                # Ensure we are writing text, assuming UTF-8
                content = post_data.decode('utf-8')
                with open(FILE_TO_SAVE, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"Saved successfully")
                print(f"Successfully saved {FILE_TO_SAVE}")
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
                print(f"Error saving file: {e}")
        else:
            self.send_error(404, "File not found")

    def end_headers(self):
        # Add CORS headers for good measure, though not strictly needed for same-origin
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == "__main__":
    # Change directory to the script's directory to serve files correctly
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), EditorRequestHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        print(f"Open http://localhost:{PORT}/{FILE_TO_SAVE} to edit")
        httpd.serve_forever()
