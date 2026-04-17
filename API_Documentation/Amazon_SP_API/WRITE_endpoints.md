# SP-API WRITE/MODIFY Endpoints Reference v1.0
## GoAmrita Bhandar / Made in Heavens

**Last Updated:** 13 April 2026
**Region:** EU (India marketplace)
**Base URL:** `https://sellingpartnerapi-eu.amazon.com`
**Marketplace ID:** `A21TJRUUN4KGV`

---

## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
## !!!  DANGER ZONE: ALL ENDPOINTS IN THIS FILE MODIFY LIVE DATA  !!!
## !!!  EVERY WRITE CALL AFFECTS THE REAL SELLER ACCOUNT           !!!
## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

---

## Common Headers (Required for ALL Write Requests)

```
x-amz-access-token: {LWA_access_token}
x-amz-date: {ISO8601_timestamp}
Host: sellingpartnerapi-eu.amazon.com
Content-Type: application/json
User-Agent: GoAmrita/1.0 (Language=Python/3; Platform=Windows)
```

### Authentication
Same LWA flow as READ endpoints:
1. POST `https://api.amazon.com/auth/o2/token` with refresh_token
2. Get access_token (valid 1 hour)
3. Pass in `x-amz-access-token` header

---

## 1. Feeds API v2021-06-30

**Role Required:** Product Listing, Pricing, Inventory and Order Tracking
**Use Case:** Bulk updates to prices, inventory, listings via JSON feed documents.

### DANGER LEVEL: HIGH
### A single malformed feed can change prices/inventory for ALL products at once.

---

### Step-by-Step Feed Submission Process:

#### Step 1: Create Feed Document (get upload URL)

### POST /feeds/2021-06-30/documents

**Description:** Create a feed document and get a presigned URL to upload feed content.

**Rate Limit:** Burst: 15, Restore: 2/sec

**Request Body:**
```json
{
  "contentType": "application/json; charset=UTF-8"
}
```

**Response:**
```json
{
  "feedDocumentId": "amzn1.tortuga.4.eu.XXXXXXXX",
  "url": "https://tortuga-prod-eu.s3-eu-west-1.amazonaws.com/...",
  "encryptionDetails": {
    "standard": "AES",
    "initializationVector": "...",
    "key": "..."
  }
}
```

**Action Required:** Upload your JSON feed content to the `url` via HTTP PUT.

#### Step 2: Upload Feed Content to S3

**HTTP PUT to the presigned URL from Step 1**

```
PUT {presigned_url}
Content-Type: application/json; charset=UTF-8

{feed_content}
```

#### Step 3: Submit the Feed

### POST /feeds/2021-06-30/feeds

**Description:** Submit a feed for processing.

**Rate Limit:** Burst: 15, Restore: 2/sec

**Request Body:**
```json
{
  "feedType": "JSON_LISTINGS_FEED",
  "marketplaceIds": ["A21TJRUUN4KGV"],
  "inputFeedDocumentId": "amzn1.tortuga.4.eu.XXXXXXXX"
}
```

**Response:**
```json
{
  "feedId": "FeedId-XXXXXX"
}
```

#### Step 4: Check Feed Processing Status

### GET /feeds/2021-06-30/feeds/{feedId}

**Rate Limit:** Burst: 15, Restore: 2/sec

**Response:**
```json
{
  "feedId": "FeedId-XXXXXX",
  "feedType": "JSON_LISTINGS_FEED",
  "marketplaceIds": ["A21TJRUUN4KGV"],
  "processingStatus": "DONE",
  "resultFeedDocumentId": "amzn1.tortuga.4.eu.YYYYYYYY"
}
```

**processingStatus values:** `CANCELLED`, `DONE`, `FATAL`, `IN_PROGRESS`, `IN_QUEUE`

#### Step 5: Get Processing Results

### GET /feeds/2021-06-30/documents/{resultFeedDocumentId}

Download the result document URL, decompress, and check for errors.

---

### Feed Types We Need:

#### A. JSON_LISTINGS_FEED (Primary - Recommended)

For updating listings via JSON Patch format. This is the modern approach.

