#!/usr/bin/env python3
"""Job Pipeline Dashboard — local server.

Double-click dashboard.pyw (no console) or run:
  python scripts/dashboard_server.py
"""
import ctypes, http.server, json, os, signal, subprocess, urllib.parse, webbrowser

PORT = 8787
BASE = os.path.normpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def kill_existing():
    """Kill any existing server on our port."""
    try:
        out = subprocess.check_output(
            ["netstat", "-ano", "-p", "TCP"], text=True, creationflags=0x08000000
        )
        for line in out.splitlines():
            if f"127.0.0.1:{PORT}" in line and "LISTENING" in line:
                pid = int(line.strip().split()[-1])
                if pid != os.getpid():
                    os.kill(pid, signal.SIGTERM)
    except Exception:
        pass


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=BASE, **kw)

    def log_message(self, fmt, *args):
        pass  # silent

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if parsed.path == "/api/open":
            raw = params.get("path", [""])[0]
            full = os.path.normpath(os.path.join(BASE, raw))
            if not full.startswith(BASE):
                self._json(403, {"error": "forbidden"})
                return
            if os.path.isdir(full):
                # Alt-key trick: unlocks foreground window permission
                u32 = ctypes.windll.user32
                u32.keybd_event(0x12, 0, 0, 0)   # Alt down
                u32.keybd_event(0x12, 0, 2, 0)   # Alt up
                subprocess.Popen(["explorer", "/select,", full])
            elif os.path.isfile(full):
                os.startfile(full)
            else:
                self._json(404, {"error": "not found"})
                return
            self._json(200, {"ok": True})
            return

        if parsed.path == "/api/file":
            raw = params.get("path", [""])[0]
            full = os.path.normpath(os.path.join(BASE, raw))
            if not full.startswith(BASE) or not os.path.isfile(full):
                self._json(404, {"error": "not found"})
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            with open(full, encoding="utf-8") as f:
                self.wfile.write(f.read().encode())
            return

        if parsed.path == "/api/stop":
            self._json(200, {"ok": True, "msg": "stopping"})
            import threading
            threading.Thread(target=lambda: (self.server.shutdown()), daemon=True).start()
            return

        # Default: serve static files. Root → dashboard.html
        if parsed.path == "/":
            self.path = "/dashboard.html"
        super().do_GET()

    def _json(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())


if __name__ == "__main__":
    kill_existing()
    print(f"Dashboard → http://localhost:{PORT}")
    webbrowser.open(f"http://localhost:{PORT}")
    try:
        srv = http.server.HTTPServer(("127.0.0.1", PORT), Handler)
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
