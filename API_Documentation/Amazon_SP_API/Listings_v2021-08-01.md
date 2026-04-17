# Selling Partner API for Listings Items v2021-08-01
## Official OpenAPI Spec Documentation
**Source:** https://github.com/amzn/selling-partner-api-models/blob/main/models/listings-items-api-model/listingsItems_2021-08-01.json
**Fetched:** 2026-04-13
**Spec Version:** Swagger 2.0
**API Version:** 2021-08-01

---

## API Info
- **Title:** Selling Partner API for Listings Items
- **Description:** Programmatic access to selling partner listings on Amazon, used with Product Type Definitions API.
- **Host:** sellingpartnerapi-na.amazon.com (use `sellingpartnerapi-eu.amazon.com` for India/EU)
- **Base Path:** /
- **Schemes:** HTTPS
- **Consumes:** application/json
- **Produces:** application/json
- **License:** Apache License 2.0

---

## Endpoints

### 1. GET /listings/2021-08-01/items/{sellerId}/{sku}
**Operation:** getListingsItem
**Description:** Returns details about a listings item for a selling partner.

**Parameters:**
| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| sellerId | path | string | Yes | A selling partner identifier (e.g., merchant account ID) |
| sku | path | string | Yes | A seller-provided identifier for an Amazon listing |
| marketplaceIds | query | array[string] (csv, max 1) | Yes | Comma-delimited Amazon marketplace identifiers |
| issueLocale | query | string | No | Locale for issue localization (e.g., en_US, fr_CA, fr_FR) |
| includedData | query | array[string] (csv) | No | Data sets to include. Default: `["summaries"]`. Enum: `summaries`, `attributes`, `issues`, `offers`, `fulfillmentAvailability`, `procurement`, `relationships`, `productTypes` |

**Responses:**
| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Success | Item |
| 400 | Invalid parameters | ErrorList |
| 403 | Access forbidden | ErrorList |
| 404 | Resource not found | ErrorList |
| 413 | Request size exceeded | ErrorList |
| 415 | Unsupported format | ErrorList |
| 429 | Rate limit exceeded | ErrorList |
| 500 | Server error | ErrorList |
| 503 | Service unavailable | ErrorList |

**Response Headers:**
- `x-amzn-RateLimit-Limit` (string): Rate limit
- `x-amzn-RequestId` (string): Unique request ID

---

### 2. PUT /listings/2021-08-01/items/{sellerId}/{sku}
**Operation:** putListingsItem
**Description:** Creates a new listings item or fully updates an existing one.

**Parameters:**
| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| sellerId | path | string | Yes | Selling partner identifier |
| sku | path | string | Yes | Seller-provided listing identifier |
| marketplaceIds | query | array[string] (csv, max 1) | Yes | Marketplace IDs |
| includedData | query | array[string] (csv) | No | Default: `["issues"]`. Enum: `identifiers`, `issues` |
| mode | query | string | No | Enum: `VALIDATION_PREVIEW` - Preview validation without submission |
| issueLocale | query | string | No | Issue localization locale |
| body | body | ListingsItemPutRequest | Yes | Listing item attributes |

**Responses:** Same status codes as GET, returns `ListingsItemSubmissionResponse`

---

### 3. PATCH /listings/2021-08-01/items/{sellerId}/{sku}
**Operation:** patchListingsItem
**Description:** Partially updates an existing listings item.

**Parameters:**
| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| sellerId | path | string | Yes | Selling partner identifier |
| sku | path | string | Yes | Seller-provided listing identifier |
| marketplaceIds | query | array[string] (csv, max 1) | Yes | Marketplace IDs |
| includedData | query | array[string] (csv) | No | Default: `["issues"]`. Enum: `identifiers`, `issues` |
| mode | query | string | No | Enum: `VALIDATION_PREVIEW` |
| issueLocale | query | string | No | Issue localization locale |
| body | body | ListingsItemPatchRequest | Yes | Patch attributes |

**Responses:** Same status codes, returns `ListingsItemSubmissionResponse`

---

### 4. DELETE /listings/2021-08-01/items/{sellerId}/{sku}
**Operation:** deleteListingsItem
**Description:** Deletes a listings item for a selling partner.

**Parameters:**
| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| sellerId | path | string | Yes | Selling partner identifier |
| sku | path | string | Yes | Seller-provided listing identifier |
| marketplaceIds | query | array[string] (csv, max 1) | Yes | Marketplace IDs |
| issueLocale | query | string | No | Issue localization locale |

**Responses:** Same status codes, returns `ListingsItemSubmissionResponse`

---

### 5. GET /listings/2021-08-01/items/{sellerId}
**Operation:** searchListingsItems
**Description:** Search for and return list of listings items and truncated details.

**Parameters:**
| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| sellerId | path | string | Yes | Selling partner identifier |
| marketplaceIds | query | array[string] (csv, max 1) | Yes | Marketplace IDs |
| issueLocale | query | string | No | Issue localization locale |
| includedData | query | array[string] (csv) | No | Default: `["summaries"]`. Enum: `summaries`, `attributes`, `issues`, `offers`, `fulfillmentAvailability`, `procurement`, `relationships`, `productTypes` |
| identifiers | query | array[string] (csv, max 20) | No | Product identifiers for search |
| identifiersType | query | string | No | Enum: `ASIN`, `EAN`, `FNSKU`, `GTIN`, `ISBN`, `JAN`, `MINSAN`, `SKU`, `UPC` |
| variationParentSku | query | string | No | Filter for variation children of specified SKU |
| packageHierarchySku | query | string | No | Filter for package hierarchy SKU relationships |
| createdAfter | query | string (date-time) | No | Items created at or after (ISO 8601) |
| createdBefore | query | string (date-time) | No | Items created at or before (ISO 8601) |
| lastUpdatedAfter | query | string (date-time) | No | Items updated at or after (ISO 8601) |
| lastUpdatedBefore | query | string (date-time) | No | Items updated at or before (ISO 8601) |
| withIssueSeverity | query | array[string] (csv) | No | Enum: `WARNING`, `ERROR` |
| withStatus | query | array[string] (csv) | No | Enum: `BUYABLE`, `DISCOVERABLE` |
| withoutStatus | query | array[string] (csv) | No | Enum: `BUYABLE`, `DISCOVERABLE` |
| sortBy | query | string | No | Enum: `sku`, `createdDate`, `lastUpdatedDate`. Default: `lastUpdatedDate` |
| sortOrder | query | string | No | Enum: `ASC`, `DESC`. Default: `DESC` |
| pageSize | query | integer | No | Results per page. Max: 20, Default: 10 |
| pageToken | query | string | No | Pagination token |

