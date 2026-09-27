"""
DURGAM Static Asset Sync Script
Copies all frontend assets (HTML, CSS, JS, images) from the project root
into backend/app/static for production serving via FastAPI.
Run this before starting the server or after modifying frontend files.
"""
import os
import shutil
import sys

ROOT_DIR   = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(ROOT_DIR, "backend", "app", "static")

os.makedirs(STATIC_DIR, exist_ok=True)

# ── 1. Copy root-level frontend files ──────────────────────────────────────
COPY_EXTENSIONS = ('.html', '.css', '.js')
copied = 0
skipped = 0

for fname in os.listdir(ROOT_DIR):
    if not fname.endswith(COPY_EXTENSIONS):
        continue
    src = os.path.join(ROOT_DIR, fname)
    dst = os.path.join(STATIC_DIR, fname)
    if os.path.isfile(src):
        shutil.copy2(src, dst)
        print(f"  [SYNC] {fname}")
        copied += 1

# ── 2. Copy images/ directory ───────────────────────────────────────────────
root_images = os.path.join(ROOT_DIR, "images")
static_images = os.path.join(STATIC_DIR, "images")
if os.path.isdir(root_images):
    os.makedirs(static_images, exist_ok=True)
    for fname in os.listdir(root_images):
        src = os.path.join(root_images, fname)
        dst = os.path.join(static_images, fname)
        if os.path.isfile(src):
            shutil.copy2(src, dst)
            print(f"  [SYNC] images/{fname}")
            copied += 1
    print(f"  [OK] images/ directory synced")
else:
    print(f"  [SKIP] images/ directory not found (optional)")

# ── 3. Copy manifest.json / sw.js / robots.txt if they exist ───────────────
for extra_file in ("manifest.json", "sw.js", "robots.txt", "favicon.ico"):
    src = os.path.join(ROOT_DIR, extra_file)
    if os.path.isfile(src):
        shutil.copy2(src, os.path.join(STATIC_DIR, extra_file))
        print(f"  [SYNC] {extra_file}")
        copied += 1

print(f"\n[OK] Static sync complete -- {copied} file(s) synchronized to backend/app/static/")
