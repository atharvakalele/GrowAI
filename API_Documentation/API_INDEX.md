# API Documentation -- Master Index
**Last Updated:** 13 April 2026
**Version:** 1.3
**Purpose:** Quick reference to find any API endpoint, capability, or data field
**Rule:** Always read relevant doc BEFORE coding any API call!

---

## ⚠️ MANDATORY READING BEFORE ANY API WORK

| Priority | File | What It Contains | Read When |
|----------|------|-----------------|-----------|
| **#1 MUST READ** | **[Amazon_Official_Guidelines.md](Amazon_Official_Guidelines.md)** | Official Amazon API rules: rate limiting, error handling, pagination, versioning, bid/budget constraints, common mistakes to avoid, India-specific limits | **BEFORE writing ANY API code. Every developer. Every time.** |

> **WHY THIS FILE IS #1:** It contains rules that prevent bugs, rate limiting, data inconsistency, and wasted development time. Every rule in this file was written by Amazon and ignoring any of them leads to specific, known problems. It also lists 15 gaps found vs our internal rules (`04_API_INTEGRATION.md`) that need to be added.

---

> **FALLBACK SYSTEM:** Some files contain content from older API versions, marked with
> `FALLBACK / OLD VERSION` at the top. These are kept as workaround references if our
> primary pinned version has bugs or missing endpoints. Files marked with `[F]` in the
> tables below contain fallback/older version content.

---

## Amazon Ads API (advertising-api-eu.amazon.com)

### Our Pinned Versions:
- Campaign Management: Ads API v1 Unified (v3 in URLs = same, architectural reboot)
- Reporting: v1 Unified Reporting (PRIMARY), v3 (fallback)

### Documentation Files:

| File | What's Inside | Use When | Fallback? |
|------|--------------|----------|-----------|
| SP_v3_OpenAPI_OFFICIAL.md | 73 SP endpoints -- all CRUD operations, filters, pagination | Building any SP campaign/keyword/ad feature | PRIMARY |
| SP_Campaigns_v3_official.md | v2 SP endpoints, data models, query params | **[F]** Fallback if v3 endpoint missing | **[F] v2** |
| SP_Detailed_Guides_OFFICIAL.md | Step-by-step tutorials with curl examples | Learning how to use SP API, first-time implementation | PRIMARY |
| Campaign_Management_API_v1_OFFICIAL.md | v1 entity specs -- SP, SB, SD, DSP fields, JSON examples | Understanding data models, field-level details | PRIMARY |
| Reporting_v3_OFFICIAL_Part1.md | 10 report types, metrics, async workflow | Building report features (C02-C04, R01) | PRIMARY |
| Reporting_v3_OFFICIAL_Part2.md | Search term, targeting, placement, purchased product, gross/invalid traffic + 400+ columns reference | Search term analysis (C03, K10), targeting reports, traffic quality | PRIMARY |
| Reporting_v3_official.md | Partial v3 reporting extraction | **[F]** Quick reference if Part1 too detailed | **[F] Partial** |
| Conversions_and_Events_API_OFFICIAL.md | Conversion tracking, CAPI, Attribution | Building conversion attribution features | PRIMARY |
| Exports_API_OFFICIAL.md | Snapshot replacement, entity models, all enums | Bulk data export, enum reference | PRIMARY |
| SB_v4_Campaigns_OFFICIAL.md | Sponsored Brands -- video, store spotlight, goals | Future: SB campaign management (GAP-22) | PRIMARY |
| SD_Campaigns_OFFICIAL.md | Sponsored Display -- audiences, contextual, location | Future: SD campaign management (GAP-22) | PRIMARY |
| DSP_Forecasting_API_OFFICIAL.md | DSP campaign forecasting -- metrics, curves, replanning, Python client | DSP campaign planning, budget optimization, performance prediction | PRIMARY |
| DSP_Bid_Adjustments_API_OFFICIAL.md | DSP bid adjustments -- dimensions, rules, A/B testing, rate limits | DSP bid optimization by device/geo/domain/audience | PRIMARY |
| DSP_Guidance_and_Insights_API_OFFICIAL.md | DSP guidance, quick actions, overlapping audiences, persona builder, Brand+/Performance+ insights | DSP campaign optimization, audience discovery, ML recommendations | PRIMARY |
| Brand_Store_API_OFFICIAL.md | Brand Store info, insights, ASIN metrics, quality scores | Store analytics, performance tracking, quality optimization | PRIMARY |
| Budget_and_Bidding_Rules_Detailed_Guide_OFFICIAL.md | Budget rules (schedule + performance) for SP/SB/SD, bidding rules for SP, schedule bid rules | Automating budget/bid adjustments (C16), rule-based optimization | PRIMARY |
| Partner_Opportunities_API_OFFICIAL.md | Partner recommendations catalog, CSV download, Marketing Stream integration | Partner Network optimization, bulk recommendations | PRIMARY |
| Amazon_Attribution_API_OFFICIAL.md | Attribution tags (macro + non-macro), measurement, reports, troubleshooting | External traffic attribution, cross-channel measurement | PRIMARY |
| READ_endpoints.md | Summary of all read endpoints + recommendations | Quick lookup of read operations | -- |
| WRITE_endpoints.md | Summary of all write endpoints + danger levels | Quick lookup of write operations (approval needed) | -- |

