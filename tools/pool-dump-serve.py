#!/usr/bin/env python3
"""Serve the repository for the pool dump (tools/pool-dump.js), and keep what it sends.

    python -I tools/pool-dump-serve.py <OUT DIR> [--port 8105]

A static server over the repository root that never lets the browser cache (python's own http.server does, and an edited
assets/hamilton-show.json then is not the one the page reads - TRAPS), plus POST /save/<name>: the body is written to
<OUT DIR>/<name>.  Open http://localhost:<port>/midtown.html?cap=N (a fresh N after every edit), paste tools/pool-dump.js into the
console - or `eval(await (await fetch('/tools/pool-dump.js')).text())` - and run DUMPALL.  Standard library only.
"""
import functools, http.server, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Handler(http.server.SimpleHTTPRequestHandler):
    out = '.'

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store'); super().end_headers()

    def do_POST(self):
        body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        name = os.path.basename(self.path.split('?')[0])
        if not self.path.startswith('/save/') or not name:
            self.send_response(404); self.end_headers(); return
        with open(os.path.join(self.out, name), 'wb') as f: f.write(body)
        self.send_response(200); self.end_headers(); self.wfile.write(b'ok')

    def log_message(self, *a): pass


def main(argv):
    if not argv or argv[0].startswith('-'): print(__doc__); return 2
    out = argv[0]; os.makedirs(out, exist_ok=True)
    port = int(argv[argv.index('--port') + 1]) if '--port' in argv else 8105
    Handler.out = out
    print(f'serving {ROOT} on http://localhost:{port}/ - saving to {out}')
    http.server.ThreadingHTTPServer(('127.0.0.1', port), functools.partial(Handler, directory=ROOT)).serve_forever()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
