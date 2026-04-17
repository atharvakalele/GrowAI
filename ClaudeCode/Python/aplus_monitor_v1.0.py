#!/usr/bin/env python3
"""
AutoGrow AI — A+ Content Monitor v1.0 (G15/G19)
==================================================
Checks A+ content status for all ASINs.
Identifies: which products have A+, which don't, content status.
Tracks impact: conversion rate before/after A+ added.
Alerts: top sellers without A+ = biggest opportunity.

API: A+ Content Management API v2020-11-01

Usage:
    python aplus_monitor_v1.0.py
    python aplus_monitor_v1.0.py --check-all   (check every ASIN)
"""

import json
import os
import sys
import ssl
import time
import argparse
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote
from urllib.error import HTTPError

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
SP_CREDS = json.load(open(os.path.join(PROJECT_DIR, "sp_api_credentials.json")))["sp_api_credentials"]

REPORT_BASE = os.path.join(SCRIPT_DIR, "..", "Report")
report_folders = [f for f in os.listdir(REPORT_BASE) if os.path.isdir(os.path.join(REPORT_BASE, f))]
report_folders.sort(key=lambda x: os.path.getmtime(os.path.join(REPORT_BASE, x)), reverse=True)
LATEST_REPORT = report_folders[0] if report_folders else datetime.now().strftime("%d %B %Y")
JSON_DIR = os.path.join(REPORT_BASE, LATEST_REPORT, "Json")

MARKETPLACE_ID = "A21TJRUUN4KGV"
SP_ENDPOINT = "https://sellingpartnerapi-eu.amazon.com"
OUTPUT_FILE = os.path.join(JSON_DIR, "aplus_status.json")

SSL_CONTEXT = None
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

_token = None
_expiry = None