### Key Capabilities Quick Reference:

| Need | API/Endpoint | Doc File |
|------|-------------|----------|
| List campaigns | POST /sp/campaigns/list | SP_v3_OpenAPI_OFFICIAL.md |
| Create campaign | POST /sp/campaigns | SP_v3_OpenAPI_OFFICIAL.md |
| Change bid | PUT /sp/keywords | SP_v3_OpenAPI_OFFICIAL.md |
| Change budget | PUT /sp/campaigns | SP_v3_OpenAPI_OFFICIAL.md |
| Pause campaign | PUT /sp/campaigns (state->PAUSED) | SP_v3_OpenAPI_OFFICIAL.md |
| Add negative keyword | POST /sp/negativeKeywords | SP_v3_OpenAPI_OFFICIAL.md |
| Get performance report | POST /reporting/reports | Reporting_v3_OFFICIAL_Part1.md |
| Budget rules (auto) | POST /sp/budgetRules | Budget_and_Bidding_Rules_Detailed_Guide_OFFICIAL.md |
| Optimization rules | POST /sp/rules/optimization | Budget_and_Bidding_Rules_Detailed_Guide_OFFICIAL.md |
| Rule-based bidding | POST /sp/rules/campaignOptimization | Budget_and_Bidding_Rules_Detailed_Guide_OFFICIAL.md |
| Target promotion groups | POST /sp/targetPromotionGroups | SP_v3_OpenAPI_OFFICIAL.md |
| Keyword suggestions | POST /sp/targets/keywords/recommendations | SP_v3_OpenAPI_OFFICIAL.md |
| Bid recommendations | POST /sp/targets/bid/recommendations | SP_v3_OpenAPI_OFFICIAL.md |
| Budget recommendations | POST /sp/campaigns/budgetRecommendations | SP_v3_OpenAPI_OFFICIAL.md |
| Special events/festivals | GET /sp/v1/events | SP_v3_OpenAPI_OFFICIAL.md |
| Export/snapshot data | Exports API endpoints | Exports_API_OFFICIAL.md |
| DSP campaign forecast | POST /adsApi/v1/retrieve/campaignForecasts/dsp | DSP_Forecasting_API_OFFICIAL.md |
| DSP bid adjustments | POST /dsp/rules/bidmodifier | DSP_Bid_Adjustments_API_OFFICIAL.md |
| DSP guidance/recommendations | POST /dsp/v1/guidance/campaigns/list | DSP_Guidance_and_Insights_API_OFFICIAL.md |
| DSP quick actions | POST /dsp/v1/quickactions/{id}/executions | DSP_Guidance_and_Insights_API_OFFICIAL.md |
| Overlapping audiences | GET /insights/audiences/{id}/overlappingAudiences | DSP_Guidance_and_Insights_API_OFFICIAL.md |
| Persona builder | POST /insights/bandedSize, /demographics, etc. | DSP_Guidance_and_Insights_API_OFFICIAL.md |
| Combined audiences | POST /dsp/audiences/combinedAudiences | DSP_Guidance_and_Insights_API_OFFICIAL.md |
| Brand+/Performance+ insights | POST /dsp/v1/campaign/insights | DSP_Guidance_and_Insights_API_OFFICIAL.md |
| Brand Store info | GET /v2/stores | Brand_Store_API_OFFICIAL.md |
| Brand Store insights | POST /stores/{brandEntityId}/insights | Brand_Store_API_OFFICIAL.md |
| Brand Store ASIN metrics | POST /stores/{brandEntityId}/asinMetrics | Brand_Store_API_OFFICIAL.md |
| Partner opportunities | GET /partnerOpportunities | Partner_Opportunities_API_OFFICIAL.md |
| Attribution tags (macro) | GET /attribution/tags/macroTag | Amazon_Attribution_API_OFFICIAL.md |
| Attribution tags (non-macro) | GET /attribution/tags/nonMacroTemplateTag | Amazon_Attribution_API_OFFICIAL.md |
| Attribution reports | POST /attribution/report | Amazon_Attribution_API_OFFICIAL.md |

