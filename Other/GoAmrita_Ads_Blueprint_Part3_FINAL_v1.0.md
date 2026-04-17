# 💎 GoAmrita Ads Optimization — Blueprint PART 3 (FINAL DIAMOND EDITION)
## All Corrections Applied + All New Features + Blue Ocean Strategy
**Date:** 11 April 2026 | **Version:** 1.0

---

# SECTION A: ✅ ALL USER CORRECTIONS APPLIED

## A.1 — IQ Score System (Backend Only → User Gets Easy Labels)

### Backend (Hidden from User):
```python
# IQ Score Engine (Backend calculation)
def calculate_iq_score(metric_data):
    score = 0
    score += conversion_rate_score(0-25)
    score += acos_efficiency_score(0-25)
    score += trend_direction_score(0-20)
    score += historical_success_score(0-15)
    score += confidence_level(0-15)
    return score  # 0-100
```

### What User SEES (Simple Labels → All Pre-Approved):

| Backend IQ | User Label (Auto-filled in Excel) | Default Status |
|-----------|----------------------------------|----------------|
| 90-100 | 🟢 **"Strong Recommend & Approved"** | ✅ APPROVED |
| 75-89 | 🟢 **"Good to Do & Approved"** | ✅ APPROVED |
| 60-74 | 🟡 **"Medium Recommend & Approved"** | ✅ APPROVED |
| 40-59 | 🟡 **"May Try This New Strategy & Approved"** | ✅ APPROVED |
| 20-39 | 🟠 **"Low Confidence & Review"** | 📋 REVIEW |
| 0-19 | 🔴 **"Not Recommended & Skip"** | ⏭️ SKIP |

**Key:** ALL cells default = APPROVED. User rarely needs to change.  
User CAN change any cell to: `Approved` / `Reject` / `Skip` / `Custom Value`

## A.2 — Campaign Exclusion = TIME-BASED (Not Lifetime)
```
🚫 EXCLUSION SYSTEM:

Config: excluded_campaigns = [
  {"campaign_id": "xxx", "exclude_days": 30, "start_date": "2026-04-11", "reason": "testing new structure"},
  {"campaign_id": "yyy", "exclude_days": 14, "start_date": "2026-04-15", "reason": "seasonal product"}
]

Behavior:
├── Excluded for defined number of days ONLY
├── After days expire → automatically re-enters optimization cycle
├── Still monitored (data collected) during exclusion
├── Still shows in reports (marked as "EXCLUDED - X days left")
├── User can manually remove exclusion anytime
└── NOT lifetime — everything eventually gets optimized
```

## A.3 — Post-Change Response Monitoring → Smart Decision
```
📊 AFTER EVERY CHANGE:

Day 1-3: OBSERVE (just collect data)
Day 4-7: ANALYZE (is it improving?)

Then DECIDE:
├── IF improving → Continue same direction (increase/decrease more, smaller %)
├── IF no change → Hold position, try 3 more days
├── IF worsening → REVERSE the change (rollback to old value)
├── IF mixed → Try NEW strategy (different approach)

Decision auto-logged with reason:
"Bid increased ₹5→₹6 on Day 1. By Day 7: ACoS improved 22%→18%. 
 Decision: CONTINUE. Next action: Increase ₹6→₹6.30 (+5%)"
```

## A.4 — Product Strategy Modes (UPDATED with Budget & Day Limits)
```
📦 PRODUCT STRATEGY MODES:

🔴 EXTRA AGGRESSIVE (100% Mode — New Product Launch)
├── Bid multiplier: 2x normal
├── ACoS target: Up to 100% (spend = sales, break-even on ads)
├── MAX BUDGET LIMIT: ₹___/day (user configurable)
├── MAX DAYS LIMIT: ___ days (user configurable, default: 15)
├── After max days → AUTO SHIFTS to AGGRESSIVE
├── Purpose: Dominate rankings, get reviews fast
└── Use: Brand new product, first 2 weeks

🟠 AGGRESSIVE (50% Mode)
├── Bid multiplier: 1.5x normal
├── ACoS target: Up to 50%
├── MAX BUDGET LIMIT: ₹___/day (user configurable)
├── MAX DAYS LIMIT: ___ days (user configurable, default: 30)
├── After max days → AUTO SHIFTS to AVERAGE
├── Purpose: Fast growth, market capture
└── Use: New product after initial push

🟡 AVERAGE (Balanced Mode)
├── Bid multiplier: 1x normal
├── ACoS target: 15-25%
├── Budget: Normal allocation
├── No time limit — steady state
├── Purpose: Growth + Profit balance
└── Use: Growing products

🟢 PROFITABLE ONLY (Conservative Mode)
├── Bid multiplier: 0.7x normal
├── ACoS target: < 15% strict
├── Budget: Minimum efficient
├── Only proven exact keywords
├── Purpose: Maximum profit extraction
└── Use: Established products with good organic rank

🤖 AUTOMATIC (AI Decides)
├── New product → Start EXTRA AGGRESSIVE (X days)
├── After X days → AGGRESSIVE (Y days)
├── After Y days → AVERAGE
├── If ACoS < 15% consistently → PROFITABLE
├── If ACoS spikes → Back to AVERAGE
├── All transitions logged with reason
└── User just sets product mode to "AUTO" and forgets
```