**Feed Content Format (for price update):**

```json
{
  "header": {
    "sellerId": "ENTITY1TVPGA5B1GOJW",
    "version": "2.0",
    "issueLocale": "en_US"
  },
  "messages": [
    {
      "messageId": 1,
      "sku": "SKU-001",
      "operationType": "PATCH",
      "productType": "GROCERY",
      "patches": [
        {
          "op": "replace",
          "path": "/attributes/purchasable_offer",
          "value": [
            {
              "marketplace_id": "A21TJRUUN4KGV",
              "currency": "INR",
              "our_price": [
                {
                  "schedule": [
                    {
                      "value_with_tax": 299.00
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

**Feed Content Format (for inventory update):**

```json
{
  "header": {
    "sellerId": "ENTITY1TVPGA5B1GOJW",
    "version": "2.0",
    "issueLocale": "en_US"
  },
  "messages": [
    {
      "messageId": 1,
      "sku": "SKU-001",
      "operationType": "PATCH",
      "productType": "GROCERY",
      "patches": [
        {
          "op": "replace",
          "path": "/attributes/fulfillment_availability",
          "value": [
            {
              "fulfillment_channel_code": "DEFAULT",
              "quantity": 100,
              "marketplace_id": "A21TJRUUN4KGV"
            }
          ]
        }
      ]
    }
  ]
}
```

#### B. POST_FLAT_FILE_PRICEANDQUANTITYONLY_UPDATE_DATA (Legacy TSV)

Legacy flat-file feed for simple price + quantity updates. Still supported.

**Feed Content (TSV):**
```
sku	price	minimum-seller-allowed-price	maximum-seller-allowed-price	quantity	leadtime-to-ship
SKU-001	299	199	499	100	1
SKU-002	599	399	799	50	1
```

#### C. POST_PRODUCT_PRICING_DATA (Legacy XML)

Legacy XML feed for pricing updates. Use JSON_LISTINGS_FEED instead.

### Feed Types Reference:

| Feed Type | Purpose | Format | Danger |
|-----------|---------|--------|--------|
| `JSON_LISTINGS_FEED` | Update any listing attribute | JSON | HIGH |
| `POST_FLAT_FILE_PRICEANDQUANTITYONLY_UPDATE_DATA` | Price + inventory only | TSV | MEDIUM |
| `POST_PRODUCT_DATA` | Create/update products | XML | VERY HIGH |
| `POST_INVENTORY_AVAILABILITY_DATA` | Update inventory | XML | HIGH |
| `POST_PRODUCT_PRICING_DATA` | Update pricing | XML | HIGH |
| `POST_PRODUCT_IMAGE_DATA` | Update images | XML | MEDIUM |
| `POST_FLAT_FILE_LISTINGS_DATA` | Create/update listings | TSV | VERY HIGH |
| `POST_FLAT_FILE_INVLOADER_DATA` | Inventory loader | TSV | HIGH |

### What Could Go Wrong:
- Setting price to 0 or 1 INR = Amazon auto-flags account, potential suspension
- Setting quantity to 0 = listings go inactive
- Wrong SKU mapping = wrong product gets updated
- Malformed feed = partial processing, some items updated, some not
- No rollback mechanism = must submit corrective feed

---

## 2. Listings Items API v2021-08-01

**Role Required:** Product Listing
**Use Case:** Update individual listing attributes (price, title, description, images, etc.)

### DANGER LEVEL: MEDIUM-HIGH
### Changes individual listings. Safer than feeds but still affects live listings.

---

### PUT /listings/2021-08-01/items/{sellerId}/{sku}

**Description:** Create or fully replace a listing.

| Parameter | Location | Required | Type | Description |
|-----------|----------|----------|------|-------------|
| `sellerId` | path | Yes | string | Our seller ID |
| `sku` | path | Yes | string | SKU to update |
| `marketplaceIds` | query | Yes | string[] | `A21TJRUUN4KGV` |
| `issueLocale` | query | No | string | `en_US` |

**Rate Limit:** Burst: 5, Restore: 5/sec

**Request Body (Full Replace):**
```json
{
  "productType": "GROCERY",
  "requirements": "LISTING",
  "attributes": {
    "item_name": [{ "value": "GoAmrita Pure Desi Ghee 500ml", "marketplace_id": "A21TJRUUN4KGV" }],
    "brand": [{ "value": "GoAmrita" }],
    "manufacturer": [{ "value": "GoAmrita Bhandar" }],
    "purchasable_offer": [{
      "marketplace_id": "A21TJRUUN4KGV",
      "currency": "INR",
      "our_price": [{
        "schedule": [{
          "value_with_tax": 599.00
        }]
      }]
    }],
    "fulfillment_availability": [{
      "fulfillment_channel_code": "DEFAULT",
      "quantity": 100,
      "marketplace_id": "A21TJRUUN4KGV"
    }],
    "condition_type": [{ "value": "new_new" }],
    "merchant_suggested_asin": [{ "value": "B0XXXXXXXX" }]
  }
}
```

**Response:**
```json
{
  "sku": "SKU-001",
  "status": "ACCEPTED",
  "submissionId": "...",
  "issues": []
}
```

**status values:** `ACCEPTED`, `INVALID`

### PATCH /listings/2021-08-01/items/{sellerId}/{sku}

**Description:** Partially update a listing (recommended for targeted changes).

**Rate Limit:** Burst: 5, Restore: 5/sec

**Request Body (Price Update Only):**
```json
{
  "productType": "GROCERY",
  "patches": [
    {
      "op": "replace",
      "path": "/attributes/purchasable_offer",
      "value": [{
        "marketplace_id": "A21TJRUUN4KGV",
        "currency": "INR",
        "our_price": [{
          "schedule": [{
            "value_with_tax": 549.00
          }]
        }]
      }]
    }
  ]
}
```

**Request Body (Inventory Update Only):**
```json
{
  "productType": "GROCERY",
  "patches": [
    {
      "op": "replace",
      "path": "/attributes/fulfillment_availability",
      "value": [{
        "fulfillment_channel_code": "DEFAULT",
        "quantity": 75,
        "marketplace_id": "A21TJRUUN4KGV"
      }]
    }
  ]
}
```

**Request Body (Title Update):**
```json
{
  "productType": "GROCERY",
  "patches": [
    {
      "op": "replace",
      "path": "/attributes/item_name",
      "value": [{ "value": "GoAmrita Premium Pure Desi Ghee 500ml - A2 Cow", "marketplace_id": "A21TJRUUN4KGV" }]
    }
  ]
}
```

### DELETE /listings/2021-08-01/items/{sellerId}/{sku}

**Description:** Delete a listing.

| Parameter | Location | Required | Type | Description |
|-----------|----------|----------|------|-------------|
| `sellerId` | path | Yes | string | Our seller ID |
| `sku` | path | Yes | string | SKU to delete |
| `marketplaceIds` | query | Yes | string[] | `A21TJRUUN4KGV` |
| `issueLocale` | query | No | string | `en_US` |

**Rate Limit:** Burst: 5, Restore: 5/sec

### DANGER LEVEL: VERY HIGH - Permanently removes listing!

### GET /listings/2021-08-01/items/{sellerId}/{sku}

**Description:** Get current listing details (READ - safe to call).

| Parameter | Location | Required | Type | Description |
|-----------|----------|----------|------|-------------|
| `sellerId` | path | Yes | string | Our seller ID |
| `sku` | path | Yes | string | SKU |
| `marketplaceIds` | query | Yes | string[] | `A21TJRUUN4KGV` |
| `issueLocale` | query | No | string | `en_US` |
| `includedData` | query | No | string[] | `summaries`, `attributes`, `issues`, `offers`, `fulfillmentAvailability`, `procurement` |

**Rate Limit:** Burst: 5, Restore: 5/sec

### What Could Go Wrong:
- PUT replaces ENTIRE listing - missing fields get blanked out
- Wrong productType = listing rejected or miscategorized
- Title changes may trigger Amazon review (24-48hr delay)
- Price outside allowed range = listing suppressed
- DELETE is permanent, cannot be undone easily
- Bulk PATCH operations could overwhelm rate limits

---

## 3. Pricing Update (via Listings Items API)

**Role Required:** Pricing
**Use Case:** Update price for individual products.

### DANGER LEVEL: HIGH
### Wrong price = financial loss or account suspension

---

### Recommended: Use Listings Items API PATCH

See Section 2 above. The PATCH endpoint is the safest way to update individual prices.

**Price Update Example:**
```
PATCH /listings/2021-08-01/items/ENTITY1TVPGA5B1GOJW/SKU-001?marketplaceIds=A21TJRUUN4KGV
```

```json
{
  "productType": "GROCERY",
  "patches": [
    {
      "op": "replace",
      "path": "/attributes/purchasable_offer",
      "value": [{
        "marketplace_id": "A21TJRUUN4KGV",
        "currency": "INR",
        "our_price": [{
          "schedule": [{
            "value_with_tax": 449.00
          }]
        }]
      }]
    }
  ]
}
```

### Pricing Safety Rules:
1. NEVER set price below cost
2. NEVER set price below Amazon's minimum allowed price
3. NEVER set price above Amazon's maximum allowed price
4. ALWAYS validate price against current price before updating
5. Set `minimum-seller-allowed-price` and `maximum-seller-allowed-price` as guardrails
6. Log every price change with timestamp, old price, new price
7. Implement price change limits (e.g., max 20% change per day)

### What Could Go Wrong:
- Price set too low = selling at loss on every order
- Price set to 0 = Amazon may suppress listing + flag account
- Price set too high = Buy Box loss, no sales
- Price war loop = automated repricing spirals prices to floor
- Missing currency code = defaults may cause issues
- Tax-inclusive vs tax-exclusive confusion in India (Amazon India uses tax-inclusive pricing)

---

## 4. Notifications API v1 (Write Operations)

**Role Required:** Various
**Use Case:** Create/delete notification subscriptions and destinations.

### DANGER LEVEL: LOW
### Only creates/removes event subscriptions. Does not modify products or pricing.

---

### POST /notifications/v1/destinations

**Description:** Create a notification destination (SQS queue or EventBridge).

**Rate Limit:** Burst: 5, Restore: 1/sec

**Request Body (SQS):**
```json
{
  "name": "GoAmrita_SP_Notifications",
  "resourceSpecification": {
    "sqs": {
      "arn": "arn:aws:sqs:eu-west-1:123456789012:goamrita-sp-notifications"
    }
  }
}
```

**Request Body (EventBridge):**
```json
{
  "name": "GoAmrita_EventBridge",
  "resourceSpecification": {
    "eventBridge": {
      "region": "eu-west-1",
      "accountId": "123456789012"
    }
  }
}
```

**Response:**
```json
{
  "payload": {
    "destinationId": "dest-XXXXXXXX",
    "name": "GoAmrita_SP_Notifications",
    "resource": {
      "sqs": {
        "arn": "arn:aws:sqs:eu-west-1:123456789012:goamrita-sp-notifications"
      }
    }
  }
}
```

### POST /notifications/v1/subscriptions/{notificationType}

**Description:** Create a subscription for a notification type.

| Parameter | Location | Required | Type | Description |
|-----------|----------|----------|------|-------------|
| `notificationType` | path | Yes | string | e.g., `ANY_OFFER_CHANGED` |

**Rate Limit:** Burst: 5, Restore: 1/sec

**Request Body:**
```json
{
  "payloadVersion": "1.0",
  "destinationId": "dest-XXXXXXXX",
  "processingDirective": {
    "eventFilter": {
      "eventFilterType": "ANY_OFFER_CHANGED",
      "marketplaceIds": ["A21TJRUUN4KGV"],
      "aggregationSettings": {
        "aggregationTimePeriod": "FiveMinutes"
      }
    }
  }
}
```

**Response:**
```json
{
  "payload": {
    "subscriptionId": "sub-XXXXXXXX",
    "payloadVersion": "1.0",
    "destinationId": "dest-XXXXXXXX"
  }
}
```

### DELETE /notifications/v1/subscriptions/{notificationType}/{subscriptionId}

**Description:** Delete a subscription.

**Rate Limit:** Burst: 5, Restore: 1/sec

### DELETE /notifications/v1/destinations/{destinationId}

**Description:** Delete a destination (must delete all subscriptions first).

**Rate Limit:** Burst: 5, Restore: 1/sec

### Notification Types to Subscribe:

| Type | Priority | Why |
|------|----------|-----|
| `ANY_OFFER_CHANGED` | 1 | Detect competitor price changes, Buy Box changes |
| `ORDER_CHANGE` | 1 | Real-time order tracking |
| `LISTINGS_ITEM_STATUS_CHANGE` | 2 | Know when listings go inactive/suppressed |
| `LISTINGS_ITEM_ISSUES_CHANGE` | 2 | Quality alerts |
| `REPORT_PROCESSING_FINISHED` | 2 | Know when reports are ready |
| `FEED_PROCESSING_FINISHED` | 2 | Know when feed updates complete |
| `ACCOUNT_STATUS_CHANGED` | 1 | Critical account health alerts |
| `LISTINGS_ITEM_MFN_QUANTITY_CHANGE` | 3 | Inventory changes (MFN only) |
| `FBA_OUTBOUND_SHIPMENT_STATUS` | 3 | FBA shipment tracking |

### What Could Go Wrong:
- SQS queue not in correct region = messages never arrive
- Missing IAM permissions = subscription fails silently
- Too many subscriptions = cost + message volume management
- Not processing messages = queue fills up
- Deleting subscription accidentally = miss critical events

---

## 5. FBA Inbound Shipment API v2024-03-20

**Role Required:** Amazon Fulfilment
**Use Case:** Create and manage FBA inbound shipment plans.

### DANGER LEVEL: MEDIUM
### Creates real shipment plans. Incorrect plans = wrong inventory at wrong FC.

---

### POST /inbound/fba/2024-03-20/inboundPlans

**Description:** Create an inbound plan (first step of sending inventory to FBA).

**Rate Limit:** Burst: 2, Restore: 2/sec

**Request Body:**
```json
{
  "destinationMarketplaces": ["A21TJRUUN4KGV"],
  "items": [
    {
      "label": "AMAZON_BARCODE",
      "msku": "SKU-001",
      "prepOwner": "AMAZON",
      "quantity": 100
    }
  ],
  "name": "GoAmrita Ghee Shipment April 2026",
  "sourceAddress": {
    "addressLine1": "Shop Address Line 1",
    "city": "City",
    "countryCode": "IN",
    "name": "GoAmrita Bhandar",
    "postalCode": "000000",
    "stateOrProvinceCode": "MH"
  }
}
```

**Response:**
```json
{
  "inboundPlanId": "wf-XXXXXXXX",
  "operationId": "op-XXXXXXXX",
  "packingOptions": [...],
  "shipmentPlacements": [...]
}
```

### GET /inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}

**Description:** Get inbound plan details.

**Rate Limit:** Burst: 2, Restore: 2/sec

### PUT /inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/packingOption

**Description:** Select packing option for the plan.

### POST /inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/shipment/{shipmentId}/confirm

**Description:** Confirm a shipment (commits to sending inventory).

### DANGER LEVEL: HIGH after confirmation - Amazon expects the shipment to arrive.

### Key Workflow:
1. **Create Plan** (POST /inboundPlans) - Define items and source address
2. **Get Packing Options** - Amazon suggests how to pack
3. **Select Packing Option** (PUT) - Choose one
4. **Get Placement Options** - Amazon assigns fulfillment centers
5. **Select Placement** (PUT) - Confirm which FC
6. **Generate Transportation** - Get shipping labels/BOL
7. **Confirm Shipment** (POST) - Commit to sending
8. **Update Tracking** - Add tracking numbers

### What Could Go Wrong:
- Wrong quantity = mismatch at FC = fees + reconciliation issues
- Wrong product mapping = wrong items sent to FC
- Missing prep requirements = items refused at FC
- Cancelling after confirmation = potential fees
- Multiple FC assignments = higher shipping costs

---

## Safety Protocol for ALL Write Operations

### Pre-Flight Checklist:

```
1. [ ] Msir approval obtained for this operation
2. [ ] Test with single item first (never bulk first)
3. [ ] Verify current state BEFORE change (read first)
4. [ ] Log: timestamp, endpoint, request body, response
5. [ ] Validate all values (price > 0, quantity >= 0, etc.)
6. [ ] Compare new value vs old value (sanity check)
7. [ ] Set rate limit guards in code
8. [ ] Have rollback plan ready
9. [ ] Monitor after change (check listing, check price)
```

### Price Update Safety:

```python
# MANDATORY safety check before any price update
def validate_price_change(old_price, new_price, sku):
    if new_price <= 0:
        raise ValueError(f"BLOCKED: Price <= 0 for {sku}")
    if new_price < 10:  # Minimum INR 10 for any product
        raise ValueError(f"BLOCKED: Price < INR 10 for {sku}")
    
    change_pct = abs(new_price - old_price) / old_price * 100
    if change_pct > 30:  # Max 30% change without manual approval
        raise ValueError(f"BLOCKED: Price change {change_pct:.1f}% > 30% for {sku}. Needs manual approval.")
    
    return True
