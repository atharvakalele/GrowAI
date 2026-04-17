#!/usr/bin/env python3
"""
Grow24 AI - Buy Box Monitor v1.1
================================
Checks Buy Box status for ASINs from current ads catalog, routes pricing and
listing recovery actions, and publishes dashboard-ready summaries.
"""

import json
import os
import ssl
import subprocess
import sys
import time
from datetime import datetime, timedelta
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
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
            raise RuntimeError("Project root not found for buy box monitor")
        current = parent


PROJECT_DIR = find_project_dir(SCRIPT_DIR)
SP_CREDS_FILE = os.path.join(PROJECT_DIR, "sp_api_credentials.json")

REPORT_BASE = os.path.join(PROJECT_DIR, "ClaudeCode", "Report")
report_folders = [f for f in os.listdir(REPORT_BASE) if os.path.isdir(os.path.join(REPORT_BASE, f))]
report_folders.sort(key=lambda x: os.path.getmtime(os.path.join(REPORT_BASE, x)), reverse=True)
LATEST_REPORT = report_folders[0] if report_folders else datetime.now().strftime("%d %B %Y")
JSON_DIR = os.path.join(REPORT_BASE, LATEST_REPORT, "Json")

FEATURE_ID = "M02"
FEATURE_KEY = "buybox"
FEATURE_NAME = "Buy Box Monitor"
MODULE_GROUP = "market_intelligence"

LATEST_FILE = os.path.join(JSON_DIR, "buy_box_status.json")
IMPACT_LATEST_FILE = os.path.join(JSON_DIR, "impact_buybox_latest.json")
ACTIVITY_LATEST_FILE = os.path.join(JSON_DIR, "activity_buybox_latest.json")
REPORT_REGISTRY_FILE = os.path.join(JSON_DIR, "report_registry_latest.json")
PRICE_ROUTE_REQUEST_FILE = os.path.join(JSON_DIR, "buybox_price_route_latest.json")
PRICE_ROUTE_RESULT_FILE = os.path.join(JSON_DIR, "buybox_price_route_result_latest.json")
LISTING_ROUTE_REQUEST_FILE = os.path.join(JSON_DIR, "buybox_listing_route_latest.json")
LISTING_ROUTE_RESULT_FILE = os.path.join(JSON_DIR, "buybox_listing_route_result_latest.json")
PRICE_OPTIMIZER_SCRIPT = os.path.join(
    PROJECT_DIR, "Grow24_AI", "marketplaces", "amazon", "seller_api", "pricing", "price_optimizer_v1.0.py"
)
PRICE_OPTIMIZER_STATUS_FILE = os.path.join(JSON_DIR, "price_optimizer_status.json")
LISTING_RECOVERY_SCRIPT = os.path.join(
    PROJECT_DIR, "Grow24_AI", "marketplaces", "amazon", "seller_api", "listing_health", "listing_recovery_v1.0.py"
)
LISTING_RECOVERY_STATUS_FILE = os.path.join(JSON_DIR, "listing_recovery_status.json")

MARKETPLACE_ID = "A21TJRUUN4KGV"
OUR_SELLER_ID = "A2AC2AS9R9CBEA"
SP_ENDPOINT = "https://sellingpartnerapi-eu.amazon.com"
TOKEN_URL = "https://api.amazon.com/auth/o2/token"
BATCH_SIZE = 20
DELAY = 32

SSL_CONTEXT = None
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

SP = json.load(open(SP_CREDS_FILE, encoding="utf-8"))["sp_api_credentials"]
_cached_token = None
_token_expiry = None


def load_json(path, default=None):
    if default is None:
        default = {}
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


