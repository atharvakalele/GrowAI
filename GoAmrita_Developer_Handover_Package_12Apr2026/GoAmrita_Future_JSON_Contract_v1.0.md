# Grow24 AI / GoAmrita - Future JSON Contract v1.0
**Project Name:** Grow24 AI (formerly GoAmrita)  
**Date:** 15 April 2026  
**Purpose:** Implementation-ready JSON contract for ALL NEW future modules/features

---

# 1. PURPOSE

This document defines the exact JSON contracts future modules must follow for dashboard/report integration.

It applies only to:
- new future modules
- new future dashboard-facing reports
- new future registry entries

It does **not** force changes to existing/legacy JSON files.

---

# 2. CONTRACTS DEFINED

Future modules may keep raw JSON in any module-specific shape.

But all dashboard-facing outputs must follow these contracts:

1. Impact Summary Contract
2. Activity Summary Contract
3. Registry Entry Contract
4. Central Report Registry Contract

---

# 3. COMMON ALLOWED VALUES

## `status`
Allowed:
- `success`
- `partial`
- `warning`
- `failed`

## `impact_level`
Allowed:
- `low`
- `medium`
- `high`
- `critical`

## `run_mode`
Allowed:
- `manual`
- `scheduled`
- `event`
- `retry`

## `dashboard_targets`
Allowed:
- `main`
- `activity`
- `both`

## `module_group`
Allowed:
- `core_engine`
- `ads_optimization`
- `market_intelligence`
- `growth_engine`
- `listing_health`
- `pricing_profit`
- `inventory_fba`
- `review_feedback`
- `alerts_protection`
- `automation_control`
- `integration_sync`
- `ai_learning`

## `schema_version`
Current:
- `1.0`

---

# 4. FIELD NAMING RULES

Use:
- snake_case keys
- ISO 8601 timestamps
- relative report paths from the current report folder when possible
- `_rs` suffix for rupee values
- `_pct` suffix for percentages
- `_count` suffix for counts
- `_sec` suffix for seconds
- boolean values as `true` / `false`

Avoid:
- mixed casing
- unclear abbreviations
- UI-only labels in raw metrics
- hardcoded absolute paths unless required by local app integration

---

# 5. IMPACT SUMMARY CONTRACT

## Purpose
Used by:
```text
Strategy Impact Dashboard / Main Dashboard
```

Answers:
```text
What business impact happened?
```

## Required Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `schema_type` | string | yes | Must be `impact_summary` |
| `schema_version` | string | yes | Current `1.0` |
| `feature_id` | string | yes | MASTER feature ID if available |
| `feature_key` | string | yes | Stable machine key |
| `feature_name` | string | yes | Human readable name |
| `module_group` | string | yes | Must use allowed module group |
| `generated_at` | string | yes | ISO 8601 |
| `period` | string | yes | `daily`, `weekly`, `manual`, etc. |
| `status` | string | yes | allowed status |
| `impact_level` | string | yes | allowed impact level |
| `business_areas` | array | yes | e.g. `profit`, `buy_box`, `rank` |
| `headline` | string | yes | Owner-facing summary |
| `summary_metrics` | object | yes | standard business metrics |
| `positive_impacts` | array | yes | may be empty |
| `negative_impacts` | array | yes | may be empty |
| `top_winners` | array | yes | may be empty |
| `top_risks` | array | yes | may be empty |
| `detail_ref` | object | yes | raw/detail file references |

## Optional Fields
- `ai_learning`
- `ai_action_summary`
- `recommendations`
- `confidence`
- `priority_score`
- `notes`

## Standard JSON Shape

```json
{
  "schema_type": "impact_summary",
  "schema_version": "1.0",
  "feature_id": "",
  "feature_key": "",
  "feature_name": "",
  "module_group": "",
  "generated_at": "",
  "period": "",
  "status": "success",
  "impact_level": "medium",
  "business_areas": [],
  "headline": "",
  "summary_metrics": {
    "profit_impact_rs": 0,
    "loss_prevented_rs": 0,
    "waste_blocked_rs": 0,
    "revenue_protected_rs": 0,
    "rank_up_count": 0,
    "rank_down_count": 0,
    "buy_box_won_count": 0,
    "buy_box_lost_count": 0,
    "conversion_up_count": 0,
    "conversion_down_count": 0,
    "organic_gain_count": 0,
    "organic_decline_count": 0
  },
  "positive_impacts": [],
  "negative_impacts": [],
  "top_winners": [],
  "top_risks": [],
  "ai_action_summary": {
    "headline": "",
    "actions_identified": 0,
    "actions_executed": 0,
    "expected_sales_protected_rs": 0,
    "items": []
  },
  "ai_learning": {
    "new_rule_learned": false,
    "rule_promoted_count": 0,
    "confidence": 0.0,
    "notes": ""
  },
  "detail_ref": {
    "raw_file": "",
    "detail_file": "",
    "supporting_report": ""
  }
}
```

## `ai_action_summary` Rule
- Use only when the module took action, routed action, or can clearly estimate benefit from AI action
- Keep one reusable AI-benefit block only
- Do not invent second duplicate benefit objects for the same module
- Use this for compact dashboard benefit summary and item-level AI action detail

