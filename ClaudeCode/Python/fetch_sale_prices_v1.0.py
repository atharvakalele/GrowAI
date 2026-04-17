#!/usr/bin/env python3
"""
GoAmrita - Fetch Sale Prices via SP-API v1.0
=============================================
Author: Msir + Claude
Date: 13 April 2026

Fetches actual sale prices for all ASINs using SP-API Catalog Items API v2022-04-01
Then updates true_profit_per_asin.json with real prices

API: Catalog Items v2022-04-01
Endpoint: sellingpartnerapi-eu.amazon.com
Rate: 2 req/sec (burst: 2) — max 20 ASINs per request
Marketplace: A21TJRUUN4KGV (India)

Usage:
    python fetch_sale_prices_v1.0.py
"""

import json
import os
import sys
import ssl
import time
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote
from urllib.error import HTTPError

# ============================================
# CONFIGURATION
# ============================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
SP_CREDS_FILE = os.path.join(PROJECT_DIR, "sp_api_credentials.json")

REPORT_BASE = os.path.join(SCRIPT_DIR, "..", "Report")
report_folders = [f for f in os.listdir(REPORT_BASE) if os.path.isdir(os.path.join(REPORT_BASE, f))]
report_folders.sort(key=lambda x: os.path.getmtime(os.path.join(REPORT_BASE, x)), reverse=True)
LATEST_REPORT = report_folders[0] if report_folders else datetime.now().strftime("%d %B %Y")
JSON_DIR = os.path.join(REPORT_BASE, LATEST_REPORT, "Json")

MARKETPLACE_ID = "A21TJRUUN4KGV"
SP_API_ENDPOINT = "https://sellingpartnerapi-eu.amazon.com"
TOKEN_URL = "https://api.amazon.com/auth/o2/token"

SSL_CONTEXT = None
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

# Rate limit: 2 req/sec, max 20 ASINs per batch
BATCH_SIZE = 20
DELAY_BETWEEN_BATCHES = 0.6  # seconds (safe margin for 2 req/sec)

