#!/usr/bin/env python3
"""
Laddar ner Mulle Meck Bygger Bilar från mulle.dongers.net
Kör med: python3 ladda_ner_mulle.py
"""

import urllib.request
import urllib.parse
import os
import re
import sys
import time

BASE_URL = "http://mulle.dongers.net"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mulle-meck-lokal")

ROOT_FILES = [
    "index.html",
    "style.css",
    "phaser.min.js",
    "bundle.js",
    "loading.png",
]

DIRS_TO_MIRROR = ["assets", "data", "ui"]


def download_file(url, dest_path):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    if os.path.exists(dest_path):
        print(f"  Finns redan: {dest_path}")
        return True
    try:
        print(f"  ↓ {url}")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(dest_path, "wb") as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"  FEL: {url} — {e}")
        return False


def list_directory(url):
    """Hämta alla href-länkar från en Apache-kataloglistning."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        hrefs = re.findall(r'href="([^"?#]+)"', html)
        entries = []
        for h in hrefs:
            if h.startswith("/") or h.startswith("http") or h == "../":
                continue
            entries.append(h)
        return entries
    except Exception as e:
        print(f"  Kunde inte lista {url}: {e}")
        return []


def mirror_dir(remote_path, local_path):
    url = f"{BASE_URL}/{remote_path}/"
    entries = list_directory(url)
    for entry in entries:
        if entry.endswith("/"):
            # Undermapp
            mirror_dir(remote_path + "/" + entry.rstrip("/"),
                       os.path.join(local_path, entry.rstrip("/")))
        else:
            file_url = url + entry
            dest = os.path.join(local_path, entry)
            download_file(file_url, dest)
            time.sleep(0.05)  # Var snäll mot servern


def main():
    print(f"Skapar mappen: {OUTPUT_DIR}\n")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=== Rotnivåfiler ===")
    for f in ROOT_FILES:
        download_file(f"{BASE_URL}/{f}", os.path.join(OUTPUT_DIR, f))

    for d in DIRS_TO_MIRROR:
        print(f"\n=== Mapp: {d}/ ===")
        mirror_dir(d, os.path.join(OUTPUT_DIR, d))

    print("\n✓ Klart! Starta spelet med:")
    print(f"  cd '{OUTPUT_DIR}'")
    print("  python3 -m http.server 8000")
    print("Öppna sedan http://localhost:8000 i webbläsaren.")


if __name__ == "__main__":
    main()