---

## Amazon SP-API (sellingpartnerapi-eu.amazon.com)

### Our Pinned Versions:
- Catalog Items: v2022-04-01
- Pricing: v2022-05-01
- Orders: v2026-01-01
- Feeds: v2021-06-30 (JSON only!)
- Listings Items: v2021-08-01
- Notifications: v1
- FBA Inventory: v1
- Reports: v2021-06-30
- Product Fees: v0
- Brand Analytics: v1
- Sales & Traffic: v2024-04-24
- Customer Feedback: v2024-06-01

### Documentation Files:

| File | What's Inside | Use When | Fallback? |
|------|--------------|----------|-----------|
| Catalog_Items_v2022-04-01.md | Search/get product details, images, BSR, attributes | Getting product info, sale price, BSR (C08, M09) | PRIMARY |
| Pricing_v2022-05-01.md | Buy Box price, competitor prices, featured offer | Buy Box monitor (P07), competitor tracking (M01) | PRIMARY |
| Feeds_v2021-06-30.md | Bulk update price/inventory/listings (JSON feeds) | Bulk price change, inventory update (P06, P07) | PRIMARY |
| Orders_v2026-01-01.md | Order list, details, items, buyer info (v0 content) | **[F]** Fallback -- actual v0, pinned is v2026-01-01 | **[F] v0** |
| Orders_official.md | Additional order endpoint details (v0 content) | **[F]** Alternate v0 extraction | **[F] v0** |
| Listings_v2021-08-01.md | Get/put/patch/delete listings | Listing management, A+ content | PRIMARY |
| Listings_v2021-08-01_official.md | Additional listing details | Extended listing reference | PRIMARY |
| Notifications_v1.md | Event subscriptions (offer change, order, inventory) | Real-time triggers (EN-5) | PRIMARY |
| Notifications_v1_official.md | Additional notification details | Extended notification reference | PRIMARY |
| FBA_Inventory_v1.md | Stock levels, reserved, unfulfillable quantities | Stock monitoring (P04, P05) | PRIMARY |
| FBA_Inventory_v1_official.md | Additional FBA inventory details | Extended FBA reference | PRIMARY |
| Product_Fees.md | Fee estimation per SKU/ASIN | True profit calculation (C08) | PRIMARY |
| Product_Fees_official.md | Additional fee details | Extended fees reference | PRIMARY |
| SP_API_Reports_2021-06-30.md | Report types, schedules, document download | Report generation | PRIMARY |
| Reports_v2021-06-30_official.md | Additional report details | Extended reports reference | PRIMARY |
| READ_endpoints.md | Summary of all SP-API read operations | Quick lookup | -- |
| WRITE_endpoints.md | Summary of all write operations + danger levels | Write ops (approval needed) | -- |

### Key Capabilities Quick Reference:

| Need | API/Endpoint | Doc File |
|------|-------------|----------|
| Get sale price | GET /catalog/2022-04-01/items/{asin} (attributes) | Catalog_Items_v2022-04-01.md |
| Get BSR/sales rank | GET /catalog/2022-04-01/items/{asin} (salesRanks) | Catalog_Items_v2022-04-01.md |
| Get Buy Box price | POST /batches/.../competitiveSummary | Pricing_v2022-05-01.md |
| Get competitor prices | POST /batches/.../competitiveSummary (lowestPricedOffers) | Pricing_v2022-05-01.md |
| Target price to win Buy Box | POST /batches/.../featuredOfferExpectedPrice | Pricing_v2022-05-01.md |
| Get orders/sales | GET /orders/v0/orders | Orders_v2026-01-01.md |
| Get stock levels | GET /fba/inventory/v1/summaries | FBA_Inventory_v1.md |
| Get product fees | POST /products/fees/v0/feesEstimate | Product_Fees.md |
| Update price (bulk) | Feeds API -> JSON_LISTINGS_FEED | Feeds_v2021-06-30.md |
| Update listing | PATCH /listings/2021-08-01/items/{sku} | Listings_v2021-08-01.md |
| Subscribe to events | POST /notifications/v1/subscriptions | Notifications_v1.md |
| Get reports | POST /reports/2021-06-30/reports | SP_API_Reports_2021-06-30.md |

