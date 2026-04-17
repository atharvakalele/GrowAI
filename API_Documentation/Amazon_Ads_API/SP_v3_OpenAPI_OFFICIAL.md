# Sponsored Products Campaign Management API v3 - OFFICIAL Documentation
# Source: Amazon Advertising API Official Website (manually copied by Msir)
# Copied: April 2026
# API Version: Version 3 (OAS 3.0.1)
# Organized: 13 April 2026

---

## Authentication & Required Headers

All endpoints require these headers:

| Header | Required | Description |
|--------|----------|-------------|
| Amazon-Advertising-API-ClientId | Yes | Client ID from Login with Amazon app |
| Amazon-Advertising-API-Scope | Yes | Profile ID for advertiser account |
| Authorization | Yes | Bearer {access_token} |
| Prefer | No | `return=representation` to get full objects on create/update/delete |

**For India Marketplace:** Use EU endpoint `https://advertising-api-eu.amazon.com`

---

## Permissions

Most endpoints require one of:
- `advertiser_campaign_edit` - Full edit access
- `advertiser_campaign_view` - Read-only access
- `campaign_proposed` - Proposed campaign access

---

## Standard Error Responses

All endpoints return these standard error codes:

| Code | Error | Description |
|------|-------|-------------|
| 400 | INVALID_ARGUMENT | Bad request / invalid parameters |
| 401 | UNAUTHORIZED | Authentication failed |
| 403 | ACCESS_DENIED | Insufficient permissions |
| 415 | UNSUPPORTED_MEDIA_TYPE | Wrong Content-Type header |
| 422 | UNPROCESSABLE_ENTITY | Valid syntax but cannot process |
| 429 | THROTTLED | Rate limited (check Retry-After header) |
| 500 | INTERNAL_ERROR | Server error |

**Rate Limiting:** 429 responses include `Retry-After` header (integer, seconds).

---

## Endpoint Categories

### 1. Ad Groups
Content-Type: `application/vnd.spAdGroup.v3+json`

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /sp/adGroups | Create | Create ad groups (up to 1000 per request) |
| PUT | /sp/adGroups | Update | Update ad groups (up to 1000 per request) |
| POST | /sp/adGroups/delete | Delete | Delete ad groups by ID filter |
| POST | /sp/adGroups/list | List | List ad groups with filters |

**List Filters:**
- adGroupIdFilter, campaignIdFilter, campaignTargetingTypeFilter (AUTO/MANUAL)
- nameFilter (BROAD_MATCH/EXACT_MATCH), stateFilter (ENABLED/PAUSED/ARCHIVED)
- includeExtendedDataFields (creationDate, lastUpdateDate, servingStatus)
- maxResults, nextToken (pagination)

---

### 2. Budget Recommendation - New Campaigns
Content-Type: `application/vnd.spinitialbudgetrecommendation.v3.4+json`

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /sp/campaigns/initialBudgetRecommendation | getBudgetRecommendation | Daily budget recommendation for new campaign |

**Request:** adGroups (array), bidding (strategy + adjustments), targetingType (auto/manual), startDate, endDate
**Response:** dailyBudget (recommended), benchmark (forecasted metrics for 7 days), specialEvents, recommendationId

**Bidding Strategies:** AUTO_FOR_SALES, LEGACY_FOR_SALES, MANUAL

---

### 3. Budget Recommendations & Missed Opportunities
Content-Type: `application/vnd.budgetrecommendation.v3+json`

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /sp/campaigns/budgetRecommendations | Get recommendations | Budget recs + missed opportunities for existing campaigns |

**Request:** campaignIds (array, 1-100)
**Response:** Recommended daily budget, percent time in budget, estimated missed impressions/clicks/sales

---

### 4. Budget Usage
Content-Type: `application/vnd.spcampaignbudgetusage.v1+json`

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /sp/campaigns/budget/usage | Get budget usage | Budget usage data for SP campaigns |

**Request:** campaignIds (array, 1-100)

---

