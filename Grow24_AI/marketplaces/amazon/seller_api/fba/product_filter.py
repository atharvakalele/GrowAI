#!/usr/bin/env python3
"""
FBA Product Filter — Grow24 AI
================================
Controls which SKUs go to FBA shipment, and calculates box configuration.

Detection Priority (configurable in fba_config.json → category_detection.priority):
  1. product_override  — Per-product override defined in menu (SKU or ASIN key)
  2. sp_api_category   — Category from SP-API Catalog Items API
  3. title_keyword     — Keyword match in product title
  4. default           — Default category from config

Keyword Match Mode (configurable):
  AND_WITHIN_GROUP  → each group is a list; ALL words in group must be in title
                      groups are OR'd: any group can match
  OR_ANY            → any single keyword match is enough (legacy flat-list mode)

Example detect_keywords with AND_WITHIN_GROUP:
  [["celtic", "salt"], ["himalayan", "salt"], ["namak"]]
  → title with "celtic salt" → match (both in group 1)
  → title with "himalayan" alone → NO match (missing "salt")
  → title with "namak" → match (single-word group 3)
"""

import json
import math
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]
FBA_CONFIG   = PROJECT_ROOT / "config" / "fba_config.json"

try:
    import certifi, ssl
    _SSL = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    import ssl
    _SSL = ssl.create_default_context()

from urllib.request import Request, urlopen
from urllib.parse import urlencode


