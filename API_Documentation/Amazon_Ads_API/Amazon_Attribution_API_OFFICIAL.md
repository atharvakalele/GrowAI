# Amazon Attribution API — Official Documentation
**Source:** Amazon Ads Developer Documentation (Part 4)
**Saved:** 13 April 2026
**Status:** Beta
**Category:** Amazon Ads API (advertising-api-eu.amazon.com)

---

## Overview

Amazon Attribution enables measurement of non-Amazon advertising campaigns that drive traffic to Amazon. It tracks click-attributed conversions within a 14-day window.

---

## Getting Started

### Prerequisites
1. Set up Advertising API developer account
2. Obtain authorization for advertiser's Amazon Ads account via:
   - OAuth Login With Amazon application (recommended)
   - Advertiser invitation to ad console account
   - Manager account invitation

### API Resources
| Resource | Description |
|----------|-------------|
| Profiles (`/v2/profiles`) | Advertiser accounts per marketplace |
| Advertisers | Attribution advertisers per profile |
| Publishers | Supported publisher list with macro support info |
| Attribution Tags | Macro and non-macro tags for tracking |
| Reports | Performance and Products reports |

---

## Attribution Tags

### Macro Tags
For publishers that support dynamic parameters (Google Ads, Facebook, Microsoft Ads, Pinterest):
```
GET /attribution/tags/macroTag
```
- Single tag works across all campaigns on that publisher
- Publisher dynamically inserts campaign IDs via macros

### Non-Macro Tags
For publishers without macro support:
```
GET /attribution/tags/nonMacroTemplateTag
```
- Must provide unique `aa_campaignid`, `aa_adgroupid`, `aa_creativeid` values
- Each tag can only be used on ONE landing page

### Tag Parameter Rules
- Values max 255 characters (after macro expansion)
- Forbidden characters: `/`, `&`, `=`, `#`, `?`, `+`, `'`, `"`, `%`, `$`
- `aa_campaignid` must be unique per account + marketplace
- Remove pre-existing `ref_` or `tag` parameters from URLs

**CRITICAL:** Calling a tag-retrieval endpoint is **mandatory** to enable measurement for each profile.

---

## Implementation Options
1. Append tag to landing page URL as query parameters
2. Use publisher's tracking template field (with {unescapedlpurl} for Google, {lpurl} for Microsoft)
3. Use publisher's URL parameters field (Facebook/Social)
4. Implement as click-tracker

---

## Measurement

- Campaigns auto-created from tag parameter values
- Products auto-associated from landing page
- 14-day click attribution window
- Last-clicked tag gets full credit
- **Privacy threshold:** Rows with <10 lifetime clicks show zeros

---

## Reports

### Report Types

| Type | Dimensions | Aggregation | Metrics | Date Range |
|------|-----------|-------------|---------|------------|
| PERFORMANCE | campaign, adgroup, creative, publisher | CAMPAIGN / ADGROUP / CREATIVE | Clicks + Promoted + Total conversions | 13 months |
| PRODUCTS | campaign, adgroup, publisher, product details | Ad group level | Promoted + Brand halo (no clicks). Top 100 products | 90 days |

### Brand Referral Bonus
For BRB-enrolled advertisers: request `brb_bonus_amount` metric at CAMPAIGN or ADGROUP level.

### Data Freshness
- Clicks: Up to 24 hours
- Conversions: Up to 48 hours
- Historical restatements at 1, 7, 28 days (returns/refunds)
- Recommendation: Pull last 30 days daily

---

## Migration Notes

Legacy Amazon Attribution accounts (DSP-based):
- Identified by `subType: "AMAZON_ATTRIBUTION"` on profile
- New integrators should filter these out
- Same API endpoints work for both legacy and ad console profiles

---

## Troubleshooting

### Common Issues

| Issue | Cause / Solution |
|-------|-----------------|
| Campaign not showing | Invalid landing page, tag retrieval not called, wait 4 hours |
| Clicks/conversions zero | Wait 24-48h, need 10+ clicks for privacy threshold |
| No conversions despite clicks | Wrong marketplace tag, wrong advertiser's product, parameter too long |
| {campaignid} in campaign name | Macro not processed — wrong publisher or wrong field |
| API vs Console numbers differ | Privacy threshold masking at different levels |
| No view-through conversions | Attribution API is click-only, no impression attribution |

---
*File version: 1.0 | Extracted from Part 4 documentation*
