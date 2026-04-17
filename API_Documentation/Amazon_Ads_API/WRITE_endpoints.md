# Amazon Advertising API - WRITE Endpoints Reference v1.0
# ======================================================
# Account: Made in Heavens (GoAmrita Bhandar)
# Marketplace: Amazon.in (India) - EU Region
# Base URL: https://advertising-api-eu.amazon.com
# Profile ID: 42634532240933
# API Version: Ads API v1 Unified + Reporting API v3
# Created: 13 April 2026
# ======================================================
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: ALL ENDPOINTS IN THIS FILE MODIFY LIVE AD DATA
# CHANGES ARE IMMEDIATE AND AFFECT REAL AD SPEND
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

---

## Common Headers (Required for ALL Endpoints)

```
Authorization: Bearer {access_token}
Amazon-Advertising-API-ClientId: {client_id}
Amazon-Advertising-API-Scope: {profile_id}
```

Each endpoint has specific Content-Type and Accept headers documented below.

---

# SECTION 1: CAMPAIGNS
========================

## 1.1 Create Campaign

Creates one or more new Sponsored Products campaigns.

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /sp/campaigns` |
| **HTTP Method** | POST |
| **Content-Type** | `application/vnd.spCampaign.v3+json` |
| **Accept** | `application/vnd.spCampaign.v3+json` |
| **DANGER LEVEL** | **HIGH** |

### NEEDS APPROVAL BEFORE TESTING

**Headers:**
```
Content-Type: application/vnd.spCampaign.v3+json
Accept: application/vnd.spCampaign.v3+json
Authorization: Bearer {access_token}
Amazon-Advertising-API-ClientId: {client_id}
Amazon-Advertising-API-Scope: {profile_id}
```

**Request Body (create single campaign):**
```json
{
  "campaigns": [
    {
      "name": "GoAmrita_TestCampaign_API_v1",
      "state": "PAUSED",
      "targetingType": "MANUAL",
      "startDate": "2026-04-15",
      "budget": {
        "budgetType": "DAILY",
        "budget": 100.0
      },
      "dynamicBidding": {
        "strategy": "AUTO_FOR_SALES",
        "placementBidding": [
          { "placement": "PLACEMENT_TOP", "percentage": 25 },
          { "placement": "PLACEMENT_PRODUCT_PAGE", "percentage": 0 }
        ]
      }
    }
  ]
}
```

**Request Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Campaign name (must be unique) |
| state | string | Yes | ENABLED or PAUSED (use PAUSED for safety!) |
| targetingType | string | Yes | MANUAL or AUTO |
| startDate | string | Yes | YYYY-MM-DD (today or future) |
| endDate | string | No | YYYY-MM-DD (null = no end date) |
| budget.budgetType | string | Yes | DAILY |
| budget.budget | number | Yes | Daily budget in INR (min: 50.0 for India) |
| dynamicBidding.strategy | string | Yes | AUTO_FOR_SALES, LEGACY_FOR_SALES, MANUAL |
| dynamicBidding.placementBidding | array | No | Placement bid adjustments (0-900%) |

**Response (207 Multi-Status):**
```json
{
  "campaigns": {
    "success": [
      {
        "campaignId": "123456789",
        "index": 0,
        "campaign": { ... }
      }
    ],
    "error": []
  }
}
```

**What It Changes:** Creates a NEW campaign in your account. If state is ENABLED, it starts spending immediately.

**What Could Go Wrong:**
- Setting state to ENABLED instead of PAUSED = immediate spending
- Budget too high = overspend
- Wrong targetingType = wrong campaign behavior
- Duplicate name = API error (campaign names must be unique)
- Missing budget = API error
- startDate in the past = API error

**SAFETY TIP:** Always create with `"state": "PAUSED"` first, verify in Amazon Console, then enable.

---

## 1.2 Update Campaign

Updates existing campaign properties (state, budget, bidding strategy, name, dates).

| Field | Value |
|-------|-------|
| **Endpoint** | `PUT /sp/campaigns` |
| **HTTP Method** | PUT |
| **Content-Type** | `application/vnd.spCampaign.v3+json` |
| **Accept** | `application/vnd.spCampaign.v3+json` |
| **DANGER LEVEL** | **HIGH** (budget/state changes) |

### NEEDS APPROVAL BEFORE TESTING

**Headers:**
```
Content-Type: application/vnd.spCampaign.v3+json
Accept: application/vnd.spCampaign.v3+json
Authorization: Bearer {access_token}
Amazon-Advertising-API-ClientId: {client_id}
Amazon-Advertising-API-Scope: {profile_id}
```

**Request Body (update budget):**
```json
{
  "campaigns": [
    {
      "campaignId": "302164316622266",
      "budget": {
        "budgetType": "DAILY",
        "budget": 300.0
      }
    }
  ]
}
```

**Request Body (pause campaign):**
```json
{
  "campaigns": [
    {
      "campaignId": "302164316622266",
      "state": "PAUSED"
    }
  ]
}
```

**Request Body (change bidding strategy):**
```json
{
  "campaigns": [
    {
      "campaignId": "302164316622266",
      "dynamicBidding": {
        "strategy": "LEGACY_FOR_SALES",
        "placementBidding": [
          { "placement": "PLACEMENT_TOP", "percentage": 50 }
        ]
      }
    }
  ]
}
```

**Request Body (enable campaign):**
```json
{
  "campaigns": [
    {
      "campaignId": "302164316622266",
      "state": "ENABLED"
    }
  ]
}
```

**Updatable Fields:**
| Field | DANGER | Description |
|-------|--------|-------------|
| state | HIGH | ENABLED = spending, PAUSED = stopped, ARCHIVED = permanent |
| budget.budget | HIGH | Changes daily spend limit immediately |
| name | LOW | Rename campaign |
| dynamicBidding.strategy | MEDIUM | Changes how bids adjust |
| dynamicBidding.placementBidding | MEDIUM | Adjusts placement bid percentages |
| endDate | LOW | Set or change end date |

**Response (207 Multi-Status):**
```json
{
  "campaigns": {
    "success": [
      {
        "campaignId": "302164316622266",
        "index": 0,
        "campaign": { ... }
      }
    ],
    "error": []
  }
}
```

**What It Changes:** Modifies campaign properties in real-time. Budget and state changes take effect immediately.

**What Could Go Wrong:**
- Setting state to ARCHIVED = **PERMANENT, IRREVERSIBLE** (campaign cannot be re-enabled)
- Increasing budget too much = overspend
- Reducing budget too much = lost impressions/sales
- Wrong bidding strategy = unexpected bid behavior
- Enabling a poorly configured campaign = wasted spend

**CRITICAL WARNING:** `ARCHIVED` state is PERMANENT. You CANNOT re-enable an archived campaign. Only use for campaigns you truly want to permanently stop.

---

## 1.3 Delete Campaign (Archive)

There is no true "delete" in Amazon Ads. Deleting = setting state to ARCHIVED (permanent).

| Field | Value |
|-------|-------|
| **Endpoint** | `DELETE /sp/campaigns` |
| **HTTP Method** | DELETE |
| **Content-Type** | `application/vnd.spCampaign.v3+json` |
| **Accept** | `application/vnd.spCampaign.v3+json` |
| **DANGER LEVEL** | **CRITICAL** |

### NEEDS APPROVAL BEFORE TESTING

**Request Body:**
```json
{
  "campaignIdFilter": {
    "include": ["302164316622266"]
  }
}
```

**What Could Go Wrong:** IRREVERSIBLE. Campaign and all child entities (ad groups, keywords, ads) are permanently archived.

---

# SECTION 2: AD GROUPS
========================

## 2.1 Create Ad Group

Creates one or more ad groups within a campaign.

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /sp/adGroups` |
| **HTTP Method** | POST |
| **Content-Type** | `application/vnd.spAdGroup.v3+json` |
| **Accept** | `application/vnd.spAdGroup.v3+json` |
| **DANGER LEVEL** | **MEDIUM** |

