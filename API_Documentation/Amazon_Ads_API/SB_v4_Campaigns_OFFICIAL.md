# Sponsored Brands v4 - Campaign Management OFFICIAL Documentation
**Source:** Official Amazon Advertising documentation (manually copied by Msir)
**Date Captured:** 13 April 2026
**API Version:** Sponsored Brands v4
**Our Endpoint:** advertising-api-eu.amazon.com
**Our Profile ID:** 42634532240933
**Part of:** Part 3 API documentation batch

---

## Table of Contents
1. [Campaign Structure](#1-campaign-structure)
2. [Creating Campaigns (Step-by-Step)](#2-creating-campaigns)
3. [Goal-Based Campaigns](#3-goal-based-campaigns)
4. [Ad Types](#4-ad-types)
5. [Product Collection Ads](#5-product-collection-ads)
6. [Video & Brand Video Ads](#6-video--brand-video-ads)
7. [Store Spotlight Ads](#7-store-spotlight-ads)
8. [Targeting](#8-targeting)
9. [Bidding](#9-bidding)
10. [Reserve Share of Voice](#10-reserve-share-of-voice)
11. [SB Migration v3 to v4](#11-sb-migration-v3-to-v4)

---

## 1. Campaign Structure

### Hierarchy:
- **Campaigns:** Group ads by budget and dates
- **Ad Groups:** Organize by brands, keywords, products, ad formats, landing pages. Only 1 ad type per ad group
- **Ads:** Manage creative variations (video, store spotlight, product collection)
- **Creative Assets:** Images and videos per ad
- **Targeting:** Keyword OR product targeting per ad group

### Key Rule:
Each ad group can only contain a single type of ad.

---

## 2. Creating Campaigns

### Step 1: Create Campaign
**Endpoint:** `POST /sb/v4/campaigns`

For sellers with approved brands, include `brandEntityId` (get via `GET /brands`).

### Step 2: Create Ad Group
**Endpoint:** `POST /sb/v4/adGroups`

```json
{
  "adGroups": [{
    "campaignId": "{{campaignId}}",
    "name": "My ad group name",
    "state": "ENABLED"
  }]
}
```

### Step 3: Upload and Register Assets
Use the creative asset library API for video/image assets.

### Step 4: Create an Ad
Ad types: collections, product collection, video, brand video, store spotlight.
At least 1 ad per ad group required.

### Step 5: Add Targeting
- Keywords: `POST /sb/keywords`
- Product targeting: `POST /sb/targets`
- Theme targeting: `POST /sb/themes`

### Step 6: Check Moderation Status
Pass adId to the Moderation API.

### Step 7: Make Changes Based on Moderation
Edit ad/creative as needed.

---

## 3. Goal-Based Campaigns

### Goals:
| Goal | Description | Allowed costType |
|------|-------------|-----------------|
| BRAND_IMPRESSION_SHARE | Show ads to shoppers searching your brand | VCPM only |
| PAGE_VISIT | Drive traffic to landing/detail pages | CPC or VCPM |

### costType:
- **CPC:** Cost per click
- **VCPM:** Cost per 1000 viewable impressions

### smartDefault:
- **MANUAL:** No default targeting created
- **TARGETING:** Theme targeting auto-created with ad group

### Validation Rules:
- Both `goal` and `costType` must be included together
- If only one is provided: INVALID_ARGUMENT error
- Once created, goal/costType/smartDefault are NOT editable

### Sample Goal-Based Campaign:
```json
{
  "campaigns": [{
    "budgetType": "DAILY",
    "name": "Goal-based campaign",
    "state": "ENABLED",
    "startDate": "2023-08-21",
    "budget": 10,
    "goal": "BRAND_IMPRESSION_SHARE",
    "costType": "VCPM",
    "smartDefault": ["TARGETING"]
  }]
}
```

### Tip for VCPM/TARGETING:
Do NOT include bidding optimizations (bidOptimizationStrategy, bidAdjustmentsByShopperSegment, etc.).

---

## 4. Ad Types

| Ad Type | Description | API Resource |
|---------|-------------|-------------|
| Collections | ASIN-only product collection (being deprecated for custom image) | /sb/v4/ads/productCollection |
| Product Collection | Products with custom image, brand logo, headline | /sb/ads/creatives/productCollection |
| Video | Horizontal/vertical video for single product | /sb/v4/ads/video |
| Brand Video | Video with brand store landing page | /sb/v4/ads/brandVideo |
| Store Spotlight | Showcases Amazon Store + sub-pages | /sb/v4/ads/storeSpotlight |

### Ad Restrictions for BRAND_IMPRESSION_SHARE goal:
Must use one of:
- Product collection with custom image + Store landing page
- Store spotlight with Store landing page
- Brand video with Store landing page

---

## 5. Product Collection Ads

### Create: `POST /sb/v4/ads/productCollection`

### Key Components:
- Brand logo (assetId from asset library)
- Custom image (recommended, 50% CTR increase avg)
- Headline (max 50 chars, 30 for Japan)
- Minimum 3 products
- Landing page: PRODUCT_LIST, STORE, or CUSTOM_URL

### Landing Page Types:
- **Simple (PRODUCT_LIST):** List of ASINs
- **Store:** Amazon Brand Store page URL
- **Custom URL:** Custom Amazon landing page URL

### Edit Endpoints:
- `POST /sb/ads/creatives/productCollection` - Edit creative
- `POST /sb/ads/creatives/productCollectionExtended` - Edit with extended options

---

## 6. Video & Brand Video Ads

### Video (Single Product -> Detail Page):
**Endpoint:** `POST /sb/v4/ads/video`
- No landing page needed (auto-links to product detail page)
- Only horizontal video allowed

### Brand Video (Brand Store Landing):
**Endpoint:** `POST /sb/v4/ads/brandVideo`
- Requires STORE landing page
- ASIN in creative must appear on Store page
- Check ASINs on page: `GET /pageAsins`
- Supports 1-3 products (PAGE_VISIT goal) or 0-3 (BRAND_IMPRESSION_SHARE)
- Supports horizontal and vertical video

### Brand Logo Requirements:
- Size: 400x400px or larger
- File size: 1MB or smaller
- Format: PNG or JPG
- Content: Logo fills image or white/transparent background

### Vertical Video Specs:
| Spec | Requirement |
|------|-------------|
| Aspect Ratio | 9:16 |
| Dimensions | 720x1280, 1080x1920, or 2160x3840 |
| Duration | 6-45 seconds |
| Framerate | 23.976-30 FPS |
| Video Bitrate | 1 mbps+ |
| Codec | H.264 or H.265 |
| Audio Sample Rate | 44.1 kHz+ |
| Audio Bitrate | 96 kbps+ |
| Audio Codec | PCM, AAC, or MP3 |

### Edit Brand Video Landing: `POST /sb/ads/creatives/brandVideo`

---

## 7. Store Spotlight Ads

Feature Amazon Store and chosen sub-pages with cards.

---

## 8. Targeting

### Keywords: `POST /sb/keywords`
### Product Targeting: `POST /sb/targets`
### Theme Targeting: `POST /sb/themes`
### Negative Targets: `POST /sb/negativeTargets`
### Negative Keywords: `POST /sb/negativeKeywords`

---

## 9. Bidding

### Strategies (via campaign creation):
- Auto optimization by Amazon for placements other than top of search
- Custom bidding adjustments

---

## 10. Reserve Share of Voice

Reserve branded keywords for top-of-search SB placements at fixed upfront price.

### Workflow:
1. (Optional) Get keyword recommendations: `POST /adsApi/v1/create/recommendations/sb`
2. (Optional) Validate keywords: `POST /adsApi/v1/create/keywordReservationValidations/sb`
3. (Optional) Get pricing: `POST /adsApi/v1/create/brandedKeywordsPricings/sb`
4. Create deal: `POST /adsApi/v1/create/advertisingDeals/sb`
5. Create 5+ deal targets: `POST /adsApi/v1/create/advertisingDealTargets/sb`
6. Set deal state to PROPOSED: `POST /adsApi/v1/update/advertisingDeals/sb` (triggers pricing)
7. Create campaign with targetPGDealId (deal must be in PROPOSED state)

### Additional Operations:
- List deal targets: `POST /adsApi/v1/query/advertisingDealTargets/sb`
- Delete deal target: `POST /adsApi/v1/delete/advertisingDealTargets/sb`
- Get deal: `POST /adsApi/v1/query/advertisingDeals/sb`
- Delete deal: `POST /adsApi/v1/delete/advertisingDeals/sb`

### Date Format Note:
Only the day portion (before "T") is used. Interpreted in marketplace default timezone (e.g., US = Pacific Time).

---

## 11. SB Migration v3 to v4

Migration API available for transitioning from SB v3 to v4.

---
*Document version: 1.0 | Created: 13 April 2026*
