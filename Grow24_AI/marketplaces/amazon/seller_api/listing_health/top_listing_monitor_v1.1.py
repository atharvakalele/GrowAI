#!/usr/bin/env python3
"""
Grow24 AI - Top Listing Monitor v1.1
====================================
Legacy-compatible listing monitor with future-module summaries and shared
listing recovery routing.
"""

import argparse
import json
import os
import ssl
import subprocess
import sys
import time
from datetime import datetime, timedelta
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def find_project_dir(start_dir):
    current = os.path.abspath(start_dir)
    while True:
        if (
            os.path.exists(os.path.join(current, "sp_api_credentials.json"))
            and os.path.exists(os.path.join(current, "config_features.json"))
        ):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            raise RuntimeError("Project root not found for top listing monitor")
        current = parent


PROJECT_DIR = find_project_dir(SCRIPT_DIR)
SP_CREDS_FILE = os.path.join(PROJECT_DIR, "sp_api_credentials.json")
EMAIL_CONFIG = os.path.join(PROJECT_DIR, "config_email.json")

REPORT_BASE = os.path.join(PROJECT_DIR, "ClaudeCode", "Report")
report_folders = [f for f in os.listdir(REPORT_BASE) if os.path.isdir(os.path.join(REPORT_BASE, f))]
report_folders.sort(key=lambda x: os.path.getmtime(os.path.join(REPORT_BASE, x)), reverse=True)
LATEST_REPORT = report_folders[0] if report_folders else datetime.now().strftime("%d %B %Y")
JSON_DIR = os.path.join(REPORT_BASE, LATEST_REPORT, "Json")

FEATURE_ID = "M03"
FEATURE_KEY = "listing_monitor"
FEATURE_NAME = "Top Listing Monitor"
MODULE_GROUP = "listing_health"

STATUS_FILE = os.path.join(JSON_DIR, "top_listing_status.json")
IMPACT_LATEST_FILE = os.path.join(JSON_DIR, "impact_listing_monitor_latest.json")
ACTIVITY_LATEST_FILE = os.path.join(JSON_DIR, "activity_listing_monitor_latest.json")
REPORT_REGISTRY_FILE = os.path.join(JSON_DIR, "report_registry_latest.json")
LISTING_ROUTE_REQUEST_FILE = os.path.join(JSON_DIR, "listing_monitor_route_latest.json")
LISTING_ROUTE_RESULT_FILE = os.path.join(JSON_DIR, "listing_monitor_route_result_latest.json")
LISTING_RECOVERY_SCRIPT = os.path.join(PROJECT_DIR, "Grow24_AI", "marketplaces", "amazon", "seller_api", "listing_health", "listing_recovery_v1.0.py")
LISTING_RECOVERY_STATUS_FILE = os.path.join(JSON_DIR, "listing_recovery_status.json")

MARKETPLACE_ID = "A21TJRUUN4KGV"
SELLER_ID = "A2AC2AS9R9CBEA"
SP_ENDPOINT = "https://sellingpartnerapi-eu.amazon.com"

SSL_CONTEXT = None
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

SP_CREDS = json.load(open(SP_CREDS_FILE, encoding="utf-8"))["sp_api_credentials"]
_token = None
_expiry = None


