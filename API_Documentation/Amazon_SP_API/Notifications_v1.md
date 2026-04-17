# Selling Partner API for Notifications v1
## Official OpenAPI Spec Documentation
**Source:** https://github.com/amzn/selling-partner-api-models/blob/main/models/notifications-api-model/notifications.json
**Fetched:** 2026-04-13
**Spec Version:** Swagger 2.0
**API Version:** v1

---

## API Info
- **Title:** Selling Partner API for Notifications
- **Description:** Subscribe to notifications relevant to selling partner business. Manage destinations and subscriptions.
- **Host:** sellingpartnerapi-na.amazon.com (use `sellingpartnerapi-eu.amazon.com` for India/EU)
- **Schemes:** HTTPS
- **Consumes:** application/json
- **Produces:** application/json
- **License:** Apache License 2.0

---

## Endpoints

### 1. GET /notifications/v1/subscriptions/{notificationType}
**Operation:** getSubscription
**Description:** Returns subscription information for the specified notification type (for the application, not a specific seller).

**Parameters:**
| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| notificationType | path | string | Yes | The type of notification |
| payloadVersion | query | string | No | The version of the payload object to be used in the notification |

**Responses:**
| Status | Description | Schema |
|--------|-------------|--------|
| 200 | Success | GetSubscriptionResponse |
| 400 | Invalid parameters | ErrorList |
| 403 | Access forbidden | ErrorList |
| 404 | Resource not found | ErrorList |
| 413 | Request size exceeded | ErrorList |
| 415 | Unsupported format | ErrorList |
| 429 | Rate limit exceeded | ErrorList |
| 500 | Server error | ErrorList |
| 503 | Service unavailable | ErrorList |

---

### 2. POST /notifications/v1/subscriptions/{notificationType}
**Operation:** createSubscription
**Description:** Creates a subscription for the specified notification type.

**Parameters:**
| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| notificationType | path | string | Yes | The notification type |
| body | body | CreateSubscriptionRequest | Yes | Subscription details |

**Responses:** Same as above + `409 Conflict`

---

### 3. GET /notifications/v1/subscriptions/{notificationType}/{subscriptionId}
**Operation:** getSubscriptionById
**Description:** Returns information about a subscription for the specified notification type.

**Parameters:**
| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| notificationType | path | string | Yes | The notification type |
| subscriptionId | path | string | Yes | The subscription identifier |

**Responses:** Same as endpoint 1 + `409 Conflict`

---

### 4. DELETE /notifications/v1/subscriptions/{notificationType}/{subscriptionId}
**Operation:** deleteSubscriptionById
**Description:** Deletes the subscription indicated by the subscription identifier.

**Parameters:**
| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| notificationType | path | string | Yes | The notification type |
| subscriptionId | path | string | Yes | The subscription identifier to delete |

**Responses:** Same as above

---

### 5. GET /notifications/v1/destinations
**Operation:** getDestinations
**Description:** Returns information about all destinations.

**Parameters:** None

**Responses:** Returns GetDestinationsResponse

---

### 6. POST /notifications/v1/destinations
**Operation:** createDestination
**Description:** Creates a destination resource to receive notifications.

**Parameters:**
| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| body | body | CreateDestinationRequest | Yes | Destination details |

**Responses:** Returns CreateDestinationResponse

---

### 7. GET /notifications/v1/destinations/{destinationId}
**Operation:** getDestination
**Description:** Returns information about the destination that you specify.

**Parameters:**
| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| destinationId | path | string | Yes | The destination identifier |

**Responses:** Returns GetDestinationResponse

---

### 8. DELETE /notifications/v1/destinations/{destinationId}
**Operation:** deleteDestination
**Description:** Deletes the destination that you specify.

**Parameters:**
| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| destinationId | path | string | Yes | The destination identifier to delete |

**Responses:** Returns DeleteDestinationResponse

---

## Data Models

### Subscription
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| subscriptionId | string | Yes | The subscription identifier generated at creation |
| payloadVersion | string | Yes | The version of the payload object used in notification |
| destinationId | string | Yes | The destination identifier |
| processingDirective | ProcessingDirective | No | Additional processing controls |

### ProcessingDirective
| Property | Type | Description |
|----------|------|-------------|
| eventFilter | EventFilter | Notification type specific filter |

### EventFilter
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| eventFilterType | string | Yes | Enum: `ANY_OFFER_CHANGED`, `ORDER_CHANGE` |
| marketplaceIds | MarketplaceIds | No | List of marketplace IDs to filter |
| aggregationSettings | AggregationSettings | No | Aggregation configuration |
| orderChangeTypes | OrderChangeTypes | No | Order change type filter |

