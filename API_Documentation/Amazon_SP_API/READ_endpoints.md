# SP-API READ-ONLY Endpoints Reference v1.0
## GoAmrita Bhandar / Made in Heavens

**Last Updated:** 13 April 2026
**Region:** EU (India marketplace)
**Base URL:** `https://sellingpartnerapi-eu.amazon.com`
**Marketplace ID:** `A21TJRUUN4KGV`
**Developer Type:** Private Developer (10 roles authorized)

---

## Common Headers (Required for ALL Requests)

```
x-amz-access-token: {LWA_access_token}
x-amz-date: {ISO8601_timestamp}  (format: 20260413T120000Z)
Host: sellingpartnerapi-eu.amazon.com
User-Agent: GoAmrita/1.0 (Language=Python/3; Platform=Windows)
Content-Type: application/json
```

### Authentication Flow (LWA - Login With Amazon)
1. POST `https://api.amazon.com/auth/o2/token`
2. Body: `grant_type=refresh_token&refresh_token={token}&client_id={id}&client_secret={secret}`
3. Response: `{ "access_token": "...", "token_type": "bearer", "expires_in": 3600 }`
4. Use access_token in `x-amz-access-token` header for all SP-API calls
5. Token valid for 1 hour, then refresh

### Rate Limiting
- SP-API uses **token bucket** rate limiting
- Each endpoint has its own burst rate and restore rate
- HTTP 429 = rate limited, implement exponential backoff
- `x-amzn-RateLimit-Limit` header in response shows current rate

---

## 1. Catalog Items API v2022-04-01

**Role Required:** Product Listing
**Use Case:** Get product details, images, sales ranks, dimensions, identifiers for any ASIN

### GET /catalog/2022-04-01/items/{asin}

**Description:** Get detailed info for a single catalog item by ASIN.

| Parameter | Location | Required | Type | Description |
|-----------|----------|----------|------|-------------|
| `asin` | path | Yes | string | The ASIN of the item |
| `marketplaceIds` | query | Yes | string[] | Comma-separated. Use `A21TJRUUN4KGV` for India |
| `includedData` | query | No | string[] | Comma-separated. Options: `attributes`, `dimensions`, `identifiers`, `images`, `productTypes`, `relationships`, `salesRanks`, `summaries`, `vendorDetails` |
| `locale` | query | No | string | Locale for attributes. e.g., `en_IN` |

**Rate Limit:** Burst: 2, Restore: 2/sec

**Response Key Fields:**
```json
{
  "asin": "B0XXXXXXXX",
  "attributes": { ... },        // Product attributes (title, brand, etc.)
  "dimensions": [{               // Package dimensions
    "marketplaceId": "A21TJRUUN4KGV",
    "item": { "height": {...}, "length": {...}, "weight": {...}, "width": {...} },
    "package": { "height": {...}, "length": {...}, "weight": {...}, "width": {...} }
  }],
  "identifiers": [{              // EAN, UPC, etc.
    "marketplaceId": "A21TJRUUN4KGV",
    "identifiers": [{ "identifierType": "EAN", "identifier": "..." }]
  }],
  "images": [{                   // Product images
    "marketplaceId": "A21TJRUUN4KGV",
    "images": [{ "variant": "MAIN", "link": "https://...", "height": 500, "width": 500 }]
  }],
  "productTypes": [{             // Product type classification
    "marketplaceId": "A21TJRUUN4KGV",
    "productType": "GROCERY"
  }],
  "salesRanks": [{               // Best Seller Rank
    "marketplaceId": "A21TJRUUN4KGV",
    "classificationRanks": [{ "classificationId": "...", "title": "Grocery & Gourmet Foods", "rank": 12345 }],
    "displayGroupRanks": [{ "websiteDisplayGroup": "grocery_display_on_website", "title": "...", "rank": 500 }]
  }],
  "summaries": [{                // Quick summary
    "marketplaceId": "A21TJRUUN4KGV",
    "brandName": "GoAmrita",
    "itemName": "Product Title",
    "manufacturer": "...",
    "modelNumber": "...",
    "itemClassification": "BASE_PRODUCT"
  }]
}
```

### GET /catalog/2022-04-01/items

**Description:** Search catalog items by keywords or identifiers.

| Parameter | Location | Required | Type | Description |
|-----------|----------|----------|------|-------------|
| `marketplaceIds` | query | Yes | string[] | `A21TJRUUN4KGV` |
| `identifiers` | query | Conditional | string[] | ASINs, EANs, UPCs to look up (max 20) |
| `identifiersType` | query | Conditional | string | `ASIN`, `EAN`, `UPC`, `ISBN` (required with identifiers) |
| `keywords` | query | Conditional | string[] | Search keywords (required if no identifiers) |
| `includedData` | query | No | string[] | Same as single item endpoint |
| `brandNames` | query | No | string[] | Filter by brand names |
| `classificationIds` | query | No | string[] | Filter by classification |
| `pageSize` | query | No | integer | Items per page (1-20, default 10) |
| `pageToken` | query | No | string | Pagination token from previous response |
| `locale` | query | No | string | `en_IN` |

