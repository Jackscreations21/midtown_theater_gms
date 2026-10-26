"""A tiny Chrome DevTools client (no packages) for timing the page when the Claude app's Browser pane is hidden (it then runs
NO frames at all — TRAPS, the slow-motion round). Start a headless Chrome on the page with its own profile:
  chrome --headless=new --remote-debugging-port=9333 --user-data-dir=<scratch>/prof --autoplay-policy=no-user-gesture-required
         --mute-audio http://localhost:8080/midtown.html
then  python -I tools/cdp-eval.py 9333 test.js   evaluates test.js in that page, awaiting its promise, and prints the result;
      python -I tools/cdp-eval.py 9333 shot.png  saves a screenshot.
Stop that Chrome by its command line (the port), never by image name: that closes Jack's own Chrome too."""
import base64, json, os, socket, struct, sys, urllib.request

port, jsfile = int(sys.argv[1]), sys.argv[2]
tabs = json.load(urllib.request.urlopen(f'http://127.0.0.1:{port}/json'))
page = next(t for t in tabs if t['type'] == 'page')
url = page['webSocketDebuggerUrl']
path = url.split(f':{port}', 1)[1]
s = socket.create_connection(('127.0.0.1', port))
key = base64.b64encode(os.urandom(16)).decode()
s.sendall((f'GET {path} HTTP/1.1\r\nHost: 127.0.0.1:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n'
           f'Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n').encode())
buf = b''
while b'\r\n\r\n' not in buf: buf += s.recv(4096)
rest = buf.split(b'\r\n\r\n', 1)[1]

def send(obj):
    data = json.dumps(obj).encode(); mask = os.urandom(4); n = len(data)
    hdr = bytes([0x81]) + (bytes([0x80 | n]) if n < 126 else bytes([0x80 | 126]) + struct.pack('>H', n) if n < 65536 else bytes([0x80 | 127]) + struct.pack('>Q', n))
    s.sendall(hdr + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))

def recv_exact(n):
    global rest
    while len(rest) < n:
        c = s.recv(65536)
        if not c: raise EOFError
        rest += c
    out, rest = rest[:n], rest[n:]
    return out

def recv():
    msg = b''
    while True:
        b0, b1 = recv_exact(2); n = b1 & 0x7f
        if n == 126: n = struct.unpack('>H', recv_exact(2))[0]
        elif n == 127: n = struct.unpack('>Q', recv_exact(8))[0]
        msg += recv_exact(n)
        if b0 & 0x80: return json.loads(msg)

if jsfile.endswith('.png'):
    send({'id': 1, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'}})
    while True:
        m = recv()
        if m.get('id') == 1: open(jsfile, 'wb').write(base64.b64decode(m['result']['data'])); print('saved'); sys.exit()
send({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': open(jsfile, encoding='utf-8').read(), 'awaitPromise': True, 'returnByValue': True, 'timeout': 600000}})
while True:
    m = recv()
    if m.get('id') == 1:
        r = m.get('result', {})
        print(json.dumps(r.get('result', {}).get('value', r), indent=1) if 'exceptionDetails' not in r else json.dumps(r['exceptionDetails'], indent=1)[:3000])
        break
