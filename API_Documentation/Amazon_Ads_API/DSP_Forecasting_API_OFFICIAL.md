# Amazon DSP Forecasting API — Official Documentation
**Source:** Amazon Ads Developer Documentation (Part 4)
**API Version:** v1
**Endpoint:** `POST /adsApi/v1/retrieve/campaignForecasts/dsp`
**Saved:** 13 April 2026
**Category:** Amazon DSP (advertising-api-eu.amazon.com)

---

## Overview

The Amazon DSP Forecasting API provides campaign-level performance, delivery, and spend forecasts. It offers the same forecasting capabilities available through Amazon's DSP forecasting widgets, but accessible programmatically.

### Key Strategic Benefits
- Predictive Campaign Planning: Forecast key metrics before budget allocation
- Risk Mitigation: Delivery confidence indicators identify potential underperformance before launch
- Budget Optimization: Spend forecasting enables more accurate budget allocation
- Data-Driven Decisions: Replace guesswork with statistical forecasts

---

## Core Capabilities

### Campaign-Level Forecasting
- Performance Predictions: Forecast CPC, CPA, ROAS before campaign launch
- Delivery Forecasting: Predict campaign delivery confidence and potential issues
- Spend Forecasting: Estimate budget utilization and pacing

### Flight-Level Granularity
- Support for up to 5 flights per campaign forecast
- Individual flight performance predictions
- Cross-flight optimization recommendations

### Multiple Forecast Periodicities
- **Daily:** Day-by-day performance predictions
- **Weekly:** Week-over-week aggregated forecasts
- **Monthly:** Monthly performance summaries
- **Lifetime:** Total campaign performance predictions

---

## Available Endpoint

```
POST /adsApi/v1/retrieve/campaignForecasts/dsp
```

**Rate Limits:** Subject to standard Amazon Ads API rate limiting
**Batch:** Up to 1 campaign per request in current version

### Required Headers
| Header | Value |
|--------|-------|
| Content-Type | application/json |
| Amazon-Ads-ClientId | Your client ID |
| Amazon-Ads-AccountId | DSP account ID |
| Authorization | Bearer {access-token} |

---

## Supported Forecast Metrics

### Performance Metrics
| Code | Name | Description | Business Value |
|------|------|-------------|----------------|
| CPC | Cost Per Click | Predicted cost per click | Efficiency planning |
| CPA | Cost Per Action | Predicted cost per conversion | ROI planning |
| CPM | Cost Per Mille | Predicted cost per thousand impressions | Media planning |
| ROAS | Return on Ad Spend | Predicted return on investment | Profitability forecasting |

### Delivery & Reach Metrics
| Code | Name | Description |
|------|------|-------------|
| DC | Delivery Confidence | Probability of full campaign delivery (0.0-1.0) |
| AIMP | Available Impressions | Total impressions available for targeting |
| EIMP | Expected Impressions | Predicted impression delivery |
| AREA | Available Reach | Total unique users reachable |
| EREA | Expected Reach | Predicted unique reach |
| IREA | Incremental Reach | Additional unique users beyond existing campaigns |

### Budget & Spend Metrics
| Code | Name | Description |
|------|------|-------------|
| TAS | Total Available Spend | Maximum spendable budget given market conditions |
| CAS | Capped Available Spend | Available spend limited by budget constraints |

---

## Request Examples

### Simple Request
```json
{
  "campaignForecastDescriptions": [
    {
      "campaignId": "campaign-123456",
      "enabledFeatures": {
        "curve": false,
        "replanning": false,
        "campaignSettingsCache": true,
        "metrics": {
          "allMetrics": true,
          "selectedMetrics": []
        }
      }
    }
  ]
}
```

### Advanced Request with Specific Metrics
```json
{
  "campaignForecastDescriptions": [
    {
      "campaignId": "campaign-123456",
      "flightIds": ["flight-001", "flight-002"],
      "enabledFeatures": {
        "curve": true,
        "replanning": true,
        "campaignSettingsCache": true,
        "metrics": {
          "allMetrics": false,
          "selectedMetrics": ["CPC", "CPA", "ROAS", "DC", "EIMP"]
        }
      },
      "replanningSettings": {
        "flights": [
          {
            "flightId": "flight-001",
            "budget": {
              "budgetValue": {
                "monetaryBudgetValue": {
                  "monetaryBudget": {
                    "currencyCode": "USD",
                    "value": 10000.00
                  }
                }
              }
            },
            "startDateTime": "2024-01-15T00:00:00Z",
            "endDateTime": "2024-01-31T23:59:59Z"
          }
        ]
      }
    }
  ]
}
```

---

## Response Structure

### HTTP 207 Multi-Status Response
- `success[]` — Array of successful forecasts
- `error[]` — Array of failed forecasts

### Forecast Values
```json
{
  "low": 1.25,    // Conservative estimate (10th percentile)
  "high": 2.75,   // Optimistic estimate (90th percentile)
  "mean": 2.00    // Expected value (50th percentile)
}
```

### Confidence Levels
| Value | Meaning | Probability |
|-------|---------|-------------|
| HIGH | Strong confidence | 80-95% |
| MEDIUM | Moderate confidence | 60-79% |
| LOW | Limited confidence | 40-59% |
| UNAVAILABLE | Insufficient data | N/A |

---

## Advanced Features

### Forecast Curves
- Bid/Spend vs. Performance curves for optimization
- X-Axis labels: SPEND, BID, TAS, CAS
- Y-Axis labels: DC, AIMP/EIMP, AREA/EREA, CPC/CPA/CPM, ROAS
- Focus Points identify optimal performance ranges

### Replanning Recommendations
- Automated suggestions for campaign optimization
- Scenario-based recommendations with performance predictions
- Alternative flight configurations

---

## FAQ

**Q: Can I forecast for campaigns that haven't been created yet?**
A: No, the API requires existing campaign and flight IDs. Use a "template campaign" approach — create template campaigns for different types and update settings for forecasting.

**Q: How accurate are the forecasts?**
A: Accuracy depends on historical data, market stability, targeting specificity, seasonality, and campaign complexity. HIGH confidence typically means 85-95% accuracy.

**Q: allMetrics vs selectedMetrics?**
A: allMetrics=true returns everything (larger payload, best for exploration). selectedMetrics returns only specified metrics (faster, best for production).

---

## Python Reference Implementation

A full Python client class `ADSPForecastingClient` is available in the source documentation with:
- `get_campaign_forecast()` method with flexible options
- `visualize_curves()` method for matplotlib visualization
- Response parsing and metric extraction utilities

---
*File version: 1.0 | Extracted from Part 4 documentation*