### 5. Budget Rules
Content-Type: `application/json`

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| GET | /sp/budgetRules | List all | Get all budget rules (paginated, max 30) |
| POST | /sp/budgetRules | Create | Create budget rules (up to 25) |
| PUT | /sp/budgetRules | Update | Update budget rules (up to 25) |
| GET | /sp/budgetRules/{budgetRuleId} | Get by ID | Get specific budget rule |
| GET | /sp/budgetRules/{budgetRuleId}/campaigns | Get campaigns | Campaigns associated with a rule |
| POST | /sp/budgetRulesAssociation | Associate | Associate rules to campaigns (up to 50) |
| POST | /sp/budgetRulesAssociation/delete | Disassociate | Remove rule-campaign associations |
| GET | /sp/campaigns/{campaignId}/budgetRules | List rules for campaign | Budget rules for a campaign |
| POST | /sp/campaigns/{campaignId}/budgetRules | Associate to campaign | Associate rules to specific campaign (up to 25) |
| DELETE | /sp/campaigns/{campaignId}/budgetRules/{budgetRuleId} | Disassociate from campaign | Remove specific rule from campaign |

**Max rules per campaign:** 250 (each rule name must be unique per campaign)
**Budget Rule States:** ACTIVE, and others
**Global Ad Account support:** Amazon-Ads-AccountId header supported

---

### 6. Budget Rules Recommendations
Content-Type: `application/vnd.spbudgetrulesrecommendation.v3+json`

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /sp/campaigns/budgetRules/recommendations | Get recommendations | Special events + suggested budget increase for campaign |
| POST | /sp/v1/events | Get events | All special events with suggested date ranges |

**recommendationType:** EVENTS_FOR_EXISTING_CAMPAIGN

---

### 7. Campaign Negative Keywords
Content-Type: `application/vnd.spCampaignNegativeKeyword.v3+json`

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /sp/campaignNegativeKeywords | Create | Create (up to 1000) |
| PUT | /sp/campaignNegativeKeywords | Update | Update (up to 1000) |
| POST | /sp/campaignNegativeKeywords/delete | Delete | Delete by ID filter |
| POST | /sp/campaignNegativeKeywords/list | List | List with filters |

**List Filters:** campaignIdFilter, campaignNegativeKeywordIdFilter, campaignNegativeKeywordTextFilter, matchTypeFilter (NEGATIVE_BROAD, NEGATIVE_EXACT, NEGATIVE_PHRASE, OTHER), stateFilter, includeExtendedDataFields

---

### 8. Campaign Negative Targeting Clauses
Content-Type: `application/vnd.spCampaignNegativeTargetingClause.v3+json`

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /sp/campaignNegativeTargets | Create | Create (up to 1000) |
| PUT | /sp/campaignNegativeTargets | Update | Update (up to 1000) |
| POST | /sp/campaignNegativeTargets/delete | Delete | Delete by ID filter |
| POST | /sp/campaignNegativeTargets/list | List | List with filters |

**List Filters:** asinFilter, campaignIdFilter, campaignNegativeTargetIdFilter, stateFilter, includeExtendedDataFields

---

### 9. Campaign Optimization Rules
Content-Type: `application/vnd.optimizationrules.v1+json`

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /sp/rules/campaignOptimization | Create | Create optimization rule |
| PUT | /sp/rules/campaignOptimization | Update | Update optimization rule |
| POST | /sp/rules/campaignOptimization/eligibility | Check eligibility | Check campaign eligibility for rules |
| POST | /sp/rules/campaignOptimization/state | Get state | Get rule state (refresh daily) |
| DELETE | /sp/rules/campaignOptimization/{id} | Delete | Delete by ID |
| GET | /sp/rules/campaignOptimization/{id} | Get | Get by ID |

**Rule Types:** BID, KEYWORD, PRODUCT (currently only BID supported)
**Rule Actions:** ADOPT
**Recurrence:** DAILY
**Condition Metrics:** AVERAGE_BID, ROAS
**Comparison Operators:** EQUAL_TO, GREATER_THAN, GREATER_THAN_OR_EQUAL_TO, LESS_THAN, LESS_THAN_OR_EQUAL_TO
**Max campaigns per rule:** 20
**Max conditions per rule:** 3
**Rule Statuses:** ACTIVE and others

---

### 10. Campaigns
Content-Type: `application/vnd.spCampaign.v3+json`

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /sp/campaigns | Create | Create campaigns (up to 1000) |
| PUT | /sp/campaigns | Update | Update campaigns (up to 1000, targetingType cannot change) |
| POST | /sp/campaigns/delete | Delete | Delete by ID filter |
| POST | /sp/campaigns/list | List | List with filters |

**List Filters:** campaignIdFilter, stateFilter, nameFilter, portfolioIdFilter, marketplaceBudgetAllocationFilter, includeExtendedDataFields, maxResults, nextToken

