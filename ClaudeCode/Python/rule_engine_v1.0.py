#!/usr/bin/env python3
"""
AutoGrow AI — Custom Rule Engine v1.0 (W13)
=============================================
Executes user-defined rules from config_custom_rules.json.
All 129+ data fields available for conditions.

Usage:
    python rule_engine_v1.0.py                (run all enabled rules)
    python rule_engine_v1.0.py --dry-run      (preview, no execute)
    python rule_engine_v1.0.py --rule rule_001 (run specific rule)
"""

import json
import os
import sys
import ssl
import re
import argparse
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
RULES_FILE = os.path.join(PROJECT_DIR, "config_custom_rules.json")
ADS_CREDS = json.load(open(os.path.join(PROJECT_DIR, "api_credentials.json")))

REPORT_BASE = os.path.join(SCRIPT_DIR, "..", "Report")
report_folders = [f for f in os.listdir(REPORT_BASE) if os.path.isdir(os.path.join(REPORT_BASE, f))]
report_folders.sort(key=lambda x: os.path.getmtime(os.path.join(REPORT_BASE, x)), reverse=True)
LATEST_REPORT = report_folders[0] if report_folders else datetime.now().strftime("%d %B %Y")
JSON_DIR = os.path.join(REPORT_BASE, LATEST_REPORT, "Json")
LOG_FILE = os.path.join(JSON_DIR, "rule_engine_log.json")

SSL_CONTEXT = None
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

_token = None
_expiry = None

