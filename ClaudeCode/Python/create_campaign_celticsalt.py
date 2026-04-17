#!/usr/bin/env python3
"""Quick: Create campaign for AmazingCelticSalt2kg"""
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
data = urlencode({'grant_type':'refresh_token','refresh_token':creds['refresh_token'],
    'client_id':creds['client_id'],'client_secret':creds['client_secret']}).encode()
req = Request(creds['token_url'], data=data, headers={'Content-Type':'application/x-www-form-urlencoded'})
token = json.loads(urlopen(req, context=ctx).read().decode())['access_token']

def api(method, path, body, ct):
    url = creds['api_endpoint'] + path
    headers = {'Authorization':'Bearer '+token,'Amazon-Advertising-API-ClientId':creds['client_id'],
        'Amazon-Advertising-API-Scope':str(creds['profile_id']),'Content-Type':ct,'Accept':ct}
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method=method)
    try:
        resp = urlopen(req, context=ctx)
        return json.loads(resp.read().decode()), resp.status
    except Exception as e:
        return {'error': e.read().decode()[:500] if hasattr(e,'read') else str(e)}, getattr(e,'code',0)

ASIN = 'B0DFM7TY5T'
SKU = 'AmazingCelticSalt2kg'
PROFIT = 1755
BUDGET = round(PROFIT * 0.25)
BID = round(BUDGET * 0.05, 2)
NAME = 'CelticSalt2kg_13Apr2026_AI_BidDown5pctAdSpend25pctProfit'
TODAY = datetime.now().strftime('%Y-%m-%d')

print(f"Product: {SKU} | Budget: Rs.{BUDGET} | Bid: Rs.{BID}")

# Get keywords
print("\n[0] Keywords...")
r0, _ = api('POST', '/sp/targets/keywords/recommendations', {
    'recommendationType':'KEYWORDS_FOR_ASINS','asins':[ASIN],
    'maxRecommendations':50,'sortDimension':'CLICKS','locale':'en_IN'
}, 'application/vnd.spkeywordsrecommendation.v5+json')

all_kw = r0.get('keywordTargetList', [])
competitor_brands = ['proman','titan','viagra','patanjali','himalaya','dabur','tata','baidyanath']

campaign_kw = []
opportunity_kw = []
for kw in all_kw:
    word = kw.get('keyword','').lower()
    if any(cb in word for cb in competitor_brands):
        opportunity_kw.append(kw.get('keyword',''))
    else:
        words = len(word.split())
        campaign_kw.append({'keyword':kw.get('keyword',''), 'matchType':'PHRASE' if words<=2 else 'EXACT'})

print(f"  Campaign: {len(campaign_kw)} | Opportunity: {len(opportunity_kw)}")

# Create Campaign
print("\n[1] Campaign...")
r1, _ = api('POST', '/sp/campaigns', {'campaigns':[{
    'name':NAME,'state':'ENABLED','targetingType':'MANUAL',
    'dynamicBidding':{'strategy':'LEGACY_FOR_SALES','placementBidding':[]},
    'budget':{'budgetType':'DAILY','budget':float(BUDGET)},'startDate':TODAY
}]}, 'application/vnd.spCampaign.v3+json')

cid = str(r1.get('campaigns',{}).get('success',[{}])[0].get('campaignId',''))
print(f"  ID: {cid}" if cid else f"  Error: {json.dumps(r1)[:200]}")
if not cid: sys.exit(1)
time.sleep(1)

# Ad Group
print("\n[2] Ad Group...")
r2, _ = api('POST', '/sp/adGroups', {'adGroups':[{
    'campaignId':cid,'name':'AG_'+SKU+'_KW','state':'ENABLED','defaultBid':BID
}]}, 'application/vnd.spAdGroup.v3+json')

agid = str(r2.get('adGroups',{}).get('success',[{}])[0].get('adGroupId',''))
print(f"  ID: {agid}" if agid else f"  Error: {json.dumps(r2)[:200]}")
if not agid: sys.exit(1)
time.sleep(1)

# Product Ad
print("\n[3] Product Ad...")
r3, _ = api('POST', '/sp/productAds', {'productAds':[{
    'campaignId':cid,'adGroupId':agid,'asin':ASIN,'sku':SKU,'state':'ENABLED'
}]}, 'application/vnd.spProductAd.v3+json')

ad_ok = r3.get('productAds',{}).get('success',[])
ad_err = r3.get('productAds',{}).get('error',[])
if ad_ok:
    print(f"  Ad created!")
else:
    err_detail = ad_err[0].get('errors',[{}])[0] if ad_err else {}
    print(f"  FAILED: {json.dumps(err_detail)[:200]}")
time.sleep(1)

# Keywords
kws = campaign_kw[:20]
print(f"\n[4] {len(kws)} Keywords...")
r4, _ = api('POST', '/sp/keywords', {'keywords':[{
    'campaignId':cid,'adGroupId':agid,'keywordText':k['keyword'],
    'matchType':k['matchType'],'bid':BID,'state':'ENABLED'
} for k in kws]}, 'application/vnd.spKeyword.v3+json')

ks = r4.get('keywords',{}).get('success',[])
ke = r4.get('keywords',{}).get('error',[])
print(f"  Success: {len(ks)} | Errors: {len(ke)}")

print(f"\n{'='*60}")
print(f"  RESULT: {'LIVE!' if ad_ok else 'Ad INELIGIBLE (campaign+keywords created)'}")
print(f"  Campaign: {cid} | AdGroup: {agid}")
print(f"  Budget: Rs.{BUDGET} | Bid: Rs.{BID} | KW: {len(ks)}")
print(f"  Opportunity: {len(opportunity_kw)} competitor keywords")
print(f"{'='*60}")

# Save
json.dump({'campaign_id':cid,'adgroup_id':agid,'asin':ASIN,'sku':SKU,
    'budget':BUDGET,'bid':BID,'keywords':len(ks),'ad_eligible':bool(ad_ok),
    'opportunities':opportunity_kw,'name':NAME,'profit':PROFIT,
    'created':datetime.now().isoformat()},
    open(f'C:/Users/Clu/Documents/Amazon Bussiness Grouth Automation AI/ClaudeCode/Report/12 April 2026/Json/campaign_created_{SKU}.json','w'),indent=2)