---

### 11. Consolidated Recommendations

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| GET | /sp/campaign/recommendations | getCampaignRecommendations | Top recommendations (bid, budget, targeting) |
| POST | /sp/campaign/recommendations | fetchCampaignRecommendations | Fetch specific recommendations for campaigns |

**GET params:** campaignIds (optional), nextToken, maxResults
**POST body:** campaigns (1-10, with recommendation types), maxResults (1-5), nextToken
**POST Content-Type:** `application/vnd.spgetcampaignrecommendationsrequest.v2+json`

---

### 12. Keyword Group Targeting Recommendations (BETA)
Content-Type: `application/vnd.spkeywordgroupsrecommendations.v1.0+json`

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /sp/targeting/recommendations/keywordGroups | getKeywordGroupRecommendations | Keyword Group targets for ASINs |

**Request:** asins (1-1000), countryCode, nextToken
**Global Ad Account support:** Amazon-Ads-AccountId header
**Locale support:** IETF BCP 47 (e.g., en-us, fr-CA)

---

### 13. Keyword Targets / Keyword Recommendations

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /sp/global/targets/keywords/recommendations/list | Get global keyword recommendations | Multi-country keyword recs |
| POST | /sp/targets/keywords/recommendations | Get keyword recommendations | Single marketplace keyword recs |

**Versions:** v3, v4, v5 available
**V5 New Features:** Theme-based bid recommendations, impact metrics
**Themes:** CONVERSION_OPPORTUNITIES, SPECIAL_DAYS
**Bidding Strategies:** LEGACY_FOR_SALES, AUTO_FOR_SALES, MANUAL
**Sort Dimensions:** CLICKS, CONVERSIONS, DEFAULT
**Max Recommendations:** 200
**Supported Locales:** ar_EG, de_DE, en_AE, en_AU, en_CA, en_GB, en_IN, en_SA, en_SG, en_US, es_ES, es_MX, fr_FR, it_IT, ja_JP, nl_NL, pl_PL, pt_BR, sv_SE, tr_TR, zh_CN

**V5 Availability:** US, CA, BR, MX, UK, DE, FR, ES, IN, IT, NL, AE, SA, TR, EG, BE, SE, PL, JP, AU, SG
**V4 Availability:** All marketplaces

---

### 14. Keywords
Content-Type: `application/vnd.spKeyword.v3+json`

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /sp/keywords | Create | Create keywords (up to 1000) |
| PUT | /sp/keywords | Update | Update keywords (up to 1000) |
| POST | /sp/keywords/delete | Delete | Delete by ID filter |
| POST | /sp/keywords/list | List | List with filters |

**List Filters:** adGroupIdFilter, campaignIdFilter, keywordIdFilter, keywordTextFilter, matchTypeFilter (BROAD, EXACT, PHRASE, OTHER), stateFilter, locale, includeExtendedDataFields

---

### 15. Multi Country Theme-based Bid Recommendations
Content-Type: `application/json`

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /sp/global/targets/bid/recommendations | Get bids | Multi-country bid recommendations for ad groups |

**Requires:** Global Ad Account ID (Amazon-Ads-AccountId header)
**Supported Countries:** US, CA, MX, BR, UK, DE, FR, ES, IT, IN, AE, SA, NL, PL, BE, SE, TR, EG, JP, AU, SG
**V5 Features:** Estimated impressions for bids, bid analyzer (8 bids per target, set includeAnalysis=true)
**V4 Features:** PAT_ASIN, PAT_CATEGORY, PAT_CATEGORY_REFINEMENT, KEYWORD_GROUP targeting
**Max targeting expressions:** 100 per request per country

---

### 16. Negative Keywords
Content-Type: `application/vnd.spNegativeKeyword.v3+json`

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /sp/negativeKeywords | Create | Create (up to 1000) |
| PUT | /sp/negativeKeywords | Update | Update (up to 1000) |
| POST | /sp/negativeKeywords/delete | Delete | Delete by ID filter |
| POST | /sp/negativeKeywords/list | List | List with filters |

**Match Types:** NEGATIVE_BROAD, NEGATIVE_EXACT, NEGATIVE_PHRASE, OTHER

---