def fetch_competitive_batch(asin_list):
    try:
        token = get_token()
    except (URLError, RuntimeError) as e:
        return None, str(e)
    body = {"requests": []}
    for asin in asin_list:
        body["requests"].append({
            "asin": asin,
            "marketplaceId": MARKETPLACE_ID,
            "includedData": ["featuredBuyingOptions", "lowestPricedOffers", "referencePrices"],
            "method": "GET",
            "uri": "/products/pricing/2022-05-01/items/competitiveSummary"
        })
    url = f"{SP_ENDPOINT}/batches/products/pricing/2022-05-01/items/competitiveSummary"
    headers = {
        "x-amz-access-token": token,
        "x-amz-date": datetime.utcnow().strftime('%Y%m%dT%H%M%SZ'),
        "Content-Type": "application/json",
        "Host": "sellingpartnerapi-eu.amazon.com"
    }
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    try:
        resp = urlopen(req, context=SSL_CONTEXT)
        return json.loads(resp.read().decode()), ""
    except HTTPError as e:
        return None, e.read().decode()[:300]


def find_latest_json_file(filename):
    for folder in report_folders:
        candidate = os.path.join(REPORT_BASE, folder, "Json", filename)
        if os.path.exists(candidate):
            return candidate
    return os.path.join(JSON_DIR, filename)


def get_asin_pool():
    ads_file = find_latest_json_file("sp_product_ads_list.json")
    perf_file = find_latest_json_file("sp_advertisedproduct_daily.json")
    ads = load_json(ads_file, [])
    perf = load_json(perf_file, [])
    perf_map = {}
    for row in perf:
        asin = str(row.get("advertisedAsin", "")).strip()
        if not asin:
            continue
        item = perf_map.setdefault(asin, {"sales7d": 0.0, "orders7d": 0})
        item["sales7d"] += float(row.get("sales7d", 0) or 0)
        item["orders7d"] += int(row.get("purchases7d", 0) or 0)

    seen = {}
    for row in ads:
        asin = str(row.get("asin", "")).strip()
        if not asin:
            continue
        if asin not in seen:
            item = {
                "asin": asin,
                "sku": row.get("sku", ""),
                "sales7d": 0.0,
                "orders7d": 0
            }
            item.update(perf_map.get(asin, {}))
            seen[asin] = item
    return list(seen.values()), [relative_path(ads_file), relative_path(perf_file)]


def analyze_buybox(response_body):
    asin = response_body.get("asin", "")
    result = {
        "asin": asin,
        "buy_box_status": "UNKNOWN",
        "our_price": 0.0,
        "bb_price": 0.0,
        "bb_seller": "",
        "bb_fulfillment": "",
        "lowest_price": 0.0,
        "lowest_seller": "",
        "lowest_fulfillment": "",
        "competitor_count": 0,
        "price_gap_rs": 0.0,
        "price_gap_pct": 0.0,
        "action_priority": "LOW",
        "recommendation": "Monitor",
        "signals": [],
        "reason": "",
    }
    fbo = response_body.get("featuredBuyingOptions", [])
    for opt in fbo:
        offers = opt.get("segmentedFeaturedOffers", [])
        for offer in offers:
            price = float(offer.get("listingPrice", {}).get("amount", 0) or 0)
            seller = offer.get("sellerId", "")
            fulfillment = offer.get("fulfillmentType", "")
            result["bb_price"] = price
            result["bb_seller"] = seller
            result["bb_fulfillment"] = fulfillment
            result["buy_box_status"] = "WON" if seller == OUR_SELLER_ID else "LOST"
            if seller == OUR_SELLER_ID:
                result["our_price"] = price
            break
        if result["bb_seller"]:
            break

    competitors = []
    for offer_group in response_body.get("lowestPricedOffers", []):
        for offer in offer_group.get("offers", []):
            price = float(offer.get("listingPrice", {}).get("amount", 0) or 0)
            seller = offer.get("sellerId", "")
            fulfillment = offer.get("fulfillmentType", "")
            if seller == OUR_SELLER_ID:
                result["our_price"] = price
            competitors.append({"price": price, "seller": seller, "fulfillment": fulfillment})
    result["competitor_count"] = len([c for c in competitors if c["seller"] != OUR_SELLER_ID])
    if competitors:
        cheapest = min(competitors, key=lambda x: x["price"])
        result["lowest_price"] = cheapest["price"]
        result["lowest_seller"] = cheapest["seller"]
        result["lowest_fulfillment"] = cheapest["fulfillment"]
    if not fbo:
        result["buy_box_status"] = "NO_BUYBOX"
        result["action_priority"] = "HIGH"
        result["recommendation"] = "Check listing suppression, pricing, and availability"
        result["signals"].append("No Buy Box available")
        result["reason"] = "No Buy Box available (listing may be suppressed or inactive)"
        return result

    if result["our_price"] > 0 and result["bb_price"] > 0:
        gap_rs = result["our_price"] - result["bb_price"]
        gap_pct = (gap_rs / result["bb_price"] * 100) if result["bb_price"] > 0 else 0
        result["price_gap_rs"] = round(gap_rs, 2)
        result["price_gap_pct"] = round(gap_pct, 2)

    if result["buy_box_status"] == "LOST":
        result["action_priority"] = "HIGH"
        if result["price_gap_rs"] > 0:
            result["recommendation"] = "Lower price or coupon to recover Buy Box"
            result["signals"].append("Price disadvantage")
            result["reason"] = f"Price too high by Rs.{result['price_gap_rs']:.2f}"
        elif result["bb_fulfillment"] == "AFN" and result["lowest_fulfillment"] != "AFN":
            result["recommendation"] = "Check FBA / Prime competitiveness"
            result["signals"].append("Fulfillment disadvantage")
            result["reason"] = "Competitor has FBA advantage"
        else:
            result["recommendation"] = "Review listing health, seller metrics, and availability"
            result["signals"].append("Non-price Buy Box loss")
            result["reason"] = f"Lost Buy Box to seller {result['bb_seller'][:12]}"
    elif result["buy_box_status"] == "WON":
        if result["competitor_count"] == 0:
            result["recommendation"] = "Maintain; no direct competitor pressure"
            result["signals"].append("Only seller")
        else:
            result["recommendation"] = "Defend Buy Box and monitor frequently"
            result["signals"].append("Buy Box won")
    return result


