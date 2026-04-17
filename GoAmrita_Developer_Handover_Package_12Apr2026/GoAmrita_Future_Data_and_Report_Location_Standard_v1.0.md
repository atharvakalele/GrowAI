# Grow24 AI / GoAmrita - Future Data and Report Location Standard v1.0
**Project Name:** Grow24 AI (formerly GoAmrita)  
**Date:** 15 April 2026  
**Purpose:** Permanent storage standard for future module data, reports, and dashboard-ready files

---

# 1. CORE RULE

Future code must live in `Grow24_AI`.

Future data and reports must also live in `Grow24_AI`.

The permanent main data root is:

```text
Grow24_AI/data/
```

For Amazon marketplace work, the main marketplace data root is:

```text
Grow24_AI/data/amazon/
```

The main future report root is:

```text
Grow24_AI/data/amazon/reports/
```

---

# 2. MAIN FOLDER STRUCTURE

Use this structure for future Amazon reporting:

```text
Grow24_AI/
  data/
    amazon/
      reports/
        latest/
          json/
          excel/
          html/
        <dated folder>/
          json/
          excel/
          html/
```

Recommended dated folder format:

```text
15 April 2026
```

This keeps the system human-readable and compatible with the existing report style.

---

# 3. WHAT GOES WHERE

## Stable dashboard-readable latest files

Use:

```text
Grow24_AI/data/amazon/reports/latest/json/
```

This is where the dashboard/orchestrator should read the most recent machine-readable report outputs.

Typical files:
- `<feature_key>_latest.json`
- `impact_<feature_key>_latest.json`
- `activity_<feature_key>_latest.json`
- `report_registry_latest.json`

## Historical archive files

Use:

```text
Grow24_AI/data/amazon/reports/<dated folder>/json/
```

Typical files:
- `<feature_key>_<timestamp>.json`
- `impact_<feature_key>_<timestamp>.json`
- `activity_<feature_key>_<timestamp>.json`

## Excel outputs

Use:

```text
Grow24_AI/data/amazon/reports/latest/excel/
Grow24_AI/data/amazon/reports/<dated folder>/excel/
```

## HTML outputs

Use:

```text
Grow24_AI/data/amazon/reports/latest/html/
Grow24_AI/data/amazon/reports/<dated folder>/html/
```

---

# 4. DASHBOARD READING RULE

Future dashboards should prefer reading:

```text
Grow24_AI/data/amazon/reports/latest/json/report_registry_latest.json
```

Then follow registry references to the other latest files.

The dashboard should not guess file names from random folders.

---

# 5. MODULE OUTPUT RULE

Every future module should write to both:

1. latest stable location
2. dated archive location

Example for competitor tracker:

```text
Grow24_AI/data/amazon/reports/latest/json/competitor_tracker_latest.json
Grow24_AI/data/amazon/reports/latest/json/impact_competitor_tracker_latest.json
Grow24_AI/data/amazon/reports/latest/json/activity_competitor_tracker_latest.json
Grow24_AI/data/amazon/reports/latest/json/report_registry_latest.json

Grow24_AI/data/amazon/reports/15 April 2026/json/competitor_tracker_20260415_120000.json
Grow24_AI/data/amazon/reports/15 April 2026/json/impact_competitor_tracker_20260415_120000.json
Grow24_AI/data/amazon/reports/15 April 2026/json/activity_competitor_tracker_20260415_120000.json
```

---

# 6. COMPATIBILITY BRIDGE RULE

Current legacy/beta dashboard storage still exists under:

```text
ClaudeCode/Report/
```

That old location may continue temporarily only as a migration bridge.

But future architecture must treat it as temporary, not permanent.

Do not design new modules assuming `ClaudeCode/Report` is the final storage home.

---

# 7. AI TOOL RULE

Before adding a new future module, the AI tool must check:

- does `Grow24_AI/data/amazon/reports/` exist?
- does `latest/json/` exist?
- does the current dated folder exist?

If not, create the required folders before writing outputs.

---

# 8. FINAL RULE

**Future code lives in `Grow24_AI`. Future report/data output also lives in `Grow24_AI`.**

For Amazon modules, the main report folder is:

```text
Grow24_AI/data/amazon/reports/
```

