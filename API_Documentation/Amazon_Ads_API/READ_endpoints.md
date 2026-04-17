# Amazon Advertising API - READ Endpoints Reference v1.0
# =====================================================
# Account: Made in Heavens (GoAmrita Bhandar)
# Marketplace: Amazon.in (India) - EU Region
# Base URL: https://advertising-api-eu.amazon.com
# Profile ID: 42634532240933
# API Version: Ads API v1 Unified + Reporting API v3
# Created: 13 April 2026
# =====================================================

---

## Common Headers (Required for ALL Endpoints)

```
Authorization: Bearer {access_token}
Amazon-Advertising-API-ClientId: {client_id}
Amazon-Advertising-API-Scope: {profile_id}
```

**Token Refresh Endpoint:**
```
POST https://api.amazon.com/auth/o2/token
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&refresh_token={refresh_token}&client_id={client_id}&client_secret={client_secret}
```
Response: `{ "access_token": "...", "token_type": "bearer", "expires_in": 3600 }`

---

# SECTION 1: PROFILES API (v2)
===============================

## 1.1 List Profiles

Returns all advertising profiles associated with the account. Each profile represents a marketplace/country.

| Field | Value |
|-------|-------|
| **Endpoint** | `GET /v2/profiles` |
| **HTTP Method** | GET |
| **Content-Type** | Not needed (GET request) |
| **Accept** | `application/json` |
| **Rate Limit** | ~10 requests/second |

**Headers:**
```
Authorization: Bearer {access_token}
Amazon-Advertising-API-ClientId: {client_id}
```
Note: `Amazon-Advertising-API-Scope` is NOT needed for this endpoint (it returns all profiles).

**Request:** No body or parameters needed.

**Response (Array):**
```json
[
  {
    "profileId": 42634532240933,
    "countryCode": "IN",
    "currencyCode": "INR",
    "dailyBudget": 999999999.0,
    "timezone": "Asia/Kolkata",
    "accountInfo": {
      "marketplaceStringId": "A21TJRUUN4KGV",
      "id": "ENTITY1TVPGA5B1GOJW",
      "type": "seller",
      "name": "Made in Heavens",
      "validPaymentMethod": true
    }
  }
]
```

**Key Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| profileId | number | **Use as Amazon-Advertising-API-Scope header** |
| countryCode | string | IN, US, UK, etc. |
| currencyCode | string | INR, USD, GBP, etc. |
| accountInfo.type | string | "seller" or "vendor" |
| accountInfo.name | string | Account display name |
| accountInfo.validPaymentMethod | boolean | Whether payment method is set up |
| accountInfo.id | string | Entity ID |

**Business Meaning:** First API call to make. Returns profile_id needed for all subsequent calls. Verify India marketplace (countryCode: "IN") is present.

---

# SECTION 2: SPONSORED PRODUCTS - CAMPAIGNS
=============================================

## 2.1 List Campaigns

Returns all SP campaigns with full configuration details. Uses POST with filter body (NOT GET).

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /sp/campaigns/list` |
| **HTTP Method** | POST |
| **Content-Type** | `application/vnd.spCampaign.v3+json` |
| **Accept** | `application/vnd.spCampaign.v3+json` |
| **Rate Limit** | ~10 requests/second (shared across SP entity endpoints) |

**Headers:**
```
Content-Type: application/vnd.spCampaign.v3+json
Accept: application/vnd.spCampaign.v3+json
Authorization: Bearer {access_token}
Amazon-Advertising-API-ClientId: {client_id}
Amazon-Advertising-API-Scope: {profile_id}
```

**Request Body:**
```json
{
  "maxResults": 100,
  "stateFilter": {
    "include": ["ENABLED", "PAUSED", "ARCHIVED"]
  },
  "includeExtendedDataFields": true,
  "nextToken": null
}
```

**Request Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| maxResults | integer | No | Max results per page (default: 100, max: 100) |
| stateFilter.include | array[string] | No | Filter by state: ENABLED, PAUSED, ARCHIVED |
| includeExtendedDataFields | boolean | No | If true, includes servingStatus, lastUpdateDateTime |
| nextToken | string | No | Pagination token from previous response |
| nameFilter.queryTermMatchType | string | No | BROAD_MATCH or EXACT_MATCH |
| nameFilter.include | array[string] | No | Campaign names to filter |
| campaignIdFilter.include | array[string] | No | Specific campaign IDs to filter |
| portfolioIdFilter.include | array[string] | No | Filter by portfolio IDs |

**Response:**
```json
{
  "campaigns": [
    {
      "campaignId": "29137304488031",
      "name": "Campaign - 13/1/2026 21:20:59.241",
      "state": "ENABLED",
      "budget": {
        "budget": 500.0,
        "budgetType": "DAILY"
      },
      "dynamicBidding": {
        "strategy": "AUTO_FOR_SALES",
        "placementBidding": [
          { "placement": "PLACEMENT_TOP", "percentage": 25 },
          { "placement": "SITE_AMAZON_BUSINESS", "percentage": 25 }
        ]
      },
      "targetingType": "MANUAL",
      "startDate": "2026-01-13",
      "endDate": null,
      "marketplaceBudgetAllocation": "MANUAL",
      "tags": {},
      "offAmazonSettings": {},
      "extendedData": {
        "servingStatus": "CAMPAIGN_STATUS_ENABLED",
        "lastUpdateDateTime": "2026-04-10T12:00:00Z"
      }
    }
  ],
  "nextToken": "string_or_null"
}
```

**Key Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| campaignId | string | Unique campaign identifier |
| name | string | Campaign name |
| state | string | ENABLED, PAUSED, ARCHIVED |
| budget.budget | number | Daily budget in INR |
| budget.budgetType | string | DAILY |
| dynamicBidding.strategy | string | AUTO_FOR_SALES, LEGACY_FOR_SALES, MANUAL |
| dynamicBidding.placementBidding | array | Placement bid adjustments (percentage) |
| targetingType | string | MANUAL or AUTO |
| startDate | string | YYYY-MM-DD format |
| endDate | string/null | YYYY-MM-DD or null (ongoing) |
| extendedData.servingStatus | string | Detailed serving status |
| nextToken | string/null | For pagination |

**Bidding Strategy Values:**
| Value | Meaning |
|-------|---------|
| AUTO_FOR_SALES | Dynamic bids - up and down (recommended) |
| LEGACY_FOR_SALES | Dynamic bids - down only |
| MANUAL | Fixed bids |
| RULE_BASED | Rule-based bidding |

**Placement Values:**
| Value | Meaning |
|-------|---------|
| PLACEMENT_TOP | Top of search results |
| PLACEMENT_PRODUCT_PAGE | Product detail pages |
| PLACEMENT_REST_OF_SEARCH | Rest of search |
| SITE_AMAZON_BUSINESS | Amazon Business placements |

**Business Meaning:** Core endpoint for seeing all campaigns, their budgets, states, and bidding strategies. Use for campaign overview dashboard.

---

## 2.2 Get Campaign by ID

Get a single campaign's full details.

| Field | Value |
|-------|-------|
| **Endpoint** | `GET /sp/campaigns/{campaignId}` |
| **HTTP Method** | GET |
| **Content-Type** | Not needed |
| **Accept** | `application/vnd.spCampaign.v3+json` |

**Headers:**
```
Accept: application/vnd.spCampaign.v3+json
Authorization: Bearer {access_token}
Amazon-Advertising-API-ClientId: {client_id}
Amazon-Advertising-API-Scope: {profile_id}
```

**Request:** Campaign ID in URL path.

**Response:** Single campaign object (same structure as list item above, without the wrapper).

---

# SECTION 3: SPONSORED PRODUCTS - AD GROUPS
=============================================

## 3.1 List Ad Groups

Returns all ad groups with their default bids.

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /sp/adGroups/list` |
| **HTTP Method** | POST |
| **Content-Type** | `application/vnd.spAdGroup.v3+json` |
| **Accept** | `application/vnd.spAdGroup.v3+json` |
| **Rate Limit** | ~10 requests/second |

