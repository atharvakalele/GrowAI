#!/usr/bin/env python3
"""
GoAmrita Ads — 7-Day Campaign Performance Report v1.0
=====================================================
Author: Msir + Claude
Date: 12 April 2026
Account: Made in Heavens (GoAmrita Bhandar)
Marketplace: Amazon.in (India) — EU Region

Uses: Amazon Ads Reporting API v3 (async report)
Endpoint: advertising-api-eu.amazon.com
reportTypeId: spCampaigns

Usage:
    python ads_report_7day_v1.0.py
"""

import json
import os
import sys
import ssl
import time
import gzip
import io
from datetime import datetime, timedelta
from urllib.request import Request, urlopen

# Fix Windows console encoding for emojis
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
from urllib.parse import urlencode
from urllib.error import HTTPError
from io import BytesIO

# ============================================
# CONFIGURATION
# ============================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDS_FILE = os.path.join(SCRIPT_DIR, "api_credentials.json")

def load_credentials():
    """Load credentials from JSON file"""
    with open(CREDS_FILE, "r") as f:
        return json.load(f)

CREDS = load_credentials()

CLIENT_ID = CREDS["client_id"]
CLIENT_SECRET = CREDS["client_secret"]
REFRESH_TOKEN = CREDS["refresh_token"]
PROFILE_ID = str(CREDS["profile_id"])
API_ENDPOINT = CREDS["api_endpoint"]  # https://advertising-api-eu.amazon.com
TOKEN_URL = CREDS["token_url"]

# SSL Context (certifi for Windows compatibility)
SSL_CONTEXT = None
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

# ============================================
# TOKEN MANAGEMENT
# ============================================
_cached_token = None
_token_expiry = None

def get_access_token():
    """Get fresh access token using refresh token"""
    global _cached_token, _token_expiry

    if _cached_token and _token_expiry and datetime.now() < _token_expiry:
        return _cached_token

    print("  🔄 Refreshing access token...")

    data = urlencode({
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }).encode()

    req = Request(TOKEN_URL, data=data, headers={
        "Content-Type": "application/x-www-form-urlencoded"
    })

    try:
        with urlopen(req, context=SSL_CONTEXT) as resp:
            result = json.loads(resp.read().decode())
            _cached_token = result["access_token"]
            _token_expiry = datetime.now() + timedelta(seconds=result["expires_in"] - 60)
            print("  ✅ Token ready!")
            return _cached_token
    except HTTPError as e:
        error_body = e.read().decode()
        print(f"  ❌ Token refresh failed: {e.code} — {error_body}")
        sys.exit(1)

# ============================================
# API HELPER
# ============================================
def api_call(method, path, body=None, headers_extra=None, raw_response=False):
    """Make authenticated API call"""
    token = get_access_token()
    url = f"{API_ENDPOINT}{path}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Amazon-Advertising-API-ClientId": CLIENT_ID,
        "Amazon-Advertising-API-Scope": PROFILE_ID,
    }

    if headers_extra:
        headers.update(headers_extra)

    data = json.dumps(body).encode() if body else None

    req = Request(url, data=data, headers=headers, method=method)

    try:
        with urlopen(req, context=SSL_CONTEXT) as resp:
            if raw_response:
                return resp.read(), resp.status
            return json.loads(resp.read().decode()), resp.status
    except HTTPError as e:
        error_body = e.read().decode()
        print(f"  ❌ API Error {e.code}: {path}")
        try:
            err = json.loads(error_body)
            print(f"     Message: {json.dumps(err, indent=2)}")
        except:
            print(f"     Response: {error_body[:500]}")
        return None, e.code

