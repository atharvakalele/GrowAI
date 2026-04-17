# Grow24 AI / GoAmrita - Future Data Collection Standard v1.0
**Project Name:** Grow24 AI (formerly GoAmrita)  
**Date:** 15 April 2026  
**Purpose:** Standard for the first half of every future feature/module: get data, detect issues, and publish findings

---

# 1. CORE IDEA

Every future goal should be divided into 2 parts:

1. Get Data
2. Take Action

This document defines **Part 1 = Get Data**.

The data layer is responsible for:
- collecting required inputs
- analyzing the situation
- detecting opportunities/issues
- publishing structured findings

The data layer does **not** directly own final business action execution.

---

# 2. WHAT "GET DATA" MEANS

For any future feature, the first question is:

```text
What is happening right now?
```

So the data layer should:
- call APIs or read files
- normalize enough information for internal use
- identify problems/opportunities
- score priority
- recommend what should happen next

Examples:
- competitor analysis finds 1 ASIN with Buy Box risk
- listing health scan finds suppressed ASINs
- stock scan finds low-stock SKUs
- pricing scan finds price-gap opportunities

---

# 3. REQUIRED OUTPUT OF DATA LAYER

The data layer should publish:

1. Raw output
2. Impact summary
3. Activity summary
4. Registry entry
5. Action candidate list

The action candidate list is the handoff from **Get Data** to **Take Action**.

---

# 4. ACTION CANDIDATE RULE

If the data layer finds an issue or opportunity, it must describe:
- what item is affected
- what problem/opportunity was detected
- how serious it is
- what action is recommended
- whether auto-action is allowed

Example:

```text
Competitor Tracker
- found 1 ASIN with no Buy Box
- recommendation: check listing suppression, price, and availability
- auto-action eligibility: yes/no depends on action settings and module rules
```

---

# 5. DATA LAYER QUESTIONS

Every future data module should answer:
- what did I inspect?
- what did I find?
- what is at risk?
- what is the likely impact?
- what should be done next?

If it cannot answer "what should be done next," the module is incomplete.

---

# 6. WHAT DATA LAYER MUST NOT DO

The data layer must not:
- hide detected issues without publishing them
- execute business action silently with no action record
- skip action recommendation text
- directly mix dashboard rendering logic into detection logic

---

# 7. EXAMPLE FLOW

```text
Competitor module runs
-> reads competitor and Buy Box data
-> finds 1 risky ASIN
-> creates action candidate:
   "Review listing suppression, pricing, and availability"
-> publishes dashboard/report outputs
-> passes candidate to action layer
```

---

# 8. FINAL RULE

For all new future modules/features:

**Part 1 must always be "Get Data and Publish Findings."**

No feature should jump directly to action without first producing a visible, structured finding.