### 17. Negative Targeting Clauses
Content-Type: `application/vnd.spNegativeTargetingClause.v3+json`

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /sp/negativeTargets | Create | Create (up to 1000) |
| PUT | /sp/negativeTargets | Update | Update (up to 1000) |
| POST | /sp/negativeTargets/delete | Delete | Delete by ID filter |
| POST | /sp/negativeTargets/list | List | List with filters |

---

### 18. Optimization Rules
Content-Type: `application/vnd.spoptimizationrules.v1+json`

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /sp/campaigns/{campaignId}/optimizationRules | Associate | Associate rules to campaign (1-25) |
| POST | /sp/rules/optimization | Create | Create optimization rules (1 at a time) |
| PUT | /sp/rules/optimization | Update | Update optimization rules (1-25) |
| POST | /sp/rules/optimization/search | Search | Search rules with filters |

**Search Filters:** campaignFilter (campaignId), optimizationRuleFilter (ruleCategory, ruleSubCategory), pageSize, nextToken

---

### 19. Product Ads
Content-Type: `application/vnd.spProductAd.v3+json`

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /sp/productAds | Create | Create product ads (up to 1000) |
| PUT | /sp/productAds | Update | Update product ads (up to 1000) |
| POST | /sp/productAds/delete | Delete | Delete by ID filter |
| POST | /sp/productAds/list | List | List with filters |

**List Filters:** adGroupIdFilter, adIdFilter, campaignIdFilter, stateFilter, includeExtendedDataFields

---

### 20. Product Recommendation Service
Content-Type: `application/vnd.spproductrecommendation.v3+json`

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /sp/targets/products/recommendations | Get recommendations | Suggested ASINs for product targeting |

**Request:** adAsins (array), count, cursor, locale
**Themes:**
- Top converting targets (sorted by sales)
- Similar items (frequently viewed together)
- Complements (frequently purchased together)
- Similar items with low ratings and reviews
- Other books read by your readers (for books)

**Locales:** en_US, en_GB, zh_CN, es_ES, jp_JP, de_DE, fr_FR, it_IT
**Pagination:** Cursor-based (next/previous cursors)
**Max results:** 1000 (ASIN format), 10 (themed format)

---

### 21. Product Targeting

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| GET | /sp/negativeTargets/brands/recommendations | Get negative brands | Brands recommended for negative targeting |
| POST | /sp/negativeTargets/brands/search | Search negative brands | Search brands by keyword (up to 100) |
| GET | /sp/targets/categories | Get categories | All targetable categories (tree structure) |
| POST | /sp/targets/categories/recommendations | Get category recs | Category recommendations for ASINs |
| GET | /sp/targets/category/{categoryId}/refinements | Get refinements | Refinements for a category |
| POST | /sp/targets/products/count | Get ASIN count | Count targetable ASINs with refinements |

**Category Locales:** ar_AE, de_DE, en_AE, en_AU, en_CA, en_GB, en_IN, en_SG, en_US, es_ES, es_MX, fr_CA, fr_FR, hi_IN, it_IT, ja_JP, ko_KR, nl_NL, pl_PL, pt_BR, sv_SE, ta_IN, th_TH, tr_TR, vi_VN, zh_CN

**Refinements:** ageRanges (toys/games), brands, genres (books), isPrimeShipping, priceRange, ratingRange (0-5)

---

### 22. Targeting Clauses
Content-Type: `application/vnd.spTargetingClause.v3+json`

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /sp/targets | Create | Create targeting clauses (up to 1000) |
| PUT | /sp/targets | Update | Update targeting clauses (up to 1000) |
| POST | /sp/targets/delete | Delete | Delete by ID filter |
| POST | /sp/targets/list | List | List with filters |

**List Filters:** adGroupIdFilter, asinFilter, campaignIdFilter, expressionTypeFilter, targetIdFilter, stateFilter, includeExtendedDataFields

---

### 23. Target Promotion Groups

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /sp/targetPromotionGroups | Create | Create target promotion group |
| POST | /sp/targetPromotionGroups/list | List | List target promotion groups |
| POST | /sp/targetPromotionGroups/recommendations | Get recommendations | Get keyword/product target recommendations |
| POST | /sp/targetPromotionGroups/targets | Create targets | Add targets to promotion group |
| POST | /sp/targetPromotionGroups/targets/list | List targets | List targets in promotion groups |

Content-Type: `application/vnd.sptargetpromotiongroup.v1+json`

**Purpose:** Groups auto-targeting and manual-targeting ad groups together. Promotes top-performing auto targets to manual campaigns.

