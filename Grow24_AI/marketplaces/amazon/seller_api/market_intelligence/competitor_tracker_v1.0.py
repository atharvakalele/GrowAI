#!/usr/bin/env python3
"""
AutoGrow AI - Competitor Tracker v1.0
=====================================
Tracks competitor pressure for ASINs using SP-API competitive summary.

What it does:
  1. Selects ASINs from current ad catalog + optional watchlist
  2. Fetches Buy Box + lowest priced competitor data in batches
  3. Detects price gaps, Buy Box loss, competitor count, and offer pressure
  4. Saves latest snapshot + dated history JSON for trend comparison

Usage:
    python competitor_tracker_v1.0.py
    python competitor_tracker_v1.0.py --top 50
    python competitor_tracker_v1.0.py --asin B012345678 B09ABCDEFG
"""

import argparse
import json
import os
import ssl
import subprocess
import sys
import time
from datetime import datetime, timedelta
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def find_project_dir(start_dir):
    """Find repository root from both legacy and Grow24_AI module locations."""
    current = os.path.abspath(start_dir)
    while True:
        if (
            os.path.exists(os.path.join(current, "sp_api_credentials.json"))
            and os.path.exists(os.path.join(current, "config_competitor.json"))
        ):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            raise RuntimeError("Project root not found for competitor tracker")
        current = parent


PROJECT_DIR = find_project_dir(SCRIPT_DIR)
SP_CREDS_FILE = os.path.join(PROJECT_DIR, "sp_api_credentials.json")
CONFIG_FILE = os.path.join(PROJECT_DIR, "config_competitor.json")

REPORT_BASE = os.path.join(PROJECT_DIR, "ClaudeCode", "Report")
report_folders = [f for f in os.listdir(REPORT_BASE) if os.path.isdir(os.path.join(REPORT_BASE, f))]
report_folders.sort(key=lambda x: os.path.getmtime(os.path.join(REPORT_BASE, x)), reverse=True)
LATEST_REPORT = report_folders[0] if report_folders else datetime.now().strftime("%d %B %Y")
JSON_DIR = os.path.join(REPORT_BASE, LATEST_REPORT, "Json")

SP_ENDPOINT = "https://sellingpartnerapi-eu.amazon.com"
TOKEN_URL = "https://api.amazon.com/auth/o2/token"
ADS_PRODUCT_FILE = os.path.join(JSON_DIR, "sp_product_ads_list.json")
ADS_PERFORMANCE_FILE = os.path.join(JSON_DIR, "sp_advertisedproduct_daily.json")
LATEST_FILE = os.path.join(JSON_DIR, "competitor_tracker_latest.json")
FEATURE_ID = "M01"
FEATURE_KEY = "competitor_tracker"
FEATURE_NAME = "Competitor Tracker"
MODULE_GROUP = "market_intelligence"
IMPACT_LATEST_FILE = os.path.join(JSON_DIR, f"impact_{FEATURE_KEY}_latest.json")
ACTIVITY_LATEST_FILE = os.path.join(JSON_DIR, f"activity_{FEATURE_KEY}_latest.json")
REPORT_REGISTRY_FILE = os.path.join(JSON_DIR, "report_registry_latest.json")
PRICE_ROUTE_REQUEST_FILE = os.path.join(JSON_DIR, "competitor_price_route_latest.json")
PRICE_ROUTE_RESULT_FILE = os.path.join(JSON_DIR, "competitor_price_route_result_latest.json")
PRICE_OPTIMIZER_SCRIPT = os.path.join(
    PROJECT_DIR, "Grow24_AI", "marketplaces", "amazon", "seller_api", "pricing", "price_optimizer_v1.0.py"
)
PRICE_OPTIMIZER_STATUS_FILE = os.path.join(JSON_DIR, "price_optimizer_status.json")
LISTING_ROUTE_REQUEST_FILE = os.path.join(JSON_DIR, "competitor_listing_route_latest.json")
LISTING_ROUTE_RESULT_FILE = os.path.join(JSON_DIR, "competitor_listing_route_result_latest.json")
LISTING_RECOVERY_SCRIPT = os.path.join(
    PROJECT_DIR, "Grow24_AI", "marketplaces", "amazon", "seller_api", "listing_health", "listing_recovery_v1.0.py"
)
LISTING_RECOVERY_STATUS_FILE = os.path.join(JSON_DIR, "listing_recovery_status.json")

SSL_CONTEXT = None
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

SP = json.load(open(SP_CREDS_FILE, encoding="utf-8"))["sp_api_credentials"]

DEFAULT_CONFIG = {
    "version": "1.0",
    "enabled": True,
    "marketplace_id": "A21TJRUUN4KGV",
    "our_seller_id": "A2AC2AS9R9CBEA",
    "top_asins_limit": 30,
    "min_orders_7d": 1,
    "batch_size": 20,
    "delay_between_batches_sec": 32,
    "alert_thresholds": {
        "price_gap_loss_rs": 10,
        "price_gap_loss_pct": 3,
        "competitor_count_high": 3
    },
    "watchlist_asins": [],
    "action_routing": {
        "enabled": True,
        "self_action_enabled": True,
        "action_engine": "price_optimizer",
        "listing_engine": "listing_recovery",
        "dry_run": False,
        "max_price_routes_per_run": 10,
        "max_listing_routes_per_run": 10
    }
}

_cached_token = None
_token_expiry = None


def deep_merge_dict(base, override):
    merged = dict(base)
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge_dict(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, encoding="utf-8") as f:
            loaded = json.load(f)
        return deep_merge_dict(DEFAULT_CONFIG, loaded)
    return json.loads(json.dumps(DEFAULT_CONFIG))


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
    try:
        result = json.loads(urlopen(req, context=SSL_CONTEXT).read().decode())
    except URLError as e:
        raise RuntimeError(f"Token fetch failed: {e.reason}")
    _cached_token = result["access_token"]
    _token_expiry = datetime.now() + timedelta(seconds=result["expires_in"] - 60)
    return _cached_token


def load_json(path, default):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return default


def find_latest_json_file(filename):
    """Search newest report folders first and return first matching JSON path."""
    for folder in report_folders:
        candidate = os.path.join(REPORT_BASE, folder, "Json", filename)
        if os.path.exists(candidate):
            return candidate
    return os.path.join(JSON_DIR, filename)


