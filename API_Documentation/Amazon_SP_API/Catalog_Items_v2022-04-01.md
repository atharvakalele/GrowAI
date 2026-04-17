# Catalog Items API v2022-04-01 — Official Reference
**Source:** Amazon GitHub OpenAPI Spec (amzn/selling-partner-api-models)
**Our Endpoint:** sellingpartnerapi-eu.amazon.com
**Marketplace:** A21TJRUUN4KGV (India)

## Endpoints

### 1. Search Catalog Items
- **Path:** GET /catalog/2022-04-01/items
- **Rate:** 2 req/sec (burst: 2)

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| identifiers | array[string] | No | Product identifiers (max 20); cannot combine with keywords |
| identifiersType | enum | No | ASIN, EAN, GTIN, ISBN, JAN, MINSAN, SKU, UPC. Required when identifiers present |
| marketplaceIds | array[string] | YES | Marketplace IDs (max 1). For us: A21TJRUUN4KGV |
| includedData | array[enum] | No | summaries, attributes, dimensions, identifiers, images, productTypes, relationships, salesRanks, classifications, vendorDetails. Default: summaries |
| locale | string | No | Localization (defaults to marketplace) |
| sellerId | string | No | Required for SKU searches |
| keywords | array[string] | No | Search terms (max 20); cannot combine with identifiers |
| brandNames | array[string] | No | Brand filter (keywords only) |
| classificationIds | array[string] | No | Browse node filter (keywords only) |
| pageSize | integer | No | Max 20, default 10 |
| pageToken | string | No | Pagination token |
| keywordsLocale | string | No | Keyword language |

**Response 200:**
```json
{
  "numberOfResults": integer,
  "pagination": { "nextToken": string, "previousToken": string },
  "refinements": {
    "brands": [{ "numberOfResults": int, "brandName": string }],
    "classifications": [{ "numberOfResults": int, "displayName": string, "classificationId": string }]
  },
  "items": [Item]
}
```

### 2. Get Catalog Item
- **Path:** GET /catalog/2022-04-01/items/{asin}
- **Rate:** 2 req/sec (burst: 2)

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| asin | string (path) | YES | ASIN |
| marketplaceIds | array[string] | YES | A21TJRUUN4KGV |
| includedData | array[enum] | No | Same options as search |
| locale | string | No | Localization |

**Response:** Single Item object

## Item Data Model
```
Item:
  asin: string (Amazon ID)
  attributes: object (dynamic keys — brand, color, weight, dimensions, bullet_point etc.)
  classifications: [{ displayName, classificationId, parent: recursive }]
  dimensions: [{ marketplaceId, item: {height,length,width,weight with units}, package: same }]
  identifiers: [{ marketplaceId, identifiers: [{identifierType, identifier}] }]
  images: [{ marketplaceId, images: [{variant: MAIN/PT01-PT08, link, height, width}] }]
  productTypes: [{ marketplaceId, productType }]
  relationships: [{ marketplaceId, relationships: [{childAsins, parentAsins, type, variationTheme}] }]
  salesRanks: [{ marketplaceId, classificationRanks: [{classificationId,title,rank}], displayGroupRanks: [{websiteDisplayGroup,title,rank}] }]
  summaries: [{ marketplaceId, brand, color, itemName, manufacturer, modelNumber, packageQuantity, partNumber, size, style, websiteDisplayGroup, itemClassification: Base|Variation|Parental|VirtualBundle|Bundle }]
  vendorDetails: vendor-only
```

## Key Capabilities for Our System:
- **Sale Price:** Get via attributes or summaries (listPrice in attributes)
- **BSR/Sales Rank:** salesRanks → classificationRanks + displayGroupRanks
- **Images:** images → check count, variant types
- **Product Name:** summaries → itemName
- **Brand:** summaries → brand
- **Category:** classifications → browse nodes
- **Variations:** relationships → parent/child ASINs

## Limitations:
- Max 20 identifiers per request
- Max 1 marketplace per request  
- Rate: only 2 req/sec — need batching for 300+ products
- salesRanks may not be available for all ASINs
- attributes schema varies by product type

## Error Codes:
400 (bad params), 403 (auth), 404 (not found), 413 (too large), 415 (wrong content type), 429 (rate limit), 500, 503
