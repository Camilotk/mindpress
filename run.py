import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

with open("config.json", encoding="utf-8") as f:
    config = json.load(f)

os.chdir(config.get("output_dir", "public"))
print(f"Servidor iniciado em http://localhost:8000")
HTTPServer(("localhost", 8000), SimpleHTTPRequestHandler).serve_forever()