### NEEDS APPROVAL BEFORE TESTING

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
  "adGroups": [
    {
      "campaignId": "302164316622266",
      "name": "AdGroup_Libidex_Exact_API_v1",
      "state": "PAUSED",
      "defaultBid": 5.0
    }
  ]
}
```

**Request Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaignId | string | Yes | Parent campaign ID |
| name | string | Yes | Ad group name |
| state | string | Yes | ENABLED or PAUSED |
| defaultBid | number | Yes | Default bid in INR (min: 1.0 for India) |

**Response (207 Multi-Status):**
```json
{
  "adGroups": {
    "success": [
      {
        "adGroupId": "987654321",
        "index": 0,
        "adGroup": { ... }
      }
    ],
    "error": []
  }
}
```

**What It Changes:** Creates new ad group structure inside a campaign.

**What Could Go Wrong:**
- defaultBid too high = expensive clicks if campaign is enabled
- Creating in wrong campaign = organizational mess
- State ENABLED in an enabled campaign = immediate spending once keywords/ads added

---

## 2.2 Update Ad Group

Update ad group properties (default bid, state, name).

| Field | Value |
|-------|-------|
| **Endpoint** | `PUT /sp/adGroups` |
| **HTTP Method** | PUT |
| **Content-Type** | `application/vnd.spAdGroup.v3+json` |
| **Accept** | `application/vnd.spAdGroup.v3+json` |
| **DANGER LEVEL** | **MEDIUM** |

### NEEDS APPROVAL BEFORE TESTING

**Request Body (update default bid):**
```json
{
  "adGroups": [
    {
      "adGroupId": "448483975362602",
      "defaultBid": 3.5
    }
  ]
}
```

**Request Body (pause ad group):**
```json
{
  "adGroups": [
    {
      "adGroupId": "448483975362602",
      "state": "PAUSED"
    }
  ]
}
```

**Updatable Fields:**
| Field | DANGER | Description |
|-------|--------|-------------|
| state | MEDIUM | ENABLED/PAUSED/ARCHIVED (archived = permanent) |
| defaultBid | MEDIUM | Changes bid for all keywords without custom bids |
| name | LOW | Rename ad group |

**What Could Go Wrong:**
- Increasing defaultBid = higher CPC for all keywords using default bid
- Archiving ad group = permanent, affects all keywords and ads in it

---

## 2.3 Delete Ad Group (Archive)

| Field | Value |
|-------|-------|
| **Endpoint** | `DELETE /sp/adGroups` |
| **HTTP Method** | DELETE |
| **Content-Type** | `application/vnd.spAdGroup.v3+json` |
| **Accept** | `application/vnd.spAdGroup.v3+json` |
| **DANGER LEVEL** | **HIGH** |

### NEEDS APPROVAL BEFORE TESTING

**Request Body:**
```json
{
  "adGroupIdFilter": {
    "include": ["448483975362602"]
  }
}
```

**IRREVERSIBLE.** Archives ad group and all child keywords and product ads.

---

# SECTION 3: KEYWORDS (POSITIVE)
==================================

## 3.1 Create Keywords

Add positive keywords to an ad group (these trigger your ads).

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /sp/keywords` |
| **HTTP Method** | POST |
| **Content-Type** | `application/vnd.spKeyword.v3+json` |
| **Accept** | `application/vnd.spKeyword.v3+json` |
| **DANGER LEVEL** | **MEDIUM** |

