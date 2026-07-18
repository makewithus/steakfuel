#!/usr/bin/env python3
"""Local dev server for the static site, matching vercel.json's routing
exactly (so http://localhost:PORT/ behaves the same as the real Vercel
deploy) — a plain `python3 -m http.server` or `npx serve` from the repo
root will NOT do this, since vercel.json rewrites are Vercel-only and
index.html/pages no longer live at the repo root.

Usage: python3 scripts/dev-server.py [port]   (default port: 3000)
"""
import http.server
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

REWRITES = [
    (re.compile(r"^/$"), "/pages/index.html"),
    (re.compile(r"^/launch-list$"), "/pages/launch-list.html"),
    (re.compile(r"^/([^/]+)\.html$"), "/pages/{0}.html"),
    (re.compile(r"^/admin/([^/]+)\.html$"), "/pages/admin/{0}.html"),
    (re.compile(r"^/blog-article/([^/]+)\.html$"), "/pages/blog-article/{0}.html"),
    (re.compile(r"^/category/([^/]+)\.html$"), "/pages/category/{0}.html"),
    (re.compile(r"^/product/([^/]+)\.html$"), "/pages/product/{0}.html"),
]

def resolve(path: str):
    # Vercel serves a literal static file at the exact path before
    # consulting rewrites (this is what keeps /404.html working).
    local = REPO / path.lstrip("/")
    if local.is_file():
        return local
    for pattern, template in REWRITES:
        m = pattern.match(path)
        if m:
            dest_local = REPO / template.format(*m.groups()).lstrip("/")
            if dest_local.is_file():
                return dest_local
    return None

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        path = urllib.parse.unquote(urllib.parse.urlparse(self.path).path)
        f = resolve(path)
        if f is None:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404 not found: " + path.encode())
            return
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
