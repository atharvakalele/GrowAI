#!/usr/bin/env python3
"""
GoAmrita - Fetch Actual Selling Prices via SP-API Pricing v1.0
===============================================================
Uses: Pricing API v2022-05-01 (getCompetitiveSummary)
Returns: Your Price, Buy Box winner, Reference Prices, Fulfillment type

Rate: 0.033 req/sec = ~2 per minute (SLOW! batch + queue required)
Batch: max 20 ASINs per request

Usage: python fetch_pricing_v1.0.py
"""

import json
import os
import sys
import ssl
import time
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
SP_CREDS_FILE = os.path.join(PROJECT_DIR, "sp_api_credentials.json")

REPORT_BASE = os.path.join(SCRIPT_DIR, "..", "Report")
report_folders = [f for f in os.listdir(REPORT_BASE) if os.path.isdir(os.path.join(REPORT_BASE, f))]
report_folders.sort(key=lambda x: os.path.getmtime(os.path.join(REPORT_BASE, x)), reverse=True)
LATEST_REPORT = report_folders[0] if report_folders else datetime.now().strftime("%d %B %Y")
JSON_DIR = os.path.join(REPORT_BASE, LATEST_REPORT, "Json")

MARKETPLACE_ID = "A21TJRUUN4KGV"
OUR_SELLER_ID = "A2AC2AS9R9CBEA"
SP_ENDPOINT = "https://sellingpartnerapi-eu.amazon.com"
TOKEN_URL = "https://api.amazon.com/auth/o2/token"

SSL_CONTEXT = None
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

BATCH_SIZE = 20
DELAY_BETWEEN = 32  # 0.033 req/sec = 1 per 30 sec, 32 for safety

SP = json.load(open(SP_CREDS_FILE))["sp_api_credentials"]

_cached_token = None
_token_expiry = None

