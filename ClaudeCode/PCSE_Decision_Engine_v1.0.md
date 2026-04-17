# Profit-Controlled Scaling Engine (PCSE) v1.0
## Final Decision Engine — Merged from 4 Proposals
**Date:** 13 April 2026
**Status:** FINAL — Production Ready
**Purpose:** THE brain that decides all bid, budget, pause actions

---

## COMPARISON: 4 Proposals Analyzed

### Proposal 1 (Initial — Claude)
```
Base:       ACOS distance from flat 25% target
Confidence: clicks-based (0.3 to 1.0)
Trend:      improving/stable/worsening
Missing:    No profit awareness, no CVR, no volume factor
Rating:     6/10 — too simple, flat target = wrong for different products
```

### Proposal 2 (Msir-Refined — True Profit Based)
```
Base:       ACR (Ad Cost on True Profit) — profit-aware!
Confidence: 0.1 to 1.0 (detailed click scale)
Trend:      3 levels
Formula:    25% profit = budget, 5% = bid (for new campaigns)
Missing:    No CVR factor, no volume factor, no entity classification
Rating:     8.5/10 — strong foundation, needs tactical add-ons
```

### Proposal 3 (Claude Expanded)
```
Same as P2 + cooling periods + pause rules + min/max limits + examples
Added:      Budget utilization check (don't increase if underspent)
Missing:    CVR factor, volume factor, prioritization
Rating:     8.7/10 — more complete but still missing tactical intelligence
```

### Proposal 4 (PCSE v1.0 — Msir Shared)
```
Base:       Target ACOS from break-even (= profit-aware via different path)
NEW:        CVR Factor (conversion rate vs account avg) — CRITICAL!
NEW:        Volume Factor (impression/click health) — CRITICAL!
NEW:        Entity classification (Scale/Optimize/Fix/Kill)
NEW:        Impossible Product filter
NEW:        Profit weight for budget decisions
NEW:        Multi-cycle logic (adjust → observe → adjust → pause)
NEW:        Prioritization engine
Rating:     9.3/10 — most complete, needs P2's ACR + confidence scale merged
```

---

## FINAL MERGED ENGINE: PCSE v1.0 (Best of All 4)

### What we KEEP from each:

| From | What | Why |
|------|------|-----|
| P2 | True Profit as foundation | Real money, not misleading ACOS |
| P2 | ACR (Ad Cost Ratio on True Profit) | Better than ACOS — directly measures profit erosion |
| P2 | Confidence scale (0.1 to 1.0, 10 levels) | More granular than P4's 5 levels |
| P2 | 25% profit = budget, 5% = bid (new campaigns) | Proven safe start |
| P3 | Cooling periods (3d bid, 2d budget) | Prevents over-optimization |
| P3 | Budget utilization check | Don't increase budget if underspent |
| P3 | Detailed pause rules | 4 clear conditions |
| P4 | CVR Factor (conversion rate) | CRITICAL — high CVR = scale, low CVR = restrict |
| P4 | Volume Factor (impression/click health) | CRITICAL — diagnoses visibility vs attractiveness |
| P4 | Entity Classification (Scale/Optimize/Fix/Kill) | Clear decision framework |
| P4 | Impossible Product Filter | Saves 30-50% wasted spend |
| P4 | Profit Weight for budget | High profit products get more budget |
| P4 | Multi-Cycle Logic | Prevents hasty decisions |
| P4 | Prioritization Engine | Fix worst first |

---

## 1. FOUNDATION: True Profit Per ASIN

```
True Profit = Sale Price
            - Product Cost (user input, 3-level inheritance)
            - Referral Fee (3% configurable)
            - Closing Fee (Rs.5 configurable)
            - Shipping (Rs.95 configurable)
            - Return Cost (5% of sale price, configurable)
```

### Derived Metrics:

```
Break-even CPA     = True Profit per unit
                     (max you can spend on ads per sale before loss)

Break-even ACOS    = (True Profit / Sale Price) × 100
                     (max ACOS before losing money)

Target ACOS        = Break-even ACOS × Safety Factor (0.7 default)
                     (your comfortable ACOS with 30% buffer)

ACR                = (Ad Spend per Sale / True Profit) × 100
                     (what % of your profit ads are eating)

Target ACR         = 40% (default = keep 60% profit after ads)
                     (configurable per account/category/product)
```

