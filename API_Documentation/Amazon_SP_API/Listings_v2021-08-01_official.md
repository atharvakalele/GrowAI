# Amazon SP-API - Listings Items API v2021-08-01 - Official Reference
# Source: GitHub amzn/selling-partner-api-models/listingsItems_2021-08-01.json
# Extracted: 2026-04-13

## API Overview
- **Title:** Selling Partner API for Listings Items
- **Version:** 2021-08-01
- **Host:** sellingpartnerapi-eu.amazon.com (for India/EU)
- **Schemes:** HTTPS
- **Content Types:** application/json
- **Authentication:** AWS Signature Version 4

---

## Endpoints

### 1. GET /listings/2021-08-01/items/{sellerId}/{sku}
**Operation ID:** getListingsItem
**Description:** Returns details about a listing item
**Rate Limit:** 5 req/s, burst 10

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sellerId | string | **Yes** | Selling partner identifier |
| sku | string | **Yes** | Seller-provided listing identifier |

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| marketplaceIds | array[string] | **Yes** | Comma-delimited marketplace IDs (max 1) |
| issueLocale | string | No | Locale for issue localization (e.g., en_US, fr_CA) |
| includedData | array[string] | No | Datasets to include (default: summaries) |

**includedData Enum Values:**
- summaries
- attributes
- issues
- offers
- fulfillmentAvailability
- procurement
- relationships
- productTypes

**Responses:**
- 200: Item schema
- 400, 403, 404, 413, 415, 429, 500, 503: ErrorList

---

### 2. PUT /listings/2021-08-01/items/{sellerId}/{sku}
**Operation ID:** putListingsItem
**Description:** Creates or fully updates a listing item
**Rate Limit:** 5 req/s, burst 10

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sellerId | string | **Yes** | Selling partner identifier |
| sku | string | **Yes** | Seller-provided listing identifier |

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| marketplaceIds | array[string] | **Yes** | Marketplace IDs (max 1) |
| includedData | array[string] | No | Datasets to include (default: issues). Enum: identifiers, issues |
| mode | string | No | Enum: VALIDATION_PREVIEW |
| issueLocale | string | No | Locale for issue localization |

**Request Body:** ListingsItemPutRequest

**Responses:**
- 200: ListingsItemSubmissionResponse
- 400, 403, 413, 415, 429, 500, 503: ErrorList

---

### 3. PATCH /listings/2021-08-01/items/{sellerId}/{sku}
**Operation ID:** patchListingsItem
**Description:** Partially updates a listing item
**Rate Limit:** 5 req/s, burst 5

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sellerId | string | **Yes** | Selling partner identifier |
| sku | string | **Yes** | Seller-provided listing identifier |

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| marketplaceIds | array[string] | **Yes** | Marketplace IDs (max 1) |
| includedData | array[string] | No | Datasets (default: issues). Enum: identifiers, issues |
| mode | string | No | Enum: VALIDATION_PREVIEW |
| issueLocale | string | No | Locale for issue localization |

**Request Body:** ListingsItemPatchRequest

**Responses:**
- 200: ListingsItemSubmissionResponse
- 400, 403, 413, 415, 429, 500, 503: ErrorList

---

### 4. DELETE /listings/2021-08-01/items/{sellerId}/{sku}
**Operation ID:** deleteListingsItem
**Description:** Deletes a listing item
**Rate Limit:** 5 req/s, burst 5

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sellerId | string | **Yes** | Selling partner identifier |
| sku | string | **Yes** | Seller-provided listing identifier |

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| marketplaceIds | array[string] | **Yes** | Marketplace IDs (max 1) |
| issueLocale | string | No | Locale for issue localization |

**Responses:**
- 200: ListingsItemSubmissionResponse
- 400, 403, 413, 415, 429, 500, 503: ErrorList

---

### 5. GET /listings/2021-08-01/items/{sellerId}
**Operation ID:** searchListingsItems
**Description:** Search listings items for a selling partner
**Rate Limit:** 5 req/s, burst 5

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sellerId | string | **Yes** | Selling partner identifier |

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| marketplaceIds | array[string] | **Yes** | Marketplace IDs (max 1) |
| issueLocale | string | No | Locale for issue localization |
| includedData | array[string] | No | Default: summaries. Enum: summaries, attributes, issues, offers, fulfillmentAvailability, procurement, relationships, productTypes |
| identifiers | array[string] | No | Product identifiers (max 20) |
| identifiersType | string | No | Type of identifiers. Enum: ASIN, EAN, FNSKU, GTIN, ISBN, JAN, MINSAN, SKU, UPC |
| variationParentSku | string | No | Filter by variation parent SKU |
| packageHierarchySku | string | No | Filter by package hierarchy SKU |
| createdAfter | string (date-time) | No | Filter by creation date (ISO 8601) |
| createdBefore | string (date-time) | No | Filter by creation date (ISO 8601) |
| lastUpdatedAfter | string (date-time) | No | Filter by update date (ISO 8601) |
| lastUpdatedBefore | string (date-time) | No | Filter by update date (ISO 8601) |
| withIssueSeverity | array[string] | No | Filter by issue severity. Enum: WARNING, ERROR |
| withStatus | array[string] | No | Filter by status. Enum: BUYABLE, DISCOVERABLE |
| withoutStatus | array[string] | No | Exclude by status. Enum: BUYABLE, DISCOVERABLE |
| sortBy | string | No | Default: lastUpdatedDate. Enum: sku, createdDate, lastUpdatedDate |
| sortOrder | string | No | Default: DESC. Enum: ASC, DESC |
| pageSize | integer | No | Default: 10, max: 20 |
| pageToken | string | No | Pagination token |