### NEEDS APPROVAL BEFORE TESTING

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
  "keywords": [
    {
      "campaignId": "302164316622266",
      "adGroupId": "448483975362602",
      "keywordText": "libidex capsule for men",
      "matchType": "EXACT",
      "bid": 5.0,
      "state": "ENABLED"
    },
    {
      "campaignId": "302164316622266",
      "adGroupId": "448483975362602",
      "keywordText": "libidex capsule",
      "matchType": "PHRASE",
      "bid": 3.5,
      "state": "ENABLED"
    },
    {
      "campaignId": "302164316622266",
      "adGroupId": "448483975362602",
      "keywordText": "sexual wellness capsule for men",
      "matchType": "BROAD",
      "bid": 2.5,
      "state": "ENABLED"
    }
  ]
}
```

**Request Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaignId | string | Yes | Parent campaign ID (must be MANUAL targeting) |
| adGroupId | string | Yes | Parent ad group ID |
| keywordText | string | Yes | The keyword text (max 80 chars, 10 words) |
| matchType | string | Yes | EXACT, PHRASE, or BROAD |
| bid | number | No | Custom bid in INR (uses ad group default if omitted) |
| state | string | Yes | ENABLED or PAUSED |

**Limits:**
- Max 1000 keywords per ad group
- Max 10,000 keywords per campaign
- Max keywords per request: 1000

**Response (207 Multi-Status):**
```json
{
  "keywords": {
    "success": [
      {
        "keywordId": "111222333",
        "index": 0,
        "keyword": { ... }
      }
    ],
    "error": [
      {
        "index": 2,
        "errors": [
          {
            "errorType": "DUPLICATE_VALUE",
            "message": "Keyword already exists"
          }
        ]
      }
    ]
  }
}
```

**What It Changes:** Adds new keyword targets to your ad group. If campaign and ad group are both ENABLED, these keywords start matching searches immediately.

**What Could Go Wrong:**
- Bid too high = expensive clicks
- Wrong match type = wrong traffic (BROAD can match very loosely)
- Adding to wrong ad group = targeting wrong products
- Adding to enabled campaign = immediate spend
- Duplicate keywords = API error (not harmful but wastes request)

---

## 3.2 Update Keywords

Update keyword bids and state.

| Field | Value |
|-------|-------|
| **Endpoint** | `PUT /sp/keywords` |
| **HTTP Method** | PUT |
| **Content-Type** | `application/vnd.spKeyword.v3+json` |
| **Accept** | `application/vnd.spKeyword.v3+json` |
| **DANGER LEVEL** | **MEDIUM** |

### NEEDS APPROVAL BEFORE TESTING

**Request Body (update bid):**
```json
{
  "keywords": [
    {
      "keywordId": "175803581922075",
      "bid": 7.5
    }
  ]
}
```

**Request Body (pause keyword):**
```json
{
  "keywords": [
    {
      "keywordId": "175803581922075",
      "state": "PAUSED"
    }
  ]
}
```

**Request Body (batch update multiple keywords):**
```json
{
  "keywords": [
    { "keywordId": "175803581922075", "bid": 7.5 },
    { "keywordId": "196725621027619", "bid": 4.0 },
    { "keywordId": "280488490567670", "state": "PAUSED" }
  ]
}
```

**Updatable Fields:**
| Field | DANGER | Description |
|-------|--------|-------------|
| bid | MEDIUM | Changes cost per click for this keyword |
| state | MEDIUM | ENABLED/PAUSED/ARCHIVED |

**What Could Go Wrong:**
- Increasing bid too much = expensive clicks
- Archiving keyword = permanent (cannot re-enable)
- Pausing a high-converting keyword = lost sales

**NOTE:** You CANNOT change keywordText or matchType. To change these, archive the old keyword and create a new one.

---

## 3.3 Delete Keywords (Archive)

| Field | Value |
|-------|-------|
| **Endpoint** | `DELETE /sp/keywords` |
| **HTTP Method** | DELETE |
| **Content-Type** | `application/vnd.spKeyword.v3+json` |
| **Accept** | `application/vnd.spKeyword.v3+json` |
| **DANGER LEVEL** | **HIGH** |

### NEEDS APPROVAL BEFORE TESTING

**Request Body:**
```json
{
  "keywordIdFilter": {
    "include": ["175803581922075", "196725621027619"]
  }
}
```

**IRREVERSIBLE.** Archives keywords permanently. Historical data preserved but keyword cannot be re-enabled.

---

# SECTION 4: NEGATIVE KEYWORDS
================================

## 4.1 Create Negative Keywords (Ad Group Level)

Adds negative keywords to block unwanted search terms from triggering ads.

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /sp/negativeKeywords` |
| **HTTP Method** | POST |
| **Content-Type** | `application/vnd.spNegativeKeyword.v3+json` |
| **Accept** | `application/vnd.spNegativeKeyword.v3+json` |
| **DANGER LEVEL** | **LOW** (blocks ads, doesn't spend money) |

### NEEDS APPROVAL BEFORE TESTING

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
  "negativeKeywords": [
    {
      "campaignId": "429878877190326",
      "adGroupId": "297574255948083",
      "keywordText": "weight gain capsule",
      "matchType": "NEGATIVE_EXACT",
      "state": "ENABLED"
    },
    {
      "campaignId": "429878877190326",
      "adGroupId": "297574255948083",
      "keywordText": "horse power",
      "matchType": "NEGATIVE_PHRASE",
      "state": "ENABLED"
    }
  ]
}
```

**Request Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaignId | string | Yes | Campaign ID |
| adGroupId | string | Yes | Ad group ID |
| keywordText | string | Yes | Search term to block |
| matchType | string | Yes | NEGATIVE_EXACT or NEGATIVE_PHRASE |
| state | string | Yes | ENABLED |

**Response (207 Multi-Status):**
```json
{
  "negativeKeywords": {
    "success": [
      {
        "keywordId": "444555666",
        "index": 0,
        "negativeKeyword": { ... }
      }
    ],
    "error": []
  }
}
```

**What It Changes:** Blocks matching search terms from triggering ads in this ad group. SAVES money by preventing irrelevant clicks.

**What Could Go Wrong:**
- Blocking a high-converting search term = lost sales
- Using NEGATIVE_PHRASE too aggressively = blocking too many searches
- Adding wrong negative = blocking profitable traffic

**SAFETY NOTE:** This is one of the SAFEST write operations. Negative keywords only prevent spending, they don't cause spending.

---

## 4.2 Create Campaign-Level Negative Keywords

Negative keywords that apply to ALL ad groups in a campaign.

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /sp/campaignNegativeKeywords` |
| **HTTP Method** | POST |
| **Content-Type** | `application/vnd.spCampaignNegativeKeyword.v3+json` |
| **Accept** | `application/vnd.spCampaignNegativeKeyword.v3+json` |
| **DANGER LEVEL** | **LOW** |