**Headers:**
```
Content-Type: application/vnd.spAdGroup.v3+json
Accept: application/vnd.spAdGroup.v3+json
Authorization: Bearer {access_token}
Amazon-Advertising-API-ClientId: {client_id}
Amazon-Advertising-API-Scope: {profile_id}
```

**Request Body:**
```json
{
  "maxResults": 100,
  "stateFilter": {
    "include": ["ENABLED", "PAUSED", "ARCHIVED"]
  },
  "nextToken": null,
  "campaignIdFilter": {
    "include": ["302164316622266"]
  }
}
```

**Request Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| maxResults | integer | No | Max results (default: 100) |
| stateFilter.include | array[string] | No | ENABLED, PAUSED, ARCHIVED |
| campaignIdFilter.include | array[string] | No | Filter by campaign IDs |
| adGroupIdFilter.include | array[string] | No | Filter by specific ad group IDs |
| nameFilter.include | array[string] | No | Filter by ad group names |
| nextToken | string | No | Pagination token |

**Response:**
```json
{
  "adGroups": [
    {
      "adGroupId": "448483975362602",
      "campaignId": "302164316622266",
      "name": "Ad Group - 20/3/2026 07:40:36.400",
      "defaultBid": 3.0,
      "state": "ENABLED"
    }
  ],
  "nextToken": "string_or_null"
}
```

**Key Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| adGroupId | string | Unique ad group identifier |
| campaignId | string | Parent campaign ID |
| name | string | Ad group name |
| defaultBid | number | Default bid (INR) for keywords without custom bids |
| state | string | ENABLED, PAUSED, ARCHIVED |

**Business Meaning:** Shows how campaigns are organized into ad groups. Each ad group has a default bid that applies to all its keywords unless overridden.

---

## 3.2 Get Ad Group by ID

| Field | Value |
|-------|-------|
| **Endpoint** | `GET /sp/adGroups/{adGroupId}` |
| **HTTP Method** | GET |
| **Accept** | `application/vnd.spAdGroup.v3+json` |

Same headers as list. Returns single ad group object.

---

# SECTION 4: SPONSORED PRODUCTS - KEYWORDS (POSITIVE)
======================================================

## 4.1 List Keywords