**Rate Limit:** Burst: 2, Restore: 2/sec

**Response:** Same structure as single item but wrapped in:
```json
{
  "numberOfResults": 50,
  "pagination": { "nextToken": "...", "previousToken": "..." },
  "items": [ { "asin": "...", ... } ]
}
```

**Business Use:** Product research, competitor catalog analysis, getting images/BSR for dashboards, verifying our listing data.

---

## 2. Pricing API v2022-05-01

**Role Required:** Pricing
**Use Case:** Get Buy Box price, competitive prices, featured offer (lowest price). Critical for pricing strategy.

### POST /batches/pricing/2022-05-01/items/competitiveSummary

**Description:** Batch request for competitive pricing summary including Buy Box (Featured Offer).

**Rate Limit:** Burst: 1, Restore: 1/5sec

**Request Body:**
```json
{
  "requests": [
    {
      "uri": "/products/pricing/2022-05-01/items/competitiveSummary",
      "method": "GET",
      "queryParams": {
        "marketplaceId": "A21TJRUUN4KGV",
        "asin": "B0XXXXXXXX",
        "includedData": ["featuredBuyingOptions", "lowestPricedOffersForCondition", "referencePrices", "competitorOfferCounts"]
      }
    }
  ]
}
```

**includedData Options:**
- `featuredBuyingOptions` - Current Buy Box winner price & seller
- `lowestPricedOffersForCondition` - Lowest offers by condition (New, Used, etc.)
- `referencePrices` - MRP, was-price, list price
- `competitorOfferCounts` - Number of sellers per condition

**Max items per batch:** 20

**Response Key Fields:**
```json
{
  "responses": [{
    "status": { "statusCode": 200 },
    "body": {
      "asin": "B0XXXXXXXX",
      "marketplaceId": "A21TJRUUN4KGV",
      "featuredBuyingOptions": [{
        "buyingOptionType": "NEW",
        "segmentedFeaturedOffers": [{
          "condition": "New",
          "listingPrice": { "currencyCode": "INR", "amount": 299.00 },
          "shippingPrice": { "currencyCode": "INR", "amount": 0.00 },
          "points": { "pointsNumber": 0, "pointsMonetaryValue": {...} },
          "sellerId": "A1XXXXX",
          "isFeaturedBuyBoxWinner": true,
          "isFulfilledByAmazon": true
        }]
      }],
      "lowestPricedOffersForCondition": [{
        "condition": "New",
        "offers": [{
          "listingPrice": { "currencyCode": "INR", "amount": 285.00 },
          "shippingPrice": {...},
          "sellerId": "...",
          "isFulfilledByAmazon": true
        }]
      }],
      "referencePrices": [{
        "basisPriceType": "MRP",
        "basisPrice": { "currencyCode": "INR", "amount": 399.00 }
      }],
      "competitorOfferCounts": [
        { "condition": "New", "offerCount": 5 },
        { "condition": "Used", "offerCount": 0 }
      ]
    }
  }]
}
```

### GET /products/pricing/v0/price

**Description:** Get pricing for seller's own SKUs (older v0 API, still functional).

| Parameter | Location | Required | Type | Description |
|-----------|----------|----------|------|-------------|
| `MarketplaceId` | query | Yes | string | `A21TJRUUN4KGV` |
| `Asins` | query | Conditional | string[] | Up to 20 ASINs |
| `Skus` | query | Conditional | string[] | Up to 20 SKUs |
| `ItemType` | query | Yes | string | `Asin` or `Sku` |
| `ItemCondition` | query | No | string | `New`, `Used`, `Collectible`, `Refurbished`, `Club` |
| `OfferType` | query | No | string | `B2C` or `B2B` |

**Rate Limit:** Burst: 10, Restore: 10/sec (for getSKU), Burst: 10, Restore: 10/sec (for getASIN)

### GET /products/pricing/v0/competitivePrice

**Description:** Get competitive pricing for items.

| Parameter | Location | Required | Type | Description |
|-----------|----------|----------|------|-------------|
| `MarketplaceId` | query | Yes | string | `A21TJRUUN4KGV` |
| `Asins` | query | Conditional | string[] | Up to 20 ASINs |
| `ItemType` | query | Yes | string | `Asin` or `Sku` |
| `CustomerType` | query | No | string | `Consumer` or `Business` |

**Rate Limit:** Burst: 10, Restore: 10/sec

**Business Use:** Track Buy Box ownership, monitor competitor prices, automate pricing decisions, find underpriced/overpriced products.

---

## 3. Orders API v0

**Role Required:** Inventory and Order Tracking
**Use Case:** Get order history, order details, and order items for sales velocity analysis.

### GET /orders/v0/orders

**Description:** Get a list of orders within a date range.

