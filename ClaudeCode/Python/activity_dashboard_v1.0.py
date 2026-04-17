#!/usr/bin/env python3
"""
GoAmrita - Activity Dashboard v1.0
====================================
One place to see everything: what ran, what happened, what's next.
Generates clean HTML dashboard + CLI summary.

Usage:
    python activity_dashboard_v1.0.py              (CLI summary)
    python activity_dashboard_v1.0.py --html       (generate + open HTML dashboard)
    python activity_dashboard_v1.0.py --html --no-open  (generate only)
"""

import json
import os
import sys
import subprocess
import argparse
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))

REPORT_BASE = os.path.join(SCRIPT_DIR, "..", "Report")
report_folders = [f for f in os.listdir(REPORT_BASE) if os.path.isdir(os.path.join(REPORT_BASE, f))]
report_folders.sort(key=lambda x: os.path.getmtime(os.path.join(REPORT_BASE, x)), reverse=True)
LATEST_REPORT = report_folders[0] if report_folders else datetime.now().strftime("%d %B %Y")
JSON_DIR = os.path.join(REPORT_BASE, LATEST_REPORT, "Json")
DASHBOARD_FILE = os.path.join(REPORT_BASE, LATEST_REPORT, "GoAmrita_Dashboard.html")

SCHEDULER_LOG = os.path.join(SCRIPT_DIR, "..", "scheduler_log.json")


