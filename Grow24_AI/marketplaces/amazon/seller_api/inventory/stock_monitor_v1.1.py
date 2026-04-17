#!/usr/bin/env python3
"""
Grow24 AI - Stock Monitor v1.1
==============================
Legacy-compatible seller-listing stock monitor with future-module summaries
and stock control routing.
"""

import argparse
import json
import os
import ssl
import subprocess
import sys
import time
from datetime import datetime, timedelta
from urllib.error import HTTPError, URLError
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
            raise RuntimeError("Project root not found for stock monitor")
        current = parent


PROJECT_DIR = find_project_dir(SCRIPT_DIR)
SP_CREDS_FILE = os.path.join(PROJECT_DIR, "sp_api_credentials.json")
REPORT_BASE = os.path.join(PROJECT_DIR, "ClaudeCode", "Report")
report_folders = [f for f in os.listdir(REPORT_BASE) if os.path.isdir(os.path.join(REPORT_BASE, f))]
report_folders.sort(key=lambda x: os.path.getmtime(os.path.join(REPORT_BASE, x)), reverse=True)
LATEST_REPORT = report_folders[0] if report_folders else datetime.now().strftime("%d %B %Y")
JSON_DIR = os.path.join(REPORT_BASE, LATEST_REPORT, "Json")

FEATURE_ID = "M04"
FEATURE_KEY = "stock"
FEATURE_NAME = "Stock Monitor"
MODULE_GROUP = "inventory"

STATUS_FILE = os.path.join(JSON_DIR, "stock_status.json")
IMPACT_LATEST_FILE = os.path.join(JSON_DIR, "impact_stock_latest.json")
ACTIVITY_LATEST_FILE = os.path.join(JSON_DIR, "activity_stock_latest.json")
REPORT_REGISTRY_FILE = os.path.join(JSON_DIR, "report_registry_latest.json")
RESTOCK_ROUTE_REQUEST_FILE = os.path.join(JSON_DIR, "stock_restock_route_latest.json")
RESTOCK_ROUTE_RESULT_FILE = os.path.join(JSON_DIR, "stock_restock_route_result_latest.json")
RESTOCK_SCRIPT = os.path.join(PROJECT_DIR, "Grow24_AI", "marketplaces", "amazon", "seller_api", "inventory", "stock_restock_v1.0.py")
RESTOCK_ACTIVITY_LOG_FILE = os.path.join(JSON_DIR, "stock_activity_log.json")
CONTROL_CONFIG_FILE = os.path.join(PROJECT_DIR, "config_stock_control.json")

MARKETPLACE_ID = "A21TJRUUN4KGV"
SELLER_ID = "A2AC2AS9R9CBEA"
SP_ENDPOINT = "https://sellingpartnerapi-eu.amazon.com"

SSL_CONTEXT = None
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

SP_CREDS = json.load(open(SP_CREDS_FILE, encoding="utf-8"))["sp_api_credentials"]
_token = None
_expiry = None


def load_json(path, default=None):
    if default is None:
        default = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return default


def default_stock_control_config():
    return {
        "schema_type": "stock_control",
        "schema_version": "1.0",
        "scope": "seller_listing_only",
        "default_target_stock": 1000,
        "default_minimum_threshold": 1,
        "manual_entries": []
    }