| Parameter | Location | Required | Type | Description |
|-----------|----------|----------|------|-------------|
| `MarketplaceIds` | query | Yes | string[] | `A21TJRUUN4KGV` |
| `CreatedAfter` | query | Conditional | string | ISO 8601 datetime (required if LastUpdatedAfter not given) |
| `CreatedBefore` | query | No | string | ISO 8601 datetime |
| `LastUpdatedAfter` | query | Conditional | string | ISO 8601 (required if CreatedAfter not given) |
| `LastUpdatedBefore` | query | No | string | ISO 8601 |
| `OrderStatuses` | query | No | string[] | `Pending`, `Unshipped`, `PartiallyShipped`, `Shipped`, `Canceled`, `Unfulfillable`, `InvoiceUnconfirmed`, `PendingAvailability` |
| `FulfillmentChannels` | query | No | string[] | `MFN` (merchant), `AFN` (FBA) |
| `PaymentMethods` | query | No | string[] | `COD`, `CVS`, `Other` |
| `BuyerEmail` | query | No | string | Filter by buyer email |
| `SellerOrderId` | query | No | string | Seller's custom order ID |
| `MaxResultsPerPage` | query | No | integer | 1-100, default 100 |
| `NextToken` | query | No | string | Pagination token |
| `AmazonOrderIds` | query | No | string[] | Specific order IDs (max 50) |
| `ActualFulfillmentSupplySourceId` | query | No | string | Supply source ID |
| `IsISPU` | query | No | boolean | In-store pickup |
| `StoreChainStoreId` | query | No | string | Store chain ID |
| `EarliestDeliveryDateBefore` | query | No | string | ISO 8601 |
| `EarliestDeliveryDateAfter` | query | No | string | ISO 8601 |
| `LatestDeliveryDateBefore` | query | No | string | ISO 8601 |
| `LatestDeliveryDateAfter` | query | No | string | ISO 8601 |

**Rate Limit:** Burst: 20, Restore: 2/sec

**Response Key Fields:**
```json
{
  "payload": {
    "Orders": [{
      "AmazonOrderId": "402-XXXXXXX-XXXXXXX",
      "PurchaseDate": "2026-04-12T10:30:00Z",
      "LastUpdateDate": "2026-04-12T12:00:00Z",
      "OrderStatus": "Shipped",
      "FulfillmentChannel": "AFN",
      "SalesChannel": "Amazon.in",
      "OrderChannel": "...",
      "ShipServiceLevel": "Expedited",
      "OrderTotal": { "CurrencyCode": "INR", "Amount": "599.00" },
      "NumberOfItemsShipped": 1,
      "NumberOfItemsUnshipped": 0,
      "PaymentMethod": "Other",
      "PaymentMethodDetails": ["Standard"],
      "IsReplacementOrder": false,
      "MarketplaceId": "A21TJRUUN4KGV",
      "ShipmentServiceLevelCategory": "Expedited",
      "OrderType": "StandardOrder",
      "EarliestShipDate": "...",
      "LatestShipDate": "...",
      "EarliestDeliveryDate": "...",
      "LatestDeliveryDate": "...",
      "IsBusinessOrder": false,
      "IsPrime": false,
      "IsGlobalExpressEnabled": false,
      "IsPremiumOrder": false,
      "IsSoldByAB": false,
      "IsIBA": false,
      "ShippingAddress": {
        "Name": "...",
        "AddressLine1": "...",
        "City": "...",
        "StateOrRegion": "...",
        "PostalCode": "...",
        "CountryCode": "IN"
      },
      "BuyerInfo": {
        "BuyerEmail": "xxxxx@marketplace.amazon.in",
        "BuyerName": "...",
        "BuyerTaxInfo": { ... }
      }
    }],
    "NextToken": "..."
  }
}
```

### GET /orders/v0/orders/{orderId}

**Description:** Get a single order's details.

| Parameter | Location | Required | Type | Description |
|-----------|----------|----------|------|-------------|
| `orderId` | path | Yes | string | Amazon Order ID |

**Rate Limit:** Burst: 20, Restore: 2/sec

### GET /orders/v0/orders/{orderId}/orderItems

**Description:** Get line items for an order (ASIN, SKU, quantity, price per item).

| Parameter | Location | Required | Type | Description |
|-----------|----------|----------|------|-------------|
| `orderId` | path | Yes | string | Amazon Order ID |
| `NextToken` | query | No | string | Pagination |

**Rate Limit:** Burst: 20, Restore: 2/sec

**Response Key Fields:**
```json
{
  "payload": {
    "AmazonOrderId": "402-XXXXXXX-XXXXXXX",
    "OrderItems": [{
      "ASIN": "B0XXXXXXXX",
      "SellerSKU": "SKU-001",
      "OrderItemId": "...",
      "Title": "Product Name",
      "QuantityOrdered": 2,
      "QuantityShipped": 2,
      "ItemPrice": { "CurrencyCode": "INR", "Amount": "598.00" },
      "ShippingPrice": { "CurrencyCode": "INR", "Amount": "0.00" },
      "ItemTax": { "CurrencyCode": "INR", "Amount": "50.00" },
      "ShippingTax": { ... },
      "PromotionDiscount": { ... },
      "ShippingDiscount": { ... },
      "IsGift": false,
      "ConditionId": "New",
      "IsTransparency": false,
      "ProductInfo": { "NumberOfItems": 1 },
      "BuyerInfo": { ... }
    }]
  }
}
```

