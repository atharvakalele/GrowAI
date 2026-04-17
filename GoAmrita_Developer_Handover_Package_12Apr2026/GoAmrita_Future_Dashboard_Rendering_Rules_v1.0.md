# Grow24 AI / GoAmrita - Future Dashboard Rendering Rules v1.0
**Project Name:** Grow24 AI (formerly GoAmrita)  
**Date:** 15 April 2026  
**Purpose:** Rendering rules for future Strategy Impact Dashboard and Activity Dashboard

---

# 1. PURPOSE

This document defines how future dashboards should render standardized future module outputs.

It tells developers:
- what file to read
- how to sort items
- how to choose badges/colors
- how to display impact cards
- how to display activity rows
- how to handle errors/warnings

This applies only to future dashboard/report architecture.

---

# 2. DATA SOURCES FOR DASHBOARD RENDERING

## Strategy Impact Dashboard
Primary input:
```text
Impact Summary
```

Discovered through:
```text
Report Registry
```

## Activity Dashboard
Primary input:
```text
Activity Summary
```

Discovered through:
```text
Report Registry
```

## Raw Output
Raw output is for:
- drill-down
- detail view
- debugging
- advanced analysis

Raw output should not be the main source for dashboard cards unless explicitly needed.

---

# 3. REGISTRY-FIRST RULE

Future dashboards should discover reports through:

```text
Json/report_registry_latest.json
```

Dashboard should not:
- guess file names
- hardcode every module file
- scan random JSON files and infer meaning

Registry decides:
- visibility
- section placement
- priority
- critical state
- review state
- file references

---

# 4. STRATEGY IMPACT DASHBOARD RENDERING

## Goal
Render business outcome first.

## Render from
- `impact_summary`
- registry `importance`
- registry `dashboard_visibility`
- optional `ai_action_summary` inside `impact_summary`

## AI Benefit Rendering Rule
- Reuse one AI benefit area per module only
- Do not render duplicate AI cards and duplicate AI detail sections with the same story repeated
- Summary card may show one short AI benefit value
- Detail area may show AI action rows, exact items, and execution detail
- If no meaningful AI action benefit exists, do not force an empty AI benefit block
- registry `display_rules`

## Recommended card fields
- headline
- impact level
- priority score
- key metric
- top risk / top winner
- generated time
- detail link

## Do not show by default
- stack traces
- API retries
- raw file paths
- technical logs
- long processing details

---

# 5. ACTIVITY DASHBOARD RENDERING

## Goal
Render system activity and operational state.

## Render from
- `activity_summary`
- registry `review_state`
- registry `importance.status`
- registry `files`

## Recommended row/card fields
- feature name
- status
- run mode
- duration
- last generated time
- items processed
- warnings count
- errors count
- needs review
- output files

## Do not show by default
- profit storytelling
- strategic business conclusions
- owner-level impact summaries

---

# 6. SORTING RULES

## Strategy Impact Dashboard sort order

Sort by:
1. `importance.is_critical = true`
2. highest `importance.priority_score`
3. `review_state.needs_review = true`
4. newest `generated_at`
5. configured `display_rules.sort_order`

## Activity Dashboard sort order

Sort by:
1. `review_state.has_errors = true`
2. `review_state.needs_review = true`
3. status: `failed`, `warning`, `partial`, `success`
4. newest `generated_at`
5. configured `display_rules.sort_order`

---

# 7. BADGE RULES

Use consistent badge names:

## Status badges
- `success`
- `partial`
- `warning`
- `failed`

## Impact badges
- `low`
- `medium`
- `high`
- `critical`

## Review badges
- `review`
- `approval`
- `blocked`
- `info`

## Badge meaning
- `critical` = immediate business risk
- `failed` = module did not complete
- `warning` = module completed but needs attention
- `review` = human review needed
- `approval` = explicit approval needed

---

# 8. COLOR GUIDANCE

Suggested colors:

- `success` / `low positive`: green
- `partial`: blue
- `warning`: orange
- `failed`: red
- `critical`: red
- `review`: orange
- `approval`: purple or amber
- `info`: gray/blue

Do not rely only on color.

Always pair color with:
- text label
- icon/badge
- clear wording

---

# 9. EMPTY STATE RULES

## Strategy Impact Dashboard
If no impact summaries exist:
```text
No future-standard impact reports available yet.
Legacy reports may still exist separately.
```

## Activity Dashboard
If no activity summaries exist:
```text
No future-standard activity reports available yet.
Legacy logs may still exist separately.
```

This avoids confusing users during transition from legacy to future standard.

---

# 10. ERROR DISPLAY RULES

## Strategy Impact Dashboard
If impact summary is invalid:
- do not show it as business truth
- show warning in system/activity area
- optionally show "Impact unavailable"

## Activity Dashboard
If activity summary is invalid:
- show module as `warning` or `failed`
- show validation issue
- show source registry entry if available

## Registry errors
If registry is missing or invalid:
- Activity Dashboard should show registry load error
- Strategy Impact Dashboard should show safe empty state

---

# 11. REVIEW / APPROVAL DISPLAY RULES

If `review_state.needs_review = true`:
- pin item higher
- show `review` badge
- provide detail link

If `review_state.needs_approval = true`:
- show `approval` badge
- do not auto-execute anything
- show approval action only if approval system supports it

If `review_state.has_errors = true`:
- show error badge
- show developer/operator detail in Activity Dashboard
- do not show as positive business impact

---

# 12. DETAIL VIEW RULES

Each dashboard card/row should allow drill-down to:
- impact summary file
- activity summary file
- raw output file
- detail report file if available

Default detail order:
1. summary view
2. top risks/winners or warnings/errors
3. raw/detail file links
4. full JSON viewer if needed

---

# 13. REFRESH / FRESHNESS RULES

Use:
- `generated_at`
- `freshness_hours`
- registry status

Display:
- fresh
- stale
- unknown

Suggested logic:
```text
if age_hours <= freshness_hours -> fresh
if age_hours > freshness_hours -> stale
if missing timestamp -> unknown
```

Stale reports should not disappear.
They should show a stale badge.

---

# 14. HOME PAGE LIMITS

To keep the dashboard clean:

## Strategy Impact Dashboard home
- show top 5 critical risks
- show top 5 winners
- show top 5 product risks
- collapse low-priority modules

## Activity Dashboard home
- show all failed/warning modules
- show pending reviews
- show latest 10 activities
- collapse successful normal runs

---

# 15. LEGACY TRANSITION RULE

During transition:
- future-standard reports come from registry
- legacy reports can still be shown in legacy sections
- do not mix legacy raw JSON into future cards without wrapper summaries

If legacy module has no wrapper:
```text
Show only in legacy/old report area, not future-standard dashboard cards.
```

---

# 16. FINAL RENDERING RULE

```text
Strategy Impact Dashboard shows business truth.
Activity Dashboard shows system truth.
Registry tells both dashboards what exists.
```

This is the core rendering contract.

---

*Future Dashboard Rendering Rules v1.0 | 15 April 2026*  
*For future dashboard/report architecture only*