## A.5 — TRUE PROFIT Based ACoS (NEW — Game Changer!)
```
💰 REAL PROFIT ACoS vs AMAZON ACoS:

❌ What Amazon Shows (MISLEADING):
   ACoS = Ad Spend ÷ Sale Price × 100
   Example: ₹50 ad spend ÷ ₹500 sale = 10% ACoS (looks great!)

✅ What ACTUALLY Matters (OUR SYSTEM):
   True ACoS = Ad Spend ÷ ACTUAL PROFIT × 100
   
   ACTUAL PROFIT per sale = Sale Price
     − Product cost (COGS)
     − Amazon referral fee (typically 5-15%)
     − FBA/shipping fees
     − Packaging cost
     − GST component
     − Returns allowance (2-5% buffer)
     = TRUE PROFIT

   Example Reality:
   Sale Price: ₹500
   − COGS: ₹200
   − Referral fee (12%): ₹60
   − FBA/Shipping: ₹80
   − Packaging: ₹20
   − GST: ₹30
   − Returns buffer (3%): ₹15
   = TRUE PROFIT: ₹95

   Now: ₹50 ad spend ÷ ₹95 profit = 52.6% TRUE ACoS!
   
   Amazon showed 10% → Reality is 52.6% → LOSING MONEY!

USER INPUT (One-time per product):
{
  "product_id": "ASIN123",
  "sale_price": 500,
  "cogs": 200,
  "referral_fee_pct": 12,
  "fba_fee": 80,
  "packaging": 20,
  "gst_pct": 6,
  "returns_pct": 3,
  "other_costs": 0
}

SYSTEM AUTO-CALCULATES:
├── True profit per sale
├── Break-even ACoS (max ACoS where you still profit)
├── Target ACoS (comfortable profit margin)
├── Maximum bid (profitable bid limit)
└── All reports show BOTH: Amazon ACoS AND True ACoS
```

## A.6 — Search Term Monitoring (Not Auto Campaign)
```
🔍 KEYWORD DISCOVERY (OUR METHOD):

Primary Source: Amazon Search Bar Auto-Suggestions
├── Manual research on Amazon.in buyer portal
├── Type product-related terms
├── Collect auto-suggested keywords
└── These are REAL customer searches

Secondary Source: Search Term Report Monitoring
├── NOT from Auto campaigns (we don't use Auto)
├── FROM our Phrase Match campaigns
├── Monitor what actual buyers searched to find us
├── Discover new keyword variations
├── Find negative keyword candidates
└── This is ONGOING keyword intelligence

System monitors Phrase campaign search terms:
├── High converting terms → Recommend: Add to Exact campaign
├── Irrelevant terms → Recommend: Add as Negative
├── New interesting terms → Flag for review
└── All with IQ scores and auto-filled recommendations
```

