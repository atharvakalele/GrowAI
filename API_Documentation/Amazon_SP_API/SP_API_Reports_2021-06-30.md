# SP-API for Managing Seller Data Exports v2021-06-30

Source: github.com/amzn/selling-partner-api-models - reports_2021-06-30.json
Fetched: 2026-04-13 | Swagger 2.0 | Host: sellingpartnerapi-eu.amazon.com (India/EU)

## Endpoints & Parameters

### GET /reports/2021-06-30/reports
Operation: getReports | Rate: 0.0222/s, Burst: 10
| Param | In | Type | Required | Notes |
|-------|-----|------|----------|-------|
| reportTypes | query | array[string] | No | 1-10 types |
| processingStatuses | query | array[string] | No | CANCELLED, DONE, FATAL, IN_PROGRESS, IN_QUEUE |
| marketplaceIds | query | array[string] | No | 1-10 IDs |
| pageSize | query | integer | No | 1-100, default 10 |
| createdSince | query | date-time | No | Default: 90 days ago |
| createdUntil | query | date-time | No | Default: now |
| nextToken | query | string | No | Pagination (use as sole param) |
Response: GetReportsResponse {reports: array[Report], nextToken: string}

### POST /reports/2021-06-30/reports
Operation: createReport | Rate: 0.0167/s, Burst: 15
Body - CreateReportSpecification:
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| reportType | string | Yes | Type identifier |
| marketplaceIds | array[string] | Yes | 1-25 IDs |
| dataStartTime | date-time | No | Default: now |
| dataEndTime | date-time | No | Default: now |
| reportOptions | object(str->str) | No | Type-specific options |
Response 202: {reportId: string}

### GET /reports/2021-06-30/reports/{reportId}
Operation: getReport | Rate: 2.0/s, Burst: 15
Path param: reportId (string, required)
Response: Report object

### DELETE /reports/2021-06-30/reports/{reportId}
Operation: cancelReport | Rate: 0.0222/s, Burst: 10
Cancels only IN_QUEUE status.

### GET /reports/2021-06-30/schedules
Operation: getReportSchedules | Rate: 0.0222/s, Burst: 10
Required: reportTypes (query, array, 1-10 types)
Response: ReportScheduleList

### POST /reports/2021-06-30/schedules
Operation: createReportSchedule | Rate: 0.0222/s, Burst: 10
Body - CreateReportScheduleSpecification:
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| reportType | string | Yes | Type identifier |
| marketplaceIds | array[string] | Yes | 1-25 IDs |
| reportOptions | object(str->str) | No | Options |
| period | string | Yes | ISO 8601 (see enum below) |
| nextReportCreationTime | date-time | No | First creation time |
Replaces existing schedule with same type+marketplace.
Response 201: {reportScheduleId: string}

### GET /reports/2021-06-30/schedules/{reportScheduleId}
Operation: getReportSchedule | Rate: 0.0222/s, Burst: 10

### DELETE /reports/2021-06-30/schedules/{reportScheduleId}
Operation: cancelReportSchedule | Rate: 0.0222/s, Burst: 10

### GET /reports/2021-06-30/documents/{reportDocumentId}
Operation: getReportDocument | Rate: 0.0167/s, Burst: 15
| Param | In | Type | Required | Notes |
|-------|-----|------|----------|-------|
| reportDocumentId | path | string | Yes | Document ID |
| enableContentEncodingUrlHeader | query | boolean | No | gzip instead of identity |
Response: ReportDocument

## Data Models

### Report
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| reportId | string | Yes | Unique with seller ID |
| reportType | string | Yes | Type identifier |
| marketplaceIds | array[string] | No | Marketplace IDs |
| dataStartTime | date-time | No | Data range start |
| dataEndTime | date-time | No | Data range end |
| reportScheduleId | string | No | Schedule that created this |
| createdTime | date-time | Yes | Creation timestamp |
| processingStatus | string | Yes | CANCELLED, DONE, FATAL, IN_PROGRESS, IN_QUEUE |
| processingStartTime | date-time | No | Processing start |
| processingEndTime | date-time | No | Processing end |
| reportDocumentId | string | No | Present when DONE |

### ReportSchedule
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| reportScheduleId | string | Yes | Unique with seller ID |
| reportType | string | Yes | Type identifier |
| marketplaceIds | array[string] | No | Marketplace IDs |
| reportOptions | object | No | Type-specific options |
| period | string | Yes | ISO 8601 period |
| nextReportCreationTime | date-time | No | Next creation time |

### Period Enum Values
| Value | Meaning |
|-------|---------|
| PT5M | Every 5 minutes |
| PT15M | Every 15 minutes |
| PT30M | Every 30 minutes |
| PT1H | Hourly |
| PT2H | Every 2 hours |
| PT4H | Every 4 hours |
| PT8H | Every 8 hours |
| PT12H | Every 12 hours |
| P1D | Daily |
| P2D | Every 2 days |
| P3D | Every 3 days |
| PT84H | Every 84 hours |
| P7D | Weekly |
| P14D | Every 2 weeks |
| P15D | Every 15 days |
| P18D | Every 18 days |
| P30D | Every 30 days |
| P1M | Monthly |

### ReportDocument
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| reportDocumentId | string | Yes | Document ID |
| url | string | Yes | Presigned URL (expires 5 min) |
| compressionAlgorithm | string | No | Enum: GZIP |

### Error
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| code | string | Yes | Error code |
| message | string | Yes | Description |
| details | string | No | Context |

## Standard Workflow
1. POST /reports with reportType + marketplaceIds -> get reportId
2. Poll GET /reports/{reportId} until processingStatus = DONE
3. GET /documents/{reportDocumentId} -> get presigned url
4. HTTP GET the url directly -> download content (decompress if GZIP)

## Common India Marketplace Types
- GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_GENERAL (All orders)
- GET_FLAT_FILE_ACTIONABLE_ORDER_DATA_SHIPPING (Actionable orders)
- GET_MERCHANT_LISTINGS_ALL_DATA (All listings)
- GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA (FBA inventory)
- GET_FBA_FULFILLMENT_CURRENT_INVENTORY_DATA (Current FBA inventory)
- GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE (Settlements)
- GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE (Returns)
- GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA (FBA fees)
- GET_SELLER_FEEDBACK_DATA (Feedback)
- GET_FLAT_FILE_OPEN_LISTINGS_DATA (Open listings)

## HTTP Status Codes
400 (invalid params), 401 (auth invalid), 403 (forbidden), 404 (not found), 415 (bad content-type), 429 (rate limit), 500 (server error), 503 (unavailable)

## GoAmrita Bhandar Notes
- India = EU endpoint: sellingpartnerapi-eu.amazon.com
- Marketplace ID: A21TJRUUN4KGV
- Presigned URL expires in 5 minutes - download immediately
- Check compressionAlgorithm for GZIP compressed content
- Very low rate limits - implement proper throttling and backoff
- Use nextToken as sole parameter when paginating
- Schedule automated data collection with createReportSchedule