def get_asin_pool(config, explicit_asins=None, top_override=None):
    explicit_asins = explicit_asins or []
    products_file = find_latest_json_file("sp_product_ads_list.json")
    performance_file = find_latest_json_file("sp_advertisedproduct_daily.json")
    products = load_json(products_file, [])
    performance = load_json(performance_file, [])

    asin_meta = {}
    for row in products:
        asin = row.get("asin", "").strip()
        if not asin:
            continue
        asin_meta.setdefault(asin, {
            "asin": asin,
            "sku": row.get("sku", ""),
            "campaign_name": row.get("campaignName", ""),
            "ad_group_name": row.get("adGroupName", ""),
            "state": row.get("state", "")
        })

    perf_map = {}
    for row in performance:
        asin = row.get("advertisedAsin", "").strip()
        if not asin:
            continue
        perf = perf_map.setdefault(asin, {"sales7d": 0.0, "orders7d": 0, "clicks7d": 0, "impressions7d": 0})
        perf["sales7d"] += float(row.get("sales7d", 0) or 0)
        perf["orders7d"] += int(row.get("purchases7d", 0) or 0)
        perf["clicks7d"] += int(row.get("clicks", 0) or 0)
        perf["impressions7d"] += int(row.get("impressions", 0) or 0)
        if asin in asin_meta and not asin_meta[asin].get("sku"):
            asin_meta[asin]["sku"] = row.get("advertisedSku", "")

    candidates = []
    min_orders = int(config.get("min_orders_7d", 1))
    for asin, meta in asin_meta.items():
        perf = perf_map.get(asin, {"sales7d": 0.0, "orders7d": 0, "clicks7d": 0, "impressions7d": 0})
        if perf["orders7d"] >= min_orders or not performance:
            item = dict(meta)
            item.update(perf)
            candidates.append(item)

    candidates.sort(
        key=lambda x: (
            1 if str(x.get("state", "")).upper() == "ENABLED" else 0,
            x["sales7d"],
            x["orders7d"]
        ),
        reverse=True
    )
    limit = top_override or int(config.get("top_asins_limit", 30))
    selected = candidates[:limit] if limit > 0 else candidates

    selected_map = {item["asin"]: item for item in selected}
    for asin in config.get("watchlist_asins", []):
        asin = str(asin).strip()
        if asin and asin not in selected_map:
            meta = asin_meta.get(asin, {"asin": asin, "sku": "", "campaign_name": "", "ad_group_name": ""})
            perf = perf_map.get(asin, {"sales7d": 0.0, "orders7d": 0, "clicks7d": 0, "impressions7d": 0})
            item = dict(meta)
            item.update(perf)
            selected_map[asin] = item

    for asin in explicit_asins:
        asin = str(asin).strip()
        if asin and asin not in selected_map:
            meta = asin_meta.get(asin, {"asin": asin, "sku": "", "campaign_name": "", "ad_group_name": ""})
            perf = perf_map.get(asin, {"sales7d": 0.0, "orders7d": 0, "clicks7d": 0, "impressions7d": 0})
            item = dict(meta)
            item.update(perf)
            selected_map[asin] = item

    return list(selected_map.values())


def fetch_competitive_batch(asin_list, marketplace_id):
    try:
        token = get_token()
    except RuntimeError as e:
        print(f"    {e}")
        return None, str(e)

    body = {"requests": []}
    for asin in asin_list:
        body["requests"].append({
            "asin": asin,
            "marketplaceId": marketplace_id,
            "includedData": ["featuredBuyingOptions", "lowestPricedOffers", "referencePrices"],
            "method": "GET",
            "uri": "/products/pricing/2022-05-01/items/competitiveSummary"
        })

    url = f"{SP_ENDPOINT}/batches/products/pricing/2022-05-01/items/competitiveSummary"
    headers = {
        "x-amz-access-token": token,
        "x-amz-date": datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"),
        "Content-Type": "application/json",
        "Host": "sellingpartnerapi-eu.amazon.com"
    }
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")

    try:
        resp = urlopen(req, context=SSL_CONTEXT)
        return json.loads(resp.read().decode()), None
    except HTTPError as e:
        error_body = e.read().decode()[:300]
        print(f"    API Error {e.code}: {error_body}")
        return None, f"HTTP {e.code}: {error_body}"
    except RuntimeError as e:
        print(f"    {e}")
        return None, str(e)
    except URLError as e:
        print(f"    Network error: {e.reason}")
        return None, f"Network error: {e.reason}"