### Decision Metric: Use BOTH
```
ACOS → for classification (easy to understand, Amazon standard)
ACR  → for profit decisions (actual money impact)

Frontend shows: "Ad Efficiency: 27%" (= ACOS in simple language)
Backend uses: ACR for all calculations
```

---

## 2. ENTITY CLASSIFICATION (from P4)

Every campaign, keyword, product gets classified:

```
🟢 SCALE        ACR < Target ACR (40%)        → profitable, push harder
                 OR ACOS < Target ACOS

🟡 OPTIMIZE     Target ACR ≤ ACR ≤ 1.5× Target  → borderline, fine-tune
                 (40% ≤ ACR ≤ 60%)

🔴 FIX/REDUCE   1.5× Target < ACR ≤ 3× Target   → losing money, reduce
                 (60% < ACR ≤ 120%)

⛔ KILL/PAUSE    ACR > 3× Target                  → massive loss, stop
                 (ACR > 120%)
                 OR zero sales with spend > 2× sale price
```

---

## 3. IMPOSSIBLE PRODUCT FILTER (from P4)

**Run BEFORE any optimization — saves 30-50% wasted spend!**

```
IF True Profit < Rs.20 per unit:
  → "No Price Available — Excluded from Optimization" 
  → Don't run ads on this product

IF Break-even ACOS < 10%:
  → Product economics too tight for ads
  → Unless CPC < Rs.2 (very low competition)
  → Flag: "Low Margin — Ads Not Recommended"

IF True Profit = negative:
  → Product loses money even WITHOUT ads
  → Flag: "Product Cost > Sale Price — Fix Pricing First"
```

---

## 4. SMART BID ENGINE (MERGED BEST OF ALL)

### Master Formula:

```
quality_score = cvr_factor × volume_factor × margin_factor

bid_change_% = CLAMP(
    gap × confidence × trend × quality_score
, -MAX_CAP, +MAX_CAP)

WHERE MAX_CAP = based on confidence level (10% to 50%)
```

### Component 1: Gap (Core Signal) — from P4, enhanced with ACR

```
IF SCALE (profitable):
  gap = (target_ACR - current_ACR) / target_ACR × 0.5
  → Positive = room to increase bid
  → Example: ACR=15%, target=40% → gap = (40-15)/40 × 0.5 = +31%

IF FIX (losing):
  gap = (current_ACR - target_ACR) / current_ACR × 0.5
  → Negative = must decrease bid
  → Example: ACR=80%, target=40% → gap = (80-40)/80 × 0.5 = -25%

IF KILL:
  gap = not calculated → PAUSE directly
```

### Component 2: Confidence (UPGRADED — Conversion-Aware)

**Old (flawed):** Only clicks → 100 clicks with 0 sales = 0.7 (WRONG! no proof it works)
**New:** Clicks + Conversion stability = TRUE confidence

```
Step A: Base confidence from clicks
  0-5 clicks     → 0.1
  6-15           → 0.3
  16-30          → 0.5
  31-50          → 0.6
  51-100         → 0.7
  101-300        → 0.8
  301-1000       → 0.9
  1000+          → 1.0

Step B: Conversion adjustment
  IF orders = 0 AND clicks > 20:  confidence × 0.5  (no proof of conversion!)
  IF orders >= 3 AND CVR > account avg: confidence × 1.1  (proven converter!)
  IF orders = 1 (single lucky sale): confidence × 0.7  (not reliable yet)
  
  CLAMP confidence: min 0.1, max 1.0

Example:
  100 clicks, 0 orders → base 0.7 × 0.5 = 0.35 (LOW! don't act boldly)
  30 clicks, 5 orders  → base 0.5 × 1.1 = 0.55 (decent! can act)
  50 clicks, 1 order   → base 0.6 × 0.7 = 0.42 (cautious, single sale)
```

### HARD CAPS based on Confidence (Safety Layer):
```
confidence < 0.3  → max bid change ±10% (almost no data)
confidence 0.3-0.5 → max bid change ±25%
confidence 0.5-0.8 → max bid change ±40%
confidence > 0.8   → max bid change ±50% (full range)
```

### Component 3: Trend (from P3/P4 merged)

```
Compare: This week ACR vs Last week ACR

Improving (ACR dropping)  → 0.5 (less aggressive, let trend continue)
Stable (±5%)              → 1.0
Worsening (ACR rising)    → 1.4 (more aggressive, act faster)

Note: P4 uses 0.6/1.0/1.4, P2 uses 0.5/1.0/1.5
→ We use 0.5/1.0/1.4 (slightly less extreme on worsening)
```

