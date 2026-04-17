# Selling Partner API for Product Fees v0
## Official OpenAPI Spec Documentation
**Source:** https://github.com/amzn/selling-partner-api-models/blob/main/models/product-fees-api-model/productFeesV0.json
**Fetched:** 2026-04-13
**Spec Version:** Swagger 2.0
**API Version:** v0

---

## API Info
- **Title:** Selling Partner API for Product Fees
- **Description:** Programmatically retrieve estimated fees for a product. Use to estimate fees for any marketplace.
- **Host:** sellingpartnerapi-na.amazon.com (use `sellingpartnerapi-eu.amazon.com` for India/EU)
- **Schemes:** HTTPS
- **Consumes:** application/json
- **Produces:** application/json

---

## Endpoints

### 1. POST /products/fees/v0/listings/{SellerSKU}/feesEstimate
**Operation:** getMyFeesEstimateForSKU
**Description:** Returns estimated fees for the item specified by seller SKU.

**Parameters:**
| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| SellerSKU | path | string | Yes | Product identifier qualified by seller ID |
| body | body | GetMyFeesEstimateRequest | Yes | Fee estimate request |

**Responses:**
| Status | Description |
|--------|-------------|
| 200 | Success - GetMyFeesEstimateResponse |
| 400 | Invalid parameters |
| 401 | Authorization header malformed |
| 403 | Access forbidden |
| 404 | Resource not found |
| 429 | Rate limit exceeded |
| 500 | Server error |
| 503 | Service unavailable |

**Rate Limit:** 1 request/sec, Burst: 2

---

### 2. POST /products/fees/v0/items/{Asin}/feesEstimate
**Operation:** getMyFeesEstimateForASIN
**Description:** Returns estimated fees for the item specified by ASIN.

**Parameters:**
| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| Asin | path | string | Yes | Amazon Standard Identification Number |
| body | body | GetMyFeesEstimateRequest | Yes | Fee estimate request |

**Responses:** Same as endpoint 1
**Rate Limit:** 1 request/sec, Burst: 2

---

### 3. POST /products/fees/v0/feesEstimate
**Operation:** getMyFeesEstimates
**Description:** Returns estimated fees for a batch of items.

**Parameters:**
| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| body | body | array[FeesEstimateByIdRequest] | Yes | Batch fee estimate request |

**Responses:** Array of FeesEstimateResult objects
**Rate Limit:** 0.5 request/sec, Burst: 1

---

## Data Models

### GetMyFeesEstimateRequest
| Property | Type | Description |
|----------|------|-------------|
| FeesEstimateRequest | FeesEstimateRequest | The fee estimate request data |

### FeesEstimateRequest
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| MarketplaceId | string | Yes | Marketplace identifier |
| IsAmazonFulfilled | boolean | No | Whether the offer is fulfilled by Amazon (FBA) |
| PriceToEstimateFees | PriceToEstimateFees | Yes | Product price basis for fee estimation |
| Identifier | string | Yes | Unique caller-provided request tracker |
| OptionalFulfillmentProgram | string | No | Enum: `FBA_CORE` (standard fees), `FBA_SNL` (Small and Light reduced fees), `FBA_EFN` (European cross-border) |

### FeesEstimateByIdRequest
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| FeesEstimateRequest | FeesEstimateRequest | No | Fee estimate request |
| IdType | string | Yes | Enum: `ASIN`, `SellerSKU` |
| IdValue | string | Yes | Item identifier value |

### PriceToEstimateFees
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| ListingPrice | MoneyType | Yes | Item listing price |
| Shipping | MoneyType | No | Shipping cost |
| Points | Points | No | Amazon Points data |

### Points
| Property | Type | Description |
|----------|------|-------------|
| PointsNumber | integer | Amazon Points count |
| PointsMonetaryValue | MoneyType | Points monetary equivalent |

### MoneyType
| Property | Type | Description |
|----------|------|-------------|
| CurrencyCode | string | ISO 4217 currency code (e.g., "INR") |
| Amount | number | Monetary value |

