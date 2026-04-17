---
## FALLBACK / OLD VERSION
**WARNING:** This file is a partial/early extraction. Use ONLY if primary version fails or lacks specific functionality.
**Our Primary Version:** Reporting v3 -- see `Reporting_v3_OFFICIAL_Part1.md`
**This File's Version:** Same v3, but INCOMPLETE (partial extraction from SPA-rendered docs)
**Primary Doc:** `Reporting_v3_OFFICIAL_Part1.md` (10 report types, full async workflow)
---

# Amazon Ads API - Reporting v3 (Unified) - Reference
# Source: Amazon Advertising API Documentation
# Extracted: 2026-04-13
# STATUS: PARTIAL - Ads docs are SPA-rendered, needs manual Chrome extraction for full coverage.

## API Overview
- Title: Amazon Advertising Reporting API v3
- Base URL: https://advertising-api-eu.amazon.com (EU/India)
- Auth: OAuth 2.0 + API headers
- Required Headers: Amazon-Advertising-API-ClientId, Amazon-Advertising-API-Scope, Authorization Bearer token
- Accept: application/vnd.createAsyncReportRequest.v3+json

## Endpoints

### POST /reporting/reports
Create async report request.
Body: name, startDate (YYYY-MM-DD), endDate (YYYY-MM-DD), configuration (adProduct, groupBy, columns, reportTypeId, timeUnit, format, filters)

Configuration fields:
- adProduct: SPONSORED_PRODUCTS, SPONSORED_BRANDS, SPONSORED_DISPLAY
- timeUnit: SUMMARY, DAILY
- format: GZIP_JSON (default)

### GET /reporting/reports/{reportId}
Get report status. Returns: reportId, status (PROCESSING/COMPLETED/FAILED), url (download when COMPLETED), fileSize, timestamps.

### GET /reporting/reports
List report requests.

## SP Report Types
- spCampaigns: Campaign-level metrics
- spAdGroups: Ad group-level metrics
- spAdvertisedProduct: Product-level metrics (SKU/ASIN)
- spSearchTerm: Search term report
- spTargeting: Targeting report
- spPlacement: Placement report

## Common Metrics
impressions, clicks, cost, purchases1d/7d/14d/30d, sales1d/7d/14d/30d, unitsSoldClicks1d/7d/14d/30d, costPerClick, clickThroughRate, acosClicks7d/14d, roasClicks7d/14d

## Common Dimensions
campaignId, campaignName, campaignStatus, campaignBudgetAmount, adGroupId, adGroupName, advertiserSku, asin, searchTerm, keywordId, keywordText, matchType, targetId, targetingExpression, placementClassification, date

## Filter Format
field: campaignStatus, values: [ENABLED]

## Workflow
1. POST /reporting/reports with config
2. Poll GET /reporting/reports/{reportId} until COMPLETED
3. Download GZIP_JSON from URL
4. Decompress and parse

## NOTE
This file needs completion via manual browser extraction from:
https://advertising.amazon.com/API/docs/en-us/reporting/v3/overview
