# Grow24 AI / GoAmrita - Future Module Registration Template v1.0
**Project Name:** Grow24 AI (formerly GoAmrita)  
**Date:** 15 April 2026  
**Purpose:** Required registration template for ALL NEW future modules/features

---

# 1. RULE

No new future module should start coding until its registration is defined.

This registration is the planning layer before build.

---

# 2. HUMAN-FRIENDLY TEMPLATE

```md
# New Feature Registration

## 1. Basic Identity
- Feature ID:
- Feature Key:
- Feature Name:
- Module Group:
- Phase:

## 2. Why This Feature Exists
- Business goal:
- Problem it solves:
- Expected business impact:
- Why it matters now:

## 3. Inputs
- Main data sources:
- APIs used:
- Required dependency modules:
- Minimum data needed to run:

## 4. Outputs
- Raw output file(s):
- Impact summary needed: Yes/No
- Activity summary needed: Yes/No
- Registry entry needed: Yes/No
- Optional detail report:

## 5. Dashboard Placement
- Show on Main Dashboard / Activity Dashboard / Both:
- Main Dashboard section:
- Activity Dashboard section:
- Should appear on homepage: Yes/No

## 6. Main Metrics
- Business/impact metrics:
- Activity/operation metrics:
- Headline metric:
- Risk metric:

## 7. Approval and Safety
- Mode: Recommend Only / Semi-Auto / Full-Auto
- User approval required: Yes/No
- Auto action allowed: Yes/No
- Risk level: Low / Medium / High / Critical
- Rollback needed: Yes/No

## 8. Run Logic
- Schedule type:
- Freshness:
- Priority level:
- When should it be considered urgent:
- When should it be considered review-needed:

## 9. Notes
- Developer notes:
- Future migration notes:
- Legacy compatibility notes:
```

---

# 3. STRICT JSON TEMPLATE

```json
{
  "feature_id": "",
  "feature_key": "",
  "feature_name": "",
  "module_group": "",
  "phase": "",
  "status": "planned",

  "business_goal": "",
  "problem_statement": "",
  "expected_business_impact": [],

  "input_sources": [],
  "api_dependencies": [],
  "depends_on": [],
  "minimum_data_requirements": [],

  "output_files": {
    "raw_outputs": [],
    "impact_summary": "",
    "activity_summary": "",
    "detail_report": "",
    "registry_entry": ""
  },

  "dashboard_targets": [],
  "dashboard_placement": {
    "main_section": "",
    "activity_section": "",
    "show_on_home": true
  },

  "impact_metrics": [],
  "activity_metrics": [],
  "headline_metric": "",
  "risk_metric": "",

  "approval_mode": "recommend_only",
  "user_approval_required": false,
  "auto_action_allowed": false,
  "risk_level": "medium",
  "rollback_required": false,

  "schedule_type": "",
  "freshness_hours": 24,
  "priority_score_base": 50,
  "urgent_when": [],
  "needs_review_when": [],

  "developer_notes": "",
  "future_migration_notes": "",
  "legacy_compatibility_notes": ""
}
```

---

# 4. MINIMUM REQUIRED FIELDS

Every registration must define at least:
- feature id
- feature key
- feature name
- module group
- dashboard target
- impact metrics
- activity metrics
- approval mode
- risk level
- output file names

---

*Future Module Registration Template v1.0 | 15 April 2026*
