"""API HTTP mínima (apenas stdlib) para submeter solicitações ao WSS13_GOS.

Endpoints:
    POST /requests            -> executa o pipeline com o JSON do corpo
    GET  /requests/<id>       -> retorna a solicitação persistida
    GET  /evidence            -> lista a cadeia de evidências
    GET  /evidence/verify     -> valida a integridade da cadeia
    GET  /health              -> status

Uso:
    python -m wss13_gos.api            # sobe em 127.0.0.1:8013
"""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .orchestrator import GovernanceOrchestrator


def _json_default(o):
    if isinstance(o, datetime):
        return o.isoformat()
    if hasattr(o, "value"):
        return o.value
    raise TypeError(f"não serializável: {type(o)}")


def make_handler(orchestrator: GovernanceOrchestrator):
    class Handler(BaseHTTPRequestHandler):
        server_version = "WSS13_GOS/0.1"

        def _send(self, code: int, body: dict) -> None:
            payload = json.dumps(body, default=_json_default, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, *args) -> None:  # silencia log padrão
            pass

        def do_GET(self) -> None:
            if self.path == "/health":
                self._send(200, {"status": "ok", "protocol": "WSS13-SGI-AI-PSEUDOCODE-001"})
            elif self.path == "/evidence":
                self._send(200, {"evidence": [asdict(e) for e in orchestrator.repo.all_evidence()]})
            elif self.path == "/evidence/verify":
                self._send(200, {"chain_valid": orchestrator.evidence.verify_chain()})
            elif self.path.startswith("/requests/"):
                rid = self.path.split("/requests/", 1)[1]
                req = orchestrator.repo.get_request(rid)
                if req is None:
                    self._send(404, {"error": "request not found"})
                else:
                    self._send(200, {"request": asdict(req)})
            else:
                self._send(404, {"error": "not found"})

        def do_POST(self) -> None:
            if self.path != "/requests":
                self._send(404, {"error": "not found"})
                return
            length = int(self.headers.get("Content-Length", 0))
            try:
                event = json.loads(self.rfile.read(length) or b"{}")
            except json.JSONDecodeError:
                self._send(400, {"error": "invalid JSON"})
                return
            try:
                response = orchestrator.execute(event)
            except ValueError as exc:
                self._send(422, {"error": str(exc)})
                return
            self._send(201, {
                "status": response.status,
                "reason": response.reason,
                "request_id": response.request.request_id,
                "risk_level": response.risk_assessment.risk_level.value
                if response.risk_assessment else None,
                "total_score": response.risk_assessment.total_score
                if response.risk_assessment else None,
                "required_approvers": [r.value for r in response.risk_assessment.required_approvers]
                if response.risk_assessment else [],
            })

    return Handler


def serve(host: str = "127.0.0.1", port: int = 8013) -> None:
    orchestrator = GovernanceOrchestrator()
    httpd = ThreadingHTTPServer((host, port), make_handler(orchestrator))
    print(f"WSS13_GOS API ouvindo em http://{host}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()


if __name__ == "__main__":
    serve()
