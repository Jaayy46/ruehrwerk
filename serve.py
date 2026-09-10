#!/usr/bin/env python3
"""Rührwerk lokal starten:  python3 serve.py  ->  http://localhost:8777"""
import os, sys, http.server

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8777
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with http.server.HTTPServer(('', PORT), http.server.SimpleHTTPRequestHandler) as s:
    print(f'Rührwerk läuft auf http://localhost:{PORT}  (Strg+C zum Beenden)')
    s.serve_forever()