### GET /orders/v0/orders/{orderId}/address

**Description:** Get shipping address for an order.

**Rate Limit:** Burst: 20, Restore: 2/sec

### GET /orders/v0/orders/{orderId}/buyerInfo

**Description:** Get buyer info for an order.

**Rate Limit:** Burst: 20, Restore: 2/sec

**Business Use:** Sales velocity tracking, revenue analysis, SKU performance, return rate monitoring, delivery speed analysis, geographic distribution of orders.

---

## 4. Product Fees API v0

**Role Required:** Pricing
**Use Case:** Estimate Amazon fees before setting prices. Critical for profitability calculations.

### GET /products/fees/v0/items/{asin}/feesEstimate

**Description:** Get estimated fees for an item. (Actually uses POST for the request body)

### POST /products/fees/v0/items/{asin}/feesEstimate

**Description:** Get fee estimate for an ASIN.

| Parameter | Location | Required | Type | Description |
|-----------|----------|----------|------|-------------|
| `asin` | path | Yes | string | The ASIN |

**Request Body:**
```json
{
  "FeesEstimateRequest": {
    "MarketplaceId": "A21TJRUUN4KGV",
    "PriceToEstimateFees": {
      "ListingPrice": { "CurrencyCode": "INR", "Amount": 399.00 },
      "Shipping": { "CurrencyCode": "INR", "Amount": 0.00 }
    },
    "Identifier": "request-001",
    "IsAmazonFulfilled": true,
    "OptionalFulfillmentProgram": "FBA_CORE"
  }
}
```

**Rate Limit:** Burst: 10, Restore: 10/sec

**Response Key Fields:**
```json
{
  "payload": {
    "FeesEstimateResult": {
      "Status": "Success",
      "FeesEstimateIdentifier": {
        "MarketplaceId": "A21TJRUUN4KGV",
        "IdType": "ASIN",
        "IdValue": "B0XXXXXXXX",
        "IsAmazonFulfilled": true,
        "PriceToEstimateFees": { ... },
        "SellerInputIdentifier": "request-001"
      },
      "FeesEstimate": {
        "TotalFeesEstimate": { "CurrencyCode": "INR", "Amount": 95.00 },
        "TimeOfFeesEstimation": "2026-04-13T...",
        "FeeDetailList": [
          {
            "FeeType": "ReferralFee",
            "FeeAmount": { "CurrencyCode": "INR", "Amount": 40.00 },
            "FeePromotion": { ... },
            "TaxAmount": { ... },
            "FinalFee": { "CurrencyCode": "INR", "Amount": 40.00 }
          },
          {
            "FeeType": "FBAFees",
            "FeeAmount": { "CurrencyCode": "INR", "Amount": 45.00 },
            "FinalFee": { ... }
          },
          {
            "FeeType": "ClosingFee",
            "FeeAmount": { "CurrencyCode": "INR", "Amount": 10.00 },
            "FinalFee": { ... }
          }
        ]
      }
    }
  }
}
```

### POST /products/fees/v0/feesEstimate

**Description:** Batch fee estimate for multiple items (up to 20).

**Request Body:**
```json
[
  {
    "FeesEstimateRequest": {
      "MarketplaceId": "A21TJRUUN4KGV",
      "IdType": "ASIN",
      "IdValue": "B0XXXXXXXX",
      "PriceToEstimateFees": { ... },
      "Identifier": "request-001",
      "IsAmazonFulfilled": true
    }
  }
]
```

**Rate Limit:** Burst: 1, Restore: 1/sec

**Fee Types Returned:**
- `ReferralFee` - Amazon's commission (varies by category, typically 5-15% in India)
- `FBAFees` - Fulfillment by Amazon fees (pick, pack, ship)
- `ClosingFee` - Fixed closing fee (INR 4-61 depending on category/price)
- `VariableClosingFee` - Additional closing fees
- `GiftwrapChargeFee` - If gift wrap offered
- `ShippingChargeFee` - Shipping fee component

**Business Use:** Calculate net profit per product, determine minimum selling price, compare FBA vs self-fulfillment costs, automate pricing to maintain target margins.

---

## 5. Reports API v2021-06-30

**Role Required:** Multiple (depends on report type)
**Use Case:** Access bulk data reports - sales, inventory, fees, returns, traffic. Most comprehensive data source.

### POST /reports/2021-06-30/reports

**Description:** Create a report request.

**Request Body:**
```json
{
  "reportType": "GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL",
  "marketplaceIds": ["A21TJRUUN4KGV"],
  "dataStartTime": "2026-04-01T00:00:00Z",
  "dataEndTime": "2026-04-13T23:59:59Z",
  "reportOptions": {}
}
```

**Rate Limit:** Burst: 15, Restore: 1/min

### GET /reports/2021-06-30/reports/{reportId}

**Description:** Check report processing status.

**Rate Limit:** Burst: 15, Restore: 2/sec