## A.7 — Excel Design (Multi-Tab: Reports + Action Templates)
```
📊 EXCEL FILE STRUCTURE:

PART 1: REPORT TABS (User READS these — visual, colorful)
├── Tab 1: Dashboard (glance view)
├── Tab 2: Strategy Impact Log (what worked/didn't)
├── Tab 3: Trends & Comparisons
├── Tab 4: Search Terms Intelligence
├── Tab 5: Product Performance
├── Tab 6: Full Changelog
└── Tab 7: Calendar & Reminders

PART 2: ACTION TABS (Tool READS these when user returns Excel)
├── Tab A1: CRITICAL Actions (pre-approved, just review)
├── Tab A2: STRONG Actions (pre-approved, just review)
├── Tab A3: NORMAL Actions (approved, review recommended)
├── Tab A4: NEW STRATEGY Actions (approved, worth trying)
└── Tab A5: CUSTOM Actions (user can add manual actions)

When user returns Excel:
├── System reads ONLY Action tabs (A1-A5)
├── Processes all "Approved" rows
├── Skips all "Reject" / "Skip" rows
├── Executes "Custom" values as specified
└── Logs everything to changelog
```

## A.8 — Full Transparency (NOT Black Box)
```
🔍 EVERY DECISION IS EXPLAINED:

In every action row:
├── WHAT: "Increase bid from ₹5 → ₹6"
├── WHY: "ACoS improved 22%→18% in 7 days, still below target"
├── EVIDENCE: "7-day trend: ↓ steady, 15 clicks, 3 orders"
├── RISK: "Low risk — proven keyword with consistent sales"
├── IQ SCORE: 85 (Backend)
├── LABEL: "Good to Do & Approved" (User sees this)
├── EXPECTED: "ACoS may improve to ~16%, daily spend +₹20"
└── PREVIOUS: "Last time similar change on this keyword: +12% improvement"

Nothing is hidden. User always knows WHY.
```

---

# SECTION B: 🆕 NEW KILLER FEATURES (Blue Ocean Advantages)

## B.1 — 🎯 Competitor Intelligence Module

### Feature: Competitor Price & Stock Monitor
```
🕵️ COMPETITOR TRACKING (via SP-API + scraping):

What we track for top 5 competitors per product:
├── Current price (daily check)
├── Price history (trend: going up or down?)
├── Stock status (in stock / out of stock)
├── BSR (Best Seller Rank) trend
├── Review count & rating
├── Coupon/Deal status
└── Buy Box winner

SMART ACTIONS:
├── Competitor OUT OF STOCK → 🟢 ALERT: "Increase bid! Competitor gone!"
│   └── Auto-recommend: Increase bid 20%, increase budget 30%
│
├── Competitor PRICE DROP → 🟡 ALERT: "Competitor cut price to ₹X"
│   └── Auto-recommend: Review our pricing, maybe adjust bids down
│
├── Competitor RUNNING DEAL → 🟡 ALERT: "Competitor has Lightning Deal"
│   └── Auto-recommend: Save budget today, they'll capture traffic
│
├── Our BSR IMPROVING → 🟢 "Organic rank rising!"
│   └── Auto-recommend: Gradually reduce aggressive bids
│
└── Our BSR DROPPING → 🔴 "Organic rank falling!"
    └── Auto-recommend: Increase visibility, check listing quality
```

## B.2 — 📈 TACoS Tracker (Total ACoS = True Health Metric)

```
📊 TACoS = Total Advertising Cost of Sales

TACoS = Ad Spend ÷ TOTAL Revenue (organic + ad sales) × 100

Why TACoS > ACoS:
├── ACoS only shows ad-attributed sales
├── TACoS shows FULL business health
├── If TACoS is DECREASING over time = 🟢 WINNING
│   (means organic sales growing, less ad-dependent)
├── If TACoS is INCREASING = 🔴 WARNING
│   (means more dependent on ads, organic declining)
└── Goal: TACoS should steadily decrease month over month

TACoS TARGETS:
├── New product: TACoS 20-30% (heavy ad-dependent = normal)
├── Growing product: TACoS 10-20% (building organic)
├── Established product: TACoS 5-10% (organic-dominant = IDEAL)
└── Market leader: TACoS < 5% (barely needs ads)

System tracks:
├── Daily TACoS trend
├── Weekly TACoS comparison
├── Per-product TACoS breakdown
├── TACoS vs ACoS correlation
└── Alert if TACoS trending UP consistently
```

## B.3 — 🔄 Organic Rank Flywheel Engine