def load_stock_control_config():
    cfg = load_json(CONTROL_CONFIG_FILE, default_stock_control_config())
    cfg.setdefault("schema_type", "stock_control")
    cfg.setdefault("schema_version", "1.0")
    cfg["scope"] = "seller_listing_only"
    cfg["default_target_stock"] = int(cfg.get("default_target_stock", 1000) or 1000)
    cfg["default_minimum_threshold"] = int(cfg.get("default_minimum_threshold", 1) or 1)
    cfg["manual_entries"] = [
        {
            "type": str(entry.get("type", "")).strip().lower(),
            "value": str(entry.get("value", "")).strip(),
            "excluded": bool(entry.get("excluded", False)),
            "created_at": entry.get("created_at", ""),
            "updated_at": entry.get("updated_at", ""),
        }
        for entry in cfg.get("manual_entries", [])
        if str(entry.get("type", "")).strip().lower() in ("asin", "sku") and str(entry.get("value", "")).strip()
    ]
    if not os.path.exists(CONTROL_CONFIG_FILE):
        with open(CONTROL_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    return cfg


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


def find_latest_json_file(filename):
    for folder in report_folders:
        candidate = os.path.join(REPORT_BASE, folder, "Json", filename)
        if os.path.exists(candidate):
            return candidate
    return os.path.join(JSON_DIR, filename)


def get_token():
    global _token, _expiry
    if _token and _expiry and datetime.now() < _expiry:
        return _token
    data = urlencode({
        "grant_type": "refresh_token",
        "refresh_token": SP_CREDS["refresh_token"],
        "client_id": SP_CREDS["lwa_client_id"],
        "client_secret": SP_CREDS["lwa_client_secret"]
    }).encode()
    req = Request(SP_CREDS["token_url"], data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    result = json.loads(urlopen(req, context=SSL_CONTEXT).read().decode())
    _token = result["access_token"]
    _expiry = datetime.now() + timedelta(seconds=result["expires_in"] - 60)
    return _token


def fetch_mfn_stock(sku):
    token = get_token()
    url = (
        f"{SP_ENDPOINT}/listings/2021-08-01/items/{SELLER_ID}/{quote(sku)}"
        f"?marketplaceIds={MARKETPLACE_ID}&includedData=fulfillmentAvailability,attributes"
    )
    headers = {
        "x-amz-access-token": token,
        "x-amz-date": datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"),
        "Host": "sellingpartnerapi-eu.amazon.com",
    }
    req = Request(url, headers=headers)
    resp = urlopen(req, context=SSL_CONTEXT)
    result = json.loads(resp.read().decode())
    for item in result.get("fulfillmentAvailability", []):
        if item.get("fulfillmentChannelCode") == "DEFAULT":
            return int(item.get("quantity", 0) or 0)
    attrs = result.get("attributes", {})
    for item in attrs.get("fulfillment_availability", []) if isinstance(attrs.get("fulfillment_availability", []), list) else []:
        if item.get("fulfillment_channel_code") == "DEFAULT":
            return int(item.get("quantity", 0) or 0)
    return 0


def get_asin_sku_map():
    ads_file = find_latest_json_file("sp_product_ads_list.json")
    ads_rows = load_json(ads_file, [])
    sku_map = {}
    asin_skus = {}
    for row in ads_rows:
        sku = str(row.get("sku", "")).strip()
        asin = str(row.get("asin", "")).strip()
        if not sku:
            continue
        sku_map[sku] = asin
        if asin:
            asin_skus.setdefault(asin, [])
            if sku not in asin_skus[asin]:
                asin_skus[asin].append(sku)
    return sku_map, asin_skus, [relative_path(ads_file)]


def get_sales_map():
    sales_file = find_latest_json_file("sp_advertisedproduct_daily.json")
    rows = load_json(sales_file, [])
    sales_map = {}
    for row in rows:
        asin = str(row.get("advertisedAsin", "")).strip()
        if not asin:
            continue
        item = sales_map.setdefault(asin, {"sales7d": 0.0, "orders7d": 0})
        item["sales7d"] += float(row.get("sales7d", 0) or 0)
        item["orders7d"] += int(row.get("purchases7d", 0) or 0)
    return sales_map, [relative_path(sales_file)]


def run_live_snapshot(threshold):
    sku_map, asin_skus, source_files = get_asin_sku_map()
    sales_map, sales_sources = get_sales_map()
    source_files.extend(sales_sources)

    mfn_stock = {}
    api_errors = []
    unique_skus = list({sku for sku in sku_map.keys() if sku})
    for index, sku in enumerate(unique_skus):
        try:
            mfn_stock[sku] = fetch_mfn_stock(sku)
        except HTTPError as e:
            api_errors.append(f"{sku}: HTTP {e.code}")
        except URLError as e:
            api_errors.append(f"{sku}: {str(e.reason)[:60]}")
        except Exception as e:
            api_errors.append(f"{sku}: {str(e)[:60]}")
        if index and index % 50 == 0:
            time.sleep(0.5)
        time.sleep(0.25)

    combined = []
    zero_stock = []
    low_stock = []
    healthy_count = 0
    for asin, skus in asin_skus.items():
        mfn_total = sum(int(mfn_stock.get(sku, 0) or 0) for sku in skus)
        total_stock = mfn_total
        sales = sales_map.get(asin, {})
        item = {
            "asin": asin,
            "sku": skus[0][:25] if skus else "",
            "fba_stock": 0,
            "mnf_stock": mfn_total,
            "total_stock": total_stock,
            "stock_status": "OUT OF STOCK" if total_stock == 0 else "LOW STOCK" if total_stock <= threshold else "HEALTHY",
            "sales7d": round(float(sales.get("sales7d", 0) or 0), 2),
            "orders7d": int(sales.get("orders7d", 0) or 0),
            "recommendation": "Auto stock seller listing" if total_stock <= threshold else "Monitor stock"
        }
        combined.append(item)
        legacy_item = {
            "asin": item["asin"],
            "sku": item["sku"],
            "fba_stock": item["fba_stock"],
            "mnf_stock": item["mnf_stock"],
            "total_stock": item["total_stock"],
        }
        if total_stock == 0:
            zero_stock.append(legacy_item)
        elif total_stock <= threshold:
            low_stock.append(legacy_item)
        else:
            healthy_count += 1

    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "threshold": threshold,
        "total": len(combined),
        "zero_stock": zero_stock,
        "low_stock": low_stock,
        "healthy_count": healthy_count,
        "results": combined,
        "run_errors": api_errors,
        "input_sources": source_files,
        "scope": "seller_listing_only",
    }
    return snapshot


def enrich_from_status(status_data):
    threshold = int(status_data.get("threshold", 5) or 5)
    sales_map, sales_sources = get_sales_map()
    combined = []
    seen = set()
    zero_stock = list(status_data.get("zero_stock", []))
    low_stock = list(status_data.get("low_stock", []))
    for entry in zero_stock + low_stock:
        asin = entry.get("asin", "")
        sales = sales_map.get(asin, {})
        total_stock = int(entry.get("total_stock", 0) or 0)
        combined.append({
            "asin": asin,
            "sku": str(entry.get("sku", ""))[:25],
            "fba_stock": int(entry.get("fba_stock", 0) or 0),
            "mnf_stock": int(entry.get("mnf_stock", 0) or 0),
            "total_stock": total_stock,
            "stock_status": "OUT OF STOCK" if total_stock == 0 else "LOW STOCK",
            "sales7d": round(float(sales.get("sales7d", 0) or 0), 2),
            "orders7d": int(sales.get("orders7d", 0) or 0),
            "recommendation": "Auto stock seller listing"
        })
        seen.add(asin)
    total_count = int(status_data.get("total", 0) or 0)
    inferred_healthy = max(total_count - len(zero_stock) - len(low_stock), 0)
    healthy_count = int(status_data.get("healthy_count", inferred_healthy) or 0)
    if total_count and healthy_count > total_count:
        healthy_count = inferred_healthy
    return {
        "timestamp": datetime.now().isoformat(),
        "threshold": threshold,
        "total": total_count or (healthy_count + len(zero_stock) + len(low_stock)),
        "zero_stock": zero_stock,
        "low_stock": low_stock,
        "healthy_count": healthy_count,
        "results": combined,
        "run_errors": [],
        "input_sources": sales_sources,
        "scope": "seller_listing_only",
    }


def build_legacy_payload(snapshot):
    return {
        "timestamp": snapshot.get("timestamp", datetime.now().isoformat()),
        "threshold": int(snapshot.get("threshold", 5) or 5),
        "total": int(snapshot.get("total", 0) or 0),
        "zero_stock": snapshot.get("zero_stock", []),
        "low_stock": snapshot.get("low_stock", []),
        "healthy_count": int(snapshot.get("healthy_count", 0) or 0),
    }


def build_restock_route_requests(snapshot, started_at, control_config):
    requests = []
    threshold = int(snapshot.get("threshold", 5) or 5)
    manual_entries = control_config.get("manual_entries", [])
    asin_rules = {
        str(entry.get("value", "")).strip(): entry
        for entry in manual_entries
        if str(entry.get("type", "")).strip().lower() == "asin"
    }
    for item in snapshot.get("results", []):
        if int(item.get("total_stock", 0) or 0) > threshold:
            continue
        asin = str(item.get("asin", "")).strip()
        asin_rule = asin_rules.get(asin, {})
        if bool(asin_rule.get("excluded", False)):
            continue
        requests.append({
            "asin": asin,
            "sku": item.get("sku", ""),
            "stock_status": item.get("stock_status", ""),
            "current_stock": int(item.get("total_stock", 0) or 0),
            "sales7d_rs": round(float(item.get("sales7d", 0) or 0), 2),
            "target_stock": int(control_config.get("default_target_stock", 1000) or 1000),
            "recommendation": "Auto stock seller listing"
        })
    payload = {
        "schema_type": "action_route_request",
        "schema_version": "1.0",
        "route_run_id": f"{FEATURE_KEY}_route_{started_at.strftime('%Y%m%d_%H%M%S')}",
        "generated_at": datetime.now().isoformat(),
        "source_feature_key": FEATURE_KEY,
        "source_feature_name": FEATURE_NAME,
        "action_engine": "stock_restock",
        "requests": requests
    }
    history_file = save_json_pair(RESTOCK_ROUTE_REQUEST_FILE, "stock_restock_route", payload, started_at)
    return payload, history_file


def execute_restock_routes(route_payload, started_at, auto_action_enabled=True):
    result = {
        "route_type": "stock_restock_auto",
        "engine": "stock_restock",
        "generated_at": datetime.now().isoformat(),
        "request_count": len(route_payload.get("requests", [])),
        "status": "skipped",
        "reason": "",
        "actions": []
    }
    if not route_payload.get("requests"):
        result["reason"] = "No seller listing items qualified for auto stock."
        return result, save_json_pair(RESTOCK_ROUTE_RESULT_FILE, "stock_restock_route_result", result, started_at)
    if not auto_action_enabled:
        result["status"] = "pending"
        result["reason"] = "Self action disabled for stock feature."
        return result, save_json_pair(RESTOCK_ROUTE_RESULT_FILE, "stock_restock_route_result", result, started_at)
    if not os.path.exists(RESTOCK_SCRIPT):
        result["status"] = "failed"
        result["reason"] = "Restock script not found."
        return result, save_json_pair(RESTOCK_ROUTE_RESULT_FILE, "stock_restock_route_result", result, started_at)

    cmd = [sys.executable, RESTOCK_SCRIPT, "--execute"]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_DIR)
    result["status"] = "executed" if proc.returncode == 0 else "failed"
    result["reason"] = (
        "Seller listing auto stock executed from stock control panel."
        if result["status"] == "executed"
        else "Could not execute seller listing auto stock."
    )
    result["return_code"] = proc.returncode
    result["command"] = " ".join(cmd)
    result["output_file"] = relative_path(RESTOCK_ACTIVITY_LOG_FILE) if os.path.exists(RESTOCK_ACTIVITY_LOG_FILE) else ""
    result["actions"] = [{
        "action": "AUTO_STOCK_SELLER_LISTING",
        "status": result["status"],
        "asin": item.get("asin", ""),
        "sku": item.get("sku", ""),
        "reason": item.get("stock_status", ""),
        "current_stock": item.get("current_stock", 0),
        "target_stock": item.get("target_stock", 1000),
    } for item in route_payload.get("requests", [])[:10]]
    return result, save_json_pair(RESTOCK_ROUTE_RESULT_FILE, "stock_restock_route_result", result, started_at)