Returns all positive keywords with bids and match types.

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /sp/keywords/list` |
| **HTTP Method** | POST |
| **Content-Type** | `application/vnd.spKeyword.v3+json` |
| **Accept** | `application/vnd.spKeyword.v3+json` |
| **Rate Limit** | ~10 requests/second |

**Headers:**
```
Content-Type: application/vnd.spKeyword.v3+json
Accept: application/vnd.spKeyword.v3+json
Authorization: Bearer {access_token}
Amazon-Advertising-API-ClientId: {client_id}
Amazon-Advertising-API-Scope: {profile_id}
```

**Request Body:**
```json
{
  "maxResults": 100,
  "stateFilter": {
    "include": ["ENABLED", "PAUSED", "ARCHIVED"]
  },
  "campaignIdFilter": {
    "include": ["302164316622266"]
  },
  "adGroupIdFilter": {
    "include": ["448483975362602"]
  },
  "nextToken": null
}
```

**Request Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| maxResults | integer | No | Max results (default: 100) |
| stateFilter.include | array[string] | No | ENABLED, PAUSED, ARCHIVED |
| campaignIdFilter.include | array[string] | No | Filter by campaign IDs |
| adGroupIdFilter.include | array[string] | No | Filter by ad group IDs |
| keywordIdFilter.include | array[string] | No | Filter by keyword IDs |
| nextToken | string | No | Pagination token |

**Response:**
```json
{
  "keywords": [
    {
      "keywordId": "175803581922075",
      "campaignId": "302164316622266",
      "adGroupId": "448483975362602",
      "keywordText": "addyi",
      "matchType": "EXACT",
      "bid": 5.0,
      "state": "ENABLED"
    }
  ],
  "nextToken": "string_or_null"
}
```

**Key Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| keywordId | string | Unique keyword identifier |
| campaignId | string | Parent campaign ID |
| adGroupId | string | Parent ad group ID |
| keywordText | string | The actual keyword text |
| matchType | string | EXACT, PHRASE, or BROAD |
| bid | number | Custom bid in INR (overrides ad group default) |
| state | string | ENABLED, PAUSED, ARCHIVED |

**Match Type Values:**
| Value | Meaning |
|-------|---------|
| EXACT | Exact match - shows ad only for this exact search |
| PHRASE | Phrase match - shows ad when search contains this phrase |
| BROAD | Broad match - shows ad for related searches |

**Business Meaning:** Core targeting data. Shows which keywords trigger ads and what you bid for each. Essential for bid optimization.

---

## 4.2 Get Keyword by ID

| Field | Value |
|-------|-------|
| **Endpoint** | `GET /sp/keywords/{keywordId}` |
| **HTTP Method** | GET |
| **Accept** | `application/vnd.spKeyword.v3+json` |

Returns single keyword object.

---

# SECTION 5: SPONSORED PRODUCTS - NEGATIVE KEYWORDS
=====================================================

## 5.1 List Negative Keywords

Returns all negative keywords (keywords that PREVENT ads from showing).

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /sp/negativeKeywords/list` |
| **HTTP Method** | POST |
| **Content-Type** | `application/vnd.spNegativeKeyword.v3+json` |
| **Accept** | `application/vnd.spNegativeKeyword.v3+json` |
| **Rate Limit** | ~10 requests/second |

**Headers:**
```
Content-Type: application/vnd.spNegativeKeyword.v3+json
Accept: application/vnd.spNegativeKeyword.v3+json
Authorization: Bearer {access_token}
Amazon-Advertising-API-ClientId: {client_id}
Amazon-Advertising-API-Scope: {profile_id}
```

**Request Body:**
```json
{
  "maxResults": 100,
  "stateFilter": {
    "include": ["ENABLED", "PAUSED", "ARCHIVED"]
  },
  "campaignIdFilter": {
    "include": ["429878877190326"]
  },
  "nextToken": null
}
```

**Response:**
```json
{
  "negativeKeywords": [
    {
      "keywordId": "93947938042907",
      "campaignId": "429878877190326",
      "adGroupId": "297574255948083",
      "keywordText": "fastest weight gain capsule",
      "matchType": "NEGATIVE_EXACT",
      "state": "ENABLED"
    }
  ],
  "nextToken": "string_or_null"
}
```

**Key Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| keywordId | string | Unique negative keyword identifier |
| keywordText | string | Search term to block |
| matchType | string | NEGATIVE_EXACT or NEGATIVE_PHRASE |
| state | string | ENABLED or ARCHIVED |

**Match Type Values:**
| Value | Meaning |
|-------|---------|
| NEGATIVE_EXACT | Block only this exact search term |
| NEGATIVE_PHRASE | Block any search containing this phrase |

**Business Meaning:** Prevents wasted ad spend. Shows which unwanted search terms are being blocked. Critical for controlling ACOS.

---

## 5.2 List Campaign Negative Keywords

Negative keywords at the campaign level (apply to all ad groups in the campaign).

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /sp/campaignNegativeKeywords/list` |
| **HTTP Method** | POST |
| **Content-Type** | `application/vnd.spCampaignNegativeKeyword.v3+json` |
| **Accept** | `application/vnd.spCampaignNegativeKeyword.v3+json` |

Same request/response pattern as negativeKeywords/list, but returns campaign-level negatives.

---

# SECTION 6: SPONSORED PRODUCTS - PRODUCT ADS
===============================================

## 6.1 List Product Ads

Returns all product ads (ASIN/SKU assignments within ad groups).

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /sp/productAds/list` |
| **HTTP Method** | POST |
| **Content-Type** | `application/vnd.spProductAd.v3+json` |
| **Accept** | `application/vnd.spProductAd.v3+json` |
| **Rate Limit** | ~10 requests/second |

**Headers:**
```
Content-Type: application/vnd.spProductAd.v3+json
Accept: application/vnd.spProductAd.v3+json
Authorization: Bearer {access_token}
Amazon-Advertising-API-ClientId: {client_id}
Amazon-Advertising-API-Scope: {profile_id}
```

**Request Body:**
```json
{
  "maxResults": 100,
  "stateFilter": {
    "include": ["ENABLED", "PAUSED", "ARCHIVED"]
  },
  "campaignIdFilter": {
    "include": ["302164316622266"]
  },
  "nextToken": null
}
```

