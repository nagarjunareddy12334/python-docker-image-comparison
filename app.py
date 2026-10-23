
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import platform
import socket


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            response = {
                "status": "healthy",
                "application": "Python Docker Demo",
                "hostname": socket.gethostname(),
                "python_version": platform.python_version(),
                "base_image": os.getenv("BASE_IMAGE", "unknown")
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(
                b"Hello from the Python Docker application!"
            )

    def log_message(self, format, *args):
        print(f"{self.client_address[0]} - {format % args}")


server = HTTPServer(("0.0.0.0", 8000), AppHandler)
print("Application listening on port 8000", flush=True)
server.serve_forever()
