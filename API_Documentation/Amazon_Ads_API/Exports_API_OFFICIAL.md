# Amazon Ads Exports API - OFFICIAL Documentation
**Source:** Official Amazon Advertising documentation (manually copied by Msir)
**Date Captured:** 13 April 2026
**API Version:** Exports v1
**Our Endpoint:** advertising-api-eu.amazon.com
**Our Profile ID:** 42634532240933
**Part of:** Part 3 API documentation batch

---

## Table of Contents
1. [Exports Overview](#1-exports-overview)
2. [Exports vs Reports vs List Operations](#2-exports-vs-reports-vs-list-operations)
3. [API Workflow](#3-api-workflow)
4. [Endpoints & Headers](#4-endpoints--headers)
5. [Common Models - Campaigns](#5-common-models---campaigns)
6. [Common Models - Ad Groups](#6-common-models---ad-groups)
7. [Common Models - Ads](#7-common-models---ads)
8. [Common Models - Targets](#8-common-models---targets)
9. [Enums Reference](#9-enums-reference)
10. [Rate Limits & FAQ](#10-rate-limits--faq)

---

## 1. Exports Overview

Exports are a **replacement for the snapshots functionality**. They efficiently retrieve campaign structure/metadata asynchronously at multiple levels.

### Export Availability by Ad Type:

| Export Type | Sponsored Products | Sponsored Brands | Sponsored Display |
|-------------|-------------------|-------------------|-------------------|
| campaigns | x | x | x |
| adGroups | x | x | x |
| targets | x | x | x |
| ads | x | x | x |

### Entity Hierarchy:
Account > Campaigns > Ad Groups > (Ads + Targets)

---

## 2. Exports vs Reports vs List Operations

| Feature | Exports | Reports | List (GET) Operations |
|---------|---------|---------|----------------------|
| Data type | Metadata (current state) | Performance data (historical) | Metadata (current state) |
| Execution | Asynchronous | Asynchronous | Synchronous |
| Best for | Many campaigns, bulk sync | Day-level impression/click/cost data | Single campaign details |
| Intended use | 1-2 times per day sync | Performance analysis | Real-time single lookups |

---

## 3. API Workflow

### Step 1: Request an Export

```
POST /campaigns/export
POST /adGroups/export
POST /targets/export
POST /ads/export
```

**Required Headers:**

| Parameter | Description |
|-----------|-------------|
| Amazon-Advertising-API-ClientId | Client ID for auth |
| Authorization | Access token |
| Amazon-Advertising-API-Scope | Profile ID |

**Accept/Content-Type Headers by Type:**

| Type | Header Value |
|------|-------------|
| Campaigns | application/vnd.campaignsexport.v1+json |
| Ad Groups | application/vnd.adgroupsexport.v1+json |
| Targets | application/vnd.targetsexport.v1+json |
| Ads | application/vnd.adsexport.v1+json |

**Request Body:**
- `adProductFilter` (required): e.g., "SPONSORED_PRODUCTS"
- `stateFilter` (optional): "ENABLED", "PAUSED", "ARCHIVED" (comma-separated for multiple)

**Response (202):**
```json
{
    "exportId": "xxxxxxxxxxxxxxxxxxx",
    "status": "IN_PROGRESS"
}
```

### Step 2: Check Export Status

```
GET /exports/{exportId}
```

**Response when complete (200):**
```json
{
    "exportId": "xxxxxxxxxxxxxxx",
    "status": "COMPLETED",
    "url": "https://snapshots-prod-us-east-1.s3.us-east-1.amazonaws.com/...",
    "fileSize": 794,
    "urlExpiresAt": "2023-09-19T17:53:55.778Z",
    "generatedAt": "2023-09-19T16:53:53.867Z",
    "createdAt": "2023-09-19T16:53:53.405Z"
}
```

### Step 3: Download Export

- Download from the `url` returned in status check
- New download URL generated on each GET call (valid 1 hour)
- URLs generated up to 24 hours after completion
- Format: JSON compressed in gzip

---

## 5. Common Models - Campaigns

### Campaign Schema:

| Field | Type | Required | Read-only | Description |
|-------|------|----------|-----------|-------------|
| campaignId | String | Yes | Yes | Unique campaign ID |
| adProduct | Enum | | | SP, SB, or SD |
| portfolioId | String | | | Portfolio association |
| name | String | Yes | | Campaign name |
| startDate | String | | | Start date |
| endDate | String | | | End date |
| lastUpdatedDateTime | String | Yes | Yes | Last update timestamp |
| creationDateTime | String | Yes | Yes | Creation timestamp |
| state | Enum | Yes | | ENABLED, PAUSED, ARCHIVED |
| deliveryStatus | Enum | Yes | Yes | DELIVERING, NOT_DELIVERING, UNAVAILABLE |
| deliveryReasons | Enum | | Yes | List of non-delivery reasons |
| brandEntityId | String | | | Required for sellers creating SB campaigns |
| optimization.bidStrategy | Enum | | | Auto bidding strategy |
| optimization.placementBidAdjustments.placement | Enum | | | Placement for bid adjustment |
| optimization.placementBidAdjustments.percentage | Integer | | | Percentage adjustment |
| optimization.shopperSegmentBidAdjustment.shopperSegment | Enum | | | Shopper segment for bid adjustment |
| optimization.shopperSegmentBidAdjustment.percentage | Integer | | | Percentage adjustment |
| optimization.shopperCohortBidAdjustment.shopperCohortType | Enum | | | Cohort type |
| optimization.shopperCohortBidAdjustment.percentage | Integer | | | Cohort percentage |
| optimization.shopperCohortBidAdjustment.audienceSegments.audienceId | String | | | Audience segment ID |
| optimization.shopperCohortBidAdjustment.audienceSegments.audienceSegmentType | Enum | | | Segment type |
| budgetCaps.budgetType | Enum | Yes | | MONETARY |
| budgetCaps.recurrenceTimePeriod | Enum | Yes | | DAILY, LIFETIME, OTHER |
| budgetCaps.budgetValue.monetaryBudget.currencyCode | Enum | Yes | | ISO 4217 currency |
| budgetCaps.budgetValue.monetaryBudget.amount | Decimal | Yes | | Budget amount |
| budgetCaps.budgetValue.monetaryBudget.ruleAmount | Decimal | | Yes | Amount when budget rule applied |
| targetingSettings | Enum | | | MANUAL, AUTO, T00020, T00030 |
| costType | Enum | | | CPC or VCPM |
| tags.key / tags.value | String | | | Custom labels |

### Campaign API Representations:

| Feature | Operations |
|---------|-----------|
| sp/campaigns | POST create, POST list, PUT update, POST delete |
| sb/v4/campaigns | POST create, POST list, PUT update, POST delete |
| sd/campaigns | POST create, GET list, PUT update, DELETE by ID |
| st/campaigns | POST create, POST list, PUT update, POST delete |
| campaigns/exports | POST /campaigns/exports |

### Ad Product Version Mapping:

| Ad Product | Latest Campaign API Version |
|------------|---------------------------|
| Sponsored Products | Version 3 |
| Sponsored Brands | Version 4 |
| Sponsored Display | Version 1 |
| Sponsored Television | Version 1 |

---

## 6. Common Models - Ad Groups

### Ad Group Schema:

| Field | Type | Required | Read-only | Description |
|-------|------|----------|-----------|-------------|
| adGroupId | String | Yes | Yes | Unique ad group ID |
| campaignId | String | Yes | | Parent campaign ID |
| adProduct | Enum | Yes | | Ad product type |
| name | String | Yes | | Ad group name |
| state | Enum | Yes | | ENABLED, PAUSED, ARCHIVED |
| deliveryStatus | Enum | Yes | Yes | Delivery status |
| deliveryReasons | Enum | | Yes | Non-delivery reasons |
| creativeType | String | | | Creative type (SD only) |
| creationDateTime | datetime | Yes | Yes | Created timestamp |
| lastUpdatedDateTime | datetime | Yes | Yes | Last updated timestamp |
| bid.defaultBid | double | Yes | | Default max bid |
| bid.currencyCode | Enum | Yes | | Currency code |
| optimization.goalSetting.goal | Enum | | | AWARENESS, CONSIDERATION, CONVERSIONS |
| optimization.goalSetting.kpi | Enum | | | CLICKS |

---

## 7. Common Models - Ads

### Ad Types:

| Ad Type | Description | SP | SB | SD |
|---------|-------------|----|----|------|
| PRODUCT_AD | Based on advertised product | x | | x |
| IMAGE | Custom images | | | x |
| VIDEO | Videos/brand video | | x | x |
| PRODUCT_COLLECTION | Collection of products | | x | |
| STORE_SPOTLIGHT | Amazon Store + sub-pages | | x | |

### Ad Schema (key fields):

| Field | Type | Required | Read-only | Description |
|-------|------|----------|-----------|-------------|
| adId | string | Yes | Yes | Unique ad ID |
| adGroupId | string | Yes | | Parent ad group |
| adProduct | Enum | Yes | | Ad product |
| state | Enum | Yes | | State |
| adType | Enum | Yes | | Ad type |
| creative | obj | Yes | | Creative details |
| creative.products | array | | | Featured products |
| creative.brandLogo | obj | | | Brand logo asset |
| creative.customImages | array | | | Custom images |
| creative.videos | array | | | Video assets |
| creative.headline | string | | | Ad headline |
| creative.brandName | string | | | Brand name |
| creative.landingPage | obj | | | Landing page details |
| creative.cards | array | | | Card sections (Store Spotlight) |
| deliveryStatus | Enum | Yes | Yes | Delivery status |
| adVersionId | string | | Yes | Version of the ad |

---

## 8. Common Models - Targets

### Targeting Types:

| Type | Supports Negative | Campaign-level | Description | SP | SB | SD |
|------|-------------------|----------------|-------------|----|----|------|
| AUTO | No | No | Amazon-chosen targets | x | x | x |
| AUDIENCE | No | No | Amazon audience segment | | | x |
| KEYWORD | Yes | Yes (SP neg only) | Search term targeting | x | x | |
| PRODUCT_CATEGORY | Yes | Yes (SP neg only) | Category targeting | x | x | x |
| PRODUCT | Yes | Yes (SP neg only) | ASIN targeting | x | x | x |
| PRODUCT_CATEGORY_AUDIENCE | No | No | Category view/purchase remarketing | | | x |
| PRODUCT_AUDIENCE | No | No | Product view/purchase remarketing | | | x |
| THEME | No | No | Theme-related keywords | x | | |

### Target Schema (key fields):

| Field | Type | Required | Read-only |
|-------|------|----------|-----------|
| targetId | string | Yes | Yes |
| adGroupId | string | | |
| campaignId | string | | |
| adProduct | Enum | Yes | |
| state | Enum | Yes | |
| negative | boolean | Yes | |
| deliveryStatus | Enum | Yes | Yes |
| bid.bid | double | | |
| targetType | Enum | Yes | |
| targetDetails.matchType | Enum | | |
| targetDetails.keyword | string | | |
| targetDetails.productCategoryId | string | | |
| targetDetails.asin | string | | |
| targetDetails.audienceId | string | | |
| targetDetails.event | Enum | | |
| targetDetails.lookback | integer | | |

---

## 9. Enums Reference

### bidStrategy:
| Value | SP (dynamicBidding) | SB (bidOptimizationStrategy) |
|-------|--------------------|-----------------------------|
| SALES_DOWN_ONLY | LEGACY_FOR_SALES | none |
| SALES | AUTO_FOR_SALES | MAXIMIZE_IMMEDIATE_SALES |
| NEW_TO_BRAND | none | MAXIMIZE_NEW_TO_BRAND_CUSTOMERS |
| RULE_BASED | RULE_BASED | none if bidRule present |

### costType: CPC, VCPM

### currencyCode: AED, AUD, BRL, CAD, CHF, CNY, DKK, EUR, GBP, **INR**, JPY, MXN, NOK, SAR, SEK, SGD, TRY, USD, + many more

### deliveryStatus: DELIVERING, NOT_DELIVERING, UNAVAILABLE

### event: PURCHASE, VIEW

### goal: AWARENESS (reach), CONSIDERATION (clicks), CONVERSIONS (conversions)

### landingPageType:
| Value | IMAGE | VIDEO | PRODUCT_COLLECTION | STORE_SPOTLIGHT |
|-------|-------|-------|-------------------|-----------------|
| PRODUCT_LIST | | | x | |
| STORE | x | x | x | x |
| CUSTOM_URL | | | x | |
| DETAIL_PAGE | | x | | |
| OFF_AMAZON_LINK | x | | | |

### matchType - Auto targets:
| Value | SP Mapping | Description |
|-------|-----------|-------------|
| SEARCH_LOOSE_MATCH | QUERY_BROAD_REL_MATCHES | Loosely related search terms |
| SEARCH_CLOSE_MATCH | QUERY_HIGH_REL_MATCHES | Closely related search terms |
| PRODUCT_SUBSTITUTES | ASIN_SUBSTITUTE_RELATED | Similar product detail pages |
| PRODUCT_COMPLEMENTS | ASIN_ACCESSORY_RELATED | Complementary product pages |

### matchType - Keywords: BROAD, PHRASE, EXACT

### placement:
| Value | SP | SB |
|-------|----|----|
| HOME_PAGE | | HOME |
| TOP_OF_SEARCH | PLACEMENT_TOP | |
| PRODUCT_PAGE | PLACEMENT_PRODUCT_PAGE | DETAIL_PAGE |
| REST_OF_SEARCH | REST_OF_SEARCH | |

### state: ENABLED, PAUSED, ARCHIVED, OTHER

### targetingSettings: MANUAL, AUTO, T00020 (SD contextual), T00030 (SD audience)

### targetType: AUTO, KEYWORD, PRODUCT_CATEGORY, PRODUCT, PRODUCT_CATEGORY_AUDIENCE, PRODUCT_AUDIENCE, AUDIENCE

---

## 10. Rate Limits & FAQ

### Throttling:
- Queue-based throttling system
- Default cap: **5 jobs per endpoint** for all developers
- Per endpoint limit (e.g., 5 campaign exports + 5 ad group exports simultaneously)
- Must wait for completion before submitting more
- Contact support for limit increase

### Best Practice:
- Use exports to sync advertising data 1-2 times per day
- Do NOT use for continual real-time data retrieval
- Exclude campaign metadata from report requests, then join with export data using entity IDs

---
*Document version: 1.0 | Created: 13 April 2026*