### Component 4: CVR Factor (NEW from P4 — CRITICAL)

```
CVR = Orders / Clicks (conversion rate)
Account Avg CVR = Total Orders / Total Clicks (across all campaigns)

CVR Ratio = Keyword CVR / Account Avg CVR

> 120% of avg → 1.2 (this converts WELL → scale more aggressively)
80-120%      → 1.0 (normal)
< 80%        → 0.7 (converts poorly → restrict, don't throw money)

WHY THIS MATTERS:
  Keyword A: ACOS 30%, CVR 8% → good converter, scale!
  Keyword B: ACOS 30%, CVR 1% → lucky few sales, don't scale blindly
  
  Without CVR factor: both get same treatment (WRONG!)
  With CVR factor: A gets +20% boost, B gets -30% restriction (RIGHT!)
```

### Component 5: Volume Factor (NEW from P4 — CRITICAL)

```
Diagnoses: Is the problem visibility or attractiveness?

High impressions + Low clicks (CTR < 0.2%)  → 0.7
  = People see ad but don't click
  = Problem is ad copy/image/price, NOT bid
  = Increasing bid won't help → restrict

Low impressions (< 100 in 7 days)           → 1.2
  = Ad not getting shown enough
  = Bid too low for competition
  = Increase bid to gain visibility

Normal (CTR > 0.3%, reasonable impressions) → 1.0
  = Healthy, normal processing

WHY THIS MATTERS:
  10,000 impressions + 5 clicks = terrible CTR
  Increasing bid = more impressions = still no clicks = more waste!
  
  100 impressions + 3 clicks = good CTR, just need more visibility
  Increasing bid = more impressions = proportionally more clicks = good!
```

### Component 6: Margin Factor (NEW — from P5 analysis)

```
margin_factor = True Profit / Sale Price

HIGH margin (> 50%):  → 1.2 (scale faster, can afford more)
MEDIUM (20-50%):      → 1.0 (normal)
LOW (< 20%):          → 0.7 (tight margin, conservative)

WHY IN BID FORMULA (not just budget):
  Product A: Rs.999, True Profit Rs.600 (60%) → can afford high bids
  Product B: Rs.999, True Profit Rs.50 (5%)  → every rupee matters

  Same ACOS, same clicks, same CVR — but A should bid MORE aggressively!
  Without margin_factor: both treated same (WRONG)
  With margin_factor: A gets 1.2x, B gets 0.7x (RIGHT)
```

### Quality Score (combined):
```
quality_score = cvr_factor × volume_factor × margin_factor

This groups the "product intelligence" signals:
  CVR = does it convert? (demand signal)
  Volume = is it visible? (supply signal)
  Margin = can it afford ads? (economic signal)

CLAMP quality_score: min 0.3, max 1.8
(prevents extreme multiplication)
```

### FULL EXAMPLES (All 6 Factors):

```
EXAMPLE 1: STAR keyword (Scale Up)
═══════════════════════════════════
Keyword: "celtic sea salt organic"
Sale Price: Rs.924 | True Profit: Rs.492 (53% margin)
Ad Spend per Sale: Rs.58 | ACR: 11.8% | Target ACR: 40%
Clicks: 56 | Orders: 4 | CVR: 7.1% (acct avg: 4.5%)
Impressions: 8900 | CTR: 0.63% | Trend: stable

Classification: 🟢 SCALE (ACR 11.8% < 40%)

CALCULATION:
  gap            = (40-11.8)/40 × 0.5 = +35.3%
  confidence     = base 0.7 (56 clicks) × 1.1 (4 orders, CVR > avg) = 0.77
  trend          = 1.0 (stable)
  cvr_factor     = 1.2 (7.1% vs 4.5% = 158%)
  volume_factor  = 1.0 (CTR 0.63% = healthy)
  margin_factor  = 1.2 (53% margin = high)
  quality_score  = 1.2 × 1.0 × 1.2 = 1.44

  bid_change = 35.3% × 0.77 × 1.0 × 1.44 = 39.1%
  confidence cap = 0.77 → max ±40%
  CLAMP → 39%

  → "Increase Bid 39%" ✅ (high margin + high CVR = aggressive scale!)
```