**Response:**
```json
{
  "productAds": [
    {
      "adId": "344613073990305",
      "campaignId": "302164316622266",
      "adGroupId": "448483975362602",
      "asin": "B0CV4FSM3C",
      "sku": "UsLabsAddyiPlusForWomen_30cps",
      "state": "PAUSED"
    }
  ],
  "nextToken": "string_or_null"
}
```

**Key Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| adId | string | Unique product ad identifier |
| campaignId | string | Parent campaign ID |
| adGroupId | string | Parent ad group ID |
| asin | string | Amazon Standard Identification Number |
| sku | string | Seller SKU |
| state | string | ENABLED, PAUSED, ARCHIVED |

**Business Meaning:** Shows which actual products (ASINs) are being advertised in which campaigns/ad groups. Map to see campaign -> product association.

---

## 6.2 Get Product Ad by ID

| Field | Value |
|-------|-------|
| **Endpoint** | `GET /sp/productAds/{adId}` |
| **HTTP Method** | GET |
| **Accept** | `application/vnd.spProductAd.v3+json` |

Returns single product ad object.

---

# SECTION 7: SPONSORED PRODUCTS - TARGETS (Product Targeting)
==============================================================

## 7.1 List Product Targets

Returns product targeting rules (ASIN targeting, category targeting).

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /sp/targets/list` |
| **HTTP Method** | POST |
| **Content-Type** | `application/vnd.spTargetingClause.v3+json` |
| **Accept** | `application/vnd.spTargetingClause.v3+json` |
| **Rate Limit** | ~10 requests/second |

**Headers:**
```
Content-Type: application/vnd.spTargetingClause.v3+json
Accept: application/vnd.spTargetingClause.v3+json
Authorization: Bearer {access_token}
Amazon-Advertising-API-ClientId: {client_id}
Amazon-Advertising-API-Scope: {profile_id}
```

**Request Body:**
```json
{
  "maxResults": 100,
  "stateFilter": {
    "include": ["ENABLED", "PAUSED", "ARCHIVED"]
  },
  "campaignIdFilter": {
    "include": ["302164316622266"]
  },
  "nextToken": null
}
```

**Response:**
```json
{
  "targetingClauses": [
    {
      "targetId": "123456789",
      "campaignId": "302164316622266",
      "adGroupId": "448483975362602",
      "expressionType": "MANUAL",
      "expression": [
        {
          "type": "asinSameAs",
          "value": "B0ABC12345"
        }
      ],
      "resolvedExpression": [
        {
          "type": "asinSameAs",
          "value": "B0ABC12345"
        }
      ],
      "bid": 5.0,
      "state": "ENABLED"
    }
  ],
  "nextToken": "string_or_null"
}
```

**Expression Type Values:**
| Value | Meaning |
|-------|---------|
| MANUAL | Manually defined targeting expression |
| AUTO | Auto-generated targeting (from auto campaigns) |

**Targeting Expression Types:**
| type | Description |
|------|-------------|
| asinSameAs | Target specific ASIN |
| asinCategorySameAs | Target all ASINs in a category |
| asinBrandSameAs | Target all ASINs of a brand |
| asinPriceLessThan | Target ASINs below a price |
| asinPriceGreaterThan | Target ASINs above a price |
| asinPriceBetween | Target ASINs in a price range |
| asinReviewRatingLessThan | Target ASINs with lower ratings |
| asinReviewRatingGreaterThan | Target ASINs with higher ratings |
| asinReviewRatingBetween | Target ASINs in a rating range |
| queryBroadRelMatches | Auto: Broad match (loose) |
| queryHighRelMatches | Auto: Close match |
| asinSubstituteRelated | Auto: Substitutes |
| asinAccessoryRelated | Auto: Complements |

**Business Meaning:** Shows product targeting rules for manual targeting campaigns. Auto campaigns have auto-generated targeting expressions.

---

## 7.2 List Negative Targets

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /sp/negativeTargets/list` |
| **HTTP Method** | POST |
| **Content-Type** | `application/vnd.spNegativeTargetingClause.v3+json` |
| **Accept** | `application/vnd.spNegativeTargetingClause.v3+json` |

Same pattern as targets/list. Returns ASINs/brands/categories to EXCLUDE from targeting.

---

# SECTION 8: REPORTING API v3 (Async Reports with Performance Metrics)
======================================================================

The Reporting API is async: Create -> Poll -> Download.
This is the ONLY way to get performance metrics (impressions, clicks, spend, orders, sales).

## 8.1 Create Report

