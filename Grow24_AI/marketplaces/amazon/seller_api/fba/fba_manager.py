#!/usr/bin/env python3
"""
FBA Manager — Grow24 AI
==========================
Main pipeline entry point for FBA Inbound Shipment automation.

Orchestrates all 15 steps:
  STEP 1-2:   Create inbound plan + poll
  STEP 3-5:   Packing options (list → generate → confirm)
  STEP 6:     Set packing information (box dims + items)
  STEP 7-8:   Placement options (generate → confirm DED3/DED5)
  STEP 9-10:  Transportation options (generate → confirm self-ship)
  STEP 11-13: Self-ship appointment (generate slots → choose → book)
  STEP 14-15: Documents (labels PDF + delivery challan PDF)
  POST:       Write Purchase Order to Google Sheet

Usage:
  python fba_manager.py                        # Full auto run
  python fba_manager.py --dry-run              # Preview only (no API calls)
  python fba_manager.py --sku SKU-001 SKU-002  # Specific SKUs only
  python fba_manager.py --plan-id FBA_PLAN_XXX --from-step 7  # Resume from step

Architecture: Grow24_AI / marketplaces / amazon / seller_api / fba /
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]
FBA_CONFIG   = PROJECT_ROOT / "config" / "fba_config.json"
RESULTS_DIR  = PROJECT_ROOT / "output" / "fba_runs"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Add parent to path for auth import
sys.path.insert(0, str(Path(__file__).parent.parent))
from auth import sp_get

# FBA sub-modules
from product_filter   import apply_filter, detect_category, get_box_config, calculate_boxes
from quantity_predictor import predict_all
from shipment_creator import (
    create_inbound_plan,
    get_packing_options,
    generate_packing_options,
    confirm_packing_option,
    set_packing_information,
    generate_and_confirm_placement,
    generate_and_confirm_transportation,
    get_shipment_ids,
)
from appointment_booker import book_all_shipments
from po_generator import generate_all_documents, write_po_to_sheet

MARKETPLACE_ID = "A21TJRUUN4KGV"  # India


def _load_config() -> dict:
    with open(FBA_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_run_result(result: dict) -> Path:
    """Save run result to JSON file for audit/resume."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plan_id   = result.get("plan_id", "unknown")[:12]
    save_path = RESULTS_DIR / f"fba_run_{timestamp}_{plan_id}.json"
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n  [AUDIT] Run saved: {save_path.name}")
    return save_path


def get_fba_sku_list() -> dict[str, str]:
    """
    Get all FBA-eligible SKUs and their ASINs from SP-API inventory.

    Returns: {sku: asin} — only FBA-fulfillment type SKUs
    """
    print("\n  [INVENTORY] Loading FBA SKU list from SP-API...")
    try:
        resp = sp_get(
            "/fba/inventory/v1/summaries",
            {
                "details":        "true",
                "granularityType": "Marketplace",
                "granularityId":   MARKETPLACE_ID,
                "marketplaceIds":  MARKETPLACE_ID,
            }
        )
        items = resp.get("payload", {}).get("inventorySummaries", [])

        sku_asin_map = {}
        for item in items:
            sku  = item.get("sellerSku", "")
            asin = item.get("asin", "")
            if sku and asin:
                sku_asin_map[sku] = asin

        print(f"  [OK] {len(sku_asin_map)} FBA SKUs found")
        return sku_asin_map

    except Exception as e:
        print(f"  [ERROR] Could not load FBA inventory: {e}")
        return {}


def get_product_details(asin: str) -> dict:
    """
    Fetch product title and category from SP-API Catalog Items.
    Used for category detection (box size calculation).

    Returns: {"title": str, "category": str}
    """
    try:
        resp = sp_get(
            f"/catalog/2022-04-01/items/{asin}",
            {
                "marketplaceIds": MARKETPLACE_ID,
                "includedData":   "summaries,classifications",
            }
        )
        summaries       = resp.get("summaries", [{}])
        classifications = resp.get("classifications", [{}])

        title    = summaries[0].get("itemName", "") if summaries else ""
        category = classifications[0].get("classificationId", "") if classifications else ""

        # Also try display group
        if not category and classifications:
            category = classifications[0].get("displayName", "")

        return {"title": title, "category": category}

    except Exception as e:
        # Non-fatal: category detection will fall back to defaults
        return {"title": "", "category": ""}


