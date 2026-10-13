import json
import threading
import unittest
import urllib.request

from museforge import MuseAgent, Config
from museforge.serving.http_server import MuseHTTPServer, make_handler


class TestServing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        agent = MuseAgent(Config())
        agent.remember("hello world", kind="semantic")
        handler = make_handler(agent)
        cls.server = MuseHTTPServer(("127.0.0.1", 0), handler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def _get(self, path):
        with urllib.request.urlopen("http://127.0.0.1:%d%s" % (self.port, path), timeout=10) as r:
            return r.status, json.loads(r.read().decode("utf-8"))

    def test_health(self):
        status, body = self._get("/health")
        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "ok")

    def test_models(self):
        status, body = self._get("/v1/models")
        self.assertEqual(status, 200)
        self.assertIn("mock", body["data"])

    def test_chat(self):
        req = urllib.request.Request(
            "http://127.0.0.1:%d/v1/chat/completions" % self.port,
            data=json.dumps({"messages": [{"role": "user", "content": "hello"}]}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            body = json.loads(r.read().decode("utf-8"))
        self.assertIn("choices", body)
        self.assertEqual(len(body["choices"]), 1)


if __name__ == "__main__":
    unittest.main()
