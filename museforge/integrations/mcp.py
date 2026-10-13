"""MCP (Model Context Protocol) server exposing memory + focus tools.

Uses the stdlib `json` only -- no MCP SDK dependency. The server speaks the MCP
JSON-RPC wire protocol over stdin/stdout, exposing two tools:

  * muse.remember(content, kind, importance) -> add a memory
  * muse.recall(query, k)                    -> retrieve relevant memories
"""
from __future__ import annotations

import json
import sys

TOOLS = [
    {
        "name": "muse.remember",
        "description": "Persist a piece of user context (fact/preference/event) into Active Memory.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content": {"type": "string"},
                "kind": {"type": "string", "enum": ["episodic", "semantic"]},
                "importance": {"type": "number"},
            },
            "required": ["content"],
        },
    },
    {
        "name": "muse.recall",
        "description": "Proactively retrieve the most relevant memories for a query.",
        "inputSchema": {
            "type": "object",
            "properties": {"query": {"type": "string"}, "k": {"type": "integer"}},
            "required": ["query"],
        },
    },
]


def _reply(req_id, result):
    return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result}, ensure_ascii=False)


def _error(req_id, code, message):
    return json.dumps({"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}, ensure_ascii=False)


def _dispatch(req, agent):
    method = req.get("method")
    params = req.get("params") or {}
    req_id = req.get("id")
    if method == "initialize":
        return _reply(req_id, {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "museforge", "version": "0.1.0"}})
    if method == "tools/list":
        return _reply(req_id, {"tools": TOOLS})
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        if name == "muse.remember":
            m = agent.remember(args.get("content", ""), kind=args.get("kind", "episodic"), importance=args.get("importance", 0.5))
            return _reply(req_id, {"content": [{"type": "text", "text": "remembered " + m.id}]})
        if name == "muse.recall":
            out = agent.recall(args.get("query", ""), k=args.get("k"))
            text = "\n".join("- [%.3f] %s" % (s, m.content) for m, s in out)
            return _reply(req_id, {"content": [{"type": "text", "text": text}]})
        return _error(req_id, -32601, "unknown tool: %s" % name)
    if method == "notifications/initialized":
        return None
    return _error(req_id, -32601, "method not found")


def serve(agent):
    """Run the MCP server over stdin/stdout."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue
        resp = _dispatch(req, agent)
        if resp is not None:
            print(resp, flush=True)