def analyze_response(body, our_seller_id, thresholds):
    asin = body.get("asin", "")
    result = {
        "asin": asin,
        "buy_box_status": "UNKNOWN",
        "buy_box_owner": "",
        "buy_box_price": 0.0,
        "our_price": 0.0,
        "our_fulfillment": "",
        "lowest_competitor_price": 0.0,
        "lowest_competitor_seller": "",
        "lowest_competitor_fulfillment": "",
        "competitor_count": 0,
        "price_gap_rs": 0.0,
        "price_gap_pct": 0.0,
        "reference_prices": {},
        "action_priority": "LOW",
        "recommendation": "Monitor",
        "signals": []
    }

    fbo = body.get("featuredBuyingOptions", [])
    for opt in fbo:
        offers = opt.get("segmentedFeaturedOffers", [])
        for offer in offers:
            price = float(offer.get("listingPrice", {}).get("amount", 0) or 0)
            seller = offer.get("sellerId", "")
            fulfillment = offer.get("fulfillmentType", "")
            result["buy_box_owner"] = seller
            result["buy_box_price"] = price
            if seller == our_seller_id:
                result["buy_box_status"] = "WON"
                result["our_price"] = price
                result["our_fulfillment"] = fulfillment
            else:
                result["buy_box_status"] = "LOST"
            break
        if result["buy_box_owner"]:
            break

    offers = []
    for offer_group in body.get("lowestPricedOffers", []):
        for offer in offer_group.get("offers", []):
            seller = offer.get("sellerId", "")
            price = float(offer.get("listingPrice", {}).get("amount", 0) or 0)
            fulfillment = offer.get("fulfillmentType", "")
            offers.append({"seller": seller, "price": price, "fulfillment": fulfillment})
            if seller == our_seller_id and price > 0 and result["our_price"] == 0:
                result["our_price"] = price
                result["our_fulfillment"] = fulfillment

    competitors = [o for o in offers if o["seller"] != our_seller_id]
    result["competitor_count"] = len({o["seller"] for o in competitors if o["seller"]})

    if competitors:
        lowest = min(competitors, key=lambda x: x["price"])
        result["lowest_competitor_price"] = lowest["price"]
        result["lowest_competitor_seller"] = lowest["seller"]
        result["lowest_competitor_fulfillment"] = lowest["fulfillment"]

    for rp in body.get("referencePrices", []):
        name = rp.get("name", "")
        amount = float(rp.get("price", {}).get("amount", 0) or 0)
        if name:
            result["reference_prices"][name] = amount

    if not fbo:
        result["buy_box_status"] = "NO_BUYBOX"
        result["action_priority"] = "HIGH"
        result["recommendation"] = "Check listing suppression, pricing, and availability"
        result["signals"].append("No Buy Box available")
        return result

    if result["our_price"] > 0 and result["lowest_competitor_price"] > 0:
        gap_rs = round(result["our_price"] - result["lowest_competitor_price"], 2)
        gap_pct = round((gap_rs / result["lowest_competitor_price"] * 100), 2) if result["lowest_competitor_price"] else 0
        result["price_gap_rs"] = gap_rs
        result["price_gap_pct"] = gap_pct

    if result["buy_box_status"] == "LOST":
        result["action_priority"] = "HIGH"
        if result["price_gap_rs"] >= thresholds["price_gap_loss_rs"] or result["price_gap_pct"] >= thresholds["price_gap_loss_pct"]:
            result["recommendation"] = "Review price or coupon strategy immediately"
            result["signals"].append("Competitor price undercut")
        elif result["lowest_competitor_fulfillment"] == "AFN" and result["our_fulfillment"] != "AFN":
            result["recommendation"] = "Check FBA / Prime competitiveness"
            result["signals"].append("Competitor fulfillment advantage")
        else:
            result["recommendation"] = "Review listing quality, seller metrics, and content"
            result["signals"].append("Lost Buy Box without major price gap")
    elif result["buy_box_status"] == "WON":
        if result["competitor_count"] >= thresholds["competitor_count_high"]:
            result["action_priority"] = "MEDIUM"
            result["recommendation"] = "Defend position; monitor price and reviews closely"
            result["signals"].append("High competitor density")
        elif result["competitor_count"] == 0:
            result["recommendation"] = "Low pressure; maintain price discipline"
            result["signals"].append("No direct offer competition")
        else:
            result["recommendation"] = "Monitor"
            result["signals"].append("Buy Box won")

    return result