def build_price_route_requests(results, started_at):
    route_run_id = f"{FEATURE_KEY}_price_route_{started_at.strftime('%Y%m%d_%H%M%S')}"
    requests = []
    for item in results:
        if item.get("buy_box_status") != "LOST":
            continue
        if not item.get("sku"):
            continue
        our_price = float(item.get("our_price", 0) or 0)
        bb_price = float(item.get("bb_price", 0) or 0)
        if our_price <= 0 or bb_price <= 0 or our_price <= bb_price:
            continue
        requests.append({
            "route_run_id": route_run_id,
            "source_feature_key": FEATURE_KEY,
            "source_feature_name": FEATURE_NAME,
            "action_family": "pricing",
            "target_engine": "price_optimizer",
            "issue_type": "buy_box_lost_price_gap",
            "asin": item.get("asin", ""),
            "sku": item.get("sku", ""),
            "current_price": round(our_price, 2),
            "lowest_competitor_price": round(bb_price, 2),
            "target_price": round(bb_price, 2),
            "price_gap_rs": round(float(item.get("price_gap_rs", 0) or 0), 2),
            "price_gap_pct": round(float(item.get("price_gap_pct", 0) or 0), 2),
            "sales7d_rs": round(float(item.get("sales7d", 0) or 0), 2),
            "buy_box_status": item.get("buy_box_status", ""),
            "recommendation": item.get("recommendation", ""),
            "signals": item.get("signals", []),
            "route_reason": f"Lost Buy Box with price gap of Rs.{item.get('price_gap_rs', 0):.2f}.",
            "auto_action_allowed": True
        })
    payload = {
        "schema_type": "action_route_request",
        "schema_version": "1.0",
        "route_run_id": route_run_id,
        "generated_at": datetime.now().isoformat(),
        "source_feature_key": FEATURE_KEY,
        "source_feature_name": FEATURE_NAME,
        "action_engine": "price_optimizer",
        "requests": requests
    }
    history_file = save_json_pair(PRICE_ROUTE_REQUEST_FILE, "buybox_price_route", payload, started_at)
    return payload, history_file


