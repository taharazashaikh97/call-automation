from __future__ import annotations

import http.server
import socketserver
from pathlib import Path

PORT = 8000
HOST = "0.0.0.0"


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    handler = http.server.SimpleHTTPRequestHandler

    with ReusableTCPServer((HOST, PORT), handler) as httpd:
        print(f"Serving Call Automation AI website from {repo_root}")
        print(f"Open: http://localhost:{PORT}/")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
