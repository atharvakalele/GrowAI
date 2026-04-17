# Amazon SP-API - Reports API v2021-06-30 - Official Reference
# Source: GitHub amzn/selling-partner-api-models/reports_2021-06-30.json
# Extracted: 2026-04-13

## API Overview
- **Title:** Selling Partner API for Reports
- **Version:** 2021-06-30
- **Host:** sellingpartnerapi-eu.amazon.com (for India/EU)
- **Schemes:** HTTPS
- **Content Types:** application/json

## Endpoints

### 1. GET /reports/2021-06-30/reports
**Operation ID:** getReports
**Rate Limit:** 0.0222 req/sec, burst 10

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| reportTypes | array[string] | No | 1-10 items |
| processingStatuses | array[string] | No | Enum: CANCELLED, DONE, FATAL, IN_PROGRESS, IN_QUEUE |
| marketplaceIds | array[string] | No | 1-10 items |
| pageSize | integer | No | 1-100, default 10 |
| createdSince | string (date-time) | No | Default: 90 days ago |
| createdUntil | string (date-time) | No | Default: now |
| nextToken | string | No | Pagination token |

### 2. POST /reports/2021-06-30/reports
**Operation ID:** createReport
**Rate Limit:** 0.0167 req/sec, burst 15

**Body - CreateReportSpecification:**
| Field | Type | Required |
|-------|------|----------|
| reportType | string | Yes |
| marketplaceIds | array[string] | Yes (1-25) |
| dataStartTime | string (date-time) | No |
| dataEndTime | string (date-time) | No |
| reportOptions | ReportOptions | No |

**Response:** 202 -> CreateReportResponse { reportId }

### 3. GET /reports/2021-06-30/reports/{reportId}
**Operation ID:** getReport
**Rate Limit:** 2 req/sec, burst 15
**Response:** Report object

### 4. DELETE /reports/2021-06-30/reports/{reportId}
**Operation ID:** cancelReport (only IN_QUEUE reports)
**Rate Limit:** 0.0222 req/sec, burst 10

### 5. GET /reports/2021-06-30/schedules
**Operation ID:** getReportSchedules
**Rate Limit:** 0.0222 req/sec, burst 10
**Parameters:** reportTypes (array, required, 1-10)

### 6. POST /reports/2021-06-30/schedules
**Operation ID:** createReportSchedule
**Rate Limit:** 0.0222 req/sec, burst 10

**Body - CreateReportScheduleSpecification:**
| Field | Type | Required |
|-------|------|----------|
| reportType | string | Yes |
| period | string | Yes (see Period enum) |
| marketplaceIds | array[string] | Yes (1-25) |
| reportOptions | ReportOptions | No |
| nextReportCreationTime | string (date-time) | No |

**Response:** 201 -> CreateReportScheduleResponse { reportScheduleId }

### 7. GET /reports/2021-06-30/schedules/{reportScheduleId}
**Operation ID:** getReportSchedule
**Rate Limit:** 0.0222 req/sec, burst 10

### 8. DELETE /reports/2021-06-30/schedules/{reportScheduleId}
**Operation ID:** cancelReportSchedule
**Rate Limit:** 0.0222 req/sec, burst 10

### 9. GET /reports/2021-06-30/documents/{reportDocumentId}
**Operation ID:** getReportDocument
**Rate Limit:** 0.0167 req/sec, burst 15
**Parameters:** enableContentEncodingUrlHeader (boolean, optional)

## Data Models

### Report
| Field | Type | Required |
|-------|------|----------|
| reportId | string | Yes |
| reportType | string | Yes |
| processingStatus | string | Yes - CANCELLED/DONE/FATAL/IN_PROGRESS/IN_QUEUE |
| createdTime | date-time | Yes |
| marketplaceIds | array[string] | No |
| dataStartTime | date-time | No |
| dataEndTime | date-time | No |
| reportScheduleId | string | No |
| processingStartTime | date-time | No |
| processingEndTime | date-time | No |
| reportDocumentId | string | No (available when DONE) |

### ReportSchedule
| Field | Type | Required |
|-------|------|----------|
| reportScheduleId | string | Yes |
| reportType | string | Yes |
| period | string | Yes |
| marketplaceIds | array[string] | No |
| reportOptions | ReportOptions | No |
| nextReportCreationTime | date-time | No |

### ReportDocument
| Field | Type | Required |
|-------|------|----------|
| reportDocumentId | string | Yes |
| url | string | Yes (presigned download URL) |
| compressionAlgorithm | string | No (enum: GZIP) |

### ReportOptions
Key-value pairs (additionalProperties: string)

### Error
code (string, required), message (string, required), details (string, optional)

## Period Enum (ISO 8601)
PT5M (5min), PT15M (15min), PT30M (30min), PT1H (1hr), PT2H (2hr), PT4H (4hr), PT8H (8hr), PT12H (12hr), P1D (1day), P2D (2day), P3D (3day), PT84H (84hr), P7D (7day), P14D (14day), P15D (15day), P18D (18day), P30D (30day), P1M (1month)

## Processing Status Enum
IN_QUEUE -> IN_PROGRESS -> DONE/FATAL/CANCELLED

## Report Workflow
1. POST /reports -> get reportId
2. Poll GET /reports/{reportId} -> wait for DONE
3. GET /documents/{reportDocumentId} -> get presigned URL
4. Download from URL (may be GZIP)

## Response Headers (all endpoints)
x-amzn-RateLimit-Limit, x-amzn-RequestId

## HTTP Status Codes
200 (Success), 201 (Created), 202 (Accepted), 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 415 (Unsupported Media), 429 (Rate Limited), 500 (Server Error), 503 (Unavailable)
