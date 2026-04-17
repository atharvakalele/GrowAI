#!/usr/bin/env python3
"""
Grow24 AI - Stock Restock Manager v1.0
======================================
Seller-listing auto stock manager driven by stock control config.

Usage:
    python stock_restock_v1.0.py --list
    python stock_restock_v1.0.py --execute
    python stock_restock_v1.0.py --execute --dry-run
"""

import argparse
import json
import os
import ssl
import sys
import time
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
            and os.path.exists(os.path.join(current, "config_features.json"))
        ):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            raise RuntimeError("Project root not found for stock restock")
        current = parent


PROJECT_DIR = find_project_dir(SCRIPT_DIR)
SP_CREDS = json.load(open(os.path.join(PROJECT_DIR, "sp_api_credentials.json"), encoding="utf-8"))["sp_api_credentials"]

REPORT_BASE = os.path.join(PROJECT_DIR, "ClaudeCode", "Report")
report_folders = [f for f in os.listdir(REPORT_BASE) if os.path.isdir(os.path.join(REPORT_BASE, f))]
report_folders.sort(key=lambda x: os.path.getmtime(os.path.join(REPORT_BASE, x)), reverse=True)
LATEST_REPORT = report_folders[0] if report_folders else datetime.now().strftime("%d %B %Y")
JSON_DIR = os.path.join(REPORT_BASE, LATEST_REPORT, "Json")

MARKETPLACE_ID = "A21TJRUUN4KGV"
SELLER_ID = "A2AC2AS9R9CBEA"
SP_ENDPOINT = "https://sellingpartnerapi-eu.amazon.com"

CONTROL_CONFIG_FILE = os.path.join(PROJECT_DIR, "config_stock_control.json")
STATUS_FILE = os.path.join(JSON_DIR, "stock_status.json")
ACTIVITY_LOG_FILE = os.path.join(JSON_DIR, "stock_activity_log.json")
CANDIDATES_FILE = os.path.join(JSON_DIR, "stock_restock_candidates_latest.json")

DEFAULT_TARGET_STOCK = 1000
DEFAULT_THRESHOLD = 1

SSL_CONTEXT = None
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

_token = None
_expiry = None


def load_json(path, default=None):
    if default is None:
        default = {}
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default


def save_json(path, payload):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def default_stock_control_config():
    return {
        "schema_type": "stock_control",
        "schema_version": "1.0",
        "scope": "seller_listing_only",
        "default_target_stock": DEFAULT_TARGET_STOCK,
        "default_minimum_threshold": DEFAULT_THRESHOLD,
        "manual_entries": []
    }


def normalize_entry(entry):
    return {
        "type": str(entry.get("type", "")).strip().lower(),
        "value": str(entry.get("value", "")).strip(),
        "excluded": bool(entry.get("excluded", False)),
        "created_at": entry.get("created_at", ""),
        "updated_at": entry.get("updated_at", ""),
    }


def load_stock_control_config():
    cfg = load_json(CONTROL_CONFIG_FILE, default_stock_control_config())
    cfg.setdefault("schema_type", "stock_control")
    cfg.setdefault("schema_version", "1.0")
    cfg["scope"] = "seller_listing_only"
    cfg["default_target_stock"] = int(cfg.get("default_target_stock", DEFAULT_TARGET_STOCK) or DEFAULT_TARGET_STOCK)
    cfg["default_minimum_threshold"] = int(cfg.get("default_minimum_threshold", DEFAULT_THRESHOLD) or DEFAULT_THRESHOLD)
    cfg["manual_entries"] = [
        normalize_entry(entry)
        for entry in cfg.get("manual_entries", [])
        if str(entry.get("type", "")).strip().lower() in ("asin", "sku") and str(entry.get("value", "")).strip()
    ]
    if not os.path.exists(CONTROL_CONFIG_FILE):
        save_json(CONTROL_CONFIG_FILE, cfg)
    return cfg


def get_token():
    global _token, _expiry
    if _token and _expiry and datetime.now() < _expiry:
        return _token
    data = urlencode({
        "grant_type": "refresh_token",
        "refresh_token": SP_CREDS["refresh_token"],
        "client_id": SP_CREDS["lwa_client_id"],
        "client_secret": SP_CREDS["lwa_client_secret"],
    }).encode()
    req = Request(SP_CREDS["token_url"], data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    result = json.loads(urlopen(req, context=SSL_CONTEXT).read().decode())
    _token = result["access_token"]
    _expiry = datetime.now() + timedelta(seconds=result["expires_in"] - 60)
    return _token


def sp_api_patch(sku, body):
    token = get_token()
    encoded_sku = quote(sku)
    url = f"{SP_ENDPOINT}/listings/2021-08-01/items/{SELLER_ID}/{encoded_sku}?marketplaceIds={MARKETPLACE_ID}"
    headers = {
        "x-amz-access-token": token,
        "x-amz-date": datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"),
        "Content-Type": "application/json",
        "Host": "sellingpartnerapi-eu.amazon.com",
    }
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="PATCH")
    try:
        resp = urlopen(req, context=SSL_CONTEXT)
        return json.loads(resp.read().decode()), resp.status
    except HTTPError as e:
        return {"error": e.read().decode()[:500]}, e.code


