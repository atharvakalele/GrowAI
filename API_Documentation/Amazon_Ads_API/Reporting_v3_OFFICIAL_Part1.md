# Amazon Ads Reporting API v3 - OFFICIAL Documentation (Part 1)
# Source: Amazon Advertising API Official Website (manually copied by Msir)
# Copied: April 2026
# Organized: 13 April 2026

---

## Overview

Version 3 reporting provides daily and summary performance reports for sponsored ads and Amazon DSP campaigns.

### Data Freshness
- Sponsored Ads: Initial data within 12 hours. Wait 5 days for accurate click data. Conversion data refreshed up to 60 days back.
- DSP: Invalid traffic invalidated within 72 hours.

### Reports vs Exports
- Reports = performance data (impressions, clicks, etc.)
- Exports = campaign metadata (budget, status, etc.)
- Use campaignId to join report + export data

### Rate Limits
- 429 response when rate limited. Dynamic based on time of day and request volume.

---

## Test Accounts

- Additional permission: advertising::test:create_account
- Account types: VENDOR, AUTHOR
- Create: POST /testAccounts
- Check status: GET /testAccounts?requestId={requestId}
- VENDOR marketplaces: US, CA, BR, MX, JP, AU, SG, UK, IT, ES, FR, DE, AE, SA, NL, TR, PL, SE, EG, BE
- AUTHOR marketplaces: US, UK, IT, ES, FR, DE
- Limitations: No performance data, no Lock Screen Ads/Posts/Stores, IMAGE assets only

---

## Async Report Workflow

Step 1: POST /reporting/reports (Content-Type: application/vnd.createasyncreportrequest.v3+json)
Step 2: GET /reporting/reports/{reportId} (poll until COMPLETED, up to 3 hours)
Step 3: Download from url field (S3 bucket, gzip JSON)

### Required Headers
- Amazon-Ads-ClientId: LwA client ID
- Authorization: Bearer {access_token}
- Amazon-Advertising-API-Scope: Profile ID
- Content-Type: application/vnd.createasyncreportrequest.v3+json
- Amazon-Ads-AccountId: Required for all ad products

### Request Body Structure
- name, startDate (YYYY-MM-DD), endDate (YYYY-MM-DD)
- configuration: adProduct, groupBy, columns, reportTypeId, timeUnit (DAILY/SUMMARY), format, filters
- DAILY timeUnit: include "date" column
- SUMMARY timeUnit: include "startDate" and "endDate" columns
- Duplicate requests return 425

---

## Report Types Availability Matrix

| Report Type | SP | SB | SD | ST | DSP | ALL |
|-------------|----|----|----|----|-----|-----|
| Ad | | Y | | | | |
| Ad group | | Y | Y | | | |
| Advertised product | Y | | Y | | | |
| Audience | Y | Y | | | Y | |
| Audio and video (beta) | | | | | Y | |
| Benchmarks (beta) | | | | | | Y |
| Bid adjustments | | | | | Y | |
| Brand suitability | | | | | Y | |
| Campaign | Y | Y | Y | Y | Y | |
| Conversion Path | | | | | | Y |
| Geo | | | | | Y | |
| Gross and invalid traffic | Y | Y | Y | | | |
| Inventory | | | | | Y | |
| Placement | | Y | | | | |
| Prompt Ad Extension | Y | | | | | |
| Product | | | | | Y | |
| Purchased product | Y | Y | Y | | | |
| Reach and frequency | | | | | Y | |
| Search term | Y | Y | | | | |
| Targeting | Y | Y | Y | Y | | |
| Tech | | | | | Y | |

---

## Report Type Details

### 1. Ad Reports (SB only) - reportTypeId: sbAds
- Max: 31 days, Retention: 60 days, groupBy: ads, format: GZIP_JSON
- Filters: adStatus (ENABLED, PAUSED, ARCHIVED)

