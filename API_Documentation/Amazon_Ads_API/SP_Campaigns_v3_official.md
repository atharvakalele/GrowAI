---
## FALLBACK / OLD VERSION
**WARNING:** This entire file contains content from an older API version (v2). Use ONLY if primary version fails or lacks specific functionality.
**Our Primary Version:** Ads API v3 (Campaign Management) -- see `SP_v3_OpenAPI_OFFICIAL.md`
**This File's Version:** v2 (with some v3 migration notes)
**Primary Doc:** `SP_v3_OpenAPI_OFFICIAL.md` (73 v3 endpoints, full CRUD)
---

# Amazon Ads API - Sponsored Products v2/v3
## Official OpenAPI Spec Documentation
**Source:** https://github.com/wangjoshuah/Amazon-Ads-Sponsored-Products-API-Python-Client/blob/main/openapi.yaml (community-maintained from official spec)
**Official Docs:** https://advertising.amazon.com/API/docs/en-us/sponsored-products/3-0/openapi
**Fetched:** 2026-04-13
**API Version:** v2 (with v3 endpoints noted where applicable)

**NOTE:** The v3 OpenAPI spec is not publicly downloadable as raw JSON/YAML from Amazon. The official spec is served behind JS on the Amazon Ads portal. This documentation is from the v2 spec with v3 references noted. Amazon is migrating SP endpoints to v3 progressively.

---

## API Info
- **Title:** Amazon Ads API - Sponsored Products
- **Description:** Manages campaigns, ad groups, keywords, negative keywords, and product ads for Sponsored Products.
- **License:** Amazon Ads API License Agreement
- **Security:** HTTP Bearer Token (bearer)

## Servers
| Server | Description |
|--------|-------------|
| https://advertising-api-test.amazon.com | Sandbox/Test |
| https://advertising-api.amazon.com | North America Production |
| https://advertising-api-eu.amazon.com | Europe/India Production |
| https://advertising-api-fe.amazon.com | Far East Production |

**For GoAmrita Bhandar (India):** Use `https://advertising-api-eu.amazon.com`

---

## Required Headers (All Endpoints)
| Header | Type | Required | Description |
|--------|------|----------|-------------|
| Amazon-Advertising-API-ClientId | string | Yes | Client identifier from LWA app |
| Amazon-Advertising-API-Scope | string | Yes | Profile/account identifier |
| Authorization | string | Yes | Bearer token |

---

## Endpoints

### Campaigns
| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /v2/sp/campaigns | createCampaigns | Create one or more campaigns |
| PUT | /v2/sp/campaigns | updateCampaigns | Update one or more campaigns |
| GET | /v2/sp/campaigns | listCampaigns | List campaigns with filters |
| GET | /v2/sp/campaigns/{campaignId} | getCampaign | Get single campaign |
| DELETE | /v2/sp/campaigns/{campaignId} | archiveCampaign | Archive a campaign |
| GET | /v2/sp/campaigns/extended | listCampaignsEx | List with extended data |
| GET | /v2/sp/campaigns/extended/{campaignId} | getCampaignEx | Get single with extended data |

### Ad Groups
| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /v2/sp/adGroups | createAdGroups | Create ad groups |
| PUT | /v2/sp/adGroups | updateAdGroups | Update ad groups |
| GET | /v2/sp/adGroups | listAdGroups | List ad groups |
| GET | /v2/sp/adGroups/{adGroupId} | getAdGroup | Get single ad group |
| DELETE | /v2/sp/adGroups/{adGroupId} | archiveAdGroup | Archive ad group |
| GET | /v2/sp/adGroups/extended | listAdGroupsEx | List extended |
| GET | /v2/sp/adGroups/extended/{adGroupId} | getAdGroupEx | Get extended |

### Keywords
| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /v2/sp/keywords | createKeywords | Create keywords |
| PUT | /v2/sp/keywords | updateKeywords | Update keywords |
| GET | /v2/sp/keywords | listKeywords | List keywords |
| GET | /v2/sp/keywords/{keywordId} | getKeyword | Get single keyword |
| DELETE | /v2/sp/keywords/{keywordId} | archiveKeyword | Archive keyword |
| GET | /v2/sp/keywords/extended | listKeywordsEx | List extended |
| GET | /v2/sp/keywords/extended/{keywordId} | getKeywordEx | Get extended |

