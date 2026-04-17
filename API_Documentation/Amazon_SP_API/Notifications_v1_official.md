# Amazon SP-API - Notifications API v1 - Official Reference
# Source: GitHub amzn/selling-partner-api-models/notifications.json
# Extracted: 2026-04-13

## API Overview
- **Title:** Selling Partner API for Notifications
- **Version:** v1
- **Host:** sellingpartnerapi-eu.amazon.com (for India/EU)
- **Schemes:** HTTPS
- **Content Types:** application/json
- **Authentication:** AWS Signature Version 4

---

## Endpoints

### 1. GET /notifications/v1/subscriptions/{notificationType}
**Operation ID:** getSubscription
**Description:** Returns information about subscription of the specified notification type and payload version
**Rate Limit:** 1 request/second, burst 5

**Parameters:**
| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| notificationType | path | string | **Yes** | The notification type |
| payloadVersion | query | string | No | Version of payload object |

**Responses:**
- 200: GetSubscriptionResponse
- 400, 403, 404, 413, 415, 429, 500, 503: Error responses

---

### 2. POST /notifications/v1/subscriptions/{notificationType}
**Operation ID:** createSubscription
**Description:** Creates a subscription for the specified notification type to be delivered to the specified destination
**Rate Limit:** 1 request/second, burst 5

**Parameters:**
| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| notificationType | path | string | **Yes** | The notification type |
| body | body | CreateSubscriptionRequest | **Yes** | Request body |

**CreateSubscriptionRequest:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| payloadVersion | string | **Yes** | Payload version |
| destinationId | string | **Yes** | Destination identifier |
| processingDirective | ProcessingDirective | No | Control notification processing |

**Responses:**
- 200: CreateSubscriptionResponse
- 400, 403, 404, 409, 413, 415, 429, 500, 503: Error responses

---

### 3. GET /notifications/v1/subscriptions/{notificationType}/{subscriptionId}
**Operation ID:** getSubscriptionById
**Description:** Returns information about a subscription. Grantless operation.
**Rate Limit:** 1 request/second, burst 5

**Parameters:**
| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| notificationType | path | string | **Yes** | The notification type |
| subscriptionId | path | string | **Yes** | Subscription identifier |

**Responses:**
- 200: GetSubscriptionByIdResponse
- 400, 403, 404, 409, 413, 415, 429, 500, 503: Error responses

---

### 4. DELETE /notifications/v1/subscriptions/{notificationType}/{subscriptionId}
**Operation ID:** deleteSubscriptionById
**Description:** Deletes the subscription. Grantless operation.
**Rate Limit:** 1 request/second, burst 5

**Parameters:**
| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| notificationType | path | string | **Yes** | The notification type |
| subscriptionId | path | string | **Yes** | Subscription identifier |

**Responses:**
- 200: DeleteSubscriptionByIdResponse
- 400, 403, 404, 409, 413, 415, 429, 500, 503: Error responses

---

### 5. GET /notifications/v1/destinations
**Operation ID:** getDestinations
**Description:** Returns information about all destinations. Grantless operation.
**Rate Limit:** 1 request/second, burst 5

**Parameters:** None

**Responses:**
- 200: GetDestinationsResponse
- 400, 403, 404, 409, 413, 415, 429, 500, 503: Error responses

---

### 6. POST /notifications/v1/destinations
**Operation ID:** createDestination
**Description:** Creates a destination resource to receive notifications. Grantless operation.
**Rate Limit:** 1 request/second, burst 5

**Request Body - CreateDestinationRequest:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string (max 256 chars) | **Yes** | Developer-defined destination name |
| resourceSpecification | DestinationResourceSpecification | **Yes** | Resource specification |

**Responses:**
- 200: CreateDestinationResponse
- 400, 403, 404, 409, 413, 415, 429, 500, 503: Error responses

---

### 7. GET /notifications/v1/destinations/{destinationId}
**Operation ID:** getDestination
**Description:** Returns information about the destination. Grantless operation.
**Rate Limit:** 1 request/second, burst 5

**Parameters:**
| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| destinationId | path | string | **Yes** | Destination identifier |

**Responses:**
- 200: GetDestinationResponse
- 400, 403, 404, 409, 413, 415, 429, 500, 503: Error responses

---

### 8. DELETE /notifications/v1/destinations/{destinationId}
**Operation ID:** deleteDestination
**Description:** Deletes the destination. Grantless operation.
**Rate Limit:** 1 request/second, burst 5

**Parameters:**
| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| destinationId | path | string | **Yes** | Destination identifier |

**Responses:**
- 200: DeleteDestinationResponse
- 400, 403, 404, 409, 413, 415, 429, 500, 503: Error responses

---

## Data Models

### Subscription
**Required Fields:** destinationId, payloadVersion, subscriptionId

| Field | Type | Description |
|-------|------|-------------|
| subscriptionId | string | Generated when subscription created |
| payloadVersion | string | Version of payload object |
| destinationId | string | Destination receiving notifications |
| processingDirective | ProcessingDirective | Control notification processing (optional) |