---

# 6. ACTIVITY SUMMARY CONTRACT

## Purpose
Used by:
```text
Activity Dashboard
```

Answers:
```text
What system activity happened?
```

## Required Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `schema_type` | string | yes | Must be `activity_summary` |
| `schema_version` | string | yes | Current `1.0` |
| `feature_id` | string | yes | MASTER feature ID if available |
| `feature_key` | string | yes | Stable machine key |
| `feature_name` | string | yes | Human readable name |
| `module_group` | string | yes | Must use allowed module group |
| `run_id` | string | yes | Stable unique run id |
| `generated_at` | string | yes | ISO 8601 |
| `status` | string | yes | allowed status |
| `run_mode` | string | yes | allowed run mode |
| `duration_sec` | number | yes | runtime seconds |
| `freshness_hours` | number | yes | freshness window |
| `needs_review` | boolean | yes | true/false |
| `input_sources` | array | yes | inputs used |
| `output_files` | array | yes | files created |
| `counts` | object | yes | operation counts |
| `run_events` | array | yes | may be empty |
| `warnings_list` | array | yes | may be empty |
| `errors_list` | array | yes | may be empty |
| `review_items` | object | yes | user/dev/blocked arrays |

## Optional Fields
- `retry_count`
- `api_calls_count`
- `rate_limit_wait_sec`
- `source_report_folder`
- `notes`

## Standard JSON Shape

```json
{
  "schema_type": "activity_summary",
  "schema_version": "1.0",
  "feature_id": "",
  "feature_key": "",
  "feature_name": "",
  "module_group": "",
  "run_id": "",
  "generated_at": "",
  "status": "success",
  "run_mode": "scheduled",
  "duration_sec": 0,
  "freshness_hours": 24,
  "needs_review": false,
  "input_sources": [],
  "output_files": [],
  "counts": {
    "items_scanned": 0,
    "items_processed": 0,
    "alerts_generated": 0,
    "approvals_needed": 0,
    "warnings": 0,
    "errors": 0
  },
  "run_events": [],
  "warnings_list": [],
  "errors_list": [],
  "review_items": {
    "user_review": [],
    "developer_review": [],
    "blocked_items": []
  }
}
```

---

# 7. REGISTRY ENTRY CONTRACT

## Purpose
Used by:
```text
Dashboard discovery layer
```

Answers:
```text
What report exists, where is it, and where should it show?
```

## Required Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `schema_type` | string | yes | Must be `registry_entry` |
| `schema_version` | string | yes | Current `1.0` |
| `feature_id` | string | yes | MASTER feature ID if available |
| `feature_key` | string | yes | Stable machine key |
| `feature_name` | string | yes | Human readable name |
| `module_group` | string | yes | Must use allowed module group |
| `files` | object | yes | raw/impact/activity/detail paths |
| `generated_at` | string | yes | ISO 8601 |
| `dashboard_visibility` | object | yes | where to show |
| `importance` | object | yes | status/priority/critical |
| `display_rules` | object | yes | headline/badge/sort |
| `review_state` | object | yes | review/approval/errors/warnings |

## Standard JSON Shape

```json
{
  "schema_type": "registry_entry",
  "schema_version": "1.0",
  "feature_id": "",
  "feature_key": "",
  "feature_name": "",
  "module_group": "",
  "files": {
    "raw_output": "",
    "impact_summary": "",
    "activity_summary": "",
    "detail_report": ""
  },
  "generated_at": "",
  "dashboard_visibility": {
    "show_on_main": true,
    "show_on_activity": true,
    "show_on_home": true,
    "main_section": "",
    "activity_section": ""
  },
  "importance": {
    "status": "success",
    "impact_level": "medium",
    "priority_score": 50,
    "strategic_weight": 5,
    "is_critical": false
  },
  "display_rules": {
    "headline": "",
    "badge": "",
    "sort_order": 50,
    "collapse_by_default": false,
    "pin_to_top_when": []
  },
  "review_state": {
    "needs_review": false,
    "needs_approval": false,
    "has_warnings": false,
    "has_errors": false
  },
  "notes": {
    "dashboard_note": "",
    "developer_note": "",
    "migration_note": ""
  }
}
```

---

# 8. CENTRAL REPORT REGISTRY CONTRACT

## Purpose
The dashboard should read this central registry to discover future module reports.

## Standard File Name

```text
Json/report_registry_latest.json
```

## Required Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `schema_type` | string | yes | Must be `report_registry` |
| `schema_version` | string | yes | Current `1.0` |
| `generated_at` | string | yes | ISO 8601 |
| `entries` | array | yes | list of registry entries |

## Standard JSON Shape

```json
{
  "schema_type": "report_registry",
  "schema_version": "1.0",
  "generated_at": "",
  "entries": []
}
```

---

# 9. FILE NAMING CONTRACT

For future modules:

## Base Report Root
```text
Grow24_AI/data/amazon/reports/
```

## Latest JSON Root
```text
Grow24_AI/data/amazon/reports/latest/json/
```