# ============================================
# STEP 1: CREATE REPORT REQUEST
# ============================================
def create_report(start_date, end_date):
    """Create async campaign performance report"""
    print(f"\n📋 Creating report: {start_date} to {end_date}...")

    body = {
        "name": f"GoAmrita SP Campaign Report {start_date} to {end_date}",
        "startDate": start_date,
        "endDate": end_date,
        "configuration": {
            "adProduct": "SPONSORED_PRODUCTS",
            "groupBy": ["campaign"],
            "columns": [
                "campaignName",
                "campaignId",
                "campaignStatus",
                "campaignBudgetAmount",
                "campaignBudgetType",
                "impressions",
                "clicks",
                "cost",
                "purchases1d",
                "purchases7d",
                "purchases14d",
                "purchases30d",
                "sales1d",
                "sales7d",
                "sales14d",
                "sales30d",
                "costPerClick",
                "clickThroughRate"
            ],
            "reportTypeId": "spCampaigns",
            "timeUnit": "DAILY",
            "format": "GZIP_JSON"
        }
    }

    result, status = api_call(
        "POST", "/reporting/reports",
        body=body,
        headers_extra={
            "Content-Type": "application/vnd.createasyncreportrequest.v3+json",
            "Accept": "application/vnd.createasyncreportrequest.v3+json"
        }
    )

    if result and "reportId" in result:
        report_id = result["reportId"]
        print(f"  ✅ Report created! ID: {report_id}")
        print(f"     Status: {result.get('status', 'N/A')}")
        return report_id
    else:
        print(f"  ❌ Failed to create report. Response: {result}")
        return None

# ============================================
# STEP 2: POLL FOR REPORT COMPLETION
# ============================================
def wait_for_report(report_id, max_wait=300, poll_interval=10):
    """Poll report status until complete or timeout"""
    print(f"\n⏳ Waiting for report {report_id}...")

    elapsed = 0
    while elapsed < max_wait:
        result, status = api_call(
            "GET", f"/reporting/reports/{report_id}",
            headers_extra={
                "Accept": "application/vnd.createasyncreportrequest.v3+json"
            }
        )

        if not result:
            print(f"  ❌ Failed to check report status")
            return None

        report_status = result.get("status", "UNKNOWN")
        print(f"  📊 Status: {report_status} ({elapsed}s elapsed)")

        if report_status == "COMPLETED":
            download_url = result.get("url")
            if download_url:
                print(f"  ✅ Report ready! Download URL obtained.")
                return download_url
            else:
                print(f"  ❌ Report completed but no download URL")
                return None

        elif report_status == "FAILURE":
            print(f"  ❌ Report FAILED!")
            print(f"     Details: {json.dumps(result, indent=2)}")
            return None

        time.sleep(poll_interval)
        elapsed += poll_interval

    print(f"  ❌ Timeout after {max_wait}s")
    return None

# ============================================
# STEP 3: DOWNLOAD & PARSE REPORT
# ============================================
def download_report(download_url):
    """Download and decompress GZIP_JSON report"""
    print(f"\n📥 Downloading report...")

    req = Request(download_url)

    try:
        with urlopen(req, context=SSL_CONTEXT) as resp:
            compressed_data = resp.read()
            print(f"  📦 Downloaded: {len(compressed_data):,} bytes (compressed)")

            # Decompress GZIP
            decompressed = gzip.decompress(compressed_data)
            data = json.loads(decompressed.decode())

            print(f"  ✅ Parsed: {len(data)} rows")
            return data

    except HTTPError as e:
        print(f"  ❌ Download failed: {e.code}")
        return None
    except Exception as e:
        print(f"  ❌ Parse error: {str(e)}")
        return None

