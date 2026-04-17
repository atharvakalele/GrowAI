---
## FALLBACK / OLD VERSION
**WARNING:** This file contains v0 API content. Our pinned version is v2026-01-01 which was not available on GitHub at extraction time.
**Our Primary Version:** Orders v2026-01-01
**This File's Version:** v0 (alternate extraction format)
**Note:** Use this as reference when v2026-01-01 docs are unavailable. Also see `Orders_v2026-01-01.md` for the more detailed v0 reference.
---

# Amazon SP-API - Orders API v0 - Official Reference
# Source: GitHub amzn/selling-partner-api-models/ordersV0.json
# Extracted: 2026-04-13

## API Overview
- **Title:** Selling Partner API for Orders
- **Version:** v0
- **Host:** sellingpartnerapi-na.amazon.com (NA) / sellingpartnerapi-eu.amazon.com (EU/India)
- **Schemes:** HTTPS
- **Content Types:** application/json
- **Authentication:** AWS Signature Version 4

---

## Endpoints

### 1. GET /orders/v0/orders
**Description:** Returns orders created or updated during the specified time period
**Status:** Deprecated (use newer version when available)
**Rate Limit:** 0.0167 requests/second, burst 20

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| CreatedAfter | string (ISO 8601) | No | Start of creation date range |
| CreatedBefore | string (ISO 8601) | No | End of creation date range |
| LastUpdatedAfter | string (ISO 8601) | No | Start of update date range |
| LastUpdatedBefore | string (ISO 8601) | No | End of update date range |
| OrderStatuses | array[string] | No | Filter by order status |
| MarketplaceIds | array[string] | **Yes** | Max 50 items |
| FulfillmentChannels | array[string] | No | AFN or MFN |
| PaymentMethods | array[string] | No | COD, CVS, Other |
| SellerOrderId | string | No | Seller-defined order ID |
| MaxResultsPerPage | integer | No | Range 1-100, default 100 |
| EasyShipShipmentStatuses | array[string] | No | 16 possible values |
| ElectronicInvoiceStatuses | array[string] | No | See enum below |
| NextToken | string | No | Pagination token |
| AmazonOrderIds | array[string] | No | Max 50 items |
| ActualFulfillmentSupplySourceId | string | No | Supply source filter |
| IsISPU | boolean | No | In-Store Pickup filter |
| StoreChainStoreId | string | No | Store chain filter |
| EarliestDeliveryDateBefore | string (ISO 8601) | No | Delivery date filter |
| EarliestDeliveryDateAfter | string (ISO 8601) | No | Delivery date filter |
| LatestDeliveryDateBefore | string (ISO 8601) | No | Delivery date filter |
| LatestDeliveryDateAfter | string (ISO 8601) | No | Delivery date filter |

**OrderStatuses Enum:**
- PendingAvailability
- Pending
- Unshipped
- PartiallyShipped
- Shipped
- InvoiceUnconfirmed
- Canceled
- Unfulfillable

**ElectronicInvoiceStatuses Enum:**
- NotRequired
- NotFound
- Processing
- Errored
- Accepted

**Responses:**
- 200: GetOrdersResponse (payload with NextToken, Orders array)
- 400: Invalid parameters
- 403: Access forbidden
- 404: Resource not found
- 429: Rate limit exceeded
- 500: Server error
- 503: Service unavailable

---

### 2. GET /orders/v0/orders/{orderId}
**Description:** Returns the specified order
**Status:** Deprecated
**Rate Limit:** 0.5 requests/second, burst 30

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| orderId | string | **Yes** | Amazon order ID (3-7-7 format) |

**Responses:** 200, 400, 403, 404, 429, 500, 503

---

### 3. GET /orders/v0/orders/{orderId}/buyerInfo
**Description:** Returns buyer information for the specified order
**Status:** Deprecated
**Rate Limit:** 0.5 requests/second, burst 30

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| orderId | string | **Yes** | Amazon order ID (3-7-7 format) |

**Responses:** 200: GetOrderBuyerInfoResponse, 400, 403, 404, 429, 500, 503

---

### 4. GET /orders/v0/orders/{orderId}/address
**Description:** Returns the shipping address for the specified order
**Status:** Deprecated
**Rate Limit:** 0.5 requests/second, burst 30

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| orderId | string | **Yes** | Amazon order ID (3-7-7 format) |

**Responses:** 200: GetOrderAddressResponse, 400, 403, 404, 429, 500, 503

---