```

### Inventory Update Safety:

```python
# MANDATORY safety check before any inventory update
def validate_inventory_change(old_qty, new_qty, sku):
    if new_qty < 0:
        raise ValueError(f"BLOCKED: Negative quantity for {sku}")
    if old_qty > 0 and new_qty == 0:
        # Setting to 0 = listing goes inactive
        log.warning(f"WARNING: Setting {sku} inventory to 0 - listing will go INACTIVE")
        # Require explicit confirmation
    
    return True
```

---

## Rate Limit Implementation

```python
import time
from collections import defaultdict

class RateLimiter:
    """Token bucket rate limiter for SP-API"""
    
    def __init__(self):
        self.buckets = defaultdict(lambda: {"tokens": 0, "last_refill": time.time(), "burst": 1, "restore_rate": 1})
    
    def configure(self, endpoint, burst, restore_per_sec):
        self.buckets[endpoint] = {
            "tokens": burst,
            "last_refill": time.time(),
            "burst": burst,
            "restore_rate": restore_per_sec
        }
    
    def acquire(self, endpoint):
        bucket = self.buckets[endpoint]
        now = time.time()
        elapsed = now - bucket["last_refill"]
        bucket["tokens"] = min(bucket["burst"], bucket["tokens"] + elapsed * bucket["restore_rate"])
        bucket["last_refill"] = now
        
        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return True
        else:
            wait_time = (1 - bucket["tokens"]) / bucket["restore_rate"]
            time.sleep(wait_time)
            bucket["tokens"] = 0
            bucket["last_refill"] = time.time()
            return True