def summarize_action_routes(route_result, route_request_file, route_request_history_file, route_result_file, route_result_history_file):
    return {
        "status": route_result.get("status", "skipped"),
        "reason": route_result.get("reason", ""),
        "request_count": int(route_result.get("request_count", 0) or 0),
        "actions": route_result.get("actions", []),
        "files": [
            relative_path(path) for path in [
                route_request_file,
                route_request_history_file,
                route_result_file,
                route_result_history_file,
            ] if path
        ],
        "routes": [{
            "route_type": route_result.get("route_type", "stock_restock_auto"),
            "engine": route_result.get("engine", "stock_restock"),
            "status": route_result.get("status", "skipped"),
            "request_count": int(route_result.get("request_count", 0) or 0),
            "actions": route_result.get("actions", []),
            "reason": route_result.get("reason", "")
        }]
    }


def get_status_and_impact(snapshot):
    risk_count = len(snapshot.get("zero_stock", [])) + len(snapshot.get("low_stock", []))
    if snapshot.get("run_errors") and not snapshot.get("results") and not risk_count:
        return "failed", "critical"
    if snapshot.get("run_errors"):
        return "partial", "high"
    if len(snapshot.get("zero_stock", [])):
        return "warning", "high"
    if len(snapshot.get("low_stock", [])):
        return "warning", "medium"
    return "success", "low"