### Negative Keywords
| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /v2/sp/negativeKeywords | createNegativeKeywords | Create |
| PUT | /v2/sp/negativeKeywords | updateNegativeKeywords | Update |
| GET | /v2/sp/negativeKeywords | listNegativeKeywords | List |
| GET | /v2/sp/negativeKeywords/{keywordId} | getNegativeKeyword | Get |
| DELETE | /v2/sp/negativeKeywords/{keywordId} | archiveNegativeKeyword | Archive |
| GET | /v2/sp/negativeKeywords/extended | listNegativeKeywordsEx | List extended |
| GET | /v2/sp/negativeKeywords/extended/{keywordId} | getNegativeKeywordEx | Get extended |

### Campaign Negative Keywords
| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /v2/sp/campaignNegativeKeywords | create | Create |
| PUT | /v2/sp/campaignNegativeKeywords | update | Update |
| GET | /v2/sp/campaignNegativeKeywords | list | List |
| GET | /v2/sp/campaignNegativeKeywords/{keywordId} | get | Get |
| DELETE | /v2/sp/campaignNegativeKeywords/{keywordId} | archive | Archive |
| GET | /v2/sp/campaignNegativeKeywords/extended | listEx | List extended |
| GET | /v2/sp/campaignNegativeKeywords/extended/{keywordId} | getEx | Get extended |

### Product Ads
| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /v2/sp/productAds | createProductAds | Create product ads |
| PUT | /v2/sp/productAds | updateProductAds | Update product ads |
| GET | /v2/sp/productAds | listProductAds | List product ads |
| GET | /v2/sp/productAds/{adId} | getProductAd | Get single |
| DELETE | /v2/sp/productAds/{adId} | archiveProductAd | Archive |
| GET | /v2/sp/productAds/extended | listProductAdsEx | List extended |
| GET | /v2/sp/productAds/extended/{adId} | getProductAdEx | Get extended |

### Product Targeting
| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /v2/sp/targets | createTargets | Create targeting clauses |
| PUT | /v2/sp/targets | updateTargets | Update targeting clauses |
| GET | /v2/sp/targets | listTargets | List targeting clauses |
| GET | /v2/sp/targets/{targetId} | getTarget | Get single |
| DELETE | /v2/sp/targets/{targetId} | archiveTarget | Archive |
| GET | /v2/sp/targets/extended | listTargetsEx | List extended |
| GET | /v2/sp/targets/extended/{targetId} | getTargetEx | Get extended |
| POST | /v2/sp/targets/productRecommendations | getProductRecommendations | Get product recs |
| GET | /v2/sp/targets/brands | getBrandRecommendations | Get brand recs |

### Negative Product Targeting
| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /v2/sp/negativeTargets | create | Create |
| PUT | /v2/sp/negativeTargets | update | Update |
| GET | /v2/sp/negativeTargets | list | List |
| GET | /v2/sp/negativeTargets/{targetId} | get | Get |
| DELETE | /v2/sp/negativeTargets/{targetId} | archive | Archive |
| GET | /v2/sp/negativeTargets/extended | listEx | List extended |
| GET | /v2/sp/negativeTargets/extended/{targetId} | getEx | Get extended |

### Bid Recommendations
| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| GET | /v2/sp/adGroups/{adGroupId}/bidRecommendations | getAdGroupBidRec | Ad group bid recommendation |
| GET | /v2/sp/keywords/{keywordId}/bidRecommendations | getKeywordBidRec | Keyword bid recommendation |
| POST | /v2/sp/keywords/bidRecommendations | getBulkKeywordBidRec | Bulk keyword bid recs |
| POST | /v2/sp/targets/bidRecommendations | getTargetBidRec | Target bid recommendation |

### Suggested Keywords
| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| GET | /v2/sp/adGroups/{adGroupId}/suggested/keywords | getAdGroupSuggested | Ad group suggestions |
| GET | /v2/sp/adGroups/{adGroupId}/suggested/keywords/extended | getAdGroupSuggestedEx | Extended suggestions |
| GET | /v2/sp/asins/{asinValue}/suggested/keywords | getAsinSuggested | ASIN suggestions |
| POST | /v2/sp/asins/suggested/keywords | getBulkAsinSuggested | Bulk ASIN suggestions |

