#!/usr/bin/env python3
"""
GoAmrita - Auto Campaign Creator v2.0 (G09)
=============================================
Full pipeline: Find product > Keywords > Smart Filter > Create Campaign

2 MODES:
  Mode 1: --mode profit    Top profit ASINs not in any campaign (every 15 days)
  Mode 2: --mode newlisting New listings last N days not in any campaign (daily)

CAMPAIGN NAMES:
  Mode 1: {SKU}_{Date}_AI_BidDown5pctAdSpend25pctProfit
  Mode 2: {SKU}_AI_AutoLaunch_New_Listing

BID FORMULA: 25% of True Profit = daily budget, 5% of budget = bid

PIPELINE:
  1. Find candidates (mode based)
  2. Check NOT in existing campaigns
  3. Fetch Amazon keyword suggestions
  4. Fetch product listing (title + bullets + description)
  5. Smart filter: keywords vs listing content
  6. Match type: 1-2 words=PHRASE, 3+=EXACT
  7. Create: Campaign > Ad Group > Product Ad > Keywords
  8. Save Product Opportunities (irrelevant/competitor keywords)

Usage:
    python auto_campaign_creator_v2.0.py --mode newlisting --days 8
    python auto_campaign_creator_v2.0.py --mode newlisting --days 8 --dry-run
    python auto_campaign_creator_v2.0.py --mode profit --top 3
    python auto_campaign_creator_v2.0.py --mode profit --top 1 --dry-run
    python auto_campaign_creator_v2.0.py --asin B0DFM7TY5T
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

# ============================================
# CONFIG
# ============================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))

REPORT_BASE = os.path.join(SCRIPT_DIR, "..", "Report")
report_folders = [f for f in os.listdir(REPORT_BASE) if os.path.isdir(os.path.join(REPORT_BASE, f))]
report_folders.sort(key=lambda x: os.path.getmtime(os.path.join(REPORT_BASE, x)), reverse=True)
LATEST_REPORT = report_folders[0] if report_folders else datetime.now().strftime("%d %B %Y")
JSON_DIR = os.path.join(REPORT_BASE, LATEST_REPORT, "Json")

ADS_CREDS = json.load(open(os.path.join(PROJECT_DIR, "api_credentials.json")))
SP_CREDS = json.load(open(os.path.join(PROJECT_DIR, "sp_api_credentials.json")))["sp_api_credentials"]

try:
    PROFIT_CONFIG = json.load(open(os.path.join(PROJECT_DIR, "config_true_profit.json")))
except:
    PROFIT_CONFIG = {"account_default": {"product_cost": 85}, "amazon_fees": {"referral_fee_pct": 3, "closing_fee": 5}, "shipping": {"default": 95}}

MARKETPLACE_ID = "A21TJRUUN4KGV"
OUR_SELLER_ID = "A2AC2AS9R9CBEA"
OPP_FILE = os.path.join(JSON_DIR, "product_opportunities.json")

SSL_CONTEXT = None
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

# Known ineligible ASINs (adult flag, suppressed, etc.)
INELIGIBLE_ASINS = ['B0FK4PK4HK']  # LiBiDEXX30 — adult false flag

# Wrong product / competitor markers for keyword filtering
WRONG_PRODUCT_MARKERS = [
    'black salt', 'rock salt', 'flaky', 'flake', 'pink salt', 'himalayan salt',
    'table salt', 'iodized', 'sendha', 'kala namak',
    'viagra', 'proman', 'titan', 'patanjali', 'himalaya', 'dabur',
    'baidyanath', 'zandu', 'tata'
]

# ============================================
# TOKEN MANAGEMENT
# ============================================
_ads_token = None
_ads_expiry = None
_sp_token = None
_sp_expiry = None

def get_ads_token():
    global _ads_token, _ads_expiry
    if _ads_token and _ads_expiry and datetime.now() < _ads_expiry:
        return _ads_token
    data = urlencode({'grant_type': 'refresh_token', 'refresh_token': ADS_CREDS['refresh_token'],
        'client_id': ADS_CREDS['client_id'], 'client_secret': ADS_CREDS['client_secret']}).encode()
    req = Request(ADS_CREDS['token_url'], data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    result = json.loads(urlopen(req, context=SSL_CONTEXT).read().decode())
    _ads_token = result['access_token']
    _ads_expiry = datetime.now() + timedelta(seconds=result['expires_in'] - 60)
    return _ads_token

def get_sp_token():
    global _sp_token, _sp_expiry
    if _sp_token and _sp_expiry and datetime.now() < _sp_expiry:
        return _sp_token
    data = urlencode({'grant_type': 'refresh_token', 'refresh_token': SP_CREDS['refresh_token'],
        'client_id': SP_CREDS['lwa_client_id'], 'client_secret': SP_CREDS['lwa_client_secret']}).encode()
    req = Request(SP_CREDS['token_url'], data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    result = json.loads(urlopen(req, context=SSL_CONTEXT).read().decode())
    _sp_token = result['access_token']
    _sp_expiry = datetime.now() + timedelta(seconds=result['expires_in'] - 60)
    return _sp_token

# ============================================
# API HELPERS
# ============================================
def ads_api(method, path, body, ct):
    token = get_ads_token()
    url = ADS_CREDS['api_endpoint'] + path
    headers = {'Authorization': 'Bearer ' + token, 'Amazon-Advertising-API-ClientId': ADS_CREDS['client_id'],
        'Amazon-Advertising-API-Scope': str(ADS_CREDS['profile_id']), 'Content-Type': ct, 'Accept': ct}
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method=method)
    try:
        resp = urlopen(req, context=SSL_CONTEXT)
        return json.loads(resp.read().decode()), resp.status
    except HTTPError as e:
        return {'error': e.read().decode()[:500]}, e.code

def sp_api_get(path):
    token = get_sp_token()
    url = SP_CREDS['endpoint'] + path
    headers = {'x-amz-access-token': token,
        'x-amz-date': datetime.utcnow().strftime('%Y%m%dT%H%M%SZ'),
        'Host': 'sellingpartnerapi-eu.amazon.com'}
    req = Request(url, headers=headers)
    try:
        resp = urlopen(req, context=SSL_CONTEXT)
        return json.loads(resp.read().decode())
    except HTTPError as e:
        return {'error': e.read().decode()[:500]}

# ============================================
# GET ALL EXISTING CAMPAIGN ASINs
# ============================================
def get_existing_campaign_asins(include_paused=False):
    """
    Get ASINs already in campaigns.
    include_paused=False (DEFAULT): Only ENABLED ads count → paused ASINs are candidates
    include_paused=True: Both ENABLED+PAUSED count → paused ASINs are NOT candidates

    DEFAULT = True (don't re-run paused) to avoid loop:
      Feature X pauses campaign (loss) → This feature creates new → Feature X pauses again → LOOP!
    Set include_paused=False ONLY if user explicitly enables re-run on paused in config.
    """
    states = ['ENABLED', 'PAUSED'] if include_paused else ['ENABLED']
    r, _ = ads_api('POST', '/sp/productAds/list', {
        'stateFilter': {'include': states}
    }, 'application/vnd.spProductAd.v3+json')

    asins = set()
    paused_only_asins = set()
    enabled_asins = set()

    for ad in r.get('productAds', []):
        asin = ad.get('asin', '')
        if not asin:
            continue
        asins.add(asin)
        if ad.get('state') == 'ENABLED':
            enabled_asins.add(asin)
        elif ad.get('state') == 'PAUSED':
            paused_only_asins.add(asin)

    # Paused-only = has paused ads but NO enabled ads
    paused_only_asins = paused_only_asins - enabled_asins

    if include_paused:
        return asins  # ALL (enabled + paused) = skip everything
    else:
        return enabled_asins  # Only enabled = paused are candidates

# ============================================
# MODE 1: TOP PROFIT CANDIDATES
# ============================================
def find_profit_candidates(top_n=5, include_paused_skip=True):
    """
    include_paused_skip=True (DEFAULT): Skip paused ASINs (avoid loop)
    include_paused_skip=False: Include paused ASINs as candidates (user enabled in config)
    """
    existing = get_existing_campaign_asins(include_paused=include_paused_skip)
    print(f"  Existing campaign ASINs (skipping): {len(existing)}")

    # Also get paused-only ASINs for tracking
    all_ads, _ = ads_api('POST', '/sp/productAds/list', {
        'stateFilter': {'include': ['PAUSED']}
    }, 'application/vnd.spProductAd.v3+json')
    paused_asins = set(a.get('asin','') for a in all_ads.get('productAds', []))

    profit_file = os.path.join(JSON_DIR, "true_profit_per_asin.json")
    pricing_file = os.path.join(JSON_DIR, "sp_pricing_data.json")

    with open(profit_file) as f:
        profits = json.load(f)
    with open(pricing_file) as f:
        prices = json.load(f)

    candidates = []
    for p in profits:
        asin = p.get('asin', '')
        if asin in existing or asin in INELIGIBLE_ASINS:
            continue
        pr = prices.get(asin, {})
        if p.get('true_profit', 0) > 0 and pr.get('buy_box_winner', False) and pr.get('your_price', 0) > 100:
            was_paused = asin in paused_asins
            candidates.append({
                'asin': asin,
                'sku': p.get('sku', 'UNKNOWN'),
                'price': pr.get('your_price', 0),
                'true_profit': p.get('true_profit', 0),
                'mode': 'profit',
                'was_paused': was_paused,
            })

    candidates.sort(key=lambda x: x['true_profit'], reverse=True)
    return candidates[:top_n]

# ============================================
# MODE 2: NEW LISTING CANDIDATES
# ============================================
def find_newlisting_candidates(days=8):
    existing = get_existing_campaign_asins()
    print(f"  Existing campaign ASINs: {len(existing)}")

    # Fetch all our ASINs from product ads list
    ads_file = os.path.join(JSON_DIR, "sp_product_ads_list.json")
    with open(ads_file) as f:
        ads = json.load(f)

    all_asins = list(set(a['asin'] for a in ads if a.get('asin')))
    # Also include ASINs NOT in ads (truly new)
    pricing_file = os.path.join(JSON_DIR, "sp_pricing_data.json")
    if os.path.exists(pricing_file):
        with open(pricing_file) as f:
            prices = json.load(f)
        all_asins = list(set(all_asins + list(prices.keys())))

    print(f"  Total ASINs to check: {len(all_asins)}")

    # Fetch listing dates from Catalog API (product_site_launch_date in attributes)
    cutoff = datetime.now() - timedelta(days=days)
    cutoff_str = cutoff.strftime('%Y-%m-%d')
    print(f"  Looking for listings after: {cutoff_str}")

    # Batch fetch catalog data (20 per batch)
    new_asins = []
    batches = [all_asins[i:i+20] for i in range(0, len(all_asins), 20)]

    for i, batch in enumerate(batches):
        identifiers = ','.join(batch)
        path = f"/catalog/2022-04-01/items?identifiers={identifiers}&identifiersType=ASIN&marketplaceIds={MARKETPLACE_ID}&includedData=attributes,summaries"
        result = sp_api_get(path)

        for item in result.get('items', []):
            asin = item.get('asin', '')
            if asin in existing or asin in INELIGIBLE_ASINS:
                continue

            attrs = item.get('attributes', {})
            launch_date_list = attrs.get('product_site_launch_date', [])
            if launch_date_list:
                ld = launch_date_list[0] if isinstance(launch_date_list, list) else launch_date_list
                date_val = ld.get('value', '')
                if date_val:
                    launch_date = date_val[:10]  # "2026-04-10T..." -> "2026-04-10"
                    if launch_date >= cutoff_str:
                        summaries = item.get('summaries', [])
                        item_name = ''
                        for s in summaries:
                            if s.get('marketplaceId') == MARKETPLACE_ID:
                                item_name = s.get('itemName', '')
                                break
                        new_asins.append({
                            'asin': asin,
                            'title': item_name[:50],
                            'launch_date': launch_date,
                        })

        if i < len(batches) - 1:
            time.sleep(0.5)  # Rate: 2 req/sec

    print(f"  New listings found (last {days} days): {len(new_asins)}")

    # Get SKU + profit for these ASINs
    profit_file = os.path.join(JSON_DIR, "true_profit_per_asin.json")
    pricing_file = os.path.join(JSON_DIR, "sp_pricing_data.json")
    profit_map = {}
    price_map = {}

    if os.path.exists(profit_file):
        with open(profit_file) as f:
            for p in json.load(f):
                profit_map[p['asin']] = p
    if os.path.exists(pricing_file):
        with open(pricing_file) as f:
            price_map = json.load(f)

    # Get SKU mapping
    sku_map = {a['asin']: a['sku'] for a in ads if a.get('asin')}

    candidates = []
    for na in new_asins:
        asin = na['asin']
        pr = price_map.get(asin, {})
        p = profit_map.get(asin, {})

        sku = sku_map.get(asin, na['title'][:30].replace(' ', '_'))
        price = pr.get('your_price', 0)
        true_profit = p.get('true_profit', 0)

        # If no profit data, calculate quick estimate
        if true_profit == 0 and price > 0:
            cost = PROFIT_CONFIG['account_default']['product_cost']
            ref_fee = PROFIT_CONFIG['amazon_fees'].get('referral_fee_pct', 3) / 100 * price
            closing = PROFIT_CONFIG['amazon_fees'].get('closing_fee', 5)
            shipping = PROFIT_CONFIG['shipping']['default']
            true_profit = price - cost - ref_fee - closing - shipping

        if true_profit > 0 and price > 100:
            candidates.append({
                'asin': asin,
                'sku': sku,
                'price': price,
                'true_profit': true_profit,
                'launch_date': na['launch_date'],
                'title': na['title'],
                'mode': 'newlisting'
            })

    candidates.sort(key=lambda x: x['launch_date'], reverse=True)  # newest first
    return candidates

# ============================================
# FETCH KEYWORD SUGGESTIONS
# ============================================
def fetch_keywords(asin):
    r, _ = ads_api('POST', '/sp/targets/keywords/recommendations', {
        'recommendationType': 'KEYWORDS_FOR_ASINS',
        'asins': [asin],
        'maxRecommendations': 50,
        'sortDimension': 'CLICKS',
        'locale': 'en_IN'
    }, 'application/vnd.spkeywordsrecommendation.v5+json')
    return r.get('keywordTargetList', [])

# ============================================
# FETCH LISTING CONTENT
# ============================================
def fetch_listing(sku):
    encoded_sku = quote(sku)
    path = f"/listings/2021-08-01/items/{OUR_SELLER_ID}/{encoded_sku}?marketplaceIds={MARKETPLACE_ID}&includedData=attributes"
    result = sp_api_get(path)

    if 'error' in result:
        return ""

    attrs = result.get('attributes', {})
    text = ""
    for key in ['item_name', 'bullet_point', 'product_description']:
        val = attrs.get(key, [])
        if isinstance(val, list):
            for item in val:
                if isinstance(item, dict):
                    text += item.get('value', '') + " "
    return text

# ============================================
# SMART KEYWORD FILTER
# ============================================
def smart_filter(kw_raw, listing_text):
    listing_lower = listing_text.lower()
    relevant = []
    opportunities = []

    seen = set()
    for kw_obj in kw_raw:
        kw = kw_obj.get('keyword', kw_obj.get('value', '')).strip()
        kw_lower = kw.lower()

        if not kw or kw_lower in seen:
            continue
        seen.add(kw_lower)

        # Competitor / wrong product type
        if any(m in kw_lower for m in WRONG_PRODUCT_MARKERS):
            opportunities.append({'keyword': kw, 'reason': 'competitor_or_wrong_product'})
            continue

        # Check keyword relevance to listing
        kw_words = [w for w in kw_lower.split() if len(w) > 2]
        if not kw_words:
            relevant.append(kw)
            continue

        matches = sum(1 for w in kw_words if w in listing_lower)
        match_pct = matches / len(kw_words) * 100

        if match_pct >= 40:
            relevant.append(kw)
        else:
            opportunities.append({'keyword': kw, 'reason': 'not_in_listing'})

    return relevant, opportunities

# ============================================
# MATCH TYPE RULE
# ============================================
def apply_match_type(keywords):
    return [{'keyword': kw, 'matchType': 'PHRASE' if len(kw.split()) <= 2 else 'EXACT'} for kw in keywords]

# ============================================
# BID FORMULA
# ============================================
def calc_bid(true_profit):
    budget = max(round(true_profit * 0.25), 50)  # min Rs.50/day
    bid = max(round(budget * 0.05, 2), 2.0)  # min Rs.2 bid
    return budget, bid

# ============================================
# CREATE CAMPAIGN ON AMAZON
# ============================================
def create_on_amazon(asin, sku, name, budget, bid, keywords_typed):
    today = datetime.now().strftime('%Y-%m-%d')
    result = {'campaign_id': None, 'adgroup_id': None, 'ad_ok': False, 'kw_count': 0, 'errors': []}

    # Campaign
    r1, _ = ads_api('POST', '/sp/campaigns', {'campaigns': [{
        'name': name, 'state': 'ENABLED', 'targetingType': 'MANUAL',
        'dynamicBidding': {'strategy': 'LEGACY_FOR_SALES', 'placementBidding': []},
        'budget': {'budgetType': 'DAILY', 'budget': float(budget)}, 'startDate': today,
    }]}, 'application/vnd.spCampaign.v3+json')

    s1 = r1.get('campaigns', {}).get('success', [])
    if not s1:
        result['errors'].append(f"Campaign: {json.dumps(r1)[:200]}")
        return result
    result['campaign_id'] = str(s1[0].get('campaignId', ''))
    time.sleep(1)

    # Ad Group
    r2, _ = ads_api('POST', '/sp/adGroups', {'adGroups': [{
        'campaignId': result['campaign_id'], 'name': f"AG_{sku[:25]}_KW",
        'state': 'ENABLED', 'defaultBid': bid
    }]}, 'application/vnd.spAdGroup.v3+json')

    s2 = r2.get('adGroups', {}).get('success', [])
    if not s2:
        result['errors'].append(f"AdGroup: {json.dumps(r2)[:200]}")
        return result
    result['adgroup_id'] = str(s2[0].get('adGroupId', ''))
    time.sleep(1)

    # Product Ad (with SKU!)
    r3, _ = ads_api('POST', '/sp/productAds', {'productAds': [{
        'campaignId': result['campaign_id'], 'adGroupId': result['adgroup_id'],
        'asin': asin, 'sku': sku, 'state': 'ENABLED'
    }]}, 'application/vnd.spProductAd.v3+json')

    ad_s = r3.get('productAds', {}).get('success', [])
    ad_e = r3.get('productAds', {}).get('error', [])
    result['ad_ok'] = bool(ad_s)
    if ad_e:
        err_msg = ad_e[0].get('errors', [{}])[0].get('errorValue', {})
        result['errors'].append(f"ProductAd: {json.dumps(err_msg)[:150]}")
        INELIGIBLE_ASINS.append(asin)
    time.sleep(1)

    # Keywords (max 100 per batch)
    kw_body = [{'campaignId': result['campaign_id'], 'adGroupId': result['adgroup_id'],
        'keywordText': k['keyword'], 'matchType': k['matchType'],
        'bid': bid, 'state': 'ENABLED'} for k in keywords_typed[:100]]

    r4, _ = ads_api('POST', '/sp/keywords', {'keywords': kw_body}, 'application/vnd.spKeyword.v3+json')
    result['kw_count'] = len(r4.get('keywords', {}).get('success', []))

    return result

# ============================================
# SAVE OPPORTUNITIES
# ============================================
def save_opps(asin, sku, opps):
    if not opps:
        return 0
    if os.path.exists(OPP_FILE):
        try:
            with open(OPP_FILE, encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            data = {'opportunities': [], 'total': 0}
    else:
        data = {'opportunities': [], 'total': 0}

    for o in opps:
        data['opportunities'].append({
            'keyword': o['keyword'], 'source_asin': asin, 'source_product': sku,
            'competitor_brand': '', 'product_type': o.get('reason', ''),
            'impression_rank': None, 'status': 'new',
            'discovered_date': datetime.now().strftime('%Y-%m-%d'),
            'action': 'Launch Your Product'
        })
    data['total'] = len(data['opportunities'])
    data['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    with open(OPP_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return len(opps)

# ============================================
# FULL PIPELINE
# ============================================
def run_pipeline(candidate, dry_run=False):
    asin = candidate['asin']
    sku = candidate['sku']
    profit = candidate['true_profit']
    price = candidate['price']
    mode = candidate.get('mode', 'profit')

    print(f"\n  {'='*55}")
    print(f"  ASIN: {asin} | SKU: {sku[:30]}")
    print(f"  Price: Rs.{price:.0f} | Profit: Rs.{profit:.0f} | Mode: {mode}")
    if candidate.get('launch_date'):
        print(f"  Launch Date: {candidate['launch_date']}")
    print(f"  {'='*55}")

    budget, bid = calc_bid(profit)
    print(f"  [1] Budget: Rs.{budget}/day | Bid: Rs.{bid}")

    print(f"  [2] Fetching keywords...")
    kw_raw = fetch_keywords(asin)
    print(f"      Amazon suggested: {len(kw_raw)}")
    if not kw_raw:
        print(f"      No keywords! SKIP.")
        return None

    print(f"  [3] Fetching listing content...")
    listing = fetch_listing(sku)
    print(f"      Listing: {len(listing)} chars")
    if not listing:
        listing = sku + " " + candidate.get('title', '')

    print(f"  [4] Smart filtering...")
    relevant, opps = smart_filter(kw_raw, listing)
    print(f"      Relevant: {len(relevant)} | Opportunity: {len(opps)}")
    if not relevant:
        print(f"      No relevant keywords! SKIP.")
        if opps:
            save_opps(asin, sku, opps)
        return None

    print(f"  [5] Match types...")
    kw_typed = apply_match_type(relevant)
    phrase = sum(1 for k in kw_typed if k['matchType'] == 'PHRASE')
    exact = len(kw_typed) - phrase
    print(f"      {phrase} PHRASE + {exact} EXACT")

    # Campaign name based on mode + paused status
    sku_clean = sku[:25].replace(' ', '')
    date_str = datetime.now().strftime('%d%b%Y')
    was_paused = candidate.get('was_paused', False)

    if mode == 'newlisting':
        name = f"{sku_clean}_AI_AutoLaunch_New_Listing"
    elif was_paused:
        name = f"{sku_clean}_{date_str}_AI_Relaunch_WasInOldPaused"
    else:
        name = f"{sku_clean}_{date_str}_AI_BidDown5pctAdSpend25pctProfit"

    print(f"  Campaign: {name}")

    if dry_run:
        print(f"\n  DRY RUN -- preview only, no creation")
        for k in kw_typed[:10]:
            print(f"    {k['keyword']:<40} {k['matchType']}")
        if len(kw_typed) > 10:
            print(f"    ... +{len(kw_typed)-10} more")
        save_opps(asin, sku, opps)
        return {'dry_run': True, 'keywords': len(kw_typed), 'opps': len(opps)}

    print(f"  [6] Creating on Amazon...")
    result = create_on_amazon(asin, sku, name, budget, bid, kw_typed)
    print(f"      Campaign: {result['campaign_id']}")
    print(f"      Ad: {'OK' if result['ad_ok'] else 'INELIGIBLE'}")
    print(f"      Keywords: {result['kw_count']}")
    for e in result['errors']:
        print(f"      ERROR: {e}")

    print(f"  [7] Saving opportunities...")
    opp_count = save_opps(asin, sku, opps)
    print(f"      {opp_count} saved")

    # Save record
    record = {**candidate, 'campaign_name': name, 'campaign_id': result['campaign_id'],
        'adgroup_id': result['adgroup_id'], 'budget': budget, 'bid': bid,
        'keywords_created': result['kw_count'], 'ad_eligible': result['ad_ok'],
        'opportunities': len(opps), 'created_at': datetime.now().isoformat()}
    record_file = os.path.join(JSON_DIR, f"campaign_created_{sku[:25].replace(' ','_')}.json")
    with open(record_file, 'w') as f:
        json.dump(record, f, indent=2)

    status = "LIVE!" if result['ad_ok'] else "CREATED (ad ineligible)"
    print(f"\n  RESULT: {status}")
    return result

# ============================================
# MAIN
# ============================================
def main():
    parser = argparse.ArgumentParser(description='GoAmrita Auto Campaign Creator v2.0')
    parser.add_argument('--mode', choices=['profit', 'newlisting'], default='profit')
    parser.add_argument('--top', type=int, default=1, help='How many campaigns (profit mode)')
    parser.add_argument('--days', type=int, default=8, help='New listing days (newlisting mode)')
    parser.add_argument('--asin', type=str, help='Specific ASIN')
    parser.add_argument('--dry-run', action='store_true', help='Preview only')
    parser.add_argument('--include-paused', action='store_true', default=False,
        help='Also create campaigns for paused ASINs (DEFAULT: No — avoids pause/create loop)')
    args = parser.parse_args()

    print("=" * 60)
    print("  GoAmrita - Auto Campaign Creator v2.0")
    print(f"  {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print(f"  Mode: {args.mode.upper()} | Dry: {args.dry_run}")
    print("=" * 60)

    if args.asin:
        # Load data for specific ASIN
        profit_map = {}
        if os.path.exists(os.path.join(JSON_DIR, "true_profit_per_asin.json")):
            with open(os.path.join(JSON_DIR, "true_profit_per_asin.json")) as f:
                for p in json.load(f):
                    profit_map[p['asin']] = p
        price_map = {}
        if os.path.exists(os.path.join(JSON_DIR, "sp_pricing_data.json")):
            with open(os.path.join(JSON_DIR, "sp_pricing_data.json")) as f:
                price_map = json.load(f)
        ads_list = []
        if os.path.exists(os.path.join(JSON_DIR, "sp_product_ads_list.json")):
            with open(os.path.join(JSON_DIR, "sp_product_ads_list.json")) as f:
                ads_list = json.load(f)

        sku = next((a['sku'] for a in ads_list if a['asin'] == args.asin), 'UNKNOWN')
        p = profit_map.get(args.asin, {})
        pr = price_map.get(args.asin, {})
        candidates = [{'asin': args.asin, 'sku': sku,
            'price': pr.get('your_price', p.get('sale_price', 0)),
            'true_profit': p.get('true_profit', 0), 'mode': args.mode}]
    elif args.mode == 'profit':
        rerun = not args.include_paused  # Default: skip paused (include_paused=False means pass True to get_existing)
        print(f"\n  Finding top {args.top} profitable ASINs without campaigns...")
        print(f"  Re-run paused: {'YES' if args.include_paused else 'NO (default — avoids loop)'}")
        candidates = find_profit_candidates(top_n=args.top, include_paused_skip=not args.include_paused)
    else:
        print(f"\n  Finding new listings (last {args.days} days) without campaigns...")
        candidates = find_newlisting_candidates(days=args.days)

    if not candidates:
        print("\n  No candidates found!")
        return 1

    print(f"\n  Candidates: {len(candidates)}")
    for i, c in enumerate(candidates, 1):
        date_info = f" | Listed: {c.get('launch_date','')}" if c.get('launch_date') else ''
        print(f"    {i}. {c['asin']} | {c['sku'][:25]} | Rs.{c['price']:.0f} | Profit: Rs.{c['true_profit']:.0f}{date_info}")

    created = 0
    for c in candidates:
        r = run_pipeline(c, dry_run=args.dry_run)
        if r:
            created += 1
        time.sleep(2)

    action = 'previewed' if args.dry_run else 'created'
    print(f"\n{'='*60}")
    print(f"  DONE! {created}/{len(candidates)} campaigns {action}")
    print(f"{'='*60}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