### 5. GET /orders/v0/orders/{orderId}/orderItems
**Description:** Returns detailed order item information
**Status:** Deprecated
**Rate Limit:** 0.5 requests/second, burst 30

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| orderId | string | **Yes** | Amazon order ID (3-7-7 format) |

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| NextToken | string | No | Pagination token |

**Responses:** 200: GetOrderItemsResponse, 400, 403, 404, 429, 500, 503

---

### 6. GET /orders/v0/orders/{orderId}/orderItems/buyerInfo
**Description:** Returns buyer information for order items
**Status:** Deprecated
**Rate Limit:** 0.5 requests/second, burst 30

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| orderId | string | **Yes** | Amazon order ID (3-7-7 format) |

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| NextToken | string | No | Pagination token |

**Responses:** 200: GetOrderItemsBuyerInfoResponse, 400, 403, 404, 429, 500, 503

---

### 7. POST /orders/v0/orders/{orderId}/shipment
**Description:** Update the shipment status for an order
**Rate Limit:** 5 requests/second, burst 15

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| orderId | string | **Yes** | Amazon order ID (3-7-7 format) |

**Request Body:** UpdateShipmentStatusRequest

**Responses:**
- 204: Success (no content)
- 400: UpdateShipmentStatusErrorResponse
- 403, 404, 413, 415, 429, 500, 503

---

### 8. GET /orders/v0/orders/{orderId}/regulatedInfo
**Description:** Returns regulated information for the specified order
**Rate Limit:** 0.5 requests/second, burst 30

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| orderId | string | **Yes** | Amazon order ID (3-7-7 format) |

**Responses:** 200: GetOrderRegulatedInfoResponse, 400, 403, 404, 429, 500, 503

---

### 9. PATCH /orders/v0/orders/{orderId}/verificationStatus
**Description:** Update order verification status

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| orderId | string | **Yes** | Amazon order ID (3-7-7 format) |

---

### 10. POST /orders/v0/orders/{orderId}/confirmShipment
**Description:** Confirm shipment for an order

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| orderId | string | **Yes** | Amazon order ID (3-7-7 format) |

---

## Data Models

### Order
| Field | Type | Description |
|-------|------|-------------|
| AmazonOrderId | string | Amazon order identifier |
| PurchaseDate | string (ISO 8601) | Purchase timestamp |
| LastUpdateDate | string (ISO 8601) | Last update timestamp |
| OrderStatus | string | See OrderStatuses enum |
| FulfillmentChannel | string | AFN or MFN |
| SalesChannel | string | Sales channel |
| ShipServiceLevel | string | Shipping service level |
| OrderTotal | Money | Total order amount |
| NumberOfItemsShipped | integer | Items shipped count |
| NumberOfItemsUnshipped | integer | Items unshipped count |
| PaymentMethod | string | Payment method |
| PaymentMethodDetails | array[string] | Payment method details |
| PaymentExecutionDetail | array | Payment execution details |
| IsReplacementOrder | boolean | Replacement order flag |
| MarketplaceId | string | Marketplace identifier |
| ShipmentServiceLevelCategory | string | Shipment service category |
| OrderType | string | Order type |
| EarliestShipDate | string (ISO 8601) | Earliest ship date |
| LatestShipDate | string (ISO 8601) | Latest ship date |
| EarliestDeliveryDate | string (ISO 8601) | Earliest delivery date |
| LatestDeliveryDate | string (ISO 8601) | Latest delivery date |
| IsBusinessOrder | boolean | Business order flag |
| IsPrime | boolean | Prime order flag |
| IsGlobalExpressEnabled | boolean | Global Express flag |
| IsPremiumOrder | boolean | Premium order flag |
| IsSoldByAB | boolean | Sold by Amazon Business flag |
| IsIBA | boolean | IBA flag |
| IsAccessPointOrder | boolean | Access point order flag |
| DefaultShipFromLocationAddress | Address | Default ship-from address |
| FulfillmentInstruction | object | Contains FulfillmentSupplySourceId |
| IsISPU | boolean | In-Store Pickup flag |
| AutomatedShippingSettings | object | Automated shipping settings |
| EasyShipShipmentStatus | string | Easy Ship status |
| ElectronicInvoiceStatus | string | Electronic invoice status |
| ShippingAddress | Address | Shipping address |
| BuyerInfo | BuyerInfo | Buyer information |

### Address
| Field | Type | Description |
|-------|------|-------------|
| Name | string | Recipient name |
| AddressLine1 | string | Address line 1 |
| AddressLine2 | string | Address line 2 (optional) |
| City | string | City |
| StateOrRegion | string | State/region |
| PostalCode | string | Postal code |
| CountryCode | string | Country code |
| Phone | string | Phone number (optional) |
| AddressType | string | Address type (optional) |