def build_impact_summary(snapshot, history_file):
    status, impact_level = get_status_and_impact(snapshot)
    results = snapshot.get("results", [])
    action_routing = snapshot.get("action_routing", {})
    risk_items = sorted(results, key=lambda x: float(x.get("sales7d", 0) or 0), reverse=True)
    zero_count = len(snapshot.get("zero_stock", []))
    low_count = len(snapshot.get("low_stock", []))
    risk_count = zero_count + low_count
    revenue_at_risk = round(sum(float(item.get("sales7d", 0) or 0) for item in risk_items), 2)
    healthy_count = int(snapshot.get("healthy_count", 0) or 0)
    ai_headline = (
        f"AI auto-stocked seller listings for {risk_count} risky ASIN(s)."
        if action_routing.get("status") == "executed"
        else f"AI found {risk_count} risky ASIN(s), but seller auto stock is {action_routing.get('status', 'pending')}."
        if risk_count else
        "AI found no seller listing stock risk that needed action in this cycle."
    )
    top_risks = []
    for item in risk_items[:10]:
        top_risks.append({
            "asin": item.get("asin", ""),
            "sku": item.get("sku", ""),
            "sales7d_rs": round(float(item.get("sales7d", 0) or 0), 2),
            "buy_box_status": item.get("stock_status", ""),
            "competitor_count": int(item.get("total_stock", 0) or 0),
            "price_gap_rs": 0,
            "recommendation": item.get("recommendation", "")
        })
    return {
        "schema_type": "impact_summary",
        "schema_version": "1.0",
        "feature_id": FEATURE_ID,
        "feature_key": FEATURE_KEY,
        "feature_name": FEATURE_NAME,
        "module_group": MODULE_GROUP,
        "generated_at": snapshot.get("timestamp", datetime.now().isoformat()),
        "period": "manual",
        "status": status,
        "impact_level": impact_level,
        "business_areas": ["inventory", "availability", "revenue_protection"],
        "headline": (
            f"Stock risk detected on {risk_count} ASIN(s)."
            if risk_count else
            "Stock monitor found no low-stock or out-of-stock ASIN."
        ),
        "summary_metrics": {
            "profit_impact_rs": 0,
            "loss_prevented_rs": 0,
            "waste_blocked_rs": 0,
            "revenue_protected_rs": 0,
            "ai_action_sales_protected_rs": 0,
            "ai_actions_executed_count": 1 if action_routing.get("status") == "executed" else 0,
            "ai_actions_identified_count": int(action_routing.get("request_count", 0) or 0),
            "tracked_asins_count": int(snapshot.get("total", 0) or 0),
            "risk_item_count": risk_count,
            "zero_stock_count": zero_count,
            "low_stock_count": low_count,
            "healthy_count": healthy_count,
            "revenue_at_risk_7d_rs": revenue_at_risk
        },
        "positive_impacts": [{
            "type": "healthy_inventory",
            "message": f"{healthy_count} ASIN(s) currently look healthy on stock.",
            "estimated_sales7d_rs": 0
        }] if healthy_count else [],
        "negative_impacts": [{
            "type": "stock_risk",
            "message": f"{zero_count} ASIN(s) are out of stock and {low_count} ASIN(s) are below threshold.",
            "estimated_sales7d_at_risk_rs": revenue_at_risk
        }] if risk_count else [],
        "top_risks": top_risks,
        "ai_action_summary": {
            "headline": ai_headline,
            "status": action_routing.get("status", "not_routed"),
            "actions_identified": int(action_routing.get("request_count", 0) or 0),
            "actions_executed": 1 if action_routing.get("status") == "executed" else 0,
            "expected_sales_protected_rs": 0,
            "items": []
        },
        "recommendations": [
            "Seller listing stock is controlled from the stock control panel.",
            "Excluded products remain visible in the panel but will not auto stock.",
            f"Action routing status: {action_routing.get('status', 'not_routed')}."
        ],
        "detail_ref": {
            "raw_file": relative_path(STATUS_FILE),
            "detail_file": relative_path(history_file),
            "supporting_report": relative_path(STATUS_FILE)
        }
    }