**Response:**
```json
{
  "reportId": "...",
  "reportType": "...",
  "processingStatus": "DONE",
  "marketplaceIds": ["A21TJRUUN4KGV"],
  "reportDocumentId": "amzn1.spdoc.1.4.na.xxx",
  "dataStartTime": "...",
  "dataEndTime": "...",
  "createdTime": "...",
  "processingStartTime": "...",
  "processingEndTime": "..."
}
```

**processingStatus values:** `CANCELLED`, `DONE`, `FATAL`, `IN_PROGRESS`, `IN_QUEUE`

### GET /reports/2021-06-30/documents/{reportDocumentId}

**Description:** Get download URL for completed report.

**Rate Limit:** Burst: 15, Restore: 2/sec

**Response:**
```json
{
  "reportDocumentId": "...",
  "url": "https://tortuga-prod-eu.s3-eu-west-1.amazonaws.com/...",
  "compressionAlgorithm": "GZIP"
}
```
Download the URL (valid for 5 min), decompress GZIP, parse TSV/CSV/JSON.

### GET /reports/2021-06-30/reports

**Description:** Get list of reports (with filters).

| Parameter | Location | Required | Type | Description |
|-----------|----------|----------|------|-------------|
| `reportTypes` | query | No | string[] | Filter by report type |
| `processingStatuses` | query | No | string[] | `IN_QUEUE`, `IN_PROGRESS`, `DONE`, `CANCELLED`, `FATAL` |
| `marketplaceIds` | query | No | string[] | `A21TJRUUN4KGV` |
| `pageSize` | query | No | integer | 1-100, default 10 |
| `createdSince` | query | No | string | ISO 8601 |
| `createdUntil` | query | No | string | ISO 8601 |
| `nextToken` | query | No | string | Pagination |

**Rate Limit:** Burst: 15, Restore: 2/sec

### GET /reports/2021-06-30/schedules

**Description:** List scheduled report configurations.

**Rate Limit:** Burst: 15, Restore: 2/sec

### Key Report Types for Our Business:

| Report Type | Description | Data Format |
|------------|-------------|-------------|
| `GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL` | All orders by date | TSV |
| `GET_FLAT_FILE_ORDERS_DATA` | Unshipped orders | TSV |
| `GET_MERCHANT_LISTINGS_ALL_DATA` | All active listings | TSV |
| `GET_MERCHANT_LISTINGS_DATA` | Active listings summary | TSV |
| `GET_MERCHANT_LISTINGS_INACTIVE_DATA` | Inactive listings | TSV |
| `GET_AFN_INVENTORY_DATA` | FBA inventory levels | TSV |
| `GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA` | FBA inventory (detailed) | TSV |
| `GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA` | FBA fee estimates per product | TSV |
| `GET_FBA_REIMBURSEMENTS_DATA` | FBA reimbursements | TSV |
| `GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA` | FBA returns | TSV |
| `GET_FBA_FULFILLMENT_REMOVAL_ORDER_DETAIL_DATA` | FBA removal orders | TSV |
| `GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE` | Returns data | TSV |
| `GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE` | Settlement (payment) | TSV |
| `GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2` | Settlement v2 | TSV |
| `GET_SALES_AND_TRAFFIC_REPORT` | Sales & traffic (ASIN level) | JSON |
| `GET_BRAND_ANALYTICS_SEARCH_TERMS_REPORT` | Search term analytics | JSON |
| `GET_BRAND_ANALYTICS_MARKET_BASKET_REPORT` | Market basket analysis | JSON |
| `GET_BRAND_ANALYTICS_REPEAT_PURCHASE_REPORT` | Repeat purchase behavior | JSON |
| `GET_COUPON_PERFORMANCE_REPORT` | Coupon performance | TSV |
| `GET_PROMOTION_PERFORMANCE_REPORT` | Promotion performance | TSV |

**Business Use:** Comprehensive data extraction for dashboards, profitability analysis, inventory planning, returns analysis, settlement reconciliation.

---

## 6. Notifications API v1

**Role Required:** Multiple (depends on notification type)
**Use Case:** Subscribe to real-time events instead of polling. Much more efficient.

### GET /notifications/v1/subscriptions/{notificationType}

**Description:** Get current subscription for a notification type.

| Parameter | Location | Required | Type | Description |
|-----------|----------|----------|------|-------------|
| `notificationType` | path | Yes | string | The notification type |
| `payloadVersion` | query | No | string | Version of payload |

**Rate Limit:** Burst: 5, Restore: 1/sec

### GET /notifications/v1/destinations

**Description:** List registered notification destinations (SQS, EventBridge).

**Rate Limit:** Burst: 5, Restore: 1/sec

**Response:**
```json
{
  "payload": {
    "destinations": [{
      "destinationId": "...",
      "name": "GoAmrita_Events",
      "resource": {
        "sqs": {
          "arn": "arn:aws:sqs:eu-west-1:XXXX:goamrita-sp-notifications"
        }
      }
    }]
  }
}
```

### Key Notification Types:

