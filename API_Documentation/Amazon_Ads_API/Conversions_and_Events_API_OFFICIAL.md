# Amazon Ads Conversions & Events API - OFFICIAL Documentation
**Source:** Official Amazon Advertising documentation (manually copied by Msir)
**Date Captured:** 13 April 2026
**API Version:** CAPI v1, Events API (CAPI v2), AAT, Attribution Tags
**Our Endpoint:** advertising-api-eu.amazon.com
**Our Profile ID:** 42634532240933
**Part of:** Part 3 API documentation batch

---

## Table of Contents
1. [Conversion Tracking Overview](#1-conversion-tracking-overview)
2. [On-Amazon vs Off-Amazon Conversions](#2-on-amazon-vs-off-amazon-conversions)
3. [Conversions API (CAPI v1)](#3-conversions-api-capi-v1)
4. [Events API (CAPI v2)](#4-events-api-capi-v2)
5. [Amazon Ad Tag (AAT)](#5-amazon-ad-tag-aat)
6. [Amazon Attribution Tags](#6-amazon-attribution-tags)
7. [Ads Data Manager (ADM)](#7-ads-data-manager-adm)
8. [Amazon Marketing Cloud (AMC)](#8-amazon-marketing-cloud-amc)
9. [AMC on AWS Clean Rooms](#9-amc-on-aws-clean-rooms)
10. [FAQ](#10-faq)

---

## 1. Conversion Tracking Overview

Amazon Ads provides comprehensive conversion tracking solutions for both on-Amazon and off-Amazon conversions.

### Key Definitions:
- **Conversion:** A specific, measurable action taken by a user after interacting with an ad
- **On-Amazon conversions:** Actions occurring directly on Amazon's platform (purchases, add-to-cart)
- **Off-Amazon conversions:** Actions occurring outside Amazon (advertiser's website, app, offline)
- **Ad-attributed conversions:** Conversions where user was served a traffic event within 28-day period prior
- **Match Keys:** Customer/device identifiers used for attribution (email, phone, mobile ID)
- **ID Resolution:** Process of matching uploaded identifiers to Amazon user records

### Conversion Attribution:
Attribution measures conversion events/shopping behaviors that occur following an ad interaction. Conversions are attributed to the most relevant ad campaign traffic using multi-touch attribution.

---

## 2. On-Amazon vs Off-Amazon Conversions

### On-Amazon Conversions
- **Tracking:** Automatic, no setup needed
- **Data Availability:** Reporting API and AMC
- **Use Case:** Track conversions on Amazon.com (purchases, add-to-cart)

### Off-Amazon Conversion Methods

| Method | Type | Data Available In | Best For |
|--------|------|-------------------|----------|
| Amazon Ad Tag (AAT) | Client-side (JavaScript) | Reporting API, AMC | Website events |
| Attribution Tags | URL tracking | Attribution Tag Reports | External marketing (social, email) |
| Conversions API (CAPI v1) | Server-side | Reporting API, AMC | Server-to-server (DEPRECATED) |
| Events API (CAPI v2) | Server-side | ADSP Reporting, AMC, ADM | Server-to-server (RECOMMENDED) |
| ADM | Data upload | AMC | Bulk data management |
| AMC ADU | Dataset upload | AMC only | Advanced analysis |
| AMC on ACR | AWS Clean Rooms | AMC only | Privacy-preserving collaboration |

**IMPORTANT:** For off-Amazon conversion data to appear in AMC tables using CAPI v1:
1. Create a Conversion Definition
2. Associate that definition with a campaign

---

## 3. Conversions API (CAPI v1)

> **NOTE:** CAPI v1 is being replaced by the Events API. Use Events API going forward.

### Prerequisites:
- Amazon DSP advertiser account required
- **Self-Service (SS) accounts:** Supported
- **Manager Accounts (MA):** NOT Supported
- **Managed Service (MS):** NOT Supported

### Implementation Steps:

#### Step 1: Enable Conversions API in Amazon DSP
1. Open DSP advertiser, select entity
2. Navigate to "Events Manager" tab
3. Accept terms and conditions
4. Note the advertiser ID

#### Step 2: Create a Conversion Definition
```
POST /accounts/{accountId}/dsp/conversionDefinitions
```
- Create for each event type (Purchase, Add to Cart, Subscription, etc.)
- Save the returned conversion definition ID

#### Step 3: Get List of Conversion Definitions
```
POST /accounts/{accountId}/dsp/conversionDefinitions/list
```

#### Step 4: Associate Conversion Definition to an Order
```
POST /accounts/{accountId}/dsp/orders/{orderId}/conversionDefinitionAssociations
```

#### Step 5: Import Conversion Events
```
POST /accounts/{accountId}/dsp/conversionDefinitions/eventData
```
- Batch or streaming delivery
- **Rate limit:** 5 TPS per advertiser
- Invalid events in batch are rejected; valid events accepted

### Error Codes:

| Code | Description | Solution |
|------|-------------|----------|
| 400 | Bad Request - Invalid payload | Check JSON formatting and required fields |
| 401 | Unauthorized | Re-authenticate |
| 403 | Forbidden - Insufficient permissions | Verify account permissions |
| 429 | Rate Limited | Implement throttling |
| 500 | Server Error | Retry, contact support |

### Important Notes:
- Events appear in Events Manager within ~30 minutes
- Attribution in campaign reports: allow up to 24 hours
- Events older than 7 days are rejected
- Max 500 events per API request
- clientDedupeId used for deduplication across all ingestion mechanisms

### Required Match Keys (at least one):
- Email (hashed)
- Phone (hashed)
- Mobile ID
- Other identifiers

### Conversion Definition Fields in Events Manager:
- **Conversion Source:** Where ADSP received from (AAT, CAPI)
- **Conversion Name:** User-defined event name
- **Conversion Type:** Category (one of 10 defaults or Other)
- **Conversion Method:** "Every" (count all) or "Only the First" (unique per 24hr)
- **Default conversion value:** Static or dynamic
- **Last Activity:** Last event sent
- **Last Update:** Last settings change

---

## 4. Events API (CAPI v2)

The newer, recommended server-to-server solution replacing CAPI v1.

### Key Features:
- Server-to-server (S2S) integration
- No browser-based dependencies
- Real-time conversion streaming
- Cross-channel performance measurement

### Endpoint:
```
POST /adsApi/v1/create/events
```

### Authentication:
- Login with Amazon (LWA) with appropriate scope for DSP entity

### Event Payload Includes:
- Hashed identifiers (email, phone, mobile IDs)
- Event details (type, timestamp, value)
- Consent signals (TCF or Amazon Consent Signal)

### Account Requirements:
- Advertiser-owned (self-service)
- Admin access to seat/entity OR Events Manager API permission at ADSP account level
- Supports agency-driven or multi-brand advertisers

### Data Availability:
- ADSP Reporting
- Amazon Marketing Cloud (AMC)
- Ads Data Manager (ADM)

---

## 5. Amazon Ad Tag (AAT)

Client-side JavaScript solution for tracking website events.

### Key Points:
- Only 1 tag per advertiser
- Different events by changing trackEvent parameter value
- Data available in Reporting API and AMC

### Implementation Steps:
1. Get an AdTag for the advertiser (API or Console)
2. Create an Amazon Ads conversion definition
3. Associate AAT event to a conversion definition
4. Associate order to conversion definition

---

## 6. Amazon Attribution Tags

URL-based tracking for external marketing channels.

### Use Case:
Track conversions from external advertising (social media, email, etc.)

### Data Availability:
Attribution Tag Reports

### Implementation Steps:
1. Get publishers (Google Ads, Facebook Ads, etc.)
2. Create an Amazon Attribution Tag
3. Insert into the ad as landing page (publisher dependent)
4. Report

---

## 7. Ads Data Manager (ADM)

Secure first-party data upload to Amazon Ads.

- Uses UI (Ads data manager console) or APIs
- Broader scope than Events API (audience creation + event data)
- While Events API focuses on real-time tracking, ADM handles bulk data management

---

## 8. Amazon Marketing Cloud (AMC)

### Advertiser Data Upload (ADU) API (ADU 2.0):
- Upload customizable datasets including conversions to AMC instance
- Any combination of columns defined by advertiser
- Uploaded data can be joined with existing AMC data for analysis
- **Conversion data uploaded via ADU is ONLY available in AMC**
- Can be used to create audiences and send to ADSP

---

## 9. AMC on AWS Clean Rooms

- Collaborate with Amazon Ads signals without moving data outside AWS
- Share conversions data with AMC on ACR
- Join with existing AMC data for analysis
- **Only available in AMC** but can create audiences for DSP and Sponsored Ads

---

## 10. FAQ

### How to improve match rates?
- Include more user identifiers (email, phone, mobile ID)
- Verify PII data formatting before sending
- Add geographic information (city, state, postal code)
- Include user agent for web events
- Use consistent external IDs across touchpoints

### AAT vs CAPI difference?
AAT tracks from browser (client-side), affected by ad blockers/privacy settings. CAPI sends from server directly, more reliable. Using both with deduplication gives most comprehensive tracking.

### Deduplication across AAT/CAPI?
clientDedupeId is set on event payload; ADSP deduplicates across all ingestion mechanisms with same clientDedupeId.

### Consent handling?
Send TCF OR Amazon Consent Signal (AdStorage and UserData). Only 1 consent signal should be sent. If both are sent, TCF is used as primary signal.

### Can I send custom events?
Yes, use "OTHER" event type for events that don't fit standard categories.

### Historical data?
Events must be sent within 7 days of occurrence.

### Reporting for conversions:
1. **Campaign Manager tables:** Supports pre-defined event types (SignUp, Subscribe). Customize columns > Off-Amazon conversions
2. **Custom reporting (Report Center):** Supports custom conversion names. Amazon DSP reports > New custom report > Off-Amazon dropdown

---
*Document version: 1.0 | Created: 13 April 2026*