def build_listing_route_requests(results, started_at):
    route_run_id = f"{FEATURE_KEY}_listing_route_{started_at.strftime('%Y%m%d_%H%M%S')}"
    requests = []
    for item in results:
        if item.get("buy_box_status") != "NO_BUYBOX":
            continue
        if not item.get("sku"):
            continue
        requests.append({
            "route_run_id": route_run_id,
            "source_feature_key": FEATURE_KEY,
            "source_feature_name": FEATURE_NAME,
            "action_family": "listing_recovery",
            "target_engine": "listing_recovery",
            "issue_type": "no_buy_box_listing_check",
            "asin": item.get("asin", ""),
            "sku": item.get("sku", ""),
            "current_price": round(float(item.get("our_price", 0) or 0), 2),
            "sales7d_rs": round(float(item.get("sales7d", 0) or 0), 2),
            "buy_box_status": item.get("buy_box_status", ""),
            "recommendation": item.get("recommendation", ""),
            "signals": item.get("signals", []),
            "route_reason": "No Buy Box found; verify listing state and start recovery if needed.",
            "auto_action_allowed": True
        })
    payload = {
        "schema_type": "action_route_request",
        "schema_version": "1.0",
        "route_run_id": route_run_id,
        "generated_at": datetime.now().isoformat(),
        "source_feature_key": FEATURE_KEY,
        "source_feature_name": FEATURE_NAME,
        "action_engine": "listing_recovery",
        "requests": requests
    }
    history_file = save_json_pair(LISTING_ROUTE_REQUEST_FILE, "buybox_listing_route", payload, started_at)
    return payload, history_file


def execute_route(route_payload, route_history_file, started_at, route_kind):
    if route_kind == "pricing":
        latest_file = PRICE_ROUTE_RESULT_FILE
        prefix = "buybox_price_route_result"
        script = PRICE_OPTIMIZER_SCRIPT
        status_file = PRICE_OPTIMIZER_STATUS_FILE
        cmd = [sys.executable, script, "--route-file", route_history_file]
    else:
        latest_file = LISTING_ROUTE_RESULT_FILE
        prefix = "buybox_listing_route_result"
        script = LISTING_RECOVERY_SCRIPT
        status_file = LISTING_RECOVERY_STATUS_FILE
        cmd = [sys.executable, script, "--route-file", route_history_file]
    result = {
        "route_type": route_kind,
        "route_run_id": route_payload.get("route_run_id", ""),
        "generated_at": datetime.now().isoformat(),
        "engine": "price_optimizer" if route_kind == "pricing" else "listing_recovery",
        "request_count": len(route_payload.get("requests", [])),
        "status": "skipped",
        "reason": "",
        "actions": []
    }
    if not route_payload.get("requests"):
        result["reason"] = f"No {route_kind} routes qualified."
        return result, save_json_pair(latest_file, prefix, result, started_at)
    if not os.path.exists(script):
        result["status"] = "failed"
        result["reason"] = f"{route_kind} engine script not found."
        return result, save_json_pair(latest_file, prefix, result, started_at)
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_DIR)
    status_data = load_json(status_file, {})
    result["status"] = "executed" if proc.returncode == 0 else "failed"
    result["reason"] = f"{route_kind} route executed." if proc.returncode == 0 else f"{route_kind} route execution failed."
    result["command"] = " ".join(cmd)
    result["return_code"] = proc.returncode
    if route_kind == "pricing":
        result["actions"] = [
            action for action in status_data.get("actions", [])
            if action.get("route_run_id") == route_payload.get("route_run_id")
        ]
    else:
        result["actions"] = list(status_data.get("price_route", {}).get("actions", []))
        result["checked_items"] = status_data.get("checked_items", [])
    return result, save_json_pair(latest_file, prefix, result, started_at)


def summarize_action_routes(route_results):
    priority = {"failed": 5, "blocked": 4, "pending": 3, "executed": 2, "skipped": 1}
    status = "skipped"
    for route in route_results:
        if priority.get(route.get("status", "skipped"), 0) > priority.get(status, 0):
            status = route.get("status", "skipped")
    files = []
    for route in route_results:
        for key in ("request_file", "request_history_file", "result_file", "result_history_file"):
            if route.get(key):
                files.append(route.get(key))
    return {
        "status": status,
        "reason": " | ".join(route.get("reason", "") for route in route_results if route.get("reason")),
        "request_count": sum(int(route.get("request_count", 0) or 0) for route in route_results),
        "actions": [action for route in route_results for action in route.get("actions", [])],
        "files": files,
        "routes": route_results
    }


