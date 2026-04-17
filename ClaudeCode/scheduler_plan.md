# GoAmrita Task Scheduler Plan v1.0
**Date:** 13 April 2026
**Purpose:** Central scheduler for all automated tasks
**Status:** PLANNING — will build scheduler engine after all tasks defined

---

## SCHEDULED TASKS

### 1. Auto Campaign Creator — New Listing (DAILY)
```
Schedule:     Daily 8:30 AM
Mode:         --mode newlisting --days 8
What it does:
  1. Fetch all ASINs from Catalog API with product_site_launch_date
  2. Filter: listed in last 8 days (configurable)
  3. Check: NOT already in any existing campaign
  4. For each new ASIN:
     → Fetch keyword suggestions
     → Fetch listing content (title + bullets)
     → Smart filter keywords vs listing
     → Calculate bid (25% profit budget, 5% bid)
     → Create campaign: {SKU}_AI_AutoLaunch_New_Listing
     → Save product opportunities
  5. Log results

Script:       auto_campaign_creator_v1.0.py --mode newlisting --days 8
Campaign Name:{SKU}_AI_AutoLaunch_New_Listing
```

### 2. Auto Campaign Creator — Top Profit (EVERY 15 DAYS)
```
Schedule:     Every 15 days, 9:00 AM
Mode:         --mode profit --top 5
What it does:
  1. Find ASINs with highest True Profit
  2. Filter: NOT in any existing campaign
  3. Filter: Buy Box = ours, price > Rs.100
  4. Top 5 (configurable) → create campaigns
  5. Campaign name: {SKU}_{Date}_AI_BidDown5pctAdSpend25pctProfit

Script:       auto_campaign_creator_v1.0.py --mode profit --top 5
Campaign Name:{SKU}_{Date}_AI_BidDown5pctAdSpend25pctProfit
```

### 3. Daily Data Import (DAILY)
```
Schedule:     Daily 8:00 AM (before campaign creator)
What it does:
  1. Pull all Ads API data (campaigns, keywords, search terms, products)
  2. Pull SP-API data (pricing, inventory, catalog)
  3. Calculate True Profit
  4. Store in JSON (later SQLite)

Script:       sp_ads_complete_import_v1.0.py
Depends on:   Nothing (runs first)
```

### 4. True Profit Calculator (DAILY)
```
Schedule:     Daily 8:15 AM (after data import)
What it does:
  1. Load imported data
  2. Calculate true profit per ASIN
  3. Sale price priority: actual sales > API price > fallback
  4. Save true_profit_per_asin.json
  
Data Freshness: 5 days (recalculate if older)

Script:       true_profit_calculator_v1.0.py
Depends on:   Data Import (task 3)
```

### 5. Buy Box Monitor (EVERY 2 HOURS)
```
Schedule:     Every 2 hours
What it does:
  1. Check Buy Box status all ASINs
  2. Alert if Buy Box lost
  3. Log changes

Script:       Grow24_AI/marketplaces/amazon/seller_api/market_intelligence/buy_box_monitor_v1.1.py
Depends on:   Nothing (independent)
```

### 6. Stock Monitor (EVERY 2 HOURS)
```
Schedule:     Every 2 hours  
What it does:
  1. Check FBA inventory levels
  2. Alert if stock < threshold
  3. Pause ads if stock = 0

Script:       Grow24_AI/marketplaces/amazon/seller_api/inventory/stock_monitor_v1.1.py
Depends on:   Nothing (independent)
```

### 7. Intraday Sales Compare (EVERY 4 HOURS)
```
Schedule:     Every 4 hours
What it does:
  1. Check today sales at this time
  2. Compare vs yesterday same time
  3. Alert if drop > 30% (configurable)

Script:       [TO BUILD] intraday_sales_v1.0.py
Depends on:   Nothing (independent)
```

### 8. Budget Monitor (EVERY 8 HOURS)
```
Schedule:     Every 8 hours
What it does:
  1. Check campaign spend vs budget
  2. Alert if any campaign > 150% budget (spike)
  3. Alert if star campaign hitting budget limit (missing opportunity)

Script:       [TO BUILD] budget_monitor_v1.0.py
Depends on:   Data Import (for latest data)
```

### 9. Excel Action Report (DAILY)
```
Schedule:     Daily 8:45 AM (after all analysis)
What it does:
  1. Generate action report Excel (5 sheets)
  2. Email to configured recipients
  3. Wait for approval file return

Script:       create_action_report_v2.0.py
Depends on:   True Profit (task 4), Data Import (task 3)
```