**Constraints:**
- identifiers cannot be used with variationParentSku or packageHierarchySku
- identifiersType required when identifiers provided

**Responses:**
- 200: ItemSearchResults
- 400, 403, 413, 415, 429, 500, 503: ErrorList

---

## Data Models

### Item
| Field | Type | Description |
|-------|------|-------------|
| sku | string | Stock Keeping Unit |
| summaries | array[ItemSummary] | Summary details (optional) |
| attributes | object | Structured attribute data keyed by name (optional) |
| issues | array[Issue] | Associated issues (optional) |
| offers | array[Offer] | Current offers (optional) |
| fulfillmentAvailability | array[FulfillmentAvailability] | Fulfillment details (optional) |
| procurement | object | Vendor procurement details (optional) |
| relationships | array[Relationship] | Item relationships (optional) |
| productTypes | array[ProductType] | Associated product types (optional) |

### ItemSummary
| Field | Type | Description |
|-------|------|-------------|
| marketplaceId | string | Amazon marketplace ID |
| asin | string | Amazon Standard Identification Number |
| productType | string | Product type name |
| conditionType | string | Item condition (e.g., new_new) |
| status | array[string] | Status values: BUYABLE, DISCOVERABLE |
| itemName | string | Listing title |
| createdDate | string (date-time) | Creation timestamp (ISO 8601) |
| lastUpdatedDate | string (date-time) | Last update timestamp (ISO 8601) |
| mainImage | Image | Primary product image (optional) |

### Image
| Field | Type | Description |
|-------|------|-------------|
| link | string | Image URL |
| height | integer | Image height in pixels (optional) |
| width | integer | Image width in pixels (optional) |

### Issue
| Field | Type | Description |
|-------|------|-------------|
| code | string | Issue code identifier |
| message | string | Issue description |
| severity | string | Enum: ERROR, WARNING |
| attributeNames | array[string] | Related attribute names (optional) |
| categories | array[string] | Issue categories (optional) |
| enforcements | Enforcement | Enforcement details (optional) |

### Enforcement
| Field | Type | Description |
|-------|------|-------------|
| actions | array[Action] | Enforcement actions (optional) |
| exemption | Exemption | Exemption status (optional) |

### Action
| Field | Type | Description |
|-------|------|-------------|
| action | string | Enum: SEARCH_SUPPRESSED, ATTRIBUTE_SUPPRESSED, LISTING_SUPPRESSED, CATALOG_ITEM_REMOVED |

### Exemption
| Field | Type | Description |
|-------|------|-------------|
| status | string | Enum: EXEMPT, EXEMPT_UNTIL_EXPIRY_DATE, NOT_EXEMPT |
| expiryDate | string (date-time) | Exemption expiration (optional) |

### Offer
| Field | Type | Description |
|-------|------|-------------|
| marketplaceId | string | Amazon marketplace ID |
| offerType | string | Offer type (e.g., B2C) |
| price | Price | Offer price |
| audience | Audience | Target audience (optional) |

### Price
| Field | Type | Description |
|-------|------|-------------|
| currencyCode | string | ISO 4217 currency code |
| amount | string | Price amount |

### Audience
| Field | Type | Description |
|-------|------|-------------|
| value | string | Audience type (e.g., ALL) |
| displayName | string | Human-readable audience name |

### FulfillmentAvailability
| Field | Type | Description |
|-------|------|-------------|
| fulfillmentChannelCode | string | Fulfillment channel (DEFAULT, AFN, etc.) |
| quantity | integer | Available quantity |

### ListingsItemSubmissionResponse
| Field | Type | Description |
|-------|------|-------------|
| sku | string | Stock Keeping Unit |
| status | string | Enum: ACCEPTED, INVALID, VALID |
| submissionId | string | Unique submission identifier |
| issues | array[Issue] | Associated issues (optional) |
| identifiers | array[Identifier] | Product identifiers (optional) |

### Identifier
| Field | Type | Description |
|-------|------|-------------|
| marketplaceId | string | Amazon marketplace ID |
| asin | string | Amazon Standard Identification Number |

### ItemSearchResults
| Field | Type | Description |
|-------|------|-------------|
| numberOfResults | integer | Total results matching query |
| pagination | Pagination | Pagination details (optional) |
| items | array[Item] | Listing items |

### Pagination
| Field | Type | Description |
|-------|------|-------------|
| nextToken | string | Token for next page (optional) |
| previousToken | string | Token for previous page (optional) |

### Error
| Field | Type | Description |
|-------|------|-------------|
| code | string | Error code |
| message | string | Error message |
| details | string | Additional error details (optional) |

---

## Common Response Headers
| Header | Type | Description |
|--------|------|-------------|
| x-amzn-RateLimit-Limit | string | Current rate limit |
| x-amzn-RequestId | string | Unique request reference |

---

## Key Constraints
- Marketplace IDs limited to 1 per request (maxItems: 1)
- Search identifiers limited to 20 per request (maxItems: 20)
- Page size maximum: 20 results
- Only top-level attributes can be patched
- identifiers mutually exclusive with variationParentSku/packageHierarchySku
- identifiersType required when identifiers provided
- VALIDATION_PREVIEW mode validates without submitting

---

## Notes for GoAmrita Bhandar
- Use EU endpoint: sellingpartnerapi-eu.amazon.com
- India Marketplace ID: A21TJRUUN4KGV
- Use with Product Type Definitions API for attribute schemas
- sellerId = our Entity ID: ENTITY1TVPGA5B1GOJW (or seller ID from credentials)
