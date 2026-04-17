# Amazon SP-API - Product Fees API v0 - Official Reference
# Source: GitHub amzn/selling-partner-api-models/productFeesV0.json
# Extracted: 2026-04-13

## API Overview
- **Title:** Selling Partner API for Product Fees
- **Version:** v0
- **Host:** sellingpartnerapi-eu.amazon.com (for India/EU)
- **Schemes:** HTTPS
- **Content Types:** application/json

## Endpoints

### 1. POST /products/fees/v0/listings/{SellerSKU}/feesEstimate
**Operation ID:** getMyFeesEstimateForSKU
**Rate Limit:** 1 req/sec, burst 2

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| SellerSKU | string | Yes | Seller SKU identifier |

**Request Body:** GetMyFeesEstimateRequest
**Response:** GetMyFeesEstimateResponse

### 2. POST /products/fees/v0/items/{Asin}/feesEstimate
**Operation ID:** getMyFeesEstimateForASIN
**Rate Limit:** 1 req/sec, burst 2

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| Asin | string | Yes | Amazon Standard Identification Number |

**Request Body:** GetMyFeesEstimateRequest
**Response:** GetMyFeesEstimateResponse

**Note:** ASIN-based estimates use catalog size which may differ from actual item size.

### 3. POST /products/fees/v0/feesEstimate
**Operation ID:** getMyFeesEstimates
**Rate Limit:** 0.5 req/sec, burst 1

**Request Body:** GetMyFeesEstimatesRequest (array of FeesEstimateByIdRequest)
**Response:** GetMyFeesEstimatesResponse (array of FeesEstimateResult)

## Data Models

### GetMyFeesEstimateRequest
| Field | Type | Description |
|-------|------|-------------|
| FeesEstimateRequest | FeesEstimateRequest | The fees estimate request |

### FeesEstimateRequest
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| MarketplaceId | string | Yes | Marketplace identifier |
| IsAmazonFulfilled | boolean | No | True if fulfilled by Amazon |
| PriceToEstimateFees | PriceToEstimateFees | Yes | Price for fee estimate |
| Identifier | string | Yes | Unique caller-provided ID |
| OptionalFulfillmentProgram | string | No | Enum: FBA_CORE, FBA_SNL, FBA_EFN |

### FeesEstimateByIdRequest
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| FeesEstimateRequest | FeesEstimateRequest | No | Fees estimate request |
| IdType | string | Yes | Enum: ASIN, SellerSKU |
| IdValue | string | Yes | Item identifier value |

### PriceToEstimateFees
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ListingPrice | MoneyType | Yes | Item price |
| Shipping | MoneyType | No | Shipping cost |
| Points | Points | No | Amazon Points (Japan only) |

### MoneyType
| Field | Type | Description |
|-------|------|-------------|
| CurrencyCode | string | ISO 4217 currency code |
| Amount | number | Monetary value |

### Points
| Field | Type | Description |
|-------|------|-------------|
| PointsNumber | integer (int32) | Number of Amazon Points |
| PointsMonetaryValue | MoneyType | Points monetary value |

### GetMyFeesEstimateResponse
| Field | Type | Description |
|-------|------|-------------|
| payload | GetMyFeesEstimateResult | Operation payload |
| errors | ErrorList | Error array |

### GetMyFeesEstimateResult
| Field | Type | Description |
|-------|------|-------------|
| FeesEstimateResult | FeesEstimateResult | Estimated fees |

### FeesEstimateResult
| Field | Type | Description |
|-------|------|-------------|
| Status | string | Success, ClientError, ServiceError |
| FeesEstimateIdentifier | FeesEstimateIdentifier | Request identifier info |
| FeesEstimate | FeesEstimate | Total estimated fees |
| Error | FeesEstimateError | Error details |

### FeesEstimateIdentifier
| Field | Type | Description |
|-------|------|-------------|
| MarketplaceId | string | Marketplace ID |
| SellerId | string | Seller ID |
| IdType | string | ASIN or SellerSKU |
| IdValue | string | Item identifier |
| IsAmazonFulfilled | boolean | Amazon fulfilled flag |
| PriceToEstimateFees | PriceToEstimateFees | Price used |
| SellerInputIdentifier | string | Caller-provided ID |
| OptionalFulfillmentProgram | string | FBA_CORE/FBA_SNL/FBA_EFN |

### FeesEstimate
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| TimeOfFeesEstimation | date-time | Yes | Estimate timestamp |
| TotalFeesEstimate | MoneyType | No | Total fees |
| FeeDetailList | array[FeeDetail] | No | Fee breakdown |

### FeeDetail
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| FeeType | string | Yes | Fee type name |
| FeeAmount | MoneyType | Yes | Fee amount |
| FeePromotion | MoneyType | No | Promotion discount |
| TaxAmount | MoneyType | No | Tax on fee |
| FinalFee | MoneyType | Yes | Final fee after promotions |
| IncludedFeeDetailList | array[IncludedFeeDetail] | No | Sub-fees |

### IncludedFeeDetail
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| FeeType | string | Yes | Fee type name |
| FeeAmount | MoneyType | Yes | Fee amount |
| FeePromotion | MoneyType | No | Promotion discount |
| TaxAmount | MoneyType | No | Tax on fee |
| FinalFee | MoneyType | Yes | Final fee |

### FeesEstimateError
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Type | string | Yes | Error originator (receiver/sender) |
| Code | string | Yes | Error code |
| Message | string | Yes | Error message |
| Detail | array[object] | Yes | Additional info |

### IdType Enum
- ASIN: Amazon Standard Identification Number
- SellerSKU: Seller-provided identifier

### OptionalFulfillmentProgram Enum
- FBA_CORE: Standard Amazon fulfillment (default)
- FBA_SNL: Small and Light (sunset Sept 2023 in US/EU)
- FBA_EFN: Cross-border European Fulfillment Network

## Response Headers
x-amzn-RateLimit-Limit, x-amzn-RequestId

## HTTP Status Codes
200, 400, 401, 403, 404, 429, 500, 503
