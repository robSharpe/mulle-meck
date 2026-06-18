#!/usr/bin/env python3
"""Flertrådig lokal webbserver för Mulle Meck Bygger Bilar."""
import http.server
import socketserver
import os
import sys

PORT = 8000

# Servera alltid från mulle-meck-lokal/ oavsett var skriptet körs från
script_dir = os.path.dirname(os.path.abspath(__file__))
game_dir = os.path.join(script_dir, "mulle-meck-lokal")

if not os.path.isdir(game_dir):
    print(f"Fel: hittade inte {game_dir}")
    print("Kör ladda_ner_mulle.py först.")
    sys.exit(1)

os.chdir(game_dir)


class ThreadedServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class Handler(http.server.SimpleHTTPRequestHandler):
    # Utöka basklassens MIME-tabell istället för att ersätta den, annars
    # serveras allt som inte räknas upp här som application/octet-stream.
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".js": "application/javascript",
        ".json": "application/json",
        ".png": "image/png",
        ".ogg": "audio/ogg",
        ".svg": "image/svg+xml",
    }

    def end_headers(self):
        # Tvinga omvalidering så patchade spelfiler (t.ex. bundle.js) slår
        # igenom direkt istället för att webbläsaren kör en gammal cachad version.
        # no-cache = validera mot servern varje gång; oförändrade filer ger
        # billiga 304-svar, ändrade filer hämtas på nytt.
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, format, *args):
        pass  # Tyst – ta bort för att se requests i terminalen


try:
    with ThreadedServer(("", PORT), Handler) as httpd:
        print(f"Servrar {game_dir}")
        print(f"http://localhost:{PORT}")
        httpd.serve_forever()
except OSError as e:
    if e.errno in (48, 98):  # Address already in use (macOS 48 / Linux 98)
        print(f"Fel: port {PORT} används redan av en annan process.")
        print(f"Stäng den (lsof -ti tcp:{PORT} | xargs kill) och försök igen.")
        sys.exit(1)
    raise
except KeyboardInterrupt:
    print("\nServern stoppad.")
