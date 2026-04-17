# Grow24 AI / GoAmrita - Future Module Location Standard v1.0
**Project Name:** Grow24 AI (formerly GoAmrita)  
**Date:** 15 April 2026  
**Purpose:** Permanent folder rules for AI-built future modules

---

# 1. CORE RULE

`ClaudeCode/Python` is the old beta/minimum-working-tool area.

Future AI tools must not place new production modules there.

All new future modules must live under the dedicated `Grow24_AI` architecture.

---

# 2. AMAZON MARKETPLACE MODULE ROOT

All Amazon marketplace modules must start under:

```text
Grow24_AI/marketplaces/amazon/
```

Seller-side SP-API modules must live under:

```text
Grow24_AI/marketplaces/amazon/seller_api/
```

Examples:

```text
Grow24_AI/marketplaces/amazon/seller_api/fba/
Grow24_AI/marketplaces/amazon/seller_api/market_intelligence/
Grow24_AI/marketplaces/amazon/seller_api/pricing_profit/
Grow24_AI/marketplaces/amazon/seller_api/listing_health/
Grow24_AI/marketplaces/amazon/seller_api/ads_optimization/
Grow24_AI/marketplaces/amazon/seller_api/review_feedback/
```

If the required folder does not exist, the AI tool must create it before adding the module.

---

# 3. DO NOT USE BETA FOLDER FOR NEW MODULES

Do not create new production modules in:

```text
ClaudeCode/Python/
```

That folder may still contain:
- dashboard server
- old scripts
- beta tools
- legacy compatibility utilities
- temporary migration bridges

But it is not the future module home.

---

# 4. FEATURE CONFIG RULE

When a module lives outside `ClaudeCode/Python`, its `config_features.json` entry must include:

```json
{
  "script": "module_file.py",
  "script_dir": "Grow24_AI/marketplaces/amazon/seller_api/<domain_folder>"
}
```

This lets the dashboard runner and scheduler find the module safely.

---

# 5. REPORT OUTPUT RULE

Until dashboard/report storage is migrated, moved modules may continue writing dashboard-facing outputs to:

```text
ClaudeCode/Report/<latest report folder>/Json/
```

This is allowed only as a compatibility bridge.

Future migration should later move report/data storage into:

```text
Grow24_AI/data/
```

Do not move report storage and code location in the same step unless explicitly approved.

---

# 6. COMPETITOR TRACKER DECISION

The competitor tracker now belongs at:

```text
Grow24_AI/marketplaces/amazon/seller_api/market_intelligence/competitor_tracker_v1.0.py
```

It remains dashboard-compatible by writing its current output summaries to the existing dashboard report folder.

---

# 7. FINAL RULE

**New code goes to `Grow24_AI`. `ClaudeCode/Python` is legacy/beta unless a specific compatibility reason exists.**