| Notification Type | Description | Trigger |
|------------------|-------------|---------|
| `ANY_OFFER_CHANGED` | Price/offer changes on our ASINs | Competitor price change, Buy Box change |
| `ORDER_CHANGE` | Order status changes | New order, shipped, cancelled |
| `LISTINGS_ITEM_STATUS_CHANGE` | Listing status changes | Active, inactive, suppressed |
| `LISTINGS_ITEM_ISSUES_CHANGE` | Listing quality issues | New issue, resolved issue |
| `LISTINGS_ITEM_MFN_QUANTITY_CHANGE` | MFN inventory quantity change | Stock update |
| `REPORT_PROCESSING_FINISHED` | Report is ready to download | Report done processing |
| `FEED_PROCESSING_FINISHED` | Feed processing complete | Feed done processing |
| `ACCOUNT_STATUS_CHANGED` | Seller account health | Account deactivation warning |
| `B2B_ANY_OFFER_CHANGED` | B2B offer changes | B2B price changes |
| `ITEM_PRODUCT_TYPE_CHANGE` | Product type reclassification | Amazon changes product type |
| `BRANDED_ITEM_CONTENT_CHANGE` | A+ content changes | Content update on our brand |
| `FBA_OUTBOUND_SHIPMENT_STATUS` | FBA shipment status | Shipment tracking updates |
| `ORDER_STATUS_CHANGE` | Granular order status (newer) | Detailed status transitions |

**Business Use:** Real-time alerts for price wars, order monitoring, listing health, inventory alerts. Eliminates need for constant polling.

---

## 7. Brand Analytics (via Reports API)

**Role Required:** Brand Analytics
**Use Case:** Search term data, market basket analysis, repeat purchase insights. Only for brand-registered sellers.

### Search Terms Report
**Report Type:** `GET_BRAND_ANALYTICS_SEARCH_TERMS_REPORT`

**Create via POST /reports/2021-06-30/reports:**
```json
{
  "reportType": "GET_BRAND_ANALYTICS_SEARCH_TERMS_REPORT",
  "marketplaceIds": ["A21TJRUUN4KGV"],
  "dataStartTime": "2026-04-07T00:00:00Z",
  "dataEndTime": "2026-04-13T23:59:59Z",
  "reportOptions": {
    "reportPeriod": "WEEK"
  }
}
```

**reportPeriod options:** `DAY`, `WEEK`, `MONTH`, `QUARTER`

**Response Data (JSON):**
```json
{
  "dataByDepartmentAndSearchTerm": [{
    "departmentName": "All Departments",
    "searchTerm": "organic ghee",
    "searchFrequencyRank": 1234,
    "clickedAsin1": "B0XXXXXXXX",
    "clickShareRank1": 15.5,
    "conversionShareRank1": 12.3,
    "clickedAsin2": "B0YYYYYYYY",
    "clickShareRank2": 10.2,
    "conversionShareRank2": 8.5,
    "clickedAsin3": "B0ZZZZZZZZ",
    "clickShareRank3": 7.8,
    "conversionShareRank3": 6.1
  }]
}
```

### Market Basket Report
**Report Type:** `GET_BRAND_ANALYTICS_MARKET_BASKET_REPORT`

Shows what other products customers buy with your products. Useful for bundling strategies.

### Repeat Purchase Report
**Report Type:** `GET_BRAND_ANALYTICS_REPEAT_PURCHASE_REPORT`

Shows repeat purchase behavior for your brand ASINs. Useful for customer loyalty analysis.

**Business Use:** Keyword research, competitor ASIN analysis, search volume trends, cross-sell opportunities, customer loyalty metrics.

---

## 8. Sales & Traffic Report (via Reports API)

**Role Required:** Selling Partner Insights
**Use Case:** ASIN-level sessions, page views, conversion rate, units ordered. Essential for performance dashboards.

**Report Type:** `GET_SALES_AND_TRAFFIC_REPORT`

**Create Request:**
```json
{
  "reportType": "GET_SALES_AND_TRAFFIC_REPORT",
  "marketplaceIds": ["A21TJRUUN4KGV"],
  "dataStartTime": "2026-04-01T00:00:00Z",
  "dataEndTime": "2026-04-13T23:59:59Z",
  "reportOptions": {
    "dateGranularity": "DAY",
    "asinGranularity": "CHILD"
  }
}
```

**dateGranularity:** `DAY`, `WEEK`, `MONTH`
**asinGranularity:** `PARENT`, `CHILD`, `SKU`

