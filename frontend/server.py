from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen, build_opener, HTTPCookieProcessor
from http.cookiejar import CookieJar
import json
import mimetypes
import os

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
BACKEND = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")

# Maintain a persistent session with the backend so cookies are preserved across requests.
_backend_session = build_opener(HTTPCookieProcessor(CookieJar()))


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/backendapi/session":
            self._proxy("/api/session")
            return
        if self.path == "/backendapi/validate":
            self._proxy("/api/validate")
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_GET(self):
        if self.path.startswith("/backendapi/"):
            self.send_error(HTTPStatus.METHOD_NOT_ALLOWED)
            return
        self._serve_static()

    def _proxy(self, backend_path: str):
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length) if length else b""
        headers = {"Content-Type": self.headers.get("Content-Type", "application/json"), "Accept": "application/json"}

        request = Request(
            BACKEND + backend_path,
            data=body if body else None,
            headers=headers,
            method="POST",
        )

        try:
            with _backend_session.open(request) as response:
                payload = response.read()
                self.send_response(response.status)
                for key, value in response.headers.items():
                    if key.lower() in {"content-length", "transfer-encoding", "connection"}:
                        continue
                    if key.lower() == "set-cookie":
                        self.send_header(key, value)
                self.send_header("Content-Type", response.headers.get_content_type())
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
        except HTTPError as error:
            payload = error.read()
            self.send_response(error.code)
            self.send_header("Content-Type", error.headers.get_content_type() if error.headers else "application/json")
            self.send_header("Content-Length", str(len(payload)))
            if error.headers:
                cookie = error.headers.get("Set-Cookie")
                if cookie:
                    self.send_header("Set-Cookie", cookie)
            self.end_headers()
            self.wfile.write(payload)
        except URLError:
            body = json.dumps({"detail": "bad gateway"}).encode()
            self.send_response(HTTPStatus.BAD_GATEWAY)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    def _serve_static(self):
        path = self.path.split("?", 1)[0]
        if path == "/":
            path = "/index.html"
        file_path = DIST / path.lstrip("/")
        if file_path.is_dir():
            file_path = file_path / "index.html"
        if not file_path.exists():
            file_path = DIST / "index.html"
        if not file_path.exists():
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        content = file_path.read_bytes()
        mime = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "4321"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()