Creates an async report request that Amazon processes in the background.

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /reporting/reports` |
| **HTTP Method** | POST |
| **Content-Type** | `application/vnd.createasyncreportrequest.v3+json` |
| **Accept** | `application/vnd.createasyncreportrequest.v3+json` |
| **Rate Limit** | ~10 requests/second |

**Headers:**
```
Content-Type: application/vnd.createasyncreportrequest.v3+json
Accept: application/vnd.createasyncreportrequest.v3+json
Authorization: Bearer {access_token}
Amazon-Advertising-API-ClientId: {client_id}
Amazon-Advertising-API-Scope: {profile_id}
```

**Request Body:**
```json
{
  "name": "GoAmrita SP Campaign Report 2026-04-05 to 2026-04-11",
  "startDate": "2026-04-05",
  "endDate": "2026-04-11",
  "configuration": {
    "adProduct": "SPONSORED_PRODUCTS",
    "groupBy": ["campaign"],
    "columns": [
      "campaignName", "campaignId", "campaignStatus",
      "campaignBudgetAmount", "campaignBudgetType",
      "impressions", "clicks", "cost",
      "purchases7d", "sales7d",
      "costPerClick", "clickThroughRate"
    ],
    "reportTypeId": "spCampaigns",
    "timeUnit": "DAILY",
    "format": "GZIP_JSON"
  }
}
```

**Request Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | No | Human-readable report name |
| startDate | string | Yes | YYYY-MM-DD format |
| endDate | string | Yes | YYYY-MM-DD format (max 60 days range) |
| configuration.adProduct | string | Yes | Always "SPONSORED_PRODUCTS" for SP |
| configuration.groupBy | array[string] | Yes | Aggregation level (see per-report docs) |
| configuration.columns | array[string] | Yes | Which data columns to include |
| configuration.reportTypeId | string | Yes | Report type (see section 8.4) |
| configuration.timeUnit | string | Yes | DAILY or SUMMARY |
| configuration.format | string | Yes | GZIP_JSON (recommended) |
| configuration.filters | array | No | Optional filters (see below) |

**Filter Example:**
```json
{
  "configuration": {
    "filters": [
      {
        "field": "campaignStatus",
        "values": ["ENABLED"]
      }
    ]
  }
}
```

**Response:**
```json
{
  "reportId": "amzn1.report.abc123",
  "status": "PROCESSING",
  "createdAt": "2026-04-12T10:00:00Z",
  "updatedAt": "2026-04-12T10:00:00Z",
  "configuration": { ... }
}
```

---

## 8.2 Get Report Status

Check if the async report is ready for download.

| Field | Value |
|-------|-------|
| **Endpoint** | `GET /reporting/reports/{reportId}` |
| **HTTP Method** | GET |
| **Accept** | `application/vnd.createasyncreportrequest.v3+json` |

**Headers:**
```
Accept: application/vnd.createasyncreportrequest.v3+json
Authorization: Bearer {access_token}
Amazon-Advertising-API-ClientId: {client_id}
Amazon-Advertising-API-Scope: {profile_id}
```

**Response:**
```json
{
  "reportId": "amzn1.report.abc123",
  "status": "COMPLETED",
  "url": "https://advertising-api-eu.amazon.com/...",
  "fileSize": 12345,
  "createdAt": "2026-04-12T10:00:00Z",
  "updatedAt": "2026-04-12T10:01:30Z"
}
```

**Status Values:**
| Value | Meaning | Action |
|-------|---------|--------|
| PROCESSING | Report is being generated | Wait and poll again (10s interval) |
| COMPLETED | Report is ready | Download from `url` field |
| FAILURE | Report generation failed | Check error, retry |

**Business Meaning:** Poll this endpoint every 10 seconds after creating a report. Typical completion time: 30-120 seconds.

---

## 8.3 Download Report

Download the completed report file. The URL is from the status response.

| Field | Value |
|-------|-------|
| **Endpoint** | `GET {url from report status}` |
| **HTTP Method** | GET |
| **Auth** | No auth headers needed (pre-signed URL) |

**Response:** GZIP compressed JSON. Decompress with gzip, parse as JSON array.

```python
import gzip, json
decompressed = gzip.decompress(response_bytes)
data = json.loads(decompressed.decode())  # Returns list of dicts
```

---

## 8.4 Report Types & Available Columns

### 8.4.1 spCampaigns (Campaign-Level Report)

**reportTypeId:** `spCampaigns`
**groupBy options:** `["campaign"]`
**timeUnit:** `DAILY` or `SUMMARY`

**Available Columns:**

| Column | Type | Description |
|--------|------|-------------|
| **Dimension Columns** | | |
| campaignName | string | Campaign name |
| campaignId | number | Campaign ID |
| campaignStatus | string | ENABLED, PAUSED, ARCHIVED |
| campaignBudgetAmount | number | Daily budget (INR) |
| campaignBudgetType | string | DAILY_BUDGET |
| campaignBudgetCurrencyCode | string | INR |
| date | string | Date (YYYY-MM-DD) - only with DAILY timeUnit |
| **Performance Metrics** | | |
| impressions | integer | Number of ad impressions |
| clicks | integer | Number of clicks |
| cost | number | Total ad spend (INR) |
| costPerClick | number | Average CPC (INR) |
| clickThroughRate | number | CTR as percentage (e.g., 1.5 = 1.5%) |
| **Attribution Metrics (by lookback window)** | | |
| purchases1d | integer | Orders attributed (1-day window) |
| purchases7d | integer | Orders attributed (7-day window) |
| purchases14d | integer | Orders attributed (14-day window) |
| purchases30d | integer | Orders attributed (30-day window) |
| sales1d | number | Revenue attributed (1-day window, INR) |
| sales7d | number | Revenue attributed (7-day window, INR) |
| sales14d | number | Revenue attributed (14-day window, INR) |
| sales30d | number | Revenue attributed (30-day window, INR) |
| unitsSoldClicks1d | integer | Units sold (1-day) |
| unitsSoldClicks7d | integer | Units sold (7-day) |
| unitsSoldClicks14d | integer | Units sold (14-day) |
| unitsSoldClicks30d | integer | Units sold (30-day) |
| topOfSearchImpressionShare | number | Share of top-of-search impressions |

**Example Response Row (DAILY):**
```json
{
  "campaignName": "Campaign - 13/1/2026 21:20:59.241",
  "campaignId": 29137304488031,
  "campaignStatus": "ENABLED",
  "campaignBudgetAmount": 500.0,
  "campaignBudgetType": "DAILY_BUDGET",
  "impressions": 325,
  "clicks": 3,
  "cost": 19.75,
  "costPerClick": 6.58,
  "clickThroughRate": 0.923,
  "purchases1d": 0,
  "purchases7d": 0,
  "purchases14d": 0,
  "purchases30d": 0,
  "sales1d": 0,
  "sales7d": 0,
  "sales14d": 0,
  "sales30d": 0
}
```

---

### 8.4.2 spSearchTerm (Search Term Report)

**reportTypeId:** `spSearchTerm`
**groupBy options:** `["searchTerm"]`
**timeUnit:** `DAILY` or `SUMMARY`

**Available Columns:**

| Column | Type | Description |
|--------|------|-------------|
| **Dimension Columns** | | |
| searchTerm | string | Actual customer search query |
| campaignName | string | Campaign name |
| campaignId | number | Campaign ID |
| adGroupName | string | Ad group name |
| adGroupId | number | Ad group ID |
| keyword | string | Matched keyword (or "loose-match", "close-match" for auto) |
| keywordId | number | Keyword ID |
| keywordType | string | TARGETING_EXPRESSION, TARGETING_EXPRESSION_PREDEFINED, BROAD, PHRASE, EXACT |
| **Performance Metrics** | | |
| impressions | integer | Impressions |
| clicks | integer | Clicks |
| cost | number | Spend (INR) |
| costPerClick | number | CPC (INR) |
| clickThroughRate | number | CTR % |
| **Attribution Metrics** | | |
| purchases1d / 7d / 14d / 30d | integer | Orders by lookback window |
| sales1d / 7d / 14d / 30d | number | Revenue by lookback window (INR) |

**Example Response Row:**
```json
{
  "searchTerm": "libidex capsule",
  "campaignName": "Campaign - Libidexx",
  "campaignId": 407322014558764,
  "adGroupName": "Ad Group - Libidex",
  "adGroupId": 414466891622281,
  "keyword": "libidex capsule",
  "keywordId": 113563727847553,
  "keywordType": "PHRASE",
  "impressions": 2,
  "clicks": 1,
  "cost": 9.44,
  "costPerClick": 9.44,
  "clickThroughRate": 50,
  "purchases7d": 0,
  "sales7d": 0
}
```

**Business Meaning:** THE MOST VALUABLE REPORT. Shows exactly what customers searched to trigger your ads. Essential for:
- Finding new high-converting keywords to add as exact match
- Finding irrelevant searches to add as negative keywords
- Understanding actual ACOS per search term

---

### 8.4.3 spTargeting (Keyword/Target-Level Report)

**reportTypeId:** `spTargeting`
**groupBy options:** `["targeting"]`
**timeUnit:** `DAILY` or `SUMMARY`

**Available Columns:**

| Column | Type | Description |
|--------|------|-------------|
| **Dimension Columns** | | |
| campaignName | string | Campaign name |
| campaignId | number | Campaign ID |
| adGroupName | string | Ad group name |
| adGroupId | number | Ad group ID |
| keyword | string | Keyword or targeting expression text |
| keywordId | number | Keyword/target ID |
| matchType | string | EXACT, PHRASE, BROAD, TARGETING_EXPRESSION, TARGETING_EXPRESSION_PREDEFINED |
| keywordType | string | Type of keyword |
| keywordBid | number | Current bid amount |
| **Performance Metrics** | | |
| impressions | integer | Impressions |
| clicks | integer | Clicks |
| cost | number | Spend (INR) |
| costPerClick | number | CPC |
| clickThroughRate | number | CTR % |
| **Attribution Metrics** | | |
| purchases1d / 7d / 14d / 30d | integer | Orders |
| sales1d / 7d / 14d / 30d | number | Revenue (INR) |

**Business Meaning:** Performance at the keyword/target level. Shows which keywords are profitable and which are wasting money. Use for bid optimization.

---

### 8.4.4 spAdvertisedProduct (Advertised Product Report)

**reportTypeId:** `spAdvertisedProduct`
**groupBy options:** `["advertiser"]`
**timeUnit:** `DAILY` or `SUMMARY`

**Available Columns:**

| Column | Type | Description |
|--------|------|-------------|
| **Dimension Columns** | | |
| campaignName | string | Campaign name |
| campaignId | number | Campaign ID |
| adGroupName | string | Ad group name |
| adGroupId | number | Ad group ID |
| advertisedAsin | string | ASIN being advertised |
| advertisedSku | string | SKU of advertised product |
| **Performance Metrics** | | |
| impressions | integer | Impressions |
| clicks | integer | Clicks |
| cost | number | Spend (INR) |
| costPerClick | number | CPC |
| clickThroughRate | number | CTR % |
| **Attribution Metrics** | | |
| purchases1d / 7d / 14d / 30d | integer | Orders |
| sales1d / 7d / 14d / 30d | number | Revenue (INR) |
| unitsSoldClicks1d / 7d / 14d / 30d | integer | Units sold |

**Example Response Row:**
```json
{
  "campaignName": "TL_EL_SPN_SG_FEB_Listed",
  "campaignId": 429878877190326,
  "adGroupName": "Ad group - 18/2/2025 07:26:41.735",
  "adGroupId": 297574255948083,
  "advertisedAsin": "B0DX7J5ZXT",
  "advertisedSku": "JoshBoosterLibidex30_p2",
  "impressions": 1200,
  "clicks": 8,
  "cost": 101.89,
  "costPerClick": 12.74,
  "clickThroughRate": 0.67,
  "purchases7d": 1,
  "sales7d": 2413.34
}
```

**Business Meaning:** Performance per advertised product (ASIN). Shows which products are performing well in ads and which are not. Use for product-level ACOS analysis.

---

### 8.4.5 spPurchasedProduct (Purchased Product Report)

**reportTypeId:** `spPurchasedProduct`
**groupBy options:** `["asin"]`
**timeUnit:** `DAILY` or `SUMMARY`

**Available Columns:**

| Column | Type | Description |
|--------|------|-------------|
| **Dimension Columns** | | |
| campaignName | string | Campaign name |
| campaignId | number | Campaign ID |
| adGroupName | string | Ad group name |
| adGroupId | number | Ad group ID |
| keyword | string | Keyword that triggered |
| matchType | string | Match type |
| advertisedAsin | string | ASIN in the ad |
| advertisedSku | string | SKU in the ad |
| purchasedAsin | string | ASIN actually purchased |
| **Attribution Metrics** | | |
| purchases7d / 14d | integer | Orders (only 7d and 14d available) |
| sales7d / 14d | number | Revenue (INR) |
| unitsSoldClicks7d / 14d | integer | Units sold |

**Example Response Row:**
```json
{
  "campaignName": "TL_EL_SPN_SG_FEB_Listed",
  "campaignId": 429878877190326,
  "adGroupName": "Ad group - 18/2/2025 07:26:41.735",
  "adGroupId": 297574255948083,
  "keyword": "libidex capsule men original",
  "matchType": "PHRASE",
  "advertisedAsin": "B0DX7J5ZXT",
  "advertisedSku": "JoshBoosterLibidex30_p2",
  "purchasedAsin": "B0FF39TSL1",
  "purchases7d": 0,
  "sales7d": 0
}
```

**Business Meaning:** Shows WHAT customers actually bought after clicking your ad. The purchasedAsin may differ from advertisedAsin (cross-product purchases). Essential for understanding true attribution.

---

# SECTION 9: BUDGET RECOMMENDATIONS
=====================================

## 9.1 Get Campaign Budget Recommendations

Get Amazon's recommended budget for a campaign.

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /sp/campaigns/budgetRecommendations` |
| **HTTP Method** | POST |
| **Content-Type** | `application/vnd.spbudgetrecommendation.v3+json` |
| **Accept** | `application/vnd.spbudgetrecommendation.v3+json` |

