"""JanSahayak low-bandwidth chatbot server.

Run:
    python app.py --port 8011

Endpoints:
    GET  /                  Lightweight web chatbot
    POST /api/chat          JSON chat API
    GET  /api/schemes       Grounded scheme catalogue
    GET  /api/checklist     Download/checklist text for a session + scheme
    POST /webhook/sms       Twilio-compatible SMS webhook
    POST /webhook/whatsapp  Twilio WhatsApp Sandbox-compatible webhook
    POST /webhook/ivr       TwiML voice/DTMF webhook
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import secrets
import sys
import urllib.parse
from html import escape
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.chatbot import WelfareChatbot, load_catalogue, render_checklist  # noqa: E402
from src.i18n import t  # noqa: E402


BOT = WelfareChatbot()
STATIC_DIR = ROOT / "static"


def make_session_id(prefix: str = "web") -> str:
    return f"{prefix}-{secrets.token_hex(8)}"


def parse_body(handler: BaseHTTPRequestHandler) -> tuple[dict, str]:
    length = int(handler.headers.get("content-length", "0"))
    raw = handler.rfile.read(length).decode("utf-8") if length else ""
    content_type = handler.headers.get("content-type", "")
    if "application/json" in content_type:
        return json.loads(raw or "{}"), raw
    parsed = urllib.parse.parse_qs(raw, keep_blank_values=True)
    return {key: values[0] if values else "" for key, values in parsed.items()}, raw


def twiml_message(text: str) -> str:
    return f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{escape(text)}</Message></Response>'


def twiml_voice(text: str, gather: bool = True) -> str:
    safe = escape(text)
    if gather:
        return (
            '<?xml version="1.0" encoding="UTF-8"?><Response>'
            '<Gather input="speech dtmf" timeout="5" language="hi-IN" action="/webhook/ivr" method="POST">'
            f"<Say language=\"hi-IN\">{safe}</Say>"
            "</Gather>"
            f"<Say language=\"hi-IN\">{safe}</Say>"
            "</Response>"
        )
    return f'<?xml version="1.0" encoding="UTF-8"?><Response><Say language="hi-IN">{safe}</Say></Response>'


class Handler(BaseHTTPRequestHandler):
    server_version = "JanSahayak/1.0"

    def log_message(self, fmt: str, *args) -> None:
        print("%s - - [%s] %s" % (self.client_address[0], self.log_date_time_string(), fmt % args))

    def _send(self, body: bytes | str, status: int = 200, content_type: str = "text/plain; charset=utf-8") -> None:
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "content-type")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, payload: dict, status: int = 200) -> None:
        self._send(json.dumps(payload, ensure_ascii=False), status, "application/json; charset=utf-8")

    def do_OPTIONS(self) -> None:
        self._send("", HTTPStatus.NO_CONTENT)

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path == "/health":
            self._send_json({"ok": True, "service": "JanSahayak"})
            return
        if path == "/api/schemes":
            self._send_json(load_catalogue())
            return
        if path == "/api/checklist":
            query = urllib.parse.parse_qs(parsed.query)
            session_id = query.get("session_id", [""])[0]
            scheme_id = query.get("scheme", [""])[0]
            lang = query.get("lang", [""])[0]
            session = BOT.sessions.get(session_id)
            if session and not lang:
                lang = session.lang or "en"
            scheme = next((item for item in BOT.schemes if item["id"] == scheme_id), None)
            if not scheme:
                self._send("Scheme not found", HTTPStatus.NOT_FOUND)
                return
            text = render_checklist(scheme, lang or "en")
            filename = f"{scheme_id}_checklist_{lang or 'en'}.txt"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            encoded = text.encode("utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(encoded)
            return
        self.serve_static(path)

    def serve_static(self, path: str) -> None:
        if path in {"", "/"}:
            file_path = STATIC_DIR / "index.html"
        else:
            safe_path = Path(urllib.parse.unquote(path.lstrip("/")))
            file_path = (STATIC_DIR / safe_path).resolve()
            if STATIC_DIR.resolve() not in file_path.parents and file_path != STATIC_DIR.resolve():
                self._send("Forbidden", HTTPStatus.FORBIDDEN)
                return
        if not file_path.exists() or not file_path.is_file():
            self._send("Not found", HTTPStatus.NOT_FOUND)
            return
        content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
        self._send(file_path.read_bytes(), 200, content_type)

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        try:
            payload, _raw = parse_body(self)
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON"}, HTTPStatus.BAD_REQUEST)
            return

        if parsed.path == "/api/chat":
            session_id = payload.get("session_id") or make_session_id("web")
            text = payload.get("message") or payload.get("text") or ""
            channel = payload.get("channel") or "web"
            result = BOT.chat(session_id, text, channel=channel)
            result["lang"] = BOT.sessions.get(session_id).lang if session_id in BOT.sessions else None
            self._send_json(result)
            return

        if parsed.path in {"/webhook/sms", "/webhook/whatsapp"}:
            sender = payload.get("From") or payload.get("WaId") or make_session_id("phone")
            text = payload.get("Body") or payload.get("body") or ""
            channel = "whatsapp" if "whatsapp" in parsed.path else "sms"
            result = BOT.chat(sender, text, channel=channel)
            self._send(twiml_message(result["reply"]), content_type="text/xml; charset=utf-8")
            return

        if parsed.path == "/webhook/ivr":
            sender = payload.get("From") or make_session_id("ivr")
            text = payload.get("SpeechResult") or payload.get("Digits") or payload.get("Body") or ""
            if not text:
                text = "1"
            result = BOT.chat(sender, text, channel="ivr")
            self._send(twiml_voice(result["reply"]), content_type="text/xml; charset=utf-8")
            return

        self._send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8011)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"JanSahayak running at http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