def build_activity_summary(snapshot, history_file, impact_file, started_at, duration_sec):
    action_routing = snapshot.get("action_routing", {})
    zero_count = len(snapshot.get("zero_stock", []))
    low_count = len(snapshot.get("low_stock", []))
    warnings = []
    if zero_count:
        warnings.append(f"{zero_count} ASIN(s) are out of stock.")
    if low_count:
        warnings.append(f"{low_count} ASIN(s) are below stock threshold.")
    action_history = [{
        "route_type": route.get("route_type", route.get("engine", "")),
        "engine": route.get("engine", ""),
        "status": route.get("status", ""),
        "request_count": int(route.get("request_count", 0) or 0),
        "actions_executed": 1 if route.get("status") == "executed" else 0,
        "reason": route.get("reason", "")
    } for route in action_routing.get("routes", [])]
    status, _impact_level = get_status_and_impact(snapshot)
    output_files = [
        relative_path(STATUS_FILE),
        relative_path(history_file),
        relative_path(impact_file),
        relative_path(ACTIVITY_LATEST_FILE),
        relative_path(REPORT_REGISTRY_FILE),
    ] + [path for path in action_routing.get("files", []) if path]
    return {
        "schema_type": "activity_summary",
        "schema_version": "1.0",
        "feature_id": FEATURE_ID,
        "feature_key": FEATURE_KEY,
        "feature_name": FEATURE_NAME,
        "module_group": MODULE_GROUP,
        "run_id": f"{FEATURE_KEY}_{started_at.strftime('%Y%m%d_%H%M%S')}",
        "generated_at": snapshot.get("timestamp", datetime.now().isoformat()),
        "status": status,
        "run_mode": "manual",
        "duration_sec": round(duration_sec, 2),
        "freshness_hours": 2,
        "needs_review": bool(warnings),
        "input_sources": snapshot.get("input_sources", []),
        "output_files": output_files,
        "counts": {
            "items_scanned": int(snapshot.get("total", 0) or 0),
            "items_processed": int(snapshot.get("total", 0) or 0),
            "alerts_generated": len(warnings),
            "approvals_needed": 0,
            "warnings": len(warnings),
            "errors": len(snapshot.get("run_errors", [])),
            "action_routes_created": int(action_routing.get("request_count", 0) or 0),
            "action_routes_executed": 1 if action_routing.get("status") == "executed" else 0
        },
        "run_events": [
            "Loaded seller listing stock position from Listings API or source status file.",
            "Saved legacy stock_status.json for compatibility.",
            "Published stock impact summary, activity summary, and report registry entry.",
            f"Seller auto stock routing status: {action_routing.get('status', 'not_routed')}."
        ],
        "warnings_list": warnings,
        "errors_list": snapshot.get("run_errors", []),
        "review_items": {
            "user_review": warnings + ([action_routing.get("reason", "")] if action_routing.get("reason") else []),
            "developer_review": [],
            "blocked_items": []
        },
        "action_history": action_history,
        "source_report_folder": LATEST_REPORT,
        "notes": "Compatibility migration: legacy stock_status.json remains available while auto stock control is now panel-driven and seller listing only."
    }