def get_status_and_impact(results, failed_asins, run_errors):
    lost = len([r for r in results if r.get("buy_box_status") == "LOST"])
    no_bb = len([r for r in results if r.get("buy_box_status") == "NO_BUYBOX"])
    if run_errors and not results:
        return "failed", "critical"
    if run_errors or failed_asins:
        return "partial", "high"
    if lost or no_bb:
        return "warning", "high"
    return "success", "low"


def build_impact_summary(snapshot, history_file):
    results = snapshot.get("results", [])
    failed_asins = snapshot.get("failed_asins", [])
    run_errors = snapshot.get("run_errors", [])
    action_routing = snapshot.get("action_routing", {})
    status, impact_level = get_status_and_impact(results, failed_asins, run_errors)
    lost = [r for r in results if r.get("buy_box_status") == "LOST"]
    no_bb = [r for r in results if r.get("buy_box_status") == "NO_BUYBOX"]
    won = [r for r in results if r.get("buy_box_status") == "WON"]
    risk_items = lost + no_bb
    revenue_at_risk = round(sum(float(r.get("sales7d", 0) or 0) for r in risk_items), 2)
    protected_revenue = round(sum(float(r.get("sales7d", 0) or 0) for r in won), 2)
    actions_taken = action_routing.get("actions", [])
    action_asins = {item.get("asin", "") for item in actions_taken if item.get("asin")}
    action_sales_protected = round(sum(float(r.get("sales7d", 0) or 0) for r in results if r.get("asin") in action_asins), 2)
    action_items = []
    for action in actions_taken[:10]:
        action_items.append({
            "asin": action.get("asin", ""),
            "sku": action.get("sku", ""),
            "action": action.get("action", ""),
            "status": action.get("status", ""),
            "old_price": round(float(action.get("old_price", 0) or 0), 2),
            "new_price": round(float(action.get("new_price", 0) or 0), 2),
            "reason": action.get("reason", "")
        })
    if actions_taken:
        ai_headline = f"AI executed {len(actions_taken)} Buy Box fix action(s) covering Rs.{action_sales_protected:.2f} 7-day sales."
    elif action_routing.get("request_count", 0):
        ai_headline = f"AI identified {action_routing.get('request_count', 0)} Buy Box action candidate(s), execution status: {action_routing.get('status', 'pending')}."
    else:
        ai_headline = "AI did not execute a Buy Box corrective action in this cycle."
    top_risks = []
    for item in sorted(risk_items, key=lambda x: float(x.get("sales7d", 0) or 0), reverse=True)[:10]:
        top_risks.append({
            "asin": item.get("asin", ""),
            "sku": item.get("sku", ""),
            "sales7d_rs": round(float(item.get("sales7d", 0) or 0), 2),
            "buy_box_status": item.get("buy_box_status", ""),
            "competitor_count": int(item.get("competitor_count", 0) or 0),
            "price_gap_rs": round(float(item.get("price_gap_rs", 0) or 0), 2),
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
        "business_areas": ["buy_box", "pricing", "listing_health", "revenue_protection"],
        "headline": f"Buy Box risk detected on {len(risk_items)} ASIN(s)." if risk_items else "Buy Box monitor found no immediate risk.",
        "summary_metrics": {
            "profit_impact_rs": 0,
            "loss_prevented_rs": 0,
            "waste_blocked_rs": 0,
            "revenue_protected_rs": protected_revenue,
            "ai_action_sales_protected_rs": action_sales_protected,
            "ai_actions_executed_count": len(actions_taken),
            "ai_actions_identified_count": int(action_routing.get("request_count", 0) or 0),
            "tracked_asins_count": len(results),
            "buy_box_won_count": len(won),
            "buy_box_lost_count": len(lost),
            "no_buy_box_count": len(no_bb),
            "revenue_at_risk_7d_rs": revenue_at_risk
        },
        "positive_impacts": [{
            "type": "buy_box_protected",
            "message": f"{len(won)} ASIN(s) currently hold Buy Box.",
            "estimated_sales7d_rs": protected_revenue
        }] if won else [],
        "negative_impacts": [{
            "type": "buy_box_risk",
            "message": f"{len(risk_items)} ASIN(s) need Buy Box or listing recovery action.",
            "estimated_sales7d_at_risk_rs": revenue_at_risk
        }] if risk_items else [],
        "top_risks": top_risks,
        "ai_action_summary": {
            "headline": ai_headline,
            "status": action_routing.get("status", "not_routed"),
            "actions_identified": int(action_routing.get("request_count", 0) or 0),
            "actions_executed": len(actions_taken),
            "expected_sales_protected_rs": action_sales_protected,
            "items": action_items
        },
        "recommendations": [
            "Price-gap Buy Box losses should route to price optimizer.",
            "No Buy Box items should route to listing recovery.",
            f"Action routing status: {action_routing.get('status', 'not_routed')}."
        ],
        "detail_ref": {
            "raw_file": relative_path(LATEST_FILE),
            "detail_file": relative_path(history_file),
            "supporting_report": relative_path(LATEST_FILE)
        }
    }


def build_activity_summary(snapshot, history_file, impact_history_file, started_at, duration_sec, input_sources):
    results = snapshot.get("results", [])
    failed_asins = snapshot.get("failed_asins", [])
    run_errors = snapshot.get("run_errors", [])
    action_routing = snapshot.get("action_routing", {})
    status, _impact_level = get_status_and_impact(results, failed_asins, run_errors)
    warnings = []
    lost_count = len([r for r in results if r.get("buy_box_status") == "LOST"])
    no_bb_count = len([r for r in results if r.get("buy_box_status") == "NO_BUYBOX"])
    if lost_count:
        warnings.append(f"{lost_count} ASIN(s) lost Buy Box.")
    if no_bb_count:
        warnings.append(f"{no_bb_count} ASIN(s) have no Buy Box.")
    action_history = []
    for route in action_routing.get("routes", []):
        action_history.append({
            "route_type": route.get("route_type", route.get("engine", "")),
            "engine": route.get("engine", ""),
            "status": route.get("status", ""),
            "request_count": int(route.get("request_count", 0) or 0),
            "actions_executed": len(route.get("actions", [])),
            "reason": route.get("reason", "")
        })
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
        "needs_review": bool(warnings or failed_asins or run_errors),
        "input_sources": input_sources,
        "output_files": [relative_path(LATEST_FILE), relative_path(history_file), relative_path(impact_history_file), relative_path(ACTIVITY_LATEST_FILE), relative_path(REPORT_REGISTRY_FILE)] + [path for path in action_routing.get("files", []) if path],
        "counts": {
            "items_scanned": len(results) + len(failed_asins),
            "items_processed": len(results),
            "alerts_generated": len(warnings),
            "approvals_needed": len(warnings),
            "warnings": len(warnings),
            "errors": len(run_errors),
            "action_routes_created": int(action_routing.get("request_count", 0) or 0),
            "action_routes_executed": len(action_routing.get("actions", []))
        },
        "run_events": [
            "Loaded ASINs from ads import data.",
            "Fetched Buy Box competitive summary from Amazon SP-API.",
            "Saved legacy buy_box_status.json output.",
            f"Action routing status: {action_routing.get('status', 'not_routed')}."
        ],
        "warnings_list": warnings,
        "errors_list": run_errors,
        "review_items": {
            "user_review": warnings,
            "developer_review": [],
            "blocked_items": failed_asins
        },
        "action_history": action_history,
        "source_report_folder": LATEST_REPORT,
        "notes": "Buy Box monitor now publishes impact and activity summaries beside legacy output."
    }


