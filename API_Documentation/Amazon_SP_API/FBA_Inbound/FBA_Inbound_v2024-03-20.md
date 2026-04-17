# FBA Inbound API v2024-03-20
## Official Reference — Grow24 AI Project
**Date Documented:** 14 April 2026
**Source:** https://developer-docs.amazon.com/sp-api/docs/fulfillment-inbound-api-v2024-03-20-reference
**Region:** EU (India = Europe region)
**Base URL:** `https://sellingpartnerapi-eu.amazon.com`
**Marketplace ID (India):** `A21TJRUUN4KGV`

---

## ⚠️ VERSION RULE
```
PRIMARY:  FBA Inbound v2024-03-20   ← ALWAYS use this
FALLBACK: FBA Inbound v0 (legacy)   ← in legacy/ folder
⛔ DO NOT use v0 without explicit Msir approval
⛔ DO NOT mix v0 and v2024-03-20 calls in same flow
```

---

## 🔐 Authentication
- OAuth 2.0 via LWA (Login with Amazon)
- Role required: **"Amazon Fulfillment"** (must be granted in Seller Central)
- Same auth as other SP-API calls (use existing `auth.py`)
- Headers: `x-amz-access-token`, `x-amz-date`, `Authorization` (AWS Signature V4)

---

## 🔄 Complete Workflow (India — Self Ship)

```
STEP 1: createInboundPlan         → get inboundPlanId + operationId
STEP 2: getInboundOperationStatus → wait until COMPLETE
STEP 3: listPackingOptions        → see available packing groups
STEP 4: generatePackingOptions    → generate options
STEP 5: confirmPackingOption      → choose packing option
STEP 6: setPackingInformation     → set box size/weight/items
STEP 7: generatePlacementOptions  → get warehouse options (DED3/DED5)
STEP 8: confirmPlacementOption    → choose DED3 (or DED5 fallback)
STEP 9: generateTransportationOptions → get transport options
STEP 10: confirmTransportationOptions → confirm self-ship
STEP 11: generateSelfShipAppointmentSlots → generate time slots
STEP 12: getSelfShipAppointmentSlots → list available slots
STEP 13: scheduleSelfShipAppointment → book slot (2pm-4pm, no Sunday)
STEP 14: createMarketplaceItemLabels → get FNSKU barcode labels (if needed)
STEP 15: getDeliveryChallanDocument → get delivery challan (India required)
```

---

## 📋 Endpoints Reference

### STEP 1 — Create Inbound Plan
```
POST /inbound/v2024-03-20/inboundPlans
```

**Request Body:**
```json
{
  "name": "Grow24_FBA_20260414",
  "sourceAddress": {
    "name": "Msir Name",
    "companyName": "GoAmrita Bhandar",
    "addressLine1": "Your Address Line 1",
    "addressLine2": "Optional",
    "city": "Your City",
    "stateOrProvinceCode": "UP",
    "postalCode": "201001",
    "countryCode": "IN",
    "phoneNumber": "+91XXXXXXXXXX",
    "email": "mahendrasir23@gmail.com"
  },
  "destinationMarketplaces": ["A21TJRUUN4KGV"],
  "items": [
    {
      "msku": "SKU-001",
      "quantity": 100,
      "prepOwner": "SELLER",
      "labelOwner": "SELLER"
    }
  ]
}
```

**Required fields in items:**
| Field | Type | Values | Note |
|-------|------|--------|------|
| msku | string | your SKU | Merchant SKU (NOT ASIN) |
| quantity | integer | > 0 | units to send |
| prepOwner | string | "SELLER" / "AMAZON" | who preps |
| labelOwner | string | "SELLER" / "AMAZON" | who labels |

**Response:**
```json
{
  "inboundPlanId": "plan_xxxxx38chars",
  "operationId": "op_xxxxx"
}
```

---

### STEP 2 — Check Operation Status
```
GET /inbound/v2024-03-20/operationStatus/{operationId}
```

**Poll until status = "SUCCESS"**

**Response:**
```json
{
  "operationStatus": "SUCCESS",   // or "IN_PROGRESS" / "FAILED"
  "operationProblems": []
}
```

---

### STEP 3 — List Packing Options
```
GET /inbound/v2024-03-20/packingOptions?inboundPlanId={id}
```

---

### STEP 4 — Generate Packing Options
```
POST /inbound/v2024-03-20/packingOptions/generate
```
```json
{ "inboundPlanId": "plan_xxx" }
```

---

### STEP 5 — Confirm Packing Option
```
POST /inbound/v2024-03-20/packingOptions/{packingOptionId}/confirm
```
```json
{ "inboundPlanId": "plan_xxx" }
```