---

## Rate Limit Quick Reference

| API | Rate | Note |
|-----|------|------|
| Ads API (most endpoints) | ~10 req/sec | Generous |
| Ads DSP Bid Adjustments | 5-10 req/sec | Per endpoint |
| SP-API Pricing | 0.033 req/sec (2/min!) | BOTTLENECK -- batch + queue required |
| SP-API Catalog | 2 req/sec | Moderate -- batch for 300+ ASINs |
| SP-API Orders | ~1 req/sec | OK for daily pulls |
| SP-API Feeds (create) | 0.0083 req/sec | Slow -- plan ahead |
| SP-API Reports (create) | ~0.017 req/sec | Moderate |
| DSP Campaign Insights | 25 requests per API call | Batch limit |

---

## Feature -> API Mapping

| Feature | Ads API Needed | SP-API Needed |
|---------|---------------|---------------|
| C02 Data Pull | campaigns/list, adGroups/list, keywords/list | -- |
| C03 Search Terms | Reporting v3 (spSearchTerm) | -- |
| C08 True Profit | -- | Catalog (price), Product Fees, Orders |
| C12 Negative Keywords | negativeKeywords/create | -- |
| C15 Bid Optimizer | keywords/update (bid), bid/recommendations | -- |
| C16 Budget Manager | campaigns/update (budget), budgetRules | -- |
| P04 Stock-Out | -- | FBA Inventory |
| P07 Buy Box | -- | Pricing (competitiveSummary) |
| M01 Competitor Price | -- | Pricing (lowestPricedOffers) |
| R01 Daily Report | Reporting v3 (all SP report types) | -- |
| K10 Search Term Graduate | Reporting + keywords/create + negativeKeywords/create | -- |
| EN-5 Real-time Triggers | -- | Notifications (subscribe) |
| Store Analytics | Brand Store API (insights, ASIN metrics) | -- |
| External Traffic | Amazon Attribution API (tags, reports) | -- |
| Auto Budget Rules | Budget Rules API (schedule + performance) | -- |
| Auto Bid Rules | Bidding Rules API (campaignOptimization, optimization) | -- |
| DSP Forecasting | DSP Forecasting API | -- |
| DSP Bid Optimization | DSP Bid Adjustments API | -- |

---

## Fallback Content Summary

Files marked **[F]** contain older API version content kept as workaround references.

| File | Primary Version | Fallback Version | Why Kept |
|------|----------------|-----------------|----------|
| SP_Campaigns_v3_official.md | v3 (SP_v3_OpenAPI_OFFICIAL.md) | v2 | v2 has detailed data models, query params, response codes not yet in v3 doc |
| Reporting_v3_official.md | v3 Part1 (Reporting_v3_OFFICIAL_Part1.md) | v3 partial | Quick-reference format, simpler than full Part1 doc |
| Orders_v2026-01-01.md | v2026-01-01 (not yet on GitHub) | v0 | Only version available on GitHub; core endpoints similar |
| Orders_official.md | v2026-01-01 (not yet on GitHub) | v0 | Alternate extraction of same v0 spec |

**Rule:** Always use PRIMARY docs first. Only check fallback if primary doc is missing an endpoint or field you need.

---

## Still Missing Documentation:
- Reporting API Part 2 (search term reports, targeting reports, columns reference, FAQ)
- Brand Analytics detailed endpoint reference
- Sales & Traffic API v2024-04-24 detailed reference
- Customer Feedback API v2024-06-01 detailed reference
- Amazon Marketing Cloud API reference
- Amazon Marketing Stream API reference
- Orders API v2026-01-01 official spec (v0 used as fallback until available)

---
*Index version: 1.2 | Update when new docs added.*
*v1.1: Added fallback version tracking column, fallback content summary section*
*v1.2: Added MANDATORY READING section at top with Amazon_Official_Guidelines.md*
