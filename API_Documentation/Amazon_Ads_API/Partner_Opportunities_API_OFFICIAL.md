# Partner Opportunities API — Official Documentation
**Source:** Amazon Ads Developer Documentation (Part 4)
**Saved:** 13 April 2026
**Category:** Amazon Ads API (advertising-api-eu.amazon.com)

---

## Overview

The Partner Opportunities API provides automated, data-driven recommendations and insights for Amazon Ads Partner Network members managing advertiser accounts. It curates opportunities across your entire book of business.

---

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/partnerOpportunities` | GET | List all opportunities |
| `/partnerOpportunities/{id}/file` | GET | Download opportunity data (CSV) |
| `/partnerOpportunities/{id}/apply` | POST | Apply recommendations (up to 100 IDs) |

### Required Headers
| Header | Value |
|--------|-------|
| Accept | `application/vnd.partneropportunity.v1+json` |
| Amazon-Advertising-API-ClientId | LWA App Client ID |
| Amazon-Advertising-API-Manager-Account | Partner Network Account ID |
| Authorization | Bearer {access_token} |

### Optional Filters
- `locale` for translation (e.g., `en_US`)
- `advertiserId` or `profileId` for specific advertisers

---

## Opportunity Catalog Categories

### Account Team Recommendations
Curated suggestions from Amazon Ads account managers, including:
- Optimize bids for SP/SB/SD campaigns
- Create campaigns for declining CTR/CVR ASINs
- Add targets for high-performing campaigns
- Add event budget rules
- Create SB video campaigns
- Increase budget for high-performing campaigns

### Campaign Optimization
- Target Promotion Groups (AT to MT conversion)
- Reduce risk of campaigns exhausting budgets
- Drive visibility for ad-restricted ASINs
- Showcase newly launched ASINs
- Campaign presets for easy launch
- Budget recommendations with missed opportunities

### Category Insights, Click Credits, Deals, Unlaunched ASINs
Additional opportunity types for various optimization scenarios.

---

## Integration with Amazon Marketing Stream

Subscribe to `sponsored-ads-campaign-diagnostics-recommendations` dataset for real-time push notifications. Use `recommendation_id` from Stream payloads with the Apply API.

### Required Attributes Mapping
| PO Attribute | Marketing Stream Attribute |
|-------------|---------------------------|
| advertiserType | Recommendation.advertiser_type |
| encryptedAdvertiserId | advertiserId |
| entityId | entityId |
| marketplace | Recommendation.marketplace_name |
| recommendationIds | recommendationIds |

---

## Troubleshooting

| Error | Solution |
|-------|---------|
| 401 Unauthorized | Verify headers, re-authenticate |
| 403 Forbidden | Check Admin/Custom-Editor permissions |
| 404 Not Found | Verify rowCount > 0 before download |
| 415 Unsupported Media Type | Check Accept header (no wildcards) |

---
*File version: 1.0 | Extracted from Part 4 documentation*