def load_activity_log():
    log = load_json(ACTIVITY_LOG_FILE, {"log_version": "1.0", "activities": []})
    if not isinstance(log.get("activities"), list):
        log["activities"] = []
    return log


def save_activity_log(log):
    save_json(ACTIVITY_LOG_FILE, log)


def log_activity(log, activity):
    activity["timestamp"] = datetime.now().isoformat()
    activity["log_id"] = f"ACT_{len(log['activities'])+1:04d}_{datetime.now().strftime('%H%M%S')}"
    log["activities"].append(activity)
    save_activity_log(log)
    return activity["log_id"]


def get_asin_sku_map():
    ads_file = os.path.join(JSON_DIR, "sp_product_ads_list.json")
    ads_rows = load_json(ads_file, [])
    if not ads_rows:
        for folder in report_folders:
            candidate = os.path.join(REPORT_BASE, folder, "Json", "sp_product_ads_list.json")
            if os.path.exists(candidate):
                ads_rows = load_json(candidate, [])
                if ads_rows:
                    break
    asin_skus = {}
    for row in ads_rows:
        sku = str(row.get("sku", "")).strip()
        asin = str(row.get("asin", "")).strip()
        if sku and asin:
            asin_skus.setdefault(asin, [])
            if sku not in asin_skus[asin]:
                asin_skus[asin].append(sku)
    return asin_skus


def build_entry_maps(cfg):
    asin_map = {}
    sku_map = {}
    for entry in cfg.get("manual_entries", []):
        if entry["type"] == "asin":
            asin_map[entry["value"]] = entry
        elif entry["type"] == "sku":
            sku_map[entry["value"]] = entry
    return asin_map, sku_map


def is_excluded_for_sku(asin, sku, cfg):
    asin_map, sku_map = build_entry_maps(cfg)
    if sku and sku in sku_map:
        return bool(sku_map[sku].get("excluded", False))
    if asin and asin in asin_map:
        return bool(asin_map[asin].get("excluded", False))
    return False


def resolve_status_file():
    if os.path.exists(STATUS_FILE):
        return STATUS_FILE
    for folder in report_folders:
        candidate = os.path.join(REPORT_BASE, folder, "Json", "stock_status.json")
        if os.path.exists(candidate):
            return candidate
    return STATUS_FILE


def build_candidate_payload():
    cfg = load_stock_control_config()
    status = load_json(resolve_status_file(), {})
    asin_skus = get_asin_sku_map()
    threshold = int(cfg.get("default_minimum_threshold", DEFAULT_THRESHOLD) or DEFAULT_THRESHOLD)
    target_stock = int(cfg.get("default_target_stock", DEFAULT_TARGET_STOCK) or DEFAULT_TARGET_STOCK)

    risk_items = []
    for item in list(status.get("zero_stock", [])) + list(status.get("low_stock", [])):
        asin = str(item.get("asin", "")).strip()
        skus = asin_skus.get(asin, [])
        excluded = all(is_excluded_for_sku(asin, sku, cfg) for sku in skus) if skus else is_excluded_for_sku(asin, "", cfg)
        risk_items.append({
            "type": "asin",
            "value": asin,
            "asin": asin,
            "sku": str(item.get("sku", "")).strip(),
            "seller_stock": int(item.get("total_stock", 0) or 0),
            "status": str(item.get("stock_status", "")).strip(),
            "threshold": threshold,
            "target_stock": target_stock,
            "excluded": excluded,
            "scope_skus": skus,
        })

    manual_items = []
    risk_asins = {item["asin"] for item in risk_items if item.get("asin")}
    for entry in cfg.get("manual_entries", []):
        if entry["type"] == "asin" and entry["value"] in risk_asins:
            continue
        manual_items.append({
            "type": entry["type"],
            "value": entry["value"],
            "asin": entry["value"] if entry["type"] == "asin" else "",
            "sku": entry["value"] if entry["type"] == "sku" else "",
            "seller_stock": None,
            "status": "MANUAL",
            "threshold": threshold,
            "target_stock": target_stock,
            "excluded": bool(entry.get("excluded", False)),
            "scope_skus": asin_skus.get(entry["value"], []) if entry["type"] == "asin" else [entry["value"]],
        })

    payload = {
        "schema_type": "stock_restock_candidates",
        "schema_version": "1.0",
        "generated_at": datetime.now().isoformat(),
        "scope": "seller_listing_only",
        "default_target_stock": target_stock,
        "default_minimum_threshold": threshold,
        "risk_items": risk_items,
        "manual_items": manual_items,
        "eligible_items": [item for item in risk_items if not item.get("excluded")],
        "excluded_items": [item for item in risk_items if item.get("excluded")],
    }
    save_json(CANDIDATES_FILE, payload)
    return payload