### NEEDS APPROVAL BEFORE TESTING

**Request Body:**
```json
{
  "campaignNegativeKeywords": [
    {
      "campaignId": "429878877190326",
      "keywordText": "wholesale",
      "matchType": "NEGATIVE_PHRASE",
      "state": "ENABLED"
    }
  ]
}
```

Same as ad group negatives but applies campaign-wide. No adGroupId needed.

---

## 4.3 Delete Negative Keywords (Archive)

| Field | Value |
|-------|-------|
| **Endpoint** | `DELETE /sp/negativeKeywords` |
| **HTTP Method** | DELETE |
| **Content-Type** | `application/vnd.spNegativeKeyword.v3+json` |
| **Accept** | `application/vnd.spNegativeKeyword.v3+json` |
| **DANGER LEVEL** | **MEDIUM** (removing a negative = more spending) |

### NEEDS APPROVAL BEFORE TESTING

**Request Body:**
```json
{
  "keywordIdFilter": {
    "include": ["93947938042907"]
  }
}
```

**What Could Go Wrong:** Removing a negative keyword means previously blocked searches will now trigger ads and spend money.

---

# SECTION 5: PRODUCT ADS
==========================

## 5.1 Create Product Ads

Associates ASINs/SKUs with an ad group.

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /sp/productAds` |
| **HTTP Method** | POST |
| **Content-Type** | `application/vnd.spProductAd.v3+json` |
| **Accept** | `application/vnd.spProductAd.v3+json` |
| **DANGER LEVEL** | **MEDIUM** |

### NEEDS APPROVAL BEFORE TESTING

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
  "productAds": [
    {
      "campaignId": "302164316622266",
      "adGroupId": "448483975362602",
      "asin": "B0DX7J5ZXT",
      "sku": "JoshBoosterLibidex30_p2",
      "state": "ENABLED"
    }
  ]
}
```