### ProcessingDirective
| Field | Type | Description |
|-------|------|-------------|
| eventFilter | EventFilter | Notification-type-specific filter (optional) |

### EventFilter
Combines: AggregationFilter + MarketplaceFilter + OrderChangeTypeFilter

| Field | Type | Description |
|-------|------|-------------|
| eventFilterType | string | **Required.** Enum: ANY_OFFER_CHANGED, ORDER_CHANGE |
| aggregationSettings | AggregationSettings | Aggregation settings (optional) |
| marketplaceIds | array[string] | Marketplace filter (optional) |
| orderChangeTypes | array[OrderChangeTypeEnum] | Order change type filter (optional) |

### AggregationSettings
**Required Fields:** aggregationTimePeriod

| Field | Type | Description |
|-------|------|-------------|
| aggregationTimePeriod | AggregationTimePeriod | Time period for aggregation |

### AggregationTimePeriod (Enum)
| Value | Description |
|-------|-------------|
| FiveMinutes | Aggregated notification sent every 5 minutes |
| TenMinutes | Aggregated notification sent every 10 minutes |

### OrderChangeTypeEnum (Enum)
| Value | Description |
|-------|-------------|
| OrderStatusChange | Order status changed |
| BuyerRequestedChange | Buyer requested a change |

### Destination
**Required Fields:** destinationId, name, resource

| Field | Type | Description |
|-------|------|-------------|
| name | string (max 256 chars) | Developer-defined destination name |
| destinationId | string | Generated when destination created |
| resource | DestinationResource | Resource receiving notifications |

### DestinationResource
| Field | Type | Description |
|-------|------|-------------|
| sqs | SqsResource | Amazon SQS queue destination (optional) |
| eventBridge | EventBridgeResource | Amazon EventBridge destination (optional) |

### DestinationResourceSpecification
| Field | Type | Description |
|-------|------|-------------|
| sqs | SqsResource | SQS queue specification (optional) |
| eventBridge | EventBridgeResourceSpecification | EventBridge specification (optional) |

### SqsResource
**Required Fields:** arn

| Field | Type | Description |
|-------|------|-------------|
| arn | string (max 1000 chars) | ARN for SQS queue. Pattern: ^arn:aws:sqs:\\S+:\\S+:\\S+ |

### EventBridgeResourceSpecification
**Required Fields:** accountId, region

| Field | Type | Description |
|-------|------|-------------|
| region | string | AWS region for receiving notifications |
| accountId | string | AWS account ID responsible for charges |

### EventBridgeResource
**Required Fields:** accountId, name, region

| Field | Type | Description |
|-------|------|-------------|
| name | string (max 256 chars) | Partner event source name |
| region | string | AWS region for notifications |
| accountId | string | AWS account ID responsible for charges |

### Error
**Required Fields:** code, message

| Field | Type | Description |
|-------|------|-------------|
| code | string | Error type identifier |
| message | string | Description of error condition |
| details | string | Additional context information (optional) |

---

## Response Schemas

| Response Type | Payload | Errors |
|---------------|---------|--------|
| GetSubscriptionResponse | Subscription | ErrorList |
| CreateSubscriptionResponse | Subscription | ErrorList |
| GetSubscriptionByIdResponse | Subscription | ErrorList |
| DeleteSubscriptionByIdResponse | - | ErrorList |
| GetDestinationsResponse | DestinationList (array[Destination]) | ErrorList |
| CreateDestinationResponse | Destination | ErrorList |
| GetDestinationResponse | Destination | ErrorList |
| DeleteDestinationResponse | - | ErrorList |

---

## Common Response Headers
| Header | Type | Description |
|--------|------|-------------|
| x-amzn-RateLimit-Limit | string | Usage plan rate limits |
| x-amzn-RequestId | string | Unique request reference (not on 403) |

---

## Notification Types (Common)
- ANY_OFFER_CHANGED - Any offer changed on a listing
- ORDER_CHANGE - Order status or buyer-requested change
- FEED_PROCESSING_FINISHED - Feed processing completed
- REPORT_PROCESSING_FINISHED - Report processing completed
- BRANDED_ITEM_CONTENT_CHANGE - A+ content changed
- ITEM_PRODUCT_TYPE_CHANGE - Product type changed
- FBA_OUTBOUND_SHIPMENT_STATUS - FBA shipment status change
- LISTINGS_ITEM_STATUS_CHANGE - Listing status changed
- LISTINGS_ITEM_ISSUES_CHANGE - Listing issues changed
- LISTINGS_ITEM_MFN_QUANTITY_CHANGE - MFN quantity changed

---

## Notes for GoAmrita Bhandar
- Use EU endpoint: sellingpartnerapi-eu.amazon.com
- Grantless operations can be called without seller authorization
- SQS or EventBridge destinations supported
- For India marketplace, use appropriate AWS region (ap-south-1)
