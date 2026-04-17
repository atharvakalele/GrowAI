#!/usr/bin/env python3
"""
FBA Appointment Booker — Grow24 AI
=====================================
Handles self-ship appointment for India FBA (Steps 11–13).

Workflow:
  STEP 11: generateSelfShipAppointmentSlots  → trigger slot generation
  STEP 12: getSelfShipAppointmentSlots       → list available slots
  STEP 13: scheduleSelfShipAppointment       → book best slot

Slot selection rules (from fba_config.json):
  - Skip Sunday pickup dates
  - Prefer 14:00–16:00 window (2pm–4pm)
  - First available non-Sunday slot within window if exact not found
  - Primary: DED3 → fallback: DED5

API: FBA Inbound v2024-03-20
"""

import json
import time
from datetime import datetime, date, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]
FBA_CONFIG   = PROJECT_ROOT / "config" / "fba_config.json"
FBA_API_VER  = "2024-03-20"
FBA_BASE     = f"/inbound/v{FBA_API_VER}"

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from auth import sp_get, sp_post


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


def _retry(func, *args, **kwargs):
    """Retry wrapper with exponential backoff from config."""
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


def generate_appointment_slots(plan_id: str, shipment_id: str) -> bool:
    """
    STEP 11: Generate self-ship appointment slots for a shipment.

    Args:
        plan_id:     inboundPlanId
        shipment_id: specific shipment ID (e.g. FBA12345678)

    Returns: True if generation succeeded
    """
    print(f"\n  [STEP 11] Generating appointment slots for shipment: {shipment_id}")
    body = {
        "inboundPlanId": plan_id,
        "shipmentId":    shipment_id,
    }
    resp = _retry(sp_post, f"{FBA_BASE}/selfShipAppointmentSlots/generate", body)
    op_id = resp.get("operationId", "")
    if op_id:
        return _poll_operation(op_id)
    return True


def get_appointment_slots(plan_id: str, shipment_id: str) -> list[dict]:
    """
    STEP 12: Get available self-ship appointment slots.

    Returns list of slot dicts, each containing:
      - slotId
      - startTime  (ISO 8601, e.g. "2024-03-22T14:00:00Z")
      - endTime
      - warehouseId (DED3 or DED5)
    """
    print(f"\n  [STEP 12] Fetching appointment slots...")
    params = {
        "inboundPlanId": plan_id,
        "shipmentId":    shipment_id,
    }
    resp = _retry(sp_get, f"{FBA_BASE}/selfShipAppointmentSlots", params)
    slots = resp.get("selfShipAppointmentSlots", [])
    print(f"    Found {len(slots)} available slots")
    return slots


def _is_sunday(dt: datetime) -> bool:
    """Check if a datetime is Sunday (weekday 6)."""
    return dt.weekday() == 6


def _slot_datetime(slot: dict, key: str) -> datetime | None:
    """Parse ISO datetime from slot, returns None on error."""
    raw = slot.get(key, "")
    if not raw:
        return None
    try:
        # Handle both "Z" suffix and "+00:00" format
        raw = raw.replace("Z", "+00:00")
        return datetime.fromisoformat(raw)
    except ValueError:
        return None


def _is_in_preferred_window(start_dt: datetime, pref_start: str, pref_end: str) -> bool:
    """
    Check if slot falls within preferred time window (local time hour comparison).

    Args:
        start_dt:   slot start as datetime
        pref_start: "14:00"
        pref_end:   "16:00"
    """
    try:
        pref_h_start, pref_m_start = map(int, pref_start.split(":"))
        pref_h_end,   pref_m_end   = map(int, pref_end.split(":"))
        slot_mins = start_dt.hour * 60 + start_dt.minute
        pref_mins_start = pref_h_start * 60 + pref_m_start
        pref_mins_end   = pref_h_end   * 60 + pref_m_end
        return pref_mins_start <= slot_mins < pref_mins_end
    except Exception:
        return False


