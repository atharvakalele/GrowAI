#!/usr/bin/env python3
"""
Grow24 AI - Listing Recovery v1.0
=================================
Shared action engine for listing-risk routes.

What it does:
  1. Accepts route requests from detector modules
  2. Verifies listing state via Listings Items API
  3. Creates targeted recovery requests only when listing is inactive/not searchable
  4. Reuses price optimizer for the actual safe recovery price decrease

Usage:
    python listing_recovery_v1.0.py --route-file path/to/route.json
    python listing_recovery_v1.0.py --route-file path/to/route.json --dry-run
"""

import argparse
import json
import os
import ssl
import subprocess
import sys
from functools import lru_cache
from datetime import datetime, timedelta
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def find_project_dir(start_dir):
    current = os.path.abspath(start_dir)
    while True:
        if (
            os.path.exists(os.path.join(current, "sp_api_credentials.json"))
            and os.path.exists(os.path.join(current, "config_price_optimizer.json"))
        ):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            raise RuntimeError("Project root not found for listing recovery")
        current = parent


PROJECT_DIR = find_project_dir(SCRIPT_DIR)
SP_CREDS_FILE = os.path.join(PROJECT_DIR, "sp_api_credentials.json")
PRICE_CONFIG_FILE = os.path.join(PROJECT_DIR, "config_price_optimizer.json")

REPORT_BASE = os.path.join(PROJECT_DIR, "ClaudeCode", "Report")
report_folders = [f for f in os.listdir(REPORT_BASE) if os.path.isdir(os.path.join(REPORT_BASE, f))]
report_folders.sort(key=lambda x: os.path.getmtime(os.path.join(REPORT_BASE, x)), reverse=True)
LATEST_REPORT = report_folders[0] if report_folders else datetime.now().strftime("%d %B %Y")
JSON_DIR = os.path.join(REPORT_BASE, LATEST_REPORT, "Json")

STATUS_FILE = os.path.join(JSON_DIR, "listing_recovery_status.json")
PRICE_ROUTE_REQUEST_FILE = os.path.join(JSON_DIR, "listing_recovery_price_route_latest.json")
PRICE_ROUTE_RESULT_FILE = os.path.join(JSON_DIR, "listing_recovery_price_route_result_latest.json")
PRICE_OPTIMIZER_SCRIPT = os.path.join(
    PROJECT_DIR, "Grow24_AI", "marketplaces", "amazon", "seller_api", "pricing", "price_optimizer_v1.0.py"
)
PRICE_OPTIMIZER_STATUS_FILE = os.path.join(JSON_DIR, "price_optimizer_status.json")
DATA_SEARCH_ROOTS = [
    os.path.join(PROJECT_DIR, "Grow24_AI", "data"),
    os.path.join(PROJECT_DIR, "ClaudeCode", "Report"),
]

MARKETPLACE_ID = "A21TJRUUN4KGV"
SELLER_ID = "A2AC2AS9R9CBEA"
SP_ENDPOINT = "https://sellingpartnerapi-eu.amazon.com"
TOKEN_URL = "https://api.amazon.com/auth/o2/token"

SSL_CONTEXT = None
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

SP = json.load(open(SP_CREDS_FILE, encoding="utf-8"))["sp_api_credentials"]
_cached_token = None
_token_expiry = None