### AggregationSettings
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| aggregationTimePeriod | AggregationTimePeriod | Yes | Enum: `FiveMinutes`, `TenMinutes` |

### OrderChangeTypes
Type: array of OrderChangeTypeEnum
- **OrderChangeTypeEnum values:** `OrderStatusChange`, `BuyerRequestedChange`

### MarketplaceIds
Type: array of strings (marketplace identifiers)

### Destination
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| name | string (max 256) | Yes | Developer-defined name for destination |
| destinationId | string | Yes | Destination identifier generated at creation |
| resource | DestinationResource | Yes | Destination resource details |

### DestinationResource
| Property | Type | Description |
|----------|------|-------------|
| sqs | SqsResource | Amazon SQS destination |
| eventBridge | EventBridgeResource | Amazon EventBridge destination |

### SqsResource
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| arn | string (max 1000) | Yes | ARN of the SQS queue. Pattern: `^arn:aws:sqs:\S+:\S+:\S+` |

### EventBridgeResource
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| name | string (max 256) | Yes | Partner event source name |
| region | string | Yes | AWS region for receiving notifications |
| accountId | string | Yes | AWS account ID responsible for charges |

### EventBridgeResourceSpecification (for creating)
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| region | string | Yes | AWS region |
| accountId | string | Yes | AWS account ID |

### DestinationResourceSpecification (for creating)
| Property | Type | Description |
|----------|------|-------------|
| sqs | SqsResource | SQS destination spec |
| eventBridge | EventBridgeResourceSpecification | EventBridge spec |

### CreateSubscriptionRequest
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| payloadVersion | string | Yes | Payload object version |
| destinationId | string | Yes | Destination identifier |
| processingDirective | ProcessingDirective | No | Processing controls |

### CreateDestinationRequest
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| name | string | Yes | Developer-defined name |
| resourceSpecification | DestinationResourceSpecification | Yes | Resource spec |

### Response Wrappers
All response models follow the pattern:
| Property | Type | Description |
|----------|------|-------------|
| payload | (varies) | Response data |
| errors | ErrorList | Error details if unsuccessful |

- **GetSubscriptionResponse** - payload: Subscription
- **CreateSubscriptionResponse** - payload: Subscription
- **GetSubscriptionByIdResponse** - payload: Subscription
- **DeleteSubscriptionByIdResponse** - errors only
- **GetDestinationsResponse** - payload: array[Destination]
- **GetDestinationResponse** - payload: Destination
- **CreateDestinationResponse** - payload: Destination
- **DeleteDestinationResponse** - errors only

### Error
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| code | string | Yes | Error code identifying the type |
| message | string | Yes | Error condition description |
| details | string | No | Additional context |

---

## Supported Notification Types
Common notification types include:
- `ANY_OFFER_CHANGED` - Buy Box or offer changes
- `ORDER_CHANGE` - Order status changes
- `FEED_PROCESSING_FINISHED` - Feed processing complete
- `REPORT_PROCESSING_FINISHED` - Report processing complete
- `FBA_OUTBOUND_SHIPMENT_STATUS` - FBA shipment status
- `LISTINGS_ITEM_STATUS_CHANGE` - Listing status changes
- `LISTINGS_ITEM_ISSUES_CHANGE` - Listing issues changes
- `B2B_ANY_OFFER_CHANGED` - B2B offer changes
- `ITEM_INVENTORY_EVENT_CHANGE` - Inventory events
- `BRANDED_ITEM_CONTENT_CHANGE` - Brand content changes

---

## Rate Limits
| Operation | Rate | Burst |
|-----------|------|-------|
| getSubscription | 1 req/sec | 5 |
| createSubscription | 1 req/sec | 5 |
| getSubscriptionById | 1 req/sec | 5 |
| deleteSubscriptionById | 1 req/sec | 5 |
| getDestinations | 1 req/sec | 5 |
| createDestination | 1 req/sec | 5 |
| getDestination | 1 req/sec | 5 |
| deleteDestination | 1 req/sec | 5 |

---

## Important Notes for GoAmrita Bhandar
- **Region:** India = EU endpoint (`sellingpartnerapi-eu.amazon.com`)
- **Destination Types:** SQS (recommended) or EventBridge
- Use `ORDER_CHANGE` notification for real-time order tracking
- Use `ANY_OFFER_CHANGED` for Buy Box monitoring
- `LISTINGS_ITEM_STATUS_CHANGE` useful for tracking listing health
- Aggregation periods: 5 or 10 minutes (reduces notification volume)
