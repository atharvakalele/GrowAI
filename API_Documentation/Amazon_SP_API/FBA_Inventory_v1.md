# Selling Partner API for FBA Inventory v1
## Official OpenAPI Spec Documentation
**Source:** https://github.com/amzn/selling-partner-api-models/blob/main/models/fba-inventory-api-model/fbaInventory.json
**Fetched:** 2026-04-13
**Spec Version:** Swagger 2.0
**API Version:** v1

---

## API Info
- **Title:** Selling Partner API for FBA Inventory
- **Description:** Programmatically retrieve information about inventory in Amazon's fulfillment network.
- **Host:** sellingpartnerapi-na.amazon.com (use `sellingpartnerapi-eu.amazon.com` for India/EU)
- **Schemes:** HTTPS
- **Consumes:** application/json
- **Produces:** application/json
- **License:** Apache License 2.0

---

## Endpoints

### 1. GET /fba/inventory/v1/summaries
**Operation:** getInventorySummaries
**Description:** Returns a list of inventory summaries with optional details.

**Parameters:**
| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| details | query | boolean | No | Default: `false`. Set `true` to return additional summarized inventory details and quantities. |
| granularityType | query | string | Yes | Enum: `Marketplace`. Granularity type for aggregation. |
| granularityId | query | string | Yes | Granularity ID (marketplace ID when granularityType is Marketplace) |
| startDateTime | query | string (date-time) | No | ISO 8601 date-time. Returns summaries changed since this time. Must not be earlier than 18 months prior. |
| sellerSkus | query | array[string] | No | List of seller SKUs (max 50) |
| sellerSku | query | string | No | Single seller SKU |
| nextToken | query | string | No | Pagination token (expires 30 seconds after creation) |
| marketplaceIds | query | array[string] (max 1) | Yes | Marketplace ID |

**Responses:**
| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Success | GetInventorySummariesResponse |
| 400 | Invalid parameters | GetInventorySummariesResponse (with errors) |
| 403 | Access forbidden | GetInventorySummariesResponse (with errors) |
| 404 | Resource not found | GetInventorySummariesResponse (with errors) |
| 429 | Rate limit exceeded | GetInventorySummariesResponse (with errors) |
| 500 | Server error | GetInventorySummariesResponse (with errors) |
| 503 | Service unavailable | GetInventorySummariesResponse (with errors) |

**Response Headers:**
- `x-amzn-RateLimit-Limit` (string): Rate limit for operation
- `x-amzn-RequestId` (string): Unique request reference ID

**Rate Limit:** 2 requests/sec, Burst: 2

---

### 2. POST /fba/inventory/v1/items
**Operation:** createInventoryItem
**Description:** Creates an inventory item (Sandbox only).

**Parameters:**
| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| body | body | CreateInventoryItemRequest | Yes | Item creation payload |

**Responses:** CreateInventoryItemResponse with same status codes

---

### 3. DELETE /fba/inventory/v1/items/{sellerSku}
**Operation:** deleteInventoryItem
**Description:** Deletes an inventory item (Sandbox only).

**Parameters:**
| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| sellerSku | path | string | Yes | Seller SKU to delete |
| marketplaceId | query | string | Yes | Marketplace ID |

**Responses:** DeleteInventoryItemResponse with same status codes

---

### 4. POST /fba/inventory/v1/items/inventory
**Operation:** addInventory
**Description:** Adds inventory (Sandbox only).

**Parameters:**
| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| x-amzn-idempotency-token | header | string | Yes | Unique idempotency token |
| body | body | AddInventoryRequest | Yes | Inventory to add |

**Responses:** AddInventoryResponse with same status codes

---

## Data Models

### GetInventorySummariesResponse
| Property | Type | Description |
|----------|------|-------------|
| payload | GetInventorySummariesResult | Inventory summaries data |
| pagination | Pagination | Pagination info |
| errors | ErrorList | Error details |

### GetInventorySummariesResult
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| granularity | Granularity | Yes | Aggregation level info |
| inventorySummaries | array[InventorySummary] | Yes | List of inventory summaries |

### Granularity
| Property | Type | Description |
|----------|------|-------------|
| granularityType | string | Aggregation type (e.g., "Marketplace") |
| granularityId | string | Granularity ID (marketplace ID) |