def _load_config() -> dict:
    with open(FBA_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_webhook_url() -> str:
    root_config = PROJECT_ROOT.parent / "config_google_sheet.json"
    try:
        with open(root_config, "r", encoding="utf-8") as f:
            return json.load(f).get("webhook_url", "")
    except Exception:
        return ""


# ─────────────────────────────────────────────────────────────────────────────
# FILTER: Which SKUs to include/exclude
# ─────────────────────────────────────────────────────────────────────────────

def get_filter_list_from_sheet() -> list[str]:
    """Fetch SKU include/exclude list from Google Sheet via GAS webhook."""
    cfg       = _load_config()
    sheet_cfg = cfg["google_sheet"]
    webhook   = _get_webhook_url()

    if not webhook or not sheet_cfg.get("sheet_id"):
        print("  [WARN] Google Sheet not configured — filter disabled")
        return []

    try:
        params = urlencode({
            "action": "read",
            "secret": "MagicalDream",
            "sheet":  sheet_cfg["sheet_id"],
            "tab":    sheet_cfg["filter_tab"],
        })
        resp = urlopen(Request(f"{webhook}?{params}"), context=_SSL, timeout=15)
        data = json.loads(resp.read().decode())

        # Extract first column values (SKU column)
        values = data.get("values", [])
        skus = []
        for row in values:
            if row and str(row[0]).strip():
                skus.append(str(row[0]).strip())

        print(f"  [OK] Filter list: {len(skus)} SKUs from sheet ({sheet_cfg['filter_tab']})")
        return skus
    except Exception as e:
        print(f"  [ERROR] Could not fetch filter list: {e}")
        return []


def apply_filter(all_skus: list[str]) -> list[str]:
    """Apply INCLUDE/EXCLUDE/NONE filter. Returns SKUs to process."""
    cfg  = _load_config()
    mode = cfg["filter"]["mode"].upper()

    if mode == "NONE":
        print(f"  [FILTER] Mode=NONE — processing all {len(all_skus)} SKUs")
        return all_skus

    filter_list = get_filter_list_from_sheet()

    if not filter_list:
        print("  [INFO] Empty filter list — processing ALL SKUs")
        return all_skus

    if mode == "INCLUDE":
        result = [s for s in all_skus if s in filter_list]
        print(f"  [INCLUDE] {len(result)}/{len(all_skus)} SKUs pass filter")
    else:  # EXCLUDE
        result = [s for s in all_skus if s not in filter_list]
        print(f"  [EXCLUDE] {len(result)}/{len(all_skus)} SKUs pass filter")

    return result


# ─────────────────────────────────────────────────────────────────────────────
# CATEGORY DETECTION — 4-level priority
# ─────────────────────────────────────────────────────────────────────────────

def _keyword_match(title: str, keywords_config: list, match_mode: str) -> bool:
    """
    Test if title matches keywords using the configured match mode.

    keywords_config formats supported:
      Flat list:   ["salt", "namak", "mineral"]    → OR: any word matches
      Nested list: [["celtic","salt"], "namak"]     → AND within each group, OR across groups

    match_mode:
      "AND_WITHIN_GROUP" — nested: all words in a sub-list must be in title
      "OR_ANY"           — any single word is enough
    """
    title_l = title.lower()

    for kw in keywords_config:
        if isinstance(kw, list):
            # AND group: ALL words in this sub-list must appear
            if all(word.lower() in title_l for word in kw):
                return True
        else:
            # Single keyword
            if str(kw).lower() in title_l:
                return True

    return False


def _match_category_by_text(text: str, categories: dict, match_mode: str, skip_keys: set) -> str | None:
    """Return category key if any keyword group matches, else None."""
    for cat_key, cat_cfg in categories.items():
        if cat_key in skip_keys:
            continue
        kws = cat_cfg.get("detect_keywords", [])
        if kws and _keyword_match(text, kws, match_mode):
            return cat_key
    return None


def get_product_override(sku: str, asin: str = "") -> dict | None:
    """
    Check product_overrides in config for a per-product box config.
    Checks by SKU first, then by ASIN.

    Returns override dict or None.
    """
    cfg       = _load_config()
    overrides = cfg.get("product_overrides", {})

    # Remove meta keys
    skip = {"_comment", "_example"}

    # Check by SKU
    if sku and sku in overrides and sku not in skip:
        return overrides[sku]

    # Check by ASIN
    if asin and asin in overrides and asin not in skip:
        return overrides[asin]

    # Check if any override entry has matching sku field
    if sku:
        for key, val in overrides.items():
            if key in skip:
                continue
            if isinstance(val, dict) and val.get("sku") == sku:
                return val

    return None


def detect_category(product_title: str, api_category: str = "",
                    sku: str = "", asin: str = "") -> str:
    """
    Detect box category using 4-level priority:
      1. product_override (per-SKU/ASIN menu config)
      2. SP-API catalog category text match
      3. Product title keyword match (AND_WITHIN_GROUP mode)
      4. Default category

    Returns: category key (e.g. "ayurved" or "salt")
    """
    cfg        = _load_config()
    categories = cfg["box_categories"]
    det_cfg    = cfg["category_detection"]
    default    = det_cfg["default_category"]
    mode       = det_cfg.get("keyword_match_mode", "AND_WITHIN_GROUP")
    priority   = det_cfg.get("priority", ["product_override", "sp_api_category", "title_keyword", "default"])
    skip_keys  = {"_comment", "_listing_detection", "_example"}

    for step in priority:

        # ── Priority 1: Product override ──────────────────────────────────────
        if step == "product_override" and (sku or asin):
            ov = get_product_override(sku, asin)
            if ov:
                cat = ov.get("category", "")
                if cat and cat in categories:
                    print(f"    [DETECT] '{sku or asin}' → product_override → {cat}")
                    return cat

        # ── Priority 2: SP-API catalog category ───────────────────────────────
        elif step == "sp_api_category" and api_category:
            cat = _match_category_by_text(api_category, categories, mode, skip_keys)
            if cat:
                print(f"    [DETECT] '{product_title[:30]}' → sp_api_category → {cat}")
                return cat

        # ── Priority 3: Title keyword match ───────────────────────────────────
        elif step == "title_keyword" and product_title:
            cat = _match_category_by_text(product_title, categories, mode, skip_keys)
            if cat:
                print(f"    [DETECT] '{product_title[:30]}' → title_keyword ({mode}) → {cat}")
                return cat

        # ── Priority 4: Default ───────────────────────────────────────────────
        elif step == "default":
            print(f"    [DETECT] '{product_title[:30]}' → default → {default}")
            return default

    return default


def get_box_config(category: str, sku: str = "", asin: str = "") -> dict:
    """
    Returns box configuration for a product.

    Priority:
      1. product_override (complete custom config per SKU/ASIN)
      2. box_categories[category] from config

    Returns dict with all fields needed for FBA API:
      category, length_cm, width_cm, height_cm, units_per_box, box_weight_kg
    """
    cfg = _load_config()

    # ── Check product override first ──────────────────────────────────────────
    if sku or asin:
        ov = get_product_override(sku, asin)
        if ov and all(k in ov for k in ("length_cm", "width_cm", "height_cm", "weight_kg", "units_per_box")):
            print(f"    [BOX] {sku or asin}: using product_override config")
            return {
                "category":      ov.get("category", category),
                "length_cm":     ov["length_cm"],
                "width_cm":      ov["width_cm"],
                "height_cm":     ov["height_cm"],
                "units_per_box": ov["units_per_box"],
                "box_weight_kg": ov["weight_kg"],
                "source":        "product_override",
            }

    # ── Category-based config ─────────────────────────────────────────────────
    default_cat = cfg["category_detection"]["default_category"]
    cat_cfg     = cfg["box_categories"].get(
        category,
        cfg["box_categories"].get(default_cat, {})
    )

    dims = cat_cfg.get("box_dimensions_cm", {"length": 28, "width": 28, "height": 28})

    # Weight: fixed or calculated
    if "box_weight_kg" in cat_cfg:
        box_weight = cat_cfg["box_weight_kg"]
    else:
        unit_wt   = cat_cfg.get("unit_weight_gm", 50) / 1000
        tare      = cat_cfg.get("box_tare_weight_kg", 0.5)
        upb       = cat_cfg.get("units_per_box", 100)
        box_weight = round((upb * unit_wt) + tare, 2)

    return {
        "category":      category,
        "length_cm":     dims["length"],
        "width_cm":      dims["width"],
        "height_cm":     dims["height"],
        "units_per_box": cat_cfg.get("units_per_box", 100),
        "box_weight_kg": box_weight,
        "source":        "category_config",
    }


def calculate_boxes(send_qty: int, units_per_box: int) -> int:
    """How many boxes needed for send_qty units."""
    if units_per_box <= 0:
        return 1
    return math.ceil(send_qty / units_per_box)