# ============================================
# STEP 4: DISPLAY REPORT
# ============================================
def display_report(data, start_date, end_date):
    """Format and display campaign performance report"""
    print("\n" + "=" * 90)
    print(f"📊 SPONSORED PRODUCTS — CAMPAIGN PERFORMANCE REPORT")
    print(f"📅 Period: {start_date} to {end_date}")
    print(f"🏪 Account: Made in Heavens | 🇮🇳 amazon.in")
    print(f"📅 Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p IST')}")
    print("=" * 90)

    if not data:
        print("  ⚠️ No data returned for this period.")
        return

    # Aggregate by campaign
    campaigns = {}
    for row in data:
        camp_id = row.get("campaignId", "Unknown")
        camp_name = row.get("campaignName", "Unnamed")
        key = camp_id

        if key not in campaigns:
            campaigns[key] = {
                "name": camp_name,
                "status": row.get("campaignStatus", "N/A"),
                "budget": float(row.get("campaignBudgetAmount", 0)),
                "impressions": 0,
                "clicks": 0,
                "cost": 0.0,
                "orders_7d": 0,
                "sales_7d": 0.0,
                "days": 0
            }

        campaigns[key]["impressions"] += int(row.get("impressions", 0))
        campaigns[key]["clicks"] += int(row.get("clicks", 0))
        campaigns[key]["cost"] += float(row.get("cost", 0))
        campaigns[key]["orders_7d"] += int(row.get("purchases7d", 0))
        campaigns[key]["sales_7d"] += float(row.get("sales7d", 0))
        campaigns[key]["days"] += 1

    # Sort by cost (highest spend first)
    sorted_camps = sorted(campaigns.items(), key=lambda x: x[1]["cost"], reverse=True)

    # Totals
    total_impressions = sum(c["impressions"] for _, c in sorted_camps)
    total_clicks = sum(c["clicks"] for _, c in sorted_camps)
    total_cost = sum(c["cost"] for _, c in sorted_camps)
    total_orders = sum(c["orders_7d"] for _, c in sorted_camps)
    total_sales = sum(c["sales_7d"] for _, c in sorted_camps)
    total_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    total_acos = (total_cost / total_sales * 100) if total_sales > 0 else 0
    total_roas = (total_sales / total_cost) if total_cost > 0 else 0
    total_cpc = (total_cost / total_clicks) if total_clicks > 0 else 0

    # === SUMMARY BOX ===
    print("\n" + "─" * 90)
    print("📈 OVERALL SUMMARY (7 Days)")
    print("─" * 90)
    print(f"  🔍 Impressions:  {total_impressions:>12,}")
    print(f"  👆 Clicks:       {total_clicks:>12,}")
    print(f"  📊 CTR:          {total_ctr:>11.2f}%")
    print(f"  💰 Total Spend:  ₹{total_cost:>11,.2f}")
    print(f"  💵 CPC:          ₹{total_cpc:>11,.2f}")
    print(f"  🛒 Orders (7d):  {total_orders:>12,}")
    print(f"  📦 Sales (7d):   ₹{total_sales:>11,.2f}")
    print(f"  📉 ACOS:         {total_acos:>11.2f}%")
    print(f"  📈 ROAS:         {total_roas:>11.2f}x")
    print(f"  📢 Active Camps: {len([c for _, c in sorted_camps if c['cost'] > 0])}")
    print("─" * 90)

    # === PER CAMPAIGN TABLE ===
    print(f"\n{'#':<4} {'Campaign Name':<40} {'Impr':>10} {'Clicks':>8} {'Spend (₹)':>12} {'Orders':>8} {'Sales (₹)':>12} {'ACOS%':>8}")
    print("─" * 104)

    for i, (camp_id, c) in enumerate(sorted_camps, 1):
        if c["cost"] == 0 and c["impressions"] == 0:
            continue  # Skip zero-activity campaigns

        name = c["name"][:39]
        acos = (c["cost"] / c["sales_7d"] * 100) if c["sales_7d"] > 0 else 0

        # ACOS indicator
        acos_str = f"{acos:.1f}%"
        if acos > 50:
            acos_str = f"🔴{acos:.1f}%"
        elif acos > 30:
            acos_str = f"🟡{acos:.1f}%"
        else:
            acos_str = f"🟢{acos:.1f}%"

        print(f"{i:<4} {name:<40} {c['impressions']:>10,} {c['clicks']:>8,} {c['cost']:>12,.2f} {c['orders_7d']:>8,} {c['sales_7d']:>12,.2f} {acos_str:>8}")

    print("─" * 104)
    total_acos_str = f"{total_acos:.1f}%"
    print(f"{'':4} {'TOTAL':<40} {total_impressions:>10,} {total_clicks:>8,} {total_cost:>12,.2f} {total_orders:>8,} {total_sales:>12,.2f} {total_acos_str:>8}")
    print("=" * 90)

    # === TOP 5 SPENDERS ===
    print("\n🔝 TOP 5 SPENDERS:")
    for i, (_, c) in enumerate(sorted_camps[:5], 1):
        acos = (c["cost"] / c["sales_7d"] * 100) if c["sales_7d"] > 0 else 0
        print(f"  {i}. {c['name'][:50]} — ₹{c['cost']:,.2f} spend | {c['orders_7d']} orders | ACOS: {acos:.1f}%")

    # === TOP 5 BY ORDERS ===
    by_orders = sorted(sorted_camps, key=lambda x: x[1]["orders_7d"], reverse=True)
    print("\n🏆 TOP 5 BY ORDERS:")
    for i, (_, c) in enumerate(by_orders[:5], 1):
        acos = (c["cost"] / c["sales_7d"] * 100) if c["sales_7d"] > 0 else 0
        print(f"  {i}. {c['name'][:50]} — {c['orders_7d']} orders | ₹{c['sales_7d']:,.2f} sales | ACOS: {acos:.1f}%")

    # === WORST ACOS (problem campaigns) ===
    with_sales = [(k, c) for k, c in sorted_camps if c["sales_7d"] > 0 and c["cost"] > 100]
    worst_acos = sorted(with_sales, key=lambda x: (x[1]["cost"] / x[1]["sales_7d"]) if x[1]["sales_7d"] > 0 else 999, reverse=True)
    if worst_acos:
        print("\n🔴 WORST ACOS (Spend > ₹100, needs attention):")
        for i, (_, c) in enumerate(worst_acos[:5], 1):
            acos = (c["cost"] / c["sales_7d"] * 100) if c["sales_7d"] > 0 else 0
            print(f"  {i}. {c['name'][:50]} — ACOS: {acos:.1f}% | ₹{c['cost']:,.2f} spend | {c['orders_7d']} orders")

    # === ZERO SALES (wasted spend) ===
    zero_sales = [(k, c) for k, c in sorted_camps if c["sales_7d"] == 0 and c["cost"] > 50]
    if zero_sales:
        zero_sales_sorted = sorted(zero_sales, key=lambda x: x[1]["cost"], reverse=True)
        total_wasted = sum(c["cost"] for _, c in zero_sales_sorted)
        print(f"\n⚠️ ZERO SALES CAMPAIGNS (Spend > ₹50 wasted: ₹{total_wasted:,.2f}):")
        for i, (_, c) in enumerate(zero_sales_sorted[:10], 1):
            print(f"  {i}. {c['name'][:50]} — ₹{c['cost']:,.2f} spent, {c['clicks']} clicks, 0 orders")

    print("\n" + "=" * 90)
    print("✅ Report complete!")
    print("=" * 90)