**Request Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaignId | string | Yes | Campaign ID |
| adGroupId | string | Yes | Ad group ID |
| asin | string | Conditional | Product ASIN (required for sellers) |
| sku | string | Conditional | Seller SKU (required for sellers) |
| state | string | Yes | ENABLED or PAUSED |

**Response (207 Multi-Status):**
```json
{
  "productAds": {
    "success": [
      {
        "adId": "777888999",
        "index": 0,
        "productAd": { ... }
      }
    ],
    "error": []
  }
}
```

**What It Changes:** Assigns a product to be advertised within an ad group. If the campaign/ad group are enabled, this product starts appearing in ads.

**What Could Go Wrong:**
- Adding wrong ASIN = advertising wrong product
- ASIN not in your catalog = API error
- Adding to wrong ad group = wrong keywords targeting this product

---

## 5.2 Update Product Ads

Update product ad state.

| Field | Value |
|-------|-------|
| **Endpoint** | `PUT /sp/productAds` |
| **HTTP Method** | PUT |
| **Content-Type** | `application/vnd.spProductAd.v3+json` |
| **Accept** | `application/vnd.spProductAd.v3+json` |
| **DANGER LEVEL** | **LOW** |

### NEEDS APPROVAL BEFORE TESTING

**Request Body (pause product ad):**
```json
{
  "productAds": [
    {
      "adId": "344613073990305",
      "state": "PAUSED"
    }
  ]
}
```

**Updatable Fields:**
| Field | DANGER | Description |
|-------|--------|-------------|
| state | LOW | ENABLED/PAUSED/ARCHIVED |

**NOTE:** You CANNOT change the ASIN or SKU. To change, archive old ad and create new one.

---

## 5.3 Delete Product Ads (Archive)

| Field | Value |
|-------|-------|
| **Endpoint** | `DELETE /sp/productAds` |
| **HTTP Method** | DELETE |
| **Content-Type** | `application/vnd.spProductAd.v3+json` |
| **Accept** | `application/vnd.spProductAd.v3+json` |
| **DANGER LEVEL** | **MEDIUM** |

### NEEDS APPROVAL BEFORE TESTING

**Request Body:**
```json
{
  "adIdFilter": {
    "include": ["344613073990305"]
  }
}
```

---

# SECTION 6: PRODUCT TARGETS (ASIN/Category Targeting)
========================================================

## 6.1 Create Product Targets

