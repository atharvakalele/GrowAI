# Sponsored Display - Campaign Management OFFICIAL Documentation
**Source:** Official Amazon Advertising documentation (manually copied by Msir)
**Date Captured:** 13 April 2026
**API Version:** Sponsored Display v1
**Our Endpoint:** advertising-api-eu.amazon.com
**Our Profile ID:** 42634532240933
**Part of:** Part 3 API documentation batch

---

## Table of Contents
1. [SD Overview](#1-sd-overview)
2. [Targeting Types](#2-targeting-types)
3. [Targetable Entities Search API](#3-targetable-entities-search-api)
4. [Audiences](#4-audiences)
5. [Contextual Targeting](#5-contextual-targeting)
6. [Entertainment Targeting](#6-entertainment-targeting)
7. [Dynamic Segments](#7-dynamic-segments)
8. [Recommendations](#8-recommendations)
9. [Brand Safety](#9-brand-safety)
10. [Creatives](#10-creatives)
11. [Businesses Not Selling on Amazon (Beta)](#11-businesses-not-selling-on-amazon)
12. [Location Targeting](#12-location-targeting)

---

## 1. SD Overview

Sponsored Display enables advertisers to reach audiences throughout shopping and entertainment journeys. Supports on-Amazon and off-Amazon placement.

### Campaign API:
| Operation | Endpoint |
|-----------|----------|
| Create | POST /sd/campaigns |
| List | GET /sd/campaigns |
| Update | PUT /sd/campaigns |
| Delete | DELETE /sd/campaigns/{campaignId} |

### Ad Group targeting settings:
- **T00020:** Contextual targeting
- **T00030:** Audience targeting

### Goal Types:
| Goal | KPI |
|------|-----|
| AWARENESS | reach |
| CONSIDERATION | clicks |
| CONVERSIONS | conversions |

### Cost Types: CPC, VCPM

---

## 2. Targeting Types

| Type | API Target Type | Description |
|------|----------------|-------------|
| Contextual targeting | PRODUCT_CATEGORY | Target by product categories on detail pages |
| Audience targeting | AUDIENCE | Amazon audience segments |
| View/purchase remarketing | PRODUCT_CATEGORY_AUDIENCE | Shoppers who viewed/purchased similar products |
| Entertainment targeting | CONTENT_CATEGORY | Reach audiences during entertainment (Movies, TV, etc.) |

---

## 3. Targetable Entities Search API

### Endpoint: `POST /targetableEntities/list`

Semantic search with spelling correction and prefix completion.

### Request Parameters:
```json
{
  "adProduct": "SPONSORED_DISPLAY",
  "searchQueryFilter": "auto care",
  "targetTypeFilter": ["PRODUCT_CATEGORY", "PRODUCT_CATEGORY_AUDIENCE", "AUDIENCE", "CONTENT_CATEGORY"],
  "pathsFilter": [
    ["Audience Category"],
    ["Product Category"],
    ["Product Category Audience"],
    ["Content Category"]
  ],
  "maxResults": 2
}
```

### Response:
```json
{
  "targetableEntities": [
    {
      "path": ["Product Category", "Automotive", "Car Care"],
      "targetType": "PRODUCT_CATEGORY",
      "id": "15718271",
      "resolved": "Car Care"
    },
    {
      "path": ["Audience Category", "In-market", "Vehicles & Automotive", ...],
      "targetType": "AUDIENCE",
      "id": "403097064506351917",
      "resolved": "IM - Automotive Exterior Care"
    }
  ],
  "nextToken": "...",
  "totalResults": 5
}
```

### Notes:
- Empty pathsFilter returns curated list (excludes in-market audiences for SD)
- Pagination via nextToken

### Discover Entity Paths: `POST /targetableEntities/paths/list`
Get all entity paths or browse children of a specific path.

---

## 4. Audiences

Access Amazon's audience segments catalog. Created via targeting on ad groups.

### SD Targeting Operations:
| Operation | Endpoint |
|-----------|----------|
| Create | POST /sd/targets |
| List | GET /sd/targets |
| Extended list | GET /sd/targets/extended |
| Update | PUT /sd/targets |
| Delete | DELETE /sd/targets/{targetId} |

### Negative Targeting:
| Operation | Endpoint |
|-----------|----------|
| Create | POST /sd/negativeTargets |
| List | GET /sd/negativeTargets |
| Extended list | GET /sd/negativeTargets/extended |
| Update | PUT /sd/negativeTargets |
| Delete | DELETE /sd/negativeTargets/{targetId} |

---

## 5. Contextual Targeting

Target by product categories on relevant product detail pages.

Expression types: `asinCategorySameAs`, `asinBrandSameAs`, `asinSameAs`, etc.

---

## 6. Entertainment Targeting

Target via CONTENT_CATEGORY type. Reach audiences during entertainment journeys (Movies & TV, etc.).

---

## 7. Dynamic Segments

Based on view-to-purchase data - shoppers viewing or purchasing products likely to buy advertised product.

---

## 8. Recommendations

API provides targeting and bid recommendations for SD campaigns.

---

## 9. Brand Safety

Brand safety controls available for SD campaigns.

---

## 10. Creatives

### SD Creative Types:
- Product ads (PRODUCT_AD)
- Image ads (IMAGE)
- Video ads (VIDEO)

### Creative Elements:
- Brand logo with cropping coordinates
- Custom images (square, horizontal, vertical)
- Videos
- Headlines
- Landing page configuration

### SD Ad Operations:
| Operation | Endpoint |
|-----------|----------|
| Product Ads | POST /sd/productAds |
| Creatives | /sd/creatives |

### Image Requirements:
- Square custom image: minimum 628x628px
- File size: max 5MB
- Cropping must not exceed original image dimensions

---

## 11. Businesses Not Selling on Amazon (Beta)

### US marketplace only. For advertisers who don't sell in the Amazon store.

### Onboarding Flow:
1. Join Amazon Ads Partner Network
2. Create manager account
3. Complete API onboarding (LWA application)
4. Authorize LwA application
5. Accept Ads Agreement (termsTokens API)
6. Register Ads account

### Account Registration:
**Single:** `POST /adsAccounts`
**Bulk:** `POST /adsAccounts/batch`

### Campaign Creation Steps:
1. Create campaign (same SD API)
2. Create ad groups with bidOptimization and creativeType
3. (Optional) Add locations
4. Add targeting
5. Create product ads
6. Add creative assets
7. (Optional) Pre-moderation check
8. Moderation status check

### bidOptimization Options:
- clicks (CONSIDERATION)
- conversions (CONVERSIONS)
- reach (AWARENESS)

### creativeType: IMAGE

### Moderation Check:
- Ad landing page: `/moderation/landingPage/{landingPageUrl}`
- Ad creative: `/moderation?id={creativeId}` or `?adGroupId={adGroupId}`
- Status values: approved, rejected (with reason)

---

## 12. Location Targeting

**Only for advertisers that don't sell on Amazon.**

### Explore Locations: `POST /locations/list`

Filter by:
- name (text search, e.g., "New Yor")
- category: STATE, POSTAL_CODE, CITY, DMA

### Add to Ad Group: `POST /sd/locations`
```json
[{
  "adGroupId": 413803530857698,
  "expressionType": "manual",
  "state": "enabled",
  "expression": [{
    "type": "location",
    "value": "amzn1.ad-geo.GP-US-10005"
  }]
}]
```

### Retrieve: `GET /sd/locations?campaignIdFilter=123` or `?adGroupIdFilter=456`
### Delete: Standard SD location deletion endpoints

---
*Document version: 1.0 | Created: 13 April 2026*