# ============================================
# LOAD CREDENTIALS
# ============================================
def load_sp_creds():
    with open(SP_CREDS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["sp_api_credentials"]

SP = load_sp_creds()

# ============================================
# TOKEN MANAGEMENT
# ============================================
_cached_token = None
_token_expiry = None

def get_access_token():
    global _cached_token, _token_expiry
    if _cached_token and _token_expiry and datetime.now() < _token_expiry:
        return _cached_token

    print("  Refreshing SP-API access token...")
    data = urlencode({
        "grant_type": "refresh_token",
        "refresh_token": SP["refresh_token"],
        "client_id": SP["lwa_client_id"],
        "client_secret": SP["lwa_client_secret"]
    }).encode()

    req = Request(TOKEN_URL, data=data, headers={
        "Content-Type": "application/x-www-form-urlencoded"
    })

    try:
        with urlopen(req, context=SSL_CONTEXT) as resp:
            result = json.loads(resp.read().decode())
            _cached_token = result["access_token"]
            _token_expiry = datetime.now() + timedelta(seconds=result["expires_in"] - 60)
            print("  Token ready!")
            return _cached_token
    except HTTPError as e:
        print(f"  Token FAILED: {e.code} — {e.read().decode()[:300]}")
        sys.exit(1)

# ============================================
# SP-API CALL
# ============================================
def sp_api_call(method, path, params=None):
    token = get_access_token()

    url = f"{SP_API_ENDPOINT}{path}"
    if params:
        url += "?" + urlencode(params, doseq=True)

    headers = {
        "x-amz-access-token": token,
        "x-amz-date": datetime.utcnow().strftime('%Y%m%dT%H%M%SZ'),
        "user-agent": "GoAmrita/1.0 (Language=Python/3.11; Platform=Windows)",
        "Host": "sellingpartnerapi-eu.amazon.com",
        "Content-Type": "application/json"
    }

    req = Request(url, headers=headers, method=method)

    try:
        with urlopen(req, context=SSL_CONTEXT) as resp:
            return json.loads(resp.read().decode()), resp.status
    except HTTPError as e:
        error_body = e.read().decode()
        print(f"  API Error {e.code}: {path[:60]}")
        print(f"    {error_body[:300]}")
        return None, e.code

# ============================================
# FETCH CATALOG ITEMS (batch of ASINs)
# ============================================
def fetch_catalog_batch(asin_list):
    """Fetch catalog data for up to 20 ASINs at once"""
    params = {
        "identifiers": ",".join(asin_list),
        "identifiersType": "ASIN",
        "marketplaceIds": MARKETPLACE_ID,
        "includedData": "summaries,attributes,salesRanks",
        "locale": "en_IN"
    }

    result, status = sp_api_call("GET", "/catalog/2022-04-01/items", params)

    if result and "items" in result:
        return result["items"]
    return []

# ============================================
# EXTRACT PRICE FROM CATALOG ITEM
# ============================================
def extract_price(item):
    """Extract sale price from catalog item attributes"""
    asin = item.get("asin", "")
    price = 0
    source = "not_found"
    title = ""
    brand = ""
    bsr = 0

    # Try summaries first (itemName, brand)
    summaries = item.get("summaries", [])
    for s in summaries:
        if s.get("marketplaceId") == MARKETPLACE_ID:
            title = s.get("itemName", "")
            brand = s.get("brand", "")
            break

    # Try attributes for price
    attrs = item.get("attributes", {})

    # list_price is common
    if "list_price" in attrs:
        lp = attrs["list_price"]
        if isinstance(lp, list) and len(lp) > 0:
            price = float(lp[0].get("value", 0))
            source = "list_price"
        elif isinstance(lp, dict):
            price = float(lp.get("value", 0))
            source = "list_price"

    # item_price / our_price
    for price_key in ["item_price", "our_price", "purchasable_offer"]:
        if price == 0 and price_key in attrs:
            pp = attrs[price_key]
            if isinstance(pp, list) and len(pp) > 0:
                val = pp[0]
                if isinstance(val, dict):
                    price = float(val.get("value", val.get("amount", 0)))
                    source = price_key
            elif isinstance(pp, dict):
                price = float(pp.get("value", pp.get("amount", 0)))
                source = price_key

    # salesRanks for BSR
    ranks = item.get("salesRanks", [])
    for r in ranks:
        if r.get("marketplaceId") == MARKETPLACE_ID:
            class_ranks = r.get("classificationRanks", [])
            if class_ranks:
                bsr = class_ranks[0].get("rank", 0)
            display_ranks = r.get("displayGroupRanks", [])
            if not bsr and display_ranks:
                bsr = display_ranks[0].get("rank", 0)
            break

    return {
        "asin": asin,
        "title": title[:60],
        "brand": brand,
        "price": price,
        "price_source": source,
        "bsr": bsr
    }

# ============================================
# MAIN
# ============================================
def main():
    print("=" * 70)
    print("  GoAmrita - Fetch Sale Prices via SP-API v1.0")
    print(f"  Date: {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print(f"  API: Catalog Items v2022-04-01")
    print(f"  Endpoint: {SP_API_ENDPOINT}")
    print("=" * 70)

    # Load ASINs from product ads list
    print("\n[1/4] Loading ASINs...")
    ads_file = os.path.join(JSON_DIR, "sp_product_ads_list.json")
    if not os.path.exists(ads_file):
        print(f"  File not found: {ads_file}")
        print("  Run sp_ads_complete_import_v1.0.py first!")
        sys.exit(1)

    with open(ads_file, "r", encoding="utf-8") as f:
        ads = json.load(f)

    # Unique ASINs
    all_asins = list(set(a.get("asin", "") for a in ads if a.get("asin")))
    print(f"  Found {len(all_asins)} unique ASINs")

    # Batch into groups of 20
    batches = [all_asins[i:i+BATCH_SIZE] for i in range(0, len(all_asins), BATCH_SIZE)]
    print(f"  Batches: {len(batches)} (max {BATCH_SIZE} ASINs each)")
    print(f"  Estimated time: {len(batches) * DELAY_BETWEEN_BATCHES:.0f} seconds")

    # Fetch
    print(f"\n[2/4] Fetching prices from SP-API Catalog...")
    all_items = {}
    success = 0
    failed = 0

    for i, batch in enumerate(batches):
        print(f"  Batch {i+1}/{len(batches)} ({len(batch)} ASINs)...", end=" ")
        items = fetch_catalog_batch(batch)

        if items:
            for item in items:
                data = extract_price(item)
                all_items[data["asin"]] = data
            print(f"{len(items)} items received")
            success += len(items)
        else:
            print("FAILED")
            failed += len(batch)

        # Rate limit delay
        if i < len(batches) - 1:
            time.sleep(DELAY_BETWEEN_BATCHES)

    print(f"\n  Total fetched: {success} | Failed: {failed}")

    # Stats
    with_price = sum(1 for v in all_items.values() if v["price"] > 0)
    without_price = sum(1 for v in all_items.values() if v["price"] == 0)
    with_bsr = sum(1 for v in all_items.values() if v["bsr"] > 0)
    print(f"  With price: {with_price} | Without price: {without_price}")
    print(f"  With BSR: {with_bsr}")

    # Show sample
    print(f"\n[3/4] Sample prices:")
    print(f"  {'ASIN':<14} {'Title':<35} {'Price':>8} {'BSR':>8} {'Source'}")
    print(f"  {'-'*85}")
    sorted_items = sorted(all_items.values(), key=lambda x: x["price"], reverse=True)
    for item in sorted_items[:15]:
        print(f"  {item['asin']:<14} {item['title'][:34]:<35} Rs.{item['price']:>6.0f} {item['bsr']:>8} {item['price_source']}")

    # Save
    print(f"\n[4/4] Saving...")
    output_file = os.path.join(JSON_DIR, "sp_catalog_prices.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_items, f, indent=2, ensure_ascii=False)
    size_kb = os.path.getsize(output_file) / 1024
    print(f"  Saved: {output_file} ({size_kb:.1f} KB)")

    # Also update true_profit if it exists
    profit_file = os.path.join(JSON_DIR, "true_profit_per_asin.json")
    if os.path.exists(profit_file):
        with open(profit_file, "r", encoding="utf-8") as f:
            profits = json.load(f)

        updated = 0
        for p in profits:
            asin = p.get("asin", "")
            if asin in all_items and all_items[asin]["price"] > 0:
                catalog_price = all_items[asin]["price"]
                if p.get("price_source") == "fallback" or catalog_price > 0:
                    p["sale_price_catalog"] = catalog_price
                    p["catalog_title"] = all_items[asin]["title"]
                    p["bsr"] = all_items[asin]["bsr"]
                    updated += 1

        with open(profit_file, "w", encoding="utf-8") as f:
            json.dump(profits, f, indent=2, ensure_ascii=False)
        print(f"  Updated true_profit_per_asin.json: {updated} ASINs enriched with catalog price")

    print(f"\n  Done!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