def get_token():
    global _token, _expiry
    if _token and _expiry and datetime.now() < _expiry:
        return _token
    data = urlencode({'grant_type': 'refresh_token', 'refresh_token': SP_CREDS['refresh_token'],
        'client_id': SP_CREDS['lwa_client_id'], 'client_secret': SP_CREDS['lwa_client_secret']}).encode()
    req = Request(SP_CREDS['token_url'], data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    result = json.loads(urlopen(req, context=SSL_CONTEXT).read().decode())
    _token = result['access_token']
    _expiry = datetime.now() + timedelta(seconds=result['expires_in'] - 60)
    return _token


def check_aplus_for_asin(asin):
    """Check if ASIN has A+ content"""
    token = get_token()
    url = f"{SP_ENDPOINT}/aplus/2020-11-01/contentDocuments?marketplaceId={MARKETPLACE_ID}&asin={asin}"
    headers = {
        'x-amz-access-token': token,
        'x-amz-date': datetime.utcnow().strftime('%Y%m%dT%H%M%SZ'),
        'Host': 'sellingpartnerapi-eu.amazon.com',
    }
    req = Request(url, headers=headers)
    try:
        resp = urlopen(req, context=SSL_CONTEXT)
        result = json.loads(resp.read().decode())
        records = result.get('contentMetadataRecords', [])

        statuses = {}
        for r in records:
            meta = r.get('contentMetadata', r)
            status = meta.get('status', 'UNKNOWN')
            statuses[status] = statuses.get(status, 0) + 1

        has_aplus = len(records) > 0
        approved = statuses.get('APPROVED', 0)
        pending = statuses.get('SUBMITTED', 0) + statuses.get('PENDING', 0)
        draft = statuses.get('DRAFT', 0)

        return {
            'has_aplus': has_aplus,
            'total_docs': len(records),
            'approved': approved,
            'pending': pending,
            'draft': draft,
            'statuses': statuses,
        }
    except HTTPError as e:
        return {'has_aplus': False, 'error': e.read().decode()[:100], 'total_docs': 0}


def get_all_asins_with_sales():
    """Get ASINs sorted by sales"""
    prod_file = os.path.join(JSON_DIR, "sp_advertisedproduct_daily.json")
    ads_file = os.path.join(JSON_DIR, "sp_product_ads_list.json")

    asins = {}
    if os.path.exists(prod_file):
        with open(prod_file, encoding='utf-8') as f:
            for r in json.load(f):
                a = r.get('advertisedAsin', '')
                if a not in asins:
                    asins[a] = {'sku': r.get('advertisedSku', ''), 'sales': 0, 'orders': 0,
                                'clicks': 0, 'impressions': 0, 'cost': 0}
                asins[a]['sales'] += float(r.get('sales7d', 0))
                asins[a]['orders'] += int(r.get('purchases7d', 0))
                asins[a]['clicks'] += int(r.get('clicks', 0))
                asins[a]['impressions'] += int(r.get('impressions', 0))
                asins[a]['cost'] += float(r.get('cost', 0))

    # Add SKU mapping
    if os.path.exists(ads_file):
        with open(ads_file, encoding='utf-8') as f:
            for a in json.load(f):
                asin = a.get('asin', '')
                if asin in asins and not asins[asin]['sku']:
                    asins[asin]['sku'] = a.get('sku', '')

    # Sort by sales desc
    sorted_asins = sorted(asins.items(), key=lambda x: x[1]['sales'], reverse=True)
    return sorted_asins


def main():
    parser = argparse.ArgumentParser(description='A+ Content Monitor')
    parser.add_argument('--check-all', action='store_true', help='Check all ASINs (slow)')
    args = parser.parse_args()

    print("=" * 55)
    print("  AutoGrow AI — A+ Content Monitor v1.0")
    print(f"  {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print("=" * 55)

    all_asins = get_all_asins_with_sales()
    print(f"\n  Total ASINs with ad data: {len(all_asins)}")

    # Check unique ASINs (avoid duplicates for same brand A+ docs)
    to_check = all_asins if args.check_all else all_asins[:50]
    print(f"  Checking: {len(to_check)} ASINs")

    results = []
    with_aplus = 0
    without_aplus = []
    errors = 0

    for i, (asin, data) in enumerate(to_check):
        status = check_aplus_for_asin(asin)
        cvr = (data['orders'] / data['clicks'] * 100) if data['clicks'] > 0 else 0

        entry = {
            'asin': asin,
            'sku': data['sku'][:25],
            'has_aplus': status['has_aplus'],
            'aplus_docs': status.get('total_docs', 0),
            'approved': status.get('approved', 0),
            'pending': status.get('pending', 0),
            'weekly_sales': round(data['sales']),
            'weekly_orders': data['orders'],
            'cvr': round(cvr, 2),
            'clicks': data['clicks'],
            'impressions': data['impressions'],
            'ad_spend': round(data['cost']),
        }

        if status.get('error'):
            entry['error'] = status['error']
            errors += 1
        elif status['has_aplus']:
            with_aplus += 1
        else:
            without_aplus.append(entry)

        results.append(entry)

        if (i + 1) % 20 == 0:
            print(f"    Checked {i+1}/{len(to_check)}...")
        time.sleep(0.5)

    # Sort without A+ by sales (biggest opportunity first)
    without_aplus.sort(key=lambda x: x['weekly_sales'], reverse=True)

    # Display
    print(f"\n  {'='*60}")
    print(f"  A+ CONTENT STATUS")
    print(f"  {'='*60}")
    print(f"  With A+ Content:    {with_aplus}")
    print(f"  Without A+ Content: {len(without_aplus)}")
    print(f"  Errors:             {errors}")

    if without_aplus:
        print(f"\n  {'='*60}")
        print(f"  OPPORTUNITY: Products WITHOUT A+ Content")
        print(f"  (Adding A+ typically improves conversion 5-15%)")
        print(f"  {'='*60}")
        print(f"  {'ASIN':<14} {'SKU':<25} {'Sales':>8} {'Orders':>7} {'CVR':>6} {'Priority'}")
        print(f"  {'-'*70}")

        for item in without_aplus[:20]:
            priority = "HIGH" if item['weekly_sales'] > 1000 else "MEDIUM" if item['weekly_sales'] > 200 else "LOW"
            print(f"  {item['asin']:<14} {item['sku']:<25} Rs.{item['weekly_sales']:>5} {item['weekly_orders']:>7} {item['cvr']:>5.1f}% {priority}")

    # Summary insight
    total_sales_without = sum(x['weekly_sales'] for x in without_aplus)
    potential_gain = total_sales_without * 0.10  # 10% conversion improvement estimate
    print(f"\n  Potential revenue gain from adding A+: Rs.{potential_gain:,.0f}/week")
    print(f"  (Based on 10% conversion improvement estimate)")

    # Save
    os.makedirs(JSON_DIR, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_checked': len(results),
            'with_aplus': with_aplus,
            'without_aplus': len(without_aplus),
            'without_aplus_details': without_aplus,
            'potential_weekly_gain': round(potential_gain),
            'results': results,
        }, f, indent=2, ensure_ascii=False)
    print(f"\n  Saved: {OUTPUT_FILE}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
