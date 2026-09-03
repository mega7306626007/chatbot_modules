"""Small standard-library web bridge for the browser interface."""

import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse


WEB_HOST = os.environ.get("HOST", "0.0.0.0")
WEB_PORT = int(os.environ.get("PORT", "8765"))
WEB_FILES = {"/": "index.html", "/index.html": "index.html", "/styles.css": "styles.css", "/app.js": "app.js"}


def run_web_server():
    """Serve the web UI and route chat messages through the real ChatBot."""
    bot = None

    def get_bot():
        nonlocal bot
        if bot is None:
            bot = ChatBot()
        return bot

    class WebHandler(BaseHTTPRequestHandler):
        def _send(self, status, body, content_type):
            payload = body.encode("utf-8") if isinstance(body, str) else body
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(payload)

        def do_OPTIONS(self):
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Content-Length", "0")
            self.end_headers()

        def do_GET(self):
            path = urlparse(self.path).path
            filename = WEB_FILES.get(path)
            if filename is None:
                self._send(404, "Not found", "text/plain; charset=utf-8")
                return
            try:
                with open(filename, "rb") as file_handle:
                    content = file_handle.read()
            except OSError:
                self._send(404, "Web file is missing", "text/plain; charset=utf-8")
                return
            content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
            self._send(200, content, f"{content_type}; charset=utf-8")

        def do_POST(self):
            if urlparse(self.path).path != "/api/chat":
                self._send(404, "Not found", "text/plain; charset=utf-8")
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length > 32_000:
                    raise ValueError("Message is too large")
                payload = json.loads(self.rfile.read(length))
                message = payload.get("message", "")
                if not isinstance(message, str) or not message.strip():
                    raise ValueError("A non-empty message is required")
                chatbot = get_bot()
                chatbot.logger.log("user", message.strip())
                reply = chatbot.respond(message.strip())
                chatbot.logger.log("bot", reply)
                self._send(200, json.dumps({"reply": reply, "bot_name": chatbot.bot_name()}), "application/json; charset=utf-8")
            except (ValueError, TypeError, json.JSONDecodeError) as error:
                self._send(400, json.dumps({"error": str(error)}), "application/json; charset=utf-8")
            except Exception:
                self._send(500, json.dumps({"error": "The chatbot could not process that message."}), "application/json; charset=utf-8")

        def log_message(self, format_string, *args):
            print(f"[web] {self.address_string()} - {format_string % args}")

    server = HTTPServer((WEB_HOST, WEB_PORT), WebHandler)
    print(f"PyChat web interface: http://{WEB_HOST}:{WEB_PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping web interface...")
    finally:
        server.server_close()
        if bot is not None:
            bot.memory.save()
            bot.logger.flush_to_disk()