# ⚠️ Amazon Official API Guidelines — MUST READ BEFORE DEVELOPMENT
**Source:** Official Amazon Advertising API documentation (https://advertising.amazon.com/API/docs/en-us)
**Date Captured:** 13 April 2026
**Purpose:** Avoid bugs, problems, trial-error. Follow these rules strictly!
**Rule:** Every developer MUST read this BEFORE writing any API code
**Covers:** Amazon Ads API (SP, SB, SD, DSP) — concepts, limits, rate limiting, versioning, developer notes, common models, reporting v3
**Version Classification:** UNIVERSAL (applies to all API versions) unless marked otherwise

---

## Table of Contents
1. [Region & Endpoint Rules](#1-region--endpoint-rules)
2. [Authentication & Authorization Rules](#2-authentication--authorization-rules)
3. [Rate Limiting & Throttling Best Practices](#3-rate-limiting--throttling-best-practices)
4. [Error Handling Guidelines](#4-error-handling-guidelines)
5. [Request/Response Formatting Rules](#5-requestresponse-formatting-rules)
6. [Pagination & Data Consistency](#6-pagination--data-consistency)
7. [Versioning & Compatibility Policy](#7-versioning--compatibility-policy)
8. [Deprecation Policies](#8-deprecation-policies)
9. [Entity Management Rules](#9-entity-management-rules)
10. [Reporting API Guidelines](#10-reporting-api-guidelines)
11. [Limits, Constraints & Quotas (India Marketplace)](#11-limits-constraints--quotas-india-marketplace)
12. [Common Model & Entity Structure](#12-common-model--entity-structure)
13. [SDK Generation Guidelines](#13-sdk-generation-guidelines)
14. [Common Mistakes to Avoid](#14-common-mistakes-to-avoid)
15. [Testing Guidelines](#15-testing-guidelines)
16. [Security Requirements](#16-security-requirements)
17. [ADD TO OUR RULES — Gaps Found](#17-add-to-our-rules--gaps-found)

---

## 1. Region & Endpoint Rules
**Classification:** UNIVERSAL

### Rule: Use the correct regional endpoint for your marketplace
| URL | Region | Marketplaces |
|-----|--------|-------------|
| `https://advertising-api.amazon.com` | North America (NA) | US, CA, MX, BR |
| `https://advertising-api-eu.amazon.com` | Europe (EU) | UK, FR, IT, ES, DE, NL, AE, PL, TR, EG, SA, SE, BE, **IN**, ZA |
| `https://advertising-api-fe.amazon.com` | Far East (FE) | JP, AU, SG |

**WHY IT MATTERS:** India (IN) is in the EUROPE region, NOT Far East. Using wrong endpoint = 403 Forbidden errors. We already made this mistake once (see our mistake log #1).

### Rule: Rate limits are determined per-region
**WHY IT MATTERS:** Report generation queues and rate limit tiers are region-specific. High usage in EU affects all EU marketplaces including India.

---

## 2. Authentication & Authorization Rules
**Classification:** UNIVERSAL

### Rule: Use OAuth 2.0 delegated access for all operations
Applications must be delegated access through an OAuth 2.0 flow. Tokens from this process are used for ALL API operations.

**WHY IT MATTERS:** Without proper OAuth flow, every API call fails with 401.

### Rule: Always pass the correct scope/account headers
- **`Amazon-Advertising-API-Scope`**: Required for most sponsored ads requests. Use Profiles API to get profile ID.
- **`Amazon-Ads-AccountId`**: Required for ADSP and cross-product requests.
- **`Amazon-Ads-Manager-AccountId`**: For manager account operations.
- **`Amazon-Advertising-API-ClientId`**: Required on all requests — your client identifier.
- **`Authorization`**: Bearer token (Ads API) or `x-amz-access-token` (SP-API).

**WHY IT MATTERS:** Missing scope header = 401 "Scope header is missing". Wrong scope = 401 "Not authorized to access scope". Different APIs use different auth headers (our mistake #5).

### Rule: Understand the account model
- **Profile ID** = used for sponsored ads operations (Scope header)
- **Account ID** = used for cross-product/DSP operations (AccountId header)
- **Body field `advertiserAccount.id`** = for specifying accounts in request bodies

**WHY IT MATTERS:** Mixing up profile ID vs account ID causes silent auth failures.

---

## 3. Rate Limiting & Throttling Best Practices
**Classification:** UNIVERSAL — CRITICAL SECTION

### Rule: Handle 429 responses with the Retry-After header
When rate-limited, the response includes a `Retry-After` header with the number of seconds to wait before retrying. Rate limiting is dynamic based on overall system load.

**WHY IT MATTERS:** Ignoring Retry-After = wasting API quota, cascading failures, potential temporary bans.

### Rule: Use exponential backoff for ALL retries
For 429 and 5xx errors, implement exponential backoff: wait 2s, then 4s, then 8s, etc. Set a maximum delay interval AND maximum number of retries.

**WHY IT MATTERS:** Linear retries during high-load periods make the problem worse for everyone and extend your throttling duration.

### Rule: Do NOT call "list extended data" operations unless you need entity status
Extended data calls hold **5x the weight** of standard calls towards throttling limits. They are expensive to process. Only use them when you specifically need computed/inherited status.

**WHY IT MATTERS:** Using extended data calls casually = hitting rate limits 5x faster than necessary. [ADD TO OUR RULES]

### Rule: Use exports instead of listing all entities
Listing all entities via batch GET requires thousands of API calls and doesn't scale. Use async exports instead — they are more efficient for bulk entity retrieval.

**WHY IT MATTERS:** Thousands of list calls = guaranteed rate limiting. Exports = one async request for everything.

### Rule: Distribute report requests throughout the day
Report rate limits vary by time of day (higher limits during low-usage, lower during peak). Spread report generation across the day; avoid large batches.

**WHY IT MATTERS:** Sending all report requests at once during peak hours = most get 429'd, wasting hours of retry time.

### Rule: Use longer backoff periods for report generation
Dynamic rate limits for reporting are unlikely to change over short periods. Short retries waste time.

**WHY IT MATTERS:** Report 429s need minutes of backoff, not seconds. Short retries just burn through your retry budget.

### Rule: Calculate inherited status locally instead of requesting extended attributes repeatedly
Extended GETs (with computed/inherited status) are inherently costlier. Store parent/grandparent status locally and compute inherited status yourself.

**WHY IT MATTERS:** Requesting extended attributes multiple times per day = unnecessary API load and rate limiting. [ADD TO OUR RULES]

---

## 4. Error Handling Guidelines
**Classification:** UNIVERSAL

### Rule: Handle ALL these status codes in your client

| Status Code | Meaning | Action |
|-------------|---------|--------|
| 200 | OK | Process response |
| 202 | Accepted | Request is processing (async). Poll for result. |
| 207 | Multi-status | Batch response — check EACH sub-request's status. Can contain both successes and errors! |
| 307 | Temporary Redirect | Follow redirect (usually file download). |
| 400 | Bad Request | Fix the request — don't retry without changes. |
| 401 | Unauthorized | Check auth token, scope header, permissions. |
| 403 | Forbidden | No access to resource — check permissions/endpoint. |
| 404 | Not Found | Resource doesn't exist or not visible for auth user. |
| 406 | Not Acceptable | Wrong Accept header. |
| 415 | Unsupported Media Type | Wrong Content-Type header. |
| 422 | Unprocessable Entity | Request understood but parameters incorrect. |
| 425 | Too Early | Duplicate of a processing request (reports). |
| 429 | Too Many Requests | Rate limited — use Retry-After header. |
| 500/502/504 | Server Error | Retry with exponential backoff. |

**WHY IT MATTERS:** Not handling 207 properly = thinking a batch succeeded when individual items failed. Not handling 425 = creating duplicate reports.

### Rule: Error response format is standardized
```json
{
  "code": "string (enumerated error code for machine use)",
  "details": "string (human-readable description)"
}
```
**WHY IT MATTERS:** Parse the `code` field for programmatic error handling, `details` for logging/debugging.

### Rule: Classify errors into three categories for retry logic
1. **Server errors (5xx)**: Retry with exponential backoff
2. **Throttling errors (429)**: Retry with exponential backoff + Retry-After
3. **Client errors (4xx except 429)**: Do NOT retry — investigate and fix the request first

**WHY IT MATTERS:** Retrying client errors wastes quota and never succeeds. Not retrying server errors means missing transient failures. [ADD TO OUR RULES]

---

## 5. Request/Response Formatting Rules
**Classification:** UNIVERSAL

### Rule: Use correct Content-Type headers for versioned resources
Some resources use content negotiation via Accept and Content-Type headers to determine version. Others use URL path (e.g., `/v2` in path). Check each resource's specification.

**WHY IT MATTERS:** Wrong Content-Type = 415 error or wrong version of data returned.

### Rule: Report creation requires specific Content-Type
- Request: `application/vnd.createasyncreportrequest.v3+json`
- Response: `application/vnd.createasyncreportresponse.v3+json`

**WHY IT MATTERS:** Using generic `application/json` for reporting endpoints = 400 or 415 errors. [ADD TO OUR RULES]

### Rule: Object IDs are 64-bit unsigned integers
IDs are in the range of 64-bit unsigned integers. IDs are unique per type within a Profile, but two different entity types CAN share the same ID.

**WHY IT MATTERS:** Using 32-bit integers = overflow/truncation. Assuming IDs are globally unique across types = data corruption.

### Rule: Dates use YYYY-MM-DD format for reports
Reports use `startDate` and `endDate` in YYYY-MM-DD format. Maximum lookback window is 95 days for most report types.

**WHY IT MATTERS:** Wrong date format = 400 error. Exceeding lookback window = error with no data returned.

---

## 6. Pagination & Data Consistency
**Classification:** UNIVERSAL

### Rule: Pagination may produce duplicate or missing records
Each page request is made independently. Results are ordered consistently, but the underlying data can change between pages. Entity exports and reports do NOT have this problem.

**WHY IT MATTERS:** If you're syncing entity data via pagination, you may miss entities or process duplicates. Use exports for consistent full data sets. [ADD TO OUR RULES]

### Rule: Use exports for bulk data synchronization
Exports provide a consistent snapshot. Use paginated batch GETs only for targeted queries, not full account syncs.

**WHY IT MATTERS:** Paginated full-account sync = inconsistent data + thousands of API calls. Exports = consistent + single request.

---

## 7. Versioning & Compatibility Policy
**Classification:** UNIVERSAL

### Rule: Resources are independently versioned using major.minor format
Each resource has its own version. Changes within a major version are backwards compatible.

**WHY IT MATTERS:** A version bump in campaigns doesn't affect keywords. Track versions per resource, not globally.

### Rule: Non-breaking changes can happen within a version WITHOUT notice
New optional fields, new enum values in responses, and other additive changes can appear within a version.

**WHY IT MATTERS:** Your code must tolerate unknown fields and new enum values. Don't fail on unexpected response data. [ADD TO OUR RULES]

### Rule: New enum values in responses are NOT considered breaking changes
The addition of a new enum value to an existing field is generally not a breaking change and won't require a version increment.

**WHY IT MATTERS:** If your code uses strict enum matching (switch without default), it will break silently when Amazon adds new values. Always have a default/unknown handler.

### Rule: These changes ARE breaking and will require version increment
- Remove/rename/change an existing enum value
- Make an optional field required
- Change default behavior of a field
- Remove or rename a field

**WHY IT MATTERS:** Plan for major version migration — Amazon guarantees these won't happen without a version bump.

### Rule: "OTHER" enum values will be removed in next version updates
Some enums currently accept "OTHER" — these will be removed in future version updates.

**WHY IT MATTERS:** Don't depend on "OTHER" values in your logic — they are temporary.

---

## 8. Deprecation Policies
**Classification:** UNIVERSAL

### Rule: Minimum 6 months notice before any version shutoff
Clients get at least 6 months from shutoff announcement. During deprecation: no new features, limited support.

**WHY IT MATTERS:** Plan migration timeline immediately when deprecation is announced. Don't wait until the last month.

### Rule: Monitor release notes for deprecation announcements
Shutoffs are announced via release notes and the Deprecations reference page.

**WHY IT MATTERS:** Missing a deprecation notice = your integration breaks on shutoff day with zero warning.

---

## 9. Entity Management Rules
**Classification:** UNIVERSAL

### Rule: Batch update/creation operations are non-atomic
A batch can partially succeed — some items succeed while others fail. Always check individual results.

**WHY IT MATTERS:** Assuming batch atomicity = thinking everything succeeded when some items failed, or vice versa. [ADD TO OUR RULES]

### Rule: All operations are idempotent (but duplicate creation returns error)
Re-running the same operation produces the same final server state. However, duplicate creation attempts return an error.

**WHY IT MATTERS:** Safe to retry on network failures, but handle "already exists" errors gracefully on creation.

### Rule: Uniqueness constraints for entity creation
- **Campaigns:** Campaign name
- **Ad groups:** Campaign name + ad group name
- **Keywords:** Campaign name + ad group name + keyword + match type
- **Product ads:** Campaign name + ad group name + SKU + ASIN

**WHY IT MATTERS:** Violating uniqueness = error saying resource already exists. Plan naming carefully for programmatic creation.

### Rule: Partial updates require only the entity ID
Only the ID is required to update an entity. All other attributes not provided remain unchanged.

**WHY IT MATTERS:** You can change just the bid without re-sending the entire keyword object. Reduces payload size and risk of accidental overwrites.

### Rule: Implicit creation/archiving via batch updates
- Missing ID + all required creation attributes = implicit creation
- Present ID + state "archived" = implicit archiving

**WHY IT MATTERS:** Accidentally omitting an ID in an update payload creates a new entity instead of updating.

### Rule: Archived entities cannot be modified
Once archived, entities cannot be changed. They remain viewable and their performance data is accessible. Archived entities don't count toward entity limits.

**WHY IT MATTERS:** Attempting to modify archived entities = errors. Archiving is effectively permanent (no unarchive).

### Rule: Sponsored Brands campaigns go through moderation (72-hour review)
New SB campaigns or changes to existing ones are reviewed via moderation. Campaigns enter "Pending Review" state. Moderation is NOT available on Sandbox.

**WHY IT MATTERS:** SB campaigns don't go live immediately — plan for 72-hour delay. Can't test moderation flow in sandbox. [ADD TO OUR RULES]

### Rule: Reports and snapshots are memorized (deduplicated)
Duplicate report/snapshot requests return the same report ID.

**WHY IT MATTERS:** Safe to retry report requests — won't create duplicates.

---

## 10. Reporting API Guidelines
**Classification:** PRIMARY (Reporting v3)

### Rule: Report generation can take up to 3 hours
Poll for status using GET `/reporting/reports/{reportId}`. When status is COMPLETED, download from the `url` field.

**WHY IT MATTERS:** Not implementing proper polling = broken report downloads. Polling too frequently = 429 errors.

### Rule: Use exponential backoff when polling report status
Repeated status checks trigger 429 responses. Implement delay between requests.

**WHY IT MATTERS:** Aggressive polling = rate limiting = even longer wait for your report.

### Rule: Reports require specific permissions
Required permissions include: `advertiser_campaign_edit`, `advertiser_campaign_view`, `nemo_report_edit`, `nemo_report_view`, `reports_edit`.

**WHY IT MATTERS:** Missing permissions = 401 errors that look like auth failures but are actually permission issues.

### Rule: Cancel PENDING reports with DELETE
Use DELETE `/reporting/reports/{reportId}` to cancel reports still in PENDING status.

**WHY IT MATTERS:** Orphaned pending reports consume queue capacity and may affect your rate limits.

### Rule: Report download URLs expire
The `url` field has an expiration timestamp in `urlExpiresAt`. Download before it expires.

**WHY IT MATTERS:** Expired download URL = need to re-request the entire report, wasting hours.

---

## 11. Limits, Constraints & Quotas (India Marketplace)
**Classification:** PRIMARY (India-specific values highlighted)

### Service Level Guarantees
| Operation | P99 Guarantee |
|-----------|---------------|
| Synchronous CRUD operations | 30 seconds |
| Impression/click event availability via API | 12 hours |
| Impression/click invalidation | 72 hours |
| Async report generation | 15 minutes |
| Async snapshot generation | 15 minutes |

**WHY IT MATTERS:** Don't expect real-time click data — there's a 12-hour delay. Report generation has a 15-min SLA, not instant.

### India (IN) Bid Constraints (INR)
| Ad Type | Min Bid | Max Bid |
|---------|---------|---------|
| Sponsored Products (CPC) | 1 | 5,000 |
| Sponsored Display (CPC) | 1 | 5,000 |
| Sponsored Display (vCPM) | 4 | 5,000 |
| Sponsored Brands (CPC) Image | 1 | 500 |
| Sponsored Brands (CPC) Video | 1.5 | 500 |
| SB (vCPM) Image - BIS | 84 | 80,000 |
| SB (vCPM) Video - BIS | 200 | 80,000 |

**WHY IT MATTERS:** Bids outside these ranges = 422 error. Hardcoding bid values without checking marketplace limits = failures.

### India (IN) Budget Constraints (INR)
| Ad Type | Entity | Min Daily | Max Daily | Min Lifetime | Max Lifetime |
|---------|--------|-----------|-----------|--------------|--------------|
| Sponsored Products | Seller, vendor | 50 | 21,000,000 | — | — |
| Sponsored Brands | Seller | 100 | 21,000,000 | 5,000 | 200,000,000 |
| Sponsored Brands | Vendor | 500 | 21,000,000 | 5,000 | 200,000,000 |
| Sponsored Display | Seller | 50 | 21,000,000 | — | — |
| Sponsored Display | Vendor | 50 | 5,000,000 | — | — |

**WHY IT MATTERS:** Budget below minimum = 422 error. Note: SB Seller vs Vendor have DIFFERENT minimums in India.

### India (IN) Metric Minimum Thresholds (Sponsored Display Rules)
| Metric | Minimum Threshold (INR) |
|--------|------------------------|
| Cost Per Click | 2 |
| Cost Per Thousand Viewable Impressions | 15 |
| Cost Per Order | 50 |

### India Default Budget (Sponsored Display)
Default budget when none specified: **1,000 INR**

### Keyword Constraints
- Max keyword length: 80 characters
- Max parts for positive keyword: 10
- Max parts for negative keyword: 4 (10 for negativeExact)
- No leading/trailing spaces
- Period (.) only in middle of keywords
- Hyphen (-) and plus (+) only in middle, no spaces around them
- Double-quotes must be in pairs
- Devanagari script (0900-097F) is supported

**WHY IT MATTERS:** Violating keyword constraints = silent rejection or 422 errors.

### Entity Name Constraints
- Campaign name max: 128 characters (sellers), 116 characters (vendors)
- Ad group name max: 255 characters
- No leading/trailing spaces
- Devanagari script supported

**WHY IT MATTERS:** Name exceeding limit = creation fails. Seller vs vendor have different limits!

---

## 12. Common Model & Entity Structure
**Classification:** PRIMARY (Ads API v1)

### Rule: Use common model for cross-product operations
The Ads API v1 common model provides standard field names across SP, SB, SD, and DSP. Required fields vary by ad product — check the field matrix.

**WHY IT MATTERS:** Using product-specific APIs when common model works = more code to maintain. v1 common model is the future.

### Key Entity Hierarchy
```
Campaign
  └── Ad Group
        ├── Targets (keywords, products, audiences)
        └── Ads (creatives)
              └── Ad Associations (DSP only)
```

### Required Fields Quick Reference
**Campaign (all products):** adProduct, name, state
**Campaign (SP):** + marketplaceScope, startDateTime, budgets
**Campaign (SB):** + marketplaceScope, startDateTime, budgets, costType
**Ad Group (all products):** adProduct, campaignId, name, state
**Target (all products):** adProduct, negative, state, targetType

### Campaign Status State Machine
Campaigns can be in states: ENABLED, PAUSED, ARCHIVED, PENDING_REVIEW, READY, SCHEDULED, RUNNING, REJECTED, ENDED, BILLING_ERROR, ASIN_NOT_BUYABLE, LANDING_PAGE_NOT_AVAILABLE, OUT_OF_BUDGET

**WHY IT MATTERS:** Not understanding the state machine = trying invalid transitions (e.g., can't go from REJECTED to ENABLED directly).

---

## 13. SDK Generation Guidelines
**Classification:** PRIMARY (v1 specific)

### Rule: Use OpenAPI Generator with Amazon's v1 specifications
Download OAS files from the specification page. Ad-product-specific specs filter to relevant fields only.

### Rule: Handle polymorphism in OAS files
Amazon's specs use oneOf/discriminator patterns that need preprocessing before code generation. Remove polymorphism and rename Error to ModelError to avoid conflicts.

**WHY IT MATTERS:** Raw OAS files may not generate clean SDKs — preprocessing is required.

### Rule: Runtime imports need path adjustment per product
Generated files need import path fixes for runtime.ts references based on directory depth.

**WHY IT MATTERS:** Broken imports = SDK won't compile.

---

## 14. Common Mistakes to Avoid
**Classification:** UNIVERSAL

| # | Mistake | Consequence | Prevention |
|---|---------|-------------|------------|
| 1 | Using wrong regional endpoint | 403 Forbidden | Check endpoint table — India = EU |
| 2 | Not handling 207 multi-status responses | Think batch succeeded when items failed | Check each sub-response individually |
| 3 | Using extended data operations casually | 5x rate limit weight | Only when entity status needed |
| 4 | Paginating for full account sync | Inconsistent data + rate limits | Use exports instead |
| 5 | Not implementing exponential backoff | Prolonged throttling | Start at 2s, double each retry |
| 6 | Strict enum matching without default | Breaks when Amazon adds new values | Always have default/unknown handler |
| 7 | Omitting entity ID in batch update | Creates new entity instead of updating | Always verify ID presence |
| 8 | Assuming batch operations are atomic | Miss partial failures | Check individual results |
| 9 | Retrying 4xx client errors | Wastes quota, never succeeds | Fix request first, then retry |
| 10 | Expecting real-time click/impression data | Data not available yet | 12-hour delay for availability |
| 11 | Aggressive report status polling | 429 throttling | Exponential backoff, minutes not seconds |
| 12 | Not checking bid/budget constraints per marketplace | 422 errors | Validate against marketplace-specific limits |
| 13 | Hardcoding Content-Type for reports | 400/415 errors | Use versioned content types |
| 14 | Not handling report URL expiration | Download fails | Check urlExpiresAt, download promptly |
| 15 | Trying to modify archived entities | Errors | Check state before modification |

---

## 15. Testing Guidelines
**Classification:** UNIVERSAL

### Rule: Use test accounts for campaign creation testing
Create a test account for testing. See Amazon's Test Account Overview.

**WHY IT MATTERS:** Testing on production account = real campaigns, real spend, real consequences.

### Rule: Create campaigns in PAUSED state for testing
All test campaigns should use `state: "PAUSED"`.

**WHY IT MATTERS:** Active test campaigns can spend real advertising budget.

### Rule: Moderation is NOT available in Sandbox
Sponsored Brands moderation workflow cannot be tested in sandbox.

**WHY IT MATTERS:** SB campaign flows behave differently in sandbox vs production. Plan for this gap.

### Rule: Campaign names must be unique per profile
Sponsored Products requires unique campaign names. Generate unique names for repeated test runs.

**WHY IT MATTERS:** Reusing test campaign names = "already exists" errors on every test run after the first.

---

## 16. Security Requirements
**Classification:** UNIVERSAL

### Rule: Store credentials in config files, never hardcode
Client ID, client secret, refresh tokens, profile IDs — all must be in secure config files.

**WHY IT MATTERS:** Hardcoded credentials in code = security breach risk + difficult rotation.

### Rule: Handle token refresh properly
OAuth tokens expire. Implement automatic refresh before expiry, not after failure.

**WHY IT MATTERS:** Post-failure refresh = user-visible errors. Pre-emptive refresh = seamless operation.

---

## 17. ADD TO OUR RULES — Gaps Found
**Classification:** Action items for updating `Learning And Rule/04_API_INTEGRATION.md`

Comparing Amazon's official guidelines with our existing `04_API_INTEGRATION.md`, these important guidelines are NOT currently covered in our rules:

| # | Gap | Amazon Guideline | Priority |
|---|-----|-----------------|----------|
| 1 | **Extended data 5x weight** | Extended data calls cost 5x towards throttling. Only use when entity status specifically needed. | HIGH |
| 2 | **Exports > Pagination for bulk sync** | Use async exports instead of paginated batch GETs for full account data sync. | HIGH |
| 3 | **207 Multi-Status handling** | Batch responses can contain mix of successes and errors. Must check each sub-response. | HIGH |
| 4 | **Non-atomic batch operations** | Batch create/update is NOT atomic — partial success possible. Always check individual results. | HIGH |
| 5 | **Error classification for retry** | 5xx = retry, 429 = retry with Retry-After, 4xx = DO NOT retry (fix request first). | MEDIUM |
| 6 | **Enum flexibility** | New enum values can appear without version bump. Always have default handler. Never use strict matching. | MEDIUM |
| 7 | **Versioned Content-Type headers** | Some APIs (reporting) require specific versioned Content-Types, not generic application/json. | MEDIUM |
| 8 | **Pagination inconsistency** | Paginated results may have duplicates/missing records. Use exports for consistency. | MEDIUM |
| 9 | **SB Moderation 72-hour delay** | SB campaigns go through moderation (up to 72h). Not testable in sandbox. | MEDIUM |
| 10 | **Report polling backoff** | Report generation rate limits need minutes of backoff, not seconds. | MEDIUM |
| 11 | **Calculate inherited status locally** | Compute entity status from parent/grandparent locally instead of requesting extended attributes. | LOW |
| 12 | **India-specific bid/budget limits** | IN marketplace has specific bid/budget constraints different from other EU markets. | HIGH |
| 13 | **Implicit creation on missing ID** | Omitting ID in batch update with full creation attributes = creates new entity. | MEDIUM |
| 14 | **Report URL expiration** | Download URLs expire (check urlExpiresAt). Must download promptly after COMPLETED status. | LOW |
| 15 | **12-hour click/impression delay** | Click/impression data has 12-hour availability delay. 72-hour invalidation window. | LOW |

---

*Document version: 1.0 | Created: 13 April 2026*
*Source file: `imporant guideline by amazon about api.txt` (4,571 lines)*
*Organized from official Amazon Advertising API documentation pages: Overview, Concepts, Errors, Limits/Constraints/Quotas, Rate Limiting, Compatibility/Versioning, Computed Status, Developer Notes, Common Models (Campaigns, Ad Groups, Targets, Ads, Ad Associations, Enums), API v1 Overview, Getting Started, SDK Generation Guide, Reporting v3 Reference*