def build_registry_entry(impact_summary, activity_summary, history_file):
    status = impact_summary.get("status", "success")
    impact_level = impact_summary.get("impact_level", "low")
    priority_score = 80 if impact_level == "critical" else 70 if impact_level == "high" else 50
    return {
        "schema_type": "registry_entry",
        "schema_version": "1.0",
        "feature_id": FEATURE_ID,
        "feature_key": FEATURE_KEY,
        "feature_name": FEATURE_NAME,
        "module_group": MODULE_GROUP,
        "files": {
            "raw_output": relative_path(LATEST_FILE),
            "impact_summary": relative_path(IMPACT_LATEST_FILE),
            "activity_summary": relative_path(ACTIVITY_LATEST_FILE),
            "detail_report": relative_path(history_file)
        },
        "generated_at": impact_summary.get("generated_at", datetime.now().isoformat()),
        "dashboard_visibility": {
            "show_on_main": True,
            "show_on_activity": True,
            "show_on_home": True,
            "main_section": "Critical Impact Alerts",
            "activity_section": "Run Status"
        },
        "importance": {
            "status": status,
            "impact_level": impact_level,
            "priority_score": priority_score,
            "strategic_weight": 8,
            "is_critical": impact_level == "critical"
        },
        "display_rules": {
            "headline": impact_summary.get("headline", ""),
            "badge": "Review" if status in ("warning", "partial") else "Healthy",
            "sort_order": priority_score,
            "collapse_by_default": status == "success",
            "pin_to_top_when": ["critical", "failed", "warning"]
        },
        "review_state": {
            "needs_review": bool(activity_summary.get("needs_review", False)),
            "needs_approval": False,
            "has_warnings": bool(activity_summary.get("warnings_list")),
            "has_errors": bool(activity_summary.get("errors_list"))
        },
        "notes": {
            "dashboard_note": "Shows Buy Box status, AI fixes, and expected benefit of routed actions.",
            "developer_note": "Future-module compatible Buy Box monitor with shared action routing.",
            "migration_note": "Legacy buy_box_status.json remains available."
        }
    }