**Headers:**
```
Content-Type: application/vnd.spbudgetrecommendation.v3+json
Accept: application/vnd.spbudgetrecommendation.v3+json
Authorization: Bearer {access_token}
Amazon-Advertising-API-ClientId: {client_id}
Amazon-Advertising-API-Scope: {profile_id}
```

**Request Body:**
```json
{
  "campaignId": "302164316622266"
}
```

**Response:**
```json
{
  "campaignId": "302164316622266",
  "suggestedBudget": 750.0,
  "missedOpportunities": {
    "estimatedMissedImpressions": 1500,
    "estimatedMissedClicks": 45,
    "estimatedMissedSales": 2500.0
  },
  "sevenDayBudgetForecast": {
    "currentBudget": 500.0,
    "suggestedBudget": 750.0,
    "averageDailyMissedOpportunities": {
      "impressions": 214,
      "clicks": 6,
      "sales": 357.14
    }
  }
}
```

**Business Meaning:** Amazon tells you if your budget is too low and estimates what you're missing. Use to decide budget increases.

---

# SECTION 10: KEYWORD RECOMMENDATIONS / SUGGESTIONS
====================================================

## 10.1 Get Keyword Recommendations for Ad Group

Get Amazon's suggested keywords for an ad group based on the products in it.

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /sp/targets/keywords/recommendations` |
| **HTTP Method** | POST |
| **Content-Type** | `application/vnd.spKeywordRecommendations.v4+json` |
| **Accept** | `application/vnd.spKeywordRecommendations.v4+json` |

**Headers:**
```
Content-Type: application/vnd.spKeywordRecommendations.v4+json
Accept: application/vnd.spKeywordRecommendations.v4+json
Authorization: Bearer {access_token}
Amazon-Advertising-API-ClientId: {client_id}
Amazon-Advertising-API-Scope: {profile_id}
```

**Request Body (by ad group):**
```json
{
  "campaignId": "302164316622266",
  "adGroupId": "448483975362602",
  "recommendationType": "KEYWORDS_FOR_ADGROUP",
  "maxRecommendations": 100,
  "sortDimension": "CLICKS",
  "locale": "en_IN"
}
```

**Request Body (by ASINs):**
```json
{
  "recommendationType": "KEYWORDS_FOR_ASINS",
  "asins": ["B0DX7J5ZXT", "B0DC48PQM7"],
  "maxRecommendations": 100,
  "sortDimension": "CLICKS",
  "locale": "en_IN"
}
```

**Request Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| recommendationType | string | Yes | KEYWORDS_FOR_ADGROUP or KEYWORDS_FOR_ASINS |
| campaignId | string | Conditional | Required for KEYWORDS_FOR_ADGROUP |
| adGroupId | string | Conditional | Required for KEYWORDS_FOR_ADGROUP |
| asins | array[string] | Conditional | Required for KEYWORDS_FOR_ASINS |
| maxRecommendations | integer | No | Max suggestions (default: 100) |
| sortDimension | string | No | CLICKS, CONVERSIONS, DEFAULT |
| locale | string | No | en_IN for India |

**Response:**
```json
{
  "recommendations": [
    {
      "keyword": "libidex capsule for men",
      "matchType": "BROAD",
      "recId": "abc123",
      "bid": {
        "rangeStart": 2.0,
        "rangeEnd": 8.0,
        "suggested": 5.0
      },
      "translation": null
    }
  ],
  "totalResults": 85
}
```

**Business Meaning:** Amazon suggests keywords for your products. Use to find new keywords to add. The bid suggestions are helpful as starting bids.

---

# SECTION 11: BID RECOMMENDATIONS
===================================

## 11.1 Get Bid Recommendations for Keywords

Get recommended bids for existing keywords.

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /sp/targets/bid/recommendations` |
| **HTTP Method** | POST |
| **Content-Type** | `application/vnd.spThemeBasedBidRecommendation.v4+json` |
| **Accept** | `application/vnd.spThemeBasedBidRecommendation.v4+json` |

