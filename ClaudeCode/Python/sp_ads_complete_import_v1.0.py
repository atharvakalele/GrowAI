#!/usr/bin/env python3
"""
GoAmrita — Sponsored Products Complete Data Import v1.0
=======================================================
Author: Msir + Claude
Date: 12 April 2026
Account: Made in Heavens (GoAmrita Bhandar)
Marketplace: Amazon.in (India) — EU Region

Phase 0.1: Import ALL Sponsored Products data (last 7 days)

7 Report Types:
  1. spCampaigns     — Campaign-level metrics (daily)
  2. spSearchTerm    — Search term report (daily)
  3. spTargeting     — Keyword/target-level metrics (daily)
  4. spAdvertisedProduct — Product ad-level metrics (daily)
  5. spPurchasedProduct  — Purchased product attribution (daily)
  6. spCampaigns (summary) — Campaign-level (summary, no daily)

Plus:
  7. Campaign list via Ads API v1 Unified (structure, budgets, states)

Output: JSON files + Excel summary

Usage:
    python sp_ads_complete_import_v1.0.py
    python sp_ads_complete_import_v1.0.py --reports campaigns,searchterm
    python sp_ads_complete_import_v1.0.py --days 14
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
from urllib.parse import urlencode
from urllib.error import HTTPError
from io import BytesIO
import argparse

# Fix Windows console encoding for emojis
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ============================================
# CONFIGURATION
# ============================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
CREDS_FILE = os.path.join(PROJECT_DIR, "api_credentials.json")

TODAY = datetime.now().strftime("%d %B %Y")
REPORT_DIR = os.path.join(SCRIPT_DIR, "..", "Report", TODAY, "Json")

def load_credentials():
    with open(CREDS_FILE, "r") as f:
        return json.load(f)

CREDS = load_credentials()
CLIENT_ID = CREDS["client_id"]
CLIENT_SECRET = CREDS["client_secret"]
REFRESH_TOKEN = CREDS["refresh_token"]
PROFILE_ID = str(CREDS["profile_id"])
API_ENDPOINT = CREDS["api_endpoint"]
TOKEN_URL = CREDS["token_url"]

SSL_CONTEXT = None
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

# ============================================
# REPORT DEFINITIONS — All Sponsored Products reports
# ============================================
REPORT_TYPES = {
    "campaigns_daily": {
        "name": "SP Campaigns (Daily)",
        "reportTypeId": "spCampaigns",
        "groupBy": ["campaign"],
        "timeUnit": "DAILY",
        "columns": [
            "campaignName", "campaignId", "campaignStatus",
            "campaignBudgetAmount", "campaignBudgetType",
            "impressions", "clicks", "cost",
            "purchases1d", "purchases7d", "purchases14d", "purchases30d",
            "sales1d", "sales7d", "sales14d", "sales30d",
            "costPerClick", "clickThroughRate"
        ],
        "filename": "sp_campaigns_daily.json"
    },
    "campaigns_summary": {
        "name": "SP Campaigns (Summary)",
        "reportTypeId": "spCampaigns",
        "groupBy": ["campaign"],
        "timeUnit": "SUMMARY",
        "columns": [
            "campaignName", "campaignId", "campaignStatus",
            "campaignBudgetAmount", "campaignBudgetType",
            "impressions", "clicks", "cost",
            "purchases7d", "sales7d",
            "costPerClick", "clickThroughRate"
        ],
        "filename": "sp_campaigns_summary.json"
    },
    "searchterm": {
        "name": "SP Search Terms (Daily)",
        "reportTypeId": "spSearchTerm",
        "groupBy": ["searchTerm"],
        "timeUnit": "DAILY",
        "columns": [
            "searchTerm", "campaignName", "campaignId",
            "adGroupName", "adGroupId",
            "keyword", "keywordId", "keywordType",
            "impressions", "clicks", "cost",
            "purchases7d", "sales7d",
            "costPerClick", "clickThroughRate"
        ],
        "filename": "sp_searchterm_daily.json"
    },
    "targeting": {
        "name": "SP Targeting/Keywords (Daily)",
        "reportTypeId": "spTargeting",
        "groupBy": ["targeting"],
        "timeUnit": "DAILY",
        "columns": [
            "campaignName", "campaignId",
            "adGroupName", "adGroupId",
            "keyword", "keywordId", "matchType",
            "impressions", "clicks", "cost",
            "purchases7d", "sales7d",
            "costPerClick", "clickThroughRate"
        ],
        "filename": "sp_targeting_daily.json"
    },
    "advertisedproduct": {
        "name": "SP Advertised Products (Daily)",
        "reportTypeId": "spAdvertisedProduct",
        "groupBy": ["advertiser"],
        "timeUnit": "DAILY",
        "columns": [
            "campaignName", "campaignId",
            "adGroupName", "adGroupId",
            "advertisedAsin", "advertisedSku",
            "impressions", "clicks", "cost",
            "purchases7d", "sales7d",
            "costPerClick", "clickThroughRate"
        ],
        "filename": "sp_advertisedproduct_daily.json"
    },
    "purchasedproduct": {
        "name": "SP Purchased Products (Daily)",
        "reportTypeId": "spPurchasedProduct",
        "groupBy": ["asin"],
        "timeUnit": "DAILY",
        "columns": [
            "campaignName", "campaignId",
            "adGroupName", "adGroupId",
            "keyword", "matchType",
            "purchasedAsin", "advertisedAsin", "advertisedSku",
            "purchases7d", "sales7d"
        ],
        "filename": "sp_purchasedproduct_daily.json"
    }
}

# ============================================
# TOKEN MANAGEMENT
# ============================================
_cached_token = None
_token_expiry = None

def get_access_token():
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
# API HELPERS
# ============================================
def api_call(method, path, body=None, headers_extra=None, raw_response=False):
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
        err_json = None
        try:
            err_json = json.loads(error_body)
        except Exception:
            pass
        # Handle 425 "Duplicate" — return existing report ID
        if e.code == 425 and err_json:
            detail = err_json.get("detail", "")
            # Extract report ID from "The Request is a duplicate of : <id>"
            import re as _re
            dup_match = _re.search(r'duplicate of\s*:\s*([a-f0-9-]+)', detail)
            if dup_match:
                dup_id = dup_match.group(1)
                print(f"  🔄 [{path}] Duplicate report exists: {dup_id} — will poll this instead")
                return {"reportId": dup_id, "_duplicate": True}, 425
        print(f"  ❌ API Error {e.code}: {path}")
        if err_json:
            print(f"     {json.dumps(err_json, indent=2)[:500]}")
        else:
            print(f"     {error_body[:500]}")
        return None, e.code

# ============================================
# REPORT: CREATE → POLL → DOWNLOAD
# ============================================
def create_report(report_key, start_date, end_date):
    cfg = REPORT_TYPES[report_key]
    print(f"\n📋 [{cfg['name']}] Creating report: {start_date} to {end_date}...")

    body = {
        "name": f"GoAmrita {cfg['name']} {start_date} to {end_date}",
        "startDate": start_date,
        "endDate": end_date,
        "configuration": {
            "adProduct": "SPONSORED_PRODUCTS",
            "groupBy": cfg["groupBy"],
            "columns": cfg["columns"],
            "reportTypeId": cfg["reportTypeId"],
            "timeUnit": cfg["timeUnit"],
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
        if result.get("_duplicate"):
            print(f"  ♻️ Using existing report: {result['reportId']}")
        else:
            print(f"  ✅ Report created! ID: {result['reportId']}")
        return result["reportId"]
    else:
        print(f"  ❌ Failed to create report")
        return None

def wait_for_report(report_id, report_name, max_wait=600, poll_interval=15):
    print(f"  ⏳ [{report_name}] Waiting for report...")
    elapsed = 0
    while elapsed < max_wait:
        result, status = api_call(
            "GET", f"/reporting/reports/{report_id}",
            headers_extra={
                "Accept": "application/vnd.createasyncreportrequest.v3+json"
            }
        )

        if not result:
            return None

        report_status = result.get("status", "UNKNOWN")

        if report_status == "COMPLETED":
            download_url = result.get("url")
            if download_url:
                print(f"  ✅ [{report_name}] Ready! ({elapsed}s)")
                return download_url
            return None
        elif report_status == "FAILURE":
            print(f"  ❌ [{report_name}] FAILED: {json.dumps(result, indent=2)[:300]}")
            return None

        if elapsed % 30 == 0 and elapsed > 0:
            print(f"     [{report_name}] Still processing... ({elapsed}s)")

        time.sleep(poll_interval)
        elapsed += poll_interval

    print(f"  ❌ [{report_name}] Timeout after {max_wait}s")
    return None

def download_report(download_url, report_name):
    print(f"  📥 [{report_name}] Downloading...")
    req = Request(download_url)

    try:
        with urlopen(req, context=SSL_CONTEXT) as resp:
            compressed = resp.read()
            decompressed = gzip.decompress(compressed)
            data = json.loads(decompressed.decode())
            print(f"  ✅ [{report_name}] {len(data)} rows downloaded ({len(compressed):,} bytes compressed)")
            return data
    except Exception as e:
        print(f"  ❌ [{report_name}] Download error: {str(e)}")
        return None

def fetch_one_report(report_key, start_date, end_date):
    cfg = REPORT_TYPES[report_key]
    report_id = create_report(report_key, start_date, end_date)
    if not report_id:
        return None

    url = wait_for_report(report_id, cfg["name"])
    if not url:
        return None

    return download_report(url, cfg["name"])

# ============================================
# CAMPAIGN LIST via Ads API v1 Unified
# ============================================
def fetch_campaign_list():
    print(f"\n📋 [Campaign List] Fetching via Ads API v1 Unified...")

    body = {
        "stateFilter": {
            "include": ["ENABLED", "PAUSED", "ARCHIVED"]
        }
    }

    result, status = api_call(
        "POST", "/sp/campaigns/list",
        body=body,
        headers_extra={
            "Content-Type": "application/vnd.spCampaign.v3+json",
            "Accept": "application/vnd.spCampaign.v3+json"
        }
    )

    if result and "campaigns" in result:
        campaigns = result["campaigns"]
        print(f"  ✅ {len(campaigns)} campaigns fetched")
        return campaigns
    elif isinstance(result, list):
        print(f"  ✅ {len(result)} campaigns fetched")
        return result
    else:
        print(f"  ❌ Failed. Response: {str(result)[:300]}")
        return None

# ============================================
# AD GROUP LIST via Ads API v1 Unified
# ============================================
def fetch_adgroup_list():
    print(f"\n📋 [Ad Group List] Fetching...")

    body = {
        "stateFilter": {
            "include": ["ENABLED", "PAUSED", "ARCHIVED"]
        }
    }

    result, status = api_call(
        "POST", "/sp/adGroups/list",
        body=body,
        headers_extra={
            "Content-Type": "application/vnd.spAdGroup.v3+json",
            "Accept": "application/vnd.spAdGroup.v3+json"
        }
    )

    if result and "adGroups" in result:
        adgroups = result["adGroups"]
        print(f"  ✅ {len(adgroups)} ad groups fetched")
        return adgroups
    elif isinstance(result, list):
        print(f"  ✅ {len(result)} ad groups fetched")
        return result
    else:
        print(f"  ❌ Failed. Response: {str(result)[:300]}")
        return None

# ============================================
# KEYWORD LIST via Ads API v1 Unified
# ============================================
def fetch_keyword_list():
    print(f"\n📋 [Keyword List] Fetching...")

    body = {
        "stateFilter": {
            "include": ["ENABLED", "PAUSED", "ARCHIVED"]
        }
    }

    result, status = api_call(
        "POST", "/sp/keywords/list",
        body=body,
        headers_extra={
            "Content-Type": "application/vnd.spKeyword.v3+json",
            "Accept": "application/vnd.spKeyword.v3+json"
        }
    )

    if result and "keywords" in result:
        keywords = result["keywords"]
        print(f"  ✅ {len(keywords)} keywords fetched")
        return keywords
    elif isinstance(result, list):
        print(f"  ✅ {len(result)} keywords fetched")
        return result
    else:
        print(f"  ❌ Failed. Response: {str(result)[:300]}")
        return None

# ============================================
# NEGATIVE KEYWORD LIST
# ============================================
def fetch_negative_keyword_list():
    print(f"\n📋 [Negative Keywords] Fetching...")

    body = {
        "stateFilter": {
            "include": ["ENABLED", "PAUSED", "ARCHIVED"]
        }
    }

    result, status = api_call(
        "POST", "/sp/negativeKeywords/list",
        body=body,
        headers_extra={
            "Content-Type": "application/vnd.spNegativeKeyword.v3+json",
            "Accept": "application/vnd.spNegativeKeyword.v3+json"
        }
    )

    if result and "negativeKeywords" in result:
        nkws = result["negativeKeywords"]
        print(f"  ✅ {len(nkws)} negative keywords fetched")
        return nkws
    elif isinstance(result, list):
        print(f"  ✅ {len(result)} negative keywords fetched")
        return result
    else:
        print(f"  ❌ Failed. Response: {str(result)[:300]}")
        return None

# ============================================
# PRODUCT ADS LIST
# ============================================
def fetch_product_ads_list():
    print(f"\n📋 [Product Ads] Fetching...")

    body = {
        "stateFilter": {
            "include": ["ENABLED", "PAUSED", "ARCHIVED"]
        }
    }

    result, status = api_call(
        "POST", "/sp/productAds/list",
        body=body,
        headers_extra={
            "Content-Type": "application/vnd.spProductAd.v3+json",
            "Accept": "application/vnd.spProductAd.v3+json"
        }
    )

    if result and "productAds" in result:
        ads = result["productAds"]
        print(f"  ✅ {len(ads)} product ads fetched")
        return ads
    elif isinstance(result, list):
        print(f"  ✅ {len(result)} product ads fetched")
        return result
    else:
        print(f"  ❌ Failed. Response: {str(result)[:300]}")
        return None

# ============================================
# SAVE DATA
# ============================================
def save_json(data, filename):
    os.makedirs(REPORT_DIR, exist_ok=True)
    filepath = os.path.join(REPORT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    size_kb = os.path.getsize(filepath) / 1024
    print(f"  💾 Saved: {filepath} ({size_kb:.1f} KB)")
    return filepath

# ============================================
# MAIN EXECUTION
# ============================================
def main():
    parser = argparse.ArgumentParser(description="GoAmrita SP Ads Complete Data Import")
    parser.add_argument("--days", type=int, default=7, help="Number of days to import (default: 7)")
    parser.add_argument("--reports", type=str, default="all",
                        help="Comma-separated report types: campaigns_daily,campaigns_summary,searchterm,targeting,advertisedproduct,purchasedproduct OR 'all'")
    args = parser.parse_args()

    end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")

    print("=" * 80)
    print(f"🚀 GoAmrita — Sponsored Products Complete Data Import v1.0")
    print(f"📅 Period: {start_date} to {end_date} ({args.days} days)")
    print(f"🏪 Account: Made in Heavens | 🇮🇳 amazon.in")
    print(f"⏰ Started: {datetime.now().strftime('%d %B %Y, %I:%M %p IST')}")
    print("=" * 80)

    # Determine which reports to run
    if args.reports == "all":
        report_keys = list(REPORT_TYPES.keys())
    else:
        report_keys = [r.strip() for r in args.reports.split(",")]
        invalid = [r for r in report_keys if r not in REPORT_TYPES]
        if invalid:
            print(f"❌ Invalid report types: {invalid}")
            print(f"   Valid: {list(REPORT_TYPES.keys())}")
            sys.exit(1)

    results = {}
    saved_files = []

    # ── PART 1: Reporting API (async reports with metrics) ──
    print(f"\n{'='*80}")
    print(f"📊 PART 1: Performance Reports ({len(report_keys)} reports)")
    print(f"{'='*80}")

    # STEP 1: Create ALL reports first (parallel processing on Amazon side)
    pending = {}
    for key in report_keys:
        report_id = create_report(key, start_date, end_date)
        if report_id:
            pending[key] = {"id": report_id, "name": REPORT_TYPES[key]["name"]}

    if pending:
        # STEP 2: Poll ALL pending reports in round-robin (with retry)
        max_wait_per_round = 900  # 15 min per round
        max_retries = 2  # total 2 rounds = 30 min max
        poll_interval = 15
        completed = {}

        for attempt in range(1, max_retries + 1):
            still_pending = [k for k in pending if k not in completed]
            if not still_pending:
                break

            if attempt == 1:
                print(f"\n  ⏳ Waiting for {len(pending)} reports (polling all in parallel)...")
            else:
                print(f"\n  🔄 Retry round {attempt}: {len(still_pending)} reports still pending...")

            elapsed = 0
            while elapsed < max_wait_per_round and len(completed) < len(pending):
                for key in still_pending:
                    if key in completed:
                        continue
                    info = pending[key]
                    result, status = api_call(
                        "GET", f"/reporting/reports/{info['id']}",
                        headers_extra={"Accept": "application/vnd.createasyncreportrequest.v3+json"}
                    )
                    if not result:
                        continue
                    report_status = result.get("status", "UNKNOWN")
                    if report_status == "COMPLETED" and result.get("url"):
                        total_elapsed = (attempt - 1) * max_wait_per_round + elapsed
                        print(f"  ✅ [{info['name']}] Ready! ({total_elapsed}s)")
                        completed[key] = result["url"]
                    elif report_status == "FAILURE":
                        print(f"  ❌ [{info['name']}] FAILED")
                        completed[key] = None

                if len(completed) < len(pending):
                    remaining = [pending[k]["name"] for k in pending if k not in completed]
                    if elapsed > 0 and elapsed % 60 == 0:
                        total_elapsed = (attempt - 1) * max_wait_per_round + elapsed
                        print(f"     Still waiting ({total_elapsed}s): {', '.join(remaining)}")
                    time.sleep(poll_interval)
                    elapsed += poll_interval

        # STEP 3: Download completed, mark timed-out as failed
        total_wait = max_retries * max_wait_per_round
        for key, info in pending.items():
            if key in completed and completed[key]:
                data = download_report(completed[key], info["name"])
                if data is not None:
                    filepath = save_json(data, REPORT_TYPES[key]["filename"])
                    results[key] = {"rows": len(data), "file": filepath, "status": "✅"}
                    saved_files.append(filepath)
                else:
                    results[key] = {"rows": 0, "file": None, "status": "❌"}
            else:
                if key not in completed:
                    print(f"  ❌ [{info['name']}] Timeout after {total_wait}s (all retries exhausted)")
                results[key] = {"rows": 0, "file": None, "status": "❌"}

    # Mark any reports that couldn't even be created
    for key in report_keys:
        if key not in results:
            results[key] = {"rows": 0, "file": None, "status": "❌"}

    # ── PART 2: Structure Data (Ads API v1 Unified — lists) ──
    print(f"\n{'='*80}")
    print(f"📋 PART 2: Account Structure (Campaigns, Ad Groups, Keywords, Ads)")
    print(f"{'='*80}")

    structure_fetchers = [
        ("campaign_list", "sp_campaign_list.json", fetch_campaign_list),
        ("adgroup_list", "sp_adgroup_list.json", fetch_adgroup_list),
        ("keyword_list", "sp_keyword_list.json", fetch_keyword_list),
        ("negative_keyword_list", "sp_negative_keyword_list.json", fetch_negative_keyword_list),
        ("product_ads_list", "sp_product_ads_list.json", fetch_product_ads_list),
    ]

    for name, filename, fetcher in structure_fetchers:
        data = fetcher()
        if data is not None:
            filepath = save_json(data, filename)
            results[name] = {"rows": len(data), "file": filepath, "status": "✅"}
            saved_files.append(filepath)
        else:
            results[name] = {"rows": 0, "file": None, "status": "❌"}

    # ── SUMMARY ──
    print(f"\n{'='*80}")
    print(f"📊 IMPORT SUMMARY")
    print(f"{'='*80}")
    print(f"{'Report':<35} {'Status':<5} {'Rows':<10} {'File'}")
    print(f"{'-'*80}")

    total_rows = 0
    success_count = 0
    for name, info in results.items():
        display_name = REPORT_TYPES.get(name, {}).get("name", name.replace("_", " ").title())
        fname = os.path.basename(info["file"]) if info["file"] else "—"
        print(f"{display_name:<35} {info['status']:<5} {info['rows']:<10} {fname}")
        total_rows += info["rows"]
        if info["status"] == "✅":
            success_count += 1

    total_count = len(results)
    print(f"{'-'*80}")
    print(f"{'TOTAL':<35} {success_count}/{total_count}  {total_rows:<10} rows")
    print(f"\n📁 All files saved in: {REPORT_DIR}")
    print(f"⏰ Completed: {datetime.now().strftime('%d %B %Y, %I:%M %p IST')}")

    # Save import metadata
    metadata = {
        "import_date": datetime.now().isoformat(),
        "period": {"start": start_date, "end": end_date, "days": args.days},
        "account": CREDS.get("account_name", "Made in Heavens"),
        "marketplace": CREDS.get("marketplace", "amazon.in"),
        "results": {k: {"rows": v["rows"], "status": v["status"]} for k, v in results.items()},
        "total_rows": total_rows,
        "success_count": success_count,
        "total_reports": total_count,
        "version": "1.0"
    }
    save_json(metadata, "_import_metadata.json")

    if success_count == total_count:
        print(f"\n🎉 All {total_count} data sources imported successfully!")
    else:
        print(f"\n⚠️ {success_count}/{total_count} succeeded. Check errors above.")

    return 0 if success_count == total_count else 1

if __name__ == "__main__":
    sys.exit(main())
