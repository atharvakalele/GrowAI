# Grow24 AI / GoAmrita - Future Report Registry Standard v1.0
**Project Name:** Grow24 AI (formerly GoAmrita)  
**Date:** 15 April 2026  
**Purpose:** Standard registry/discovery layer for ALL NEW future modules/features

---

# 1. PURPOSE

Registry Entry is the dashboard discovery layer for future modules.

Without registry:
- reports remain scattered
- dashboard must guess file names
- display order becomes messy

With registry:
- dashboard knows what exists
- dashboard knows where to show it
- dashboard knows what matters most

---

# 2. HUMAN-FRIENDLY TEMPLATE

```md
# Report Registry Entry

## 1. Identity
- Feature ID:
- Feature Key:
- Feature Name:
- Module Group:

## 2. Report Availability
- Raw output file:
- Impact summary file:
- Activity summary file:
- Detail report file:
- Latest generated at:

## 3. Dashboard Visibility
- Show on Main Dashboard: Yes / No
- Show on Activity Dashboard: Yes / No
- Show on Homepage: Yes / No
- Main Dashboard section:
- Activity Dashboard section:

## 4. Importance
- Status:
- Impact level:
- Priority score:
- Strategic weight:
- Is critical: Yes / No

## 5. Display Rules
- Headline to show:
- Badge/color:
- Sort order:
- Collapse by default: Yes / No
- Pin to top when:

## 6. Review / Action State
- Needs review: Yes / No
- Needs approval: Yes / No
- Has warnings: Yes / No
- Has errors: Yes / No

## 7. Notes
- Dashboard note:
- Developer note:
- Migration note:
```

---

# 3. STRICT JSON TEMPLATE

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

# 4. CENTRAL REGISTRY FILE EXAMPLE

```json
{
  "schema_type": "report_registry",
  "schema_version": "1.0",
  "generated_at": "2026-04-15T12:00:00Z",
  "entries": [
    {
      "feature_id": "M01",
      "feature_key": "competitor_tracker",
      "feature_name": "Competitor Tracker",
      "module_group": "market_intelligence",
      "files": {
        "raw_output": "Grow24_AI/data/amazon/reports/latest/json/competitor_tracker_latest.json",
        "impact_summary": "Grow24_AI/data/amazon/reports/latest/json/impact_competitor_tracker_latest.json",
        "activity_summary": "Grow24_AI/data/amazon/reports/latest/json/activity_competitor_tracker_latest.json",
        "detail_report": "Grow24_AI/data/amazon/reports/15 April 2026/json/competitor_tracker_20260415_120000.json"
      },
      "generated_at": "2026-04-15T12:00:00Z",
      "dashboard_visibility": {
        "show_on_main": true,
        "show_on_activity": true,
        "show_on_home": true,
        "main_section": "Critical Business Risks",
        "activity_section": "Module Run Table"
      },
      "importance": {
        "status": "success",
        "impact_level": "high",
        "priority_score": 84,
        "strategic_weight": 9,
        "is_critical": true
      },
      "display_rules": {
        "headline": "1 buy box threat detected",
        "badge": "critical",
        "sort_order": 10,
        "collapse_by_default": false,
        "pin_to_top_when": ["buy_box_lost_count > 0"]
      },
      "review_state": {
        "needs_review": true,
        "needs_approval": false,
        "has_warnings": true,
        "has_errors": false
      },
      "notes": {
        "dashboard_note": "Show in main risk block",
        "developer_note": "",
        "migration_note": "Legacy modules not yet migrated"
      }
    }
  ]
}
```

---

# 5. REGISTRY RULES

- Dashboard should read registry, not guess file names
- Registry controls visibility, section, priority, and review state
- Registry is source of truth for future module discovery
- Main Dashboard should consume impact summary references
- Activity Dashboard should consume activity summary references
- Future registry should live under `Grow24_AI/data/amazon/reports/latest/json/`

---

*Future Report Registry Standard v1.0 | 15 April 2026*