**Headers:**
```
Content-Type: application/vnd.spThemeBasedBidRecommendation.v4+json
Accept: application/vnd.spThemeBasedBidRecommendation.v4+json
Authorization: Bearer {access_token}
Amazon-Advertising-API-ClientId: {client_id}
Amazon-Advertising-API-Scope: {profile_id}
```

**Request Body:**
```json
{
  "campaignId": "302164316622266",
  "adGroupId": "448483975362602",
  "targetingExpressions": [
    {
      "type": "keyword",
      "value": "addyi"
    },
    {
      "type": "keyword",
      "value": "libidex capsule"
    }
  ]
}
```

**Alternative Request (for existing keywords by ID):**
```json
{
  "keywordId": "175803581922075",
  "campaignId": "302164316622266",
  "adGroupId": "448483975362602"
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "keyword": "addyi",
      "matchType": "EXACT",
      "bidValues": {
        "suggested": 5.50,
        "rangeStart": 2.0,
        "rangeMedian": 5.0,
        "rangeEnd": 12.0
      },
      "theme": "CONVERSIONS",
      "impact": {
        "estimatedClicks": 15,
        "estimatedImpressions": 500,
        "estimatedConversions": 2
      }
    }
  ]
}
```

**Business Meaning:** Amazon suggests optimal bid amounts based on competition and expected performance. Use for bid optimization to maximize ROI.

