#!/usr/bin/env python3
"""Local dev server matching vercel.json's routing exactly (redirects,
then filesystem, then rewrites — same order Vercel uses) — a plain
`python3 -m http.server` or `npx serve` from the repo root will NOT do
this, since vercel.json is Vercel-only and pages no longer live at the
repo root.

Usage: python3 scripts/dev-server.py [port]   (default port: 3000)
"""
import http.server
import json
import mimetypes
import re
import sys
import urllib.parse
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 3000

mimetypes.add_type("image/avif", ".avif")
mimetypes.add_type("font/otf", ".otf")
mimetypes.add_type("image/webp", ".webp")

CONFIG = json.loads((REPO / "vercel.json").read_text())

def compile_rules(rules):
    compiled = []
    for r in rules:
        # simple exact-path source only (this project's vercel.json uses no
        # path params in "source" — every route is enumerated explicitly)
        compiled.append((r["source"], r["destination"], r.get("permanent", False)))
    return compiled

REDIRECTS = compile_rules(CONFIG.get("redirects", []))
REWRITES = compile_rules(CONFIG.get("rewrites", []))

def resolve(path: str):
    # 1. redirects
    for source, destination, permanent in REDIRECTS:
        if path == source:
            return ("redirect", destination, permanent)
    # 2. literal static file at the exact path
    local = REPO / path.lstrip("/")
    if local.is_file():
        return ("file", local, None)
    # 3. rewrites
    for source, destination, _ in REWRITES:
        if path == source:
            dest_local = REPO / destination.lstrip("/")
            if dest_local.is_file():
                return ("file", dest_local, None)
    return None

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        path = urllib.parse.unquote(urllib.parse.urlparse(self.path).path)
        result = resolve(path)
        if result is None:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404 not found: " + path.encode())
            return
        kind, value, permanent = result
        if kind == "redirect":
            self.send_response(308 if permanent else 307)
            self.send_header("Location", value)
            self.end_headers()
            return
        f = value
        ctype, _ = mimetypes.guess_type(str(f))
        data = f.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype or "application/octet-stream")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} - {fmt % args}")

if __name__ == "__main__":
    server = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Serving steakfuel on http://localhost:{PORT}  (Ctrl+C to stop)")
    server.serve_forever()