Create ASIN or category targeting expressions.

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /sp/targets` |
| **HTTP Method** | POST |
| **Content-Type** | `application/vnd.spTargetingClause.v3+json` |
| **Accept** | `application/vnd.spTargetingClause.v3+json` |
| **DANGER LEVEL** | **MEDIUM** |

### NEEDS APPROVAL BEFORE TESTING

**Headers:**
```
Content-Type: application/vnd.spTargetingClause.v3+json
Accept: application/vnd.spTargetingClause.v3+json
Authorization: Bearer {access_token}
Amazon-Advertising-API-ClientId: {client_id}
Amazon-Advertising-API-Scope: {profile_id}
```

**Request Body (target specific ASINs):**
```json
{
  "targetingClauses": [
    {
      "campaignId": "302164316622266",
      "adGroupId": "448483975362602",
      "expressionType": "MANUAL",
      "expression": [
        { "type": "asinSameAs", "value": "B0ABC12345" }
      ],
      "bid": 5.0,
      "state": "ENABLED"
    }
  ]
}
```

**Request Body (target a category):**
```json
{
  "targetingClauses": [
    {
      "campaignId": "302164316622266",
      "adGroupId": "448483975362602",
      "expressionType": "MANUAL",
      "expression": [
        { "type": "asinCategorySameAs", "value": "12345678" }
      ],
      "bid": 3.0,
      "state": "ENABLED"
    }
  ]
}
```

**Request Body (target a category with refinements):**
```json
{
  "targetingClauses": [
    {
      "campaignId": "302164316622266",
      "adGroupId": "448483975362602",
      "expressionType": "MANUAL",
      "expression": [
        { "type": "asinCategorySameAs", "value": "12345678" },
        { "type": "asinPriceBetween", "value": "100-500" },
        { "type": "asinReviewRatingGreaterThan", "value": "3.5" }
      ],
      "bid": 3.0,
      "state": "ENABLED"
    }
  ]
}
```

---

## 6.2 Update Product Targets

| Field | Value |
|-------|-------|
| **Endpoint** | `PUT /sp/targets` |
| **HTTP Method** | PUT |
| **Content-Type** | `application/vnd.spTargetingClause.v3+json` |
| **Accept** | `application/vnd.spTargetingClause.v3+json` |
| **DANGER LEVEL** | **MEDIUM** |

### NEEDS APPROVAL BEFORE TESTING

**Request Body:**
```json
{
  "targetingClauses": [
    {
      "targetId": "123456789",
      "bid": 4.5,
      "state": "ENABLED"
    }
  ]
}
```

---

## 6.3 Create Negative Product Targets

Block specific ASINs or categories from targeting.

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /sp/negativeTargets` |
| **HTTP Method** | POST |
| **Content-Type** | `application/vnd.spNegativeTargetingClause.v3+json` |
| **Accept** | `application/vnd.spNegativeTargetingClause.v3+json` |
| **DANGER LEVEL** | **LOW** |

### NEEDS APPROVAL BEFORE TESTING

**Request Body:**
```json
{
  "negativeTargetingClauses": [
    {
      "campaignId": "302164316622266",
      "adGroupId": "448483975362602",
      "expressionType": "MANUAL",
      "expression": [
        { "type": "asinSameAs", "value": "B0COMPETITOR1" }
      ],
      "state": "ENABLED"
    }
  ]
}
```

---

## 6.4 Delete Negative Product Targets

| Field | Value |
|-------|-------|
| **Endpoint** | `DELETE /sp/negativeTargets` |
| **HTTP Method** | DELETE |
| **Content-Type** | `application/vnd.spNegativeTargetingClause.v3+json` |
| **Accept** | `application/vnd.spNegativeTargetingClause.v3+json` |
| **DANGER LEVEL** | **MEDIUM** |

### NEEDS APPROVAL BEFORE TESTING

---

# SECTION 7: BUDGET RULES
===========================

## 7.1 Create Budget Rule

Set automatic budget increases based on schedule or performance.

| Field | Value |
|-------|-------|
| **Endpoint** | `POST /sp/campaigns/{campaignId}/budgetRules` |
| **HTTP Method** | POST |
| **Content-Type** | `application/vnd.spBudgetRule.v3+json` |
| **Accept** | `application/vnd.spBudgetRule.v3+json` |
| **DANGER LEVEL** | **HIGH** |

### NEEDS APPROVAL BEFORE TESTING

**Headers:**
```
Content-Type: application/vnd.spBudgetRule.v3+json
Accept: application/vnd.spBudgetRule.v3+json
Authorization: Bearer {access_token}
Amazon-Advertising-API-ClientId: {client_id}
Amazon-Advertising-API-Scope: {profile_id}
```