```
🌊 THE FLYWHEEL EFFECT:

Ads → Sales → Better Rank → More Organic Sales → Less Ad Dependency

Our system tracks this cycle:
├── Phase 1: LAUNCH (heavy ads, ACoS high, TACoS high)
│   → System says: "Normal. Keep spending. Building momentum."
│
├── Phase 2: TRACTION (ads working, some organic sales appearing)
│   → System says: "Flywheel starting! TACoS dropping. Keep steady."
│
├── Phase 3: MOMENTUM (organic sales growing, can reduce ads)
│   → System says: "Reduce bid 5%. Organic carrying more weight."
│
├── Phase 4: DOMINANCE (organic is primary, ads are support only)
│   → System says: "Switch to PROFITABLE mode. Minimum ads needed."
│
└── Phase 5: DEFEND (maintain position, block competitors)
    → System says: "Defense mode. Brand keywords only. Minimum spend."

This is AUTO-DETECTED per product based on TACoS trend.
Product strategy auto-shifts through these phases.
```

## B.4 — 🛡️ Listing Health Monitor

```
🏥 LISTING PROTECTION SYSTEM:

CHECK 1: Stock Status
├── If product going OUT OF STOCK soon → PAUSE ads (don't waste money!)
├── If back in stock → RESUME ads automatically
├── Track: current stock, daily sales velocity, days of stock left
└── Alert at: 7 days, 3 days, 1 day before stockout

CHECK 2: Buy Box Status
├── If WE have Buy Box → Ads are effective, continue
├── If we LOST Buy Box → PAUSE ads immediately!
│   (Running ads without Buy Box = pure waste)
├── Alert: "Buy Box lost to seller X at price ₹Y"
└── Recommend: price adjustment or wait

CHECK 3: Listing Suppression
├── If listing suppressed by Amazon → PAUSE ads
├── Alert: "Listing suppressed! Fix immediately!"
├── Reason detection if possible
└── Checklist: compliance, images, keywords, category

CHECK 4: Review Score Drop
├── If rating drops below 3.5★ → Reduce bids 30%
├── At 3.5★ conversion rate drops sharply
├── Alert: "Rating dropped to X★ — check recent reviews"
└── No point bidding high on low-rated product

CHECK 5: Price Competitiveness
├── If our price > category average significantly → Flag
├── High price + high bid = terrible conversion
├── Recommend: adjust price or reduce bids
└── Compare with top 5 competitors daily
```

## B.5 — 💸 Budget Waste Detector (Money Saver #1)

```
🚨 WASTE DETECTION RULES:

LEVEL 1: OBVIOUS WASTE (Auto-negate immediately in full-auto mode)
├── Search term with ₹500+ spend AND 0 orders → BLOCK
├── Search term with 20+ clicks AND 0 orders → BLOCK
├── Keyword with ACoS > 100% for 7+ days → PAUSE
└── Expected saving: 20-30% of wasted budget

LEVEL 2: SLOW BLEED (The "Death by 1000 Cuts" problem)
├── Many keywords each wasting ₹10-50
├── Individually small, but TOTAL = huge waste
├── System aggregates ALL small wasters
├── Report: "257 keywords each wasting ₹10-50 = ₹6,400 total waste"
└── Batch negative/pause recommendations

LEVEL 3: STRUCTURAL WASTE
├── Duplicate keywords across campaigns (bidding against yourself)
├── Phrase match catching terms already in Exact (cannibalization)
├── Budget exhausting before peak hours
├── High bids on low-margin products
└── Ads running on out-of-stock products

LEVEL 4: OPPORTUNITY COST
├── Budget spent on Product A (low margin) instead of Product B (high margin)
├── Money going to "awareness" keywords when "purchase" keywords exist
├── High-profit products getting low budget allocation
└── Recommend: budget redistribution for maximum profit

WASTE REPORT:
Daily "Money Saved" counter:
"Today: ₹X saved by blocking wasteful terms"
"This week: ₹Y saved"
"This month: ₹Z saved"
"Since system started: ₹TOTAL saved"
```

## B.6 — 🏷️ Smart Bid Ceiling (Maximum Profitable Bid)

```
💰 BID CEILING CALCULATOR:

For each keyword, system calculates MAXIMUM bid:

Max Profitable Bid = True Profit Per Sale × Conversion Rate

Example:
├── True profit per sale = ₹95
├── This keyword's conversion rate = 8%
├── Max bid = ₹95 × 0.08 = ₹7.60
├── At ₹7.60 bid, you break even on every click
├── Target bid = ₹7.60 × 0.7 = ₹5.32 (30% profit margin on ads)
└── System NEVER bids above ceiling, even in aggressive mode

This prevents:
├── Overbidding on low-profit products
├── Emotional bid wars with competitors  
├── Budget explosion during festivals
└── Guaranteed profitable bids (within ceiling)
```

