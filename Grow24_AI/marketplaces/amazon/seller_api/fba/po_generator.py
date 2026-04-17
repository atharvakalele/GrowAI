#!/usr/bin/env python3
"""
FBA PO Generator — Grow24 AI
==============================
Steps 14-15 + Google Sheet PO + Google Drive upload.

  STEP 14: getLabels          → download barcode labels PDF → upload to Drive
  STEP 15: getDeliveryChallan → download delivery challan PDF → upload to Drive

  POST: Write Purchase Order to Google Sheet
        Auto-creates tab: "FBA PO 1", "FBA PO 2", ...

─── PO COLUMNS (editable here OR via dashboard menu) ────────────────────────
    This list controls what goes into the Google Sheet PO tab.
    Column order = sheet column order.
    Editable from: Dashboard → FBA Settings → PO Columns
    Supported values: SKU, Quantity, Box Count, Date, Status, Notes,
                      ASIN, Product Name, Category, Units Per Box,
                      Box Size (cm), Box Weight (kg), Warehouse,
                      Appointment Slot, Shipment ID
─────────────────────────────────────────────────────────────────────────────
"""

import base64
import json
import os
import ssl
import time
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

PROJECT_ROOT = Path(__file__).resolve().parents[4]
FBA_CONFIG   = PROJECT_ROOT / "config" / "fba_config.json"
FBA_API_VER  = "2024-03-20"
FBA_BASE     = f"/inbound/v{FBA_API_VER}"

# Labels stored locally as backup before Drive upload
LABELS_DIR = PROJECT_ROOT / "output" / "fba_labels"
LABELS_DIR.mkdir(parents=True, exist_ok=True)

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from auth import sp_get, get_token

try:
    import certifi
    _SSL = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL = ssl.create_default_context()

SP_ENDPOINT = "https://sellingpartnerapi-eu.amazon.com"

# ─────────────────────────────────────────────────────────────────────────────
# PO COLUMNS DEFINITION
# Edit this list to control which columns appear in the Google Sheet PO tab.
# Order of this list = column order in sheet.
# Load from config (so dashboard changes take effect); fallback to this default.
# ─────────────────────────────────────────────────────────────────────────────
_DEFAULT_PO_COLUMNS = ["SKU", "Quantity", "Box Count", "Date", "Status", "Notes"]