```
EXAMPLE 2: WASTE keyword (Reduce)
═══════════════════════════════════
Keyword: "ashwagandha powder"
Sale Price: Rs.499 | True Profit: Rs.200 (40% margin)
Spend: Rs.1048 | Orders: 0 | ACR: INFINITE
Clicks: 13 | CVR: 0% | Trend: worsening
Impressions: 1500 | CTR: 0.87%

Classification: ⛔ KILL (zero sales, high spend)

BUT confidence check:
  base = 0.3 (13 clicks) × 0.5 (0 orders) = 0.15
  confidence 0.15 < 0.3 → hard cap ±10%

DECISION CYCLE 1:
  → "Reduce Bid 10% + Monitor" (not enough data to PAUSE yet)

CYCLE 2 (3 days later, now 26 clicks, still 0 orders):
  confidence = 0.5 × 0.5 = 0.25 → still < 0.3 → cap ±10%
  → "Reduce Bid 10% more"

CYCLE 3 (now 40 clicks, 0 orders):
  confidence = 0.6 × 0.5 = 0.30 → cap ±25%
  Spend now > 2× sale price (Rs.1500 > Rs.998)
  → PAUSE Rule 1 triggered
  → "PAUSE Keyword" ✅
```

```
EXAMPLE 3: Low margin product (Conservative)
═══════════════════════════════════════════════
Keyword: "sea salt"
Sale Price: Rs.99 | True Profit: Rs.-11 (NEGATIVE!)

Classification: IMPOSSIBLE PRODUCT FILTER triggered!
  True Profit negative → product loses money even without ads
  
  → "Fix Product Pricing First — Ads Will Only Increase Loss"
  → Excluded from all optimization
  → No bid calculation needed
```

```
EXAMPLE 4: High clicks, zero conversion (Volume Factor saves money)
════════════════════════════════════════════════════════════════════
Keyword: "loose-match" (auto targeting)
Impressions: 15,000 | Clicks: 106 | Orders: 0 | CTR: 0.7%
Spend: Rs.5,352

  volume_factor: High impressions + decent clicks BUT 0 orders
  cvr_factor: 0% CVR vs 4.5% avg = 0 → clamp to 0.5
  confidence: base 0.8 (106 clicks) × 0.5 (0 orders) = 0.4
  
  quality_score = 0.5 × 1.0 × 1.0 = 0.5 (restricted!)
  
  Without quality_score: might try to reduce bid and keep running
  With quality_score: heavily restricted → "Add as Negative + PAUSE"
```

---

## 5. BUDGET ENGINE (MERGED)

### SCALE Budget (Increase):

```
CONDITIONS (ALL must be true):
  1. ACR < Target ACR (profitable)
  2. Budget Utilization ≥ 90% (spending full budget = bottleneck)
  3. Buy Box = ours (no point scaling if we lose Buy Box)

FORMULA:
  increase = min(50%, gap × 0.7 × profit_weight)

  profit_weight (from P4):
    True Profit > Rs.500/unit → 1.2 (high margin = invest more)
    True Profit Rs.100-500    → 1.0 (normal)
    True Profit < Rs.100      → 0.7 (tight margin = cautious)

EXAMPLE:
  Celtic Salt: ACR=12%, Target=40%, Budget 100% used
  True Profit Rs.492 → profit_weight = 1.0 (medium)
  gap = (40-12)/40 = 70%
  increase = min(50%, 70% × 0.7 × 1.0) = min(50%, 49%) = 49%
  → "Increase Budget 49%"
```

### REDUCE Budget (Decrease):

```
CONDITIONS:
  ACR > Target ACR (losing money on ads)

FORMULA:
  decrease = min(70%, over_ratio × 0.6)

  over_ratio = (current_ACR - target_ACR) / current_ACR

EXAMPLE:
  AcvMoringa: ACR=3299%, Target=40%
  over_ratio = (3299-40)/3299 = 98.8%
  decrease = min(70%, 98.8% × 0.6) = min(70%, 59.3%) = 59%
  BUT ACR > 300% → KILL category → "PAUSE Campaign" instead
```

### CRITICAL RULE (from P2/P3/P4 — all agree):

```
IF Budget NOT fully used (< 90% utilization):
  → DO NOT increase budget
  → Problem is bids/targeting, not budget
  → Action: "Increase Bids 15% first" (budget available, not spent)

This prevents: throwing money at a budget that isn't even being used
```

---

## 6. PAUSE ENGINE (STRICT BUT SMART — merged P3+P4)

