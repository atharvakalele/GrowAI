#!/usr/bin/env python3
"""
GoAmrita - Create SP Campaign v1.0
====================================
Creates Manual Keyword Targeting campaign on Amazon
"""
import json, ssl, sys, time
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from datetime import datetime

try:
    import certifi
    ctx = ssl.create_default_context(cafile=certifi.where())
except:
    ctx = ssl.create_default_context()

creds = json.load(open('C:/Users/Clu/Documents/Amazon Bussiness Grouth Automation AI/api_credentials.json'))

# Token
data = urlencode({'grant_type':'refresh_token','refresh_token':creds['refresh_token'],
    'client_id':creds['client_id'],'client_secret':creds['client_secret']}).encode()
req = Request(creds['token_url'], data=data, headers={'Content-Type':'application/x-www-form-urlencoded'})
token = json.loads(urlopen(req, context=ctx).read().decode())['access_token']
print("Token ready!")

def api(method, path, body, ct):
    url = f"{creds['api_endpoint']}{path}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Amazon-Advertising-API-ClientId': creds['client_id'],
        'Amazon-Advertising-API-Scope': str(creds['profile_id']),
        'Content-Type': ct, 'Accept': ct,
        'Prefer': 'return=representation'
    }
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method=method)
    try:
        resp = urlopen(req, context=ctx)
        return json.loads(resp.read().decode()), resp.status
    except Exception as e:
        err = e.read().decode() if hasattr(e, 'read') else str(e)
        return {'error': err[:500]}, getattr(e, 'code', 0)

ASIN = 'B0FK4PK4HK'
NAME = 'LiBiDEXX30_13Apr2026_AI_BidDown5%OfAdSpend25%ofProfit'
BUDGET = 462.0
BID = 23.09
TODAY = datetime.now().strftime('%Y-%m-%d')

# STEP 1: Campaign
print(f"\n[1/4] Creating Campaign: {NAME}")
r1, s1 = api('POST', '/sp/campaigns', {
    'campaigns': [{
        'name': NAME,
        'state': 'ENABLED',
        'targetingType': 'MANUAL',
        'dynamicBidding': {'strategy': 'LEGACY_FOR_SALES', 'placementBidding': []},
        'budget': {'budgetType': 'DAILY', 'budget': BUDGET},
        'startDate': TODAY,
    }]
}, 'application/vnd.spCampaign.v3+json')

campaign_id = None
if 'error' not in r1:
    success = r1.get('campaigns', {}).get('success', [])
    if success:
        campaign_id = str(success[0].get('campaignId', success[0].get('campaign', {}).get('campaignId', '')))
    if not campaign_id:
        # Try other formats
        for item in r1.get('campaigns', r1.get('success', [])) if isinstance(r1.get('campaigns', r1.get('success', [])), list) else []:
            campaign_id = str(item.get('campaignId', ''))
            if campaign_id: break
    print(f"  Campaign ID: {campaign_id}" if campaign_id else f"  Response: {json.dumps(r1)[:400]}")
else:
    print(f"  Error: {r1['error'][:300]}")

if not campaign_id:
    print(f"  Full response: {json.dumps(r1)[:500]}")
    sys.exit(1)

time.sleep(1)

# STEP 2: Ad Group
print(f"\n[2/4] Creating Ad Group...")
r2, s2 = api('POST', '/sp/adGroups', {
    'adGroups': [{
        'campaignId': campaign_id,
        'name': 'AG_LiBiDEXX30_Keywords',
        'state': 'ENABLED',
        'defaultBid': BID
    }]
}, 'application/vnd.spAdGroup.v3+json')

adgroup_id = None
if 'error' not in r2:
    success = r2.get('adGroups', {}).get('success', [])
    if success:
        adgroup_id = str(success[0].get('adGroupId', success[0].get('adGroup', {}).get('adGroupId', '')))
    print(f"  Ad Group ID: {adgroup_id}" if adgroup_id else f"  Response: {json.dumps(r2)[:400]}")
else:
    print(f"  Error: {r2['error'][:300]}")

if not adgroup_id:
    print(f"  Full: {json.dumps(r2)[:500]}")
    sys.exit(1)