def get_ads_token():
    global _token, _expiry
    if _token and _expiry and datetime.now() < _expiry:
        return _token
    data = urlencode({'grant_type': 'refresh_token', 'refresh_token': ADS_CREDS['refresh_token'],
        'client_id': ADS_CREDS['client_id'], 'client_secret': ADS_CREDS['client_secret']}).encode()
    req = Request(ADS_CREDS['token_url'], data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    result = json.loads(urlopen(req, context=SSL_CONTEXT).read().decode())
    _token = result['access_token']
    _expiry = datetime.now() + timedelta(seconds=result['expires_in'] - 60)
    return _token

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
        return {'error': e.read().decode()[:300]}, e.code


# ============================================
# LOAD ALL DATA
# ============================================
def load_all_data():
    """Load ALL available data into unified structure"""
    data = {}

    files = {
        'campaign': 'sp_campaigns_summary.json',
        'campaign_list': 'sp_campaign_list.json',
        'search_term': 'sp_searchterm_daily.json',
        'keyword': 'sp_targeting_daily.json',
        'product_ad': 'sp_advertisedproduct_daily.json',
        'product_profit': 'true_profit_per_asin.json',
        'pricing': 'sp_pricing_data.json',
        'stock': 'stock_status.json',
        'buy_box': 'buy_box_status.json',
        'keyword_list': 'sp_keyword_list.json',
        'ad_group': 'sp_adgroup_list.json',
    }

    for key, fname in files.items():
        path = os.path.join(JSON_DIR, fname)
        if os.path.exists(path):
            try:
                with open(path, encoding='utf-8') as f:
                    data[key] = json.load(f)
            except:
                data[key] = []
        else:
            data[key] = []

    return data


# ============================================
# GET ENTITIES TO CHECK (based on applies_to)
# ============================================
def get_entities(applies_to, all_data):
    """Get list of entities to evaluate rule against"""
    if applies_to == 'campaign':
        campaigns = all_data.get('campaign', [])
        campaign_map = {}
        for c in all_data.get('campaign_list', []):
            campaign_map[str(c.get('campaignId', ''))] = c

        entities = []
        for c in campaigns:
            cid = str(c.get('campaignId', ''))
            detail = campaign_map.get(cid, {})
            entity = {**c, **detail, '_type': 'campaign', '_id': cid,
                '_name': c.get('campaignName', detail.get('name', cid))}
            # Merge profit data if available
            entities.append(entity)
        return entities

    elif applies_to == 'keyword':
        return [{'_type': 'keyword', '_id': str(k.get('keywordId', '')),
            '_name': k.get('keyword', k.get('keywordText', '')), **k}
            for k in all_data.get('keyword', [])]

    elif applies_to == 'search_term':
        return [{'_type': 'search_term', '_id': str(i),
            '_name': k.get('searchTerm', ''), **k}
            for i, k in enumerate(all_data.get('search_term', []))]

    elif applies_to == 'stock':
        stock_data = all_data.get('stock', {})
        items = stock_data.get('zero_stock', []) + stock_data.get('low_stock', [])
        return [{'_type': 'stock', '_id': s.get('asin', ''),
            '_name': s.get('sku', ''), **s} for s in items]

    elif applies_to == 'buy_box':
        bb = all_data.get('buy_box', [])
        if isinstance(bb, list):
            return [{'_type': 'buy_box', '_id': b.get('asin', ''),
                '_name': b.get('sku', ''), **b} for b in bb]
        return []

    elif applies_to == 'account':
        # Single account-level entity with aggregated metrics
        campaigns = all_data.get('campaign', [])
        total_spend = sum(float(c.get('cost', 0)) for c in campaigns)
        total_sales = sum(float(c.get('sales7d', 0)) for c in campaigns)
        total_orders = sum(int(c.get('purchases7d', 0)) for c in campaigns)
        return [{'_type': 'account', '_id': 'account', '_name': 'Account',
            'total_spend': total_spend, 'total_sales': total_sales,
            'total_orders': total_orders,
            'acos': (total_spend / total_sales * 100) if total_sales > 0 else 0,
            'roas': (total_sales / total_spend) if total_spend > 0 else 0}]

    elif applies_to in ('product', 'asin_all'):
        # Merge product ad + profit + pricing + buy box + stock
        products = {}
        for p in all_data.get('product_ad', []):
            asin = p.get('advertisedAsin', '')
            if asin not in products:
                products[asin] = {'_type': 'product', '_id': asin, '_name': p.get('advertisedSku', asin)}
            for k, v in p.items():
                products[asin][f'product_ad.{k}'] = v
                products[asin][k] = v  # also flat

        profit_map = {}
        for p in all_data.get('product_profit', []):
            profit_map[p.get('asin', '')] = p

        pricing = all_data.get('pricing', {})
        stock_data = all_data.get('stock', {})
        zero_stock = {s.get('asin', ''): s for s in stock_data.get('zero_stock', [])} if isinstance(stock_data, dict) else {}
        bb_data = all_data.get('buy_box', [])
        bb_map = {b.get('asin', ''): b for b in bb_data} if isinstance(bb_data, list) else {}

        for asin, prod in products.items():
            if asin in profit_map:
                for k, v in profit_map[asin].items():
                    prod[f'product_profit.{k}'] = v
                    prod[k] = v
            if asin in pricing:
                for k, v in pricing[asin].items():
                    prod[f'pricing.{k}'] = v
                    prod[k] = v
            if asin in bb_map:
                for k, v in bb_map[asin].items():
                    prod[f'buy_box.{k}'] = v
                    prod[k] = v
            if asin in zero_stock:
                prod['stock.total_stock'] = 0
                prod['total_stock'] = 0
            else:
                prod['stock.total_stock'] = 999  # assume in stock if not in zero list

        return list(products.values())

    return []


# ============================================
# EVALUATE CONDITION
# ============================================
def evaluate_condition(entity, condition):
    """Check if entity matches a single condition"""
    field = condition.get('field', '')
    operator = condition.get('operator', '=')
    value = condition.get('value')

    # Get field value from entity (support dotted paths: "buy_box.is_ours")
    actual = entity.get(field)
    if actual is None:
        # Try without group prefix
        short_field = field.split('.')[-1] if '.' in field else field
        actual = entity.get(short_field)
    if actual is None:
        return False

    # Type convert for comparison
    try:
        if isinstance(value, (int, float)) and isinstance(actual, str):
            actual = float(actual)
        elif isinstance(value, str) and isinstance(actual, (int, float)):
            value = float(value)
        elif isinstance(value, bool):
            actual = bool(actual)
    except:
        pass

    if operator == '>': return actual > value
    if operator == '<': return actual < value
    if operator == '=': return actual == value
    if operator == '>=': return actual >= value
    if operator == '<=': return actual <= value
    if operator == '!=': return actual != value
    if operator == 'contains': return str(value).lower() in str(actual).lower()
    if operator == 'not_contains': return str(value).lower() not in str(actual).lower()

    return False


def evaluate_rule(entity, rule):
    """Check if entity matches ALL/ANY conditions of a rule"""
    conditions = rule.get('conditions', [])
    logic = rule.get('condition_logic', 'AND')

    if not conditions:
        return False

    results = [evaluate_condition(entity, c) for c in conditions]

    if logic == 'AND':
        return all(results)
    elif logic == 'OR':
        return any(results)
    return False


# ============================================
# EXECUTE ACTION
# ============================================
def execute_action(entity, action, rule_name, dry_run=False):
    """Execute a single action on an entity"""
    action_type = action.get('type', '')
    value = action.get('value', 0)
    reason = action.get('reason', action.get('message', rule_name))
    entity_name = entity.get('_name', entity.get('_id', '?'))[:30]
    entity_id = entity.get('_id', '')

    result = {
        'entity': entity_name, 'entity_id': entity_id,
        'action': action_type, 'value': value, 'rule': rule_name,
    }

    if dry_run:
        result['status'] = 'DRY_RUN'
        result['detail'] = f"Would {action_type} ({value}%) on {entity_name}"
        return result

    # Campaign actions
    if action_type == 'pause_campaign':
        cid = str(entity.get('campaignId', entity_id))
        r, _ = ads_api('PUT', '/sp/campaigns', {'campaigns': [{'campaignId': cid, 'state': 'PAUSED'}]},
            'application/vnd.spCampaign.v3+json')
        result['status'] = 'OK' if r.get('campaigns', {}).get('success') else 'FAILED'
        result['detail'] = f"Paused campaign {cid}"

    elif action_type == 'reduce_budget':
        cid = str(entity.get('campaignId', entity_id))
        budget = float(entity.get('campaignBudgetAmount', entity.get('budget', {}).get('budget', 500)))
        new_budget = max(50, round(budget * (1 - value / 100)))
        r, _ = ads_api('PUT', '/sp/campaigns', {'campaigns': [{'campaignId': cid,
            'budget': {'budgetType': 'DAILY', 'budget': float(new_budget)}}]},
            'application/vnd.spCampaign.v3+json')
        result['status'] = 'OK' if r.get('campaigns', {}).get('success') else 'FAILED'
        result['before'] = budget
        result['after'] = new_budget
        result['detail'] = f"Budget {budget} -> {new_budget}"

    elif action_type == 'increase_budget':
        cid = str(entity.get('campaignId', entity_id))
        budget = float(entity.get('campaignBudgetAmount', entity.get('budget', {}).get('budget', 500)))
        new_budget = round(budget * (1 + value / 100))
        r, _ = ads_api('PUT', '/sp/campaigns', {'campaigns': [{'campaignId': cid,
            'budget': {'budgetType': 'DAILY', 'budget': float(new_budget)}}]},
            'application/vnd.spCampaign.v3+json')
        result['status'] = 'OK' if r.get('campaigns', {}).get('success') else 'FAILED'
        result['before'] = budget
        result['after'] = new_budget

    elif action_type == 'pause_keyword':
        kid = str(entity.get('keywordId', entity_id))
        r, _ = ads_api('PUT', '/sp/keywords', {'keywords': [{'keywordId': kid, 'state': 'PAUSED'}]},
            'application/vnd.spKeyword.v3+json')
        result['status'] = 'OK' if r.get('keywords', {}).get('success') else 'FAILED'

    elif action_type in ('reduce_bid', 'increase_bid'):
        kid = str(entity.get('keywordId', entity_id))
        bid = float(entity.get('bid', entity.get('keywordBid', 5)))
        if action_type == 'reduce_bid':
            new_bid = max(2.0, round(bid * (1 - value / 100), 2))
        else:
            new_bid = round(bid * (1 + value / 100), 2)
        r, _ = ads_api('PUT', '/sp/keywords', {'keywords': [{'keywordId': kid, 'bid': new_bid}]},
            'application/vnd.spKeyword.v3+json')
        result['status'] = 'OK' if r.get('keywords', {}).get('success') else 'FAILED'
        result['before'] = bid
        result['after'] = new_bid

    elif action_type == 'send_alert':
        msg = reason.replace('{asin}', entity.get('_id', '?')).replace('{name}', entity.get('_name', '?'))
        result['status'] = 'OK'
        result['detail'] = f"Alert: {msg}"
        # TODO: integrate with email_alerts_v1.0.py

    elif action_type == 'monitor':
        result['status'] = 'OK'
        result['detail'] = 'Monitor only - no action'

    else:
        result['status'] = 'UNKNOWN_ACTION'

    return result


# ============================================
# MAIN
# ============================================
def main():
    parser = argparse.ArgumentParser(description='AutoGrow AI Rule Engine')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--rule', type=str, help='Run specific rule ID')
    args = parser.parse_args()

    print("=" * 55)
    print("  AutoGrow AI — Custom Rule Engine v1.0")
    print(f"  {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print(f"  Dry Run: {args.dry_run}")
    print("=" * 55)

    # Load rules
    with open(RULES_FILE, encoding='utf-8') as f:
        rules_config = json.load(f)

    rules = rules_config.get('rules', [])
    if args.rule:
        rules = [r for r in rules if r.get('id') == args.rule]

    enabled_rules = [r for r in rules if r.get('enabled', True)]
    print(f"\n  Rules: {len(enabled_rules)} enabled / {len(rules)} total")

    # Load data
    print(f"  Loading all data...")
    all_data = load_all_data()

    # Process each rule
    all_results = []
    for rule in enabled_rules:
        rule_name = rule.get('name', rule.get('id', '?'))
        applies_to = rule.get('applies_to', 'campaign')

        print(f"\n  Rule: {rule_name}")
        print(f"    Applies to: {applies_to}")

        entities = get_entities(applies_to, all_data)
        print(f"    Entities to check: {len(entities)}")

        matched = 0
        for entity in entities:
            if evaluate_rule(entity, rule):
                matched += 1
                for action in rule.get('actions', []):
                    result = execute_action(entity, action, rule_name, dry_run=args.dry_run)
                    result['rule_id'] = rule.get('id')
                    result['rule_name'] = rule_name
                    result['timestamp'] = datetime.now().isoformat()
                    all_results.append(result)

                    status = result.get('status', '?')
                    detail = result.get('detail', result.get('action', ''))
                    print(f"    [{status}] {entity.get('_name', '?')[:25]} → {detail}")

        print(f"    Matched: {matched} / {len(entities)}")

        # Update trigger count
        rule['last_triggered'] = datetime.now().isoformat() if matched > 0 else rule.get('last_triggered')
        rule['trigger_count'] = rule.get('trigger_count', 0) + matched

    # Save updated rules (trigger counts)
    with open(RULES_FILE, 'w', encoding='utf-8') as f:
        json.dump(rules_config, f, indent=2, ensure_ascii=False)

    # Save execution log
    os.makedirs(JSON_DIR, exist_ok=True)
    log = {
        'timestamp': datetime.now().isoformat(),
        'dry_run': args.dry_run,
        'rules_run': len(enabled_rules),
        'total_actions': len(all_results),
        'ok': sum(1 for r in all_results if r.get('status') in ('OK', 'DRY_RUN')),
        'failed': sum(1 for r in all_results if r.get('status') == 'FAILED'),
        'results': all_results,
    }
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

    print(f"\n  {'='*55}")
    print(f"  {'PREVIEW' if args.dry_run else 'EXECUTION'} COMPLETE")
    print(f"  Rules: {len(enabled_rules)} | Actions: {len(all_results)} | OK: {log['ok']} | Failed: {log['failed']}")
    print(f"  Log: {LOG_FILE}")
    print(f"  {'='*55}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