## B.7 — 📅 Smart Day/Hour Budget Pacing

```
⏰ BUDGET PACING SYSTEM:

Problem: ₹1000 daily budget runs out by 11 AM
         Misses 6-10 PM PRIME TIME (best conversion hours)

Solution: Hourly budget allocation

Hour-wise Budget Split (Health/Food Category India):
6-8 AM:   8% of budget (health searches start)
8-11 AM:  15% (office hours, health research)  
11-2 PM:  12% (lunch browsing)
2-5 PM:   10% (low activity)
5-8 PM:   25% (PRIME — evening shopping)
8-11 PM:  20% (family decision time)
11-6 AM:  10% (minimal)

Implementation:
├── Amazon's Bid Schedule Rules → increase bids during peak hours
├── Our system → adjusts campaign budgets through the day
├── Monitor hourly spend rate
├── Alert if budget pace is too fast
└── All percentages configurable per product category
```

## B.8 — 🎯 Keyword Lifecycle Manager

```
📋 EVERY KEYWORD HAS A LIFECYCLE:

Stage 1: DISCOVERY (Found in search suggestion / search term report)
├── Status: NEW
├── Action: Add to Phrase Match campaign
├── Protection: COOLING period (7 days minimum)
├── Collect data, no changes
└── IQ Label: "May Try This New Strategy & Approved"

Stage 2: TESTING (Has some data)
├── Status: TESTING
├── Action: Monitor closely
├── If 10+ clicks, 0 orders → Consider pausing
├── If 2+ orders, decent ACoS → Promote to Exact
└── IQ Label: "Medium Recommend"

Stage 3: PROVEN (Consistent performer)
├── Status: PROVEN
├── Action: Move to Exact Match campaign
├── Optimize bid for maximum profit
├── Scale budget allocation
└── IQ Label: "Strong Recommend & Approved"

Stage 4: STAR (Top performer)
├── Status: STAR ⭐
├── Action: Maximum bid (within ceiling), protect this keyword
├── If competitor appears → increase bid to defend
├── Track organic rank for this keyword
└── IQ Label: "Strong Recommend & Approved"

Stage 5: DECLINING (Was good, now fading)
├── Status: DECLINING
├── Action: Reduce bid gradually
├── Investigate: seasonal? competitor? listing issue?
├── If no recovery in 14 days → move to RETIRED
└── IQ Label: "Low Confidence & Review"

Stage 6: RETIRED (Not working)
├── Status: RETIRED
├── Action: Pause, add as negative in broader campaigns
├── Keep in records for future reference
├── Can be RE-TESTED after 90 days
└── Auto-filled: "Not Recommended & Skip"
```

## B.9 — 🧠 Strategy Learning Database

```
📚 WHAT WORKED / WHAT DIDN'T → KNOWLEDGE BASE

The system builds a permanent knowledge base:

Entry format:
{
  "date": "2026-04-15",
  "product_category": "honey",
  "action": "increased bid 10% on 'pure honey 1kg'",
  "before": {"acos": 22, "orders": 3, "spend": 150},
  "after_7_days": {"acos": 18, "orders": 5, "spend": 180},
  "iq_score": 82,
  "verdict": "SMART",
  "lesson": "Bid increase on proven exact keywords in honey category improves volume with better ACoS",
  "reuse_for": ["similar honey keywords", "similar price range products"]
}

SMART SUGGESTIONS based on history:
"Last month, increasing bid on honey keywords by 10% improved ACoS by 18%.
 You have 5 similar keywords that haven't been optimized yet.
 Recommendation: Apply same strategy.
 Label: Strong Recommend & Approved"

This makes the system SMARTER every day:
├── Week 1: Generic rules (from blueprint)
├── Month 1: Learning YOUR product patterns
├── Month 3: Predicting what will work based on history
├── Month 6: Nearly autonomous — knows your business deeply
└── The longer you use it, the better it gets
```

## B.10 — 📧 Auto-Report & Auto-Open System

