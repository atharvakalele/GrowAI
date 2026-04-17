#!/usr/bin/env python3
"""
GoAmrita - Intraday Sales Compare v1.0 (A13)
==============================================
Compares today's sales at THIS time vs yesterday at SAME time.
Alerts if drop > threshold%.

API: SP-API Orders v0 (getOrders)
Schedule: Every 4 hours (configurable)

Usage:
    python intraday_sales_v1.0.py
    python intraday_sales_v1.0.py --threshold 30  (alert if drop > 30%)
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
SP_CREDS = json.load(open(os.path.join(PROJECT_DIR, "sp_api_credentials.json")))["sp_api_credentials"]

REPORT_BASE = os.path.join(SCRIPT_DIR, "..", "Report")
report_folders = [f for f in os.listdir(REPORT_BASE) if os.path.isdir(os.path.join(REPORT_BASE, f))]
report_folders.sort(key=lambda x: os.path.getmtime(os.path.join(REPORT_BASE, x)), reverse=True)
LATEST_REPORT = report_folders[0] if report_folders else datetime.now().strftime("%d %B %Y")
JSON_DIR = os.path.join(REPORT_BASE, LATEST_REPORT, "Json")

MARKETPLACE_ID = "A21TJRUUN4KGV"
SP_ENDPOINT = "https://sellingpartnerapi-eu.amazon.com"
HISTORY_FILE = os.path.join(JSON_DIR, "sales_snapshots.json")

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


def fetch_orders(created_after, created_before):
    """Fetch orders in time window"""
    token = get_token()
    params = {
        'MarketplaceIds': MARKETPLACE_ID,
        'CreatedAfter': created_after,
        'CreatedBefore': created_before,
        # No status filter = get ALL orders (we filter canceled in calc_sales_summary)
    }
    url = f"{SP_ENDPOINT}/orders/v0/orders?" + urlencode(params)
    headers = {
        'x-amz-access-token': token,
        'x-amz-date': datetime.utcnow().strftime('%Y%m%dT%H%M%SZ'),
        'Host': 'sellingpartnerapi-eu.amazon.com',
    }
    req = Request(url, headers=headers)

    try:
        resp = urlopen(req, context=SSL_CONTEXT)
        result = json.loads(resp.read().decode())
        orders = result.get('payload', result).get('Orders', [])

        # Paginate
        next_token = result.get('payload', result).get('NextToken')
        while next_token:
            params2 = {'MarketplaceIds': MARKETPLACE_ID, 'NextToken': next_token}
            url2 = f"{SP_ENDPOINT}/orders/v0/orders?" + urlencode(params2)
            req2 = Request(url2, headers=headers)
            resp2 = urlopen(req2, context=SSL_CONTEXT)
            r2 = json.loads(resp2.read().decode())
            orders.extend(r2.get('payload', r2).get('Orders', []))
            next_token = r2.get('payload', r2).get('NextToken')
            time.sleep(0.5)

        return orders
    except HTTPError as e:
        print(f"  API Error {e.code}: {e.read().decode()[:200]}")
        return []


def calc_sales_summary(orders):
    """Calculate combined sales (exclude canceled)"""
    active = [o for o in orders if o.get('OrderStatus') != 'Canceled']
    pending = [o for o in active if o.get('OrderStatus') == 'Pending']
    confirmed = [o for o in active if o.get('OrderStatus') != 'Pending']

    revenue = 0
    for o in active:
        try:
            revenue += float(o.get('OrderTotal', {}).get('Amount', 0))
        except (ValueError, TypeError):
            pass

    # Estimate pending revenue (avg of confirmed orders)
    if confirmed and pending:
        avg_order = revenue / len(confirmed) if confirmed else 0
        pending_estimate = avg_order * len(pending)
        revenue += pending_estimate

    return {
        'orders': len(active),
        'revenue': round(revenue, 2),
        'pending': len(pending),
    }


def load_snapshots():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {'snapshots': []}


def save_snapshot(snapshots, data):
    snapshots['snapshots'].append(data)
    # Keep last 30 days
    cutoff = (datetime.now() - timedelta(days=30)).isoformat()
    snapshots['snapshots'] = [s for s in snapshots['snapshots'] if s.get('timestamp', '') > cutoff]
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(snapshots, f, indent=2, ensure_ascii=False)


def find_yesterday_snapshot(snapshots, current_hour):
    """Find yesterday's snapshot at same hour (±1 hour tolerance)"""
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    best = None
    for s in snapshots.get('snapshots', []):
        if s.get('date') == yesterday:
            hour_diff = abs(s.get('hour', 0) - current_hour)
            if hour_diff <= 1:
                if best is None or hour_diff < abs(best.get('hour', 0) - current_hour):
                    best = s
    return best


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Intraday Sales Compare')
    parser.add_argument('--threshold', type=int, default=10, help='Alert if drop > X%% (default: 10)')
    args = parser.parse_args()

    now = datetime.now()
    current_hour = now.hour

    print("=" * 60)
    print("  GoAmrita - Intraday Sales Compare v1.0")
    print(f"  {now.strftime('%d %B %Y, %I:%M %p')}")
    print(f"  Alert threshold: > {args.threshold}% drop")
    print("=" * 60)

    # Today's orders: from start of day to now
    # Amazon Orders API uses UTC. IST = UTC + 5:30
    # Today IST 00:00 = Yesterday UTC 18:30
    ist_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    utc_start = ist_midnight - timedelta(hours=5, minutes=30)
    utc_end = now - timedelta(hours=5, minutes=30)
    today_start = utc_start.strftime('%Y-%m-%dT%H:%M:%S')
    today_now = utc_end.strftime('%Y-%m-%dT%H:%M:%S')

    print(f"\n  Fetching today's orders (00:00 to {now.strftime('%H:%M')})...")
    today_orders = fetch_orders(today_start, today_now)
    ts = calc_sales_summary(today_orders)

    print(f"\n  TODAY so far:")
    print(f"    {ts['orders']} orders | Rs.{ts['revenue']:,.0f}")
    print(f"    Last Sync: {now.strftime('%I:%M %p')}")

    # Save today's snapshot
    snapshots = load_snapshots()
    today_snapshot = {
        'timestamp': now.isoformat(),
        'date': now.strftime('%Y-%m-%d'),
        'hour': current_hour,
        'time_label': now.strftime('%I:%M %p'),
        'orders': ts['orders'],
        'revenue': ts['revenue'],
    }
    save_snapshot(snapshots, today_snapshot)

    # Find yesterday's snapshot at same time
    yesterday_snap = find_yesterday_snapshot(snapshots, current_hour)

    if yesterday_snap:
        y_time = yesterday_snap.get('time_label', '?')
        y_orders = yesterday_snap.get('orders', yesterday_snap.get('total_orders', 0))
        y_revenue = yesterday_snap.get('revenue', yesterday_snap.get('total_revenue', 0))

        print(f"\n  YESTERDAY (same time ~{y_time}):")
        print(f"    {y_orders} orders | Rs.{y_revenue:,.0f}")

        def calc_change(today_val, yesterday_val):
            if yesterday_val > 0:
                return ((today_val - yesterday_val) / yesterday_val) * 100
            return 0 if today_val == 0 else 100

        def fmt_change(pct):
            if pct > 0: return f"+{pct:.0f}%"
            if pct < 0: return f"{pct:.0f}%"
            return "Same"

        changes = {
            'orders': calc_change(ts['orders'], y_orders),
            'revenue': calc_change(ts['revenue'], y_revenue),
        }

        print(f"\n  {'='*50}")
        print(f"  Today vs Yesterday")
        print(f"  {'='*50}")
        print(f"  {'':>14} {'Today':>10} {'Yesterday':>12} {'Change':>10}")
        print(f"  {'-'*50}")
        print(f"  Orders       {ts['orders']:>10} {y_orders:>12} {fmt_change(changes['orders']):>10}")
        print(f"  Revenue      Rs.{ts['revenue']:>7,.0f} Rs.{y_revenue:>9,.0f} {fmt_change(changes['revenue']):>10}")

        threshold = args.threshold
        alerts = []

        if changes['orders'] < -threshold or changes['revenue'] < -threshold:
            alerts.append(f"Sales dropped {fmt_change(changes['revenue'])} compared to yesterday")

        if alerts:
            print(f"\n  {'!'*50}")
            print(f"  ALERT: Your sales are down today!")
            for a in alerts:
                print(f"    {a}")
            print(f"\n  What to check:")
            print(f"    - Any listing suppressed or inactive?")
            print(f"    - Buy Box lost on any product?")
            print(f"    - Competitor dropped price?")
            print(f"    - Stock out on any product?")
            print(f"    - Any negative reviews recently?")
            print(f"  {'!'*50}")

        elif changes['orders'] > 20 or changes['revenue'] > 20:
            print(f"\n  Great! Your sales are UP {fmt_change(changes['revenue'])} compared to yesterday!")
        else:
            print(f"\n  Sales are steady. Looking good.")

    else:
        print(f"\n  No yesterday snapshot at {now.strftime('%I %p')} found.")
        print(f"  First run — snapshot saved. Compare available from tomorrow.")
        changes = {}
        alerts = []

    # Save result
    result_file = os.path.join(JSON_DIR, "sales_compare_latest.json")
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': now.isoformat(),
            'today': ts,
            'yesterday': {'orders': y_orders, 'revenue': y_revenue} if yesterday_snap else None,
            'changes': changes if yesterday_snap else {},
            'alerts': alerts if yesterday_snap else [],
            'alert_triggered': bool(alerts) if yesterday_snap else False,
        }, f, indent=2, ensure_ascii=False)

    print(f"\n  Saved: {result_file}")
    print(f"  Snapshots stored: {len(snapshots['snapshots'])} (last 30 days)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