**Request Body (schedule-based rule):**
```json
{
  "budgetRules": [
    {
      "ruleType": "SCHEDULE",
      "name": "Weekend Budget Increase",
      "budgetIncreaseBy": {
        "type": "PERCENT",
        "value": 50
      },
      "duration": {
        "dateRangeType": "CUSTOM",
        "startDate": "2026-04-15",
        "endDate": "2026-04-30"
      },
      "recurrence": {
        "type": "WEEKLY",
        "daysOfWeek": ["SATURDAY", "SUNDAY"]
      }
    }
  ]
}
```

**Request Body (performance-based rule):**
```json
{
  "budgetRules": [
    {
      "ruleType": "PERFORMANCE",
      "name": "Increase When ACOS Low",
      "budgetIncreaseBy": {
        "type": "PERCENT",
        "value": 30
      },
      "duration": {
        "dateRangeType": "ONGOING"
      },
      "performanceMeasureCondition": {
        "metricName": "ACOS",
        "comparisonOperator": "LESS_THAN_OR_EQUAL_TO",
        "threshold": 25.0
      }
    }
  ]
}
```

**What It Changes:** Automatically adjusts campaign budget based on schedule or performance criteria.

**What Could Go Wrong:**
- Overly aggressive budget increase = overspending
- Performance rule with wrong threshold = unexpected budget spikes
- Stacking multiple rules = compounding budget increases

---

## 7.2 List Budget Rules

| Field | Value |
|-------|-------|
| **Endpoint** | `GET /sp/campaigns/{campaignId}/budgetRules` |
| **HTTP Method** | GET |
| **Accept** | `application/vnd.spBudgetRule.v3+json` |
| **DANGER LEVEL** | **N/A (read-only)** |

---

## 7.3 Delete Budget Rule

| Field | Value |
|-------|-------|
| **Endpoint** | `DELETE /sp/campaigns/{campaignId}/budgetRules/{budgetRuleId}` |
| **HTTP Method** | DELETE |
| **DANGER LEVEL** | **LOW** |

### NEEDS APPROVAL BEFORE TESTING

---

# SECTION 8: COMPLETE CAMPAIGN CREATION WORKFLOW
=================================================

To create a fully functional campaign from scratch, you need these API calls in order:

### Step 1: Create Campaign (PAUSED)
```
POST /sp/campaigns
Content-Type: application/vnd.spCampaign.v3+json
```

### Step 2: Create Ad Group within Campaign
```
POST /sp/adGroups
Content-Type: application/vnd.spAdGroup.v3+json
```

### Step 3: Add Product Ads (ASINs) to Ad Group
```
POST /sp/productAds
Content-Type: application/vnd.spProductAd.v3+json
```

### Step 4: Add Keywords (for MANUAL campaigns) or Targets
```
POST /sp/keywords                    (keyword targeting)
POST /sp/targets                     (product targeting)
Content-Type: application/vnd.spKeyword.v3+json
```

### Step 5: (Optional) Add Negative Keywords
```
POST /sp/negativeKeywords
Content-Type: application/vnd.spNegativeKeyword.v3+json
```

### Step 6: Enable Campaign (when ready)
```
PUT /sp/campaigns
Body: { "campaigns": [{ "campaignId": "...", "state": "ENABLED" }] }
```

**IMPORTANT:** Always create campaigns in PAUSED state. Verify everything in Amazon Console before enabling.

---

# SECTION 9: BATCH OPERATIONS
===============================

All write endpoints support batch operations (multiple items in one request):

**Max Batch Sizes:**
| Entity | Max per Request |
|--------|----------------|
| Campaigns | 100 |
| Ad Groups | 100 |
| Keywords | 1000 |
| Negative Keywords | 1000 |
| Product Ads | 1000 |
| Targets | 1000 |

**Batch Response Pattern (207 Multi-Status):**
Every batch response contains `success` and `error` arrays. Always check BOTH:

```json
{
  "keywords": {
    "success": [
      { "keywordId": "111", "index": 0 }
    ],
    "error": [
      {
        "index": 1,
        "errors": [
          {
            "errorType": "DUPLICATE_VALUE",
            "message": "Keyword already exists in this ad group"
          }
        ]
      }
    ]
  }
}
```