```
📬 DAILY AUTOMATION FLOW:

6:00 AM: System wakes up (cron/launchd)
6:01 AM: Pull yesterday's data from Amazon Ads API
6:05 AM: Run all analysis engines
6:10 AM: Generate daily Excel report
6:12 AM: Email report to configured addresses
6:15 AM: Open Excel on Mac automatically

User wakes up → Excel already open → reviews in 5 minutes → done!

MULTIPLE ALERT EMAILS:
├── Daily report: msir@email.com (with Excel attachment)
├── Critical alerts: msir@email.com + team@email.com (instant)
├── Weekly summary: msir@email.com (Monday 9 AM)
├── Monthly review: msir@email.com (1st of month)
└── All configurable in alert_config.json

AUTO-OPEN CONFIG:
{
  "auto_open_enabled": true,
  "open_time": "06:15",
  "application": "Microsoft Excel",
  "open_latest_report": true
}
```

## B.11 — 🔄 One-Click Approval → Execution Flow

```
📋 THE COMPLETE USER WORKFLOW:

Morning:
1. 🖥️ Open laptop → Excel already open
2. 👀 Check Dashboard tab (30 seconds)
3. 📊 Scan Actions tabs — everything pre-approved
4. ✏️ Change 0-5 cells if needed (rare)
5. 💾 Save Excel → put in "approved" folder
6. ✅ DONE! (Total time: 3-5 minutes)

System (Background):
7. 🤖 Detects new file in approved folder
8. 📖 Reads all Action tabs
9. ⚡ Executes all "Approved" actions via API
10. 📝 Logs every action to changelog
11. 📧 Sends confirmation email: "X actions executed"
12. 🔄 Tomorrow: measures effect of today's changes
```

---

# SECTION C: 🌊 BLUE OCEAN FEATURES (Market Domination)

## C.1 — Competitor Keyword Gap Analysis
```
🎯 FIND KEYWORDS COMPETITORS MISS:

Step 1: Identify top 10 competitors per product
Step 2: Analyze their visible keywords (from search results)
Step 3: Find keywords WE rank for but THEY don't
Step 4: Find keywords THEY rank for but WE don't
Step 5: Find keywords NOBODY is targeting

Blue Ocean Keywords:
├── Low competition + decent search volume = GOLD
├── Regional/Hindi keywords most sellers ignore
├── Long-tail specific keywords ("pure forest honey 1kg glass jar")
├── Problem-based keywords ("immunity booster for kids winter")
└── These have lowest CPC and highest ROI
```

## C.2 — Dynamic Pricing Intelligence
```
💲 PRICE-AD SYNERGY:

Track how price changes affect ad performance:
├── Price decrease → conversion rate improves → ACoS improves
├── Price increase → conversion drops → ACoS worsens
├── Competitor price drop → our conversion drops
└── System recommends optimal price-bid combination

"If you reduce price by ₹20, your conversion rate historically
 improves 15%, which means you can reduce bid by ₹2 and still
 get same sales volume. Net saving: ₹X/day"
```

## C.3 — Review Impact Tracker
```
⭐ REVIEW-AD PERFORMANCE CORRELATION:

Track: Review count & rating changes → Ad performance impact

"Your product went from 4.1★ to 4.3★ this week.
 Historically, 0.2★ improvement = 8% better conversion rate.
 Recommendation: Increase bid 5% to capitalize on better conversion."

"Your product got 3 negative reviews this week. Rating dropped 4.3→4.1.
 Conversion likely to drop. Recommendation: Reduce bid 10% temporarily."

Alert on: new negative reviews, rating drops, review velocity changes
```

## C.4 — Seasonal Auto-Pilot
```
🗓️ FULL SEASONAL AUTOMATION:

System knows:
├── Indian festival calendar (pre-programmed)
├── Weather/season (winter immunity, summer hydration)
├── Salary cycle (1st-5th peak)
├── Weekend patterns
├── School holiday periods
└── Your product category seasonal trends

Auto-adjusts:
├── Budget multipliers per season
├── Keyword priority shifts (winter→immunity, summer→cooling)
├── Bid aggressiveness level
├── Product promotion priority
└── All changes logged as "Seasonal Auto-Adjust"

2 weeks before major festival:
├── Alert: "Great Indian Festival in 14 days!"
├── Checklist: stock ready? budget increased? keywords updated?
├── Auto-increase budget multiplier gradually
└── Post-festival: auto-normalize
```

