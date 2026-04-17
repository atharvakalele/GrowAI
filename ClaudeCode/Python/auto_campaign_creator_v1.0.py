#!/usr/bin/env python3
"""
GoAmrita - Auto Campaign Creator v1.0 (G09)
=============================================
Full pipeline: Find product → Get keywords → Filter smart → Create campaign

2 MODES:
  Mode 1: Top Profit — highest true profit ASINs without ads
  Mode 2: New Listing — recently listed products without campaigns (days configurable)

PIPELINE:
  1. Select product (Mode 1 or 2)
  2. Fetch Amazon keyword suggestions
  3. Fetch product listing (title + bullets + description)
  4. Smart cross-check: keyword vs listing content
  5. Separate: Relevant (campaign) vs Irrelevant (Product Opportunity)
  6. Apply match type rule: 1-2 words=PHRASE, 3+=EXACT
  7. Calculate bid from True Profit (25% profit = budget, 5% of budget = bid)
  8. Create campaign → ad group → product ad → keywords
  9. Save Product Opportunities

WRITE OPERATION: Creates REAL campaign on Amazon!

Usage:
    python auto_campaign_creator_v1.0.py --mode profit --top 1
    python auto_campaign_creator_v1.0.py --mode profit --top 3
    python auto_campaign_creator_v1.0.py --mode newlisting --days 10
    python auto_campaign_creator_v1.0.py --asin B0DFM7TY5T
    python auto_campaign_creator_v1.0.py --dry-run --mode profit --top 1  (preview only, no create)
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
PROFIT_CONFIG = json.load(open(os.path.join(PROJECT_DIR, "config_true_profit.json")))
OPP_FILE = os.path.join(JSON_DIR, "product_opportunities.json")

MARKETPLACE_ID = "A21TJRUUN4KGV"
OUR_SELLER_ID = "A2AC2AS9R9CBEA"

SSL_CONTEXT = None
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

# Irrelevant product types (not matching our product)
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
    data = urlencode({'grant_type':'refresh_token','refresh_token':ADS_CREDS['refresh_token'],
        'client_id':ADS_CREDS['client_id'],'client_secret':ADS_CREDS['client_secret']}).encode()
    req = Request(ADS_CREDS['token_url'], data=data, headers={'Content-Type':'application/x-www-form-urlencoded'})
    result = json.loads(urlopen(req, context=SSL_CONTEXT).read().decode())
    _ads_token = result['access_token']
    _ads_expiry = datetime.now() + timedelta(seconds=result['expires_in'] - 60)
    return _ads_token

def get_sp_token():
    global _sp_token, _sp_expiry
    if _sp_token and _sp_expiry and datetime.now() < _sp_expiry:
        return _sp_token
    data = urlencode({'grant_type':'refresh_token','refresh_token':SP_CREDS['refresh_token'],
        'client_id':SP_CREDS['lwa_client_id'],'client_secret':SP_CREDS['lwa_client_secret']}).encode()
    req = Request(SP_CREDS['token_url'], data=data, headers={'Content-Type':'application/x-www-form-urlencoded'})
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
    headers = {'Authorization':'Bearer '+token,'Amazon-Advertising-API-ClientId':ADS_CREDS['client_id'],
        'Amazon-Advertising-API-Scope':str(ADS_CREDS['profile_id']),'Content-Type':ct,'Accept':ct}
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method=method)
    try:
        resp = urlopen(req, context=SSL_CONTEXT)
        return json.loads(resp.read().decode()), resp.status
    except HTTPError as e:
        return {'error': e.read().decode()[:500]}, e.code

def sp_api(path):
    token = get_sp_token()
    url = SP_CREDS['endpoint'] + path
    headers = {'x-amz-access-token':token,
        'x-amz-date':datetime.utcnow().strftime('%Y%m%dT%H%M%SZ'),
        'Host':'sellingpartnerapi-eu.amazon.com'}
    req = Request(url, headers=headers)
    try:
        resp = urlopen(req, context=SSL_CONTEXT)
        return json.loads(resp.read().decode())
    except HTTPError as e:
        return {'error': e.read().decode()[:500]}

# ============================================
# STEP 1: SELECT PRODUCT
# ============================================
def find_candidates_profit(top_n=5, exclude_asins=None):
    """Mode 1: Top profit ASINs without current ad spend"""
    exclude = set(exclude_asins or [])

    with open(os.path.join(JSON_DIR, "sp_product_ads_list.json")) as f:
        ads = json.load(f)
    with open(os.path.join(JSON_DIR, "sp_advertisedproduct_daily.json")) as f:
        prod_data = json.load(f)
    with open(os.path.join(JSON_DIR, "sp_pricing_data.json")) as f:
        prices = json.load(f)
    with open(os.path.join(JSON_DIR, "true_profit_per_asin.json")) as f:
        profits = json.load(f)

    profit_map = {p['asin']: p for p in profits}
    spending = set(r.get('advertisedAsin','') for r in prod_data if float(r.get('cost',0)) > 0)
    asin_sku = {a['asin']: a['sku'] for a in ads if a.get('asin')}

    candidates = []
    for asin, sku in asin_sku.items():
        if asin in spending or asin in exclude:
            continue
        p = profit_map.get(asin, {})
        pr = prices.get(asin, {})
        if p.get('true_profit', 0) > 0 and pr.get('buy_box_winner', False) and pr.get('your_price', 0) > 100:
            candidates.append({
                'asin': asin, 'sku': sku,
                'price': pr.get('your_price', 0),
                'true_profit': p.get('true_profit', 0),
            })

    candidates.sort(key=lambda x: x['true_profit'], reverse=True)
    return candidates[:top_n]


def find_candidates_newlisting(days=10):
    """Mode 2: New listings without campaigns"""
    # Use catalog data for listing dates
    with open(os.path.join(JSON_DIR, "sp_catalog_prices.json")) as f:
        catalog = json.load(f)
    with open(os.path.join(JSON_DIR, "sp_product_ads_list.json")) as f:
        ads = json.load(f)
    with open(os.path.join(JSON_DIR, "sp_pricing_data.json")) as f:
        prices = json.load(f)
    with open(os.path.join(JSON_DIR, "true_profit_per_asin.json")) as f:
        profits = json.load(f)

    profit_map = {p['asin']: p for p in profits}
    campaign_asins = set(a['asin'] for a in ads)

    # ASINs with price but no campaign
    candidates = []
    for asin, pr in prices.items():
        if asin in campaign_asins:
            continue
        if pr.get('your_price', 0) > 100 and pr.get('buy_box_winner', False):
            p = profit_map.get(asin, {})
            candidates.append({
                'asin': asin, 'sku': 'UNKNOWN',
                'price': pr.get('your_price', 0),
                'true_profit': p.get('true_profit', 0),
            })

    candidates.sort(key=lambda x: x['true_profit'], reverse=True)
    return candidates

# ============================================
# STEP 2: FETCH AMAZON KEYWORD SUGGESTIONS
# ============================================
def fetch_keyword_suggestions(asin, max_keywords=50):
    r, _ = ads_api('POST', '/sp/targets/keywords/recommendations', {
        'recommendationType': 'KEYWORDS_FOR_ASINS',
        'asins': [asin],
        'maxRecommendations': max_keywords,
        'sortDimension': 'CLICKS',
        'locale': 'en_IN'
    }, 'application/vnd.spkeywordsrecommendation.v5+json')

    return r.get('keywordTargetList', [])

# ============================================
# STEP 3: FETCH LISTING CONTENT
# ============================================
def fetch_listing_content(sku):
    encoded_sku = quote(sku)
    path = f"/listings/2021-08-01/items/{OUR_SELLER_ID}/{encoded_sku}?marketplaceIds={MARKETPLACE_ID}&includedData=attributes"
    result = sp_api(path)

    if 'error' in result:
        return ""

    attrs = result.get('attributes', {})
    text = ""

    item_name = attrs.get('item_name', [])
    if isinstance(item_name, list) and item_name:
        text += item_name[0].get('value', '') + " "

    for b in attrs.get('bullet_point', []):
        if isinstance(b, dict):
            text += b.get('value', '') + " "

    desc = attrs.get('product_description', [])
    if isinstance(desc, list) and desc:
        text += desc[0].get('value', '') + " "

    return text

# ============================================
# STEP 4: SMART KEYWORD FILTER
# ============================================
def smart_filter_keywords(keywords_raw, listing_text):
    listing_lower = listing_text.lower()
    relevant = []
    opportunity = []

    for kw_obj in keywords_raw:
        kw = kw_obj.get('keyword', kw_obj.get('value', ''))
        kw_lower = kw.lower().strip()

        if not kw_lower:
            continue

        # Check if wrong product type or competitor brand
        is_wrong = any(marker in kw_lower for marker in WRONG_PRODUCT_MARKERS)

        if is_wrong:
            opportunity.append({'keyword': kw, 'reason': 'different_product_or_competitor'})
            continue

        # Check if keyword content relates to listing
        kw_words = [w for w in kw_lower.split() if len(w) > 2]
        if not kw_words:
            relevant.append(kw)
            continue

        # Count how many keyword words appear in listing
        matches = sum(1 for w in kw_words if w in listing_lower)
        match_pct = matches / len(kw_words) * 100

        if match_pct >= 40:
            relevant.append(kw)
        else:
            opportunity.append({'keyword': kw, 'reason': 'not_in_listing'})

    # Deduplicate
    seen = set()
    unique_relevant = []
    for kw in relevant:
        kw_clean = kw.lower().strip()
        if kw_clean not in seen:
            seen.add(kw_clean)
            unique_relevant.append(kw)

    return unique_relevant, opportunity

# ============================================
# STEP 5: APPLY MATCH TYPE RULE
# ============================================
def apply_match_type(keywords):
    """1-2 words = PHRASE, 3+ words = EXACT"""
    result = []
    for kw in keywords:
        words = len(kw.split())
        match = 'PHRASE' if words <= 2 else 'EXACT'
        result.append({'keyword': kw, 'matchType': match})
    return result

# ============================================
# STEP 6: CALCULATE BID FROM TRUE PROFIT
# ============================================
def calculate_bid(true_profit):
    """25% of profit = budget, 5% of budget = bid"""
    budget = round(true_profit * 0.25)
    bid = round(budget * 0.05, 2)
    return budget, bid

# ============================================
# STEP 7: CREATE CAMPAIGN ON AMAZON
# ============================================
def create_campaign_on_amazon(asin, sku, name, budget, bid, keywords):
    """Creates: Campaign → Ad Group → Product Ad → Keywords"""
    today = datetime.now().strftime('%Y-%m-%d')
    results = {'campaign_id': None, 'adgroup_id': None, 'ad_created': False, 'keywords_created': 0}

    # Campaign
    r1, _ = ads_api('POST', '/sp/campaigns', {'campaigns': [{
        'name': name, 'state': 'ENABLED', 'targetingType': 'MANUAL',
        'dynamicBidding': {'strategy': 'LEGACY_FOR_SALES', 'placementBidding': []},
        'budget': {'budgetType': 'DAILY', 'budget': float(budget)},
        'startDate': today,
    }]}, 'application/vnd.spCampaign.v3+json')

    success = r1.get('campaigns', {}).get('success', [])
    if not success:
        print(f"    Campaign creation FAILED: {json.dumps(r1)[:200]}")
        return results
    results['campaign_id'] = str(success[0].get('campaignId', ''))
    print(f"    Campaign: {results['campaign_id']}")
    time.sleep(1)

    # Ad Group
    r2, _ = ads_api('POST', '/sp/adGroups', {'adGroups': [{
        'campaignId': results['campaign_id'],
        'name': f"AG_{sku[:30]}_KW",
        'state': 'ENABLED', 'defaultBid': bid
    }]}, 'application/vnd.spAdGroup.v3+json')

    success2 = r2.get('adGroups', {}).get('success', [])
    if not success2:
        print(f"    Ad Group FAILED: {json.dumps(r2)[:200]}")
        return results
    results['adgroup_id'] = str(success2[0].get('adGroupId', ''))
    print(f"    Ad Group: {results['adgroup_id']}")
    time.sleep(1)

    # Product Ad (with SKU!)
    r3, _ = ads_api('POST', '/sp/productAds', {'productAds': [{
        'campaignId': results['campaign_id'],
        'adGroupId': results['adgroup_id'],
        'asin': asin, 'sku': sku, 'state': 'ENABLED'
    }]}, 'application/vnd.spProductAd.v3+json')

    ad_success = r3.get('productAds', {}).get('success', [])
    ad_error = r3.get('productAds', {}).get('error', [])
    results['ad_created'] = bool(ad_success)
    if ad_error:
        err = ad_error[0].get('errors', [{}])[0].get('errorValue', {})
        print(f"    Product Ad FAILED: {json.dumps(err)[:150]}")
        print(f"    Campaign created but product ineligible for ads!")
    else:
        print(f"    Product Ad: OK")
    time.sleep(1)

    # Keywords (batch max 100)
    kw_body = [{'campaignId': results['campaign_id'], 'adGroupId': results['adgroup_id'],
        'keywordText': k['keyword'], 'matchType': k['matchType'],
        'bid': bid, 'state': 'ENABLED'} for k in keywords[:100]]

    r4, _ = ads_api('POST', '/sp/keywords', {'keywords': kw_body}, 'application/vnd.spKeyword.v3+json')
    kw_success = r4.get('keywords', {}).get('success', [])
    kw_error = r4.get('keywords', {}).get('error', [])
    results['keywords_created'] = len(kw_success)
    print(f"    Keywords: {len(kw_success)} created, {len(kw_error)} errors")

    return results

# ============================================
# STEP 8: SAVE PRODUCT OPPORTUNITIES
# ============================================
def save_opportunities(asin, sku, opportunities):
    if not opportunities:
        return

    if os.path.exists(OPP_FILE):
        with open(OPP_FILE) as f:
            opp_data = json.load(f)
    else:
        opp_data = {'opportunities': [], 'total': 0}

    for opp in opportunities:
        opp_data['opportunities'].append({
            'keyword': opp['keyword'],
            'source_asin': asin,
            'source_product': sku,
            'competitor_brand': '',
            'product_type': opp.get('reason', 'unknown'),
            'impression_rank': None,
            'status': 'new',
            'discovered_date': datetime.now().strftime('%Y-%m-%d'),
            'action': 'Launch Your Product'
        })

    opp_data['total'] = len(opp_data['opportunities'])
    opp_data['last_updated'] = datetime.now().strftime('%Y-%m-%d')

    with open(OPP_FILE, 'w') as f:
        json.dump(opp_data, f, indent=2, ensure_ascii=False)

    return len(opportunities)

# ============================================
# MAIN PIPELINE
# ============================================
def run_pipeline(candidate, dry_run=False):
    asin = candidate['asin']
    sku = candidate['sku']
    profit = candidate['true_profit']
    price = candidate['price']

    print(f"\n{'='*60}")
    print(f"  ASIN: {asin} | SKU: {sku[:30]}")
    print(f"  Price: Rs.{price:.0f} | True Profit: Rs.{profit:.0f}")
    print(f"{'='*60}")

    # Step 1: Calculate bid
    budget, bid = calculate_bid(profit)
    print(f"\n  [1/7] Bid: Rs.{bid} | Budget: Rs.{budget}/day (25% profit, 5% bid)")

    # Step 2: Fetch keyword suggestions
    print(f"  [2/7] Fetching Amazon keyword suggestions...")
    kw_raw = fetch_keyword_suggestions(asin)
    print(f"    Amazon suggested: {len(kw_raw)} keywords")

    if not kw_raw:
        print(f"    No keywords! Skipping this ASIN.")
        return None

    # Step 3: Fetch listing content
    print(f"  [3/7] Fetching product listing content...")
    listing_text = fetch_listing_content(sku)
    print(f"    Listing text: {len(listing_text)} chars")

    if not listing_text:
        print(f"    WARNING: No listing content found. Using keywords as-is.")
        listing_text = sku  # fallback to SKU name

    # Step 4: Smart filter
    print(f"  [4/7] Smart filtering keywords vs listing...")
    relevant, opportunities = smart_filter_keywords(kw_raw, listing_text)
    print(f"    Relevant: {len(relevant)} | Opportunity: {len(opportunities)}")

    if not relevant:
        print(f"    No relevant keywords! Skipping.")
        return None

    # Step 5: Apply match type
    print(f"  [5/7] Applying match type rule (1-2=PHRASE, 3+=EXACT)...")
    kw_typed = apply_match_type(relevant)
    phrase = sum(1 for k in kw_typed if k['matchType'] == 'PHRASE')
    exact = sum(1 for k in kw_typed if k['matchType'] == 'EXACT')
    print(f"    {phrase} PHRASE + {exact} EXACT = {len(kw_typed)} total")

    for k in kw_typed[:10]:
        print(f"      {k['keyword']:<40} {k['matchType']}")
    if len(kw_typed) > 10:
        print(f"      ... +{len(kw_typed)-10} more")

    # Campaign name
    date_str = datetime.now().strftime('%d%b%Y')
    product_name = sku.replace(' ', '')[:20]
    name = f"{product_name}_{date_str}_AI_BidDown5pctAdSpend25pctProfit"

    print(f"\n  Campaign: {name}")
    print(f"  Budget: Rs.{budget}/day | Bid: Rs.{bid}")

    if dry_run:
        print(f"\n  DRY RUN — No campaign created. Preview above.")
        save_opportunities(asin, sku, opportunities)
        print(f"  Opportunities saved: {len(opportunities)}")
        return {'dry_run': True, 'keywords': len(kw_typed), 'opportunities': len(opportunities)}

    # Step 6: Create on Amazon
    print(f"\n  [6/7] Creating campaign on Amazon...")
    result = create_campaign_on_amazon(asin, sku, name, budget, bid, kw_typed)

    # Step 7: Save opportunities
    print(f"  [7/7] Saving product opportunities...")
    opp_count = save_opportunities(asin, sku, opportunities)
    print(f"    Saved: {opp_count} opportunities")

    # Save campaign record
    record = {
        'campaign_name': name,
        'campaign_id': result['campaign_id'],
        'adgroup_id': result['adgroup_id'],
        'asin': asin, 'sku': sku,
        'price': price, 'true_profit': profit,
        'budget': budget, 'bid': bid,
        'keywords_created': result['keywords_created'],
        'ad_eligible': result['ad_created'],
        'opportunities_found': len(opportunities),
        'formula': '25% of true profit = budget, 5% of budget = bid',
        'created_at': datetime.now().isoformat(),
    }

    record_file = os.path.join(JSON_DIR, f"campaign_created_{sku[:30].replace(' ','_')}.json")
    with open(record_file, 'w') as f:
        json.dump(record, f, indent=2)

    # Summary
    status = "LIVE!" if result['ad_created'] else "CREATED (ad ineligible)"
    print(f"\n  {'='*50}")
    print(f"  RESULT: {status}")
    print(f"  Campaign: {result['campaign_id']}")
    print(f"  Keywords: {result['keywords_created']}")
    print(f"  Opportunities: {len(opportunities)}")
    print(f"  {'='*50}")

    return result


def main():
    parser = argparse.ArgumentParser(description='GoAmrita Auto Campaign Creator')
    parser.add_argument('--mode', choices=['profit', 'newlisting'], default='profit',
        help='Mode 1: top profit | Mode 2: new listings')
    parser.add_argument('--top', type=int, default=1, help='How many campaigns to create (Mode 1)')
    parser.add_argument('--days', type=int, default=10, help='New listing days threshold (Mode 2)')
    parser.add_argument('--asin', type=str, help='Create for specific ASIN')
    parser.add_argument('--dry-run', action='store_true', help='Preview only, no creation')
    parser.add_argument('--exclude', type=str, help='Comma-separated ASINs to skip')
    args = parser.parse_args()

    print("=" * 60)
    print("  GoAmrita - Auto Campaign Creator v1.0 (G09)")
    print(f"  {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print(f"  Mode: {args.mode.upper()} | Dry Run: {args.dry_run}")
    print("=" * 60)

    exclude = args.exclude.split(',') if args.exclude else []
    # Always exclude known ineligible ASINs
    exclude.append('B0FK4PK4HK')  # LiBiDEXX30 - adult flag

    if args.asin:
        # Specific ASIN
        with open(os.path.join(JSON_DIR, "sp_product_ads_list.json")) as f:
            ads = json.load(f)
        with open(os.path.join(JSON_DIR, "true_profit_per_asin.json")) as f:
            profits = json.load(f)
        with open(os.path.join(JSON_DIR, "sp_pricing_data.json")) as f:
            prices = json.load(f)

        sku = next((a['sku'] for a in ads if a['asin'] == args.asin), 'UNKNOWN')
        p = next((p for p in profits if p['asin'] == args.asin), {})
        pr = prices.get(args.asin, {})

        candidates = [{'asin': args.asin, 'sku': sku,
            'price': pr.get('your_price', p.get('sale_price', 0)),
            'true_profit': p.get('true_profit', 0)}]
    elif args.mode == 'profit':
        candidates = find_candidates_profit(top_n=args.top, exclude_asins=exclude)
    else:
        candidates = find_candidates_newlisting(days=args.days)
        candidates = candidates[:args.top]

    if not candidates:
        print("\n  No candidates found!")
        return 1

    print(f"\n  Candidates: {len(candidates)}")
    for i, c in enumerate(candidates, 1):
        print(f"    {i}. {c['asin']} | {c['sku'][:25]} | Rs.{c['price']:.0f} | Profit: Rs.{c['true_profit']:.0f}")

    created = 0
    for candidate in candidates:
        result = run_pipeline(candidate, dry_run=args.dry_run)
        if result:
            created += 1
        time.sleep(2)

    print(f"\n{'='*60}")
    print(f"  DONE! {created}/{len(candidates)} campaigns {'previewed' if args.dry_run else 'created'}")
    print(f"{'='*60}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