def choose_best_slot(slots: list[dict]) -> dict | None:
    """
    Select the best appointment slot based on config rules.

    Priority order:
      1. Non-Sunday + preferred time window (14:00–16:00)
      2. Non-Sunday + any time (earliest)
      3. Any slot as last resort

    Returns chosen slot dict or None if no slots available.
    """
    cfg = _load_config()
    appt_cfg     = cfg["appointment"]
    skip_days    = [d.lower() for d in appt_cfg.get("skip_days", ["Sunday"])]
    pref_start   = appt_cfg.get("preferred_time_start", "14:00")
    pref_end     = appt_cfg.get("preferred_time_end",   "16:00")

    if not slots:
        return None

    # Parse and tag each slot
    tagged = []
    for slot in slots:
        start_dt = _slot_datetime(slot, "startTime")
        if not start_dt:
            continue

        day_name = start_dt.strftime("%A").lower()  # "monday", "sunday", etc.
        is_skip  = day_name in skip_days
        in_pref  = _is_in_preferred_window(start_dt, pref_start, pref_end)

        tagged.append({
            "slot":     slot,
            "start_dt": start_dt,
            "is_skip":  is_skip,
            "in_pref":  in_pref,
        })

    # Sort by start time ascending
    tagged.sort(key=lambda x: x["start_dt"])

    # Priority 1: non-skip day + preferred window
    for t in tagged:
        if not t["is_skip"] and t["in_pref"]:
            slot = t["slot"]
            print(f"    [BEST] Priority 1 — {t['start_dt'].strftime('%A %Y-%m-%d %H:%M')} (preferred window)")
            return slot

    # Priority 2: non-skip day, any time (earliest)
    for t in tagged:
        if not t["is_skip"]:
            slot = t["slot"]
            print(f"    [BEST] Priority 2 — {t['start_dt'].strftime('%A %Y-%m-%d %H:%M')} (non-skip, earliest)")
            return slot

    # Priority 3: any slot (last resort)
    slot = tagged[0]["slot"]
    print(f"    [WARN] Priority 3 — {tagged[0]['start_dt'].strftime('%A %Y-%m-%d %H:%M')} (last resort, skip day)")
    return slot


def schedule_appointment(plan_id: str, shipment_id: str, slot_id: str) -> bool:
    """
    STEP 13: Book the chosen appointment slot.

    Args:
        plan_id:     inboundPlanId
        shipment_id: shipment ID
        slot_id:     chosen slotId from getSelfShipAppointmentSlots

    Returns: True if booking confirmed
    """
    print(f"\n  [STEP 13] Scheduling appointment: slot {slot_id}")
    body = {
        "inboundPlanId": plan_id,
        "shipmentId":    shipment_id,
        "slotId":        slot_id,
    }
    resp = _retry(sp_post, f"{FBA_BASE}/selfShipAppointments/schedule", body)
    op_id = resp.get("operationId", "")
    if op_id:
        success = _poll_operation(op_id)
        if success:
            print(f"    [OK] Appointment confirmed!")
        return success
    # No operationId means synchronous success
    print(f"    [OK] Appointment confirmed (synchronous)")
    return True


def book_appointment(plan_id: str, shipment_id: str) -> dict:
    """
    Main appointment booking pipeline (Steps 11-13).

    Args:
        plan_id:     inboundPlanId
        shipment_id: shipment ID

    Returns:
        {
            "success":    True/False,
            "slot_id":    "SLOT_XYZ",
            "slot_time":  "2024-03-22T14:00:00+00:00",
            "slot_day":   "Friday",
            "shipment_id": shipment_id,
        }
    """
    result = {
        "success":     False,
        "slot_id":     "",
        "slot_time":   "",
        "slot_day":    "",
        "shipment_id": shipment_id,
    }

    # STEP 11
    generated = generate_appointment_slots(plan_id, shipment_id)
    if not generated:
        print(f"  [ERROR] Failed to generate appointment slots for {shipment_id}")
        return result

    # STEP 12
    slots = get_appointment_slots(plan_id, shipment_id)
    if not slots:
        print(f"  [WARN] No appointment slots available for {shipment_id}")
        return result

    # Choose best slot
    chosen = choose_best_slot(slots)
    if not chosen:
        print(f"  [ERROR] Could not select a slot for {shipment_id}")
        return result

    slot_id   = chosen.get("slotId", "")
    slot_time = chosen.get("startTime", "")
    start_dt  = _slot_datetime(chosen, "startTime")
    slot_day  = start_dt.strftime("%A") if start_dt else ""

    # STEP 13
    booked = schedule_appointment(plan_id, shipment_id, slot_id)

    result.update({
        "success":   booked,
        "slot_id":   slot_id,
        "slot_time": slot_time,
        "slot_day":  slot_day,
    })
    return result


def book_all_shipments(plan_id: str, shipment_ids: list[str]) -> list[dict]:
    """
    Book appointments for all shipments in an inbound plan.

    Args:
        plan_id:      inboundPlanId
        shipment_ids: list of shipment IDs from get_shipment_ids()

    Returns: list of booking results (one per shipment)
    """
    print(f"\n  [APPOINTMENT] Booking {len(shipment_ids)} shipment(s)...")
    results = []
    for shipment_id in shipment_ids:
        print(f"\n  --- Shipment: {shipment_id} ---")
        result = book_appointment(plan_id, shipment_id)
        results.append(result)

        if result["success"]:
            print(f"  [OK] {shipment_id}: {result['slot_day']} {result['slot_time'][:10]} "
                  f"@ {result['slot_time'][11:16] if len(result['slot_time']) > 15 else 'N/A'}")
        else:
            print(f"  [FAIL] {shipment_id}: Could not book appointment")

        # Small pause between shipments to avoid rate limiting
        if len(shipment_ids) > 1:
            time.sleep(2)

    success_count = sum(1 for r in results if r["success"])
    print(f"\n  [APPOINTMENT SUMMARY] {success_count}/{len(shipment_ids)} appointments booked")
    return results
