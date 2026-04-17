# API Learnings & Notes — Permanent Reference
**Purpose:** What we learned from actual API testing. No trial-error next time!
**Rule:** Update this file every time we discover something new about APIs.

---

## SP-API Learnings

### Catalog Items API v2022-04-01
- **Sale price NOT available** in attributes. `list_price` field exists but has no `value` — only `currency`.
- **Use for:** Product name, brand, BSR, images, dimensions, category — NOT for price.
- **Rate:** 2 req/sec, max 20 ASINs per batch via `identifiers` parameter.
- **BSR available:** Yes, via `includedData=salesRanks`. 133/168 ASINs had BSR.

### Pricing API v2022-05-01
- **Your Price = `listingPrice.amount`** in `featuredBuyingOptions → segmentedFeaturedOffers`.
- **Buy Box winner:** Check if `sellerId` matches our ID (A2AC2AS9R9CBEA).
- **Reference prices:** `WasPrice` available (the strikethrough price on Amazon).
- **Rate:** 0.033 req/sec = ~2 per MINUTE! 330 ASINs = ~9 minutes with 32s delay.
- **Batch:** Max 20 ASINs per request.
- **281/330 ASINs returned price** (85%). 49 without price = possibly inactive/suppressed.
- **Fulfillment type:** MFN (self-ship) or AFN (FBA) — tells us shipping cost difference.

### Important: Sale Price vs API Price
- **Sale Price (sales ÷ orders) is MORE ACCURATE** for True Profit calculation!
  - Reason: Includes MOQ effect (e.g., Celtic Salt ₹99 unit price, MOQ 2 = ₹198 per order)
  - Reason: Reflects actual transaction price (coupons, deals applied)
- **API Price = single unit "your price"** — useful as fallback only.
- **Priority:** Sale Price (actual) > API Price (unit) > Fallback (₹180)
- **Developer note:** When MOQ > 1, API price × orders ≠ actual sales. Always prefer sales data.

### MOQ (Minimum Order Quantity)
- **Not directly available** in Pricing API response.
- **Possible source:** Listings Items API → `purchasable_offer` attributes (to verify).
- **Workaround:** If (sales ÷ orders) > API price → likely MOQ > 1. Calculate: MOQ ≈ round(sale_price ÷ api_price).

---

## Ads API Learnings

### Reporting API v3
- **spSearchTerm** columns verified working: impressions, clicks, cost, purchases7d, sales7d, searchTerm, keyword, keywordType, campaignName, campaignId, adGroupName, adGroupId
- **spTargeting** — `keywordText` is WRONG column name. Correct = `keyword`. `targetingExpression` also not valid for spTargeting.
- **spPurchasedProduct** — `keywordText` is WRONG. Correct = `keyword`.
- **Report creation:** Async flow works reliably. Typical wait: 60-140 seconds.
- **GZIP_JSON:** All reports compressed. Use `gzip.decompress()`.

### Campaign Management
- **Campaign list:** POST /sp/campaigns/list (not GET!)
- **Versioned headers required:** `Content-Type: application/vnd.spCampaign.v3+json`
- **Batch size:** Up to 1000 items per request.
- **States:** ENABLED, PAUSED, ARCHIVED (not "ACTIVE")

---

## Rate Limit Summary (Tested)
| API | Rate | Batch | 330 ASINs Time |
|-----|------|-------|----------------|
| Ads Campaigns | ~10/sec | 1000 | < 1 sec |
| Ads Reporting | ~1/sec | 1 report | 2 min per report |
| SP Catalog | 2/sec | 20 | ~10 sec |
| SP Pricing | 0.033/sec | 20 | **~9 min** (bottleneck!) |

---

## ⚠️ Rate Limit Bottleneck & Mitigation Strategies

### Biggest Bottleneck: SP-API Pricing (0.033 req/sec = 2 per MINUTE!)
- **Problem:** 330 ASINs × batch of 20 = 17 batches. At 2/min = **~9 minutes** just for pricing!
- **Impact:** Daily pipeline total ~25 min, pricing alone is 36% of total time.

### Mitigation Strategies (MUST FOLLOW):
| Strategy | How | Saves |
|----------|-----|-------|
| **Batch Max 20 ASINs** per request | Always send 20 ASINs per call (never 1-by-1) | 16x faster |
| **Pull ONCE, Share Everywhere** | Store pricing data in JSON, ALL features read from store | Avoid duplicate API calls |
| **Freshness-Based Skip** | If pricing data < 12hr old, SKIP re-fetch | Saves entire 9 min |
| **Parallel where possible** | Run Pricing + Catalog + FBA Inventory in parallel (different APIs) | ~5 min saved |
| **Priority ASIN first** | Pull top-selling ASINs first, rest later | Business impact faster |
| **Cache with TTL** | Cache pricing responses, respect freshness_hours from config | Fewer API calls |

### Rate Limit Summary (All APIs — Tested):
| API | Rate | Batch Size | 330 ASINs Time | Bottleneck? |
|-----|------|------------|----------------|-------------|
| Ads Campaign/KW/AdGroup | ~10/sec | 1000 | < 1 sec | ❌ No |
| Ads Reporting (async) | ~1/sec create | 1 report | ~15 min (6 reports) | ⚡ Medium |
| SP-API Catalog | 2/sec | 20 ASINs | ~10 sec | ❌ No |
| **SP-API Pricing** | **0.033/sec** | **20 ASINs** | **~9 min** | **🔴 YES!** |
| SP-API FBA Inventory | 2/sec | pagination | ~5 sec | ❌ No |
| SP-API Orders | ~1/sec | pagination | ~5 sec | ❌ No |
| SP-API Feeds (create) | 0.083/sec | 1 feed | Slow — plan ahead | ⚡ Medium |

### Daily Pipeline Time Budget (~25 min total):
```
Auth tokens:        < 1 sec
Ads entity lists:   < 5 sec
Ads reports (6x):   ~15 min (async, parallel with SP-API!)
SP-API Pricing:     ~9 min  (BOTTLENECK — run parallel with Ads reports)
SP-API Catalog:     ~10 sec
SP-API FBA/Orders:  ~10 sec
─────────────────────────────
TOTAL (with parallel): ~18-25 min
```

**Rule:** Ads Reports + SP-API Pricing run IN PARALLEL = saves ~9 min!

---

### Orders API — Sales Data Accuracy
- **API is 15-30 min behind Seller Central** (real-time vs API sync delay)
- **Pending orders don't have OrderTotal** — revenue estimate needed (avg of confirmed orders × pending count)
- **Canceled orders included in response** — must filter out in calculation
- **For comparison (today vs yesterday): works perfectly** — both days have same delay, so % change accurate
- Example gap: Seller Central ₹59,493 vs API ₹42,253 (~28% gap from delay + pending)
- **Display: show "Last Sync" time** — only ONE place, replace old with new (no duplicate)
- **Alert: if difference > -10% vs yesterday → alert user**

---

*Last Updated: 13 April 2026*
*Update this file whenever new API behavior is discovered!*
