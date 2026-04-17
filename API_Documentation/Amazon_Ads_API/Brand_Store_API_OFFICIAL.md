# Amazon Brand Store API — Official Documentation
**Source:** Amazon Ads Developer Documentation (Part 4)
**Saved:** 13 April 2026
**Category:** Amazon Ads API (advertising-api-eu.amazon.com)

---

## Overview

Brand Stores are customizable storefronts that allow brands to showcase products and tell their brand story.

### Prerequisites
- Brand registered
- Existing Store created
- `brandEntityId` obtained

---

## Endpoints

### Retrieve Store Information
```
GET /v2/stores
```
Returns all registered stores under an advertiser, including `brandEntityId` and page info.

### Store Insights
```
POST /stores/{brandEntityId}/insights
```
Analytics about Brand Store performance and customer behavior.

**Accept:** `application/vnd.GetInsightsForStoreResponse.v1+json`
**Content-Type:** `application/vnd.GetInsightsForStoreRequest.v1+json`
**Max date range:** 100 days

### Store ASIN Metrics
```
POST /stores/{brandEntityId}/asinMetrics
```
Performance data per ASIN (impressions, clicks, sales).

---

## Available Insight Metrics

| Metric | Description | Dimensions |
|--------|-------------|------------|
| VIEWS | Page views | All |
| VISITS | Total visits per day | All |
| VISITORS | Unique visitors (store level) | DATE only |
| ORDERS | Estimated orders within 14 days | All |
| UNITS | Estimated units purchased within 14 days | All |
| SALES | Estimated sales within 14 days | All |
| DWELL_TIME | Average time on store | All or store-level |
| BOUNCE_RATE | Bounce visits / landing visits | All or store-level |
| NEW_TO_STORE | Unique first-time visitors | DATE or store-level |
| SCORE_LEVEL | Quality rating (HIGH/MEDIUM/LOW) | DATE only |
| RECOMMENDATIONS | Array of recommended actions | DATE only |
| CONTRIBUTORS | Applied recommendations | DATE only |
| DWELL | Average dwell time (quality) | DATE only |
| PEER_DWELL | Peer store average dwell | DATE only |

## Available ASIN Metrics

| Metric | Description |
|--------|-------------|
| VIEWS | Times ASIN was viewed |
| ORDERS | Orders on day of ASIN view |
| UNITS | Units purchased |
| CLICKS | Times ASIN widget was clicked |
| CLICK_RATE | Clicks per view |
| RENDERS | Times ASIN rendered on page |
| ADDTOCARTS | Add-to-cart count |
| IN_STOCK_VIEWS | Views while ASIN was in stock |
| IN_STOCK_RATE | % viewed while in stock |
| AVERAGE_IN_STOCK_PRICE | Average price while in stock |
| AVERAGE_SALE_PRICE | Average sale price |
| CONVERSION_RATE | Orders / clicks |
| TOTAL_VIEWS | Total ASIN views across store |
| TOTAL_CLICKS | Total ASIN clicks across store |

## Dimensions
| Dimension | Description |
|-----------|-------------|
| DATE | By date |
| PAGE | By page |
| SOURCE | By traffic source |
| TAG | By tag |
| STORE | By store (DWELL_TIME, BOUNCE_RATE, NEW_TO_STORE only) |
| ASIN | ASIN metrics only |

---

## Marketplace Availability
- Store insights: All marketplaces
- Store ASIN metrics: All marketplaces

---
*File version: 1.0 | Extracted from Part 4 documentation*