def build_registry_entry(impact_summary, history_file):
    impact_level = impact_summary.get("impact_level", "low")
    priority_score = 80 if impact_level == "critical" else 70 if impact_level == "high" else 50 if impact_level == "medium" else 25
    return {
        "schema_type": "registry_entry",
        "schema_version": "1.0",
        "feature_id": FEATURE_ID,
        "feature_key": FEATURE_KEY,
        "feature_name": FEATURE_NAME,
        "module_group": MODULE_GROUP,
        "files": {
            "raw_output": relative_path(STATUS_FILE),
            "impact_summary": relative_path(IMPACT_LATEST_FILE),
            "activity_summary": relative_path(ACTIVITY_LATEST_FILE),
            "detail_report": relative_path(history_file)
        },
        "generated_at": impact_summary.get("generated_at", datetime.now().isoformat()),
        "dashboard_visibility": {
            "show_on_main": True,
            "show_on_activity": True,
            "show_on_home": impact_level in ("high", "critical"),
            "main_section": "Critical Impact Alerts",
            "activity_section": "Run Status"
        },
        "importance": {
            "status": impact_summary.get("status", "success"),
            "impact_level": impact_level,
            "priority_score": priority_score
        },
        "display_rules": {
            "headline": impact_summary.get("headline", ""),
            "badge": impact_summary.get("impact_level", "low").upper(),
            "default_view": "impact_first"
        },
        "review_state": {
            "needs_review": impact_summary.get("status") in ("warning", "failed", "partial"),
            "has_warnings": impact_summary.get("status") == "warning"
        }
    }