---

### STEP 6 — Set Packing Information (Box Details)
```
POST /inbound/v2024-03-20/packingGroupItems/{packingGroupId}/information
```

**Request Body:**
```json
{
  "inboundPlanId": "plan_xxx",
  "boxes": [
    {
      "contentInformationSource": "BOX_CONTENT_PROVIDED",
      "dimensions": {
        "unitOfMeasurement": "CM",
        "length": 28,
        "width": 34,
        "height": 36
      },
      "weight": {
        "unit": "KG",
        "value": 5.5
      },
      "quantity": 1,
      "items": [
        {
          "msku": "SKU-001",
          "quantity": 100,
          "prepOwner": "SELLER",
          "labelOwner": "SELLER"
        }
      ]
    }
  ]
}
```

**Box dimension/weight fields:**
| Field | Type | Unit | Note |
|-------|------|------|------|
| length | number | CM | box length |
| width | number | CM | box width |
| height | number | CM | box height |
| unitOfMeasurement | string | "CM" | always CM |
| weight.value | number | KG | total box weight |
| weight.unit | string | "KG" | always KG |
| quantity | integer | — | number of identical boxes |

---

### STEP 7 — Generate Placement Options
```
POST /inbound/v2024-03-20/placementOptions/generate
```
```json
{ "inboundPlanId": "plan_xxx" }
```

Returns operationId → poll for result.

---

### STEP 8 — List + Confirm Placement (Warehouse)
```
GET  /inbound/v2024-03-20/placementOptions?inboundPlanId={id}
POST /inbound/v2024-03-20/placementOptions/{placementOptionId}/confirm
```
```json
{ "inboundPlanId": "plan_xxx" }
```

**Logic:** Choose DED3 if available, else DED5, else first available.

---

### STEP 9-10 — Transportation Options (Self Ship)
```
POST /inbound/v2024-03-20/transportationOptions/generate
GET  /inbound/v2024-03-20/transportationOptions?inboundPlanId={id}
POST /inbound/v2024-03-20/transportationOptions/confirm
```

---

### STEP 11-13 — Self Ship Appointment
```
POST /inbound/v2024-03-20/shipments/{shipmentId}/selfShipAppointmentSlots/generate
GET  /inbound/v2024-03-20/shipments/{shipmentId}/selfShipAppointmentSlots
POST /inbound/v2024-03-20/shipments/{shipmentId}/selfShipAppointmentSlots/schedule
```

**Slot selection rules (Grow24 AI):**
- Skip Sunday slots
- Prefer 14:00–16:00 window
- Primary warehouse: DED3 → fallback: DED5

**scheduleSelfShipAppointment Request:**
```json
{
  "appointmentSlotId": "slot_xxx",
  "shipmentId": "shipment_xxx"
}
```

---

### STEP 14 — Get Item Labels (Barcode)
```
POST /inbound/v2024-03-20/marketplaceItemLabels
```
```json
{
  "labelType": "BARCODE_2D",
  "marketplaceId": "A21TJRUUN4KGV",
  "msku": "SKU-001",
  "pageType": "PackageLabel_Plain_Paper"
}
```

---

### STEP 15 — Delivery Challan (India Required)
```
GET /inbound/v2024-03-20/shipments/{shipmentId}/deliveryChallans
```

Returns PDF document URL for delivery challan.

---

## 📦 Box Weight Calculation (Grow24 AI Logic)

### Ayurved Category:
```
box_weight = (units_per_box × unit_weight_gm / 1000) + box_tare_kg
           = (100 × 50 / 1000) + 0.5
           = 5.0 + 0.5
           = 5.5 kg
```

### Salt Category:
```
box_weight = 9.0 kg (fixed — declared, no calculation)
units_per_box = 10
```

### Box Count Calculation:
```
boxes_needed = ceil(send_quantity / units_per_box)
```

---

## 🔢 Rate Limits
| Operation | Rate | Burst |
|-----------|------|-------|
| createInboundPlan | 0.5/sec | 1 |
| setPackingInformation | 0.5/sec | 1 |
| generatePlacementOptions | 0.5/sec | 1 |
| confirmPlacementOption | 0.5/sec | 1 |
| scheduleSelfShipAppointment | 0.5/sec | 1 |

**Use retry with exponential backoff. Max 3 retries.**

---

## ❌ Legacy API (v0) — DO NOT USE
```
Location: legacy/FBA_Inbound_v0.md
⛔ FORBIDDEN without explicit Msir approval
⛔ DO NOT import from legacy/ without permission
Reason: v2024-03-20 is complete replacement
```
