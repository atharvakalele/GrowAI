#!/usr/bin/env python3
"""
FBA Quantity Predictor — Grow24 AI
=====================================
Decides how many units to send per ASIN based on:
  - Current FBA stock (from existing stock_monitor data)
  - Last 7 day sales (FBA + FBM combined, per ASIN)
  - Target days coverage (default: 15 days)

Logic:
  avg_daily_sales   = last_7_days_sales / 7
  required_stock    = avg_daily_sales * target_days
  send_quantity     = required_stock - current_fba_stock
  if send_quantity < min_send_quantity → skip

Data sources (reuse existing prototype data if fresh):
  FBA stock  : ClaudeCode/Report/[latest]/Json/stock_status.json
  Sales data : ClaudeCode/Report/[latest]/Json/sp_advertisedproduct_daily.json
               OR sp_purchasedproduct_daily.json
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta

PROJECT_ROOT  = Path(__file__).resolve().parents[4]
PROTOTYPE_DIR = PROJECT_ROOT.parent / "ClaudeCode" / "Report"
FBA_CONFIG    = PROJECT_ROOT / "config" / "fba_config.json"


def _load_config() -> dict:
    with open(FBA_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def _find_latest_report_dir() -> Path | None:
    """Find latest report folder from prototype system."""
    if not PROTOTYPE_DIR.exists():
        return None
    folders = [f for f in PROTOTYPE_DIR.iterdir() if f.is_dir()]
    if not folders:
        return None
    return max(folders, key=lambda f: f.stat().st_mtime)


def _is_data_fresh(file_path: Path, max_hours: int = 4) -> bool:
    """Check if a data file is recent enough to reuse."""
    if not file_path.exists():
        return False
    age_hours = (datetime.now().timestamp() - file_path.stat().st_mtime) / 3600
    return age_hours < max_hours


def get_current_fba_stock() -> dict[str, int]:
    """
    Returns {asin: fba_stock_qty} from existing stock data.
    If data is stale (>4hr), logs warning — caller should trigger fresh import.
    """
    report_dir = _find_latest_report_dir()
    if not report_dir:
        print("  [WARN] No report folder found — stock data unavailable")
        return {}

    stock_file = report_dir / "Json" / "stock_status.json"

    if not _is_data_fresh(stock_file, max_hours=4):
        print("  [WARN] Stock data is stale (>4hr) — trigger stock_monitor_v1.1.py for fresh data")

    if not stock_file.exists():
        print("  [WARN] stock_status.json not found")
        return {}

    try:
        with open(stock_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        stock_map = {}

        # Combine all stock levels per ASIN (FBA only)
        all_products = (
            data.get("healthy", []) +
            data.get("low_stock", []) +
            data.get("zero_stock", [])
        )
        for item in all_products:
            asin = item.get("asin", "")
            # Use FBA qty if available, else total
            qty = item.get("fba_qty", item.get("quantity", 0))
            if asin:
                stock_map[asin] = int(qty)

        print(f"  [OK] Stock data: {len(stock_map)} ASINs loaded")
        return stock_map

    except Exception as e:
        print(f"  [ERROR] Could not load stock data: {e}")
        return {}


def get_sales_last_7days() -> dict[str, float]:
    """
    Returns {asin: total_units_sold_last_7_days}
    Combines FBA + FBM sales (all channels per ASIN).
    Uses sp_advertisedproduct_daily or sp_purchasedproduct_daily.
    """
    report_dir = _find_latest_report_dir()
    if not report_dir:
        return {}

    json_dir = report_dir / "Json"

    # Try purchased product data first (more accurate for total sales)
    sales_file = json_dir / "sp_purchasedproduct_daily.json"
    if not sales_file.exists():
        sales_file = json_dir / "sp_advertisedproduct_daily.json"

    if not _is_data_fresh(sales_file, max_hours=4):
        print("  [WARN] Sales data is stale (>4hr) — trigger sp_ads_complete_import for fresh data")

    if not sales_file.exists():
        print("  [WARN] Sales data file not found")
        return {}

    try:
        with open(sales_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Aggregate by ASIN across 7 days
        asin_sales: dict[str, float] = {}
        cutoff = datetime.now() - timedelta(days=7)

        for record in data:
            asin = record.get("advertisedAsin") or record.get("asin", "")
            if not asin:
                continue

            # Check date if available
            date_str = record.get("date", "")
            if date_str:
                try:
                    record_date = datetime.strptime(date_str, "%Y-%m-%d")
                    if record_date < cutoff:
                        continue
                except ValueError:
                    pass

            units = (
                record.get("unitsSoldClicks14d", 0) or
                record.get("unitsSoldSameSKU14d", 0) or
                record.get("sales7d", 0) or
                record.get("units_sold", 0) or 0
            )
            asin_sales[asin] = asin_sales.get(asin, 0) + float(units)

        print(f"  [OK] Sales data: {len(asin_sales)} ASINs with sales")
        return asin_sales

    except Exception as e:
        print(f"  [ERROR] Could not load sales data: {e}")
        return {}


def predict_all(fba_sku_asin_map: dict[str, str]) -> list[dict]:
    """
    Main predictor. For each FBA SKU:
      1. Get ASIN-level stock + sales
      2. Calculate send quantity
      3. Return list of {sku, asin, current_stock, avg_daily_sales, send_qty} for qty > 0

    Args:
        fba_sku_asin_map: {sku: asin} — only FBA SKUs
    """
    cfg = _load_config()
    target_days     = cfg["quantity_predictor"]["target_days"]
    min_send_qty    = cfg["quantity_predictor"]["min_send_quantity"]

    stock_map = get_current_fba_stock()
    sales_map = get_sales_last_7days()

    results = []
    skipped = []

    for sku, asin in fba_sku_asin_map.items():
        current_stock  = stock_map.get(asin, 0)
        total_7d_sales = sales_map.get(asin, 0)
        avg_daily      = total_7d_sales / 7

        required_stock = avg_daily * target_days
        send_qty       = required_stock - current_stock

        if send_qty < min_send_qty:
            skipped.append({
                "sku": sku, "asin": asin,
                "reason": f"send_qty={send_qty:.0f} < min={min_send_qty} OR stock sufficient",
                "current_stock": current_stock,
            })
            continue

        results.append({
            "sku":           sku,
            "asin":          asin,
            "current_stock": current_stock,
            "sales_7d":      round(total_7d_sales, 1),
            "avg_daily":     round(avg_daily, 2),
            "required_stock": round(required_stock, 0),
            "send_qty":      int(send_qty),
        })

    print(f"\n  [PREDICTOR] {len(results)} SKUs need replenishment | {len(skipped)} skipped (sufficient stock)")
    for s in skipped[:5]:
        print(f"    SKIP: {s['sku']} — {s['reason']}")

    return results