**Responses:** Returns `ItemSearchResults`

---

## Data Models

### Item
| Property | Type | Description |
|----------|------|-------------|
| sku | string | Seller-provided identifier |
| summaries | array[ItemSummary] | Summary information |
| attributes | object | Product attributes (JSON) |
| issues | array[Issue] | Listing issues |
| offers | array[Offer] | Offer details |
| fulfillmentAvailability | array[FulfillmentAvailability] | Fulfillment data |
| procurement | array[object] | Procurement data |
| relationships | array[object] | Variation/package relationships |
| productTypes | array[object] | Product type information |

### ItemSummary
| Property | Type | Description |
|----------|------|-------------|
| marketplaceId | string | Marketplace identifier |
| asin | string | Amazon Standard Identification Number |
| productType | string | Amazon product type |
| conditionType | string | Item condition |
| status | array[string] | Status values (e.g., BUYABLE, DISCOVERABLE) |
| itemName | string | Display name/title |
| createdDate | string (date-time) | Creation date |
| lastUpdatedDate | string (date-time) | Last update date |
| mainImage | Image | Main product image |

### Image
| Property | Type | Description |
|----------|------|-------------|
| link | string | Image URL |
| height | integer | Image height in pixels |
| width | integer | Image width in pixels |

### Issue
| Property | Type | Description |
|----------|------|-------------|
| code | string | Issue code |
| message | string | Issue description |
| severity | string | Enum: `ERROR`, `WARNING` |
| attributeNames | array[string] | Affected attribute names |
| categories | array[string] | Issue categories |
| enforcements | Enforcements | Enforcement actions |

### Enforcements
| Property | Type | Description |
|----------|------|-------------|
| actions | array[object] | Actions taken (each has `action` string) |
| exemption | object | Exemption with `status` (string) and `expiryDate` (date-time) |

### Offer
| Property | Type | Description |
|----------|------|-------------|
| marketplaceId | string | Marketplace identifier |
| offerType | string | Offer type |
| price | Price | Offer price |
| audience | Audience | Target audience |

### Price
| Property | Type | Description |
|----------|------|-------------|
| currencyCode | string | ISO 4217 currency code |
| amount | string | Monetary amount |

### Audience
| Property | Type | Description |
|----------|------|-------------|
| value | string | Audience value |
| displayName | string | Audience display name |

### FulfillmentAvailability
| Property | Type | Description |
|----------|------|-------------|
| fulfillmentChannelCode | string | Channel code (e.g., DEFAULT, AMAZON_NA) |
| quantity | integer | Available quantity |

### ListingsItemPutRequest
| Property | Type | Description |
|----------|------|-------------|
| attributes | object | Product attributes as JSON (per Product Type Definitions schema) |

### ListingsItemPatchRequest
| Property | Type | Description |
|----------|------|-------------|
| attributes | object | Partial product attributes to update |

### ListingsItemSubmissionResponse
| Property | Type | Description |
|----------|------|-------------|
| sku | string | Seller SKU |
| status | string | Submission status (e.g., ACCEPTED, INVALID) |
| submissionId | string | Unique submission identifier |
| identifiers | array[ItemIdentifier] | Item identifiers |
| issues | array[Issue] | Submission issues |

### ItemIdentifier
| Property | Type | Description |
|----------|------|-------------|
| marketplaceId | string | Marketplace identifier |
| asin | string | ASIN assigned/matched |

### ItemSearchResults
| Property | Type | Description |
|----------|------|-------------|
| numberOfResults | integer | Total matching items |
| pagination | Pagination | Pagination tokens |
| items | array[Item] | Matching items |

### Pagination
| Property | Type | Description |
|----------|------|-------------|
| nextToken | string | Token for next page |
| previousToken | string | Token for previous page |

### ErrorList
| Property | Type | Description |
|----------|------|-------------|
| errors | array[Error] | List of errors |

### Error
| Property | Type | Description |
|----------|------|-------------|
| code | string | Error code |
| message | string | Error description |
| details | string | Additional context |

---

## Rate Limits
- **GET (single item):** 5 requests/sec
- **PUT/PATCH/DELETE:** 5 requests/sec
- **GET (search):** 5 requests/sec

---

## Important Notes for GoAmrita Bhandar
- **Region:** India = EU endpoint (`sellingpartnerapi-eu.amazon.com`)
- **Marketplace ID for India:** A21TJRUUN4KGV
- Use `VALIDATION_PREVIEW` mode in PUT/PATCH to test listings changes without submitting
- `includedData` parameter controls response size -- request only what you need
- Identifier types supported: ASIN, EAN, FNSKU, GTIN, ISBN, JAN, MINSAN, SKU, UPC
- Issues with severity `ERROR` will prevent the listing from being BUYABLE