## Dated JSON Root
```text
Grow24_AI/data/amazon/reports/<dated folder>/json/
```

## Raw Output
```text
Grow24_AI/data/amazon/reports/latest/json/<feature_key>_latest.json
Grow24_AI/data/amazon/reports/<dated folder>/json/<feature_key>_<timestamp>.json
```

## Impact Summary
```text
Grow24_AI/data/amazon/reports/latest/json/impact_<feature_key>_latest.json
Grow24_AI/data/amazon/reports/<dated folder>/json/impact_<feature_key>_<timestamp>.json
```

## Activity Summary
```text
Grow24_AI/data/amazon/reports/latest/json/activity_<feature_key>_latest.json
Grow24_AI/data/amazon/reports/<dated folder>/json/activity_<feature_key>_<timestamp>.json
```

## Registry
```text
Grow24_AI/data/amazon/reports/latest/json/report_registry_latest.json
```

---

# 10. VALIDATION RULES

Future module output should be considered invalid if:
- required fields are missing
- `schema_type` is wrong
- `schema_version` is missing
- `status` uses non-standard value
- `module_group` is not from approved list
- dashboard file references are empty when dashboard visibility is enabled
- `generated_at` is missing

## Recommended behavior on invalid output
- Activity Dashboard should show module as `warning` or `failed`
- Main Dashboard should not show incomplete business impact
- Registry should record issue in `review_state.has_errors`

---

# 11. EXAMPLE: COMPETITOR TRACKER

## Impact Summary Example

```json
{
  "schema_type": "impact_summary",
  "schema_version": "1.0",
  "feature_id": "M01",
  "feature_key": "competitor_tracker",
  "feature_name": "Competitor Tracker",
  "module_group": "market_intelligence",
  "generated_at": "2026-04-15T10:30:00Z",
  "period": "daily",
  "status": "success",
  "impact_level": "high",
  "business_areas": ["buy_box", "rank", "revenue_protection"],
  "headline": "1 critical Buy Box risk found; 4 ASINs have low competitor pressure.",
  "summary_metrics": {
    "profit_impact_rs": 0,
    "loss_prevented_rs": 2500,
    "waste_blocked_rs": 0,
    "revenue_protected_rs": 4200,
    "rank_up_count": 0,
    "rank_down_count": 1,
    "buy_box_won_count": 12,
    "buy_box_lost_count": 1,
    "conversion_up_count": 0,
    "conversion_down_count": 0,
    "organic_gain_count": 0,
    "organic_decline_count": 0
  },
  "positive_impacts": ["4 ASINs had low competitor pressure"],
  "negative_impacts": ["1 ASIN has no Buy Box"],
  "top_winners": [],
  "top_risks": [
    {
      "entity_type": "asin",
      "entity_id": "B0XXXXXXX",
      "label": "Example Product",
      "impact_note": "No Buy Box detected",
      "impact_value": "High revenue risk"
    }
  ],
  "ai_learning": {
    "new_rule_learned": false,
    "rule_promoted_count": 0,
    "confidence": 0.82,
    "notes": ""
  },
  "detail_ref": {
    "raw_file": "Json/competitor_tracker_latest.json",
    "detail_file": "Json/competitor_tracker_20260415_103000.json",
    "supporting_report": ""
  }
}
```

## Activity Summary Example

```json
{
  "schema_type": "activity_summary",
  "schema_version": "1.0",
  "feature_id": "M01",
  "feature_key": "competitor_tracker",
  "feature_name": "Competitor Tracker",
  "module_group": "market_intelligence",
  "run_id": "M01_20260415_103000",
  "generated_at": "2026-04-15T10:30:00Z",
  "status": "success",
  "run_mode": "scheduled",
  "duration_sec": 94,
  "freshness_hours": 24,
  "needs_review": true,
  "input_sources": [
    "Json/sp_product_ads_list.json",
    "Json/sp_advertisedproduct_daily.json",
    "SP-API Pricing v2022-05-01"
  ],
  "output_files": [
    "Json/competitor_tracker_latest.json",
    "Json/impact_competitor_tracker_latest.json",
    "Json/activity_competitor_tracker_latest.json"
  ],
  "counts": {
    "items_scanned": 30,
    "items_processed": 30,
    "alerts_generated": 1,
    "approvals_needed": 0,
    "warnings": 1,
    "errors": 0
  },
  "run_events": [
    "Loaded top ASINs",
    "Fetched competitive summary batches",
    "Saved latest report"
  ],
  "warnings_list": ["1 ASIN returned no Buy Box"],
  "errors_list": [],
  "review_items": {
    "user_review": ["Review ASIN with no Buy Box"],
    "developer_review": [],
    "blocked_items": []
  }
}
```

---

# 12. FINAL RULE

For future modules:

```text
Raw JSON can be custom.
Dashboard JSON must follow this contract.
```

This protects dashboard scalability and prevents future JSON confusion.

---

*Future JSON Contract v1.0 | 15 April 2026*  
*For NEW future modules only | Legacy JSON remains unchanged until planned migration phase*