**Response Data (JSON):**
```json
{
  "salesAndTrafficByAsin": [{
    "parentAsin": "B0XXXXXXXX",
    "childAsin": "B0XXXXXXXX",
    "sku": "SKU-001",
    "trafficByAsin": {
      "browserSessions": 150,
      "browserSessionsB2B": 5,
      "mobileAppSessions": 200,
      "mobileAppSessionsB2B": 2,
      "sessions": 350,
      "sessionsB2B": 7,
      "browserSessionPercentage": 0.42,
      "mobileAppSessionPercentage": 0.58,
      "sessionPercentage": 0.001,
      "browserPageViews": 180,
      "mobileAppPageViews": 250,
      "pageViews": 430,
      "pageViewsPercentage": 0.0012,
      "buyBoxPercentage": 95.0,
      "unitSessionPercentage": 8.5
    },
    "salesByAsin": {
      "unitsOrdered": 30,
      "unitsOrderedB2B": 2,
      "orderedProductSales": { "amount": 8970.00, "currencyCode": "INR" },
      "orderedProductSalesB2B": { "amount": 598.00, "currencyCode": "INR" },
      "totalOrderItems": 28,
      "totalOrderItemsB2B": 1
    }
  }],
  "salesAndTrafficByDate": [{
    "date": "2026-04-12",
    "salesByDate": {
      "orderedProductSales": { "amount": 2500.00, "currencyCode": "INR" },
      "unitsOrdered": 8,
      "totalOrderItems": 7,
      "averageSalesPerOrderItem": { "amount": 357.14, "currencyCode": "INR" },
      "averageUnitsPerOrderItem": 1.14,
      "averageSellingPrice": { "amount": 312.50, "currencyCode": "INR" },
      "unitsRefunded": 0,
      "refundRate": 0,
      "claimsGranted": 0,
      "claimsAmount": { "amount": 0, "currencyCode": "INR" },
      "shippedProductSales": { "amount": 2200.00, "currencyCode": "INR" },
      "unitsShipped": 7,
      "ordersShipped": 6
    },
    "trafficByDate": {
      "browserPageViews": 1200,
      "mobileAppPageViews": 1800,
      "pageViews": 3000,
      "browserSessions": 900,
      "mobileAppSessions": 1400,
      "sessions": 2300,
      "buyBoxPercentage": 92.5,
      "orderItemSessionPercentage": 3.5,
      "unitSessionPercentage": 4.2,
      "averageOfferCount": 1.5,
      "averageParentItems": 25,
      "feedbackReceived": 1,
      "negativeFeedbackReceived": 0,
      "receivedNegativeFeedbackRate": 0
    }
  }]
}
```

**Business Use:** Daily KPI dashboard, conversion rate optimization, session/traffic trends, Buy Box %, refund rate tracking, mobile vs desktop analysis.

---

## 9. Product Reviews / Customer Feedback

**Note:** As of 2025-2026, Amazon does NOT have a general public "Customer Feedback API v2024-06-01" in SP-API for reading product reviews programmatically. Review data is available through:

### Option A: Seller Feedback (Account-level)
Available in settlement reports and through Seller Central. Not a direct API endpoint.

### Option B: Product Reviews via Reports
**Report Type:** Not directly available as a standard report type. Product reviews are not exposed via SP-API.

### Option C: Seller Central Scraping (Not Recommended)
Reviews are visible in Seller Central but not via official API.

### What IS Available:
- **Buyer-Seller Messaging API** (`/messaging/v1/orders/{amazonOrderId}/messages`) - For direct buyer communication
- **Solicitations API** (`GET /solicitations/v1/orders/{amazonOrderId}/productReviewAndSellerFeedback`) - Check if you can request review from buyer

### GET /solicitations/v1/orders/{amazonOrderId}/productReviewAndSellerFeedback

**Description:** Check eligibility and get link for requesting review.

**Rate Limit:** Burst: 1, Restore: 1/5sec

**Business Use:** Limited. Focus on Reports API for aggregate review/feedback metrics. For individual reviews, use Seller Central UI or third-party tools.

---

## 10. FBA Inventory API v1

**Role Required:** Amazon Fulfilment
**Use Case:** Track FBA inventory levels, health, inbound shipment status.

### GET /fba/inventory/v1/summaries

**Description:** Get inventory summary for FBA items.

| Parameter | Location | Required | Type | Description |
|-----------|----------|----------|------|-------------|
| `granularityType` | query | Yes | string | `Marketplace` |
| `granularityId` | query | Yes | string | `A21TJRUUN4KGV` |
| `marketplaceIds` | query | Yes | string[] | `A21TJRUUN4KGV` |
| `details` | query | No | boolean | Include detailed info (default false) |
| `startDateTime` | query | No | string | ISO 8601 - for changes since |
| `sellerSkus` | query | No | string[] | Filter by SKUs (max 50) |
| `sellerSku` | query | No | string | Single SKU filter |
| `nextToken` | query | No | string | Pagination |

**Rate Limit:** Burst: 2, Restore: 2/sec

**Response Key Fields:**
```json
{
  "payload": {
    "granularity": { "granularityType": "Marketplace", "granularityId": "A21TJRUUN4KGV" },
    "inventorySummaries": [{
      "asin": "B0XXXXXXXX",
      "fnSku": "X001XXXXXX",
      "sellerSku": "SKU-001",
      "condition": "NewItem",
      "inventoryDetails": {
        "fulfillableQuantity": 45,
        "inboundWorkingQuantity": 0,
        "inboundShippedQuantity": 20,
        "inboundReceivingQuantity": 0,
        "totalReservedQuantity": 3,
        "pendingCustomerOrderQuantity": 2,
        "pendingTransshipmentQuantity": 1,
        "fcProcessingQuantity": 0,
        "totalResearchingQuantity": 0,
        "researchingQuantityBreakdown": [],
        "totalUnfulfillableQuantity": 0,
        "customerDamagedQuantity": 0,
        "warehouseDamagedQuantity": 0,
        "distributorDamagedQuantity": 0,
        "carrierDamagedQuantity": 0,
        "defectiveQuantity": 0,
        "expiredQuantity": 0
      },
      "lastUpdatedTime": "2026-04-13T..."
    }]
  }
}
```

