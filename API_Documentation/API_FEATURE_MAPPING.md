# API → Feature Mapping — Pipeline & Data Freshness Reference
**Purpose:** Which API feeds which feature. For Task Scheduler pipeline + smart batching.
**Rule:** Update when new feature or API added.

---

## DATA PULL PIPELINE (Morning 8:30 AM)

### Step 1: Authentication (ALL APIs need this first)
| API Call | Features That Need It |
|----------|----------------------|
| Ads OAuth Token | ALL Ads features (C02-C04, C12, C15, C16, R01, K10, etc.) |
| SP-API LWA Token | ALL SP-API features (C08, P04, P07, M01, etc.) |

### Step 2: Data Pull (parallel where possible)

#### Ads API Calls:
| API Call | Endpoint | Data | Features Using This | Freshness |
|----------|----------|------|--------------------| ----------|
| Campaign List | POST /sp/campaigns/list | 108 campaigns: name, budget, state, bidding, targeting type | C02, C15, C16, C21, R01, W01 | 4hr |
| Ad Group List | POST /sp/adGroups/list | 140 ad groups: name, bid, state | C02, C15, R01 | 4hr |
| Keyword List | POST /sp/keywords/list | 1000 keywords: text, bid, match type, state | C12, C15, K01, K04, K10, R01 | 4hr |
| Negative Keyword List | POST /sp/negativeKeywords/list | 192 negatives: text, match type | C12, GAP-7 | 4hr |
| Product Ads List | POST /sp/productAds/list | 467 ads: ASIN, SKU, state | C08, R01 | 24hr |
| Campaign Report (daily) | POST /reporting/reports (spCampaigns, DAILY) | 392 rows: metrics per campaign per day | C02, C04, C15, C16, R01, R06, R07 | 4hr |
| Campaign Report (summary) | POST /reporting/reports (spCampaigns, SUMMARY) | 60 rows: 7-day totals | R01, R05, C08 | 4hr |
| Search Term Report | POST /reporting/reports (spSearchTerm, DAILY) | 1618 rows: search terms + metrics | C03, C12, K10, R01 | 24hr |
| Targeting Report | POST /reporting/reports (spTargeting, DAILY) | 2276 rows: keyword metrics | C15, I16, K04, K09 | 24hr |
| Advertised Product Report | POST /reporting/reports (spAdvertisedProduct, DAILY) | 741 rows: per-ASIN ad metrics | C08, R01, G01 | 4hr |
| Purchased Product Report | POST /reporting/reports (spPurchasedProduct, DAILY) | 76 rows: what customers bought | K10, I24 | 24hr |

#### SP-API Calls:
| API Call | Endpoint | Data | Features Using This | Freshness | Rate Limit |
|----------|----------|------|--------------------| ----------|------------|
| Pricing (Competitive Summary) | POST /batches/.../competitiveSummary | Your price, Buy Box, competitor prices | C08, P07, M01, NM-1 | 12hr | **0.033/sec (SLOW!)** |
| Catalog Items | GET /catalog/2022-04-01/items | Product name, brand, BSR, category | C08, M09, R01 | 24hr | 2/sec |
| FBA Inventory | GET /fba/inventory/v1/summaries | Stock levels, reserved, unfulfillable | P04, P05, H08 | 2hr | 2/sec |
| Orders | GET /orders/v0/orders | Recent orders, sales velocity | A13 (intraday), G13, C08 | 4hr | 1/sec |
| Product Fees | POST /products/fees/v0/feesEstimate | Estimated Amazon fees per ASIN | C08 (Phase 0.2) | 24hr | 10/sec |

### Step 3: Calculate (uses Step 2 data — no API calls)
| Calculation | Input Data From | Features |
|-------------|----------------|----------|
| True Profit per ASIN | Pricing API + Product Ads + Campaign Reports | C08 |
| Break-even ACoS | True Profit | C10 |
| Smart Bid Ceiling | True Profit + Conversion Rate | C11 |
| TACoS | Campaign Reports + Orders | G01 |
| Waste Detection | Search Terms + True Profit | I16, C12 |

### Step 4: Analyze (uses Step 3 calculations)
| Analysis | Input | Features |
|----------|-------|----------|
| Bid Recommendations | True Profit + Keyword metrics | C15 |
| Budget Recommendations | Campaign metrics + True Profit | C16 |
| Negative Keyword Candidates | Search Terms + waste detection | C12 |
| Search Term Graduation | Search Terms + Keyword list | K10 |

### Step 5: Score & Report (uses Step 4)
| Output | Input | Features |
|--------|-------|----------|
| IQ Score per recommendation | All analysis results | I01 |
| Excel Report generation | All scored data | R01 |
| Email alert | Report file | A02, A03 |

---

## REAL-TIME MONITORS (Independent, run on schedule)

| Monitor | API Call | Interval | Features |
|---------|----------|----------|----------|
| Buy Box Check | SP-API Pricing (competitiveSummary) | Every 2hr | P07 |
| Stock Check | SP-API FBA Inventory | Every 2hr | P04, P05 |
| Sales Compare | SP-API Orders | Every 4hr | A13 (intraday) |
| Budget Monitor | Ads API Campaign List (budget vs spend) | Every 8hr | P01, P13 |

---

## SMART BATCHING — Share One API Call Across Features

| API Call (ONE time) | Features That Share This Data |
|---------------------|------------------------------|
| Campaign List pull | C02, C15, C16, C21, P01, P13, R01 |
| Keyword List pull | C12, C15, K01, K04, K10, GAP-5, GAP-7 |
| Search Term Report | C03, C12, K10, I16 |
| Pricing API pull | C08, P07, M01, NM-1, C10, C11 |
| FBA Inventory pull | P04, P05, H08, H11 |
| Catalog Items pull | C08 (name/brand), M09 (BSR), R01 (display) |

**Rule:** Scheduler pulls data ONCE, stores in JSON files, ALL features read from store.

---

## API CALL COUNT PER DAILY RUN

| API | Calls Needed | Time | Bottleneck? |
|-----|-------------|------|-------------|
| Ads Token | 1 | <1s | No |
| SP-API Token | 1 | <1s | No |
| Ads Campaign List | 1 | <1s | No |
| Ads Ad Group List | 1 | <1s | No |
| Ads Keyword List | 1 | <1s | No |
| Ads Negative KW List | 1 | <1s | No |
| Ads Product Ads List | 1 | <1s | No |
| Ads Reports (6 types) | 6 create + 6 poll + 6 download = 18 | ~15 min | Medium |
| SP Pricing (330 ASINs) | 17 batches | **~9 min** | **YES!** |
| SP Catalog (330 ASINs) | 17 batches | ~10 sec | No |
| SP FBA Inventory | 1-7 calls | ~5 sec | No |
| SP Orders | 1-5 calls | ~5 sec | No |
| **TOTAL** | ~70 calls | **~25 min** | Pricing = bottleneck |

---

*Last Updated: 13 April 2026*