def load_previous_snapshot():
    if os.path.exists(LATEST_FILE):
        with open(LATEST_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def enrich_with_change_detection(results, previous_snapshot):
    previous_map = {}
    for item in previous_snapshot.get("results", []):
        previous_map[item.get("asin")] = item

    for item in results:
        prev = previous_map.get(item["asin"])
        if not prev:
            item["change"] = "NEW"
            continue

        changes = []
        if prev.get("buy_box_status") != item.get("buy_box_status"):
            changes.append(f"Buy Box: {prev.get('buy_box_status')} -> {item.get('buy_box_status')}")
        prev_gap = float(prev.get("price_gap_rs", 0) or 0)
        curr_gap = float(item.get("price_gap_rs", 0) or 0)
        if abs(curr_gap - prev_gap) >= 5:
            changes.append(f"Gap Rs.{prev_gap:.0f} -> Rs.{curr_gap:.0f}")
        prev_comp = int(prev.get("competitor_count", 0) or 0)
        curr_comp = int(item.get("competitor_count", 0) or 0)
        if prev_comp != curr_comp:
            changes.append(f"Competitors {prev_comp} -> {curr_comp}")
        item["change"] = "; ".join(changes) if changes else "NO_MAJOR_CHANGE"


def save_outputs(snapshot):
    os.makedirs(JSON_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    history_file = os.path.join(JSON_DIR, f"competitor_tracker_{ts}.json")
    with open(LATEST_FILE, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    return history_file


def relative_path(path):
    return os.path.relpath(path, PROJECT_DIR).replace("\\", "/")


def save_json_pair(latest_file, prefix, payload, started_at):
    os.makedirs(JSON_DIR, exist_ok=True)
    ts = started_at.strftime("%Y%m%d_%H%M%S")
    history_file = os.path.join(JSON_DIR, f"{prefix}_{ts}.json")
    with open(latest_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return history_file


def build_price_route_requests(results, config, started_at):
    routing_cfg = config.get("action_routing", {})
    thresholds = config.get("alert_thresholds", {})
    max_routes = int(routing_cfg.get("max_price_routes_per_run", 10) or 10)
    route_run_id = f"{FEATURE_KEY}_price_route_{started_at.strftime('%Y%m%d_%H%M%S')}"
    candidates = []
    for item in results:
        if item.get("buy_box_status") != "LOST":
            continue
        if not item.get("sku"):
            continue
        our_price = float(item.get("our_price", 0) or 0)
        competitor_price = float(item.get("lowest_competitor_price", 0) or 0)
        gap_rs = float(item.get("price_gap_rs", 0) or 0)
        gap_pct = float(item.get("price_gap_pct", 0) or 0)
        if our_price <= 0 or competitor_price <= 0 or competitor_price >= our_price:
            continue
        if gap_rs < float(thresholds.get("price_gap_loss_rs", 10) or 10) and gap_pct < float(thresholds.get("price_gap_loss_pct", 3) or 3):
            continue
        candidates.append({
            "route_run_id": route_run_id,
            "source_feature_key": FEATURE_KEY,
            "source_feature_name": FEATURE_NAME,
            "action_family": "pricing",
            "target_engine": routing_cfg.get("action_engine", "price_optimizer"),
            "issue_type": "buy_box_lost_price_gap",
            "asin": item.get("asin", ""),
            "sku": item.get("sku", ""),
            "current_price": round(our_price, 2),
            "lowest_competitor_price": round(competitor_price, 2),
            "target_price": round(competitor_price, 2),
            "price_gap_rs": round(gap_rs, 2),
            "price_gap_pct": round(gap_pct, 2),
            "sales7d_rs": round(float(item.get("sales7d", 0) or 0), 2),
            "buy_box_status": item.get("buy_box_status", ""),
            "recommendation": item.get("recommendation", ""),
            "signals": item.get("signals", []),
            "route_reason": f"Lost Buy Box with competitor undercut of Rs.{gap_rs:.2f} ({gap_pct:.2f}%).",
            "auto_action_allowed": bool(routing_cfg.get("enabled", True) and routing_cfg.get("self_action_enabled", True))
        })
    candidates.sort(key=lambda x: (x.get("sales7d_rs", 0), x.get("price_gap_rs", 0)), reverse=True)
    payload = {
        "schema_type": "action_route_request",
        "schema_version": "1.0",
        "route_run_id": route_run_id,
        "generated_at": datetime.now().isoformat(),
        "source_feature_key": FEATURE_KEY,
        "source_feature_name": FEATURE_NAME,
        "action_engine": routing_cfg.get("action_engine", "price_optimizer"),
        "self_action_enabled": bool(routing_cfg.get("self_action_enabled", True)),
        "requests": candidates[:max_routes]
    }
    history_file = save_json_pair(PRICE_ROUTE_REQUEST_FILE, "competitor_price_route", payload, started_at)
    return payload, history_file


def execute_price_routes(route_payload, route_history_file, config, started_at):
    requests = route_payload.get("requests", [])
    routing_cfg = config.get("action_routing", {})
    result = {
        "route_run_id": route_payload.get("route_run_id", ""),
        "generated_at": datetime.now().isoformat(),
        "engine": routing_cfg.get("action_engine", "price_optimizer"),
        "self_action_enabled": bool(routing_cfg.get("self_action_enabled", True)),
        "request_count": len(requests),
        "status": "skipped",
        "reason": "",
        "summary": {},
        "actions": [],
        "request_file": relative_path(PRICE_ROUTE_REQUEST_FILE),
        "request_history_file": relative_path(route_history_file)
    }
    if not requests:
        result["reason"] = "No competitor findings qualified for price routing."
        return result, save_json_pair(PRICE_ROUTE_RESULT_FILE, "competitor_price_route_result", result, started_at)
    if not routing_cfg.get("enabled", True):
        result["status"] = "disabled"
        result["reason"] = "Action routing disabled in competitor config."
        return result, save_json_pair(PRICE_ROUTE_RESULT_FILE, "competitor_price_route_result", result, started_at)
    if not routing_cfg.get("self_action_enabled", True):
        result["status"] = "pending"
        result["reason"] = "Self action disabled; route requests created for later execution."
        return result, save_json_pair(PRICE_ROUTE_RESULT_FILE, "competitor_price_route_result", result, started_at)
    if routing_cfg.get("action_engine") != "price_optimizer":
        result["status"] = "blocked"
        result["reason"] = f"Unsupported action engine: {routing_cfg.get('action_engine')}"
        return result, save_json_pair(PRICE_ROUTE_RESULT_FILE, "competitor_price_route_result", result, started_at)
    if not os.path.exists(PRICE_OPTIMIZER_SCRIPT):
        result["status"] = "failed"
        result["reason"] = "Price optimizer script not found."
        return result, save_json_pair(PRICE_ROUTE_RESULT_FILE, "competitor_price_route_result", result, started_at)

    cmd = [sys.executable, PRICE_OPTIMIZER_SCRIPT, "--route-file", route_history_file]
    if routing_cfg.get("dry_run", False):
        cmd.append("--dry-run")
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_DIR)
    status_data = load_json(PRICE_OPTIMIZER_STATUS_FILE, {})
    result["status"] = "executed" if proc.returncode == 0 else "failed"
    result["reason"] = "Price optimizer route executed." if proc.returncode == 0 else "Price optimizer route execution failed."
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
    return result, save_json_pair(PRICE_ROUTE_RESULT_FILE, "competitor_price_route_result", result, started_at)


def build_listing_route_requests(results, config, started_at):
    routing_cfg = config.get("action_routing", {})
    max_routes = int(routing_cfg.get("max_listing_routes_per_run", 10) or 10)
    route_run_id = f"{FEATURE_KEY}_listing_route_{started_at.strftime('%Y%m%d_%H%M%S')}"
    candidates = []
    for item in results:
        if item.get("buy_box_status") != "NO_BUYBOX":
            continue
        if not item.get("sku"):
            continue
        candidates.append({
            "route_run_id": route_run_id,
            "source_feature_key": FEATURE_KEY,
            "source_feature_name": FEATURE_NAME,
            "action_family": "listing_recovery",
            "target_engine": routing_cfg.get("listing_engine", "listing_recovery"),
            "issue_type": "no_buy_box_listing_check",
            "asin": item.get("asin", ""),
            "sku": item.get("sku", ""),
            "current_price": round(float(item.get("our_price", 0) or 0), 2),
            "sales7d_rs": round(float(item.get("sales7d", 0) or 0), 2),
            "buy_box_status": item.get("buy_box_status", ""),
            "recommendation": item.get("recommendation", ""),
            "signals": item.get("signals", []),
            "route_reason": "No Buy Box found; verify listing state and start recovery if inactive or not searchable.",
            "auto_action_allowed": bool(routing_cfg.get("enabled", True) and routing_cfg.get("self_action_enabled", True))
        })
    candidates.sort(key=lambda x: x.get("sales7d_rs", 0), reverse=True)
    payload = {
        "schema_type": "action_route_request",
        "schema_version": "1.0",
        "route_run_id": route_run_id,
        "generated_at": datetime.now().isoformat(),
        "source_feature_key": FEATURE_KEY,
        "source_feature_name": FEATURE_NAME,
        "action_engine": routing_cfg.get("listing_engine", "listing_recovery"),
        "self_action_enabled": bool(routing_cfg.get("self_action_enabled", True)),
        "requests": candidates[:max_routes]
    }
    history_file = save_json_pair(LISTING_ROUTE_REQUEST_FILE, "competitor_listing_route", payload, started_at)
    return payload, history_file


def execute_listing_routes(route_payload, route_history_file, config, started_at):
    requests = route_payload.get("requests", [])
    routing_cfg = config.get("action_routing", {})
    result = {
        "route_type": "listing_recovery",
        "route_run_id": route_payload.get("route_run_id", ""),
        "generated_at": datetime.now().isoformat(),
        "engine": routing_cfg.get("listing_engine", "listing_recovery"),
        "self_action_enabled": bool(routing_cfg.get("self_action_enabled", True)),
        "request_count": len(requests),
        "status": "skipped",
        "reason": "",
        "summary": {},
        "actions": [],
        "request_file": relative_path(LISTING_ROUTE_REQUEST_FILE),
        "request_history_file": relative_path(route_history_file)
    }
    if not requests:
        result["reason"] = "No competitor findings qualified for listing recovery routing."
        return result, save_json_pair(LISTING_ROUTE_RESULT_FILE, "competitor_listing_route_result", result, started_at)
    if not routing_cfg.get("enabled", True):
        result["status"] = "disabled"
        result["reason"] = "Action routing disabled in competitor config."
        return result, save_json_pair(LISTING_ROUTE_RESULT_FILE, "competitor_listing_route_result", result, started_at)
    if not routing_cfg.get("self_action_enabled", True):
        result["status"] = "pending"
        result["reason"] = "Self action disabled; listing route requests created for later execution."
        return result, save_json_pair(LISTING_ROUTE_RESULT_FILE, "competitor_listing_route_result", result, started_at)
    if routing_cfg.get("listing_engine", "listing_recovery") != "listing_recovery":
        result["status"] = "blocked"
        result["reason"] = f"Unsupported listing engine: {routing_cfg.get('listing_engine')}"
        return result, save_json_pair(LISTING_ROUTE_RESULT_FILE, "competitor_listing_route_result", result, started_at)
    if not os.path.exists(LISTING_RECOVERY_SCRIPT):
        result["status"] = "failed"
        result["reason"] = "Listing recovery script not found."
        return result, save_json_pair(LISTING_ROUTE_RESULT_FILE, "competitor_listing_route_result", result, started_at)

    cmd = [sys.executable, LISTING_RECOVERY_SCRIPT, "--route-file", route_history_file]
    if routing_cfg.get("dry_run", False):
        cmd.append("--dry-run")
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_DIR)
    status_data = load_json(LISTING_RECOVERY_STATUS_FILE, {})
    price_route = status_data.get("price_route", {})
    result["status"] = "executed" if proc.returncode == 0 else "failed"
    result["reason"] = "Listing recovery route executed." if proc.returncode == 0 else "Listing recovery route execution failed."
    result["command"] = " ".join(cmd)
    result["return_code"] = proc.returncode
    result["stdout_tail"] = (proc.stdout or "")[-1200:]
    result["stderr_tail"] = (proc.stderr or "")[-1200:]
    result["summary"] = {
        "checked_items": len(status_data.get("checked_items", [])),
        "blocked_items": len(status_data.get("blocked_items", [])),
        "price_route_count": int(price_route.get("request_count", 0) or 0)
    }
    result["actions"] = list(price_route.get("actions", []))
    result["checked_items"] = status_data.get("checked_items", [])
    result["blocked_items"] = status_data.get("blocked_items", [])
    result["listing_recovery_status_file"] = relative_path(LISTING_RECOVERY_STATUS_FILE)
    return result, save_json_pair(LISTING_ROUTE_RESULT_FILE, "competitor_listing_route_result", result, started_at)


def summarize_action_routes(route_results):
    routes = [route for route in route_results if route]
    status_priority = {
        "failed": 6,
        "blocked": 5,
        "pending": 4,
        "disabled": 3,
        "executed": 2,
        "skipped": 1
    }
    aggregate_status = "skipped"
    for route in routes:
        if status_priority.get(route.get("status", "skipped"), 0) > status_priority.get(aggregate_status, 0):
            aggregate_status = route.get("status", "skipped")
    reasons = [route.get("reason", "") for route in routes if route.get("reason")]
    files = []
    for route in routes:
        for key in ("request_file", "request_history_file", "result_file", "result_history_file"):
            if route.get(key):
                files.append(route.get(key))
    return {
        "status": aggregate_status,
        "reason": " | ".join(reasons),
        "request_count": sum(int(route.get("request_count", 0) or 0) for route in routes),
        "actions": [action for route in routes for action in route.get("actions", [])],
        "files": files,
        "routes": routes
    }


def get_status_and_impact(summary, failed_asins, run_errors):
    lost = int(summary.get("lost_buy_box", 0) or 0)
    no_buybox = int(summary.get("no_buy_box", 0) or 0)
    high_pressure = int(summary.get("high_pressure", 0) or 0)

    if run_errors and not summary.get("tracked_asins", 0):
        return "failed", "critical"
    if run_errors or failed_asins:
        return "partial", "high"
    if lost or no_buybox:
        return "warning", "high"
    if high_pressure:
        return "warning", "medium"
    return "success", "low"


def build_impact_summary(snapshot, history_file):
    generated_at = snapshot.get("timestamp") or datetime.now().isoformat()
    summary = snapshot.get("summary", {})
    results = snapshot.get("results", [])
    failed_asins = snapshot.get("failed_asins", [])
    run_errors = snapshot.get("run_errors", [])
    action_routing = snapshot.get("action_routing", {})
    status, impact_level = get_status_and_impact(summary, failed_asins, run_errors)
    actions_taken = action_routing.get("actions", [])
    action_asins = {item.get("asin", "") for item in actions_taken if item.get("asin")}

    risk_items = [
        item for item in results
        if item.get("buy_box_status") in ("LOST", "NO_BUYBOX") or item.get("action_priority") == "HIGH"
    ]
    winners = [
        item for item in results
        if item.get("buy_box_status") == "WON" and int(item.get("competitor_count", 0) or 0) == 0
    ]
    revenue_at_risk = round(sum(float(item.get("sales7d", 0) or 0) for item in risk_items), 2)
    protected_visibility = round(sum(float(item.get("sales7d", 0) or 0) for item in winners), 2)
    action_sales_protected = round(sum(float(item.get("sales7d", 0) or 0) for item in results if item.get("asin") in action_asins), 2)
    action_history = []
    for action in actions_taken[:10]:
        action_history.append({
            "asin": action.get("asin", ""),
            "sku": action.get("sku", ""),
            "action": action.get("action", ""),
            "status": action.get("status", ""),
            "old_price": round(float(action.get("old_price", 0) or 0), 2),
            "new_price": round(float(action.get("new_price", 0) or 0), 2),
            "reason": action.get("reason", "")
        })

    if actions_taken:
        action_headline = f"AI executed {len(actions_taken)} corrective action(s) and moved Rs.{action_sales_protected:.2f} 7-day sales into protection workflow."
    elif action_routing.get("request_count", 0):
        action_headline = f"AI identified {action_routing.get('request_count', 0)} action candidate(s), but execution status is {action_routing.get('status', 'pending')}."
    else:
        action_headline = "AI did not execute a corrective action in this competitor cycle."

    if status == "failed":
        headline = "Competitor tracker could not complete live competitor analysis."
    elif risk_items:
        headline = f"Competitor risk found on {len(risk_items)} ASIN(s); review Buy Box and listing pressure."
    else:
        headline = f"Competitor scan completed: {len(winners)} ASIN(s) currently show low direct offer pressure."

    def compact_item(item):
        return {
            "asin": item.get("asin", ""),
            "sku": item.get("sku", ""),
            "sales7d_rs": round(float(item.get("sales7d", 0) or 0), 2),
            "buy_box_status": item.get("buy_box_status", ""),
            "competitor_count": int(item.get("competitor_count", 0) or 0),
            "price_gap_rs": round(float(item.get("price_gap_rs", 0) or 0), 2),
            "recommendation": item.get("recommendation", "")
        }

    return {
        "schema_type": "impact_summary",
        "schema_version": "1.0",
        "feature_id": FEATURE_ID,
        "feature_key": FEATURE_KEY,
        "feature_name": FEATURE_NAME,
        "module_group": MODULE_GROUP,
        "generated_at": generated_at,
        "period": "manual",
        "status": status,
        "impact_level": impact_level,
        "business_areas": ["buy_box", "pricing", "competitor_pressure", "revenue_protection"],
        "headline": headline,
        "summary_metrics": {
            "profit_impact_rs": 0,
            "loss_prevented_rs": 0,
            "waste_blocked_rs": 0,
            "revenue_protected_rs": protected_visibility,
            "ai_action_sales_protected_rs": action_sales_protected,
            "ai_actions_executed_count": len(actions_taken),
            "ai_actions_identified_count": int(action_routing.get("request_count", 0) or 0),
            "rank_up_count": 0,
            "rank_down_count": 0,
            "buy_box_won_count": len([r for r in results if r.get("buy_box_status") == "WON"]),
            "buy_box_lost_count": int(summary.get("lost_buy_box", 0) or 0),
            "conversion_up_count": 0,
            "conversion_down_count": 0,
            "organic_gain_count": 0,
            "organic_decline_count": 0,
            "tracked_asins_count": int(snapshot.get("tracked_asins", 0) or 0),
            "no_buy_box_count": int(summary.get("no_buy_box", 0) or 0),
            "high_pressure_count": int(summary.get("high_pressure", 0) or 0),
            "revenue_at_risk_7d_rs": revenue_at_risk,
            "low_pressure_opportunities_count": int(summary.get("low_pressure_opportunities", 0) or 0)
        },
        "positive_impacts": [
            {
                "type": "low_competitor_pressure",
                "message": f"{len(winners)} ASIN(s) currently have Buy Box and no direct offer competition.",
                "estimated_sales7d_rs": protected_visibility
            }
        ] if winners else [],
        "negative_impacts": [
            {
                "type": "competitor_or_buy_box_risk",
                "message": f"{len(risk_items)} ASIN(s) need review due to Buy Box or competitor pressure.",
                "estimated_sales7d_at_risk_rs": revenue_at_risk
            }
        ] if risk_items else [],
        "top_winners": [compact_item(item) for item in sorted(winners, key=lambda x: float(x.get("sales7d", 0) or 0), reverse=True)[:10]],
        "top_risks": [compact_item(item) for item in sorted(risk_items, key=lambda x: float(x.get("sales7d", 0) or 0), reverse=True)[:10]],
        "ai_learning": {
            "new_rule_learned": False,
            "rule_promoted_count": 0,
            "confidence": 0.78 if results else 0.25,
            "notes": "New-standard wrapper created from competitor tracker raw output."
        },
        "recommendations": [
            "Review no Buy Box ASINs for listing suppression, pricing, and availability.",
            "Use high-pressure ASINs as candidates for pricing, coupon, or fulfillment review.",
            f"Action routing status: {action_routing.get('status', 'not_routed')}."
        ] if risk_items else [
            "Maintain price discipline on low-pressure ASINs and continue daily monitoring."
        ],
        "ai_action_summary": {
            "headline": action_headline,
            "status": action_routing.get("status", "not_routed"),
            "actions_identified": int(action_routing.get("request_count", 0) or 0),
            "actions_executed": len(actions_taken),
            "expected_sales_protected_rs": action_sales_protected,
            "items": action_history
        },
        "detail_ref": {
            "raw_file": relative_path(LATEST_FILE),
            "detail_file": relative_path(history_file),
            "supporting_report": relative_path(LATEST_FILE)
        }
    }


def build_activity_summary(snapshot, history_file, impact_file, started_at, duration_sec, input_sources):
    generated_at = snapshot.get("timestamp") or datetime.now().isoformat()
    summary = snapshot.get("summary", {})
    failed_asins = snapshot.get("failed_asins", [])
    run_errors = snapshot.get("run_errors", [])
    action_routing = snapshot.get("action_routing", {})
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
    status, _impact_level = get_status_and_impact(summary, failed_asins, run_errors)
    warnings = []
    if summary.get("lost_buy_box", 0):
        warnings.append(f"{summary.get('lost_buy_box')} ASIN(s) lost Buy Box.")
    if summary.get("no_buy_box", 0):
        warnings.append(f"{summary.get('no_buy_box')} ASIN(s) have no Buy Box.")
    if summary.get("high_pressure", 0):
        warnings.append(f"{summary.get('high_pressure')} ASIN(s) have high competitor pressure.")

    route_needs_review = action_routing.get("status") in ("pending", "blocked", "failed")
    return {
        "schema_type": "activity_summary",
        "schema_version": "1.0",
        "feature_id": FEATURE_ID,
        "feature_key": FEATURE_KEY,
        "feature_name": FEATURE_NAME,
        "module_group": MODULE_GROUP,
        "run_id": f"{FEATURE_KEY}_{started_at.strftime('%Y%m%d_%H%M%S')}",
        "generated_at": generated_at,
        "status": status,
        "run_mode": "manual",
        "duration_sec": round(duration_sec, 2),
        "freshness_hours": 24,
        "needs_review": bool(warnings or failed_asins or run_errors),
        "input_sources": input_sources,
        "output_files": [
            relative_path(LATEST_FILE),
            relative_path(history_file),
            relative_path(impact_file),
            relative_path(ACTIVITY_LATEST_FILE),
            relative_path(REPORT_REGISTRY_FILE),
        ] + [path for path in action_routing.get("files", []) if path],
        "counts": {
            "items_scanned": int(snapshot.get("tracked_asins", 0) or 0) + len(failed_asins),
            "items_processed": int(snapshot.get("tracked_asins", 0) or 0),
            "alerts_generated": len(warnings),
            "approvals_needed": len(warnings) + (action_routing.get("request_count", 0) if action_routing.get("status") in ("pending", "blocked") else 0),
            "warnings": len(warnings),
            "errors": len(run_errors),
            "action_routes_created": int(action_routing.get("request_count", 0) or 0),
            "action_routes_executed": len(action_routing.get("actions", []))
        },
        "run_events": [
            "Selected ASIN pool from ads/product report data.",
            "Fetched competitive summary batches from Amazon SP-API.",
            "Saved legacy raw competitor tracker output.",
            "Published new-standard impact summary, activity summary, and registry entry.",
            f"Action routing status: {action_routing.get('status', 'not_routed')}."
        ],
        "warnings_list": warnings,
        "errors_list": run_errors,
        "review_items": {
            "user_review": warnings + ([action_routing.get("reason", "")] if route_needs_review and action_routing.get("reason") else []),
            "developer_review": [],
            "blocked_items": failed_asins
        },
        "action_history": action_history,
        "source_report_folder": LATEST_REPORT,
        "notes": "Compatibility migration: legacy raw output remains unchanged; dashboard-facing summaries follow future JSON contract."
    }


def build_registry_entry(impact_summary, activity_summary, history_file):
    status = impact_summary.get("status", "success")
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
            "raw_output": relative_path(LATEST_FILE),
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
            "status": status,
            "impact_level": impact_level,
            "priority_score": priority_score,
            "strategic_weight": 7,
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
            "dashboard_note": "Shows competitor pressure, Buy Box status, and revenue-at-risk signals.",
            "developer_note": "AI-only compatible wrapper added beside legacy competitor tracker output.",
            "migration_note": "Legacy raw competitor_tracker_latest.json remains unchanged."
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
    registry["schema_type"] = "report_registry"
    registry["schema_version"] = "1.0"
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

    activity_summary = build_activity_summary(
        snapshot,
        history_file,
        impact_history_file,
        started_at,
        duration_sec,
        input_sources
    )
    with open(ACTIVITY_LATEST_FILE, "w", encoding="utf-8") as f:
        json.dump(activity_summary, f, indent=2, ensure_ascii=False)
    with open(activity_history_file, "w", encoding="utf-8") as f:
        json.dump(activity_summary, f, indent=2, ensure_ascii=False)

    registry_entry = build_registry_entry(impact_summary, activity_summary, history_file)
    update_report_registry(registry_entry)

    return impact_history_file, activity_history_file


def main():
    started_at = datetime.now()
    parser = argparse.ArgumentParser(description="Competitor Tracker")
    parser.add_argument("--top", type=int, help="Track top N ASINs from current ad data")
    parser.add_argument("--asin", nargs="*", help="Specific ASINs to include")
    args = parser.parse_args()

    config = load_config()
    thresholds = config.get("alert_thresholds", {})

    print("=" * 70)
    print("  AutoGrow AI - Competitor Tracker v1.0")
    print(f"  {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print("=" * 70)

    if not config.get("enabled", True):
        print("\n  Competitor tracker is disabled in config_competitor.json")
        return 0

    asin_pool = get_asin_pool(config, explicit_asins=args.asin, top_override=args.top)
    products_file = find_latest_json_file("sp_product_ads_list.json")
    performance_file = find_latest_json_file("sp_advertisedproduct_daily.json")
    input_sources = [
        relative_path(CONFIG_FILE),
        relative_path(products_file),
        relative_path(performance_file)
    ]
    if not asin_pool:
        snapshot = {
            "version": "1.0",
            "timestamp": datetime.now().isoformat(),
            "marketplace_id": config.get("marketplace_id", DEFAULT_CONFIG["marketplace_id"]),
            "tracked_asins": 0,
            "failed_asins": [],
            "summary": {
                "lost_buy_box": 0,
                "no_buy_box": 0,
                "high_pressure": 0,
                "low_pressure_opportunities": 0
            },
            "results": [],
            "note": "No ASINs found from current report data. Run import or add watchlist ASINs."
        }
        history_file = save_outputs(snapshot)
        save_new_standard_outputs(snapshot, history_file, started_at, time.time() - started_at.timestamp(), input_sources)
        print("\n  No ASINs found. Saved empty competitor report for visibility.")
        print(f"  Saved latest:  {LATEST_FILE}")
        print(f"  Saved history: {history_file}")
        print(f"  Saved impact:  {IMPACT_LATEST_FILE}")
        print(f"  Saved activity:{ACTIVITY_LATEST_FILE}")
        return 1

    marketplace_id = config.get("marketplace_id", DEFAULT_CONFIG["marketplace_id"])
    our_seller_id = config.get("our_seller_id", DEFAULT_CONFIG["our_seller_id"])
    batch_size = int(config.get("batch_size", 20))
    delay = int(config.get("delay_between_batches_sec", 32))

    print(f"\n  Tracking {len(asin_pool)} ASINs")
    batches = [asin_pool[i:i + batch_size] for i in range(0, len(asin_pool), batch_size)]
    print(f"  {len(batches)} batches, ~{(len(batches) * delay) // 60}m {(len(batches) * delay) % 60}s estimated")

    previous_snapshot = load_previous_snapshot()
    results = []
    failed_asins = []
    run_errors = []

    for idx, batch in enumerate(batches, start=1):
        asin_list = [item["asin"] for item in batch]
        print(f"  Batch {idx}/{len(batches)}...", end=" ", flush=True)
        response, error_text = fetch_competitive_batch(asin_list, marketplace_id)
        if not response:
            print("FAILED")
            failed_asins.extend(asin_list)
            if error_text:
                run_errors.append({
                    "batch": idx,
                    "asins": asin_list,
                    "error": error_text
                })
        else:
            bodies = {}
            for item in response.get("responses", []):
                body = item.get("body", {})
                asin = body.get("asin", "")
                if asin:
                    bodies[asin] = body
            for meta in batch:
                asin = meta["asin"]
                if asin not in bodies:
                    failed_asins.append(asin)
                    continue
                analyzed = analyze_response(bodies[asin], our_seller_id, thresholds)
                analyzed.update({
                    "sku": meta.get("sku", ""),
                    "sales7d": round(float(meta.get("sales7d", 0) or 0), 2),
                    "orders7d": int(meta.get("orders7d", 0) or 0),
                    "clicks7d": int(meta.get("clicks7d", 0) or 0),
                    "impressions7d": int(meta.get("impressions7d", 0) or 0),
                    "campaign_name": meta.get("campaign_name", "")[:120],
                    "ad_group_name": meta.get("ad_group_name", "")[:120]
                })
                results.append(analyzed)
            print(f"{len(bodies)} items")
        if idx < len(batches):
            time.sleep(delay)

    enrich_with_change_detection(results, previous_snapshot)

    lost = [r for r in results if r["buy_box_status"] == "LOST"]
    no_buybox = [r for r in results if r["buy_box_status"] == "NO_BUYBOX"]
    high_pressure = [r for r in results if r["competitor_count"] >= thresholds.get("competitor_count_high", 3)]
    opportunities = [r for r in results if r["buy_box_status"] == "WON" and r["competitor_count"] == 0]

    results.sort(key=lambda x: (
        0 if x["action_priority"] == "HIGH" else 1 if x["action_priority"] == "MEDIUM" else 2,
        -float(x.get("sales7d", 0) or 0)
    ))

    snapshot = {
        "version": "1.0",
        "timestamp": datetime.now().isoformat(),
        "marketplace_id": marketplace_id,
        "tracked_asins": len(results),
        "failed_asins": failed_asins,
        "run_errors": run_errors,
        "summary": {
            "lost_buy_box": len(lost),
            "no_buy_box": len(no_buybox),
            "high_pressure": len(high_pressure),
            "low_pressure_opportunities": len(opportunities)
        },
        "results": results
    }

    price_route_payload, price_route_history_file = build_price_route_requests(results, config, started_at)
    price_route_result, price_route_result_history_file = execute_price_routes(
        price_route_payload, price_route_history_file, config, started_at
    )
    price_route_result["route_type"] = "pricing"
    price_route_result["request_file"] = relative_path(PRICE_ROUTE_REQUEST_FILE)
    price_route_result["request_history_file"] = relative_path(price_route_history_file)
    price_route_result["result_file"] = relative_path(PRICE_ROUTE_RESULT_FILE)
    price_route_result["result_history_file"] = relative_path(price_route_result_history_file)

    listing_route_payload, listing_route_history_file = build_listing_route_requests(results, config, started_at)
    listing_route_result, listing_route_result_history_file = execute_listing_routes(
        listing_route_payload, listing_route_history_file, config, started_at
    )
    listing_route_result["request_file"] = relative_path(LISTING_ROUTE_REQUEST_FILE)
    listing_route_result["request_history_file"] = relative_path(listing_route_history_file)
    listing_route_result["result_file"] = relative_path(LISTING_ROUTE_RESULT_FILE)
    listing_route_result["result_history_file"] = relative_path(listing_route_result_history_file)

    snapshot["action_routing"] = summarize_action_routes([price_route_result, listing_route_result])

    history_file = save_outputs(snapshot)
    impact_history_file, activity_history_file = save_new_standard_outputs(
        snapshot,
        history_file,
        started_at,
        time.time() - started_at.timestamp(),
        input_sources
    )

    print(f"\n{'=' * 70}")
    print("  SUMMARY")
    print(f"{'=' * 70}")
    print(f"  Tracked ASINs:        {len(results)}")
    print(f"  Lost Buy Box:         {len(lost)}")
    print(f"  No Buy Box:           {len(no_buybox)}")
    print(f"  High Pressure ASINs:  {len(high_pressure)}")
    print(f"  Low Pressure Wins:    {len(opportunities)}")
    print(f"  Failed ASINs:         {len(failed_asins)}")
    print(f"  Price Routes:         {price_route_result.get('request_count', 0)}")
    print(f"  Listing Routes:       {listing_route_result.get('request_count', 0)}")
    print(f"  Routing Status:       {snapshot['action_routing'].get('status', 'not_routed')}")
    if run_errors:
        print(f"  Run Errors:           {len(run_errors)}")

    if lost:
        print(f"\n  TOP COMPETITOR THREATS")
        for item in sorted(lost, key=lambda x: float(x.get("sales7d", 0) or 0), reverse=True)[:10]:
            print(
                f"    {item['asin']} | {item['sku'][:24]:<24} | "
                f"Sales7d Rs.{item['sales7d']:>7.0f} | "
                f"Gap Rs.{item['price_gap_rs']:>6.0f} | {item['recommendation']}"
            )

    print(f"\n  Saved latest:  {LATEST_FILE}")
    print(f"  Saved history: {history_file}")
    print(f"  Saved impact:  {IMPACT_LATEST_FILE}")
    print(f"  Saved activity:{ACTIVITY_LATEST_FILE}")
    print(f"  Saved registry:{REPORT_REGISTRY_FILE}")
    print(f"  Saved price route req:   {PRICE_ROUTE_REQUEST_FILE}")
    print(f"  Saved price route res:   {PRICE_ROUTE_RESULT_FILE}")
    print(f"  Saved listing route req: {LISTING_ROUTE_REQUEST_FILE}")
    print(f"  Saved listing route res: {LISTING_ROUTE_RESULT_FILE}")
    if run_errors and not results:
        print("  Note: report saved, but live API calls were blocked.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
