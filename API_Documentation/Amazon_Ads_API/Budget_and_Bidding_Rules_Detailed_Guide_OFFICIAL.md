# Sponsored Ads Budget Rules & Bidding Rules — Detailed Guide
**Source:** Amazon Ads Developer Documentation (Part 4)
**Saved:** 13 April 2026
**Category:** Amazon Ads API (advertising-api-eu.amazon.com)
**Applies to:** SP, SB, SD budget rules; SP bidding rules

---

## Part 1: Budget Rules

### Overview
Budget rules automatically increase campaign daily budgets based on schedule or performance conditions, reducing manual effort and preventing out-of-budget situations.

### Rule Types
1. **Schedule-based:** Increase budget by % during date ranges or events
2. **Performance-based:** Increase budget when campaign metrics meet thresholds

### Endpoints by Ad Type

| Ad Type | Create Rule | Associate to Campaign | Get Rules |
|---------|-------------|----------------------|-----------|
| SP | `POST /sp/budgetRules` | `POST /sp/campaigns/{id}/budgetRules` | `GET /sp/campaigns/{id}/budgetRules` |
| SB | `POST /sb/budgetRules` | `POST /sb/campaigns/{id}/budgetRules` | `GET /sb/campaigns/{id}/budgetRules` |
| SD | `POST /sd/budgetRules` | `POST /sd/campaigns/{id}/budgetRules` | `GET /sd/campaigns/{id}/budgetRules` |

### Event Recommendations (SP & SB only)
| Ad Type | Endpoint |
|---------|----------|
| SP | `POST /sp/campaigns/budgetRules/recommendations` |
| SB | `POST /sb/campaigns/budgetRules/recommendations` |

---

### Schedule-Based Rules

#### Parameters
- **ruleType:** "SCHEDULE"
- **Date range:** Custom dates or event ID (e.g., Black Friday)
- **Recurrence:** DAILY, WEEKLY (with daysOfWeek), or with intraDaySchedule
- **budgetIncreaseBy:** Percentage amount

**intraDaySchedule:** Available in US, CA, UK, IN, JP only. Requires minimum budget.

#### Example: Daily Rule for Custom Date Range
```json
{
  "budgetRulesDetails": [{
    "name": "SAMPLE_BUDGET_RULE_DAILY",
    "ruleType": "SCHEDULE",
    "duration": {
      "dateRangeTypeRuleDuration": {
        "startDate": "20201121",
        "endDate": "20201130"
      }
    },
    "recurrence": {"type": "DAILY"},
    "budgetIncreaseBy": {"type": "PERCENT", "value": 20}
  }]
}
```

#### Example: Weekly Rule (Weekends)
```json
{
  "budgetRulesDetails": [{
    "name": "SAMPLE_BUDGET_RULE_WEEKLY",
    "ruleType": "SCHEDULE",
    "duration": {"dateRangeTypeRuleDuration": {"startDate": "20200901"}},
    "recurrence": {
      "type": "weekly",
      "daysOfWeek": ["FRIDAY", "SATURDAY", "SUNDAY"]
    },
    "budgetIncreaseBy": {"type": "PERCENT", "value": 20}
  }]
}
```

#### Example: Recommended Event
```json
{
  "budgetRulesDetails": [{
    "name": "SAMPLE_BUDGET_RULE_RECOMMENDED_EVENT",
    "ruleType": "SCHEDULE",
    "duration": {
      "eventTypeRuleDuration": {"eventId": "69ce6478-5215-4bd3-8de0-a8eb28ae69a7"}
    },
    "recurrence": {"type": "DAILY"},
    "budgetIncreaseBy": {"type": "PERCENT", "value": 20}
  }]
}
```

---

### Performance-Based Rules

#### Available Metrics by Ad Type

| Metric | SP | SB | SD | Description |
|--------|----|----|----|----|
| ACOS | Yes | No | Yes | Spend / attributed sales |
| CTR | Yes | No | Yes | Clicks / impressions |
| CVR | Yes | No | Yes | Conversions / clicks |
| ROAS | Yes | Yes | Yes | Revenue / spend |
| IS | No | Yes | No | Top-of-search impression share |
| NTB | No | Yes | No | % sales from new-to-brand |

**Metric period:** 7 days for sellers, 14 days for vendors.

#### Parameters
- **ruleType:** "PERFORMANCE"
- **performanceMeasureCondition:** metricName + threshold + comparisonOperator
- **comparisonOperator:** LESS_THAN, GREATER_THAN, EQUAL_TO, LESS_THAN_OR_EQUAL_TO, GREATER_THAN_OR_EQUAL_TO