---

### 24. Theme-based Bid Recommendations
Content-Type: `application/vnd.spthemebasedbidrecommendation.v3+json`

| Method | Path | Operation | Description |
|--------|------|-----------|-------------|
| POST | /sp/targets/bid/recommendations | Get bid recommendations | Theme-based bids for ad groups |

**Recommendation Types:** BIDS_FOR_EXISTING_AD_GROUP, BIDS_FOR_NEW_AD_GROUP
**Max targeting expressions:** 100 per request
**V5 Features:** Estimated impressions, bid analyzer (set includeAnalysis=true)
**V4 Features:** PAT_ASIN, PAT_CATEGORY, PAT_CATEGORY_REFINEMENT, KEYWORD_GROUP

---

## Complete Endpoint Summary

| # | Category | Endpoints | Method/Path Examples |
|---|----------|-----------|---------------------|
| 1 | Ad Groups | 4 | POST/PUT /sp/adGroups, POST /sp/adGroups/delete, POST /sp/adGroups/list |
| 2 | Budget Rec (New) | 1 | POST /sp/campaigns/initialBudgetRecommendation |
| 3 | Budget Rec (Existing) | 1 | POST /sp/campaigns/budgetRecommendations |
| 4 | Budget Usage | 1 | POST /sp/campaigns/budget/usage |
| 5 | Budget Rules | 10 | GET/POST/PUT /sp/budgetRules and related |
| 6 | Budget Rules Rec | 2 | POST /sp/campaigns/budgetRules/recommendations, POST /sp/v1/events |
| 7 | Campaign Neg Keywords | 4 | CRUD on /sp/campaignNegativeKeywords |
| 8 | Campaign Neg Targets | 4 | CRUD on /sp/campaignNegativeTargets |
| 9 | Campaign Optimization | 6 | /sp/rules/campaignOptimization and related |
| 10 | Campaigns | 4 | POST/PUT /sp/campaigns, POST /sp/campaigns/delete, POST /sp/campaigns/list |
| 11 | Consolidated Recs | 2 | GET/POST /sp/campaign/recommendations |
| 12 | Keyword Group Recs | 1 | POST /sp/targeting/recommendations/keywordGroups |
| 13 | Keyword Targets | 2 | Global + single marketplace keyword recs |
| 14 | Keywords | 4 | CRUD on /sp/keywords |
| 15 | Multi-Country Bids | 1 | POST /sp/global/targets/bid/recommendations |
| 16 | Negative Keywords | 4 | CRUD on /sp/negativeKeywords |
| 17 | Negative Targets | 4 | CRUD on /sp/negativeTargets |
| 18 | Optimization Rules | 4 | /sp/rules/optimization and related |
| 19 | Product Ads | 4 | CRUD on /sp/productAds |
| 20 | Product Rec Service | 1 | POST /sp/targets/products/recommendations |
| 21 | Product Targeting | 6 | Categories, brands, refinements, ASIN count |
| 22 | Targeting Clauses | 4 | CRUD on /sp/targets |
| 23 | Target Promotion Groups | 5 | /sp/targetPromotionGroups and related |
| 24 | Theme-based Bids | 1 | POST /sp/targets/bid/recommendations |

**TOTAL: ~73 endpoints across 24 categories**

---

## Key Enumerations

### Entity States
- ENABLED, PAUSED, ARCHIVED

### Targeting Types
- AUTO, MANUAL

### Match Types (Keywords)
- BROAD, EXACT, PHRASE, OTHER

### Negative Match Types
- NEGATIVE_BROAD, NEGATIVE_EXACT, NEGATIVE_PHRASE, OTHER

### Bidding Strategies
- AUTO_FOR_SALES (Dynamic up/down)
- LEGACY_FOR_SALES (Dynamic down only)
- MANUAL (Fixed bids)
- RULE_BASED (Rule-based)

### Campaign Optimization Rule Types
- BID (currently only supported), KEYWORD, PRODUCT

### Sort Dimensions (Keyword Recommendations)
- CLICKS, CONVERSIONS, DEFAULT

### Recommendation Themes (Bid)
- CONVERSION_OPPORTUNITIES, SPECIAL_DAYS

---

*Document generated from official Amazon Ads API documentation (SP Campaign Management v3 OpenAPI spec)*
*Source text file: Amazon Advertising api 3-0 openapi.txt (7397 lines)*
