# Amazon Ads Campaign Management API v1 - OFFICIAL Documentation
**Source:** Official Amazon Advertising documentation (manually copied by Msir)
**Date Captured:** 12 April 2026
**API Version:** Amazon Ads API v1 (Campaign Management)
**Our Endpoint:** advertising-api-eu.amazon.com
**Our Profile ID:** 42634532240933

## Version Note:
- This file was originally labeled "Part 2 API text" but contains **Campaign Management API** docs, NOT Reporting API Part 2
- Campaign Management API v1 = unified CRUD API for all ad products
- Covers: Campaigns, Ad Groups, Ads, Targets, Ad Associations
- Supports: SP, SB, SD, ST (Sponsored TV), Amazon DSP
- API Base Path: `/adsApi/v1/`

## IMPORTANT DISCOVERY:
- **This is NOT Reporting API Part 2** - it is Campaign Management API documentation
- Reporting API Part 2 (Geo, Inventory, Placement, Purchased Product, Search Term, Targeting, Tech, Columns, FAQ) still needs to be captured separately

---

## Table of Contents
1. [Campaign Management Overview](#1-campaign-management-overview)
2. [Supported Ad Products](#2-supported-ad-products)
3. [Entity Relationship Structure](#3-entity-relationship-structure)
4. [Campaign Entity - Fields by Ad Product](#4-campaign-entity)
5. [Ad Group Entity - Fields by Ad Product](#5-ad-group-entity)
6. [Ad Entity - Fields by Ad Product](#6-ad-entity)
7. [Target Entity - Fields by Ad Product](#7-target-entity)
8. [Ad Association Entity](#8-ad-association-entity)
9. [Example Request Payloads](#9-example-request-payloads)
10. [API v1 Specification Reference](#10-api-v1-specification-reference)

---

## 1. Campaign Management Overview

The Campaign Management APIs provide CRUD operations for campaign management objects across all ad products. They are **ad product-agnostic** with the same versioning and feature naming.

### Key Points:
- Single unified API for all ad products
- Common model with ad-product-specific attributes
- At launch: calls bound to one ad product at a time
- At launch: rate limits (TPS) per ad product
- Future: multi-ad product operations in same payload

### Operations Available:
- **Create** - POST `/adsApi/v1/create/{entity}`
- **Update** - POST `/adsApi/v1/update/{entity}`
- **Query** - POST `/adsApi/v1/query/{entity}`
- **Delete** - POST `/adsApi/v1/delete/{entity}`

### Required Headers:
- `Amazon-Ads-AccountId` (required) - Advertiser Account ID
- `Amazon-Ads-ClientId` (required) - LwA client ID
- `Amazon-Advertising-API-Scope` (optional for some) - Profile ID
- `Authorization: Bearer {access_token}`

### Response Codes:
- 207: Multi-status (success + error arrays)
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 413: Content Too Large
- 429: Too Many Requests (rate limit)
- 500/502/503/504: Server errors

---

## 2. Supported Ad Products

| Ad Product | Campaign | Ad Group | Ad | Target | Ad Association |
|------------|----------|----------|-----|--------|----------------|
| Sponsored Products | Y | Y | Y | Y | - |
| Sponsored Brands | Y | Y | Y | Y | - |
| Sponsored Display | Y | Y | Y | Y | - |
| Sponsored Television | Y | - | - | - | - |
| Amazon DSP | Y | Y | Y | Y | Y |

---

## 3. Entity Relationship Structure

### Sponsored Ads (SP, SB, SD):
```
Campaign -> Ad Group -> Ad
                    -> Target
```

### Amazon DSP:
```
Campaign -> Ad Group -> Target
                    -> Ad Association -> Ad
```
Note: DSP ads are associated with ad groups via the **Ad Association** entity (not directly).

---

## 4. Campaign Entity

### Field Legend: Required/Optional/Read-only
- Required: must be provided on create
- Optional: can be provided
- Read-only: returned by API, cannot be set

### Core Campaign Fields:

| Field | SP | SB | DSP | Notes |
|-------|----|----|-----|-------|
| adProduct | Req | Req | Req | SPONSORED_PRODUCTS, SPONSORED_BRANDS, AMAZON_DSP |
| name | Req | Req | Req | Campaign name |
| state | Req | Req | Req | ENABLED, PAUSED |
| campaignId | RO | RO | RO | Auto-generated |
| marketplaceScope | Req | Req | - | SINGLE_MARKETPLACE |
| marketplaces | Opt | Opt | Opt | e.g. ["US"], ["IN"] |
| startDateTime | Req | Req | RO | ISO 8601 format |
| endDateTime | Opt | Opt | RO | |
| budgets | Req | Req | Opt | Array of Budget objects |
| costType | - | Req | - | e.g. "CPC" |
| portfolioId | Opt | Opt | - | |
| tags | Opt | Opt | Opt | Key-value pairs |
| status | RO | RO | RO | System status |
| creationDateTime | RO | RO | RO | |
| lastUpdatedDateTime | RO | RO | RO | |

### Campaign Nested Objects:

#### Budgets
| Field | SP | SB | DSP |
|-------|----|----|-----|
| budgetType | Req | Req | Req |
| budgetValue.monetaryBudgetValue | Req | Req | Req |
| recurrenceTimePeriod | Req | Req | Req |

Values: budgetType=MONETARY, recurrenceTimePeriod=DAILY/LIFETIME

#### Optimizations
| Sub-object | SP | SB | DSP |
|------------|----|----|-----|
| bidSettings | Opt | Opt | Req |
| budgetSettings | Opt | - | Opt |
| goalSettings | - | Opt | Opt |
| primaryInventoryTypes | - | - | Opt |

#### bidSettings
| Field | SP | SB | DSP |
|-------|----|----|-----|
| bidStrategy | Opt | Opt | Req |
| bidAdjustments.audienceBidAdjustments | Opt | Opt | - |
| bidAdjustments.placementBidAdjustments | Opt | Opt | - |
| bidAdjustments.shopperSegmentBidAdjustments | - | Opt | - |

#### Flights (DSP Only)
| Field | Required |
|-------|----------|
| budget.budgetType | Req |
| budget.budgetValue | Req |
| startDateTime | Req |
| endDateTime | Req |
| flightId | Opt |

#### Frequencies (DSP Only)
| Field | Required |
|-------|----------|
| eventMaxCount | Req |
| frequencyTargetingSetting | Req |
| timeCount | Req |
| timeUnit | Req |

#### Fees (DSP Only)
| Field | Required |
|-------|----------|
| feeType | Req |
| feeValue | Req |
| feeValueType | Req |

#### GoalSettings
| Field | SP | SB | DSP |
|-------|----|----|-----|
| kpi | - | Req | Req |
| kpiValue | - | - | Opt |
| goal | - | RO | RO |
| currencyCode | - | - | RO |

---

## 5. Ad Group Entity

### Core AdGroup Fields:

| Field | SP | SB | DSP | Notes |
|-------|----|----|-----|-------|
| adGroupId | RO | RO | RO | Auto-generated |
| adProduct | Req | Req | Req | |
| campaignId | Req | Req | Req | Parent campaign |
| name | Req | Req | Req | |
| state | Req | Req | Req | |
| bid | Req | - | Req | Nested bid object |
| inventoryType | - | - | Req | e.g. STREAMING_TV |
| creativeRotationType | - | - | Req | e.g. RANDOM |
| startDateTime | - | - | Req | |
| endDateTime | - | - | Req | |
| pacing.deliveryProfile | - | - | Req | e.g. PACE_AHEAD |
| tags | Opt | Opt | Opt | |

### AdGroup Bid Object:
| Field | SP | SB | DSP |
|-------|----|----|-----|
| defaultBid | Req | - | - |
| baseBid | - | - | Req |
| maxAverageBid | - | - | Opt |
| currencyCode | RO | - | RO |

### AdGroup Budgets (DSP Only):
Same structure as Campaign Budgets with LIFETIME recurrence.

### AdGroup Optimization (DSP Only):
| Field | Required |
|-------|----------|
| bidStrategy | Req |
| budgetSettings.budgetAllocation | Opt |
| budgetSettings.dailyMinSpendValue | Opt |

### AdGroup TargetingSettings (DSP Only):
| Field | Required | Notes |
|-------|----------|-------|
| amazonViewability.viewabilityTier | Req | e.g. ALL_TIERS |
| amazonViewability.includeUnmeasurableImpressions | Req | boolean |
| defaultAudienceTargetingMatchType | Opt | e.g. EXACT |
| enableLanguageTargeting | Opt | boolean |
| timeZoneType | Req | e.g. VIEWER |
| userLocationSignal | Req | e.g. MULTIPLE_SIGNALS |
| videoCompletionTier | Opt | e.g. ALL_TIERS |
| tacticsConvertersExclusionType | Opt | |
| targetedPGDealId | Opt | |

---

## 6. Ad Entity

### Core Ad Fields:

| Field | SP | SB | DSP | Notes |
|-------|----|----|-----|-------|
| adId | RO | RO | RO | Auto-generated |
| adProduct | Req | Req | Req | |
| adType | Req | Req | Req | e.g. PRODUCT_AD, COMPONENT |
| adGroupId | Req | Req | - | DSP uses Ad Associations |
| campaignId | RO | RO | - | |
| name | - | Req | Req | |
| state | Req | Req | Req | |
| creative | Opt | Opt | Opt | Nested creative object |
| marketplaces | RO | RO | Req | |
| tags | Opt | Opt | Opt | |

### Creative Types:

| Creative Type | SP | SB | DSP | Description |
|--------------|----|----|-----|-------------|
| productCreative | Y | - | - | Simple product ad |
| componentCreative | - | Y | Y | Complex creative with multiple settings |
| audioCreative | - | - | Y | Audio ads |
| displayCreative | - | - | Y | Standard display ads |
| thirdPartyCreative | - | - | Y | 3rd party served |
| videoCreative | - | - | Y | Video ads |

### SB Component Creative Sub-types:
- **productCollectionSettings** - Product collection ads with brand, logo, products, landing page
- **productVideoSettings** - Video ads with products
- **manualCollectionSettings** - Manual product selection with landing page
- **automaticCollectionSettings** - Automatic product selection
- **storeSpotlightSettings** - Store spotlight ads
- **dynamicCollectionSettings** - Dynamic product selection

### DSP Component Creative Sub-types:
- **brandStoreSettings** - Brand store creative with headlines, images, CTA
- **assetBasedCreativeSettings** - Asset-based with custom videos, images
- **responsiveEcommerceSettings** - Responsive e-commerce creative

### Key Creative Fields (SP - productCreative):
| Field | Required |
|-------|----------|
| advertisedProduct.productId | Req |
| advertisedProduct.productIdType | Req |

productIdType values: SKU, ASIN

### Key Creative Fields (SB - productVideoSettings):
| Field | Required |
|-------|----------|
| products[].productId | Opt |
| products[].productIdType | Req |
| videos[].assetId | Req |
| videos[].assetVersion | Req |
| brand | Opt |
| brandLogos | Opt |
| headlines | Opt |
| landingPage.landingPageType | Req |
| landingPage.landingPageUrl | Opt |

### Key Creative Fields (DSP - brandStoreSettings):
| Field | Required |
|-------|----------|
| brand | Req |
| callToActions.url | Req |
| callToActions.callToActionType | Opt |
| inventoryTypes | Req |
| language | Req |
| optimizationGoalKpi | Req |
| responsiveSizingBehavior | Req |
| squareImages[].assetId | Req |
| tallImages[].assetId | Req |
| wideImages[].assetId | Req |
| headlines | Opt |
| bodyText | Opt |

---

## 7. Target Entity

### Core Target Fields:

| Field | SP | SB | DSP | Notes |
|-------|----|----|-----|-------|
| targetId | RO | RO | RO | Auto-generated |
| adProduct | Req | Req | Req | |
| adGroupId | Opt | Req | Req | |
| campaignId | Opt | Opt | - | |
| negative | Req | Req | Req | boolean - negative targeting |
| state | Req | Req | Req | |
| targetType | Req | Req | Req | See types below |
| targetDetails | Opt | Opt | Opt | Nested by type |
| bid | Opt | Opt | - | |

### Target Types Available:

| Target Type | SP | SB | DSP | Key Fields |
|-------------|----|----|-----|------------|
| keywordTarget | Y | Y | Y | keyword, matchType (EXACT/BROAD/PHRASE) |
| productTarget | Y | Y | Y | matchType (PRODUCT_EXACT), productId, productIdType |
| productCategoryTarget | Y | Y | Y | productCategoryId |
| themeTarget | Y | Y | Y | matchType (KEYWORDS_RELATED_TO_YOUR_BRAND) |
| audienceTarget | - | - | Y | audienceId, groupId, operators |
| contentCategoryTarget | - | - | Y | contentCategoryId |
| contentGenreTarget | - | - | Y | contentGenre |
| contentInstreamPositionTarget | - | - | Y | instreamPosition |
| contentOutstreamPositionTarget | - | - | Y | outstreamPosition |
| contentRatingTarget | - | - | Y | contentRatingType, details |
| dayPartTarget | - | - | Y | dayOfWeek, timeOfDay (start/end) |
| deviceTarget | - | - | Y | deviceType, mobileDevice, mobileOs |
| domainTarget | - | - | Y | domainTargetType, various domain specs |
| foldPositionTarget | - | - | Y | fold position |
| inventorySourceTarget | - | - | Y | inventory source |
| locationTarget | - | - | Y | geographic targeting |
| adInitiationTarget | - | - | Y | videoInitiationType |
| adPlayerSizeTarget | - | - | Y | adPlayerSize |
| appTarget | - | - | Y | appId, appType |
| nativeContentPositionTarget | - | - | Y | native position |
| videoAdFormatTarget | - | - | Y | video format |
| videoContentDurationTarget | - | - | Y | video duration |

### Third-Party Target Details (DSP Only):
- DoubleVerify: fraud/invalid traffic settings
- Integral Ad Science (IAS): contextual targeting, fraud/invalid traffic, viewability
- NewsGuard: brand guard trusted news targeting
- Pixalate: fraud/invalid traffic settings

### Batch Limits:
- Targets: up to 1000 per request (create/update/delete)
- Query: maxResults up to 5000

---

## 8. Ad Association Entity (DSP Only)

Used to link DSP Ads to Ad Groups.

### Endpoints:
- Create: `POST /adsApi/v1/create/adAssociations`
- Delete: `POST /adsApi/v1/delete/adAssociations`
- Query: `POST /adsApi/v1/query/adAssociations`

### Required Permission: `campaign_edit` (create/delete), `creatives_view` or `campaign_view` (query)

### Query Filters:
- adAssociationIdFilter
- adGroupIdFilter
- adIdFilter
- maxResults: 1-100 (default 100)
- nextToken for pagination

### Batch Limits:
- adAssociations: 1-20 items per request
- adAssociationIds: 1-20 items per delete

---

## 9. Example Request Payloads

### SP Campaign Create:
```json
{
    "campaigns": [{
        "adProduct": "SPONSORED_PRODUCTS",
        "name": "My Test Campaign",
        "state": "ENABLED",
        "marketplaceScope": "SINGLE_MARKETPLACE",
        "marketplaces": ["US"],
        "startDateTime": "2025-11-01T00:00:00.000-07:00",
        "budgets": [{
            "budgetType": "MONETARY",
            "budgetValue": {
                "monetaryBudgetValue": {
                    "monetaryBudget": {"value": 1000.0}
                }
            },
            "recurrenceTimePeriod": "DAILY"
        }],
        "autoCreationSettings": {"autoCreateTargets": false}
    }]
}
```

### SP Target Create (Keyword):
```json
{
    "targets": [{
        "adGroupId": "420175408832647",
        "adProduct": "SPONSORED_PRODUCTS",
        "negative": false,
        "state": "ENABLED",
        "targetType": "KEYWORD",
        "targetDetails": {
            "keywordTarget": {
                "keyword": "Test keyword",
                "matchType": "EXACT"
            }
        }
    }]
}
```

### SB Campaign Create:
```json
{
    "campaigns": [{
        "adProduct": "SPONSORED_BRANDS",
        "marketplaceScope": "SINGLE_MARKETPLACE",
        "name": "My SB Campaign",
        "state": "PAUSED",
        "marketplaces": ["US"],
        "startDateTime": "2027-03-18T00:00:08Z",
        "costType": "CPC",
        "budgets": [{
            "budgetType": "MONETARY",
            "budgetValue": {
                "monetaryBudgetValue": {
                    "monetaryBudget": {"value": 1000.0}
                }
            },
            "recurrenceTimePeriod": "DAILY"
        }],
        "optimizations": {
            "goalSettings": {"kpi": "CLICKS"}
        }
    }]
}
```

### DSP Campaign Create:
```json
{
    "campaigns": [{
        "adProduct": "AMAZON_DSP",
        "name": "Test DSP Campaign",
        "state": "PAUSED",
        "marketplaces": ["US"],
        "flights": [{
            "budget": {
                "budgetType": "MONETARY",
                "budgetValue": {
                    "monetaryBudgetValue": {
                        "monetaryBudget": {"value": 45.0}
                    }
                }
            },
            "endDateTime": "2025-08-10T23:59:59Z",
            "startDateTime": "2025-08-04T04:00:00Z"
        }],
        "optimizations": {
            "bidSettings": {"bidStrategy": "SPEND_BUDGET_IN_FULL"},
            "budgetSettings": {"budgetAllocation": "MANUAL"},
            "goalSettings": {"kpi": "REACH"}
        }
    }]
}
```

### Generic Update Pattern:
```json
{
    "campaigns": [{
        "campaignId": "339874654410161",
        "state": "PAUSED"
    }]
}
```

### Generic Query Pattern:
```json
{
    "campaignIdFilter": {"include": ["339874654410161"]},
    "adProductFilter": {"include": ["SPONSORED_PRODUCTS"]}
}
```

### Generic Delete Pattern:
```json
{
    "campaignIds": ["339874654410161"]
}
```

---

## 10. API v1 Specification Reference

### Base URL: `https://advertising-api-eu.amazon.com`

### All v1 Resource Groups:
| Resource | Create | Query | Update | Delete |
|----------|--------|-------|--------|--------|
| AdAssociations | Y | Y | - | Y |
| AdExtensions | - | - | - | - |
| AdGroups | Y | Y | Y | Y |
| Ads | Y | Y | Y | Y |
| AdvertisingDeals | - | - | - | - |
| AdvertisingDealTargets | - | - | - | - |
| BrandedKeywordsPricings | - | - | - | - |
| BrandStoreEditionPublishVersions | - | - | - | - |
| BrandStoreEditions | - | - | - | - |
| BrandStorePages | - | - | - | - |
| BrandStores | - | - | - | - |
| CampaignForecasts | - | - | - | - |
| Campaigns | Y | Y | Y | Y |
| Commitments | - | - | - | - |
| CommitmentSpends | - | - | - | - |
| KeywordReservationValidations | - | - | - | - |
| Recommendations | Y (SB) | - | - | - |
| RecommendationTypes | - | Y (SB) | - | - |
| Targets | Y | Y | Y | Y |

### Specification:
- Version: 1 (OAS 3.0.1)
- OpenAPI spec downloadable from Amazon

### Permissions Required:
| Operation | Permissions |
|-----------|------------|
| Create Campaign/AdGroup/Ad | campaign_edit, advertiser_campaign_edit |
| Query Campaign/AdGroup/Ad | campaign_view, advertiser_campaign_view |
| Create/Update Target | advertiser_campaign_edit, campaign_edit, dsp_campaign_edit |
| Query Target | advertiser_campaign_edit, dsp_campaign_view, campaign_view, etc. |
| Delete Target | advertiser_campaign_edit, campaign_edit, dsp_campaign_edit |
| Create Ad Association | campaign_edit |
| Query Ad Association | creatives_view, campaign_view |

---

## Relevance to Our Setup (GoAmrita Bhandar)

### What We Can Use Now:
- **SP Campaign Management** - Create/manage Sponsored Products campaigns via API
- **SP Targeting** - Keyword and product targeting for SP
- **Query operations** - List all campaigns, ad groups, ads, targets

### What We Might Use Later:
- **SB Campaign Management** - If/when we use Sponsored Brands
- **SD Campaign Management** - If/when we use Sponsored Display

### For India Marketplace:
- marketplace value: "IN"
- Endpoint: advertising-api-eu.amazon.com (EU region)
- AccountId: Our advertiser account ID
- ProfileId: 42634532240933

---

*Document Version: 1.0*
*Created: 13 April 2026*
*Source file: part 2 api text copied from amazon.txt*