### GetMyFeesEstimateResponse
| Property | Type | Description |
|----------|------|-------------|
| payload | FeesEstimateResult | Fee estimate result |
| errors | array[Error] | Error list |

### FeesEstimateResult
| Property | Type | Description |
|----------|------|-------------|
| Status | string | Enum: `Success`, `ClientError`, `ServiceError` |
| FeesEstimateIdentifier | FeesEstimateIdentifier | Request identifier details |
| FeesEstimate | FeesEstimate | Total fees and breakdown |
| Error | FeesEstimateError | Error details if applicable |

### FeesEstimateIdentifier
| Property | Type | Description |
|----------|------|-------------|
| MarketplaceId | string | Marketplace ID |
| SellerId | string | Seller ID |
| IdType | string | Identifier type (ASIN or SellerSKU) |
| IdValue | string | Identifier value |
| IsAmazonFulfilled | boolean | FBA flag |
| PriceToEstimateFees | PriceToEstimateFees | Price used |
| SellerInputIdentifier | string | Caller-provided identifier |
| OptionalFulfillmentProgram | string | Fulfillment program |

### FeesEstimate
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| TimeOfFeesEstimation | string (date-time) | Yes | Estimation timestamp |
| TotalFeesEstimate | MoneyType | No | Total estimated fees |
| FeeDetailList | array[FeeDetail] | No | Individual fee breakdown |

### FeeDetail
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| FeeType | string | Yes | Fee category (e.g., "ReferralFee", "FBAFees", "ClosingFee") |
| FeeAmount | MoneyType | Yes | Charged amount |
| FeePromotion | MoneyType | No | Promotion amount |
| TaxAmount | MoneyType | No | Tax component |
| FinalFee | MoneyType | Yes | Final amount after promotions |
| IncludedFeeDetailList | array[IncludedFeeDetail] | No | Contributing sub-fees |

### IncludedFeeDetail
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| FeeType | string | Yes | Sub-fee type |
| FeeAmount | MoneyType | Yes | Charged amount |
| FeePromotion | MoneyType | No | Promotion amount |
| TaxAmount | MoneyType | No | Tax component |
| FinalFee | MoneyType | Yes | Final amount |

### FeesEstimateError
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| Type | string | Yes | Error origin: `Receiver` or `Sender` |
| Code | string | Yes | Error category identifier |
| Message | string | Yes | Error description |
| Detail | array[object] | Yes | Additional context |

### Error
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| code | string | Yes | Error type identifier |
| message | string | Yes | Error description |
| details | string | No | Additional context |

---

## Common Fee Types (India Marketplace)
| Fee Type | Description |
|----------|-------------|
| ReferralFee | Amazon's commission (percentage of sale price) |
| ClosingFee | Fixed fee per item |
| FBAFees | FBA fulfillment fees (pick, pack, ship) |
| FBAWeightHandling | Weight-based handling fee |
| FBAPickAndPack | Pick and pack fee |
| ShippingChargeback | Shipping fee for seller-fulfilled |

---

## Rate Limits
| Operation | Rate | Burst |
|-----------|------|-------|
| getMyFeesEstimateForSKU | 1 req/sec | 2 |
| getMyFeesEstimateForASIN | 1 req/sec | 2 |
| getMyFeesEstimates (batch) | 0.5 req/sec | 1 |

---

## Important Notes for GoAmrita Bhandar
- **Region:** India = EU endpoint (`sellingpartnerapi-eu.amazon.com`)
- **Marketplace ID for India:** A21TJRUUN4KGV
- **Currency:** INR for India marketplace
- Use `IsAmazonFulfilled=true` for FBA fee estimates, `false` for FBM (Easy Ship / Self Ship)
- `OptionalFulfillmentProgram` options: `FBA_CORE` (standard), `FBA_SNL` (Small & Light)
- `FBA_EFN` not applicable for India (European only)
- Batch endpoint (`/feesEstimate`) is more efficient for multiple products but has lower rate limit
- Fee estimates are approximate -- actual fees may differ slightly