### 2. Ad Group Reports
- SB: reportTypeId=sbAdGroup, groupBy=adGroup, Retention: 60d
- SD: reportTypeId=sdAdGroup, groupBy=adGroup or matchedTarget, Retention: 65d
- Note: SP has no separate ad group report (use campaign report with adGroup groupBy)

### 3. Advertised Product Reports
- SP: reportTypeId=spAdvertisedProduct, groupBy=advertiser, Retention: 95d
- SD: reportTypeId=sdAdvertisedProduct, groupBy=advertiser, Retention: 65d
- SP Filters: adCreativeStatus (ENABLED, PAUSED, ARCHIVED)
- SP key metrics: advertisedAsin, advertisedSku, purchases1d/7d/14d/30d, sales1d/7d/14d/30d, acosClicks7d/14d, roasClicks7d/14d

### 4. Audience Reports
- SP: reportTypeId=spAudiences, groupBy=campaign_bid_boost_segment, format: GZIP_JSON/XLSX
- SB: reportTypeId=sbAudiences, groupBy=campaign_bid_boost_segment, format: GZIP_JSON/XLSX
- DSP: reportTypeId=dspAudience, groupBy=order or lineItem, format: GZIP_JSON/CSV

### 5. Audio and Video Reports (DSP only, beta)
- reportTypeId=dspAudioAndVideo, Max: 395d, timeUnit: SUMMARY only
- groupBy: campaign, ad, supplySource, creative, content

### 6. Benchmarks Reports (beta)
- DSP: reportTypeId=dspBenchmarks, SA: reportTypeId=crossProgramBenchmarks
- timeUnit: DAILY/WEEKLY/MONTHLY, US only, brand owner required
- Available from October 1, 2025, updates every 48 hours
- Percentile metrics (P25/P50/P75) for NTB, ctr, cpc, cpm, video completion

### 7. Bid Adjustment Reports (DSP only)
- reportTypeId=dspBidAdjustment, Retention: 395d
- groupBy: bidAdjustmentRule and/or bidAdjustmentMatchedTerms

### 8. Brand Suitability Reports (DSP only)
- reportTypeId=dspBrandSuitability, Max/Retention: 395d
- groupBy: campaign, ad, supplySource, inventoryTier, contentCategory
- Cannot use both contentCategory AND inventoryTier together

### 9. Campaign Reports (ALL ad types)
- SP: spCampaigns, groupBy=campaign/adGroup/campaignPlacement, Retention: 95d
- SB: sbCampaigns, groupBy=campaign, Retention: 60d
- SD: sdCampaigns, groupBy=campaign/matchedTarget, Retention: 65d
- ST: stCampaigns, groupBy=campaign/adGroup, Retention: 95d
- DSP: dspCampaign, groupBy=campaign/ad/creative/flight, Retention: 95d
- SP campaignPlacement filter: campaignSite=AmazonBusiness (data from 9/5/2024)
- SB additions: longTermSales, longTermROAS, brandStorePageView
- ST additions: reach, householdReach, frequencyAverage, roas
- DSP flight groupBy: flightName, flightBudget, flightId, flightStartDate, flightEndDate

### 10. Conversion Path Reports
- reportTypeId=conversionPath, Max: 90d, Retention: 95d, timeUnit: SUMMARY only
- groupBy: brandConversionPath, format: CSV/GZIP_JSON
- Brand owner required, filter: brandName

---

## adProduct Values
- SPONSORED_PRODUCTS, SPONSORED_BRANDS, SPONSORED_DISPLAY, SPONSORED_TELEVISION
- DEMAND_SIDE_PLATFORM, ALL (cross-product)

## format Values
- GZIP_JSON (most common), CSV, XLSX

---

NOTE: Part 1 covers report types Ad through Conversion Path. Source also contains Geo, Gross/Invalid Traffic, Inventory, Placement, Prompt Ad Extension, Product, Purchased Product, Reach/Frequency, Search Term, Targeting, Tech, Columns, and FAQ (for Part 2).