def update_report_registry(entry):
    registry = load_json(REPORT_REGISTRY_FILE, {
        "schema_type": "report_registry",
        "schema_version": "1.0",
        "generated_at": "",
        "entries": []
    })
    entries = [item for item in registry.get("entries", []) if item.get("feature_key") != FEATURE_KEY]
    entries.append(entry)
    registry["generated_at"] = datetime.now().isoformat()
    registry["entries"] = sorted(entries, key=lambda x: x.get("importance", {}).get("priority_score", 0), reverse=True)
    with open(REPORT_REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)


def save_new_standard_outputs(snapshot, history_file, started_at, duration_sec, input_sources):
    ts = started_at.strftime("%Y%m%d_%H%M%S")
    impact_history_file = os.path.join(JSON_DIR, f"impact_{FEATURE_KEY}_{ts}.json")
    activity_history_file = os.path.join(JSON_DIR, f"activity_{FEATURE_KEY}_{ts}.json")
    impact_summary = build_impact_summary(snapshot, history_file)
    with open(IMPACT_LATEST_FILE, "w", encoding="utf-8") as f:
        json.dump(impact_summary, f, indent=2, ensure_ascii=False)
    with open(impact_history_file, "w", encoding="utf-8") as f:
        json.dump(impact_summary, f, indent=2, ensure_ascii=False)
    activity_summary = build_activity_summary(snapshot, history_file, impact_history_file, started_at, duration_sec, input_sources)
    with open(ACTIVITY_LATEST_FILE, "w", encoding="utf-8") as f:
        json.dump(activity_summary, f, indent=2, ensure_ascii=False)
    with open(activity_history_file, "w", encoding="utf-8") as f:
        json.dump(activity_summary, f, indent=2, ensure_ascii=False)
    update_report_registry(build_registry_entry(impact_summary, activity_summary, history_file))