def _load_config() -> dict:
    with open(FBA_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def get_po_columns() -> list[str]:
    """
    Load PO columns from fba_config.json.
    Falls back to _DEFAULT_PO_COLUMNS if not configured.
    """
    try:
        cfg = _load_config()
        cols = cfg.get("po_columns", [])
        if isinstance(cols, list) and cols:
            return cols
    except Exception:
        pass
    return _DEFAULT_PO_COLUMNS.copy()


def _retry(func, *args, **kwargs):
    """Retry with exponential backoff from config."""
    cfg     = _load_config()
    retries = cfg["retry"]["max_attempts"]
    delay_s = cfg["retry"]["delay_seconds"]
    mult    = cfg["retry"]["backoff_multiplier"]
    for attempt in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt < retries - 1:
                wait = delay_s * (mult ** attempt)
                print(f"    [RETRY {attempt+1}/{retries}] {e} — wait {wait}s")
                time.sleep(wait)
            else:
                raise


# ─────────────────────────────────────────────────────────────────────────────
# GOOGLE DRIVE UPLOAD
# Uses DriveUpload.gs (googledrv.gs.txt) POST endpoint.
# ─────────────────────────────────────────────────────────────────────────────

def _upload_to_drive(file_bytes: bytes, filename: str,
                     mime_type: str, folder: list[str]) -> dict:
    """
    Upload file to Google Drive via DriveUpload.gs POST webhook.

    Returns: {"ok": bool, "link": str, "fileId": str}
    """
    cfg = _load_config()
    drive_cfg = cfg.get("google_drive", {})
    webhook   = drive_cfg.get("webhook_url", "")
    secret    = drive_cfg.get("secret", "MagicalDream")

    if not webhook:
        print("  [WARN] Drive webhook URL not configured — skipping Drive upload")
        return {"ok": False, "link": "", "fileId": ""}

    payload = {
        "secret":   secret,
        "base64":   base64.b64encode(file_bytes).decode(),
        "filename": filename,
        "mimeType": mime_type,
        "folder":   folder,
    }
    data = json.dumps(payload).encode()
    req  = Request(webhook, data=data, headers={"Content-Type": "application/json"})
    try:
        resp   = urlopen(req, context=_SSL, timeout=30)
        result = json.loads(resp.read().decode())
        if result.get("ok"):
            print(f"    [DRIVE] Uploaded: {filename} → {result.get('link','')[:60]}")
        else:
            print(f"    [DRIVE ERROR] {result.get('error', 'unknown')}")
        return result
    except Exception as e:
        print(f"    [DRIVE ERROR] Upload failed: {e}")
        return {"ok": False, "link": "", "fileId": ""}


def _save_local_backup(file_bytes: bytes, save_path: Path) -> bool:
    """Save file locally as backup."""
    try:
        with open(save_path, "wb") as f:
            f.write(file_bytes)
        return True
    except Exception as e:
        print(f"    [WARN] Local backup failed: {e}")
        return False


# ─────────────────────────────────────────────────────────────────────────────
# STEP 14: Labels
# ─────────────────────────────────────────────────────────────────────────────

def get_labels(plan_id: str, shipment_id: str,
               page_type: str = "PackageLabel_Plain_Paper") -> dict:
    """
    STEP 14: Download labels PDF → save locally → upload to Drive.

    Returns: {"success": bool, "local_path": str, "drive_link": str}
    """
    print(f"\n  [STEP 14] Getting labels for: {shipment_id}")
    cfg = _load_config()
    drive_cfg = cfg.get("google_drive", {})
    folder    = drive_cfg.get("labels_folder", ["Grow24 AI", "FBA Labels"])

    params = {
        "inboundPlanId": plan_id,
        "shipmentId":    shipment_id,
        "pageType":      page_type,
        "labelType":     "BARCODE_2D",
    }

    result = {"success": False, "local_path": "", "drive_link": ""}

    try:
        url = f"{SP_ENDPOINT}{FBA_BASE}/labels?" + urlencode(params)
        req = Request(url, headers={
            "x-amz-access-token": get_token(),
            "Content-Type":       "application/json",
        })
        resp = urlopen(req, context=_SSL, timeout=30)
        data = json.loads(resp.read().decode())

        # Extract PDF bytes
        pdf_bytes = None
        content_b64 = data.get("content", "")
        if content_b64:
            pdf_bytes = base64.b64decode(content_b64)
        else:
            # Try download URL
            pdf_url = data.get("downloadURL", data.get("labelURL", ""))
            if pdf_url:
                r2 = urlopen(Request(pdf_url, headers={
                    "x-amz-access-token": get_token()
                }), context=_SSL, timeout=30)
                pdf_bytes = r2.read()

        if not pdf_bytes:
            print(f"    [WARN] No label content in response: {list(data.keys())}")
            return result

        ts        = datetime.now().strftime("%Y%m%d_%H%M")
        filename  = f"labels_{shipment_id}_{ts}.pdf"
        save_path = LABELS_DIR / filename

        # Save locally
        _save_local_backup(pdf_bytes, save_path)
        result["local_path"] = str(save_path)
        print(f"    [OK] Labels saved locally: {filename} ({len(pdf_bytes)//1024} KB)")

        # Upload to Drive
        drive_result = _upload_to_drive(pdf_bytes, filename, "application/pdf", folder)
        result["drive_link"] = drive_result.get("link", "")
        result["success"]    = True

    except Exception as e:
        print(f"    [ERROR] get_labels: {e}")

    return result


# ─────────────────────────────────────────────────────────────────────────────
# STEP 15: Delivery Challan
# ─────────────────────────────────────────────────────────────────────────────

def get_delivery_challan(plan_id: str, shipment_id: str) -> dict:
    """
    STEP 15: Download delivery challan PDF → save locally → upload to Drive.

    India-specific: Must accompany shipment to Amazon warehouse.

    Returns: {"success": bool, "local_path": str, "drive_link": str}
    """
    print(f"\n  [STEP 15] Getting delivery challan for: {shipment_id}")
    cfg = _load_config()
    drive_cfg = cfg.get("google_drive", {})
    folder    = drive_cfg.get("challans_folder", ["Grow24 AI", "FBA Challans"])

    params = {
        "inboundPlanId": plan_id,
        "shipmentId":    shipment_id,
    }
    result = {"success": False, "local_path": "", "drive_link": ""}

    try:
        url = f"{SP_ENDPOINT}{FBA_BASE}/deliveryChallan?" + urlencode(params)
        req = Request(url, headers={
            "x-amz-access-token": get_token(),
            "Content-Type":       "application/json",
        })
        resp = urlopen(req, context=_SSL, timeout=30)
        data = json.loads(resp.read().decode())

        pdf_bytes    = None
        content_b64  = data.get("content", "")
        if content_b64:
            pdf_bytes = base64.b64decode(content_b64)
        else:
            pdf_url = data.get("downloadURL", data.get("challanURL", ""))
            if pdf_url:
                r2 = urlopen(Request(pdf_url, headers={
                    "x-amz-access-token": get_token()
                }), context=_SSL, timeout=30)
                pdf_bytes = r2.read()

        if not pdf_bytes:
            print(f"    [WARN] No challan content: {list(data.keys())}")
            return result

        ts        = datetime.now().strftime("%Y%m%d_%H%M")
        filename  = f"challan_{shipment_id}_{ts}.pdf"
        save_path = LABELS_DIR / filename

        _save_local_backup(pdf_bytes, save_path)
        result["local_path"] = str(save_path)
        print(f"    [OK] Challan saved locally: {filename} ({len(pdf_bytes)//1024} KB)")

        drive_result = _upload_to_drive(pdf_bytes, filename, "application/pdf", folder)
        result["drive_link"] = drive_result.get("link", "")
        result["success"]    = True

    except Exception as e:
        print(f"    [ERROR] get_delivery_challan: {e}")

    return result


def generate_all_documents(plan_id: str, shipment_ids: list[str]) -> dict:
    """
    Generate labels + challan for all shipments (Steps 14-15).
    Returns: {shipment_id: {"labels": {...}, "challan": {...}}}
    """
    print(f"\n  [DOCUMENTS] Labels + Challans for {len(shipment_ids)} shipment(s)...")
    results = {}
    for sid in shipment_ids:
        print(f"\n  --- Shipment: {sid} ---")
        labels  = _retry(get_labels, plan_id, sid)
        challan = _retry(get_delivery_challan, plan_id, sid)
        results[sid] = {"labels": labels, "challan": challan}
        if len(shipment_ids) > 1:
            time.sleep(1)

    ok_labels   = sum(1 for r in results.values() if r["labels"]["success"])
    ok_challans = sum(1 for r in results.values() if r["challan"]["success"])
    print(f"\n  [DOCUMENTS] Labels: {ok_labels}/{len(shipment_ids)} | "
          f"Challans: {ok_challans}/{len(shipment_ids)}")
    print(f"  [DOCUMENTS] Local backup: {LABELS_DIR}")
    return results


# ─────────────────────────────────────────────────────────────────────────────
# GOOGLE SHEET PO WRITER
# ─────────────────────────────────────────────────────────────────────────────

def _get_sheet_webhook() -> str:
    root_config = PROJECT_ROOT.parent / "config_google_sheet.json"
    try:
        with open(root_config, "r", encoding="utf-8") as f:
            return json.load(f).get("webhook_url", "")
    except Exception:
        return ""


def _gas_get(params: dict) -> dict:
    """Call GAS sheet webhook (GET-based, webhook_v4.gs)."""
    webhook = _get_sheet_webhook()
    if not webhook:
        raise RuntimeError("GAS sheet webhook URL not configured")
    params["secret"] = "MagicalDream"
    url  = webhook + "?" + urlencode(params)
    resp = urlopen(Request(url), context=_SSL, timeout=20)
    return json.loads(resp.read().decode())


def _get_existing_po_tabs(sheet_id: str) -> list[str]:
    """List existing tab names from Google Sheet."""
    try:
        data = _gas_get({"action": "list", "sheet": sheet_id})
        return data.get("tabs", [])
    except Exception as e:
        print(f"  [WARN] Could not list tabs: {e}")
        return []


def _next_po_tab_name(existing_tabs: list[str], prefix: str) -> str:
    """Find next available 'FBA PO N' tab name."""
    used = set()
    for t in existing_tabs:
        if t.startswith(prefix + " "):
            try:
                used.add(int(t[len(prefix)+1:].strip()))
            except ValueError:
                pass
    n = 1
    while n in used:
        n += 1
    return f"{prefix} {n}"


def _create_tab_with_headers(sheet_id: str, tab_name: str, headers: list[str]) -> bool:
    """Create new tab + write header row via GAS exec action."""
    try:
        # Create tab using exec action
        code = f"ss.insertSheet('{tab_name}')"
        _gas_get({"action": "exec", "sheet": sheet_id, "code": code})

        # Write header row to A1
        header_json = json.dumps([headers])
        _gas_get({
            "action": "write",
            "sheet":  sheet_id,
            "tab":    tab_name,
            "range":  "A1",
            "values": header_json,
        })
        return True
    except Exception as e:
        print(f"  [ERROR] Create tab '{tab_name}': {e}")
        return False


def _append_rows(sheet_id: str, tab_name: str, rows: list[list]) -> bool:
    """Append data rows to existing tab (after header)."""
    try:
        # Get last row via exec
        result = _gas_get({
            "action": "exec",
            "sheet":  sheet_id,
            "tab":    tab_name,
            "code":   "tab.getLastRow()",
        })
        last_row = int(result.get("result", "1"))
        start    = last_row + 1

        rows_json = json.dumps(rows)
        _gas_get({
            "action": "write",
            "sheet":  sheet_id,
            "tab":    tab_name,
            "range":  f"A{start}",
            "values": rows_json,
        })
        return True
    except Exception as e:
        print(f"  [ERROR] Append rows to '{tab_name}': {e}")
        return False


# ── Column value mapping ──────────────────────────────────────────────────────
# Maps column names → field in po_item dict.
# Add more columns here if needed.
_COL_MAP = {
    "SKU":              "sku",
    "Quantity":         "send_qty",
    "Box Count":        "box_count",
    "Date":             "date",
    "Status":           "status",
    "Notes":            "notes",
    "ASIN":             "asin",
    "Product Name":     "product_name",
    "Category":         "category",
    "Units Per Box":    "units_per_box",
    "Box Size (cm)":    "box_size",
    "Box Weight (kg)":  "box_weight_kg",
    "Warehouse":        "warehouse",
    "Appointment Slot": "appointment_slot",
    "Shipment ID":      "shipment_id",
}


def write_po_to_sheet(po_items: list[dict], appointment_results: list[dict],
                      doc_results: dict) -> dict:
    """
    Write Purchase Order to Google Sheet.

    Columns loaded from fba_config.json → po_columns (editable from dashboard).
    Creates new tab "FBA PO N" auto-incremented.

    Args:
        po_items:            list of item dicts (one per SKU)
        appointment_results: list of booking results from appointment_booker
        doc_results:         dict {shipment_id: {labels, challan}} from po_generator

    Returns: {"success": bool, "tab_name": str, "rows_written": int}
    """
    cfg        = _load_config()
    sheet_cfg  = cfg["google_sheet"]
    sheet_id   = sheet_cfg.get("sheet_id", "")
    po_prefix  = sheet_cfg.get("po_tab_prefix", "FBA PO")
    po_columns = get_po_columns()

    print(f"\n  [PO] Writing PO to Google Sheet...")
    print(f"       Columns: {po_columns}")

    if not sheet_id:
        print("  [ERROR] google_sheet.sheet_id not configured in fba_config.json")
        return {"success": False, "tab_name": "", "rows_written": 0}

    # Build appointment + drive link lookups
    appt_lookup = {r["shipment_id"]: r for r in appointment_results if r.get("shipment_id")}
    drive_labels = {sid: r["labels"].get("drive_link","") for sid, r in doc_results.items()}

    # Find next PO tab name
    existing_tabs = _get_existing_po_tabs(sheet_id)
    tab_name      = _next_po_tab_name(existing_tabs, po_prefix)
    print(f"  [PO] Creating tab: {tab_name}")

    # Create tab with headers
    created = _create_tab_with_headers(sheet_id, tab_name, po_columns)
    if not created:
        return {"success": False, "tab_name": tab_name, "rows_written": 0}

    # Build rows
    today = datetime.now().strftime("%Y-%m-%d")
    rows  = []

    for item in po_items:
        sid    = item.get("shipment_id", "")
        appt   = appt_lookup.get(sid, {})

        # Format appointment slot
        appt_time = appt.get("slot_time", "")
        if appt_time:
            try:
                dt = datetime.fromisoformat(appt_time.replace("Z", "+00:00"))
                appt_disp = dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                appt_disp = appt_time
        else:
            appt_disp = ""

        # Box size string
        box_size = (f"{item.get('box_length_cm','')}×"
                    f"{item.get('box_width_cm','')}×"
                    f"{item.get('box_height_cm','')} cm")

        # Drive links for notes
        label_link  = drive_labels.get(sid, "")
        notes_extra = f"Labels: {label_link}" if label_link else ""
        existing_notes = item.get("notes", "")
        final_notes = f"{existing_notes} | {notes_extra}".strip(" |") if notes_extra else existing_notes

        # Flat dict for column mapping
        flat = {
            "sku":              item.get("sku", ""),
            "send_qty":         item.get("send_qty", 0),
            "box_count":        item.get("box_count", 0),
            "date":             item.get("date", today),
            "status":           item.get("status", "Pending"),
            "notes":            final_notes,
            "asin":             item.get("asin", ""),
            "product_name":     item.get("product_name", "")[:80],
            "category":         item.get("category", ""),
            "units_per_box":    item.get("units_per_box", 0),
            "box_size":         box_size,
            "box_weight_kg":    item.get("box_weight_kg", 0),
            "warehouse":        item.get("warehouse", "DED3"),
            "appointment_slot": appt_disp,
            "shipment_id":      sid,
        }

        # Build ordered row from selected columns
        row = [flat.get(_COL_MAP.get(col, ""), "") for col in po_columns]
        rows.append(row)

    # Write rows
    success = False
    if rows:
        success = _append_rows(sheet_id, tab_name, rows)
        if success:
            print(f"  [PO] {len(rows)} rows written to '{tab_name}'")
        else:
            print(f"  [PO ERROR] Failed to write rows")
    else:
        print("  [PO WARN] No rows to write")
        success = True

    po_num = int(tab_name.split(po_prefix)[1].strip()) if po_prefix in tab_name else 0
    return {
        "success":      success,
        "tab_name":     tab_name,
        "po_number":    po_num,
        "rows_written": len(rows),
    }