```
PAUSE if ANY of these:

Rule 1: Spend > 2× Sale Price AND 0 sales (7 days)
  Example: Product Rs.999, Spend Rs.2000+, Zero orders → PAUSE
  Why: Spent more than the product costs twice, still no sale

Rule 2: ACR > 300% AND clicks > 20 (enough data)
  Example: ACR 500%, 25 clicks → clearly not working → PAUSE
  Why 20 clicks minimum: less clicks = not enough data to judge

Rule 3: 14 days consecutive loss + no improvement trend
  Example: Week 1 ACR 200%, Week 2 ACR 210% → worsening → PAUSE
  Why 14 days: gives 2 optimization cycles before giving up

Rule 4: Break-even ACOS < 10% AND current ACOS > 50%
  Example: Product True Profit Rs.15 on Rs.199 price = 7.5% BE ACOS
  Current ACOS 55% → impossible to optimize down to 7.5%
  → "Low Margin — Ads Not Recommended"

Rule 5 (NEW): True Profit negative (product loses money even without ads)
  → "Fix Product Pricing First — Ads Will Only Increase Loss"
```

---

## 7. LEARNING PERIOD — DUAL COOLING (C24) ⚠️ CRITICAL!

### BEFORE any optimization, campaign MUST pass learning period:

```
Learning Period = EITHER condition met (whichever FIRST):
  
  Condition A: minimum_days elapsed     (default: 7 days, configurable)
  Condition B: minimum_budget spent     (default: Rs.2000, configurable)
  
  WHICHEVER COMES FIRST → learning over → optimization starts
  UNTIL THEN → DO NOT OPTIMIZE, DO NOT PAUSE, DO NOT CHANGE ANYTHING!
```

### Why DUAL (not just days)?

```
Only Days:  Campaign spends Rs.10,000 in 3 days → still waiting 4 more days 
            → LOSING money while waiting! (BAD)

Only Budget: Campaign spends Rs.50/day → takes 40 days to reach Rs.2000
             → waiting too long! (BAD)

DUAL: Spend Rs.2000 fast? → optimize early (budget condition met)
      Spend slow? → at least wait 7 days (time condition met)
      → SMART!
```

### In Excel Report — Learning Period Display:

```
Campaign in learning period:
  Classification: "📚 Learning Phase"
  ToDo: "Learning — Day 3/7, Rs.800/Rs.2000 spent"
  AI Reason: "New campaign in learning phase. Collecting data. 
              No changes until Day 7 or Rs.2000 spent (whichever first)."
  Approval: blank (no action possible)
  Confidence: N/A
```

### Exception — EMERGENCY override during learning:

```
EVEN during learning period, PAUSE if:
  Spend > 3× Sale Price AND zero sales
  (Emergency: campaign burning too much without any result)
  
  Example: Rs.2999 spent on Rs.999 product, 0 orders
  → Even Day 2 → PAUSE (emergency override)
  
  This is the ONLY exception to learning period.
```

### Configurable Settings:

```
config:
  learning_period_days: 7          (default, range: 3-14)
  learning_period_budget: 2000     (default, range: 500-10000)
  learning_emergency_multiplier: 3 (pause if spend > 3× sale price)
```

---

## 8. NEW CAMPAIGN FORMULA (from P2 — Msir approved)

For brand new campaigns with ZERO historical data:

```
Budget = True Profit × 25% (per day)
Bid    = Budget × 5%
Bidding: Dynamic DOWN ONLY (safe start)

After learning period complete:
  → Switch to PCSE formula (gap × confidence × trend × quality_score)
```

---

## 8. STABILITY SYSTEM (ANTI-OVEROPTIMIZATION)

### Cooling Periods (from P3):

```
After Bid change    → wait 3 days (Amazon takes time to adjust auction)
After Budget change → wait 2 days
After PAUSE         → re-evaluate after 7 days
```

### Multi-Cycle Logic (from P4):

```
Cycle 1 (Day 1-3):   Adjust bid/budget based on current data
Cycle 2 (Day 4-6):   OBSERVE — no changes, collect new data
Cycle 3 (Day 7-9):   Adjust again based on new data
Cycle 4 (Day 10-12): If still bad after 2 adjustments → PAUSE

This prevents:
  Day 1: bid -20%
  Day 2: still bad → bid -30% (WRONG! Day 1 change hasn't taken effect!)
  
  Instead:
  Day 1: bid -20%
  Day 2-3: wait
  Day 4: check → still bad? → bid -25% more
  Day 5-6: wait
  Day 7: check → still bad after 2 tries? → PAUSE
```