### OrderItem
| Field | Type | Description |
|-------|------|-------------|
| ASIN | string | Amazon Standard ID |
| OrderItemId | string | Order item identifier |
| SellerSKU | string | Seller SKU |
| Title | string | Item title |
| QuantityOrdered | integer | Quantity ordered |
| QuantityShipped | integer | Quantity shipped |
| ProductInfo | object | Product information |
| PointsGranted | object | Points granted |
| ItemPrice | Money | Item price |
| ItemTax | Money | Item tax |
| ShippingPrice | Money | Shipping price |
| ShippingTax | Money | Shipping tax (optional) |
| ScheduledDeliveryStartDate | string (ISO 8601) | Scheduled delivery start |
| ScheduledDeliveryEndDate | string (ISO 8601) | Scheduled delivery end |
| CODFee | Money | Cash on delivery fee |
| CODFeeDiscount | Money | COD fee discount |
| PriceDesignation | string | Price designation |
| BuyerInfo | object | Buyer info (CustomizedInfo, GiftMessageText, GiftWrapPrice, GiftWrapLevel) |
| BuyerRequestedCancel | object | Cancel request (IsBuyerRequestedCancel, BuyerCancelReason) |
| SerialNumbers | array[string] | Serial numbers |
| PromotionIds | array | Promotion IDs |
| ConditionId | string | Item condition ID |
| ConditionSubtypeId | string | Condition subtype |
| ConditionNote | string | Condition note |
| IsGift | boolean | Gift flag |
| IsTransparency | boolean | Transparency flag |
| SerialNumberRequired | boolean | Serial number required flag |
| IossNumber | string | IOSS number |
| DeemedResellerCategory | string | Deemed reseller category |
| StoreChainStoreId | string | Store chain store ID |
| PromotionDiscount | Money | Promotion discount |

### Money
| Field | Type | Description |
|-------|------|-------------|
| CurrencyCode | string | ISO 4217 currency code |
| Amount | string | Monetary amount |

### BuyerInfo
| Field | Type | Description |
|-------|------|-------------|
| BuyerName | string | Buyer name |
| BuyerTaxInfo | object | Tax info (CompanyLegalName) |
| PurchaseOrderNumber | string | PO number |

### RegulatedOrderVerificationStatus
| Field | Type | Description |
|-------|------|-------------|
| Status | string | Pending, Approved, Rejected |
| RequiresMerchantAction | boolean | Action required flag |
| RejectionReason | object | RejectionReasonId, RejectionReasonDescription |
| ValidRejectionReasons | array | Valid rejection reasons |
| ExternalReviewerId | string | External reviewer ID |
| ReviewDate | string (ISO 8601) | Review date |
| ValidVerificationDetails | array | Valid verification details |

### UpdateShipmentStatusRequest
| Field | Type | Description |
|-------|------|-------------|
| marketplaceId | string | Marketplace identifier |
| shipmentStatus | string | ReadyForPickup, PickedUp, etc. |

---

## Response Schemas

| Response Type | Fields |
|---------------|--------|
| GetOrdersResponse | payload (Orders array, NextToken), errors |
| GetOrderResponse | payload (single Order), errors |
| GetOrderBuyerInfoResponse | payload (AmazonOrderId, BuyerName, BuyerTaxInfo, PurchaseOrderNumber), errors |
| GetOrderAddressResponse | payload (AmazonOrderId, ShippingAddress), errors |
| GetOrderItemsResponse | payload (AmazonOrderId, OrderItems array, NextToken), errors |
| GetOrderItemsBuyerInfoResponse | payload (AmazonOrderId, OrderItems array), errors |
| GetOrderRegulatedInfoResponse | payload (AmazonOrderId, RequiresDosageLabel, RegulatedInformation, RegulatedOrderVerificationStatus), errors |
| UpdateShipmentStatusErrorResponse | errors (array with code, message, details) |

---

## Common Response Headers
| Header | Type | Description |
|--------|------|-------------|
| x-amzn-RateLimit-Limit | string | Rate limit for operation |
| x-amzn-RequestId | string | Unique request identifier |

---

## Notes for GoAmrita Bhandar
- Use EU endpoint: sellingpartnerapi-eu.amazon.com
- India Marketplace ID: A21TJRUUN4KGV
- All dates in ISO 8601 format
- v0 is marked deprecated but still functional; newer v2026-01-01 may be available
