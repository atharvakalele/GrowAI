# Grow24 AI / GoAmrita - Future Report Templates v1.0
**Project Name:** Grow24 AI (formerly GoAmrita)  
**Date:** 15 April 2026  
**Purpose:** Standard Impact Summary and Activity Summary templates for ALL NEW future modules/features

---

# 1. IMPACT SUMMARY

## Purpose
Impact Summary is for the **Main Dashboard**.

It must explain:
- what changed in business
- what improved
- what got worse
- what value was protected, gained, or lost

It must NOT focus on:
- stack traces
- retry logs
- scheduler mechanics
- technical noise

## Human-Friendly Template

```md
# Impact Summary

## 1. Identity
- Feature ID:
- Feature Key:
- Feature Name:
- Module Group:
- Generated At:
- Period:

## 2. Overall Impact
- Status:
- Impact Level: Low / Medium / High / Critical
- Business Areas Affected:
- Headline:

## 3. Main Business Metrics
- Profit impact:
- Loss prevented:
- Waste blocked:
- Revenue protected:
- Rank up count:
- Rank down count:
- Buy Box won count:
- Buy Box lost count:
- Conversion up/down:
- Organic impact:

## 4. Positive Outcomes
- Outcome 1
- Outcome 2
- Outcome 3

## 5. Negative Outcomes / Risks
- Risk 1
- Risk 2
- Risk 3

## 6. Top Winners
- Entity:
- Why it is a winner:
- Measured impact:

## 7. Top Risks
- Entity:
- Why it is at risk:
- Measured impact:

## 8. AI / Learning Effect
- New learning found:
- Rule promoted:
- Confidence:
- Notes:

## 9. AI Action Benefit
- Headline:
- Actions identified:
- Actions executed:
- Expected sales protected:
- Item-level AI action details:

## 10. Detail Reference
- Raw file:
- Detail file:
- Supporting report:
```

## Strict JSON Template

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

  "top_winners": [
    {
      "entity_type": "",
      "entity_id": "",
      "label": "",
      "impact_note": "",
      "impact_value": ""
    }
  ],

  "top_risks": [
    {
      "entity_type": "",
      "entity_id": "",
      "label": "",
      "impact_note": "",
      "impact_value": ""
    }
  ],

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

---

# 2. ACTIVITY SUMMARY

## Purpose
Activity Summary is for the **Activity Dashboard**.

It must explain:
- did module run
- what inputs it used
- what files it created
- what warnings/errors happened
- what needs review

It must NOT focus on:
- business storytelling
- strategic conclusions
- commercial interpretation

## Human-Friendly Template

```md
# Activity Summary

## 1. Identity
- Feature ID:
- Feature Key:
- Feature Name:
- Module Group:
- Run ID:
- Generated At:

## 2. Run Status
- Status:
- Run mode: Manual / Scheduled / Event / Retry
- Duration:
- Freshness:
- Needs review: Yes / No

## 3. Inputs Used
- Input source 1
- Input source 2
- API source 1

## 4. Outputs Created
- Raw file:
- Impact summary file:
- Activity summary file:
- Extra report file:

## 5. Processing Counts
- Items scanned:
- Items processed:
- Alerts generated:
- Approvals needed:
- Warnings:
- Errors:

## 6. Run Events
- Event 1
- Event 2
- Event 3

## 7. Warnings
- Warning 1
- Warning 2

## 8. Errors
- Error 1
- Error 2

## 9. Review Items
- What needs user review:
- What needs developer review:
- What is blocked:
```

## Strict JSON Template

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

# 3. COMMON STATUS STANDARDS

## Status
- `success`
- `partial`
- `warning`
- `failed`

## Impact Level
- `low`
- `medium`
- `high`
- `critical`

## Run Mode
- `manual`
- `scheduled`
- `event`
- `retry`

---

*Future Report Templates v1.0 | 15 April 2026*
