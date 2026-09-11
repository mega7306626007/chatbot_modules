"""Small standard-library web bridge for the browser interface."""

import json
import mimetypes
import os
import threading
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse


WEB_HOST = os.environ.get("HOST", "0.0.0.0")
WEB_PORT = int(os.environ.get("PORT", "8765"))
WEB_FILES = {
    "/": "index.html",
    "/index.html": "index.html",
    "/styles.css": "styles.css",
    "/app.js": "app.js",
    "/manifest.json": "manifest.json",
    "/sw.js": "sw.js",
    "/favicon.ico": "favicon.ico",
    "/favicon-16x16.png": "favicon-16x16.png",
    "/favicon-32x32.png": "favicon-32x32.png",
    "/favicon-180x180.png": "favicon-180x180.png",
    "/favicon-192x192.png": "favicon-192x192.png",
    "/favicon-512x512.png": "favicon-512x512.png",
    "/logo-full-512.png": "logo-full-512.png",
}
GENERATED_DIR = Path(__file__).resolve().parent / "generated_images"


def run_web_server():
    """Serve the web UI and route chat messages through the real ChatBot.

    The ChatBot is built on a background thread as the server starts
    (it can spend tens of seconds training/caching models on a fresh
    deploy). The HTTP server itself is thread-based, so the static web
    UI and the health-check path respond immediately while the bot is
    still warming up, and /api/chat returns a clean 503 JSON error
    rather than hanging until the upstream proxy gives up and the
    browser reports an HTTP 502 empty response.
    """
    bot = None
    bot_error = None
    bot_ready = threading.Event()
    # The ChatBot owns one SQLite connection (and a lot of in-memory
    # state), designed for single-client use. Access is serialized with
    # this lock so concurrent /api/chat requests can't interleave reads
    # and writes through the same connection.
    bot_lock = threading.Lock()

    def build_bot():
        nonlocal bot, bot_error
        try:
            bot = ChatBot()
        except Exception as exc:  # pragma: no cover - defensive
            bot_error = exc
            import traceback
            traceback.print_exc()
        finally:
            bot_ready.set()

    def get_bot():
        if not bot_ready.is_set():
            raise RuntimeError("chatbot is still starting up")
        if bot_error is not None:
            raise bot_error
        return bot

    threading.Thread(target=build_bot, daemon=True).start()

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
            if path.startswith("/generated_images/"):
                image_name = Path(path.removeprefix("/generated_images/")).name
                image_path = GENERATED_DIR / image_name
                if image_path.parent != GENERATED_DIR or image_path.suffix.lower() not in (".png", ".jpg", ".jpeg"):
                    self._send(404, "Not found", "text/plain; charset=utf-8")
                    return
                try:
                    mime = "image/jpeg" if image_path.suffix.lower() in (".jpg", ".jpeg") else "image/png"
                    self._send(200, image_path.read_bytes(), mime)
                except OSError:
                    self._send(404, "Image not found", "text/plain; charset=utf-8")
                return
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
                try:
                    chatbot = get_bot()
                except RuntimeError:
                    self._send(
                        503,
                        json.dumps({"error": "The chatbot is still starting up. Please try again in a moment."}),
                        "application/json; charset=utf-8",
                    )
                    return
                with bot_lock:
                    before_image_files = set(GENERATED_DIR.glob("*.png")) | set(GENERATED_DIR.glob("*.jpg")) | set(GENERATED_DIR.glob("*.jpeg"))
                    chatbot.logger.log("user", message.strip())
                    reply = chatbot.respond(message.strip())
                    chatbot.logger.log("bot", reply)
                    after_image_files = set(GENERATED_DIR.glob("*.png")) | set(GENERATED_DIR.glob("*.jpg")) | set(GENERATED_DIR.glob("*.jpeg"))
                    new_image_files = after_image_files - before_image_files
                    image_url = None
                    if new_image_files:
                        image_url = "/generated_images/" + max(new_image_files, key=lambda path: path.stat().st_mtime_ns).name
                response = {"reply": reply, "bot_name": chatbot.bot_name()}
                if image_url:
                    response["image_url"] = image_url
                self._send(200, json.dumps(response), "application/json; charset=utf-8")
            except (ValueError, TypeError, json.JSONDecodeError) as error:
                self._send(400, json.dumps({"error": str(error)}), "application/json; charset=utf-8")
            except Exception as error:
                import traceback
                traceback.print_exc()
                self._send(500, json.dumps({"error": f"The chatbot could not process that message: {error}"}), "application/json; charset=utf-8")

        def log_message(self, format_string, *args):
            print(f"[web] {self.address_string()} - {format_string % args}")

    server = ThreadingHTTPServer((WEB_HOST, WEB_PORT), WebHandler)
    print(f"PyChat web interface: http://{WEB_HOST}:{WEB_PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping web interface...")
    finally:
        server.server_close()
        if bot_ready.is_set() and bot is not None:
            bot.memory.save()
            bot.logger.flush_to_disk()