# Usage:
limiter = RateLimiter()
limiter.configure("listings_patch", burst=5, restore_per_sec=5)
limiter.configure("feeds_create", burst=15, restore_per_sec=2)
limiter.configure("pricing_batch", burst=1, restore_per_sec=0.2)  # 1 per 5 sec
```

---

## Quick Reference: Write Endpoints Summary

| API | Method | Endpoint | Danger | What It Does |
|-----|--------|----------|--------|--------------|
| Feeds | POST | /feeds/2021-06-30/documents | LOW | Get upload URL |
| Feeds | POST | /feeds/2021-06-30/feeds | HIGH | Submit feed for processing |
| Feeds | DELETE | /feeds/2021-06-30/feeds/{feedId} | LOW | Cancel pending feed |
| Listings | PUT | /listings/2021-08-01/items/{sellerId}/{sku} | HIGH | Full listing replace |
| Listings | PATCH | /listings/2021-08-01/items/{sellerId}/{sku} | MEDIUM | Partial listing update |
| Listings | DELETE | /listings/2021-08-01/items/{sellerId}/{sku} | VERY HIGH | Delete listing |
| Notifications | POST | /notifications/v1/destinations | LOW | Create event destination |
| Notifications | POST | /notifications/v1/subscriptions/{type} | LOW | Subscribe to events |
| Notifications | DELETE | /notifications/v1/subscriptions/{type}/{id} | LOW | Unsubscribe |
| Notifications | DELETE | /notifications/v1/destinations/{id} | LOW | Delete destination |
| FBA Inbound | POST | /inbound/fba/2024-03-20/inboundPlans | MEDIUM | Create shipment plan |
| FBA Inbound | POST | .../shipment/{id}/confirm | HIGH | Confirm shipment |

---

## Approval Matrix

| Operation | Danger Level | Approval Needed |
|-----------|-------------|-----------------|
| Create notification subscription | LOW | Auto-OK |
| Delete notification subscription | LOW | Auto-OK |
| Update single SKU price (< 20% change) | MEDIUM | Auto-OK with logging |
| Update single SKU price (> 20% change) | HIGH | Msir approval |
| Update single SKU inventory | MEDIUM | Auto-OK with logging |
| Set inventory to 0 | HIGH | Msir approval |
| Submit bulk feed (any type) | HIGH | Msir approval |
| PUT (full replace) listing | HIGH | Msir approval |
| PATCH listing title/description | HIGH | Msir approval |
| Delete listing | VERY HIGH | Msir approval |
| Create FBA inbound plan | MEDIUM | Msir approval |
| Confirm FBA shipment | HIGH | Msir approval |

---

## Error Handling for Write Operations

```python
import json
import time

