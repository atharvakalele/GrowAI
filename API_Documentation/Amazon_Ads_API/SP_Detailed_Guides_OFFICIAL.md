# Sponsored Products - Detailed Implementation Guides (OFFICIAL)
**Source:** Official Amazon Advertising documentation (manually copied by Msir)
**Date Captured:** 13 April 2026
**API Version:** SP v3 + Campaign Management API v1
**Our Endpoint:** advertising-api-eu.amazon.com
**Our Profile ID:** 42634532240933
**Part of:** Part 3 API documentation batch

---

## Table of Contents
1. [SP Overview](#1-sp-overview)
2. [Campaign Structure](#2-campaign-structure)
3. [Creating Auto Campaigns](#3-creating-auto-campaigns)
4. [Creating Manual Campaigns](#4-creating-manual-campaigns)
5. [Feature Availability by Marketplace](#5-feature-availability-by-marketplace)
6. [Campaigns - Create Endpoint with Examples](#6-campaigns---create-endpoint)
7. [Ad Groups - Create Endpoint with Examples](#7-ad-groups---create-endpoint)
8. [Product Ads - Create Endpoint with Examples](#8-product-ads---create-endpoint)
9. [Keyword Targeting](#9-keyword-targeting)
10. [Keyword Recommendations (v3/v4/v5)](#10-keyword-recommendations)
11. [Keyword Groups (Beta)](#11-keyword-groups-beta)
12. [Product & Category Targeting](#12-product--category-targeting)
13. [Product Targeting Recommendations](#13-product-targeting-recommendations)
14. [Category Suggestions & Refinements](#14-category-suggestions--refinements)
15. [Auto Targeting](#15-auto-targeting)
16. [Negative Keyword Targeting](#16-negative-keyword-targeting)
17. [Negative Product/Brand Targeting](#17-negative-productbrand-targeting)
18. [Budget Recommendations](#18-budget-recommendations)
19. [Theme-Based Bid Suggestions](#19-theme-based-bid-suggestions)

---

## 1. SP Overview

Sponsored Products campaigns advertise products in high-visibility placements on Amazon. Available for vendors, sellers, and Kindle Direct Publishing (KDP) authors.

---

## 2. Campaign Structure

### Auto Campaigns:
- Create: Campaign + Ad Group + Product Ad (minimum)
- Amazon assigns targeting expressions and keywords
- Optional: Auto targeting expressions, negative targets

### Manual Campaigns:
- Create: Campaign + Ad Group + Product Ad + at least 1 target/keyword
- Advertiser controls all keywords and product targeting
- Supports: Keyword targeting, product targeting, category targeting

### Both Campaign Types Support:
- Negative keyword targeting (campaign + ad group level)
- Negative product targeting (campaign + ad group level)

---

## 3. Creating Auto Campaigns

### Endpoint: `POST /adsApi/v1/create/campaigns`

Set `autoCreateTargets: true` in `autoCreationSettings`.

### Steps:
1. Create campaign (autoCreateTargets = true)
2. Create ad group(s) - `POST /adsApi/v1/create/adGroups`
3. Create product ad(s) - `POST /adsApi/v1/create/ads`
4. (Optional) Set auto targeting bids - `PUT /adsApi/v1/update/targets`
5. (Optional) Set negative targeting - `POST /adsApi/v1/create/targets` (negative=true)

---

## 4. Creating Manual Campaigns

### Endpoint: `POST /adsApi/v1/create/campaigns`

Set `autoCreateTargets: false` in `autoCreationSettings`.

### Steps:
1. Create campaign (autoCreateTargets = false)
2. Create ad group(s)
3. Create product ad(s)
4. Add targeting (at least one per ad group):
   - **Product targeting:** Get recommendations via `POST /sp/targets/products/recommendations`, create via `POST /adsApi/v1/create/targets`
   - **Category targeting:** Explore via `GET /sp/targets/categories`, get suggestions via `POST /sp/targets/categories/recommendations`, refinements via `GET sp/targets/category/{categoryId}/refinements`, create via `POST /adsApi/v1/create/targets`
   - **Keyword targeting:** Get recommendations via `POST /sp/targets/keywords/recommendations`, create via `POST /adsApi/v1/create/targets`
5. (Optional) Negative targeting

---

## 5. Feature Availability by Marketplace

### Campaign Management:
**Resources:** `/adsApi/v1/*/campaigns`, `/adsApi/v1/*/adGroups`, `/adsApi/v1/*/ads`, `/adsApi/v1/*/targets`

**Available in:**
- North America: US, CA, MX
- South America: BR
- Europe: DE, ES, FR, IT, UK, NL, SE, TR, PL, BE
- Middle East: UAE, EG, SA
- Asia Pacific: JP, **IN**, AU, SG
- Africa: ZA

### Rule-based Bidding (`/sp/rules/campaignOptimization`):
US, CA, MX, UK, DE, FR, JP

### Consolidated Recommendations (`/sp/campaign/recommendations`):
US only

### Product Recommendations (`/sp/targets/products/recommendations`):
All marketplaces (same as Campaign Management)

### Theme-based Bid Suggestions (`/sp/targets/bid/recommendations`):
US, CA, DE, ES, FR, UK, JP, **IN**

### Budget Recommendation (`/sp/campaigns/budgetRecommendations`):
US, CA, MX, DE, ES, FR, UK, IT, JP, **IN**, AU, UAE

---

## 6. Campaigns - Create Endpoint

### `POST /adsApi/v1/create/campaigns`

### Manual Campaign Example:
```json
{
  "campaigns": [{
    "adProduct": "SPONSORED_PRODUCTS",
    "autoCreationSettings": { "autoCreateTargets": false },
    "budgets": [{
      "budgetType": "MONETARY",
      "budgetValue": {
        "monetaryBudgetValue": {
          "monetaryBudget": { "value": 100 }
        }
      },
      "recurrenceTimePeriod": "DAILY"
    }],
    "countries": ["US"],
    "endDateTime": "2026-08-24T14:15:22Z",
    "marketplaceScope": "SINGLE_MARKETPLACE",
    "marketplaces": ["US"],
    "name": "Test SP Manual campaign",
    "optimizations": {
      "bidSettings": {
        "bidAdjustments": {
          "placementBidAdjustments": [{
            "percentage": 900,
            "placement": "TOP_OF_SEARCH"
          }]
        },
        "bidStrategy": "SALES_DOWN_ONLY"
      }
    },
    "startDateTime": "2026-02-24T14:15:22Z",
    "state": "ENABLED"
  }]
}
```

**Response (207):** Returns campaignId, full campaign object with deliveryStatus.

---

## 7. Ad Groups - Create Endpoint

### `POST /adsApi/v1/create/adGroups`

```json
{
  "adGroups": [{
    "adProduct": "SPONSORED_PRODUCTS",
    "bid": { "defaultBid": 3.0 },
    "campaignId": "123456780123",
    "name": "Test SP AdGroup",
    "state": "ENABLED"
  }]
}
```

### Best Practices:
- Descriptive names (internal only, not visible to shoppers)
- Group similar products
- Default bid applies to all child entities without explicit bids

---

## 8. Product Ads - Create Endpoint

### `POST /adsApi/v1/create/ads`

### Check eligibility first: `POST /eligibility/product/list`

### Vendor (ASIN):
```json
{
  "ads": [{
    "adGroupId": "3465462435645",
    "adProduct": "SPONSORED_PRODUCTS",
    "adType": "PRODUCT_AD",
    "creative": {
      "productCreative": {
        "productCreativeSettings": {
          "advertisedProduct": {
            "productId": "B09XBVBHR2",
            "productIdType": "ASIN"
          }
        }
      }
    },
    "state": "ENABLED"
  }]
}
```

### Seller (SKU):
Use `"productIdType": "SKU"` with SKU value.

### KDP Author (with headline):
Add `"headline": "An exciting thriller for all!"` in productCreativeSettings. Note: If headline is used, only 1 product ad per ad group.

---

## 9. Keyword Targeting

### Create Keyword: `POST /adsApi/v1/create/targets`

```json
{
  "targets": [{
    "adGroupId": "12345678090234",
    "adProduct": "SPONSORED_PRODUCTS",
    "bid": { "bid": 0.02 },
    "state": "ENABLED",
    "negative": false,
    "targetDetails": {
      "keywordTarget": {
        "keyword": "soap bar",
        "matchType": "EXACT"
      }
    },
    "targetType": "KEYWORD"
  }]
}
```

### With nativeLanguageLocale (for non-English regions):
Add `"nativeLanguageLocale": "zh_CN"` and `"nativeLanguageKeyword": "Chinese text"`.

---

## 10. Keyword Recommendations

### Endpoint: `POST /sp/targets/keywords/recommendations`

### Versions:
- **v3:** Base recommendations by ASINs or campaign+adGroup
- **v4:** Adds search term impression share and rank metrics
- **v5 (recommended):** Adds theme-based bid recommendations with impact metrics (weekly clicks, purchase orders)

### v5 Request Example:
```json
{
  "recommendationType": "KEYWORDS_FOR_ASINS",
  "biddingStrategy": "AUTO_FOR_SALES",
  "sortDimension": "CLICKS",
  "asins": ["asin1", "asin2"],
  "bidsEnabled": true
}
```

### Response includes:
- `keywordTargetList`: Keywords with bidInfo (matchType, theme, rank, suggestedBid with rangeStart/suggested/rangeEnd)
- `impactMetrics`: Aggregated clicks and orders at low/middle/high ranges
- `searchTermImpressionRank` / `searchTermImpressionShare`

---

## 11. Keyword Groups (Beta)

**US marketplace only.**

### Endpoint: `POST /sp/targeting/recommendations/keywordGroups`

Automatically identifies and continuously refreshes keyword targets based on ASINs.

```json
{
  "asins": ["PBTKGAT1", "B07QBVG5V9", "B0CJCKQT3B"]
}
```

Note: Cannot mix keyword group targets with product targets in same ad group.

---

## 12. Product & Category Targeting

### Create Target: `POST /adsApi/v1/create/targets`

### Single ASIN (exact):
```json
{
  "targets": [{
    "adGroupId": "123456789",
    "adProduct": "SPONSORED_PRODUCTS",
    "bid": { "bid": 1.50 },
    "negative": false,
    "state": "ENABLED",
    "targetDetails": {
      "productTarget": {
        "matchType": "PRODUCT_EXACT",
        "product": { "productId": "B07FKDZPZW" },
        "productIdType": "ASIN"
      }
    },
    "targetType": "PRODUCT"
  }]
}
```

### ASIN + Similar (expanded): Use `"matchType": "PRODUCT_SIMILAR"`

### Category (no refinements):
```json
{
  "targetDetails": {
    "productCategoryTarget": {
      "productCategoryRefinement": {
        "productCategoryRefinement": {
          "productCategoryId": "875875875"
        }
      }
    }
  },
  "targetType": "PRODUCT"
}
```

### Category with refinements (brand + rating):
```json
{
  "productCategoryRefinement": {
    "productBrandId": "8754674674",
    "productCategoryId": "34523452345",
    "productRatingGreaterThan": 3,
    "productRatingLessThan": 4.5
  }
}
```

---

## 13. Product Targeting Recommendations

### Endpoint: `POST /sp/targets/products/recommendations`

### By ASIN (Accept header: `application/vnd.spproductrecommendationresponse.asins.v3+json`):
Returns list of recommended ASINs with themes.

### By Theme (Accept header: `application/vnd.spproductrecommendationresponse.themes.v3+json`):
Returns themes (e.g., "Similar items", "Complements") each with recommended ASINs.

Supports pagination via `nextCursor` / `previousCursor`.

---

## 14. Category Suggestions & Refinements

### Get all categories: `GET /sp/targets/categories`
Returns full category tree.

### Get suggested categories: `POST /sp/targets/categories/recommendations`
Input ASINs, returns related categories with min/max product counts.

### Get refinements: `GET /sp/targets/category/{categoryId}/refinements`
Returns available brands, age ranges, and genres for a category.

### Count products: `POST /sp/targets/products/count`
Calculate available products for a category + refinements.

---

## 15. Auto Targeting

Auto targeting expressions are created automatically. You can set different bids per expression type.

### Expression Types:
- KEYWORDS_CLOSE_MATCH
- KEYWORDS_LOOSE_MATCH
- PRODUCT_SUBSTITUTES
- PRODUCT_COMPLEMENTS

### Get target IDs: `POST /adsApi/v1/query/targets` (filter by adGroupId)
### Get bid recommendations: `POST /sp/targets/bid/recommendations`
### Update bids: `PUT /adsApi/v1/update/targets`

---

## 16. Negative Keyword Targeting

### Campaign Level: `POST /adsApi/v1/create/targets`
Set `campaignId` + `negative: true` + `targetType: "KEYWORD"`
Response includes `targetLevel: "CAMPAIGN"`

### Ad Group Level:
Set `adGroupId` + `negative: true` + `targetType: "KEYWORD"`
Response includes `targetLevel: "AD_GROUP"`

---

## 17. Negative Product/Brand Targeting

### ASIN at Ad Group Level:
```json
{
  "adGroupId": "123456789",
  "negative": true,
  "targetDetails": {
    "productTarget": {
      "matchType": "PRODUCT_EXACT",
      "product": { "productId": "B037450938" },
      "productIdType": "ASIN"
    }
  },
  "targetType": "PRODUCT"
}
```

### Brand at Campaign Level:
```json
{
  "campaignId": "987654321",
  "negative": true,
  "targetDetails": {
    "productCategoryTarget": {
      "productCategoryRefinement": {
        "productCategoryRefinement": {
          "productBrandId": "5474567457",
          "productCategoryId": "23453245"
        }
      }
    }
  },
  "targetType": "PRODUCT_CATEGORY"
}
```

**Note:** Campaign-level negative product targeting for manual campaigns is vendors only. Sellers can add campaign-level negative targeting to auto campaigns only.

---

## 18. Budget Recommendations

### Endpoint: `POST /sp/campaigns/budgetRecommendations`

Returns:
- **suggestedBudget:** Estimated daily budget for full 24-hour coverage
- **percentTimeInBudget:** Share of time campaign was in budget (past 7 days)
- **estimatedMissedImpressions/Clicks/Sales:** Lost opportunities (lower/upper range)
- **budgetRuleRecommendation:** Suggested increase % if budget rule exists

Wait 9 days after campaign activation before using.

---

## 19. Theme-Based Bid Suggestions

### Endpoint: `POST /sp/targets/bid/recommendations`

Provides bid suggestions with impact metrics (weekly clicks and purchase orders).

### Supports:
- Automatic targeting (no minimum match types)
- Keyword targeting (minimum 5 keywords per ad group)

### Response includes:
- 3 suggested bids per targeting expression (low/median/high)
- Impact metrics aggregated at ad group level
- Theme: CONVERSION_OPPORTUNITIES

### Impact Metrics Caveat:
- Based on historic performance of similar products
- NOT estimates of expected performance
- Computed assuming campaign does not run out of budget

---
*Document version: 1.0 | Created: 13 April 2026*