def generate_candidate_list():
    payload = build_candidate_payload()
    risk_items = payload.get("risk_items", [])
    eligible_items = payload.get("eligible_items", [])
    print("\n  Seller listing stock candidates prepared.")
    print(f"  Risk items: {len(risk_items)}")
    print(f"  Eligible for auto stock: {len(eligible_items)}")
    print(f"  Config file: {CONTROL_CONFIG_FILE}")
    print(f"  Candidate file: {CANDIDATES_FILE}")
    return 0


def execute_restock(dry_run=False, qty=None):
    cfg = load_stock_control_config()
    payload = build_candidate_payload()
    activity_log = load_activity_log()
    target_qty = int(qty or cfg.get("default_target_stock", DEFAULT_TARGET_STOCK) or DEFAULT_TARGET_STOCK)
    eligible_items = payload.get("eligible_items", [])
    asin_skus = get_asin_sku_map()

    if not eligible_items:
        print("\n  No seller listing items qualified for auto stock.")
        return 0

    print(f"\n  {'DRY RUN - ' if dry_run else ''}Auto stock for {len(eligible_items)} risky item(s) to {target_qty} units.")
    success = 0
    failed = 0

    for item in eligible_items:
        asin = item.get("asin", "")
        current_stock = int(item.get("seller_stock", 0) or 0)
        source_skus = item.get("scope_skus", []) or asin_skus.get(asin, [])
        skus = [sku for sku in source_skus if not is_excluded_for_sku(asin, sku, cfg)]

        if not skus:
            continue

        for sku in skus:
            print(f"    {asin} ({sku[:25]}) : {current_stock} -> {target_qty}...", end=" ")
            if dry_run:
                print("DRY_RUN OK")
                log_activity(activity_log, {
                    "action": "RESTOCK_DRY_RUN",
                    "asin": asin,
                    "sku": sku,
                    "before_quantity": current_stock,
                    "after_quantity": target_qty,
                    "scope_type": item.get("type", "asin"),
                    "scope_value": item.get("value", asin),
                    "dry_run": True,
                })
                success += 1
                continue

            body = {
                "productType": "PRODUCT",
                "patches": [{
                    "op": "replace",
                    "path": "/attributes/fulfillment_availability",
                    "value": [{
                        "fulfillment_channel_code": "DEFAULT",
                        "quantity": target_qty,
                        "marketplace_id": MARKETPLACE_ID,
                    }]
                }]
            }

            result, status = sp_api_patch(sku, body)
            if "error" not in result and status in (200, 202):
                print("OK")
                success += 1
                log_activity(activity_log, {
                    "action": "RESTOCK_SUCCESS",
                    "asin": asin,
                    "sku": sku,
                    "before_quantity": current_stock,
                    "after_quantity": target_qty,
                    "scope_type": item.get("type", "asin"),
                    "scope_value": item.get("value", asin),
                    "api_status": status,
                })
            else:
                error_msg = result.get("error", str(result))[:200]
                print(f"FAILED: {error_msg}")
                failed += 1
                log_activity(activity_log, {
                    "action": "RESTOCK_FAILED",
                    "asin": asin,
                    "sku": sku,
                    "before_quantity": current_stock,
                    "target_quantity": target_qty,
                    "scope_type": item.get("type", "asin"),
                    "scope_value": item.get("value", asin),
                    "error": error_msg,
                })
            time.sleep(0.5)

    print(f"\n  {'=' * 50}")
    print(f"  AUTO STOCK {'PREVIEW' if dry_run else 'COMPLETE'}")
    print(f"  {'=' * 50}")
    print(f"  Eligible items: {len(eligible_items)}")
    print(f"  Success: {success}")
    print(f"  Failed: {failed}")
    print(f"  Activity log: {ACTIVITY_LOG_FILE}")
    return 0 if failed == 0 else 1


def main():
    parser = argparse.ArgumentParser(description="Stock Restock Manager v1.0")
    parser.add_argument("--list", action="store_true", help="Prepare seller listing candidate file")
    parser.add_argument("--execute", action="store_true", help="Execute auto stock from stock control config")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    parser.add_argument("--qty", type=int, default=0, help="Override target quantity for this run")
    args = parser.parse_args()

    print("=" * 60)
    print("  Grow24 AI - Stock Restock Manager v1.0")
    print(f"  {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print("=" * 60)

    if args.list:
        return generate_candidate_list()
    if args.execute:
        return execute_restock(dry_run=args.dry_run, qty=args.qty or None)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