### 10. Execute Approved Actions (ON DEMAND / DAILY)
```
Schedule:     Daily 10:00 AM (after user reviews Excel)
              OR on-demand when approval file received
What it does:
  1. Read returned approval Excel
  2. Execute Approved actions via Ads API
  3. Skip empty cells
  4. Log all actions

Script:       [TO BUILD] execute_approvals_v1.0.py
Depends on:   Action Report (task 9) returned by user
```

### 11. Pricing Refresh (EVERY 12 HOURS)
```
Schedule:     Every 12 hours (slow API)
What it does:
  1. Fetch current prices for all ASINs
  2. Update Buy Box status
  3. Compare vs last check

Script:       fetch_pricing_v1.0.py
Depends on:   Nothing (independent, but slow — 9 min)
```

### 12. Weekly Report (WEEKLY)
```
Schedule:     Every Sunday 10:00 PM
What it does:
  1. Compile weekly summary
  2. Top/worst campaigns
  3. Money saved/earned
  4. Trend analysis

Script:       [TO BUILD] weekly_report_v1.0.py
Depends on:   All daily data
```

---

## DAILY PIPELINE (Morning 8:00-9:00 AM)

```
8:00 AM  ──→ [3] Data Import (Ads + SP-API)
              │
8:15 AM  ──→ [4] True Profit Calculator
              │
8:30 AM  ──→ [1] Auto Campaign: New Listings (daily)
              │
8:45 AM  ──→ [9] Excel Action Report + Email
              │
10:00 AM ──→ [10] Execute Approved Actions (after user review)
```

## REAL-TIME MONITORS (Independent)

```
Every 2hr ──→ [5] Buy Box Monitor
Every 2hr ──→ [6] Stock Monitor
Every 4hr ──→ [7] Intraday Sales Compare
Every 8hr ──→ [8] Budget Monitor
Every 12hr──→ [11] Pricing Refresh
```

## PERIODIC

```
Every 15d ──→ [2] Auto Campaign: Top Profit
Every Sun ──→ [12] Weekly Report
```

---

## DATA FRESHNESS RULES (Configurable in Advanced Settings)

| Data | Fresh If | Stale After | Used By |
|------|----------|-------------|---------|
| Campaign metrics | < 4 hours | > 4 hours | Tasks 3,4,8,9 |
| Stock levels | < 2 hours | > 2 hours | Task 6 |
| Buy Box status | < 1 hour | > 1 hour | Task 5 |
| Pricing/Your Price | < 12 hours | > 12 hours | Task 11 |
| Search terms | < 24 hours | > 24 hours | Task 3 |
| True Profit | < 5 days | > 5 days | Task 4 |
| Competitor prices | < 12 hours | > 12 hours | Task 11 |

---

## DEPENDENCY CHAIN

```
If user runs task 9 (Excel Report) manually:
  → System checks: Task 3 (data import) fresh?
    → YES: proceed with report
    → NO: auto-run task 3 first, then 4, then 9
    → User sees: "Data was stale. Running fresh import first..."
```

---

## SMART BATCHING

| API Call (ONE time) | Tasks That Share |
|---------------------|------------------|
| Ads Campaign List | Tasks 3, 8, 9 |
| SP-API Pricing | Tasks 4, 5, 11 |
| SP-API Catalog | Tasks 1, 2, 4 |
| SP-API FBA Inventory | Tasks 6 |

---

## SCRIPTS STATUS

| # | Script | Status | File |
|---|--------|--------|------|
| 1 | Auto Campaign New Listing | ✅ BUILT | auto_campaign_creator_v1.0.py |
| 2 | Auto Campaign Top Profit | ✅ BUILT | auto_campaign_creator_v1.0.py (--mode profit) |
| 3 | Data Import | ✅ BUILT | sp_ads_complete_import_v1.0.py |
| 4 | True Profit | ✅ BUILT | true_profit_calculator_v1.0.py |
| 5 | Buy Box Monitor | ✅ BUILT | Grow24_AI/marketplaces/amazon/seller_api/market_intelligence/buy_box_monitor_v1.1.py |
| 6 | Stock Monitor | ✅ BUILT | Grow24_AI/marketplaces/amazon/seller_api/inventory/stock_monitor_v1.1.py |
| 7 | Intraday Sales | TO BUILD | — |
| 8 | Budget Monitor | TO BUILD | — |
| 9 | Excel Report | ✅ BUILT | create_action_report_v2.0.py |
| 10 | Execute Approvals | TO BUILD | — |
| 11 | Pricing Refresh | ✅ BUILT | fetch_pricing_v1.0.py |
| 12 | Weekly Report | TO BUILD | — |

**Built: 7/12 | To Build: 5/12**

---

*Scheduler Plan v1.0 | 13 April 2026*
*Next: Build central scheduler engine that runs all these tasks*