### Reports
| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /v2/sp/{recordType}/report | requestReport | Request a report |
| GET | /v2/reports/{reportId} | getReport | Get report status |
| GET | /v2/reports/{reportId}/download | downloadReport | Download report |

### Snapshots
| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /v2/sp/{recordType}/snapshot | requestSnapshot | Request snapshot |
| GET | /v2/sp/snapshots/{snapshotId} | getSnapshot | Get snapshot status |

---

## Common Query Parameters
| Name | Type | Description |
|------|------|-------------|
| startIndex | integer | Pagination offset (default: 0) |
| count | integer | Records per page |
| stateFilter | string | Enum: `enabled`, `paused`, `archived` |
| campaignIdFilter | string | Comma-delimited campaign IDs |
| adGroupIdFilter | string | Comma-delimited ad group IDs |
| matchTypeFilter | string | Enum: `broad`, `phrase`, `exact` |
| negativeMatchTypeFilter | string | Enum: `negativePhrase`, `negativeExact` |

---

## Core Data Models

### Campaign
| Property | Type | Description |
|----------|------|-------------|
| campaignId | number | Unique identifier |
| portfolioId | number | Portfolio association |
| name | string | Campaign name |
| tags | object | Custom key-value identifiers |
| campaignType | string | Always `sponsoredProducts` |
| targetingType | string | Enum: `manual`, `auto` |
| state | string | Enum: `enabled`, `paused`, `archived` |
| dailyBudget | number | Daily spend limit |
| startDate | string | Start date (YYYYMMDD) |
| endDate | string | End date (YYYYMMDD, nullable) |
| premiumBidAdjustment | boolean | Top placement bid increase |
| bidding | Bidding | Bidding strategy |

### Bidding
| Property | Type | Description |
|----------|------|-------------|
| strategy | string | Enum: `legacyForSales` (Dynamic down only), `autoForSales` (Dynamic up/down), `manual` (Fixed) |
| adjustments | array[Adjustment] | Placement adjustments |

### Adjustment
| Property | Type | Description |
|----------|------|-------------|
| predicate | string | Enum: `placementTop`, `placementProductPage` |
| percentage | number | Bid percentage adjustment |

### AdGroup
| Property | Type | Description |
|----------|------|-------------|
| adGroupId | number | Unique identifier |
| campaignId | number | Parent campaign ID |
| name | string | Ad group name |
| defaultBid | number | Default keyword bid |
| state | string | Enum: `enabled`, `paused`, `archived` |
| creationDate | number | Epoch timestamp |
| lastUpdatedDate | number | Epoch timestamp |
| servingStatus | string | Computed serving status |

### Keyword
| Property | Type | Description |
|----------|------|-------------|
| keywordId | number | Unique identifier |
| adGroupId | number | Parent ad group ID |
| campaignId | number | Parent campaign ID |
| keywordText | string | Search term text |
| matchType | string | Enum: `broad`, `phrase`, `exact` |
| state | string | Enum: `enabled`, `paused`, `archived` |
| bid | number | Keyword-specific bid |
| creationDate | number | Epoch timestamp |
| lastUpdatedDate | number | Epoch timestamp |

### NegativeKeyword
| Property | Type | Description |
|----------|------|-------------|
| keywordId | number | Unique identifier |
| adGroupId | number | Parent ad group ID |
| keywordText | string | Excluded term |
| matchType | string | Enum: `negativePhrase`, `negativeExact` |
| state | string | Enum: `enabled`, `archived` |

### CampaignNegativeKeyword
| Property | Type | Description |
|----------|------|-------------|
| keywordId | number | Unique identifier |
| campaignId | number | Parent campaign ID |
| keywordText | string | Excluded term |
| matchType | string | Enum: `negativePhrase`, `negativeExact` |
| state | string | Enum: `enabled`, `archived` |

### ProductAd
| Property | Type | Description |
|----------|------|-------------|
| adId | number | Unique identifier |
| adGroupId | number | Parent ad group ID |
| campaignId | number | Parent campaign ID |
| sku | string | Seller identifier |
| asin | string | Amazon identifier (for vendors) |
| state | string | Enum: `enabled`, `paused`, `archived` |