def load_json_safe(path):
    if os.path.exists(path):
        try:
            with open(path, encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {}


def get_file_age(path):
    if os.path.exists(path):
        age_sec = datetime.now().timestamp() - os.path.getmtime(path)
        if age_sec < 60: return f"{age_sec:.0f} sec ago"
        if age_sec < 3600: return f"{age_sec/60:.0f} min ago"
        if age_sec < 86400: return f"{age_sec/3600:.1f} hrs ago"
        return f"{age_sec/86400:.1f} days ago"
    return "Not found"


def get_scheduled_tasks():
    """Get Windows Task Scheduler status"""
    tasks = []
    try:
        result = subprocess.run(
            'schtasks /query /fo CSV /nh', shell=True,
            capture_output=True, text=True, timeout=10,
            env={**os.environ, 'MSYS_NO_PATHCONV': '1'}
        )
        for line in result.stdout.strip().split('\n'):
            if 'GoAmrita' in line:
                parts = line.strip('"').split('","')
                if len(parts) >= 3:
                    tasks.append({
                        'name': parts[0].replace('\\', ''),
                        'next_run': parts[1],
                        'status': parts[2] if len(parts) > 2 else '?',
                    })
    except:
        pass
    return tasks


def get_execution_logs():
    """Get all execution logs"""
    logs = []
    for f in sorted(os.listdir(JSON_DIR), reverse=True):
        if f.startswith('execution_log_') and f.endswith('.json'):
            data = load_json_safe(os.path.join(JSON_DIR, f))
            if data:
                logs.append({
                    'file': f,
                    'timestamp': data.get('timestamp', '?')[:19],
                    'dry_run': data.get('dry_run', False),
                    'total': data.get('summary', data).get('total_approved', data.get('total', 0)),
                    'ok': data.get('summary', data).get('executed_ok', data.get('ok', 0)),
                    'failed': data.get('summary', data).get('failed', 0),
                    'undo_count': len(data.get('undo_log', [])),
                })
    return logs[:10]


def get_stock_activity():
    """Get stock activity log"""
    path = os.path.join(JSON_DIR, "stock_activity_log.json")
    data = load_json_safe(path)
    activities = data.get('activities', [])
    recent = activities[-10:] if activities else []
    restocked = sum(1 for a in activities if a.get('action') == 'RESTOCK_SUCCESS')
    rejected = sum(1 for a in activities if a.get('action') == 'RESTOCK_REJECTED')
    return {'recent': recent, 'total': len(activities), 'restocked': restocked, 'rejected': rejected}


def get_sales_data():
    """Get latest sales comparison"""
    path = os.path.join(JSON_DIR, "sales_compare_latest.json")
    return load_json_safe(path)


def get_buybox_data():
    """Get Buy Box status"""
    path = os.path.join(JSON_DIR, "buy_box_status.json")
    data = load_json_safe(path)
    if isinstance(data, list):
        won = sum(1 for d in data if d.get('buy_box_status') == 'WON')
        lost = sum(1 for d in data if d.get('buy_box_status') == 'LOST')
        no_bb = sum(1 for d in data if d.get('buy_box_status') == 'NO_BUYBOX')
        return {'won': won, 'lost': lost, 'no_bb': no_bb, 'total': len(data)}
    return {'won': 0, 'lost': 0, 'no_bb': 0, 'total': 0}


def get_stock_data():
    path = os.path.join(JSON_DIR, "stock_status.json")
    data = load_json_safe(path)
    return {
        'zero': len(data.get('zero_stock', [])),
        'low': len(data.get('low_stock', [])),
        'healthy': data.get('healthy_count', 0),
    }


def get_campaign_data():
    """Get campaigns created by AI"""
    created = []
    for f in os.listdir(JSON_DIR):
        if f.startswith('campaign_created_') and f.endswith('.json'):
            data = load_json_safe(os.path.join(JSON_DIR, f))
            if data:
                created.append({
                    'name': data.get('campaign_name', data.get('name', '?'))[:40],
                    'asin': data.get('asin', ''),
                    'budget': data.get('budget', 0),
                    'keywords': data.get('keywords_created', data.get('keywords', 0)),
                    'date': data.get('created_at', data.get('created', ''))[:10],
                })
    return created


def get_reports_info():
    """Get report files info"""
    reports = []
    for f in os.listdir(os.path.join(REPORT_BASE, LATEST_REPORT)):
        if f.endswith('.xlsx') and not f.startswith('~'):
            path = os.path.join(REPORT_BASE, LATEST_REPORT, f)
            reports.append({
                'name': f,
                'size': f"{os.path.getsize(path)/1024:.0f} KB",
                'age': get_file_age(path),
            })
    return reports


def print_cli_dashboard():
    """Print CLI summary"""
    now = datetime.now()
    print(f"\n{'='*65}")
    print(f"  GoAmrita — Activity Dashboard")
    print(f"  {now.strftime('%d %B %Y, %I:%M %p')}")
    print(f"{'='*65}")

    # Scheduled Tasks
    tasks = get_scheduled_tasks()
    print(f"\n  SCHEDULED TASKS ({len(tasks)})")
    print(f"  {'-'*60}")
    for t in tasks:
        print(f"    {t['name']:<35} Next: {t['next_run']:<20} {t['status']}")

    # Sales
    sales = get_sales_data()
    today = sales.get('today', {})
    print(f"\n  TODAY'S SALES")
    print(f"  {'-'*60}")
    print(f"    Orders: {today.get('orders', '?')} | Revenue: Rs.{today.get('revenue', 0):,.0f}")
    if sales.get('alert_triggered'):
        print(f"    ALERT: Sales dropped!")

    # Buy Box
    bb = get_buybox_data()
    print(f"\n  BUY BOX")
    print(f"  {'-'*60}")
    print(f"    Won: {bb['won']} | Lost: {bb['lost']} | No BB: {bb['no_bb']}")

    # Stock
    stock = get_stock_data()
    print(f"\n  STOCK")
    print(f"  {'-'*60}")
    print(f"    Zero: {stock['zero']} | Low: {stock['low']} | Healthy: {stock['healthy']}")

    # Execution History
    logs = get_execution_logs()
    print(f"\n  RECENT EXECUTIONS")
    print(f"  {'-'*60}")
    for log in logs[:5]:
        dry = " [DRY]" if log['dry_run'] else ""
        print(f"    {log['timestamp']} | OK:{log['ok']} Failed:{log['failed']} Undo:{log['undo_count']}{dry}")

    # Campaigns Created
    camps = get_campaign_data()
    if camps:
        print(f"\n  AI-CREATED CAMPAIGNS ({len(camps)})")
        print(f"  {'-'*60}")
        for c in camps:
            print(f"    {c['name'][:35]:<35} KW:{c['keywords']} Budget:{c['budget']}")

    # Reports
    reports = get_reports_info()
    print(f"\n  REPORTS")
    print(f"  {'-'*60}")
    for r in reports:
        print(f"    {r['name']:<50} {r['size']:<8} {r['age']}")

    # Stock Activity
    sa = get_stock_activity()
    if sa['total'] > 0:
        print(f"\n  STOCK ACTIVITY")
        print(f"  {'-'*60}")
        print(f"    Restocked: {sa['restocked']} | Rejected: {sa['rejected']} | Total actions: {sa['total']}")

    print(f"\n{'='*65}")


def generate_html_dashboard():
    """Generate beautiful HTML dashboard"""
    now = datetime.now()
    tasks = get_scheduled_tasks()
    sales = get_sales_data()
    today = sales.get('today', {})
    bb = get_buybox_data()
    stock = get_stock_data()
    logs = get_execution_logs()
    camps = get_campaign_data()
    reports = get_reports_info()
    sa = get_stock_activity()

    tasks_html = ""
    for t in tasks:
        color = "#27AE60" if t['status'] == 'Ready' else "#E67E22"
        tasks_html += f'<tr><td>{t["name"]}</td><td>{t["next_run"]}</td><td style="color:{color};font-weight:bold">{t["status"]}</td></tr>'

    logs_html = ""
    for log in logs[:5]:
        dry = '<span style="color:#E67E22">[DRY RUN]</span>' if log['dry_run'] else ""
        logs_html += f'<tr><td>{log["timestamp"]}</td><td>{log["ok"]}</td><td>{log["failed"]}</td><td>{log["undo_count"]}</td><td>{dry}</td></tr>'

    camps_html = ""
    for c in camps:
        camps_html += f'<tr><td>{c["name"][:35]}</td><td>{c["asin"]}</td><td>Rs.{c["budget"]}</td><td>{c["keywords"]}</td><td>{c["date"]}</td></tr>'

    reports_html = ""
    for r in reports:
        reports_html += f'<tr><td>{r["name"]}</td><td>{r["size"]}</td><td>{r["age"]}</td></tr>'

    alert_banner = ""
    if sales.get('alert_triggered'):
        alert_banner = '<div style="background:#E74C3C;color:white;padding:15px;border-radius:8px;margin:15px 0;text-align:center;font-size:18px">ALERT: Sales dropped significantly today!</div>'
    if bb['lost'] > 0:
        alert_banner += f'<div style="background:#E67E22;color:white;padding:12px;border-radius:8px;margin:10px 0;text-align:center">Buy Box Lost: {bb["lost"]} products</div>'

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>GoAmrita Dashboard</title>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="300">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family:Calibri,Arial; background:#F5F6FA; color:#2C3E50; padding:20px; }}
        .header {{ background:linear-gradient(135deg,#1B3A5C,#2980B9); color:white; padding:25px; border-radius:12px; margin-bottom:20px; }}
        .header h1 {{ font-size:28px; margin-bottom:5px; }}
        .header p {{ opacity:0.85; }}
        .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:15px; margin-bottom:20px; }}
        .card {{ background:white; border-radius:10px; padding:20px; box-shadow:0 2px 8px rgba(0,0,0,0.08); }}
        .card h3 {{ font-size:13px; color:#7F8C8D; text-transform:uppercase; margin-bottom:8px; }}
        .card .value {{ font-size:28px; font-weight:bold; color:#1B3A5C; }}
        .card .sub {{ font-size:12px; color:#95A5A6; margin-top:4px; }}
        .section {{ background:white; border-radius:10px; padding:20px; margin-bottom:15px; box-shadow:0 2px 8px rgba(0,0,0,0.08); }}
        .section h2 {{ font-size:16px; color:#1B3A5C; margin-bottom:12px; border-bottom:2px solid #E8F0FE; padding-bottom:8px; }}
        table {{ width:100%; border-collapse:collapse; font-size:14px; }}
        th {{ background:#F8F9FA; padding:10px 12px; text-align:left; font-size:12px; color:#7F8C8D; text-transform:uppercase; }}
        td {{ padding:10px 12px; border-bottom:1px solid #F0F0F0; }}
        tr:hover {{ background:#F8F9FA; }}
        .green {{ color:#27AE60; }} .red {{ color:#E74C3C; }} .orange {{ color:#E67E22; }}
        .badge {{ display:inline-block; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:bold; }}
        .badge-green {{ background:#D5F5E3; color:#1E8449; }}
        .badge-red {{ background:#FADBD8; color:#C0392B; }}
        .badge-orange {{ background:#FDEBD0; color:#E67E22; }}
        .refresh {{ text-align:center; color:#BDC3C7; font-size:12px; margin-top:15px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>GoAmrita — Activity Dashboard</h1>
        <p>{now.strftime('%d %B %Y, %I:%M %p')} | Auto-refresh every 5 minutes</p>
    </div>

    {alert_banner}

    <div class="grid">
        <div class="card">
            <h3>Today's Sales</h3>
            <div class="value">Rs.{today.get('revenue',0):,.0f}</div>
            <div class="sub">{today.get('orders','?')} orders</div>
        </div>
        <div class="card">
            <h3>Buy Box</h3>
            <div class="value green">{bb['won']}</div>
            <div class="sub">Won | <span class="red">{bb['lost']} Lost</span> | {bb['no_bb']} No BB</div>
        </div>
        <div class="card">
            <h3>Stock Status</h3>
            <div class="value {'red' if stock['zero']>0 else 'green'}">{stock['zero']}</div>
            <div class="sub">Out of Stock | {stock['low']} Low | {stock['healthy']} OK</div>
        </div>
        <div class="card">
            <h3>AI Actions Today</h3>
            <div class="value">{logs[0]['ok'] if logs else 0}</div>
            <div class="sub">Executed | {logs[0]['failed'] if logs else 0} Failed</div>
        </div>
    </div>

    <div class="section">
        <h2>Scheduled Tasks</h2>
        <table>
            <tr><th>Task</th><th>Next Run</th><th>Status</th></tr>
            {tasks_html}
        </table>
    </div>

    <div class="section">
        <h2>Recent Executions</h2>
        <table>
            <tr><th>Time</th><th>OK</th><th>Failed</th><th>Undo Available</th><th>Note</th></tr>
            {logs_html}
        </table>
    </div>

    <div class="section">
        <h2>AI-Created Campaigns</h2>
        <table>
            <tr><th>Campaign</th><th>ASIN</th><th>Budget</th><th>Keywords</th><th>Created</th></tr>
            {camps_html}
        </table>
    </div>

    <div class="section">
        <h2>Reports</h2>
        <table>
            <tr><th>File</th><th>Size</th><th>Generated</th></tr>
            {reports_html}
        </table>
    </div>

    <div class="section">
        <h2>Stock Activity</h2>
        <p>Restocked: <b>{sa['restocked']}</b> | Don't Restock: <b>{sa['rejected']}</b> | Total Actions: <b>{sa['total']}</b></p>
    </div>

    <div class="refresh">
        Dashboard generated at {now.strftime('%I:%M %p')} | Auto-refreshes every 5 minutes | <a href="GoAmrita_Dashboard.html">Refresh Now</a>
    </div>
</body>
</html>"""

    os.makedirs(os.path.dirname(DASHBOARD_FILE), exist_ok=True)
    with open(DASHBOARD_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    return DASHBOARD_FILE


def main():
    parser = argparse.ArgumentParser(description='Activity Dashboard')
    parser.add_argument('--html', action='store_true', help='Generate HTML dashboard')
    parser.add_argument('--no-open', action='store_true', help='Do not auto-open browser')
    args = parser.parse_args()

    if args.html:
        path = generate_html_dashboard()
        print(f"  Dashboard: {path}")
        if not args.no_open:
            os.startfile(path)
    else:
        print_cli_dashboard()

    return 0


if __name__ == "__main__":
    sys.exit(main())
