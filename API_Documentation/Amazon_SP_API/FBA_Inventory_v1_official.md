# Amazon SP-API - FBA Inventory API v1 - Official Reference
# Source: GitHub amzn/selling-partner-api-models/fbaInventory.json
# Extracted: 2026-04-13

## API Overview
- **Title:** Selling Partner API for FBA Inventory
- **Version:** v1
- **Host:** sellingpartnerapi-eu.amazon.com (for India/EU)
- **Schemes:** HTTPS
- **Content Types:** application/json

## Endpoints

### 1. GET /fba/inventory/v1/summaries
**Operation ID:** getInventorySummaries
**Description:** Returns a list of inventory summaries
**Rate Limit:** 2 req/sec, burst 2

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| details | boolean | No | Return additional details (default: false) |
| granularityType | string | Yes | Enum: Marketplace |
| granularityId | string | Yes | ID for aggregation level |
| startDateTime | string (date-time) | No | ISO 8601, max 18 months ago |
| sellerSkus | array[string] | No | Max 50 SKUs |
| sellerSku | string | No | Single SKU query |
| nextToken | string | No | Pagination token (expires 30 seconds) |
| marketplaceIds | array[string] | Yes | Max 1 item |

**Response:** GetInventorySummariesResponse

### 2. POST /fba/inventory/v1/items (SANDBOX ONLY)
**Operation ID:** createInventoryItem
**Body:** CreateInventoryItemRequest { sellerSku, marketplaceId, productName }

### 3. DELETE /fba/inventory/v1/items/{sellerSku} (SANDBOX ONLY)
**Operation ID:** deleteInventoryItem
**Parameters:** sellerSku (path), marketplaceId (query)

### 4. POST /fba/inventory/v1/items/inventory (SANDBOX ONLY)
**Operation ID:** addInventory
**Headers:** x-amzn-idempotency-token (required)
**Body:** AddInventoryRequest { inventoryItems: [{ sellerSku, marketplaceId, quantity }] }

## Data Models

### InventorySummary
| Field | Type | Description |
|-------|------|-------------|
| asin | string | Amazon Standard Identification Number |
| fnSku | string | Fulfillment network SKU |
| sellerSku | string | Seller SKU |
| condition | string | Item condition (e.g., New Item) |
| inventoryDetails | InventoryDetails | Detailed breakdown |
| lastUpdatedTime | string (date-time) | Last update |
| productName | string | Localized product title |
| totalQuantity | integer | Total units in FBA |
| stores | array[string] | Applicable stores |

### InventoryDetails
| Field | Type | Description |
|-------|------|-------------|
| fulfillableQuantity | integer | Available for fulfillment |
| inboundWorkingQuantity | integer | In inbound shipment (notified) |
| inboundShippedQuantity | integer | In inbound with tracking |
| inboundReceivingQuantity | integer | Not yet received at FC |
| reservedQuantity | ReservedQuantity | Reserved inventory |
| researchingQuantity | ResearchingQuantity | Being researched |
| unfulfillableQuantity | UnfulfillableQuantity | Unsellable inventory |

**Note:** Changes to inbound quantities NOT detected by startDateTime filter.

### ReservedQuantity
| Field | Type | Description |
|-------|------|-------------|
| totalReservedQuantity | integer | Total reserved |
| pendingCustomerOrderQuantity | integer | Reserved for orders |
| pendingTransshipmentQuantity | integer | Transfer between FCs |
| fcProcessingQuantity | integer | Sidelined for processing |

### ResearchingQuantity
| Field | Type | Description |
|-------|------|-------------|
| totalResearchingQuantity | integer | Total being researched |
| researchingQuantityBreakdown | array[ResearchingQuantityEntry] | Duration breakdown |

### ResearchingQuantityEntry
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Enum: researchingQuantityInShortTerm (1-10 days), researchingQuantityInMidTerm (11-20 days), researchingQuantityInLongTerm (21+ days) |
| quantity | integer | Yes | Number of units |

### UnfulfillableQuantity
| Field | Type | Description |
|-------|------|-------------|
| totalUnfulfillableQuantity | integer | Total unsellable |
| customerDamagedQuantity | integer | Customer damaged |
| warehouseDamagedQuantity | integer | Warehouse damaged |
| distributorDamagedQuantity | integer | Distributor damaged |
| carrierDamagedQuantity | integer | Carrier damaged |
| defectiveQuantity | integer | Defective units |
| expiredQuantity | integer | Expired units |

### Granularity
| Field | Type | Description |
|-------|------|-------------|
| granularityType | string | Marketplace |
| granularityId | string | Marketplace ID |

### Pagination
| Field | Type | Description |
|-------|------|-------------|
| nextToken | string | Next page token (null = no more) |

### GetInventorySummariesResponse
| Field | Type | Description |
|-------|------|-------------|
| payload | GetInventorySummariesResult | Results |
| pagination | Pagination | Pagination info |
| errors | ErrorList | Errors |

### GetInventorySummariesResult
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| granularity | Granularity | Yes | Aggregation level |
| inventorySummaries | array[InventorySummary] | Yes | Inventory list |

### Error
code (string, required), message (string), details (string)

## Response Headers
x-amzn-RateLimit-Limit, x-amzn-RequestId

## Key Constraints
- marketplaceIds: max 1 item
- sellerSkus: max 50 items
- nextToken: expires in 30 seconds
- startDateTime: max 18 months ago
- Sandbox-only endpoints (create/delete/add) not available in production
