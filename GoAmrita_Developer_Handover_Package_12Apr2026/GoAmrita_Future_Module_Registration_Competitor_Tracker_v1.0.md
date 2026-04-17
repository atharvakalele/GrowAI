# Grow24 AI / GoAmrita - Future Module Registration: Competitor Tracker v1.0
**Project Name:** Grow24 AI (formerly GoAmrita)  
**Date:** 15 April 2026  
**Module Status:** Migrated by compatibility wrapper  
**AI-Only Rule:** Future AI tools must preserve legacy raw output and extend only through standard summaries unless approved.

---

# 1. MODULE IDENTITY

Feature ID:
```text
M01
```

Feature Key:
```text
competitor_tracker
```

Feature Name:
```text
Competitor Tracker
```

Module Group:
```text
market_intelligence
```

Primary Script:
```text
Grow24_AI/marketplaces/amazon/seller_api/market_intelligence/competitor_tracker_v1.0.py
```

---

# 2. BUSINESS PURPOSE

The Competitor Tracker detects competitor pressure, Buy Box risk, no-Buy-Box listings, and low-pressure opportunities.

It supports:
- Buy Box protection
- competitor pressure monitoring
- pricing review
- listing risk review
- revenue-at-risk visibility

Current action meaning:
- detector first
- action routing second
- should reuse shared action engines instead of creating competitor-only fix functions

---

# 3. MIGRATION DECISION

This module was originally created in the older project style.

It has now been moved to the future method using a compatibility wrapper pattern:

```text
Old raw competitor report stays unchanged.
New dashboard-facing summaries are created beside it.
Central report registry discovers the summaries.
```

This avoids breaking existing behavior while allowing future dashboards to consume the module.

The source code has been moved out of the beta `ClaudeCode/Python` area and into the dedicated Amazon marketplace architecture.

---

# 4. REQUIRED OUTPUTS

## Raw Output
```text
ClaudeCode/Report/<latest report folder>/Json/competitor_tracker_latest.json
ClaudeCode/Report/<latest report folder>/Json/competitor_tracker_<timestamp>.json
```

## Strategy Impact Dashboard Output
```text
ClaudeCode/Report/<latest report folder>/Json/impact_competitor_tracker_latest.json
ClaudeCode/Report/<latest report folder>/Json/impact_competitor_tracker_<timestamp>.json
```

## Activity Dashboard Output
```text
ClaudeCode/Report/<latest report folder>/Json/activity_competitor_tracker_latest.json
ClaudeCode/Report/<latest report folder>/Json/activity_competitor_tracker_<timestamp>.json
```

## Registry Output
```text
ClaudeCode/Report/<latest report folder>/Json/report_registry_latest.json
```

---

# 5. DASHBOARD PLACEMENT

Strategy Impact Dashboard:
- Section: `Critical Impact Alerts`
- Shows competitor risk, Buy Box status, revenue-at-risk, and low-pressure wins

Activity Dashboard:
- Section: `Run Status`
- Shows run status, input sources, output files, warnings, errors, and review items

---

# 6. STANDARD CONTRACTS USED

This module must follow:
- `GoAmrita_Future_JSON_Contract_v1.0.md`
- `GoAmrita_Future_Report_Registry_Standard_v1.0.md`
- `GoAmrita_Future_Dashboard_Rendering_Rules_v1.0.md`
- `GoAmrita_AI_Only_Development_Protocol_v1.0.md`

---

# 7. SAFETY RULES FOR FUTURE AI TOOLS

Do not remove:
- `competitor_tracker_latest.json`
- dated raw competitor history files
- existing `config_competitor.json`
- existing `config_features.json` competitor entry

Do not rewrite old raw output shape unless explicitly approved.

Allowed safe changes:
- improve impact summary mapping
- improve activity summary mapping
- add registry metadata
- add AI learning notes
- add dashboard display hints

Approval required before:
- auto-changing price
- auto-changing ads
- changing Buy Box recovery logic
- changing scheduler behavior
- migrating old historical reports

Preferred future action routing:
- pricing-related critical finding -> existing pricing action engine
- listing-risk critical finding -> existing listing/health recovery engine
- stock/availability critical finding -> existing stock/FBA action engine
- if no safe reusable action engine exists yet -> record action as pending/blocked

---

# 8. LATEST VALIDATION RESULT

Latest tested mode:
```text
python Grow24_AI/marketplaces/amazon/seller_api/market_intelligence/competitor_tracker_v1.0.py --top 30
```

Latest validation summary:
- 30 ASINs tracked
- 0 failed ASINs
- 1 no-Buy-Box risk
- 29 low-pressure opportunities
- impact summary generated
- activity summary generated
- report registry updated

---

# 9. FINAL RULE

**Competitor Tracker is now dashboard-ready by the new future method, but its old raw output remains protected.**
