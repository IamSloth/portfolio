"""Double-click to launch dashboard (no console window)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
# .pyw = pythonw.exe = no black console
exec(open(os.path.join(os.path.dirname(__file__), "dashboard_server.py"), encoding="utf-8").read())