#### Example: Increase Budget if ACOS < 20%
```json
{
  "budgetRulesDetails": [{
    "name": "SAMPLE_BUDGET_RULE_ACOS",
    "ruleType": "PERFORMANCE",
    "duration": {"dateRangeTypeRuleDuration": {"startDate": "20201121"}},
    "recurrence": {"type": "DAILY"},
    "budgetIncreaseBy": {"type": "PERCENT", "value": 10},
    "performanceMeasureCondition": {
      "metricName": "ACOS",
      "threshold": 20,
      "comparisonOperator": "LESS_THAN_OR_EQUAL_TO"
    }
  }]
}
```

---

### Rule Evaluation Logic

- Rules evaluated at start of each day
- Multiple rules (max 250): ALL matching rules applied, increases **added independently**
- New/updated rules evaluated immediately
- IntraDay rules: Additional increase during specified hours, revert after

#### Rule Statuses
| Status | Meaning |
|--------|---------|
| Active | Budget increased per rule config |
| On Hold | Conditions not met / superseded / recurrence not met |
| Paused | Manually paused |
| Budget threshold not met | Minimum budget not reached (performance rules only) |
| Pending Start | Start date in future |
| Expired | Past end date |

### Viewing Rule Effects

**SP v3:** Check `effectiveBudget` in `POST /sp/campaigns/list` response.
**SB/SD/SP v2:** Check `ruleBasedBudget` object in campaign list response.

### Budget Rule Reporting Metrics
| Metric | Description |
|--------|-------------|
| campaignRuleBasedBudget | Value of rule-based budget |
| applicableBudgetRuleId | Active rule identifier |
| applicableBudgetRuleName | Active rule name |

---

## Part 2: Bidding Rules (SP Only)

### Rule-Based Bidding (Campaign Optimization)

Automatically adjusts base bids to increase conversions while maintaining ROAS guardrail.

#### Requirements
- Campaign running 10+ days
- Minimum 10 conversions in last 30 days
- Minimum daily budget per marketplace (IN = 300 INR)

#### Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sp/rules/campaignOptimization` | POST | Create rule |
| `/sp/rules/campaignOptimization` | PUT | Update rule |
| `/sp/rules/campaignOptimization/{id}` | GET | Retrieve rule |
| `/sp/rules/campaignOptimization/{id}` | DELETE | Delete rule |
| `/sp/rules/campaignOptimization/state` | POST | Query state |
| `/sp/rules/campaignOptimization/eligibility` | POST | Check eligibility + get ROAS recommendation |

#### Create Rule Example
```json
{
  "recurrence": "DAILY",
  "ruleAction": "ADOPT",
  "ruleCondition": [{
    "metricName": "ROAS",
    "comparisonOperator": "GREATER_THAN",
    "threshold": "4"
  }],
  "ruleType": "BID",
  "ruleName": "RuleROAS4",
  "campaignIds": ["123784", "1223785"]
}
```

#### Safety: If ROAS drops to <30% of 20-40 day average, Amazon disables the rule automatically.

---

### Schedule Bid Rules (SP Only)

Automatically increase bids at specific times/days/events.

#### Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sp/rules/optimization` | POST | Create rule |
| `/sp/rules/optimization` | PUT | Update rule |
| `/sp/rules/optimization/search` | POST | Search rules |
| `/sp/campaigns/{id}/optimizationRules` | POST | Associate rule to campaign |

#### Limits
- Max 20 schedule bid rules per campaign
- Changes take effect within 24 hours
- Applied on top of Placement adjustment and Bidding strategies

#### Example: Increase Bids 15% on Mornings
```json
{
  "optimizationRules": [{
    "ruleName": "increase_bids_by_15%_on_mornings",
    "ruleCategory": "BID",
    "ruleSubCategory": "SCHEDULE",
    "recurrence": {
      "type": "DAILY",
      "timesOfDay": [{"startTime": "05:00", "endTime": "13:00"}],
      "duration": {"startTime": "2023-08-01T00:00:00Z"}
    },
    "action": {
      "actionType": "ADOPT",
      "actionDetails": {
        "actionOperator": "INCREMENT",
        "value": 15,
        "actionUnit": "PERCENT"
      }
    },
    "status": "ENABLED"
  }]
}
```

#### Example: Black Friday Event Rule
Use `POST /sp/v1/events` to get event details, then create rule with event in duration.

---

## Minimum Daily Budget for Rule-Based Bidding (India)

| Marketplace | Min Budget |
|-------------|-----------|
| IN | 300 INR |

---
*File version: 1.0 | Extracted from Part 4 documentation*