### Max Change Limits:

```
Per Cycle:
  Bid:    min 5%, max 50%
  Budget: min 10% decrease, max 70% decrease
  Budget: max 50% increase
  
Lifetime (across all cycles):
  Total bid decrease from original: max 80%
  Total budget decrease: max 90% (leave 10% for data flow)
```

---

## 9. PRIORITIZATION ENGINE (from P4)

### What to fix FIRST (execution order):

```
Priority 1: 🔴 High spend + Zero sales (IMMEDIATE MONEY DRAIN)
  → PAUSE or reduce drastically
  → Impact: stops bleeding immediately

Priority 2: 🔴 High loss campaigns (ACR > 200%)
  → Reduce budget 50-70%
  → Impact: reduces daily loss significantly

Priority 3: 🟡 Borderline high spend (ACR 60-120%)
  → Optimize bids, add negatives
  → Impact: converts loss into breakeven or profit

Priority 4: 🟢 Profitable campaigns needing scale (ACR < 40%)
  → Increase budget/bids
  → Impact: grows revenue and profit

ORDER MATTERS: Fix losses BEFORE scaling wins
  Why: Stopping Rs.5000/day waste = same as earning Rs.5000/day
  But stopping waste is FASTER and more certain than growing revenue
```

---

## 10. SIMPLE LANGUAGE (Frontend = Sweet Pot)

### ACOS → "Ad Efficiency"
### ACR → "Profit After Ads"
### CVR → "Sale Conversion Rate"
### Break-even ACOS → "Maximum Safe Ad Cost"
### Target ACOS → "Your Comfort Zone"
### TACoS → "Overall Ad Health"

### Classification Labels:
```
🟢 SCALE     → "Star Performer — Scale Up!"
🟡 OPTIMIZE  → "Good but Improvable"
🔴 FIX       → "Losing Money — Needs Attention"
⛔ KILL      → "Heavy Loss — Recommend Pause"
```

---

## FINAL CHECKLIST

| Component | Source | Status |
|-----------|--------|--------|
| True Profit foundation | P2 | ✅ |
| ACR metric | P2 | ✅ |
| ACOS for classification | P4 | ✅ |
| Confidence (conversion-aware!) | P2 + P5 upgrade | ✅ UPGRADED |
| Confidence-based hard caps | P5 (NEW) | ✅ NEW |
| Trend modifier | P3/P4 merged | ✅ |
| CVR Factor | P4 | ✅ |
| Volume Factor | P4 | ✅ |
| Margin Factor (in bid formula) | P5 (NEW) | ✅ NEW |
| Quality Score (CVR × Volume × Margin) | P5 structure | ✅ NEW |
| Entity Classification | P4 | ✅ |
| Impossible Product Filter | P4 | ✅ |
| Budget Utilization Check | P2/P3/P4 | ✅ |
| Profit Weight (budget) | P4 | ✅ |
| Cooling Periods | P3 | ✅ |
| Multi-Cycle Logic | P4 | ✅ |
| Prioritization | P4 | ✅ |
| Learning Period DUAL (C24) | Msir correction! | ✅ ADDED |
| Emergency override during learning | PCSE safety | ✅ ADDED |
| New Campaign Formula | P2 (Msir) | ✅ |
| Pause Rules (5 rules) | P3+P4 merged | ✅ |
| CLAMP with dynamic caps | P5 | ✅ NEW |
| Simple Language | Msir rule | ✅ |

### P5 Upgrades Adopted:
1. ✅ Conversion-aware confidence (clicks + orders, not just clicks)
2. ✅ Margin factor in bid formula (not just budget)
3. ✅ Confidence-based hard caps (low data = max ±10%)
4. ✅ Quality score grouping (CVR × Volume × Margin)
5. ✅ CLAMP with dynamic max based on confidence

### P5 Deferred to Phase 2:
- Trend as velocity/slope (needs time-series math)
- Log normalization for volume (mathematical refinement)

---

*PCSE v1.0 — 13 April 2026*
*Merged from 5 proposals: P1 (initial) + P2 (Msir True Profit) + P3 (expanded) + P4 (PCSE) + P5 (production-grade)*
*21 components, 6 factors in master formula, 5 pause rules, 4 classification levels*

---

*PCSE v1.0 — 13 April 2026*
*Merged from 4 proposals: the best of each, none of the weaknesses*
*This IS the production decision engine.*
