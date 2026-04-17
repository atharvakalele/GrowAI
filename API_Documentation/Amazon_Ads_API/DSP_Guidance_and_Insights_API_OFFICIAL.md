# Amazon DSP Guidance, Quick Actions & Insights API — Official Documentation
**Source:** Amazon Ads Developer Documentation (Part 4)
**Saved:** 13 April 2026
**Category:** Amazon DSP (advertising-api-eu.amazon.com)

---

## 1. Guidance & Quick Actions API

### Overview
The Guidance API enables programmatic access to Amazon DSP's ML-powered recommendations for campaign optimization.

### Guidance API Endpoints
| Endpoint | Description |
|----------|-------------|
| `POST /dsp/v1/guidance/adGroups/list` | List Ad Group Guidance |
| `POST /dsp/v1/guidance/campaigns/list` | List Campaign Guidance |
| `POST /dsp/v1/guidance/advertisers/list` | List Advertiser Guidance |

### Quick Actions API Endpoints
| Endpoint | Description |
|----------|-------------|
| `POST /dsp/v1/quickactions/{actionId}/executions` | Create execution for Quick Action |
| `PUT /dsp/v1/quickactions/{actionId}/executions/{executionId}/start` | Start execution |
| `GET /dsp/v1/quickactions/{actionId}/executions/{executionId}` | Get execution status |
| `POST /dsp/v1/quickactions/batchGetExecutions` | Batch get executions |
| `POST /dsp/v1/quickactions/batchCreateExecutions` | Batch create executions |

### Recommendation Types

#### Pre-flight (before campaign launch)
- **Tactics:** Pre-configured ad groups for targeting strategies
- **Maximum Average CPM** optimization
- **Frequency Cap** optimization

#### In-flight (active campaigns)
- **Under Delivery Guidance** — Campaign predicted to under-deliver
- **Increase Maximum Average CPM** — CPM too restrictive
- **Increase Frequency Cap** — Frequency cap constraining reach
- **Reduce Viewability Target** — Viewability too restrictive
- **Add Missing Creative Sizes** — Limited creative sizes

### Polling Recommendations
- Guidance: Poll **daily**
- Quick Actions: Poll every **30 seconds** for execution status

---

## 2. Overlapping Audiences API

### Endpoint
```
GET /insights/audiences/{audienceId}/overlappingAudiences?adType=DSP&advertiserId={id}
```

Returns top 30 overlapping audiences with affinity scores.

### Filters
- `audienceCategory` — Filter by audience type (e.g., "In-market")
- `minimumOverlapAffinity` — Minimum affinity threshold
- `maximumOverlapAffinity` — Maximum affinity threshold

---

## 3. Persona Builder API

Build insights on custom composite audience expressions.

### Endpoints
| Endpoint | Description |
|----------|-------------|
| `POST /insights/bandedSize` | Get banded size estimate (upper/lower bound) |
| `POST /insights/demographics` | Age, gender insights with affinity |
| `POST /insights/topCategoriesPurchased` | Top retail categories purchased |
| `POST /insights/topOverlappingAudiences` | Top overlapping audiences (paginated) |
| `POST /insights/primeVideo` | Top genres, actors, directors, series, movies |

### Combined Audience API
| Endpoint | Description |
|----------|-------------|
| `POST /dsp/audiences/combinedAudiences` | Save audience expression to DSP |
| `GET /dsp/audiences/combinedAudiences/{audienceID}` | View existing combined audience |

### Audience Expression Format
```json
{
  "audienceTargetingExpression": {
    "audiences": [
      {"negative": "false", "groupId": "group_name", "audienceId": "1234567890"},
      {"negative": "false", "groupId": "group_name_2", "audienceId": "0987654321"}
    ]
  }
}
```

---

## 4. DSP Campaign Insights API (Brand+ / Performance+)

### Overview
Performance insights for Brand+ and Performance+ campaigns.

- **Version:** v1
- **Base URL:** `/dsp/v1/campaign/insights`
- **Rate Limit:** Max 25 requests per API call
- **Latency SLA:** <1 second (P99)
- **Minimum:** Campaign active ~8 days with Brand+ or Performance+ tactics

### Supported Tactics
| Goal | Tactic |
|------|--------|
| Awareness | Prospecting |
| Consideration | Unified Consideration |
| Conversion | Customer Acquisition, Remarketing, Retention |

### Request Example
```json
{
  "requests": [
    {
      "campaignId": "camp_12345",
      "insightType": "PERFORMANCE_PLUS_SHOPPER_TRAIT"
    }
  ]
}
```

---
*File version: 1.0 | Extracted from Part 4 documentation*
