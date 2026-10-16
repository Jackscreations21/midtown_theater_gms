# Static server over the cues worktree, no-cache; /scratch/<f> serves the scratch helpers; POST /save/<name> writes into the dump folder.
import http.server, os, sys, functools
ROOT = sys.argv[1]; OUT = sys.argv[2]; PORT = int(sys.argv[3])
SCR = os.path.dirname(os.path.abspath(__file__))
class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store'); super().end_headers()
    def translate_path(self, path):
        p = path.split('?')[0]
        if p.startswith('/scratch/'):
            return os.path.join(SCR, os.path.basename(p))
        return super().translate_path(path)
    def do_POST(self):
        n = int(self.headers.get('Content-Length', 0)); body = self.rfile.read(n)
        name = os.path.basename(self.path.split('?')[0])
        if self.path.startswith('/save/') and name:
            with open(os.path.join(OUT, name), 'wb') as f: f.write(body)
            self.send_response(200); self.end_headers(); self.wfile.write(b'ok')
        else:
            self.send_response(404); self.end_headers()
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(('127.0.0.1', PORT), functools.partial(H, directory=ROOT)).serve_forever()