---

# SECTION 12: PAGINATION PATTERN
==================================

All list endpoints use the same pagination pattern:

```python
all_items = []
next_token = None

while True:
    body = {"maxResults": 100}
    if next_token:
        body["nextToken"] = next_token
    
    response = api_call("POST", "/sp/campaigns/list", body=body, ...)
    
    items = response.get("campaigns", [])  # or "adGroups", "keywords", etc.
    all_items.extend(items)
    
    next_token = response.get("nextToken")
    if not next_token:
        break

# all_items now has everything
```

---

# SECTION 13: ERROR CODES REFERENCE
=====================================

| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| 200 | Success | Process response |
| 207 | Partial success (batch) | Check individual items for errors |
| 400 | Bad request | Check request body format |
| 401 | Unauthorized | Refresh access token |
| 403 | Forbidden | Check profile_id, client_id, permissions |
| 404 | Not found | Check resource ID |
| 422 | Unprocessable entity | Check field values |
| 429 | Rate limit exceeded | Wait and retry (exponential backoff) |
| 500 | Server error | Retry after delay |

---

# SECTION 14: RATE LIMITS
===========================

| API Category | Limit | Notes |
|-------------|-------|-------|
| SP Entity Operations (campaigns, ad groups, keywords, etc.) | ~10 req/sec per profile | Shared across all entity endpoints |
| Reporting API (create/status) | ~10 req/sec per profile | Separate from entity limits |
| Profile API | ~10 req/sec | Lighter limit |
| Budget/Bid Recommendations | ~5 req/sec | More restrictive |

**Best Practices:**
- Implement exponential backoff on 429 errors
- Sleep 100ms between sequential calls
- Batch operations where possible
- Cache results that don't change frequently (profiles, campaign structure)

---

# SECTION 15: ENDPOINT QUICK REFERENCE TABLE
==============================================

| Endpoint | Method | Content-Type Suffix | Returns |
|----------|--------|-------------------|---------|
| /v2/profiles | GET | - | All profiles/marketplaces |
| /sp/campaigns/list | POST | spCampaign.v3+json | Campaign list with config |
| /sp/campaigns/{id} | GET | spCampaign.v3+json | Single campaign |
| /sp/adGroups/list | POST | spAdGroup.v3+json | Ad group list |
| /sp/adGroups/{id} | GET | spAdGroup.v3+json | Single ad group |
| /sp/keywords/list | POST | spKeyword.v3+json | Positive keyword list |
| /sp/keywords/{id} | GET | spKeyword.v3+json | Single keyword |
| /sp/negativeKeywords/list | POST | spNegativeKeyword.v3+json | Negative keyword list |
| /sp/campaignNegativeKeywords/list | POST | spCampaignNegativeKeyword.v3+json | Campaign-level negatives |
| /sp/productAds/list | POST | spProductAd.v3+json | Product ad list |
| /sp/productAds/{id} | GET | spProductAd.v3+json | Single product ad |
| /sp/targets/list | POST | spTargetingClause.v3+json | Product target list |
| /sp/negativeTargets/list | POST | spNegativeTargetingClause.v3+json | Negative target list |
| /reporting/reports | POST | createasyncreportrequest.v3+json | Create async report |
| /reporting/reports/{id} | GET | createasyncreportrequest.v3+json | Report status/URL |
| /sp/campaigns/budgetRecommendations | POST | spbudgetrecommendation.v3+json | Budget suggestions |
| /sp/targets/keywords/recommendations | POST | spKeywordRecommendations.v4+json | Keyword suggestions |
| /sp/targets/bid/recommendations | POST | spThemeBasedBidRecommendation.v4+json | Bid suggestions |

---

*Document Version: 1.0 | Created: 13 April 2026*
*Based on: Amazon Ads API v1 Unified + Reporting API v3*
*Verified against live API responses from Made in Heavens account*