### InventorySummary
| Property | Type | Description |
|----------|------|-------------|
| asin | string | Amazon Standard Identification Number |
| fnSku | string | Amazon's fulfillment network SKU identifier |
| sellerSku | string | Seller SKU |
| condition | string | Item condition (e.g., "New Item") |
| inventoryDetails | InventoryDetails | Detailed inventory breakdown (when details=true) |
| lastUpdatedTime | string (date-time) | Last quantity update timestamp |
| productName | string | Localized product title |
| totalQuantity | integer | Total units in inbound shipment or fulfillment centers |
| stores | array[string] | Seller-enrolled stores for this SKU |

### InventoryDetails
| Property | Type | Description |
|----------|------|-------------|
| fulfillableQuantity | integer | Quantity that can be picked, packed, and shipped |
| inboundWorkingQuantity | integer | Units in inbound shipment (notified Amazon) |
| inboundShippedQuantity | integer | Units in inbound shipment (tracking provided) |
| inboundReceivingQuantity | integer | Units not yet received but part of started inbound shipment |
| reservedQuantity | ReservedQuantity | Reserved inventory breakdown |
| researchingQuantity | ResearchingQuantity | Misplaced/damaged units being confirmed |
| unfulfillableQuantity | UnfulfillableQuantity | Unsellable inventory breakdown |

### ReservedQuantity
| Property | Type | Description |
|----------|------|-------------|
| totalReservedQuantity | integer | Total units being picked/packed/shipped or sidelined |
| pendingCustomerOrderQuantity | integer | Units reserved for customer orders |
| pendingTransshipmentQuantity | integer | Units being transferred between FCs |
| fcProcessingQuantity | integer | Units sidelined for additional processing |

### ResearchingQuantity
| Property | Type | Description |
|----------|------|-------------|
| totalResearchingQuantity | integer | Total units currently being researched |
| researchingQuantityBreakdown | array[ResearchingQuantityEntry] | Breakdown by duration |

### ResearchingQuantityEntry
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| name | string | Yes | Enum: `researchingQuantityInShortTerm`, `researchingQuantityInMidTerm`, `researchingQuantityInLongTerm` |
| quantity | integer | Yes | Number of units |

### UnfulfillableQuantity
| Property | Type | Description |
|----------|------|-------------|
| totalUnfulfillableQuantity | integer | Total unsellable units |
| customerDamagedQuantity | integer | Customer damaged |
| warehouseDamagedQuantity | integer | Warehouse damaged |
| distributorDamagedQuantity | integer | Distributor damaged |
| carrierDamagedQuantity | integer | Carrier damaged |
| defectiveQuantity | integer | Defective |
| expiredQuantity | integer | Expired |

### CreateInventoryItemRequest (Sandbox only)
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| sellerSku | string | Yes | Seller SKU |
| marketplaceId | string | Yes | Marketplace ID |
| productName | string | Yes | Item name |

### AddInventoryRequest (Sandbox only)
| Property | Type | Description |
|----------|------|-------------|
| inventoryItems | array[InventoryItem] | List of items to add |

### InventoryItem (Sandbox only)
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| sellerSku | string | Yes | Seller SKU |
| marketplaceId | string | Yes | Marketplace ID |
| quantity | integer | Yes | Quantity to add |

### Pagination
| Property | Type | Description |
|----------|------|-------------|
| nextToken | string | Token for next page (expires 30 seconds after creation) |

### Error
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| code | string | Yes | Error code |
| message | string | No | Human-readable description |
| details | string | No | Additional context |

---

## Rate Limits
| Operation | Rate | Burst |
|-----------|------|-------|
| getInventorySummaries | 2 req/sec | 2 |
| createInventoryItem | 5 req/sec | 10 |
| deleteInventoryItem | 5 req/sec | 10 |
| addInventory | 5 req/sec | 10 |

---

## Important Notes for GoAmrita Bhandar
- **Region:** India = EU endpoint (`sellingpartnerapi-eu.amazon.com`)
- **Marketplace ID for India:** A21TJRUUN4KGV
- **Primary endpoint:** `getInventorySummaries` -- the only production endpoint. Others are Sandbox-only.
- Always set `details=true` to get full inventory breakdown (fulfillable, reserved, unfulfillable)
- `granularityType` must be `Marketplace` and `granularityId` must be the marketplace ID
- `nextToken` expires after 30 seconds -- process pagination quickly
- Max 50 SKUs per request when using `sellerSkus` parameter
- `startDateTime` cannot go back more than 18 months
