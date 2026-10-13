"""Zero-dependency HTTP server exposing the MuseAgent.

Endpoints:
  GET  /health              -> {"status": "ok"}
  GET  /v1/models           -> list available backends
  POST /v1/chat/completions -> OpenAI-compatible chat completion (memory-augmented)
  POST /v1/memories         -> add a memory {"content", "kind", "importance"}
  GET  /v1/memories         -> list stored memories
  POST /v1/retrieve         -> {"query", "k"} -> ranked memories
  POST /v1/goal             -> {"description"} -> set goal
  GET  /v1/focus            -> current focus state
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from ..engine.agent import MuseAgent


def make_handler(agent: MuseAgent):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def _send(self, code, obj):
            body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _read_json(self):
            length = int(self.headers.get("Content-Length", 0) or 0)
            if length == 0:
                return {}
            return json.loads(self.rfile.read(length).decode("utf-8"))

        def do_GET(self):
            if self.path == "/health":
                return self._send(200, {"status": "ok"})
            if self.path == "/v1/models":
                from ..model.backends import list_backends
                return self._send(200, {"data": list_backends()})
            if self.path == "/v1/memories":
                mems = [{"id": m.id, "kind": m.kind, "content": m.content} for m in agent.store.all()]
                return self._send(200, {"data": mems})
            if self.path == "/v1/focus":
                return self._send(200, agent.focus_state())
            return self._send(404, {"error": "not found"})

        def do_POST(self):
            try:
                data = self._read_json()
                if self.path == "/v1/chat/completions":
                    query = (data.get("messages") or [{}])[-1].get("content", "")
                    out = agent.respond(query)
                    return self._send(200, {
                        "id": "museforge",
                        "object": "chat.completion",
                        "choices": [{"index": 0, "message": {"role": "assistant", "content": out["response"]}, "finish_reason": "stop"}],
                    })
                if self.path == "/v1/memories":
                    m = agent.remember(
                        data.get("content", ""),
                        kind=data.get("kind", "episodic"),
                        importance=data.get("importance", 0.5),
                    )
                    return self._send(200, {"id": m.id, "kind": m.kind, "content": m.content})
                if self.path == "/v1/retrieve":
                    out = agent.recall(data.get("query", ""), k=data.get("k"))
                    return self._send(200, {"data": [{"content": m.content, "score": round(s, 3)} for m, s in out]})
                if self.path == "/v1/goal":
                    g = agent.set_goal(data.get("description", ""))
                    return self._send(200, {"id": g.id, "subgoals": g.subgoals})
                return self._send(404, {"error": "not found"})
            except Exception as e:
                return self._send(500, {"error": str(e)})

    return Handler


class MuseHTTPServer(ThreadingHTTPServer):
    daemon_threads = True


def run(agent: MuseAgent, host: str = "127.0.0.1", port: int = 8000):
    handler = make_handler(agent)
    server = MuseHTTPServer((host, port), handler)
    print("museforge listening on http://%s:%d" % (host, port), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