### FBA Inventory Reports (via Reports API)

| Report Type | Description |
|------------|-------------|
| `GET_AFN_INVENTORY_DATA` | Basic FBA inventory |
| `GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA` | Detailed FBA inventory |
| `GET_FBA_MYI_ALL_INVENTORY_DATA` | All FBA inventory (incl. suppressed) |
| `GET_FBA_INVENTORY_AGED_DATA` | Inventory age (for long-term storage fees) |
| `GET_FBA_INVENTORY_PLANNING_DATA` | Inventory planning data |
| `GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT` | Restock recommendations |
| `GET_FBA_STORAGE_FEE_CHARGES_DATA` | Storage fee charges |

**Business Use:** Stock monitoring, reorder point alerts, stranded/unfulfillable inventory detection, storage fee optimization, inbound shipment tracking.

---

## 11. Sellers API v1 (Bonus - Marketplace Verification)

**Role Required:** Any
**Use Case:** Verify seller participation in marketplaces. Good health check endpoint.

### GET /sellers/v1/marketplaceParticipations

**Description:** List marketplaces the seller participates in.

**Rate Limit:** Burst: 15, Restore: 1/sec

**Response:**
```json
{
  "payload": [{
    "marketplace": {
      "id": "A21TJRUUN4KGV",
      "name": "Amazon.in",
      "countryCode": "IN",
      "defaultCurrencyCode": "INR",
      "defaultLanguageCode": "en_IN",
      "domainName": "www.amazon.in"
    },
    "participation": {
      "isParticipating": true,
      "hasSuspendedListings": false
    }
  }]
}
```

**Business Use:** System health check, confirm marketplace access, detect account suspensions early.

---

## Quick Reference: Rate Limits Summary

| API | Endpoint | Burst | Restore |
|-----|----------|-------|---------|
| Catalog Items | GET /catalog/2022-04-01/items/{asin} | 2 | 2/sec |
| Catalog Items | GET /catalog/2022-04-01/items (search) | 2 | 2/sec |
| Pricing | POST batches/competitiveSummary | 1 | 1/5sec |
| Pricing v0 | GET /products/pricing/v0/price | 10 | 10/sec |
| Orders | GET /orders/v0/orders | 20 | 2/sec |
| Orders | GET /orders/v0/orders/{id}/orderItems | 20 | 2/sec |
| Product Fees | POST /feesEstimate (single) | 10 | 10/sec |
| Product Fees | POST /feesEstimate (batch) | 1 | 1/sec |
| Reports | POST (create report) | 15 | 1/min |
| Reports | GET (check status) | 15 | 2/sec |
| Reports | GET (get document) | 15 | 2/sec |
| Notifications | GET subscriptions | 5 | 1/sec |
| FBA Inventory | GET /fba/inventory/v1/summaries | 2 | 2/sec |
| Sellers | GET /marketplaceParticipations | 15 | 1/sec |

---

## Error Codes Reference

| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| 200 | Success | Process response |
| 400 | Bad Request | Check parameters |
| 401 | Unauthorized | Refresh LWA access token |
| 403 | Forbidden | Check role permissions, endpoint region |
| 404 | Not Found | Check ASIN/OrderId exists |
| 429 | Too Many Requests | Implement backoff, check rate limits |
| 500 | Internal Server Error | Retry with exponential backoff |
| 503 | Service Unavailable | Retry after delay |

**Standard Error Response:**
```json
{
  "errors": [{
    "code": "InvalidInput",
    "message": "Detailed error message",
    "details": "Additional context"
  }]
}
```

---

## Implementation Priority for GoAmrita Bhandar

| Priority | API | Why |
|----------|-----|-----|
| 1 | Orders API | Sales velocity, revenue tracking |
| 2 | Pricing API v2022-05-01 | Buy Box monitoring, competitive intel |
| 3 | Reports API (Sales & Traffic) | KPI dashboard data |
| 4 | FBA Inventory API | Stock level monitoring |
| 5 | Catalog Items API | Product detail enrichment |
| 6 | Product Fees API | Profitability calculations |
| 7 | Reports API (Brand Analytics) | Search term & market insights |
| 8 | Notifications API | Real-time event alerts |
| 9 | Sellers API | Health checks |

---

*Document Version: 1.0 | Created: 13 April 2026*
*Source: Amazon SP-API Official Documentation (developer-docs.amazon.com/sp-api)*
*Note: Always verify against latest official docs before implementation. API versions and rate limits may change.*