time.sleep(1)

# STEP 3: Product Ad
print(f"\n[3/4] Creating Product Ad (ASIN: {ASIN})...")
r3, s3 = api('POST', '/sp/productAds', {
    'productAds': [{
        'campaignId': campaign_id,
        'adGroupId': adgroup_id,
        'asin': ASIN,
        'state': 'ENABLED'
    }]
}, 'application/vnd.spProductAd.v3+json')

if 'error' not in r3:
    print(f"  Product Ad created!")
else:
    print(f"  Error: {r3['error'][:300]}")

time.sleep(1)

# STEP 4: Keywords (15)
print(f"\n[4/4] Creating 15 Keywords...")
keywords = [
    {'kw': 'libidex capsule', 'mt': 'PHRASE'},
    {'kw': 'libidex oil', 'mt': 'PHRASE'},
    {'kw': 'libidex men', 'mt': 'PHRASE'},
    {'kw': 'libedax capsule', 'mt': 'PHRASE'},
    {'kw': 'libidecx capsule', 'mt': 'PHRASE'},
    {'kw': 'libidex capsule men', 'mt': 'EXACT'},
    {'kw': 'libidex capsule men original', 'mt': 'EXACT'},
    {'kw': 'libidex gold capsule', 'mt': 'EXACT'},
    {'kw': 'libedex original capsule', 'mt': 'EXACT'},
    {'kw': 'libidex ultimate capsule', 'mt': 'EXACT'},
    {'kw': 'libidex capsules rs 2490', 'mt': 'EXACT'},
    {'kw': 'erectile dysfunction homeopathic medicine', 'mt': 'EXACT'},
    {'kw': 'libidex gold capsule patanjali', 'mt': 'EXACT'},
    {'kw': 'libdiex capsule men', 'mt': 'EXACT'},
    {'kw': 'libidix capsule man', 'mt': 'EXACT'},
]

r4, s4 = api('POST', '/sp/keywords', {
    'keywords': [{
        'campaignId': campaign_id,
        'adGroupId': adgroup_id,
        'keywordText': k['kw'],
        'matchType': k['mt'],
        'bid': BID,
        'state': 'ENABLED'
    } for k in keywords]
}, 'application/vnd.spKeyword.v3+json')

if 'error' not in r4:
    kw_success = r4.get('keywords', {}).get('success', [])
    kw_error = r4.get('keywords', {}).get('error', [])
    print(f"  Success: {len(kw_success)} | Errors: {len(kw_error)}")
    for e in kw_error[:3]:
        print(f"    Error: {json.dumps(e)[:200]}")
else:
    print(f"  Error: {r4['error'][:300]}")

# SUMMARY
print(f"\n{'='*60}")
print(f"  CAMPAIGN CREATED!")
print(f"{'='*60}")
print(f"  Name:       {NAME}")
print(f"  Campaign ID:{campaign_id}")
print(f"  AdGroup ID: {adgroup_id}")
print(f"  ASIN:       {ASIN}")
print(f"  Budget:     Rs.{BUDGET}/day")
print(f"  Bid:        Rs.{BID}/keyword")
print(f"  Keywords:   15 (5 PHRASE + 10 EXACT)")
print(f"  Bidding:    Dynamic DOWN ONLY")
print(f"  Status:     ENABLED (LIVE!)")
print(f"{'='*60}")

# Save to JSON for reference
output = {
    'campaign_name': NAME, 'campaign_id': campaign_id,
    'adgroup_id': adgroup_id, 'asin': ASIN,
    'budget': BUDGET, 'bid': BID,
    'keywords': keywords, 'created_at': datetime.now().isoformat(),
    'formula': '25% of true profit = budget, 5% of budget = bid',
    'true_profit': 1847.28
}
out_file = 'C:/Users/Clu/Documents/Amazon Bussiness Grouth Automation AI/ClaudeCode/Report/12 April 2026/Json/campaign_created_LiBiDEXX30.json'
with open(out_file, 'w') as f:
    json.dump(output, f, indent=2)
print(f"\n  Saved: {out_file}")