def load_json(path, default=None):
    if default is None:
        default = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json_pair(latest_file, prefix, payload, started_at):
    os.makedirs(JSON_DIR, exist_ok=True)
    ts = started_at.strftime("%Y%m%d_%H%M%S")
    history_file = os.path.join(JSON_DIR, f"{prefix}_{ts}.json")
    with open(latest_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return history_file


def relative_path(path):
    return os.path.relpath(path, PROJECT_DIR).replace("\\", "/")


def find_latest_json_file(filename):
    for folder in report_folders:
        candidate = os.path.join(REPORT_BASE, folder, "Json", filename)
        if os.path.exists(candidate):
            return candidate
    return os.path.join(JSON_DIR, filename)


def get_token():
    global _token, _expiry
    if _token and _expiry and datetime.now() < _expiry:
        return _token
    data = urlencode({
        "grant_type": "refresh_token",
        "refresh_token": SP_CREDS["refresh_token"],
        "client_id": SP_CREDS["lwa_client_id"],
        "client_secret": SP_CREDS["lwa_client_secret"]
    }).encode()
    req = Request(SP_CREDS["token_url"], data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    result = json.loads(urlopen(req, context=SSL_CONTEXT).read().decode())
    _token = result["access_token"]
    _expiry = datetime.now() + timedelta(seconds=result["expires_in"] - 60)
    return _token


def check_listing_status(sku):
    try:
        token = get_token()
        encoded_sku = quote(sku)
        url = f"{SP_ENDPOINT}/listings/2021-08-01/items/{SELLER_ID}/{encoded_sku}?marketplaceIds={MARKETPLACE_ID}&includedData=summaries,issues"
        headers = {
            "x-amz-access-token": token,
            "x-amz-date": datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"),
            "Host": "sellingpartnerapi-eu.amazon.com",
        }
        req = Request(url, headers=headers)
        resp = urlopen(req, context=SSL_CONTEXT)
        result = json.loads(resp.read().decode())
    except HTTPError as e:
        return {
            "asin": "", "sku": sku, "name": "",
            "status": "API ERROR",
            "buyable": False, "discoverable": False,
            "statuses": [], "issues_count": 0, "issues": [],
            "error": e.read().decode()[:100],
        }
    except (URLError, Exception) as e:
        return {
            "asin": "", "sku": sku, "name": "",
            "status": "API ERROR",
            "buyable": False, "discoverable": False,
            "statuses": [], "issues_count": 0, "issues": [],
            "error": str(e)[:100],
        }

    summaries = result.get("summaries", [])
    issues = result.get("issues", [])
    status_list = []
    asin = ""
    item_name = ""
    for s in summaries:
        if s.get("marketplaceId") == MARKETPLACE_ID:
            status_list = s.get("status", [])
            asin = s.get("asin", "")
            item_name = s.get("itemName", "")[:40]
            break

    is_buyable = "BUYABLE" in status_list
    is_discoverable = "DISCOVERABLE" in status_list
    critical_issues = [i for i in issues if i.get("severity") in ("ERROR", "WARNING")]

    if is_buyable and is_discoverable:
        status = "ACTIVE"
    elif is_buyable and not is_discoverable:
        status = "NOT SEARCHABLE"
    elif not is_buyable:
        status = "NOT ACTIVE"
    else:
        status = "UNKNOWN"

    return {
        "asin": asin,
        "sku": sku,
        "name": item_name,
        "status": status,
        "buyable": is_buyable,
        "discoverable": is_discoverable,
        "statuses": status_list,
        "issues_count": len(critical_issues),
        "issues": [{"message": i.get("message", ""), "severity": i.get("severity", "")} for i in critical_issues[:3]],
    }


def get_top_sellers(top_n=20):
    prod_file = find_latest_json_file("sp_advertisedproduct_daily.json")
    ads_file = find_latest_json_file("sp_product_ads_list.json")

    if not os.path.exists(prod_file):
        return [], [relative_path(prod_file), relative_path(ads_file)]

    with open(prod_file, encoding="utf-8") as f:
        prod = json.load(f)

    sku_map = {}
    if os.path.exists(ads_file):
        with open(ads_file, encoding="utf-8") as f:
            for a in json.load(f):
                if a.get("asin") and a.get("sku"):
                    sku_map[a["asin"]] = a["sku"]

    asins = {}
    for r in prod:
        asin = r.get("advertisedAsin", "")
        if asin not in asins:
            asins[asin] = {"sku": r.get("advertisedSku", sku_map.get(asin, "")), "sales": 0.0, "orders": 0}
        asins[asin]["sales"] += float(r.get("sales7d", 0) or 0)
        asins[asin]["orders"] += int(r.get("purchases7d", 0) or 0)

    sellers = [(asin, data) for asin, data in asins.items() if data["orders"] >= 1]
    sellers.sort(key=lambda x: x[1]["sales"], reverse=True)
    if top_n > 0:
        sellers = sellers[:top_n]
    return (
        [{"asin": asin, "sku": data["sku"], "sales": data["sales"], "orders": data["orders"]} for asin, data in sellers],
        [relative_path(prod_file), relative_path(ads_file)]
    )


def send_alert_email(inactive_listings):
    try:
        config = load_json(EMAIL_CONFIG, {})
        if not config.get("enabled") or str(config.get("sender_app_password", "")).startswith("PASTE"):
            return
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        rows = ""
        for item in inactive_listings:
            color = "#DC2626" if item["status"] == "NOT ACTIVE" else "#D97706"
            issues = "<br>".join(f"- {i['message']}" for i in item.get("issues", [])[:3])
            rows += (
                f"<tr style='border-bottom:1px solid #eee'><td style='padding:8px'>{item['asin']}</td>"
                f"<td style='padding:8px'>{item['sku'][:25]}</td>"
                f"<td style='padding:8px;color:{color};font-weight:bold'>{item['status']}</td>"
                f"<td style='padding:8px;font-size:12px'>{issues}</td></tr>"
            )
        html = (
            "<html><body style='font-family:Calibri,Arial'>"
            "<div style='background:#DC2626;color:white;padding:15px;border-radius:8px'>"
            f"<h2>Grow24 AI - TOP SELLER ALERT!</h2><p>{len(inactive_listings)} top selling product(s) are NOT ACTIVE!</p></div>"
            "<div style='padding:15px;border:1px solid #ddd;border-radius:0 0 8px 8px'>"
            "<table style='width:100%;border-collapse:collapse'><tr style='background:#f8f8f8'><th>ASIN</th><th>SKU</th><th>Status</th><th>Issues</th></tr>"
            f"{rows}</table><p style='margin-top:15px;color:#666'>Check Amazon Seller Central immediately.</p></div></body></html>"
        )
        msg = MIMEMultipart()
        msg["From"] = f"Grow24 AI <{config['sender_email']}>"
        msg["To"] = ", ".join(config["recipients"]["critical_alerts"])
        msg["Subject"] = f"URGENT: {len(inactive_listings)} Top Seller(s) NOT ACTIVE!"
        msg.attach(MIMEText(html, "html"))
        server = smtplib.SMTP(config["smtp_server"], config["smtp_port"])
        server.starttls()
        server.login(config["sender_email"], config["sender_app_password"])
        server.send_message(msg)
        server.quit()
    except Exception:
        pass


def build_listing_route_requests(results, started_at):
    route_run_id = f"{FEATURE_KEY}_route_{started_at.strftime('%Y%m%d_%H%M%S')}"
    requests = []
    for item in results:
        if item.get("status") not in ("NOT ACTIVE", "NOT SEARCHABLE"):
            continue
        if not item.get("sku"):
            continue
        requests.append({
            "route_run_id": route_run_id,
            "source_feature_key": FEATURE_KEY,
            "source_feature_name": FEATURE_NAME,
            "action_family": "listing_recovery",
            "target_engine": "listing_recovery",
            "issue_type": "listing_not_active" if item.get("status") == "NOT ACTIVE" else "listing_not_searchable",
            "asin": item.get("asin", ""),
            "sku": item.get("sku", ""),
            "current_price": 0,
            "sales7d_rs": round(float(item.get("weekly_sales", 0) or 0), 2),
            "recommendation": "Start listing recovery workflow",
            "signals": [item.get("status", ""), *(issue.get("message", "") for issue in item.get("issues", [])[:2])],
            "route_reason": f"Listing status {item.get('status', 'UNKNOWN')} from top listing monitor.",
            "auto_action_allowed": True
        })
    payload = {
        "schema_type": "action_route_request",
        "schema_version": "1.0",
        "route_run_id": route_run_id,
        "generated_at": datetime.now().isoformat(),
        "source_feature_key": FEATURE_KEY,
        "source_feature_name": FEATURE_NAME,
        "action_engine": "listing_recovery",
        "requests": requests
    }
    history_file = save_json_pair(LISTING_ROUTE_REQUEST_FILE, "listing_monitor_route", payload, started_at)
    return payload, history_file


def execute_listing_routes(route_payload, route_history_file, started_at):
    result = {
        "route_type": "listing_recovery",
        "route_run_id": route_payload.get("route_run_id", ""),
        "generated_at": datetime.now().isoformat(),
        "engine": "listing_recovery",
        "request_count": len(route_payload.get("requests", [])),
        "status": "skipped",
        "reason": "",
        "actions": []
    }
    if not route_payload.get("requests"):
        result["reason"] = "No listing monitor findings qualified for recovery routing."
        return result, save_json_pair(LISTING_ROUTE_RESULT_FILE, "listing_monitor_route_result", result, started_at)
    if not os.path.exists(LISTING_RECOVERY_SCRIPT):
        result["status"] = "failed"
        result["reason"] = "Listing recovery script not found."
        return result, save_json_pair(LISTING_ROUTE_RESULT_FILE, "listing_monitor_route_result", result, started_at)
    cmd = [sys.executable, LISTING_RECOVERY_SCRIPT, "--route-file", route_history_file]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_DIR)
    status_data = load_json(LISTING_RECOVERY_STATUS_FILE, {})
    result["status"] = "executed" if proc.returncode == 0 else "failed"
    result["reason"] = "Listing recovery route executed." if proc.returncode == 0 else "Listing recovery route execution failed."
    result["command"] = " ".join(cmd)
    result["return_code"] = proc.returncode
    result["actions"] = list(status_data.get("price_route", {}).get("actions", []))
    result["checked_items"] = status_data.get("checked_items", [])
    return result, save_json_pair(LISTING_ROUTE_RESULT_FILE, "listing_monitor_route_result", result, started_at)


def summarize_action_routes(route_results):
    priority = {"failed": 5, "blocked": 4, "pending": 3, "executed": 2, "skipped": 1}
    status = "skipped"
    for route in route_results:
        if priority.get(route.get("status", "skipped"), 0) > priority.get(status, 0):
            status = route.get("status", "skipped")
    files = []
    for route in route_results:
        for key in ("request_file", "request_history_file", "result_file", "result_history_file"):
            if route.get(key):
                files.append(route.get(key))
    return {
        "status": status,
        "reason": " | ".join(route.get("reason", "") for route in route_results if route.get("reason")),
        "request_count": sum(int(route.get("request_count", 0) or 0) for route in route_results),
        "actions": [action for route in route_results for action in route.get("actions", [])],
        "files": files,
        "routes": route_results
    }


def get_status_and_impact(snapshot):
    run_errors = snapshot.get("run_errors", [])
    if run_errors and not snapshot.get("results"):
        return "failed", "critical"
    if run_errors:
        return "partial", "high"
    if snapshot.get("inactive", 0) or snapshot.get("warnings", 0):
        return "warning", "high"
    return "success", "low"


def build_impact_summary(snapshot, history_file):
    status, impact_level = get_status_and_impact(snapshot)
    results = snapshot.get("results", [])
    inactive_details = snapshot.get("inactive_details", [])
    warning_details = [r for r in results if r.get("status") == "NOT SEARCHABLE"]
    action_routing = snapshot.get("action_routing", {})
    actions_taken = action_routing.get("actions", [])
    action_asins = {item.get("asin", "") for item in actions_taken if item.get("asin")}
    action_sales_protected = round(sum(float(item.get("weekly_sales", 0) or 0) for item in results if item.get("asin") in action_asins), 2)
    revenue_at_risk = round(sum(float(item.get("weekly_sales", 0) or 0) for item in inactive_details + warning_details), 2)
    healthy_sales = round(sum(float(item.get("weekly_sales", 0) or 0) for item in results if item.get("status") == "ACTIVE"), 2)
    action_items = []
    for action in actions_taken[:10]:
        action_items.append({
            "asin": action.get("asin", ""),
            "sku": action.get("sku", ""),
            "action": action.get("action", ""),
            "status": action.get("status", ""),
            "old_price": round(float(action.get("old_price", 0) or 0), 2),
            "new_price": round(float(action.get("new_price", 0) or 0), 2),
            "reason": action.get("reason", "")
        })
    if actions_taken:
        ai_headline = f"AI executed {len(actions_taken)} listing recovery action(s) covering Rs.{action_sales_protected:.2f} 7-day sales."
    elif action_routing.get("request_count", 0):
        ai_headline = f"AI identified {action_routing.get('request_count', 0)} listing recovery candidate(s), execution status: {action_routing.get('status', 'pending')}."
    else:
        ai_headline = "AI did not execute a listing recovery action in this cycle."
    top_risks = []
    for item in sorted(inactive_details + warning_details, key=lambda x: float(x.get("weekly_sales", 0) or 0), reverse=True)[:10]:
        top_risks.append({
            "asin": item.get("asin", ""),
            "sku": item.get("sku", ""),
            "sales7d_rs": round(float(item.get("weekly_sales", 0) or 0), 2),
            "buy_box_status": item.get("status", ""),
            "competitor_count": 0,
            "price_gap_rs": 0,
            "recommendation": "Start listing recovery workflow"
        })
    return {
        "schema_type": "impact_summary",
        "schema_version": "1.0",
        "feature_id": FEATURE_ID,
        "feature_key": FEATURE_KEY,
        "feature_name": FEATURE_NAME,
        "module_group": MODULE_GROUP,
        "generated_at": snapshot.get("timestamp", datetime.now().isoformat()),
        "period": "manual",
        "status": status,
        "impact_level": impact_level,
        "business_areas": ["listing_health", "visibility", "revenue_protection"],
        "headline": f"Listing risk detected on {snapshot.get('inactive', 0) + snapshot.get('warnings', 0)} top ASIN(s)." if (snapshot.get("inactive", 0) or snapshot.get("warnings", 0)) else "Top listing monitor found no listing risk.",
        "summary_metrics": {
            "profit_impact_rs": 0,
            "loss_prevented_rs": 0,
            "waste_blocked_rs": 0,
            "revenue_protected_rs": healthy_sales,
            "ai_action_sales_protected_rs": action_sales_protected,
            "ai_actions_executed_count": len(actions_taken),
            "ai_actions_identified_count": int(action_routing.get("request_count", 0) or 0),
            "tracked_asins_count": int(snapshot.get("total", 0) or len(results)),
            "buy_box_won_count": 0,
            "buy_box_lost_count": int(snapshot.get("inactive", 0) or 0),
            "no_buy_box_count": int(snapshot.get("warnings", 0) or 0),
            "revenue_at_risk_7d_rs": revenue_at_risk
        },
        "positive_impacts": [{
            "type": "healthy_listings",
            "message": f"{snapshot.get('active', 0)} top ASIN(s) are active and discoverable.",
            "estimated_sales7d_rs": healthy_sales
        }] if snapshot.get("active", 0) else [],
        "negative_impacts": [{
            "type": "listing_risk",
            "message": f"{snapshot.get('inactive', 0)} inactive and {snapshot.get('warnings', 0)} not-searchable ASIN(s) need attention.",
            "estimated_sales7d_at_risk_rs": revenue_at_risk
        }] if top_risks else [],
        "top_risks": top_risks,
        "ai_action_summary": {
            "headline": ai_headline,
            "status": action_routing.get("status", "not_routed"),
            "actions_identified": int(action_routing.get("request_count", 0) or 0),
            "actions_executed": len(actions_taken),
            "expected_sales_protected_rs": action_sales_protected,
            "items": action_items
        },
        "recommendations": [
            "Inactive top ASINs should route into listing recovery.",
            "Not-searchable top ASINs should be checked for suppression and discovery issues.",
            f"Action routing status: {action_routing.get('status', 'not_routed')}."
        ],
        "detail_ref": {
            "raw_file": relative_path(STATUS_FILE),
            "detail_file": relative_path(history_file),
            "supporting_report": relative_path(STATUS_FILE)
        }
    }


def build_activity_summary(snapshot, history_file, impact_history_file, started_at, duration_sec, input_sources):
    action_routing = snapshot.get("action_routing", {})
    status, _impact_level = get_status_and_impact(snapshot)
    warnings = []
    if snapshot.get("inactive", 0):
        warnings.append(f"{snapshot.get('inactive', 0)} top ASIN(s) are NOT ACTIVE.")
    if snapshot.get("warnings", 0):
        warnings.append(f"{snapshot.get('warnings', 0)} top ASIN(s) are NOT SEARCHABLE.")
    action_history = []
    for route in action_routing.get("routes", []):
        action_history.append({
            "route_type": route.get("route_type", route.get("engine", "")),
            "engine": route.get("engine", ""),
            "status": route.get("status", ""),
            "request_count": int(route.get("request_count", 0) or 0),
            "actions_executed": len(route.get("actions", [])),
            "reason": route.get("reason", "")
        })
    return {
        "schema_type": "activity_summary",
        "schema_version": "1.0",
        "feature_id": FEATURE_ID,
        "feature_key": FEATURE_KEY,
        "feature_name": FEATURE_NAME,
        "module_group": MODULE_GROUP,
        "run_id": f"{FEATURE_KEY}_{started_at.strftime('%Y%m%d_%H%M%S')}",
        "generated_at": snapshot.get("timestamp", datetime.now().isoformat()),
        "status": status,
        "run_mode": "manual",
        "duration_sec": round(duration_sec, 2),
        "freshness_hours": 0.5,
        "needs_review": bool(warnings or snapshot.get("run_errors")),
        "input_sources": input_sources,
        "output_files": [relative_path(STATUS_FILE), relative_path(history_file), relative_path(impact_history_file), relative_path(ACTIVITY_LATEST_FILE), relative_path(REPORT_REGISTRY_FILE)] + [path for path in action_routing.get("files", []) if path],
        "counts": {
            "items_scanned": int(snapshot.get("total", 0) or 0),
            "items_processed": len(snapshot.get("results", [])),
            "alerts_generated": len(warnings),
            "approvals_needed": len(warnings),
            "warnings": len(warnings),
            "errors": len(snapshot.get("run_errors", [])),
            "action_routes_created": int(action_routing.get("request_count", 0) or 0),
            "action_routes_executed": len(action_routing.get("actions", []))
        },
        "run_events": [
            "Selected top revenue ASINs from ads data.",
            "Checked listing status via Amazon Listings API.",
            "Saved legacy top_listing_status.json output.",
            f"Action routing status: {action_routing.get('status', 'not_routed')}."
        ],
        "warnings_list": warnings,
        "errors_list": snapshot.get("run_errors", []),
        "review_items": {
            "user_review": warnings,
            "developer_review": [],
            "blocked_items": []
        },
        "action_history": action_history,
        "source_report_folder": LATEST_REPORT,
        "notes": "Top listing monitor now publishes future-module impact/activity beside legacy output."
    }


def build_registry_entry(impact_summary, activity_summary, history_file):
    status = impact_summary.get("status", "success")
    impact_level = impact_summary.get("impact_level", "low")
    priority_score = 80 if impact_level == "critical" else 70 if impact_level == "high" else 50
    return {
        "schema_type": "registry_entry",
        "schema_version": "1.0",
        "feature_id": FEATURE_ID,
        "feature_key": FEATURE_KEY,
        "feature_name": FEATURE_NAME,
        "module_group": MODULE_GROUP,
        "files": {
            "raw_output": relative_path(STATUS_FILE),
            "impact_summary": relative_path(IMPACT_LATEST_FILE),
            "activity_summary": relative_path(ACTIVITY_LATEST_FILE),
            "detail_report": relative_path(history_file)
        },
        "generated_at": impact_summary.get("generated_at", datetime.now().isoformat()),
        "dashboard_visibility": {
            "show_on_main": True,
            "show_on_activity": True,
            "show_on_home": True,
            "main_section": "Critical Impact Alerts",
            "activity_section": "Run Status"
        },
        "importance": {
            "status": status,
            "impact_level": impact_level,
            "priority_score": priority_score,
            "strategic_weight": 8,
            "is_critical": impact_level == "critical"
        },
        "display_rules": {
            "headline": impact_summary.get("headline", ""),
            "badge": "Review" if status in ("warning", "partial") else "Healthy",
            "sort_order": priority_score,
            "collapse_by_default": status == "success",
            "pin_to_top_when": ["critical", "failed", "warning"]
        },
        "review_state": {
            "needs_review": bool(activity_summary.get("needs_review", False)),
            "needs_approval": False,
            "has_warnings": bool(activity_summary.get("warnings_list")),
            "has_errors": bool(activity_summary.get("errors_list"))
        },
        "notes": {
            "dashboard_note": "Shows top listing health, AI recovery attempts, and expected business protection.",
            "developer_note": "Future-module compatible top listing monitor with shared listing recovery routing.",
            "migration_note": "Legacy top_listing_status.json remains available."
        }
    }


def update_report_registry(entry):
    registry = load_json(REPORT_REGISTRY_FILE, {
        "schema_type": "report_registry",
        "schema_version": "1.0",
        "generated_at": "",
        "entries": []
    })
    entries = [item for item in registry.get("entries", []) if item.get("feature_key") != FEATURE_KEY]
    entries.append(entry)
    registry["generated_at"] = datetime.now().isoformat()
    registry["entries"] = sorted(entries, key=lambda x: x.get("importance", {}).get("priority_score", 0), reverse=True)
    with open(REPORT_REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)


def save_new_standard_outputs(snapshot, history_file, started_at, duration_sec, input_sources):
    ts = started_at.strftime("%Y%m%d_%H%M%S")
    impact_history_file = os.path.join(JSON_DIR, f"impact_{FEATURE_KEY}_{ts}.json")
    activity_history_file = os.path.join(JSON_DIR, f"activity_{FEATURE_KEY}_{ts}.json")
    impact_summary = build_impact_summary(snapshot, history_file)
    with open(IMPACT_LATEST_FILE, "w", encoding="utf-8") as f:
        json.dump(impact_summary, f, indent=2, ensure_ascii=False)
    with open(impact_history_file, "w", encoding="utf-8") as f:
        json.dump(impact_summary, f, indent=2, ensure_ascii=False)
    activity_summary = build_activity_summary(snapshot, history_file, impact_history_file, started_at, duration_sec, input_sources)
    with open(ACTIVITY_LATEST_FILE, "w", encoding="utf-8") as f:
        json.dump(activity_summary, f, indent=2, ensure_ascii=False)
    with open(activity_history_file, "w", encoding="utf-8") as f:
        json.dump(activity_summary, f, indent=2, ensure_ascii=False)
    update_report_registry(build_registry_entry(impact_summary, activity_summary, history_file))


def main():
    started_at = datetime.now()
    parser = argparse.ArgumentParser(description="Top Listing Monitor")
    parser.add_argument("--top", type=int, default=20, help="Check top N sellers (default: 20)")
    args = parser.parse_args()

    print("=" * 55)
    print("  Grow24 AI - Top Listing Monitor v1.1")
    print(f"  {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print(f"  Checking top {args.top} sellers")
    print("=" * 55)

    top, input_sources = get_top_sellers(args.top)
    if not top:
        print("  No ad data found. Run data import first.")
        return 1

    print(f"\n  Checking {len(top)} top sellers...")
    results = []
    active = 0
    inactive = []
    warnings = []
    run_errors = []

    for i, item in enumerate(top):
        sku = item["sku"]
        if not sku:
            continue
        status = check_listing_status(sku)
        status["weekly_sales"] = item["sales"]
        status["weekly_orders"] = item["orders"]
        status["action_priority"] = "HIGH" if status["status"] in ("NOT ACTIVE", "NOT SEARCHABLE") else "LOW"
        status["recommendation"] = "Start listing recovery workflow" if status["status"] in ("NOT ACTIVE", "NOT SEARCHABLE") else "Healthy"
        status["signals"] = [status["status"], *(issue.get("message", "") for issue in status.get("issues", [])[:2])]
        results.append(status)

        if status["status"] == "ACTIVE":
            active += 1
        elif status["status"] == "NOT ACTIVE":
            inactive.append(status)
        elif status["status"] == "NOT SEARCHABLE":
            warnings.append(status)
        elif status["status"] == "API ERROR":
            run_errors.append(status.get("error", "API ERROR"))

        if (i + 1) % 10 == 0:
            print(f"    Checked {i+1}/{len(top)}...")
        time.sleep(0.5)

    legacy_payload = {
        "timestamp": datetime.now().isoformat(),
        "total": len(results),
        "active": active,
        "inactive": len(inactive),
        "warnings": len(warnings),
        "results": results,
        "inactive_details": inactive,
    }
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(legacy_payload, f, indent=2, ensure_ascii=False)

    route_payload, route_history_file = build_listing_route_requests(results, started_at)
    route_result, route_result_history_file = execute_listing_routes(route_payload, route_history_file, started_at)
    route_result["request_file"] = relative_path(LISTING_ROUTE_REQUEST_FILE)
    route_result["request_history_file"] = relative_path(route_history_file)
    route_result["result_file"] = relative_path(LISTING_ROUTE_RESULT_FILE)
    route_result["result_history_file"] = relative_path(route_result_history_file)

    snapshot = dict(legacy_payload)
    snapshot["run_errors"] = run_errors
    snapshot["action_routing"] = summarize_action_routes([route_result])
    history_file = os.path.join(JSON_DIR, f"top_listing_status_{started_at.strftime('%Y%m%d_%H%M%S')}.json")
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    save_new_standard_outputs(snapshot, history_file, started_at, time.time() - started_at.timestamp(), input_sources)

    if inactive:
        send_alert_email(inactive)

    print(f"\n  Active:             {active}")
    print(f"  NOT Active:         {len(inactive)}")
    print(f"  NOT Searchable:     {len(warnings)}")
    print(f"  Recovery Routes:    {route_result.get('request_count', 0)}")
    print(f"  Routing Status:     {snapshot['action_routing'].get('status', 'skipped')}")
    print(f"  Saved legacy:       {STATUS_FILE}")
    return 1 if inactive else 0


if __name__ == "__main__":
    sys.exit(main())