**Common Error Types:**
| errorType | Meaning |
|-----------|---------|
| DUPLICATE_VALUE | Entity already exists |
| NOT_FOUND | Referenced entity does not exist |
| INVALID_VALUE | Field value out of range |
| MALFORMED_VALUE | Wrong data format |
| MISSING_VALUE | Required field missing |
| UNAUTHORIZED | No permission for this operation |
| THROTTLED | Rate limit hit |

---

# SECTION 10: DANGER LEVEL SUMMARY
====================================

| DANGER | Endpoints | Risk |
|--------|-----------|------|
| **CRITICAL** | DELETE campaigns, DELETE ad groups | **IRREVERSIBLE**, archives permanently |
| **HIGH** | CREATE campaigns (ENABLED), UPDATE campaign state/budget, Budget rules | Immediate spending impact |
| **MEDIUM** | CREATE/UPDATE ad groups, keywords, targets, product ads | Spending impact if parent enabled |
| **LOW** | CREATE negative keywords, UPDATE product ad state, DELETE negatives | Prevents spending / minimal impact |

---

# SECTION 11: SAFETY CHECKLIST BEFORE ANY WRITE OPERATION
===========================================================

Before executing ANY write endpoint:

- [ ] Confirm correct campaignId / adGroupId / keywordId
- [ ] Double-check the entity you're modifying (read it first with list endpoint)
- [ ] If creating: use state: PAUSED first
- [ ] If updating budget: know current budget (compare old vs new)
- [ ] If changing state to ARCHIVED: understand this is PERMANENT
- [ ] If changing state to ENABLED: verify campaign structure is correct
- [ ] If updating bids: know current bid and market range
- [ ] Have Msir's approval for any live changes
- [ ] Test with a single item before batch operations
- [ ] Save a backup of current state (run list endpoint and save JSON)

---

# SECTION 12: WRITE ENDPOINT QUICK REFERENCE TABLE
====================================================

| Endpoint | Method | Content-Type Suffix | DANGER | Action |
|----------|--------|-------------------|--------|--------|
| /sp/campaigns | POST | spCampaign.v3+json | HIGH | Create campaigns |
| /sp/campaigns | PUT | spCampaign.v3+json | HIGH | Update campaigns |
| /sp/campaigns | DELETE | spCampaign.v3+json | CRITICAL | Archive campaigns |
| /sp/adGroups | POST | spAdGroup.v3+json | MEDIUM | Create ad groups |
| /sp/adGroups | PUT | spAdGroup.v3+json | MEDIUM | Update ad groups |
| /sp/adGroups | DELETE | spAdGroup.v3+json | HIGH | Archive ad groups |
| /sp/keywords | POST | spKeyword.v3+json | MEDIUM | Create keywords |
| /sp/keywords | PUT | spKeyword.v3+json | MEDIUM | Update keyword bids/state |
| /sp/keywords | DELETE | spKeyword.v3+json | HIGH | Archive keywords |
| /sp/negativeKeywords | POST | spNegativeKeyword.v3+json | LOW | Create negative keywords |
| /sp/negativeKeywords | DELETE | spNegativeKeyword.v3+json | MEDIUM | Remove negative keywords |
| /sp/campaignNegativeKeywords | POST | spCampaignNegativeKeyword.v3+json | LOW | Create campaign negatives |
| /sp/campaignNegativeKeywords | DELETE | spCampaignNegativeKeyword.v3+json | MEDIUM | Remove campaign negatives |
| /sp/productAds | POST | spProductAd.v3+json | MEDIUM | Create product ads |
| /sp/productAds | PUT | spProductAd.v3+json | LOW | Update product ad state |
| /sp/productAds | DELETE | spProductAd.v3+json | MEDIUM | Archive product ads |
| /sp/targets | POST | spTargetingClause.v3+json | MEDIUM | Create product targets |
| /sp/targets | PUT | spTargetingClause.v3+json | MEDIUM | Update target bids/state |
| /sp/targets | DELETE | spTargetingClause.v3+json | HIGH | Archive targets |
| /sp/negativeTargets | POST | spNegativeTargetingClause.v3+json | LOW | Create negative targets |
| /sp/negativeTargets | DELETE | spNegativeTargetingClause.v3+json | MEDIUM | Remove negative targets |
| /sp/campaigns/{id}/budgetRules | POST | spBudgetRule.v3+json | HIGH | Create budget rules |
| /sp/campaigns/{id}/budgetRules/{ruleId} | DELETE | - | LOW | Delete budget rules |

---

*Document Version: 1.0 | Created: 13 April 2026*
*Based on: Amazon Ads API v1 Unified*
*ALL write endpoints marked with: NEEDS APPROVAL BEFORE TESTING*