def build_po_data(
    predictions: list[dict],
    product_details: dict[str, dict],
    box_configs: dict[str, dict],
    box_counts: dict[str, int],
    shipment_map: dict[str, str],  # sku → shipment_id
    placement_id: str,
) -> list[dict]:
    """Build PO row data for Google Sheet writer."""
    today = datetime.now().strftime("%Y-%m-%d")
    cfg   = _load_config()
    wh    = cfg["warehouses"]["primary"]

    po_rows = []
    for pred in predictions:
        sku  = pred["sku"]
        asin = pred["asin"]
        det  = product_details.get(asin, {})
        bc   = box_configs.get(sku, {})

        po_rows.append({
            "date":          today,
            "sku":           sku,
            "asin":          asin,
            "product_name":  det.get("title", "")[:100],
            "category":      bc.get("category", ""),
            "send_qty":      pred["send_qty"],
            "units_per_box": bc.get("units_per_box", 0),
            "box_count":     box_counts.get(sku, 0),
            "box_length_cm": bc.get("length_cm", 0),
            "box_width_cm":  bc.get("width_cm",  0),
            "box_height_cm": bc.get("height_cm", 0),
            "box_weight_kg": bc.get("box_weight_kg", 0),
            "warehouse":     wh,
            "shipment_id":   shipment_map.get(sku, ""),
            "status":        "Booked",
            "notes":         f"Plan: {placement_id[:12]}..." if placement_id else "",
        })

    return po_rows


