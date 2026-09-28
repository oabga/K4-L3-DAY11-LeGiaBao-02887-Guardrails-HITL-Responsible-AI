"""
Assignment 11 — Audit Log starter (TODO).

Records every interaction for forensics. Never blocks by itself —
other layers catch attacks; this layer makes them reviewable.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def default_audit_log_path() -> str:
    """Always resolve to <repo>/outputs/… (safe when cwd is src/)."""
    repo_root = Path(__file__).resolve().parents[2]
    return str(repo_root / "outputs" / "audit_log.json")


class AuditLogPlugin:
    """Framework-agnostic audit logger (wire into ADK callbacks or your pipeline)."""

    def __init__(self):
        self.name = "audit_log"
        self.logs: list[dict] = []
        self._open: dict[str, float] = {}

    def record_input(self, *, user_id: str, text: str, request_id: str | None = None):
        """Store input + start timestamp keyed by request_id/user_id."""
        request_id = request_id or f"req-{len(self.logs) + 1}"
        self._open[request_id] = datetime.now(timezone.utc).timestamp()
        self.logs.append(
            {
                "event": "input",
                "request_id": request_id,
                "user_id": user_id,
                "text": text,
                "ts": utc_now_iso(),
            }
        )
        return request_id

    def record_output(
        self,
        *,
        user_id: str,
        text: str,
        blocked: bool = False,
        layer: str | None = None,
        request_id: str | None = None,
    ):
        """Store output, layer decision, latency; append to self.logs."""
        request_id = request_id or f"req-{len(self.logs) + 1}"
        start = self._open.get(request_id)
        now_ts = datetime.now(timezone.utc).timestamp()
        latency_ms = None
        if start is not None:
            latency_ms = max(0.0, (now_ts - start) * 1000.0)

        self.logs.append(
            {
                "event": "output",
                "request_id": request_id,
                "user_id": user_id,
                "text": text,
                "blocked": blocked,
                "layer": layer,
                "latency_ms": latency_ms,
                "ts": utc_now_iso(),
            }
        )
        return request_id

    def export_json(self, filepath: str | None = None):
        """Write logs to disk (JSON array) under repo-root ``outputs/`` by default."""
        path = filepath or default_audit_log_path()
        out_path = Path(path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(self.logs, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(out_path)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
