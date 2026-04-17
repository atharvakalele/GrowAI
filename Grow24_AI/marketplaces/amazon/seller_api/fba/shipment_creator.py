#!/usr/bin/env python3
"""
FBA Shipment Creator — Grow24 AI
====================================
Creates FBA inbound shipment using API v2024-03-20 (PRIMARY).

⛔ DO NOT use legacy v0 API without Msir approval.
   Legacy docs: API_Documentation/Amazon_SP_API/FBA_Inbound/legacy/

Workflow:
  STEP 1: createInboundPlan      → inboundPlanId
  STEP 2: poll operationStatus   → wait SUCCESS
  STEP 3: listPackingOptions     → packingOptionId
  STEP 4: generatePackingOptions → generate
  STEP 5: confirmPackingOption   → confirm
  STEP 6: setPackingInformation  → box dimensions + items
  STEP 7: generatePlacementOptions
  STEP 8: confirmPlacementOption → DED3 or DED5
  STEP 9: generateTransportationOptions
  STEP 10: confirmTransportationOptions
"""

import json
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]
FBA_CONFIG   = PROJECT_ROOT / "config" / "fba_config.json"
FBA_API_VER  = "2024-03-20"
FBA_BASE     = f"/inbound/v{FBA_API_VER}"
MARKETPLACE  = "A21TJRUUN4KGV"

# Import auth from same seller_api folder
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from auth import sp_get, sp_post, sp_put