def safe_sp_api_write(method, url, headers, body, max_retries=3):
    """Safe wrapper for all SP-API write calls"""
    
    # Step 1: Log the request
    log.info(f"SP-API WRITE: {method} {url}")
    log.info(f"Request Body: {json.dumps(body, indent=2)}")
    
    for attempt in range(max_retries):
        try:
            response = make_request(method, url, headers, body)
            
            if response.status_code == 200:
                log.info(f"SUCCESS: {response.json()}")
                return response.json()
            
            elif response.status_code == 400:
                # Bad request - don't retry, fix the input
                log.error(f"BAD REQUEST (400): {response.json()}")
                return None
            
            elif response.status_code == 401:
                # Token expired - refresh and retry
                log.warning("Token expired, refreshing...")
                headers["x-amz-access-token"] = refresh_lwa_token()
                continue
            
            elif response.status_code == 403:
                # Forbidden - check role permissions
                log.error(f"FORBIDDEN (403): {response.json()}")
                log.error("Check: correct region? correct role? app approved?")
                return None
            
            elif response.status_code == 429:
                # Rate limited - wait and retry
                retry_after = int(response.headers.get("Retry-After", 2))
                log.warning(f"Rate limited. Waiting {retry_after}s...")
                time.sleep(retry_after * (attempt + 1))  # Exponential backoff
                continue
            
            elif response.status_code >= 500:
                # Server error - retry with backoff
                wait = 2 ** attempt
                log.warning(f"Server error {response.status_code}. Retrying in {wait}s...")
                time.sleep(wait)
                continue
            
        except Exception as e:
            log.error(f"Exception on attempt {attempt + 1}: {e}")
            time.sleep(2 ** attempt)
    
    log.error(f"FAILED after {max_retries} attempts: {method} {url}")
    return None
```

---

## Testing Strategy for Write Operations

### Phase 1: Dry Run (No actual API call)
- Validate all parameters locally
- Check price/inventory ranges
- Log what WOULD be changed
- Verify against current state

### Phase 2: Single Item Test
- Pick ONE low-risk SKU
- Make ONE small change (e.g., price +1 INR)
- Verify change on Seller Central
- Verify via read API
- Revert if needed

### Phase 3: Small Batch Test
- 3-5 items via feed
- Monitor processing results
- Check for errors in result feed
- Verify all items on Seller Central

### Phase 4: Production
- Full batch with all safety checks
- Real-time monitoring
- Automated rollback ready

---

*Document Version: 1.0 | Created: 13 April 2026*
*Source: Amazon SP-API Official Documentation (developer-docs.amazon.com/sp-api)*

## REMINDER: ALL WRITE OPERATIONS NEED MSIR APPROVAL BEFORE FIRST TEST
## NEVER test write operations on live account without explicit approval