# ============================================
# MAIN
# ============================================
def main():
    print("\n" + "=" * 90)
    print("🚀 GoAmrita Ads — 7-Day Campaign Performance Report v1.0")
    print(f"📅 {datetime.now().strftime('%d %B %Y, %I:%M %p IST')}")
    print(f"🏪 Account: Made in Heavens | 🇮🇳 amazon.in")
    print("=" * 90)

    # Date range: last 7 days (excluding today as data may be incomplete)
    end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    print(f"\n📅 Report Period: {start_date} to {end_date}")

    # Step 1: Create report
    report_id = create_report(start_date, end_date)
    if not report_id:
        print("\n❌ Cannot proceed without report ID. Exiting.")
        sys.exit(1)

    # Step 2: Wait for completion
    download_url = wait_for_report(report_id, max_wait=300, poll_interval=10)
    if not download_url:
        print("\n❌ Report did not complete. Exiting.")
        sys.exit(1)

    # Step 3: Download
    data = download_report(download_url)
    if data is None:
        print("\n❌ Failed to download report. Exiting.")
        sys.exit(1)

    # Step 4: Display
    display_report(data, start_date, end_date)

    # Save raw data for reference
    output_file = os.path.join(SCRIPT_DIR, f"report_7day_{start_date}_to_{end_date}.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Raw data saved: {output_file}")


if __name__ == "__main__":
    main()