def main():
    started_at = datetime.now()
    asin_pool, input_sources = get_asin_pool()
    print("=" * 70)
    print("  Grow24 AI - Buy Box Monitor v1.1")
    print(f"  {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print("=" * 70)
    if not asin_pool:
        print("No ASINs found from ads data.")
        return 1
    print(f"\n  Tracking {len(asin_pool)} ASINs")
    batches = [asin_pool[i:i + BATCH_SIZE] for i in range(0, len(asin_pool), BATCH_SIZE)]
    results = []
    failed_asins = []
    run_errors = []
    for idx, batch in enumerate(batches, start=1):
        asin_list = [item["asin"] for item in batch]
        print(f"  Batch {idx}/{len(batches)}...", end=" ", flush=True)
        response, error_text = fetch_competitive_batch(asin_list)
        if not response:
            print("FAILED")
            failed_asins.extend(asin_list)
            if error_text:
                run_errors.append({"batch": idx, "asins": asin_list, "error": error_text})
        else:
            body_map = {}
            for item in response.get("responses", []):
                body = item.get("body", {})
                asin = body.get("asin", "")
                if asin:
                    body_map[asin] = body
            for meta in batch:
                asin = meta["asin"]
                if asin not in body_map:
                    failed_asins.append(asin)
                    continue
                analyzed = analyze_buybox(body_map[asin])
                analyzed.update({
                    "sku": meta.get("sku", ""),
                    "sales7d": round(float(meta.get("sales7d", 0) or 0), 2),
                    "orders7d": int(meta.get("orders7d", 0) or 0)
                })
                results.append(analyzed)
            print(f"{len(body_map)} items")
        if idx < len(batches):
            time.sleep(DELAY)
    results.sort(key=lambda x: (
        0 if x.get("action_priority") == "HIGH" else 1,
        -float(x.get("sales7d", 0) or 0)
    ))
    snapshot = {
        "version": "1.1",
        "timestamp": datetime.now().isoformat(),
        "tracked_asins": len(results),
        "failed_asins": failed_asins,
        "run_errors": run_errors,
        "results": results
    }

    with open(LATEST_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    history_file = os.path.join(JSON_DIR, f"buy_box_status_{started_at.strftime('%Y%m%d_%H%M%S')}.json")
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)

    price_route_payload, price_route_history_file = build_price_route_requests(results, started_at)
    price_route_result, price_route_result_history_file = execute_route(price_route_payload, price_route_history_file, started_at, "pricing")
    price_route_result["request_file"] = relative_path(PRICE_ROUTE_REQUEST_FILE)
    price_route_result["request_history_file"] = relative_path(price_route_history_file)
    price_route_result["result_file"] = relative_path(PRICE_ROUTE_RESULT_FILE)
    price_route_result["result_history_file"] = relative_path(price_route_result_history_file)

    listing_route_payload, listing_route_history_file = build_listing_route_requests(results, started_at)
    listing_route_result, listing_route_result_history_file = execute_route(listing_route_payload, listing_route_history_file, started_at, "listing")
    listing_route_result["request_file"] = relative_path(LISTING_ROUTE_REQUEST_FILE)
    listing_route_result["request_history_file"] = relative_path(listing_route_history_file)
    listing_route_result["result_file"] = relative_path(LISTING_ROUTE_RESULT_FILE)
    listing_route_result["result_history_file"] = relative_path(listing_route_result_history_file)

    snapshot["action_routing"] = summarize_action_routes([price_route_result, listing_route_result])
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    save_new_standard_outputs(snapshot, history_file, started_at, time.time() - started_at.timestamp(), input_sources)

    print(f"\n  Checked:            {len(results)}")
    print(f"  Lost Buy Box:       {len([r for r in results if r.get('buy_box_status') == 'LOST'])}")
    print(f"  No Buy Box:         {len([r for r in results if r.get('buy_box_status') == 'NO_BUYBOX'])}")
    print(f"  Price Routes:       {price_route_result.get('request_count', 0)}")
    print(f"  Listing Routes:     {listing_route_result.get('request_count', 0)}")
    print(f"  Routing Status:     {snapshot['action_routing'].get('status', 'skipped')}")
    print(f"  Saved latest:       {LATEST_FILE}")
    return 0 if not run_errors else 1


if __name__ == "__main__":
    sys.exit(main())