def _load_config() -> dict:
    with open(FBA_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def _poll_operation(operation_id: str, max_wait: int = 60) -> bool:
    """Poll operationStatus until SUCCESS or timeout."""
    print(f"    Polling operation: {operation_id}")
    for attempt in range(max_wait // 5):
        time.sleep(5)
        resp = sp_get(f"{FBA_BASE}/operationStatus/{operation_id}")
        status = resp.get("operationStatus", "")
        print(f"    Status: {status} (attempt {attempt+1})")
        if status == "SUCCESS":
            return True
        if status == "FAILED":
            problems = resp.get("operationProblems", [])
            print(f"    FAILED: {problems}")
            return False
    print(f"    TIMEOUT waiting for operation")
    return False


def _retry(func, *args, max_attempts: int = 3, delay: int = 5, **kwargs):
    """Retry wrapper with exponential backoff."""
    cfg = _load_config()
    retries = cfg["retry"]["max_attempts"]
    delay_s = cfg["retry"]["delay_seconds"]
    mult    = cfg["retry"]["backoff_multiplier"]

    for attempt in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt < retries - 1:
                wait = delay_s * (mult ** attempt)
                print(f"    [RETRY {attempt+1}/{retries}] Error: {e} — retrying in {wait}s")
                time.sleep(wait)
            else:
                raise


def create_inbound_plan(items: list[dict], plan_name: str = None) -> dict:
    """
    STEP 1: Create inbound plan.

    Args:
        items: [{"msku": "SKU-001", "quantity": 100}]
        plan_name: Optional custom name

    Returns: {"inboundPlanId": "...", "operationId": "..."}
    """
    cfg = _load_config()
    src = cfg["source_address"]
    ship_cfg = cfg["shipment"]

    if not plan_name:
        from datetime import datetime
        plan_name = f"Grow24_FBA_{datetime.now().strftime('%Y%m%d_%H%M')}"

    # Format items for API
    api_items = [
        {
            "msku":        item["msku"],
            "quantity":    item["quantity"],
            "prepOwner":   ship_cfg["prep_owner"],
            "labelOwner":  ship_cfg["label_owner"],
        }
        for item in items
    ]

    body = {
        "name":                    plan_name,
        "destinationMarketplaces": [MARKETPLACE],
        "items":                   api_items,
        "sourceAddress": {
            "name":                src["name"],
            "companyName":         src["company_name"],
            "addressLine1":        src["address_line1"],
            "city":                src["city"],
            "stateOrProvinceCode": src["state_code"],
            "postalCode":          src["postal_code"],
            "countryCode":         src["country_code"],
            "phoneNumber":         src["phone"],
            "email":               src["email"],
        },
    }
    if src.get("address_line2"):
        body["sourceAddress"]["addressLine2"] = src["address_line2"]

    print(f"\n  [STEP 1] Creating inbound plan: {plan_name}")
    resp = _retry(sp_post, f"{FBA_BASE}/inboundPlans", body)

    plan_id = resp.get("inboundPlanId", "")
    op_id   = resp.get("operationId", "")
    print(f"    Plan ID: {plan_id}")

    # Wait for plan to be ready
    if op_id:
        success = _poll_operation(op_id)
        if not success:
            raise RuntimeError(f"createInboundPlan operation failed: {op_id}")

    return {"inboundPlanId": plan_id, "operationId": op_id}


def get_packing_options(plan_id: str) -> list[dict]:
    """STEP 3: List available packing options."""
    print(f"\n  [STEP 3] Getting packing options...")
    resp = _retry(sp_get, f"{FBA_BASE}/packingOptions", {"inboundPlanId": plan_id})
    options = resp.get("packingOptions", [])
    print(f"    Found {len(options)} packing options")
    return options


def generate_packing_options(plan_id: str) -> bool:
    """STEP 4: Generate packing options."""
    print(f"\n  [STEP 4] Generating packing options...")
    resp = _retry(sp_post, f"{FBA_BASE}/packingOptions/generate", {"inboundPlanId": plan_id})
    op_id = resp.get("operationId", "")
    if op_id:
        return _poll_operation(op_id)
    return True


def confirm_packing_option(plan_id: str, packing_option_id: str) -> bool:
    """STEP 5: Confirm packing option."""
    print(f"\n  [STEP 5] Confirming packing option: {packing_option_id}")
    resp = _retry(sp_post, f"{FBA_BASE}/packingOptions/{packing_option_id}/confirm",
                  {"inboundPlanId": plan_id})
    op_id = resp.get("operationId", "")
    if op_id:
        return _poll_operation(op_id)
    return True


def set_packing_information(plan_id: str, packing_group_id: str, boxes: list[dict]) -> bool:
    """
    STEP 6: Set box dimensions, weight, items.

    boxes format:
    [
        {
            "items": [{"msku": "SKU-001", "quantity": 100, "prepOwner": "SELLER", "labelOwner": "SELLER"}],
            "dimensions": {"length_cm": 28, "width_cm": 34, "height_cm": 36},
            "weight_kg": 5.5,
            "box_count": 3
        }
    ]
    """
    print(f"\n  [STEP 6] Setting packing information for group: {packing_group_id}")
    cfg = _load_config()
    ship_cfg = cfg["shipment"]

    api_boxes = []
    for box in boxes:
        dims = box["dimensions"]
        api_box = {
            "contentInformationSource": ship_cfg["content_information_source"],
            "dimensions": {
                "unitOfMeasurement": "CM",
                "length": dims["length_cm"],
                "width":  dims["width_cm"],
                "height": dims["height_cm"],
            },
            "weight": {
                "unit":  "KG",
                "value": box["weight_kg"],
            },
            "quantity": box["box_count"],
            "items": [
                {
                    "msku":       item["msku"],
                    "quantity":   item["quantity"],
                    "prepOwner":  item.get("prepOwner",  ship_cfg["prep_owner"]),
                    "labelOwner": item.get("labelOwner", ship_cfg["label_owner"]),
                }
                for item in box["items"]
            ],
        }
        api_boxes.append(api_box)

    body = {
        "inboundPlanId": plan_id,
        "boxes":         api_boxes,
    }
    resp = _retry(sp_post, f"{FBA_BASE}/packingGroupItems/{packing_group_id}/information", body)
    op_id = resp.get("operationId", "")
    if op_id:
        return _poll_operation(op_id)
    return True


def generate_and_confirm_placement(plan_id: str) -> str:
    """
    STEP 7+8: Generate placement options and confirm DED3 (or DED5 fallback).
    Returns confirmed placementOptionId.
    """
    cfg = _load_config()
    primary_wh  = cfg["warehouses"]["primary"]
    fallback_wh = cfg["warehouses"]["fallback"]

    print(f"\n  [STEP 7] Generating placement options...")
    resp = _retry(sp_post, f"{FBA_BASE}/placementOptions/generate", {"inboundPlanId": plan_id})
    op_id = resp.get("operationId", "")
    if op_id:
        _poll_operation(op_id)

    print(f"\n  [STEP 8] Listing placement options...")
    resp = _retry(sp_get, f"{FBA_BASE}/placementOptions", {"inboundPlanId": plan_id})
    options = resp.get("placementOptions", [])
    print(f"    Found {len(options)} placement options")

    # Choose DED3 first, then DED5, then first available
    chosen = None
    for wh in [primary_wh, fallback_wh]:
        for opt in options:
            fc = opt.get("shipments", [{}])[0].get("warehouseId", "")
            if wh in fc:
                chosen = opt
                print(f"    Chose warehouse: {wh} (placementOptionId: {opt['placementOptionId']})")
                break
        if chosen:
            break

    if not chosen and options:
        chosen = options[0]
        print(f"    [WARN] DED3/DED5 not found — using first available: {chosen.get('placementOptionId')}")

    if not chosen:
        raise RuntimeError("No placement options available")

    placement_id = chosen["placementOptionId"]
    print(f"    Confirming placement: {placement_id}")
    resp = _retry(sp_post, f"{FBA_BASE}/placementOptions/{placement_id}/confirm",
                  {"inboundPlanId": plan_id})
    op_id = resp.get("operationId", "")
    if op_id:
        _poll_operation(op_id)

    return placement_id


def generate_and_confirm_transportation(plan_id: str) -> bool:
    """STEP 9+10: Generate and confirm transportation (self-ship for India)."""
    print(f"\n  [STEP 9] Generating transportation options...")
    resp = _retry(sp_post, f"{FBA_BASE}/transportationOptions/generate", {"inboundPlanId": plan_id})
    op_id = resp.get("operationId", "")
    if op_id:
        _poll_operation(op_id)

    print(f"\n  [STEP 10] Listing transportation options...")
    resp = _retry(sp_get, f"{FBA_BASE}/transportationOptions", {"inboundPlanId": plan_id})
    options = resp.get("transportationOptions", [])

    if not options:
        print("    [WARN] No transportation options found")
        return False

    # Prefer self-ship for India
    chosen = next(
        (o for o in options if "self" in o.get("shippingMode", "").lower()), options[0]
    )
    trans_id = chosen.get("transportationOptionId", "")
    print(f"    Confirming transportation: {trans_id} ({chosen.get('shippingMode', '')})")

    body = {
        "inboundPlanId":          plan_id,
        "transportationOptionId": trans_id,
    }
    resp = _retry(sp_post, f"{FBA_BASE}/transportationOptions/confirm", body)
    op_id = resp.get("operationId", "")
    if op_id:
        _poll_operation(op_id)

    return True


def get_shipment_ids(plan_id: str) -> list[str]:
    """Get shipment IDs from the inbound plan."""
    resp = _retry(sp_get, f"{FBA_BASE}/inboundPlans/{plan_id}")
    shipments = resp.get("shipments", [])
    ids = [s.get("shipmentId", "") for s in shipments if s.get("shipmentId")]
    print(f"    Shipment IDs: {ids}")
    return ids