### TargetingClause (Product Targeting)
| Property | Type | Description |
|----------|------|-------------|
| targetId | number | Unique identifier |
| adGroupId | number | Parent ad group ID |
| campaignId | number | Parent campaign ID |
| state | string | Enum: `enabled`, `paused`, `archived` |
| bid | number | Target-specific bid |
| expressions | array[TargetingExpression] | Targeting predicates |
| creationDate | number | Epoch timestamp |
| lastUpdatedDate | number | Epoch timestamp |

### TargetingExpression
| Property | Type | Description |
|----------|------|-------------|
| type | string | Enum: `asinCategorySameAs`, `asinBrandSameAs`, `asinPriceLessThan`, `asinPriceGreaterThan`, `asinPriceBetween`, `asinReviewRatingLessThan`, `asinReviewRatingGreaterThan`, `asinReviewRatingBetween` |
| value | string/number | Predicate value |

### SuggestedBid
| Property | Type | Description |
|----------|------|-------------|
| rangeStart | number | Minimum recommended bid |
| rangeEnd | number | Maximum recommended bid |
| recommendedBid | number | Optimal bid suggestion |

### ReportResponse
| Property | Type | Description |
|----------|------|-------------|
| reportId | string | Report identifier |
| recordType | string | Enum: `campaigns`, `adGroups`, `keywords`, `productAds`, `asins`, `targets` |
| status | string | Enum: `IN_PROGRESS`, `SUCCESS`, `FAILURE` |
| statusDetails | string | Status description |

### ReportRequest
| Property | Type | Description |
|----------|------|-------------|
| startDate | string | YYYYMMDD format |
| endDate | string | YYYYMMDD format |
| stateFilter | string | Enum: `enabled`, `paused`, `archived` |
| metrics | array[string] | Data fields to include |

### SnapshotResponse
| Property | Type | Description |
|----------|------|-------------|
| snapshotId | number | Snapshot identifier |
| recordType | string | Record type |
| status | string | Enum: `IN_PROGRESS`, `SUCCESS`, `FAILURE` |
| statusDetails | string | Status description |
| location | string | Download URL |

---

## Response Status Codes
| Status | Description |
|--------|-------------|
| 200 | Success |
| 207 | Multi-status (partial success for batch operations) |
| 400 | Bad request |
| 401 | Unauthorized |
| 404 | Not found |
| 422 | Unprocessable entity |
| 429 | Rate limit exceeded |

### Multi-Status Response Codes (207)
| Code | Description |
|------|-------------|
| SUCCESS | Operation succeeded |
| INVALID_ARGUMENT | Invalid input parameter |
| NOT_FOUND | Resource not found |
| INTERNAL_ERROR | Server error |
| SERVER_IS_BUSY | Server overloaded |
| UNAUTHORIZED | Insufficient permissions |

### Error Response
| Property | Type | Description |
|----------|------|-------------|
| code | string | Error code |
| details | string | Error description |

---

## SP v3 Migration Notes
Amazon is progressively migrating Sponsored Products endpoints from v2 to v3. Key v3 changes:
- Campaign budget type support (DAILY vs LIFETIME)
- Enhanced targeting options
- New budget rule endpoints
- Consolidated CRUD operations
- Different request/response format

v3 endpoints follow pattern: `/sp/campaigns`, `/sp/adGroups`, etc. (without `/v2/` prefix)

The v3 OpenAPI spec is available at the Amazon Advertising developer portal but not as a downloadable file.

---

## Important Notes for GoAmrita Bhandar
- **Endpoint for India:** `https://advertising-api-eu.amazon.com`
- Use `Amazon-Advertising-API-Scope` header with your India profile ID
- Campaign `targetingType`: `auto` (Amazon picks keywords) or `manual` (you choose)
- Bidding strategies: `manual` (Fixed), `legacyForSales` (Dynamic down), `autoForSales` (Dynamic up/down)
- Reports download URLs expire -- download immediately
- Use snapshots for bulk data retrieval of current state
- Batch operations return 207 with per-item status codes
