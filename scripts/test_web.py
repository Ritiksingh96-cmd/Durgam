import urllib.request

pages = [
    '/',
    '/index.html',
    '/login.html',
    '/citizen.html',
    '/bank.html',
    '/police.html',
    '/command.html',
    '/judiciary.html',
    '/verify.html',
    '/style.css',
    '/script.js',
    '/health'
]

for p in pages:
    try:
        url = 'http://127.0.0.1:8000' + p
        req = urllib.request.urlopen(url, timeout=3)
        print(f"{p:18} -> HTTP {req.status} (bytes: {len(req.read())})")
    except Exception as e:
        print(f"{p:18} -> ERROR: {e}")
