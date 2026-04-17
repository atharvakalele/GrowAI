# Grow24 AI / GoAmrita - Future Dashboard Code Location Standard v1.0
**Project Name:** Grow24 AI (formerly GoAmrita)  
**Date:** 15 April 2026  
**Purpose:** Permanent folder rules for future dashboard, web panel, and dashboard-serving code

---

# 1. CORE RULE

`ClaudeCode/Python` is the old beta/minimum-working-tool area.

Future dashboard/web production code must not be created there.

Dashboard/web code is not a marketplace module.

It is shared product/platform code, so it belongs under:

```text
Grow24_AI/core/
```

---

# 2. MAIN DASHBOARD CODE ROOT

The permanent future dashboard code root should be:

```text
Grow24_AI/core/dashboard/
```

This folder should contain shared dashboard/server logic for:
- Strategy Impact Dashboard
- Activity Dashboard
- dashboard API endpoints
- dashboard HTML/templates
- dashboard data readers
- dashboard rendering helpers

---

# 3. RECOMMENDED SUBFOLDERS

Use this structure for future dashboard/web work:

```text
Grow24_AI/
  core/
    dashboard/
      server/
      readers/
      renderers/
      templates/
      static/
      utils/
```

Suggested purpose:

- `server/`
  - Flask/FastAPI/dashboard server entry files
  - dashboard API routes

- `readers/`
  - report registry readers
  - impact summary readers
  - activity summary readers
  - compatibility readers for old report folders if needed

- `renderers/`
  - dashboard card builders
  - table builders
  - badge/status mapping
  - section layout helpers

- `templates/`
  - HTML templates
  - shared page fragments

- `static/`
  - CSS
  - JS
  - images/icons

- `utils/`
  - date formatting
  - path helpers
  - safe HTML helpers

---

# 4. WHAT MUST NOT GO IN MARKETPLACE MODULE FOLDERS

Do not place shared dashboard/web code under:

```text
Grow24_AI/marketplaces/amazon/
```

unless the file is truly marketplace-specific input/output logic.

Examples of marketplace-specific code allowed there:
- Amazon report readers
- Amazon marketplace adapters
- Amazon-specific data translators

Examples of shared dashboard code that must stay in `Grow24_AI/core/dashboard/`:
- dashboard server
- dashboard templates
- generic dashboard UI rendering
- shared summary card logic
- generic report registry display logic

---

# 5. COMPATIBILITY BRIDGE RULE

Current live dashboard code still exists in:

```text
ClaudeCode/Python/
```

That is allowed temporarily as a compatibility bridge.

But future dashboard/web architecture must treat that location as temporary, not permanent.

Do not build major new dashboard features there if a clean `Grow24_AI/core/dashboard/` location is available.

---

# 6. DATA READING RULE

Future dashboard code under `Grow24_AI/core/dashboard/` should read future dashboard data from:

```text
Grow24_AI/data/amazon/reports/latest/json/report_registry_latest.json
```

It may temporarily support old compatibility readers for:

```text
ClaudeCode/Report/
```

But only as a migration bridge.

---

# 7. CURRENT PROJECT DECISION

Current live dashboard code is still in the beta area.

Future plan:

```text
Current bridge:
Grow24_AI/core/dashboard/dashboard_server_v1.1.py

Future permanent home:
Grow24_AI/core/dashboard/server/
```

Do not migrate live dashboard code and live report storage in one large step unless explicitly approved.

---

# 8. FINAL RULE

**Marketplace modules belong under `Grow24_AI/marketplaces/...`. Shared dashboard/web code belongs under `Grow24_AI/core/dashboard/`.**
