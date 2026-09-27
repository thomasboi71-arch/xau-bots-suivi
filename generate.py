"""Regenere index.html a partir des donnees live du panneau local (127.0.0.1:8765).

Usage : python generate.py
Sortie : index.html, dans ce meme dossier.

Lecture seule : aucun ordre, aucune ecriture ailleurs que ce dossier. Les
numeros de compte (login) sont retires avant publication ; les soldes et
l'historique des trades restent visibles (demande explicite de l'utilisateur).
"""
from __future__ import annotations
import copy
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parent
TEMPLATE = BASE / "template.html"
OUT = BASE / "index.html"
STATE_URL = "http://127.0.0.1:8765/api/state"


def fetch_state() -> dict:
    req = Request(STATE_URL, headers={"Cache-Control": "no-cache"})
    with urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def redact(state: dict) -> dict:
    """Retire les numeros de compte (login), garde le reste (soldes inclus)."""
    d = copy.deepcopy(state)
    for c in d.get("comptes", []):
        if c.get("account") and "login" in c["account"]:
            c["account"]["login"] = None
    if d.get("account") and "login" in d["account"]:
        d["account"]["login"] = None
    d["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return d


def build() -> Path:
    html = TEMPLATE.read_text(encoding="utf-8")
    snapshot = redact(fetch_state())
    injection = f"<script>window.__SNAPSHOT__ = {json.dumps(snapshot, ensure_ascii=False)};</script>\n"
    out = re.sub(r"(<script>\s*const SNAPSHOT)", injection + r"\1", html, count=1)
    OUT.write_text(out, encoding="utf-8")
    return OUT


if __name__ == "__main__":
    try:
        path = build()
    except Exception as exc:  # noqa: BLE001 - message clair pour la tache planifiee
        print(f"ECHEC : {exc}", file=sys.stderr)
        raise SystemExit(1)
    print(f"OK : {path} ({path.stat().st_size} octets)")
