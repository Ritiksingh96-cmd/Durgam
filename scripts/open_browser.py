"""
DURGAM Browser Launcher Helper
Polls the health endpoint and opens the browser only once the server is actively serving.
"""
import time
import urllib.request
import webbrowser

def launch_when_ready(url="http://127.0.0.1:8000/login.html", health_url="http://127.0.0.1:8000/health", timeout_secs=30):
    start = time.time()
    while time.time() - start < timeout_secs:
        try:
            with urllib.request.urlopen(health_url, timeout=1) as resp:
                if resp.status == 200:
                    webbrowser.open(url)
                    return True
        except Exception:
            time.sleep(0.5)
    # Fallback open after timeout
    webbrowser.open(url)
    return False

if __name__ == "__main__":
    launch_when_ready()
