# Amazon DSP Bid Adjustments API — Official Documentation
**Source:** Amazon Ads Developer Documentation (Part 4)
**Saved:** 13 April 2026
**Category:** Amazon DSP (advertising-api-eu.amazon.com)

---

## Overview

Bid adjustments (previously "bid modifiers") let you adjust bids up or down for specific criteria at bidding time for a single line item. They work in tandem with Amazon DSP automated optimization.

**Important:** Bid adjustments adjust the **predicted value of impressions**, NOT the final bids. Amazon DSP continues optimizing for pacing, Target KPI, and max average CPM.

---

## API Endpoints & Rate Limits

| Endpoint | Method | Rate (req/sec) |
|----------|--------|----------------|
| `/dsp/rules/bidmodifier` | POST (create) | 10 |
| `/dsp/rules/bidmodifier/list` | POST (list) | 5 |
| `/dsp/rules/bidmodifier/{id}` | GET | 10 |
| `/dsp/rules/bidmodifier/{id}` | DELETE | 10 |
| `/dsp/rules/bidmodifier/{id}/associations` | PUT | 10 |
| `/dsp/rules/bidmodifier/{id}/associations` | DELETE | 10 |
| `/dsp/rules/bidmodifier/{id}/associations/list` | POST | 10 |
| `/dsp/rules/bidmodifier/{id}/associations/validate` | POST | 10 |

### Required Headers
| Header | Purpose |
|--------|---------|
| Amazon-Advertising-API-ClientId | Client ID for Login with Amazon |
| Amazon-Advertising-API-Scope | Profile ID for advertiser account |
| Amazon-Ads-AccountId | DSP Advertiser ID |

---

## System Limits

| Limit | Maximum |
|-------|---------|
| Payload size per rule | 1 MB |
| Terms per rule | 1,000 |
| Values per dimension | 1,000 |
| Rule description | 1,024 chars |
| Ad group IDs per association | 1,000 |
| Rules per advertiser | 2,000 |

---

## Bid Adjustment Rule Schema

| Field | Data Type | Description |
|-------|-----------|-------------|
| ruleDescription | String | Metadata description |
| ruleExpression | String | Contains terms and reconciliation logic |
| terms | List[Object] | Matching criteria + adjustment (max 1000) |
| onMultipleMatches | Enum | Only APPLY_PRODUCT supported (multiply) |
| bidAdjustment | Decimal | Multiplier 0-10.0 (truncated to 2 decimals) |
| negative (optional) | Boolean | Invert match (default false) |

**IMPORTANT:** All field names must use **camelCase** in API calls.

---

## Supported Dimensions

### Supply / Site / Slot
| Dimension | Type | Example |
|-----------|------|---------|
| domain | string | "foo.com" (case insensitive) |
| appId | string | "com.foo.mygame" (CASE SENSITIVE) |
| appName | string | "My Weather App" |
| dealId | string | Deal IDs from DSP deals API |
| slotSize | string | "300x50" |
| slotPosition | string | "ABOVE", "BELOW", "UNKNOWN" |
| supplySource | string | "Twitch", "Amazon Publisher Direct" |
| supplySourceType | string | "AMAZON", "AMAZON_PUBLISHER_DIRECT", "THIRD_PARTY_EXCHANGE" |

### Geography
| Dimension | Type | Example |
|-----------|------|---------|
| country | string | ISO 3166-1 alpha-2 ("JP", "US") |
| region | string | State name |
| dma | string | "DMA501" (Nielsen) |
| city | string | Full city name |
| postalCode | string | "US-33166", "JP-344-0063" |

### Environment
| Dimension | Type | Values |
|-----------|------|--------|
| deviceType | string | Phone, Tablet, PC, TV, ConnectedDevice, SetTopBox, Robot, Unknown |
| deviceMake | string | APPLE, GOOGLE, SAMSUNG, AMAZON |
| operatingSystem | string | MacOS, Windows, iOS, Android, Fire OS |
| browser | string | Chrome, Mozilla, Safari, Firefox |

### Ad Format
| Dimension | Type | Values |
|-----------|------|--------|
| adFormat | string | DISPLAY, AUDIO, VIDEO |

### Audience
| Dimension | Type | Description |
|-----------|------|-------------|
| behavioralSegment | string | Amazon Audience ID |

---

## How Bid Adjustments Are Calculated

When multiple terms match, bid adjustments are **multiplied** (APPLY_PRODUCT):

**Example:** Term 1 matches domain "foo.com" (0.75) + Term 2 matches device "Tablet" + OS "iOS" (1.25)
- Tablet + iOS + foo.com = 0.75 * 1.25 = 0.9375

### Negative Field
Setting `negative: true` means the adjustment applies when NONE of the dimension values match.

---

## Reporting

Two report types available:
- **Daily report:** Match rate, bids, win rate (per day)
- **Summary report:** Bids and win rate aggregated over period

Report type: `dspBidAdjustment` in reporting API.

---

## Best Practices

1. Use bid adjustments when Amazon DSP's default optimization cannot acquire needed signals
2. Focus on **relative** bid adjustment values, not absolute
3. Avoid scaling down bids aggressively (below 0.2) — can cause under-delivery
4. High final adjustments (>5x) may exhaust budget quickly
5. Always validate with A/B testing (use 10 Customer holdout groups)
6. Match rate may not sum to 100% due to low-occurrence filtering

---

## A/B Testing Setup
1. Create two identical orders (control + test)
2. Split users 50/50 using 5 Customer holdout groups each
3. Turn off Automated budget optimization
4. Apply bid adjustments to test only (or set control to 1.0 for comparison reports)

---

## Key FAQs

- **Bid adjustment of 0:** Does NOT completely stop bidding (other factors like pacing still apply). Use targeting exclusions instead.
- **Max adjustment:** Individual = 10, combined = 10, final bid capped by max avg CPM
- **Same dimension matches twice:** Multiplied accordingly
- **Fire TV / Fire Tablet:** Not currently supported

---
*File version: 1.0 | Extracted from Part 4 documentation*