## C.5 — Cannibalization Detector
```
🔄 KEYWORD CANNIBALIZATION:

Problem: Same keyword in multiple campaigns = bidding against yourself
         Amazon charges you MORE because YOU are your own competitor!

Detection:
├── Scan all campaigns for duplicate keywords
├── Identify phrase match catching exact match terms
├── Find overlapping targets across campaigns
└── Calculate how much extra we're paying

Fix Recommendation:
├── Add exact keywords as negative in phrase campaigns
├── Consolidate duplicate keywords to one campaign
├── Estimate saving: "Removing cannibalization could save ₹X/month"
└── Label: "Strong Recommend & Approved"
```

## C.6 — ASIN Targeting Intelligence
```
🎯 PRODUCT TARGETING (Target Competitor Product Pages):

Not just keywords — target specific competitor ASINs:
├── Identify competitors with lower ratings than us
├── Target their product pages with our ads
├── "Steal" their customers who are comparison shopping
├── Track which competitor ASINs convert best for us
└── Scale winners, pause losers

Strategy:
├── Target competitors with 3.5-4.0★ (we should be 4.0+)
├── Target competitors with higher price (we're cheaper)
├── Target competitors who are out of stock frequently
└── Avoid targeting market leaders (waste of money)
```

## C.7 — Subscribe & Save Optimizer
```
📦 SUBSCRIBE & SAVE SYNERGY:

Health/Food = HIGH repeat purchase category

Strategy:
├── Track which keywords bring Subscribe & Save customers
├── These customers have LIFETIME VALUE (not just 1 sale)
├── Can accept higher ACoS on first sale (customer returns for months)
├── Identify: "keywords that bring subscribers" vs "one-time buyers"
└── Bid MORE on subscriber-attracting keywords (higher LTV)

"Keyword 'organic honey monthly' has 40% Subscribe rate.
 Lifetime value of subscriber = ₹500/month × 6 months = ₹3000.
 Can accept up to ₹300 first-sale ad cost (10% of LTV).
 Current bid: ₹8. Recommended ceiling: ₹24."
```

## C.8 — Impression Share & Visibility Score
```
👁️ ARE WE VISIBLE ENOUGH?

Impression Share = Our impressions ÷ Total available impressions

Track per keyword:
├── If impression share < 30% → "Not enough visibility"
│   Recommend: Increase bid, we're missing customers
├── If impression share > 80% → "Dominating this keyword" 
│   Recommend: Stable, maybe reduce bid slightly for efficiency
├── If Top-of-Search share < 20% → "Competitors above us"
│   Recommend: Use placement bid adjustment for Top of Search
└── Weekly visibility trend → Are we gaining or losing ground?
```

## C.9 — New Product Launch Autopilot
```
🚀 AUTOMATED LAUNCH SEQUENCE:

When user marks product as "NEW LAUNCH":

Day 1-3: SEEDING PHASE
├── Auto-create Phrase Match campaign with provided keywords
├── Set to EXTRA AGGRESSIVE mode
├── Budget: User-defined launch budget
├── Bid: 1.5x category average
└── Goal: Get first impressions and clicks

Day 4-14: DATA COLLECTION
├── Monitor search term report
├── Identify converting keywords → queue for Exact
├── Identify waste keywords → queue for Negative
├── Daily mini-report specific to this launch
└── Cooling period active (no bid changes)

Day 15-30: OPTIMIZATION START
├── Move winners to Exact Match campaign
├── Apply negatives
├── Begin bid optimization (small daily changes)
├── Shift from EXTRA AGGRESSIVE → AGGRESSIVE
└── Track ACoS, TACoS, organic rank

Day 31+: NORMAL CYCLE
├── Shift to AVERAGE or PROFITABLE based on performance
├── Enter regular daily optimization cycle
├── System manages like all other products
└── Launch autopilot: OFF
```

## C.10 — Smart Notification System
```
📱 CONTEXT-AWARE NOTIFICATIONS:

Not just "ACoS changed" — intelligent notifications:

"Good morning Msir! 🌅
 Yesterday's summary:
 ✅ 3 keywords promoted to STAR status
 💰 ₹847 saved by blocking 12 waste keywords  
 📈 Overall ACoS improved 22%→20.5%
 ⚠️ 1 product stock: only 5 days left — consider restocking
 📋 Today's Excel report is ready on your laptop."

"🚨 ALERT: Competitor 'XYZ Honey' is OUT OF STOCK!
 Opportunity window! Your product 'Pure Forest Honey 500g'
 can capture their traffic. Recommendation: Increase bid 15%
 for next 3 days. Already pre-approved in today's report."

"📊 Weekly Insight: Your honey category TACoS dropped from 
 18% to 14% this month. Flywheel is working! Organic sales
 growing 23% week-over-week. Strategy: gradually reduce
 aggressive bids. System has prepared recommendations."
```