def update_report_registry(entry):
    registry = load_json(REPORT_REGISTRY_FILE, {"schema_type": "report_registry", "schema_version": "1.0", "generated_at": "", "entries": []})
    entries = [item for item in registry.get("entries", []) if item.get("feature_key") != FEATURE_KEY]
    entries.append(entry)
    entries.sort(key=lambda item: item.get("feature_key", ""))
    registry["generated_at"] = datetime.now().isoformat()
    registry["entries"] = entries
    with open(REPORT_REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)


def save_new_standard_outputs(snapshot, started_at, duration_sec):
    history_file = save_json_pair(STATUS_FILE, "stock_status", build_legacy_payload(snapshot), started_at)
    impact_summary = build_impact_summary(snapshot, history_file)
    impact_history_file = save_json_pair(IMPACT_LATEST_FILE, "impact_stock", impact_summary, started_at)
    activity_summary = build_activity_summary(snapshot, history_file, impact_history_file, started_at, duration_sec)
    save_json_pair(ACTIVITY_LATEST_FILE, "activity_stock", activity_summary, started_at)
    update_report_registry(build_registry_entry(impact_summary, history_file))
    return impact_summary, activity_summary


def main():
    parser = argparse.ArgumentParser(description="Grow24 AI Stock Monitor v1.1")
    parser.add_argument("--threshold", type=int, default=0, help="Override panel minimum threshold for this run")
    parser.add_argument("--source-status", default="", help="Use existing stock_status.json as input instead of live API")
    parser.add_argument("--no-action", action="store_true", help="Do not trigger seller listing auto stock")
    args = parser.parse_args()

    started_at = datetime.now()
    control_config = load_stock_control_config()
    run_threshold = int(args.threshold or control_config.get("default_minimum_threshold", 1) or 1)
    if args.source_status:
        snapshot = enrich_from_status(load_json(args.source_status, {}))
        snapshot["threshold"] = run_threshold or snapshot.get("threshold", 1)
    else:
        snapshot = run_live_snapshot(run_threshold)

    route_payload, route_request_history_file = build_restock_route_requests(snapshot, started_at, control_config)
    route_request_file = RESTOCK_ROUTE_REQUEST_FILE
    route_result, route_result_history_file = execute_restock_routes(route_payload, started_at, auto_action_enabled=not args.no_action)
    snapshot["action_routing"] = summarize_action_routes(
        route_result,
        route_request_file,
        route_request_history_file,
        RESTOCK_ROUTE_RESULT_FILE,
        route_result_history_file,
    )

    duration_sec = (datetime.now() - started_at).total_seconds()
    save_new_standard_outputs(snapshot, started_at, duration_sec)
    return 0


if __name__ == "__main__":
    sys.exit(main())