def load_json(path, default):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json_pair(latest_file, prefix, payload, started_at):
    os.makedirs(JSON_DIR, exist_ok=True)
    ts = started_at.strftime("%Y%m%d_%H%M%S")
    history_file = os.path.join(JSON_DIR, f"{prefix}_{ts}.json")
    with open(latest_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return history_file


def relative_path(path):
    return os.path.relpath(path, PROJECT_DIR).replace("\\", "/")


@lru_cache(maxsize=32)
def find_latest_data_file(filename):
    candidates = []
    for root in DATA_SEARCH_ROOTS:
        if not os.path.exists(root):
            continue
        for current_root, _dirs, files in os.walk(root):
            if filename in files:
                candidate = os.path.join(current_root, filename)
                try:
                    candidates.append((os.path.getmtime(candidate), candidate))
                except OSError:
                    continue
    if not candidates:
        return ""
    candidates.sort(reverse=True)
    return candidates[0][1]


def extract_price_candidates(log_entry):
    prices = []
    for key in ("new_price", "old_price"):
        try:
            value = float(log_entry.get(key, 0) or 0)
        except (TypeError, ValueError):
            value = 0
        if value > 0:
            prices.append(value)
    return prices


def resolve_current_price(asin, sku, hinted_price=0):
    try:
        hinted_price = float(hinted_price or 0)
    except (TypeError, ValueError):
        hinted_price = 0
    if hinted_price > 0:
        return round(hinted_price, 2), "route_request"

    pricing_file = find_latest_data_file("sp_pricing_data.json")
    if pricing_file:
        pricing_data = load_json(pricing_file, {})
        if isinstance(pricing_data, dict):
            price_row = pricing_data.get(asin, {})
            try:
                pricing_value = float(price_row.get("your_price", 0) or 0)
            except (AttributeError, TypeError, ValueError):
                pricing_value = 0
            if pricing_value > 0:
                return round(pricing_value, 2), "sp_pricing_data"

    optimizer_log_file = find_latest_data_file("price_optimizer_log.json")
    if optimizer_log_file:
        log_data = load_json(optimizer_log_file, {})
        if isinstance(log_data, dict):
            history = log_data.get(f"{asin}_{sku}", [])
            for entry in reversed(history):
                for price in extract_price_candidates(entry):
                    return round(price, 2), "price_optimizer_log"

    return 0.0, ""


def get_token():
    global _cached_token, _token_expiry
    if _cached_token and _token_expiry and datetime.now() < _token_expiry:
        return _cached_token

    data = urlencode({
        "grant_type": "refresh_token",
        "refresh_token": SP["refresh_token"],
        "client_id": SP["lwa_client_id"],
        "client_secret": SP["lwa_client_secret"]
    }).encode()
    req = Request(TOKEN_URL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    result = json.loads(urlopen(req, context=SSL_CONTEXT).read().decode())
    _cached_token = result["access_token"]
    _token_expiry = datetime.now() + timedelta(seconds=result["expires_in"] - 60)
    return _cached_token


def check_listing_status(sku):
    try:
        token = get_token()
        encoded_sku = quote(sku)
        url = (
            f"{SP_ENDPOINT}/listings/2021-08-01/items/{SELLER_ID}/{encoded_sku}"
            f"?marketplaceIds={MARKETPLACE_ID}&includedData=summaries,issues"
        )
        headers = {
            "x-amz-access-token": token,
            "x-amz-date": datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"),
            "Host": "sellingpartnerapi-eu.amazon.com",
        }
        req = Request(url, headers=headers)
        resp = urlopen(req, context=SSL_CONTEXT)
        result = json.loads(resp.read().decode())
    except HTTPError as e:
        return {
            "status": "API_ERROR",
            "buyable": False,
            "discoverable": False,
            "issues": [],
            "error": e.read().decode()[:200]
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "buyable": False,
            "discoverable": False,
            "issues": [],
            "error": str(e)[:200]
        }

    summaries = result.get("summaries", [])
    issues = result.get("issues", [])
    status_list = []
    asin = ""
    item_name = ""
    for summary in summaries:
        if summary.get("marketplaceId") == MARKETPLACE_ID:
            status_list = summary.get("status", [])
            asin = summary.get("asin", "")
            item_name = summary.get("itemName", "")
            break

    is_buyable = "BUYABLE" in status_list
    is_discoverable = "DISCOVERABLE" in status_list
    if is_buyable and is_discoverable:
        listing_status = "ACTIVE"
    elif is_buyable:
        listing_status = "NOT_SEARCHABLE"
    else:
        listing_status = "INACTIVE"

    critical_issues = [
        {"message": issue.get("message", ""), "severity": issue.get("severity", "")}
        for issue in issues
        if issue.get("severity") in ("ERROR", "WARNING")
    ]
    return {
        "status": listing_status,
        "asin": asin,
        "item_name": item_name[:80],
        "buyable": is_buyable,
        "discoverable": is_discoverable,
        "statuses": status_list,
        "issues": critical_issues[:5],
    }


def build_price_recovery_routes(route_payload, started_at, dry_run):
    price_config = load_json(PRICE_CONFIG_FILE, {})
    pricing_rules = price_config.get("pricing_rules", {})
    default_decrease_pct = float(pricing_rules.get("decrease_pct", 1.0) or 1.0)
    requests = route_payload.get("requests", []) if isinstance(route_payload, dict) else []
    route_run_id = f"listing_recovery_price_{started_at.strftime('%Y%m%d_%H%M%S')}"

    status_checks = []
    price_requests = []
    blocked_items = []

    for request in requests:
        asin = request.get("asin", "")
        sku = request.get("sku", "")
        current_price, price_source = resolve_current_price(asin, sku, request.get("current_price", 0))
        if not asin or not sku:
            blocked_items.append({
                "asin": asin,
                "sku": sku,
                "status": "BLOCKED",
                "reason": "Missing ASIN or SKU for listing recovery route."
            })
            continue

        listing = check_listing_status(sku)
        issues = listing.get("issues", [])
        status_checks.append({
            "asin": asin,
            "sku": sku,
            "current_price": round(current_price, 2),
            "price_source": price_source or "missing",
            "listing_status": listing.get("status", "UNKNOWN"),
            "issues": issues,
            "source_issue_type": request.get("issue_type", ""),
            "source_reason": request.get("route_reason", ""),
        })

        if listing.get("status") not in ("INACTIVE", "NOT_SEARCHABLE"):
            blocked_items.append({
                "asin": asin,
                "sku": sku,
                "status": "SKIPPED",
                "reason": f"Listing status is {listing.get('status', 'UNKNOWN')}; recovery price route not needed."
            })
            continue
        if current_price <= 0:
            blocked_items.append({
                "asin": asin,
                "sku": sku,
                "status": "BLOCKED",
                "reason": "Current price missing after fallback search; cannot create recovery route."
            })
            continue

        reduction_pct = float(request.get("reduction_pct", default_decrease_pct) or default_decrease_pct)
        target_price = float(request.get("target_price", 0) or 0)
        if target_price <= 0:
            target_price = round(current_price * (1 - reduction_pct / 100), 2)

        reason_parts = [f"Listing status {listing['status']}"]
        if issues:
            reason_parts.append(issues[0].get("message", "")[:120])
        price_requests.append({
            "route_run_id": route_run_id,
            "source_feature_key": "listing_recovery",
            "source_feature_name": "Listing Recovery",
            "source_route_feature_key": request.get("source_feature_key", ""),
            "action_family": "listing_recovery",
            "target_engine": "price_optimizer",
            "desired_action": "DECREASE_RECOVERY",
            "issue_type": request.get("issue_type", "listing_not_buyable"),
            "asin": asin,
            "sku": sku,
            "current_price": round(current_price, 2),
            "price_source": price_source or "unknown",
            "target_price": round(target_price, 2),
            "reduction_pct": reduction_pct,
            "listing_status": listing.get("status", ""),
            "sales7d_rs": round(float(request.get("sales7d_rs", 0) or 0), 2),
            "signals": list(request.get("signals", [])) + [f"Listing status: {listing.get('status', 'UNKNOWN')}"],
            "route_reason": " | ".join(part for part in reason_parts if part),
            "auto_action_allowed": bool(request.get("auto_action_allowed", True) and not dry_run)
        })

    payload = {
        "schema_type": "action_route_request",
        "schema_version": "1.0",
        "route_run_id": route_run_id,
        "generated_at": datetime.now().isoformat(),
        "source_feature_key": "listing_recovery",
        "source_feature_name": "Listing Recovery",
        "action_engine": "price_optimizer",
        "requests": price_requests,
        "status_checks": status_checks,
        "blocked_items": blocked_items
    }
    history_file = save_json_pair(PRICE_ROUTE_REQUEST_FILE, "listing_recovery_price_route", payload, started_at)
    return payload, history_file


def execute_price_routes(route_payload, route_history_file, started_at, dry_run):
    result = {
        "route_run_id": route_payload.get("route_run_id", ""),
        "generated_at": datetime.now().isoformat(),
        "engine": "price_optimizer",
        "request_count": len(route_payload.get("requests", [])),
        "status": "skipped",
        "reason": "",
        "summary": {},
        "actions": [],
        "blocked_items": route_payload.get("blocked_items", []),
        "status_checks": route_payload.get("status_checks", []),
        "request_file": relative_path(PRICE_ROUTE_REQUEST_FILE),
        "request_history_file": relative_path(route_history_file),
    }

    if not route_payload.get("requests"):
        result["reason"] = "No listing recovery routes qualified for price action."
        history_file = save_json_pair(PRICE_ROUTE_RESULT_FILE, "listing_recovery_price_route_result", result, started_at)
        return result, history_file
    if not os.path.exists(PRICE_OPTIMIZER_SCRIPT):
        result["status"] = "failed"
        result["reason"] = "Price optimizer script not found."
        history_file = save_json_pair(PRICE_ROUTE_RESULT_FILE, "listing_recovery_price_route_result", result, started_at)
        return result, history_file

    cmd = [sys.executable, PRICE_OPTIMIZER_SCRIPT, "--route-file", route_history_file]
    if dry_run:
        cmd.append("--dry-run")
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_DIR)
    status_data = load_json(PRICE_OPTIMIZER_STATUS_FILE, {})
    result["status"] = "executed" if proc.returncode == 0 else "failed"
    result["reason"] = "Listing recovery route executed." if proc.returncode == 0 else "Listing recovery route execution failed."
    result["command"] = " ".join(cmd)
    result["return_code"] = proc.returncode
    result["stdout_tail"] = (proc.stdout or "")[-1200:]
    result["stderr_tail"] = (proc.stderr or "")[-1200:]
    result["summary"] = status_data.get("summary", {})
    result["actions"] = [
        action for action in status_data.get("actions", [])
        if action.get("route_run_id") == route_payload.get("route_run_id")
    ]
    result["price_optimizer_status_file"] = relative_path(PRICE_OPTIMIZER_STATUS_FILE)
    history_file = save_json_pair(PRICE_ROUTE_RESULT_FILE, "listing_recovery_price_route_result", result, started_at)
    return result, history_file


def main():
    parser = argparse.ArgumentParser(description="Listing Recovery route engine")
    parser.add_argument("--route-file", required=True, help="Path to incoming route request JSON")
    parser.add_argument("--dry-run", action="store_true", help="Preview routed recovery actions only")
    args = parser.parse_args()

    started_at = datetime.now()
    incoming = load_json(args.route_file, {})
    incoming_requests = incoming.get("requests", []) if isinstance(incoming, dict) else []

    status_payload = {
        "schema_type": "listing_recovery_status",
        "schema_version": "1.0",
        "generated_at": datetime.now().isoformat(),
        "input_route_file": os.path.relpath(args.route_file, PROJECT_DIR).replace("\\", "/"),
        "input_route_count": len(incoming_requests),
        "status": "skipped",
        "reason": "",
        "checked_items": [],
        "blocked_items": [],
        "price_route": {},
    }

    if not incoming_requests:
        status_payload["reason"] = "No listing recovery requests received."
        save_json_pair(STATUS_FILE, "listing_recovery_status", status_payload, started_at)
        return 0

    price_route_payload, price_route_history_file = build_price_recovery_routes(incoming, started_at, args.dry_run)
    price_route_result, price_route_result_history_file = execute_price_routes(
        price_route_payload, price_route_history_file, started_at, args.dry_run
    )
    price_route_result["result_file"] = relative_path(PRICE_ROUTE_RESULT_FILE)
    price_route_result["result_history_file"] = relative_path(price_route_result_history_file)

    status_payload["checked_items"] = price_route_payload.get("status_checks", [])
    status_payload["blocked_items"] = price_route_payload.get("blocked_items", [])
    status_payload["price_route"] = price_route_result
    status_payload["status"] = price_route_result.get("status", "skipped")
    status_payload["reason"] = price_route_result.get("reason", "")

    save_json_pair(STATUS_FILE, "listing_recovery_status", status_payload, started_at)
    print(f"Checked items:      {len(status_payload['checked_items'])}")
    print(f"Recovery routes:    {price_route_result.get('request_count', 0)}")
    print(f"Recovery status:    {price_route_result.get('status', 'skipped')}")
    return 0 if price_route_result.get("status") in ("executed", "skipped") else 1


if __name__ == "__main__":
    sys.exit(main())