---

# SECTION D: 📊 COMPLETE FEATURE LIST (Final)

## All Features Categorized:

### 🔵 CORE ENGINE (Must-Have)
1. ✅ OAuth2 Authentication (exists)
2. ✅ Data Pull via Ads API v3
3. ✅ Search Term Analysis + IQ Scoring
4. ✅ Bid Optimization (rule-based + learning)
5. ✅ Budget Management (calendar + salary cycle)
6. ✅ Negative Keyword Detection
7. ✅ Keyword Lifecycle Manager
8. ✅ Daily Excel Report (9+ tabs)
9. ✅ Changelog Tracking (full transparency)
10. ✅ True Profit ACoS Calculator

### 🟢 INTELLIGENCE LAYER (Competitive Advantage)
11. ✅ Strategy Learning Database (IQ system)
12. ✅ Competitor Price/Stock Monitor
13. ✅ TACoS Tracker (organic growth)
14. ✅ Organic Rank Flywheel Detection
15. ✅ Listing Health Monitor (stock/buy box/reviews)
16. ✅ Budget Waste Detector (4 levels)
17. ✅ Smart Bid Ceiling Calculator
18. ✅ Cannibalization Detector
19. ✅ Day/Hour Budget Pacing
20. ✅ Impression Share Tracking

### 🟡 AUTOMATION LAYER (User Experience)
21. ✅ 3-Mode Action Engine (Approval/Semi-Auto/Full-Auto)
22. ✅ Excel Approval Workflow (dropdowns, pre-filled)
23. ✅ Auto-Report Email (multi-recipient)
24. ✅ Auto-Open on Mac
25. ✅ One-Click Approval → Execution
26. ✅ Campaign Exclusion (time-based)
27. ✅ Cooling Period Rules
28. ✅ Product Strategy Modes (5 modes + Auto)
29. ✅ Seasonal Auto-Pilot
30. ✅ New Product Launch Autopilot

### 🔴 BLUE OCEAN WEAPONS (Market Domination)
31. ✅ Competitor Keyword Gap Analysis
32. ✅ ASIN Targeting Intelligence
33. ✅ Dynamic Pricing Intelligence
34. ✅ Review Impact Tracker
35. ✅ Subscribe & Save Optimizer
36. ✅ Smart Notifications (context-aware)
37. ✅ Post-Change Response Monitoring (reverse/continue/new)
38. ✅ "Money Saved" Counter

### 📐 CONFIGURATION (All Configurable, No Hardcoding)
39. ✅ All thresholds in JSON config
40. ✅ Festival calendar (editable)
41. ✅ Salary cycle rules (editable)
42. ✅ Dayparting rules (editable)
43. ✅ Product cost data (per product)
44. ✅ Alert recipients (multi-email)
45. ✅ Cooling periods (customizable)
46. ✅ Strategy mode parameters (per product)
47. ✅ Excluded campaigns (time-based)
48. ✅ Bid change limits (daily %)
49. ✅ Budget limits (per mode)

---

### 💎 DESIGN PHILOSOPHY:

```
BACKEND = As POWERFUL as possible
├── 49 features
├── IQ scoring
├── Strategy learning
├── Competitor intelligence
├── Multiple analysis engines
└── Complex decision making

FRONTEND (User Excel) = As SIMPLE as sweet
├── Everything auto-filled
├── User job: LOOK → APPROVE → SUBMIT
├── Maximum 5 minutes daily
├── Color coded (green/red/yellow)
├── Plain language (not technical jargon)
├── "This keyword made ₹500 profit" not "ACoS 12% with CTR 0.8%"
└── Even a child can understand what's happening
```

---

*Blueprint Part 3 FINAL DIAMOND EDITION — Version 1.0 | 11 April 2026*
*49 Features | 5 Strategy Modes | 3 Action Modes | IQ Scoring | Full Transparency*