def run_fba_pipeline(
    specific_skus: list[str] = None,
    dry_run: bool = False,
    resume_plan_id: str = None,
    from_step: int = 1,
) -> dict:
    """
    Main FBA automation pipeline — runs all 15 steps.

    Args:
        specific_skus:  If set, only process these SKUs (bypass filter)
        dry_run:        If True, preview mode — no API write calls
        resume_plan_id: Resume an existing inbound plan from a step
        from_step:      Step to start from (for resume scenarios)

    Returns: Full result dict with plan_id, shipments, appointments, documents
    """
    print("\n" + "="*60)
    print("  Grow24 AI — FBA Automation Pipeline")
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if dry_run:
        print("  MODE: DRY RUN (preview only)")
    print("="*60)

    run_result = {
        "started_at":   datetime.now().isoformat(),
        "dry_run":      dry_run,
        "plan_id":      "",
        "predictions":  [],
        "shipment_ids": [],
        "appointments": [],
        "documents":    {},
        "po_result":    {},
        "status":       "started",
        "error":        "",
    }

    try:
        # ── PRE-STEP: Load SKU list ──────────────────────────────────────────
        if resume_plan_id and from_step > 1:
            print(f"\n  [RESUME] Resuming plan: {resume_plan_id} from step {from_step}")
            run_result["plan_id"] = resume_plan_id
        else:
            # Get FBA SKU→ASIN map
            sku_asin_map = get_fba_sku_list()
            if not sku_asin_map:
                raise RuntimeError("No FBA SKUs found — check inventory")

            # Apply filter (INCLUDE/EXCLUDE from Google Sheet)
            all_skus = list(sku_asin_map.keys())
            if specific_skus:
                filtered_skus = [s for s in specific_skus if s in sku_asin_map]
                print(f"  [FILTER] Specific SKUs: {len(filtered_skus)} provided")
            else:
                filtered_skus = apply_filter(all_skus)

            if not filtered_skus:
                print("  [WARN] No SKUs pass filter — nothing to ship")
                run_result["status"] = "skipped"
                return run_result

            # Filtered sku→asin map
            fba_map = {sku: sku_asin_map[sku] for sku in filtered_skus if sku in sku_asin_map}

            # ── PREDICT quantities ───────────────────────────────────────────
            print(f"\n  [PREDICT] Calculating send quantities for {len(fba_map)} SKUs...")
            predictions = predict_all(fba_map)
            run_result["predictions"] = predictions

            if not predictions:
                print("  [INFO] No SKUs need replenishment at this time")
                run_result["status"] = "nothing_to_send"
                return run_result

            print(f"\n  [SUMMARY] {len(predictions)} SKUs to send:")
            for p in predictions:
                print(f"    {p['sku']:20s}  send: {p['send_qty']:4d}  stock: {p['current_stock']:4d}  "
                      f"daily_avg: {p['avg_daily']:.1f}")

            # ── Fetch product details for each ASIN ─────────────────────────
            print(f"\n  [CATALOG] Fetching product details for category detection...")
            product_details = {}
            unique_asins = list({p["asin"] for p in predictions})
            for i, asin in enumerate(unique_asins):
                det = get_product_details(asin)
                product_details[asin] = det
                if det.get("title"):
                    print(f"    {asin}: {det['title'][:50]}")
                time.sleep(0.5)  # Rate limit: catalog API = 2 req/s

            # ── Detect category + box config for each SKU ───────────────────
            print(f"\n  [BOX CONFIG] Calculating box configurations...")
            box_configs  = {}
            box_counts   = {}
            items_for_api = []

            for pred in predictions:
                sku  = pred["sku"]
                asin = pred["asin"]
                det  = product_details.get(asin, {})

                # Pass sku+asin so product_override is checked FIRST
                category = detect_category(
                    product_title=det.get("title", ""),
                    api_category=det.get("category", ""),
                    sku=sku,
                    asin=asin,
                )
                bc    = get_box_config(category, sku=sku, asin=asin)
                boxes = calculate_boxes(pred["send_qty"], bc["units_per_box"])

                box_configs[sku] = bc
                box_counts[sku]  = boxes

                print(f"    {sku}: cat={category}  units_per_box={bc['units_per_box']}  "
                      f"boxes={boxes}  weight={bc['box_weight_kg']}kg")

                items_for_api.append({
                    "msku":     sku,
                    "quantity": pred["send_qty"],
                })

            if dry_run:
                print("\n  [DRY RUN] Would create inbound plan with:")
                print(f"    Items: {len(items_for_api)}")
                for it in items_for_api:
                    print(f"      {it['msku']}: {it['quantity']} units")
                run_result["status"] = "dry_run_complete"
                return run_result

            # ── STEP 1-2: Create inbound plan ────────────────────────────────
            if from_step <= 1:
                plan_result = create_inbound_plan(items_for_api)
                plan_id     = plan_result["inboundPlanId"]
                run_result["plan_id"] = plan_id
            else:
                plan_id = resume_plan_id

        # From here, plan_id is available (new or resumed)
        plan_id = run_result["plan_id"]

        # ── STEP 3: List packing options ─────────────────────────────────────
        if from_step <= 3:
            packing_options = get_packing_options(plan_id)

            # If no options yet, generate first
            if not packing_options:
                # STEP 4: Generate
                generate_packing_options(plan_id)
                packing_options = get_packing_options(plan_id)

            if not packing_options:
                raise RuntimeError("No packing options available after generation")

            # Use first packing option (typically only one for small sellers)
            chosen_packing = packing_options[0]
            packing_opt_id = chosen_packing.get("packingOptionId", "")
            packing_grp_id = (chosen_packing.get("packingGroups", [{}])[0]
                              .get("packingGroupId", ""))
            print(f"  [STEP 3] Packing option: {packing_opt_id}")
            print(f"  [STEP 3] Packing group:  {packing_grp_id}")

        # ── STEP 5: Confirm packing option ───────────────────────────────────
        if from_step <= 5:
            confirm_packing_option(plan_id, packing_opt_id)

        # ── STEP 6: Set packing information ──────────────────────────────────
        if from_step <= 6:
            print(f"\n  [STEP 6] Building box list for {len(predictions)} SKU(s)...")
            boxes_payload = []
            for pred in predictions:
                sku  = pred["sku"]
                asin = pred["asin"]
                bc   = box_configs[sku]
                bc_c = box_counts[sku]

                boxes_payload.append({
                    "items": [{
                        "msku":       sku,
                        "quantity":   pred["send_qty"],
                        "prepOwner":  "SELLER",
                        "labelOwner": "SELLER",
                    }],
                    "dimensions": {
                        "length_cm": bc["length_cm"],
                        "width_cm":  bc["width_cm"],
                        "height_cm": bc["height_cm"],
                    },
                    "weight_kg": bc["box_weight_kg"],
                    "box_count": bc_c,
                })

            set_packing_information(plan_id, packing_grp_id, boxes_payload)

        # ── STEPS 7-8: Placement ─────────────────────────────────────────────
        if from_step <= 7:
            placement_id = generate_and_confirm_placement(plan_id)
            run_result["placement_id"] = placement_id
        else:
            placement_id = ""

        # ── STEPS 9-10: Transportation ───────────────────────────────────────
        if from_step <= 9:
            generate_and_confirm_transportation(plan_id)

        # ── Get shipment IDs ─────────────────────────────────────────────────
        print(f"\n  [SHIPMENTS] Getting shipment IDs...")
        shipment_ids = get_shipment_ids(plan_id)
        run_result["shipment_ids"] = shipment_ids

        if not shipment_ids:
            raise RuntimeError("No shipment IDs found after plan creation")

        # ── STEPS 11-13: Appointments ────────────────────────────────────────
        if from_step <= 11:
            appointment_results = book_all_shipments(plan_id, shipment_ids)
            run_result["appointments"] = appointment_results

        # ── STEPS 14-15: Documents ───────────────────────────────────────────
        if from_step <= 14:
            doc_results = generate_all_documents(plan_id, shipment_ids)
            run_result["documents"] = doc_results

        # ── POST: Write PO to Google Sheet ───────────────────────────────────
        print(f"\n  [PO] Preparing Purchase Order...")

        # Build shipment map: for now map all SKUs to first shipment
        # (multi-shipment routing will refine this if needed)
        shipment_map = {}
        if shipment_ids:
            for pred in predictions:
                shipment_map[pred["sku"]] = shipment_ids[0]

        po_data = build_po_data(
            predictions      = predictions,
            product_details  = product_details,
            box_configs      = box_configs,
            box_counts       = box_counts,
            shipment_map     = shipment_map,
            placement_id     = placement_id,
        )

        appt_results = run_result.get("appointments", [])
        doc_results  = run_result.get("documents", {})
        po_result    = write_po_to_sheet(po_data, appt_results, doc_results)
        run_result["po_result"] = po_result

        run_result["status"]       = "completed"
        run_result["completed_at"] = datetime.now().isoformat()

    except Exception as e:
        run_result["status"] = "error"
        run_result["error"]  = str(e)
        print(f"\n  [ERROR] Pipeline failed: {e}")
        import traceback
        traceback.print_exc()

    finally:
        _save_run_result(run_result)

    # ── Final summary ─────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print(f"  STATUS:    {run_result['status'].upper()}")
    print(f"  Plan ID:   {run_result.get('plan_id', 'N/A')}")
    print(f"  Shipments: {len(run_result.get('shipment_ids', []))}")
    appts = run_result.get("appointments", [])
    booked = sum(1 for a in appts if a.get("success"))
    print(f"  Appointments booked: {booked}/{len(appts)}")
    po = run_result.get("po_result", {})
    if po.get("tab_name"):
        print(f"  PO written:  {po['tab_name']} ({po.get('rows_written', 0)} rows)")
    if run_result.get("error"):
        print(f"  ERROR:     {run_result['error']}")
    print("="*60)

    return run_result


# ─────────────────────────────────────────────────────────────────────────────
# CLI Entry Point
# ─────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Grow24 AI — FBA Shipment Automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fba_manager.py                             # Full auto run
  python fba_manager.py --dry-run                   # Preview quantities only
  python fba_manager.py --sku SKU-001 SKU-002       # Process specific SKUs
  python fba_manager.py --plan-id FBA_XXX --from-step 7  # Resume from step 7
        """
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview mode — show quantities without making API calls"
    )
    parser.add_argument(
        "--sku", nargs="+", metavar="SKU",
        help="Process only specific SKUs (space-separated)"
    )
    parser.add_argument(
        "--plan-id", metavar="PLAN_ID",
        help="Resume an existing inbound plan ID"
    )
    parser.add_argument(
        "--from-step", type=int, default=1, metavar="N",
        help="Start from step N (1-15, default: 1)"
    )

    args = parser.parse_args()

    result = run_fba_pipeline(
        specific_skus  = args.sku,
        dry_run        = args.dry_run,
        resume_plan_id = args.plan_id,
        from_step      = args.from_step,
    )

    sys.exit(0 if result.get("status") in ("completed", "dry_run_complete", "nothing_to_send") else 1)


if __name__ == "__main__":
    main()