def get_token():
    global _cached_token, _token_expiry
    if _cached_token and _token_expiry and datetime.now() < _token_expiry:
        return _cached_token
    data = urlencode({"grant_type": "refresh_token", "refresh_token": SP["refresh_token"],
                      "client_id": SP["lwa_client_id"], "client_secret": SP["lwa_client_secret"]}).encode()
    req = Request(TOKEN_URL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    result = json.loads(urlopen(req, context=SSL_CONTEXT).read().decode())
    _cached_token = result["access_token"]
    _token_expiry = datetime.now() + timedelta(seconds=result["expires_in"] - 60)
    return _cached_token


def fetch_pricing_batch(asin_list):
    token = get_token()
    body = {"requests": []}
    for asin in asin_list:
        body["requests"].append({
            "asin": asin,
            "marketplaceId": MARKETPLACE_ID,
            "includedData": ["featuredBuyingOptions", "referencePrices"],
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
        return json.loads(resp.read().decode())
    except HTTPError as e:
        print(f"    API Error {e.code}: {e.read().decode()[:200]}")
        return None


def extract_pricing(response):
    results = {}
    for r in response.get("responses", []):
        rbody = r.get("body", {})
        asin = rbody.get("asin", "")
        if not asin:
            continue

        price = 0
        seller_id = ""
        fulfillment = ""
        is_our_buybox = False
        ref_prices = {}

        fbo = rbody.get("featuredBuyingOptions", [])
        for opt in fbo:
            for offer in opt.get("segmentedFeaturedOffers", []):
                lp = offer.get("listingPrice", {})
                price = float(lp.get("amount", 0))
                seller_id = offer.get("sellerId", "")
                fulfillment = offer.get("fulfillmentType", "")
                is_our_buybox = seller_id == OUR_SELLER_ID
                break

        for rp in rbody.get("referencePrices", []):
            ref_prices[rp["name"]] = float(rp["price"]["amount"])

        results[asin] = {
            "your_price": price,
            "buy_box_winner": is_our_buybox,
            "seller_id": seller_id,
            "fulfillment": fulfillment,
            "was_price": ref_prices.get("WasPrice", 0),
            "list_price": ref_prices.get("ListPrice", 0),
            "ref_prices": ref_prices
        }
    return results


def main():
    print("=" * 70)
    print("  GoAmrita - Fetch Actual Prices (Pricing API v2022-05-01)")
    print(f"  {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print(f"  Rate: ~2 requests/min (slow API - please wait)")
    print("=" * 70)

    # Load ASINs
    ads_file = os.path.join(JSON_DIR, "sp_product_ads_list.json")
    with open(ads_file, "r", encoding="utf-8") as f:
        ads = json.load(f)
    all_asins = list(set(a.get("asin", "") for a in ads if a.get("asin")))
    print(f"\n  {len(all_asins)} unique ASINs to price")

    batches = [all_asins[i:i+BATCH_SIZE] for i in range(0, len(all_asins), BATCH_SIZE)]
    est_time = len(batches) * DELAY_BETWEEN
    print(f"  {len(batches)} batches x {DELAY_BETWEEN}s delay = ~{est_time//60}min {est_time%60}s estimated")

    all_prices = {}
    for i, batch in enumerate(batches):
        print(f"  Batch {i+1}/{len(batches)} ({len(batch)} ASINs)...", end=" ", flush=True)
        resp = fetch_pricing_batch(batch)
        if resp:
            prices = extract_pricing(resp)
            all_prices.update(prices)
            got_price = sum(1 for v in prices.values() if v["your_price"] > 0)
            print(f"{len(prices)} items, {got_price} with price")
        else:
            print("FAILED")

        if i < len(batches) - 1:
            print(f"    Waiting {DELAY_BETWEEN}s (rate limit)...", flush=True)
            time.sleep(DELAY_BETWEEN)

    # Stats
    total = len(all_prices)
    with_price = sum(1 for v in all_prices.values() if v["your_price"] > 0)
    our_buybox = sum(1 for v in all_prices.values() if v["buy_box_winner"])
    lost_buybox = sum(1 for v in all_prices.values() if not v["buy_box_winner"] and v["your_price"] > 0)

    print(f"\n  RESULTS:")
    print(f"  Total fetched: {total}")
    print(f"  With price: {with_price}")
    print(f"  Our Buy Box: {our_buybox}")
    print(f"  Lost Buy Box: {lost_buybox}")

    # Save
    output = os.path.join(JSON_DIR, "sp_pricing_data.json")
    with open(output, "w", encoding="utf-8") as f:
        json.dump(all_prices, f, indent=2, ensure_ascii=False)
    print(f"\n  Saved: {output}")

    # Update true profit with real prices
    profit_file = os.path.join(JSON_DIR, "true_profit_per_asin.json")
    config_file = os.path.join(PROJECT_DIR, "config_true_profit.json")

    if os.path.exists(profit_file) and os.path.exists(config_file):
        with open(profit_file, "r", encoding="utf-8") as f:
            profits = json.load(f)
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)

        updated = 0
        for p in profits:
            asin = p.get("asin", "")
            if asin in all_prices and all_prices[asin]["your_price"] > 0:
                real_price = all_prices[asin]["your_price"]
                p["sale_price_api"] = real_price
                p["buy_box_winner"] = all_prices[asin]["buy_box_winner"]
                p["fulfillment"] = all_prices[asin]["fulfillment"]

                # Recalculate true profit with real price
                cost = p.get("product_cost", 85)
                ref_pct = config["amazon_fees"].get("referral_fee_pct", 3.0)
                closing = config["amazon_fees"].get("closing_fee", 5)
                shipping = config["shipping"]["default"]
                return_rate = config["return_rate"]["default_percent"] / 100

                amazon_fee = (ref_pct / 100 * real_price) + closing
                return_cost = return_rate * real_price
                true_profit = real_price - cost - amazon_fee - shipping - return_cost
                true_profit_pct = (true_profit / real_price * 100) if real_price > 0 else 0

                p["sale_price_real"] = real_price
                p["true_profit_real"] = round(true_profit, 2)
                p["true_profit_pct_real"] = round(true_profit_pct, 1)
                p["profitable_real"] = true_profit > 0
                updated += 1

        with open(profit_file, "w", encoding="utf-8") as f:
            json.dump(profits, f, indent=2, ensure_ascii=False)
        print(f"  Updated true_profit: {updated} ASINs with REAL price + recalculated profit")

    # Show top prices
    print(f"\n  TOP 10 by Price:")
    sorted_prices = sorted(all_prices.items(), key=lambda x: x[1]["your_price"], reverse=True)
    for asin, p in sorted_prices[:10]:
        bb = "OUR BB" if p["buy_box_winner"] else "LOST BB"
        print(f"    {asin} | Rs.{p['your_price']:>7.0f} | {p['fulfillment']:<4} | {bb}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
