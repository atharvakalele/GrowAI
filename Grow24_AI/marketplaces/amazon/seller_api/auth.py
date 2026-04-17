#!/usr/bin/env python3
"""
SP-API Authentication — Grow24 AI
===================================
Handles OAuth2 LWA token for all SP-API calls.
Reused across all SP-API modules (inventory, FBA, pricing, orders, etc.)

Token is cached and auto-refreshed before expiry.
"""

import json
import ssl
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

PROJECT_ROOT = Path(__file__).resolve().parents[4]
CREDS_FILE   = PROJECT_ROOT.parent / "sp_api_credentials.json"

SP_ENDPOINT  = "https://sellingpartnerapi-eu.amazon.com"
MARKETPLACE_ID = "A21TJRUUN4KGV"  # India

# ── SSL context ──
try:
    import certifi
    _SSL = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL = ssl.create_default_context()

# ── Token cache ──
_token  = None
_expiry = None


def _load_creds() -> dict:
    with open(CREDS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("sp_api_credentials", data)


def get_token() -> str:
    global _token, _expiry
    if _token and _expiry and datetime.now() < _expiry:
        return _token

    creds = _load_creds()
    payload = urlencode({
        "grant_type":    "refresh_token",
        "refresh_token": creds["refresh_token"],
        "client_id":     creds["lwa_client_id"],
        "client_secret": creds["lwa_client_secret"],
    }).encode()
    req = Request(
        creds["token_url"],
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    result = json.loads(urlopen(req, context=_SSL).read().decode())
    _token  = result["access_token"]
    _expiry = datetime.now() + timedelta(seconds=result["expires_in"] - 60)
    return _token


def sp_get(path: str, params: dict = None) -> dict:
    """GET request to SP-API."""
    from urllib.parse import urlencode as _ue
    url = SP_ENDPOINT + path
    if params:
        url += "?" + _ue(params)
    req = Request(url, headers={
        "x-amz-access-token": get_token(),
        "Content-Type": "application/json",
    })
    resp = urlopen(req, context=_SSL)
    return json.loads(resp.read().decode())


def sp_post(path: str, body: dict) -> dict:
    """POST request to SP-API."""
    import json as _json
    url = SP_ENDPOINT + path
    data = _json.dumps(body).encode()
    req = Request(url, data=data, headers={
        "x-amz-access-token": get_token(),
        "Content-Type": "application/json",
    })
    resp = urlopen(req, context=_SSL)
    return json.loads(resp.read().decode())


def sp_put(path: str, body: dict) -> dict:
    """PUT request to SP-API."""
    import json as _json
    url = SP_ENDPOINT + path
    data = _json.dumps(body).encode()
    req = Request(url, data=data, method="PUT", headers={
        "x-amz-access-token": get_token(),
        "Content-Type": "application/json",
    })
    resp = urlopen(req, context=_SSL)
    return json.loads(resp.read().decode())
