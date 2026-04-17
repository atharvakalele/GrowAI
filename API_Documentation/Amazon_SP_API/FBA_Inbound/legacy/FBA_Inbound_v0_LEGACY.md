# ⛔ FBA Inbound API v0 — LEGACY — DO NOT USE

## 🔴 WARNING
```
THIS IS THE OLD API. IT IS DEPRECATED.
DO NOT USE THIS IN ANY NEW CODE.
DO NOT IMPORT THIS FILE WITHOUT MSIR'S EXPLICIT APPROVAL.

USE INSTEAD: FBA_Inbound_v2024-03-20.md
```

## Why deprecated?
- v2024-03-20 is the complete replacement
- v0 will eventually be shut down by Amazon
- v0 and v2024-03-20 workflows are incompatible — do not mix

## Legacy Endpoints (reference only)
- POST /fba/inbound/v0/shipments
- GET  /fba/inbound/v0/shipments
- PUT  /fba/inbound/v0/shipments/{shipmentId}/items
- GET  /fba/inbound/v0/operations/{operationId}

## If you MUST use v0 (only with Msir approval):
1. Get explicit written approval from Msir
2. Document WHY v2024-03-20 cannot be used
3. Add comment in code: # LEGACY v0 — Approved by Msir on [date]
