# 🖥️ GoAmrita Ads — Web Control Panel Design v8.0
## UI/UX Blueprint (Following Msir's Training Rules)
**Tech:** Python 3.11 + Flask 3.1.3 + SQLAlchemy 2.0.x + HTML/CSS/JS | **Works:** Laptop (localhost) + Server (same code)
**v6.0 Changes:** Universal Import, Template system, Report Import, Organic Competition, HIGH-WEIGHT Tags, Price Segment
**v7.0 Changes:** User Management pages (3-Level Admin, Module Access Control, Performance Score, Bulk Ops universal), User Screen layout (work top, performance tab, bottom bar), Notification event-based config, Audit Trail page
**v8.0 Changes:** Round 9 feature expansion UI — G08 Deal/Coupon launch toggle, A13 sales velocity preset, K07 expanded fields, H01 disabled-by-default toggle, W12 Non-Performing Listing panel, I30 Product Health Score dashboard widget, P17 Profit Cap settings, new feature toggles across pages

---

# DESIGN RULES APPLIED (From Msir's Training):
- ✅ Tab-based structure (Main → Advanced → Settings)
- ✅ Sections with light background variations
- ✅ Helper text beside every option
- ✅ Auto-save on change ("Saved ✓")
- ✅ Defaults pre-set (ready-to-use, ZERO SETUP needed)
- ✅ 3 Modes (Manual / Semi-Auto / Full-Auto)
- ✅ Progress visibility
- ✅ Clean, professional, smooth
- ✅ Top → Bottom = Important → Less important
- ✅ Browser + OS notifications for alerts
- ✅ 3-Level Inheritance: Account → Category → Product
- ✅ Per-Module: Main / Advanced / Settings tabs (v5.0!)
- ✅ Bulk Operations universal: Search + Select All + Bulk Action + One-Click (v8.0!)
- ✅ User screen: Work on TOP, Performance on 2nd/3rd tab, Stats bar at BOTTOM (v8.0!)
- ✅ Module-based auto tabs: Only assigned modules visible per user (v8.0!)
- ✅ Multi-Account + One Login (v5.0!)
- ✅ Alliance/Staff Roles (v5.0!)
- ✅ Easy Signup (must-have only, rest in Settings) (v5.0!)

---

# 🗂️ NAVIGATION STRUCTURE

```
┌─────────────────────────────────────────────────────────┐
│  🏠 GoAmrita Ads Intelligence System                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │
│  Marketplace: [Amazon India ▼] ← Future: Flipkart option │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │
│  Account: [GoAmrita Bhandar ▼] ← Multi-account selector (v5.0!)│
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │
│  [Dashboard] [Products] [Campaigns] [Keywords]            │
│  [Rules] [Reports] [Alerts] [Settings]                    │
│  [Logs] [Learning] [Users] [Training]                     │
└─────────────────────────────────────────────────────────┘
```

## Total: 12 Main Pages (was 10 in v4.0, +Users +Training) — Users page majorly updated v7.0
Each page has its own TABS following your rule:
- **Main Tab** = Frequently used
- **Advanced Tab** = Less frequent but important
- **Settings Tab** = Rarely changed

---

# PAGE 1: 🏠 DASHBOARD (Home)
**Purpose:** Strategy Impact Center — NOT Amazon metrics copy!
**Principle:** Show ONLY what Amazon doesn't — our strategy effects, actions needed, savings

## Main Tab: "Strategy Impact"
```
┌─────────────────────────────────────────────────────────────┐
│  🎯 TODAY'S STRATEGY IMPACT                                  │
│  ┌──────────┬──────────┬──────────┬──────────┐              │
│  │ Money    │ Waste    │ Bids     │ Actions  │              │
│  │ SAVED    │ BLOCKED  │ Optimized│ Taken    │              │
│  │ ₹847     │ ₹1,230   │ 23 ↑/15↓│ 38 total │              │
│  │ ↑12% vs  │ 8 keywords│ via AI  │ 35 auto  │              │
│  │ yesterday │ stopped  │ engine  │ 3 manual │              │
│  └──────────┴──────────┴──────────┴──────────┘              │
│                                                              │
│  🟢 System Status: Running | Last Run: Today 6:15 AM        │
│  🤖 AI Layers Active: L1 ✅ L2 ✅ L3 ✅                      │
│                                                              │
│  ━━━━ SECTION: Needs Your Attention ━━━━━━━━━━━━━━━━━━━━    │
│  ⚡ 3 items need manual review:                              │
│  1. 🔴 Amla Juice — ACoS 45%, AI says reduce 20% bid        │
│     → [Approve] [Reject] [View Details]                      │
│  2. 🟡 New keyword "organic honey" — 12 clicks, 0 sales     │
│     → AI watching, will act in 2 days if no sale             │
│  3. 🟢 Ashwagandha campaign — AI scaled +15%, working!       │
│     → FYI only, no action needed                             │
│                                                              │
│  ━━━━ SECTION: Strategy Effect (Last 7 Days) ━━━━━━━━━━━    │
│  ├── Profit increased: ₹4,200 (+18%)                        │
│  ├── Waste reduced: ₹8,500 blocked this week                │
│  ├── Flywheel status: 3 products improving organic           │
│  ├── Best decision: Honey bid +20% → ACoS dropped 5%        │
│  │   Tags: [L1:CORRECT] [L2:CORRECT] [PERMANENT RULE]       │
│  └── Worst decision: Amla price +10% → profit dropped        │
│      Tags: [L1:WRONG] [LEARNING: trying +5% next]           │
│                                                              │
│  ━━━━ SECTION: Permanent Rules Learned ━━━━━━━━━━━━━━━━━    │
│  This month: 5 new permanent rules discovered                │
│  All-time: 23 proven rules auto-applied daily                │
│  [View All Rules →]                                          │
│                                                              │
│  [📥 Download Today's Report] [▶️ Run Optimization Now]      │
│                                                              │
│  ━━━━ SECTION: Product Health Overview (v8.0 — I30) ━━━━━━  │
│  🏥 Products by Health Score:                                 │
│  🟢 Healthy (80+): 187 products | 🟡 Warning (50-79): 85    │
│  🔴 Critical (<50): 28 products                              │
│  Top Issues: 12 listings need images, 8 overstock alerts      │
│  [View All Product Health →]                                 │
│                                                              │
│  ━━━━ SECTION: Non-Performing Listings (v8.0 — W12) ━━━━━━  │
│  ⚠️ 5 products with zero orders past threshold:              │
│  1. Neem Soap 100g — 18 days | Diagnosis: Price too high     │
│  2. Turmeric Mix — 15 days | Diagnosis: Low visibility       │
│  [View All Non-Performing →] [Run Bulk Diagnosis →]          │
└─────────────────────────────────────────────────────────────┘
```

## Advanced Tab: "AI Layer Performance"
- Layer 1 accuracy: 72% correct | Layer 2: 81% | Layer 3: 76%
- Combined (all 3): 91% accuracy
- Decision breakdown by tag type
- Permanent rules list with IQ scores
- Cross-learn suggestions pending
- **4-Level Learning Status (v5.0 NEW!):**
  - Software Level IQ: 78 (based on 12,340 data points)
  - Category Level: Healthcare 82, Honey 75, Supplements 71
  - Product Level: Top 10 products with IQ scores
  - Cross-Module Learning: 23 active weight connections, 5 recently promoted

## Settings Tab: "Dashboard Settings"
- Choose which sections show on dashboard
- Set refresh interval
- Notification preferences (Browser / OS / Both / None)

---

# PAGE 2: 📦 PRODUCTS
**Purpose:** Per-product settings & performance

## Main Tab: "Product List"
```
┌─────────────────────────────────────────────────────────────┐
│  🔍 Search: [____________] Filter: [All Categories ▼]        │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Product          │ Strategy │ ACoS  │ True │ Status  │   │
│  │──────────────────│──────────│───────│──────│─────────│   │
│  │ Pure Honey 1kg   │ 🟢 Profit│ 8.2%  │12.1% │ Active  │   │
│  │ Ashwagandha 60ct │ 🟡 Avg   │ 18.5% │24.3% │ Active  │   │
│  │ Amla Juice 500ml │ 🔴 Aggr  │ 45.2% │68.1% │ ⚠️ Fix  │   │
│  │ Chyawanprash 1kg │ 🤖 Auto  │ 15.1% │21.0% │ Active  │   │
│  │ NEW: Tulsi Drops  │ 🔴 XAggr │ —     │—     │ Launch  │   │
│  └──────────────────────────────────────────────────────┘   │
│  Click any product → opens product detail page               │
└─────────────────────────────────────────────────────────────┘
```

## Product Detail Page (Click on product):
```
┌─────────────────────────────────────────────────────────────┐
│  📦 Pure Honey 1kg — ASIN: B0XXXXXX                         │
│                                                              │
│  ━━━━ SECTION: Strategy Mode ━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Current: [🟢 Profitable Only ▼]                             │
│  ℹ️ Only proven keywords, ACoS target < 15%                  │
│  Options: Extra Aggressive | Aggressive | Average |          │
│           Profitable | Survival | 🤖 Automatic               │
│                                                              │
│  ━━━━ SECTION: Campaign Funnel ━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Funnel Type: [Msir Method: Suggestion→Phrase→Exact ▼]       │
│  ℹ️ Keywords from Amazon auto-suggestion, then optimize       │
│  Other: Auto→Phrase→Exact | Direct Exact Only                │
│                                                              │
│  ━━━━ SECTION: Keyword Source Modes ━━━━━━━━━━━━━━━━━━━━   │
│  A. 🤖 Amazon API Smart Campaign          [✅ ENABLED]      │
│     ℹ️ AI uses Search Term Report + API keyword recs          │
│  B. 📋 Google Sheet / CSV Keywords         [✅ ENABLED]     │
│     ℹ️ Your manually researched keywords                      │
│  C. 🏥 Product Benefit Targeting            [⬜ DISABLED]    │
│     ℹ️ AI targets related problems, brands, ingredients       │
│  Test Mode: [🔬 A/B Test All Modes ▼]                       │
│                                                              │
│  ━━━━ SECTION: Cost & Profit ━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Category: [Healthcare ▼] (optional — if set, inherits)      │
│  ℹ️ Empty fields inherit from Category → Account defaults     │
│                                                              │
│  Sale Price:     [₹ 599    ]                                 │
│  COGS:           [₹ 220    ] ℹ️ Raw material + making         │
│  Referral Fee %: [         ] ℹ️ Empty = Category 12% → Acc   │
│  Shipping Fee:   [₹ 85     ] ℹ️ Current delivery charge       │
│  Packaging:      [         ] ℹ️ Empty = Category ₹25 → Acc   │
│  GST %:          [         ] ℹ️ Empty = Category 5% → Acc    │
│  Returns %:      [         ] ℹ️ Empty = Category → Acc 15%   │
│  ────────────────────────────                                │
│  TRUE PROFIT:    ₹ 165.12  (auto-calculated)  Saved ✓       │
│  Break-even ACoS: 27.6%    (auto-calculated)                 │
│  Target ACoS:    19.3%     (30% profit margin on ads)        │
│  Max Bid Ceiling: ₹ 13.21  (at 8% conversion rate)          │
│                                                              │
│  ━━━━ SECTION: Profit Cap (v8.0 NEW! — P17) ━━━━━━━━━━━━━   │
│  Profit % Cap: [OFF ▼]                                       │
│  Max Ad Spend % of True Profit: [__]%                        │
│  ℹ️ "Spend max X% of true profit on ads." Overrides account  │
│  ℹ️ Different from P14 (payout-based). This is PROFIT-based  │
│                                                              │
│  ━━━━ SECTION: Launch Autopilot (v8.0 ENHANCED — G08) ━━━━━ │
│  Auto Deal/Coupon on Launch: [OFF ▼]                         │
│  Deal Type: [Lightning Deal ▼] | [Coupon ▼]                 │
│  Discount %: [__]%  ℹ️ For visibility boost during launch     │
│  Duration: [7 days ▼]                                        │
│                                                              │
│  ━━━━ SECTION: Exclusion ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Exclude from optimization: [OFF ▼]                          │
│  If ON → Exclude for: [__] days                              │
│  Reason: [________________]                                  │
│                                                              │
│  ━━━━ SECTION: Sole Seller Check ━━━━━━━━━━━━━━━━━━━━━━━   │
│  Sole seller for this product? [NO ▼]                        │
│  ℹ️ If YES → system will reduce/skip ads (you're only seller)│
│                                                              │
│  ━━━━ SECTION: Performance (read-only) ━━━━━━━━━━━━━━━━━━   │
│  7-day: Spend ₹X | Sales ₹Y | ACoS Z% | Orders N           │
│  Flywheel Phase: 🟢 MOMENTUM (organic growing)               │
│  TACoS trend: 18% → 14% (↓ improving)                       │
│  Strategy Mode History: Aggressive→Average→Profitable         │
│                                                              │
│  ━━━━ SECTION: Price-Profit Tracker ━━━━━━━━━━━━━━━━━━━━   │
│  ┌────────────┬────────────┬────────────┬──────────┐        │
│  │ Price Point │ Profit/Day │ Units/Day  │ Period   │        │
│  │ ₹599       │ ₹495       │ 3.0        │ 30 days  │        │
│  │ ₹659 (+10%)│ ₹450       │ 2.0        │ 5 days   │        │
│  │ ₹629 (+5%) │ ₹585       │ 3.0        │ 7 days ✅│        │
│  └────────────┴────────────┴────────────┴──────────┘        │
│  ℹ️ Best price point: ₹629 (highest profit/day)              │
│                                                              │
│  ━━━━ SECTION: Review Health (v3.0 NEW!) ━━━━━━━━━━━━━━━   │
│  Source: Customer Feedback API v2024-06-01 (weekly refresh)  │
│  Average Rating: ⭐ 4.2/5                                    │
│  Distribution: 5★ 65% | 4★ 18% | 3★ 8% | 2★ 5% | 1★ 4%   │
│  Negative Ratio: 9% (healthy)                                │
│  Themes: "good quality", "fast delivery"                     │
│  Review Brake: 🟢 Not triggered (rating > 3.5)               │
│  [View Review Trend →]                                       │
│                                                              │
│  ━━━━ SECTION: BSR Tracking (v3.0 NEW!) ━━━━━━━━━━━━━━━━   │
│  Data Source: [Manual Sheet ✅ / SP-API Fallback]             │
│  Current BSR: #245 in Health & Personal Care                 │
│  Trend: ↗️ Improving (was #380 last week)                    │
│  Impact: Organic sales growing → can reduce ad spend         │
│  [Upload BSR Sheet] [View BSR History →]                     │
│                                                              │
│  ━━━━ SECTION: Product Health Score (v8.0 NEW! — I30) ━━━━━ │
│  🏥 Health Score: 78/100 🟢                                   │
│  Components:                                                 │
│    Sales Velocity: 85 | Profitability: 72 | Reviews: 81     │
│    Listing Quality: 65 | Ad Efficiency: 88 | Stock: 70      │
│  ℹ️ Single score combining ALL product health factors         │
│  [View Score Breakdown →]                                    │
│                                                              │
│  ━━━━ SECTION: Listing Health Score (v8.0 NEW! — G14) ━━━━━ │
│  📝 Listing Score: 65/100 🟡                                  │
│  Images: 5/7 ⚠️ | Keywords: 82% ✅ | A+: ❌ Missing         │
│  Description: ✅ | Bullet Points: 4/5 ⚠️ | Compliance: ✅   │
│  ℹ️ Quick listing quality check across all fields             │
│  [View Listing Audit →]                                      │
│                                                              │
│  ━━━━ SECTION: Non-Performing Alert (v8.0 NEW! — W12) ━━━━━ │
│  Days without order: 12                                      │
│  Auto-Diagnose: [ON ▼]                                       │
│  Threshold (days): [User: 14 ▼] | [AI Suggested: 10]        │
│  Diagnosis: Buy Box ✅ | Stock ✅ | Listing 🟡 | Price ⚠️    │
│  ℹ️ Auto-triggers relevant features when threshold hit        │
│  [Run Diagnosis Now →]                                       │
└─────────────────────────────────────────────────────────────┘
```

## Advanced Tab: "Bulk Settings"
- Upload CSV with costs for all products at once
- Bulk change strategy mode
- Bulk exclude/include
- **Upload BSR Sheet** (Format: ASIN | BSR | DATE) ← NEW v3.0
- **Category-Level Template Creator:**
```
┌─────────────────────────────────────────────────────────┐
│  ━━━━ SECTION: Category Templates ━━━━━━━━━━━━━━━━━━   │
│                                                          │
│  [+ Add New Category Template]                           │
│                                                          │
│  📂 Healthcare (12 products assigned)                    │
│  ├── Referral %: [12]  Shipping: [₹65]  Packaging: [₹25]│
│  ├── GST %: [5]  Returns %: [15]                         │
│  └── [Edit] [Assign Products]                            │
│                                                          │
│  📂 Honey & Sweeteners (5 products assigned)             │
│  ├── Referral %: [12]  Shipping: [₹85]  Returns %: [8]  │
│  └── [Edit] [Assign Products]                            │
│                                                          │
│  ℹ️ Category is OPTIONAL. Unassigned products use         │
│     Account-level defaults directly.                      │
│  ℹ️ Inheritance: Account → Category → Product             │
└─────────────────────────────────────────────────────────┘
```

## Settings Tab: "Default Product Settings"
```
┌─────────────────────────────────────────────────────────┐
│  ━━━━ SECTION: Defaults for New Products ━━━━━━━━━━━━   │
│                                                          │
│  Default Strategy Mode:    [🤖 Automatic ▼]              │
│  Default Campaign Funnel:  [Msir Method ▼]               │
│  Default Target ACoS:     [20]%                          │
│  Default Max Daily Budget: [₹200]                        │
│  Default Cooling Period:   [Budget-First ▼]              │
│  Auto-Campaign on New Listing: [ON ▼]                    │
│  Launch Mode Duration:     [30] days                     │
│  Launch Strategy:          [Aggressive ▼]                │
│  Category Template:        [None — use Account ▼]        │
│  Sole Seller Auto-Check:   [ON ▼]                        │
│  Exclusion Default:        [OFF ▼]                       │
│                                                          │
│  ━━━━ SECTION: Keyword Mode Defaults ━━━━━━━━━━━━━━━   │
│  Mode A (API Smart):        [ON ▼] (default)             │
│  Mode B (Sheet/CSV):        [ON ▼] (default)             │
│  Mode C (Benefit Targeting): [OFF ▼] (advanced)          │
│                                                          │
│  ℹ️ All settings here = "Set once, forget forever"        │
│     Each product can override individually                │
│  All changes auto-saved ✓                                │
└─────────────────────────────────────────────────────────┘
```

---

# PAGE 3: 🎯 CAMPAIGNS
**Purpose:** Campaign overview & management

## Main Tab: "Active Campaigns"
- List all campaigns with status, spend, ACoS, True ACoS
- Quick actions: Pause, Resume, Change budget
- Filter: by product, by strategy, by status, by keyword mode
- Color coded: 🟢 profitable 🟡 warning 🔴 losing
- **Keyword Mode badge:** [A] [B] [C] per campaign

## Advanced Tab: "Campaign Creator"
- Create new campaign with smart defaults
- Choose funnel type
- Choose keyword source mode (A / B / C / All)
- AI-suggested structure based on product
- Campaign Assignment: **Dropdown select** (existing or "Create New")

## Settings Tab: "Campaign Rules"
```
┌─────────────────────────────────────────────────────────┐
│  ━━━━ SECTION: Cooling Period ━━━━━━━━━━━━━━━━━━━━━━   │
│  Cooling Mode: [Budget-First ▼] (Days OR Budget)         │
│                                                          │
│  Low Price Products (<₹500):                             │
│    Days: [10]  Budget: [₹500]                            │
│    ℹ️ Whichever exceeds first ends cooling                │
│                                                          │
│  High Price Products (₹500+):                            │
│    Days: [12]  Budget: [100]% of sale price              │
│    ℹ️ ₹599 product → cooling ends at ₹599 spend or 12d   │
│                                                          │
│  Price Threshold: [₹500] ℹ️ Below=Low, Above=High        │
│                                                          │
│  ━━━━ SECTION: Intelligent Auto-Pause Rules ━━━━━━━━━   │
│  ℹ️ NOT Amazon's basic pause — our smart rules             │
│                                                          │
│  Zero Sales Pause:                                       │
│    After [__] days AND [₹__] spend with 0 sales → Pause  │
│  Bleeding Pause:                                         │
│    ACoS > [80]% for [5] days → Reduce → then Pause       │
│  Stock-Out Pause:                                        │
│    Stock < [5] units → Auto-pause ads                    │
│  Seasonal Pause:                                         │
│    Define off-season dates per product                    │
│  Auto Re-Activate: [ON ▼]                                │
│    ℹ️ When condition improves → auto resume                │
│                                                          │
│  ━━━━ SECTION: Budget Pacing (Advanced Only) ━━━━━━━━   │
│  ℹ️ Only custom/advanced pacing — not Amazon's basic       │
│                                                          │
│  Salary Cycle Sync: [ON ▼]                               │
│    1st-5th: [×1.3]  6th-24th: [×1.0]  25th-30th: [×0.8]│
│  Festival Multiplier: [ON ▼] [Edit Calendar →]           │
│  Profit-Based Pacing: [ON ▼]                             │
│    ℹ️ More profit = more budget allowed                    │
│  Cashflow Guardian: [ON ▼]                               │
│    ℹ️ Monthly budget smart paced (not exhaust in 10 days)  │
│  Payout Sync: [OFF ▼]                                    │
│    Max spend: [15]% of weekly Amazon payout               │
│                                                          │
│  All changes auto-saved ✓                                │
└─────────────────────────────────────────────────────────┘
```

---

# PAGE 4: 🔑 KEYWORDS
**Purpose:** Keyword management & lifecycle

## Main Tab: "Keyword Overview"
- All keywords with lifecycle status (Star ⭐ / Proven / Testing / New / Declining)
- Quick filter: Stars only, Waste only, New only
- Bulk actions: Negate, Pause, Move to Exact
- **Source badge:** [A:API] [B:Sheet] [C:Benefit] per keyword

## Advanced Tab: "Keyword Sources"
```
┌─────────────────────────────────────────────────────────┐
│  ━━━━ SECTION: Google Sheet Keyword Import ━━━━━━━━━   │
│                                                          │
│  Sheet URL: [paste Google Sheet URL______________]       │
│  Tab Name:  [Keywords_______]                            │
│  Keyword Column:    [A / keyword ▼]                      │
│  Match Type Column: [B / match_type ▼]                   │
│    ℹ️ Values: "exact", "phrase", "broad"                  │
│    ℹ️ If empty → Smart Auto:                              │
│       1-2 words → Phrase match                           │
│       3+ words → Exact match                             │
│  Product/ASIN Column: [C / asin ▼]                       │
│  Campaign Column: [D / campaign ▼]                       │
│    ℹ️ Dropdown: select existing / "Create New" / empty    │
│    ℹ️ If empty → auto-assign to product's active campaign │
│  Bid Column: [E / bid ▼] (optional)                      │
│    ℹ️ If empty → AI calculates optimal bid                │
│                                                          │
│  Auto-Fetch: [ON ▼]                                      │
│  Fetch Interval: [30] minutes                            │
│  [🔄 Test Connection] [📥 Fetch Now]                     │
│  Last Fetch: 2 hrs ago | New Keywords Found: 5           │
│                                                          │
│  ━━━━ SECTION: CSV Upload ━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Same column format as Google Sheet                      │
│  [📁 Upload CSV File]                                    │
│                                                          │
│  ━━━━ SECTION: Webhook Endpoint ━━━━━━━━━━━━━━━━━━━━   │
│  URL: http://localhost:5000/api/keywords/add             │
│  ℹ️ POST keywords from any external tool (same format)    │
│  [📋 Copy URL] [View Docs]                               │
│                                                          │
│  ━━━━ SECTION: Amazon API Keywords ━━━━━━━━━━━━━━━━━   │
│  Search Term Report: [Auto-harvest ON ▼]                 │
│  API Keyword Recommendations: [ON ▼]                     │
│  ℹ️ Priority: Search Term Report > Auto-Suggestion >      │
│     API Recs > AI Mining > Sheet Import > CSV Upload      │
│                                                          │
│  ━━━━ SECTION: AI Keywords (Mode C) ━━━━━━━━━━━━━━━━   │
│  Symptom/Ingredient Mining: [ON per enabled products ▼]  │
│  Problem→Solution Keywords: [ON ▼]                       │
│  Dietary Cross-Pollination: [OFF ▼]                      │
│  Intent Classification: [ON ▼]                           │
│    Buying / Research / Problem intent tagging             │
└─────────────────────────────────────────────────────────┘
```

## Keyword Opportunities Tab (v3.0 NEW! — M04 Keyword Gap):
```
┌─────────────────────────────────────────────────────────────┐
│  ━━━━ KEYWORD OPPORTUNITIES (M04) ━━━━━━━━━━━━━━━━━━━━━━   │
│  ⚠️ NO auto-add to campaigns — Approval required for ALL     │
│                                                              │
│  [Tab: For Ads] [Tab: Listing Optimization]                  │
│  [Tab: Category Keywords] [Tab: New Product Opportunities]   │
│                                                              │
│  ━━━━ Tab 1: For Ads (Approach A + C + D) ━━━━━━━━━━━━━━   │
│  Keywords from Search Term Analysis + Amazon Suggestions +   │
│  Brand Analytics that you're NOT targeting                   │
│  ┌──────────────┬──────────┬──────────┬──────────┐          │
│  │ Keyword      │ Source   │ Est Vol  │ Action   │          │
│  │ organic honey│ A:Search │ High     │[Approve] │          │
│  │ pure shilajit│ C:Amazon │ Medium   │[Approve] │          │
│  │ immunity tab │ D:Brand  │ High     │[Approve] │          │
│  └──────────────┴──────────┴──────────┴──────────┘          │
│  [Approve Selected] [Reject Selected]                        │
│  ℹ️ Approved keywords added to campaigns automatically        │
│                                                              │
│  ━━━━ Tab 2: Listing Optimization (Approach A reverse) ━━   │
│  Keywords with high impressions but low clicks on YOUR ads   │
│  → Suggests: "Optimize your listing for these keywords"      │
│  ┌──────────────┬──────────┬──────────────────┐             │
│  │ Keyword      │ Imp/Click│ Suggestion       │             │
│  │ ayurvedic tab│ 500/3    │ Add to title     │             │
│  │ herbal honey │ 300/2    │ Add to bullets   │             │
│  └──────────────┴──────────┴──────────────────┘             │
│                                                              │
│  ━━━━ Tab 3: Category Keywords (Approach B) ━━━━━━━━━━━━   │
│  ⚠️ WARNING: Wide category keywords — review carefully!       │
│  ❌ NOT auto-used for ads — approval required                 │
│  ┌──────────────┬──────────┬──────────┬──────────┐          │
│  │ Keyword      │ Category │ Relevance│ Action   │          │
│  │ health suppl │ Health   │ Medium   │[Approve] │          │
│  └──────────────┴──────────┴──────────┴──────────┘          │
│  [Approve for Ads] [Push to Sheet] [Dismiss]                 │
│                                                              │
│  ━━━━ Tab 4: New Product Opportunities (Approach B) ━━━━   │
│  Category keywords that suggest new product opportunities    │
│  Auto-pushed to configured Google Sheet                      │
│  Status: Last push: 2 days ago | 12 opportunities found     │
│  [Push Now] [View Sheet →]                                   │
│                                                              │
│  ━━━━ Category Keywords Google Sheet Config ━━━━━━━━━━━━   │
│  Google Sheet ID:  [_________________________]               │
│  Tab Name:         [Category Keywords]                       │
│  Column Mapping:                                             │
│    Keyword: [A]  Category: [B]  Volume: [C]  Date: [D]      │
│  Auto-Push Frequency: [Weekly ▼]                             │
│  Push Enabled: [OFF ▼] ← safety default                     │
│  [🔄 Test Connection] [📥 Push Now]                          │
└─────────────────────────────────────────────────────────────┘
```

## Settings Tab: "Keyword Rules"
- Cooling period for new keywords (days OR budget)
- Waste detection threshold (profit-based, not fixed clicks)
- Negative keyword auto-rules
- Slowly reduce vs hard block preference
- Smart Match Type: auto by word count (1-2=phrase, 3+=exact)

---

# PAGE 5: ⚙️ RULES (Optimization Engine)
**Purpose:** All optimization rules in one place

## Main Tab: "Bid Rules"
```
┌─────────────────────────────────────────────────────────────┐
│  ━━━━ SECTION: Bid Adjustment Rules ━━━━━━━━━━━━━━━━━━━━   │
│                                                              │
│  ℹ️ All percentages calculated dynamically based on           │
│     profit, bid amount, and product price                    │
│                                                              │
│  When ACoS < 10% (Star ⭐):                                  │
│  ┌─────────────┬─────────────┬──────────────┐               │
│  │ YOUR VALUE  │ AI RECOMMENDS│ LAST EFFECT  │               │
│  │             │              │              │               │
│  │First: [+20]%│ 💡 +25%      │ ↗️ +18% worked│              │
│  │      [Accept ✓]│          │ [View History]│               │
│  │Daily: [+4 ]%│ 💡 +5%       │ +3% → good   │               │
│  │      [Accept ✓]│          │ [View History]│               │
│  └─────────────┴─────────────┴──────────────┘               │
│  ℹ️ Profitable keyword, scale it up                           │
│  📊 Last adaptation: 3 days ago, +15%→ACoS dropped 2.1%      │
│                                                              │
│  When ACoS 10-15% (Good):                                    │
│  ┌─────────────┬─────────────┬──────────────┐               │
│  │First: [+15]%│ 💡 +12%      │ ↗️ worked     │               │
│  │Daily: [+3 ]%│ 💡 +3%       │ stable       │               │
│  └─────────────┴─────────────┴──────────────┘               │
│                                                              │
│  When ACoS 15-25% (Target):                                  │
│    Action: [No Change ▼]                                     │
│    ℹ️ Sweet spot, maintain                                    │
│                                                              │
│  When ACoS 25-35% (Warning):                                │
│  ┌─────────────┬─────────────┬──────────────┐               │
│  │First: [-15]%│ 💡 -12%      │ ↘️ helped     │               │
│  │Daily: [-3 ]%│ 💡 -4%       │ slow improve │               │
│  └─────────────┴─────────────┴──────────────┘               │
│                                                              │
│  When ACoS > 35% (Bleeding):                                │
│  ┌─────────────┬─────────────┬──────────────┐               │
│  │First: [-25]%│ 💡 -20%      │ ↘️ improving  │               │
│  │Daily: [-6 ]%│ 💡 -5%       │ needs more   │               │
│  └─────────────┴─────────────┴──────────────┘               │
│  ℹ️ Slowly reduce, don't hard block                           │
│                                                              │
│  ━━━━ SECTION: AI Rule Update Mode ━━━━━━━━━━━━━━━━━━━━━   │
│  Update Mode: [Semi-Auto ▼]                                  │
│  ├── Manual: AI shows suggestions, user manually accept      │
│  ├── Semi-Auto: Strong+Weak auto-apply,                      │
│  │   ask ONLY uncertain/risky/critical                       │
│  └── Full-Auto: AI auto-updates periodically                 │
│                                                              │
│  Approval Type: [Bulk Review ▼]                              │
│  ├── One-by-One: each suggestion separate                    │
│  ├── Bulk Review: all suggestions one screen                 │
│  └── Auto-Apply: IQ>85 auto-apply                            │
│                                                              │
│  All changes auto-saved ✓                                    │
└─────────────────────────────────────────────────────────────┘
```

## Advanced Tab: "Budget & Calendar Rules"
- Salary cycle multipliers (1st-5th: ×1.3, etc.)
- Festival calendar with budget multipliers
- Dayparting rules (initial — AI will learn over time)
- Daily cashflow guardian (monthly budget pacing)
- Cash-flow sync (% of Amazon payout option)

## Settings Tab: "Engine Settings"
- Confidence threshold (minimum data before acting)
- Cooling periods (keyword/campaign/bid change — Days OR Budget)
- Slow-reduce vs hard-block toggle
- A/B test duration
- What-If simulator toggle (enable/disable)

---

# PAGE 6: 📊 REPORTS
**Purpose:** View & download reports

## Main Tab: "Daily Reports"
- Calendar view — click any date → download that day's Excel
- Today's report: Preview key metrics
- [Download] [Email Now] [Open in Excel] buttons

## Advanced Tab: "Custom Reports"
- Date range selector → generate custom report
- Compare two periods
- Export format: Excel / CSV

## Settings Tab: "Report Settings"
- Auto-email time (e.g., 6:00 AM IST)
- Email recipients (multi-email)
- Auto-open on Mac toggle + time
- Report language preference
- Which tabs to include/exclude

---

# PAGE 7: 🔔 ALERTS — UPDATED v3.0
**Purpose:** Alert configuration & history

## Main Tab: "Active Alerts"
- List of all recent alerts (P1 🔴 / P2 🟡 / P3 🔵)
- Mark as read / dismiss
- Quick action from alert

## Advanced Tab: "Alert Rules"
```
┌─────────────────────────────────────────────────────────┐
│  ━━━━ SECTION: Alert Actions ━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                          │
│  P1 (Critical): Budget spike, stock-out, Buy Box lost    │
│    Action: [Auto-handle ▼]                               │
│    ℹ️ System takes action automatically                   │
│                                                          │
│  P2 (Important): ACoS spike, competitor move, review drop│
│    Action: [Notify + Auto ▼]                             │
│                                                          │
│  P3 (Insight): Trends, benchmarks, suggestions           │
│    Action: [Notify only ▼]                               │
│                                                          │
│  ━━━━ SECTION: Stock Low Actions (BOTH active) ━━━━━━   │
│                                                          │
│  Option A: Ads Side                                      │
│    [✅ Auto Reduce to Profitable Mode]                    │
│    ℹ️ Switch ads strategy to save money                   │
│    Trigger: stock < [10] units OR [7] days left           │
│                                                          │
│  Option B: Seller Side (SP-API)                          │
│    [✅ Auto Update Price on Seller Central]               │
│    ℹ️ Stock low → increase price (premium for scarcity)   │
│    Low Stock Price Increase: [+5]% ← learned optimal     │
│    Overstock Price Decrease: [-15]%                       │
│    Min Price Floor: [₹___] (never below)                  │
│    Max Price Ceiling: [₹___] (never above)                │
│                                                          │
│  Active Mode: [✅ Both A + B ▼]                           │
│    ℹ️ Reduce ads + adjust price simultaneously             │
│                                                          │
│  ━━━━ SECTION: Buy Box Recovery (v3.0 NEW!) ━━━━━━━━━   │
│                                                          │
│  Buy Box Lost Actions:                                   │
│    [✅ Reduce Ad Bids]                                    │
│    Bid Reduction %: [50]% ← configurable                 │
│                                                          │
│    [✅ Auto Price Decrease to Recover]                    │
│    Decrease %: [5]% per interval ← configurable          │
│    Interval: [30] minutes ← configurable                 │
│    Minimum Price Floor: [₹___] (cost + 10%)              │
│    Alert on every decrease: [ON ▼]                       │
│    Auto Price Decrease Enabled: [OFF ▼] ← safety default │
│    ℹ️ Decreases price 5% every 30min, rechecks Buy Box    │
│    ℹ️ Stops when Buy Box regained OR min price reached     │
│                                                          │
│    Real-time Monitoring: [ON ▼]                          │
│    ℹ️ Via SP-API Notifications v1 (ANY_OFFER_CHANGED)      │
│                                                          │
│  ━━━━ SECTION: Review Brakes (v3.0 UPDATED!) ━━━━━━━━   │
│                                                          │
│  P09 Review Score Brake:                                 │
│    Source: Customer Feedback API v2024-06-01              │
│    Trigger: avg rating < [3.5]★                          │
│    Action: Reduce bids [30]%                             │
│    Mode: [✅ Fully Automatic]                             │
│                                                          │
│  P10 Negative Review Brake:                              │
│    Source: Customer Feedback API v2024-06-01              │
│    Mode: [✅ 100% Automatic — NO manual]                  │
│    Conditions (checked automatically):                   │
│    ├── Negative ratio > 30% → 60% reduction              │
│    ├── 1★ spike detected → 40% reduction                 │
│    ├── Critical negative themes → 50% reduction          │
│    └── Negative ratio > 20% → 25% reduction              │
│    Gemini 2.5 Flash refinement: [ON if available ▼]      │
│    ℹ️ Adjusts ±10% based on theme severity                │
│                                                          │
│  ━━━━ SECTION: Competitor Actions ━━━━━━━━━━━━━━━━━━━   │
│  Competitor out of stock: [Auto increase bid ▼]          │
│  Competitor price drop: [Notify + review ▼]              │
│  Competitor running deal: [Save budget today ▼]          │
│  New competitor detected (M11): [Alert ▼]                │
│  ℹ️ Detects new competitor entering your keywords/category│
│                                                          │
│  ━━━━ SECTION: Sales Velocity Alert (v8.0 — A13) ━━━━━  │
│  Sales Drop Alert: [ON ▼]                                │
│  Threshold: Sales drop > [50]% in [24] hours → P1 Alert │
│  Auto-Action: [Diagnose + Alert ▼]                       │
│  ℹ️ Preset alert for sudden sales drops                   │
│  ℹ️ Uses A13 4-Type Alert Engine (% Change type)          │
│                                                          │
│  ━━━━ SECTION: Anomaly Detection (v8.0 — I31) ━━━━━━━━  │
│  3-Level Anomaly Detection: [ON ▼]                       │
│    Product Level: [✅] Campaign Level: [✅] Account: [✅] │
│  Detects: CPC spikes, click variance, order anomalies    │
│  Sensitivity: [Medium ▼] (Low/Medium/High)               │
│  ℹ️ Broader than P01/P02. Catches patterns across levels  │
└─────────────────────────────────────────────────────────┘
```

## Settings Tab: "Notification Settings"
```
┌─────────────────────────────────────────────────────────┐
│  ━━━━ SECTION: Notification Channels ━━━━━━━━━━━━━━━━   │
│                                                          │
│  Email Addresses (multi): ← v5.0 UPDATED!               │
│    Primary: [msir@email.com]                             │
│    Additional: [+Add Email] [email2] [email3]            │
│    Per-function: [Ads→email1 ▼] [Stock→email2 ▼]        │
│    ℹ️ If per-function blank → account primary auto-fills   │
│    Per alert type: P1→instant, P2→hourly, P3→daily       │
│                                                          │
│  Browser Notifications: [ON ▼]                           │
│    ℹ️ Popup when web panel open or in background           │
│                                                          │
│  OS Desktop Notifications: [ON ▼]                        │
│    ℹ️ System notification even when browser closed         │
│                                                          │
│  WhatsApp: [Phase 4 — LAST PHASE] [OFF ▼] ← v5.0!      │
│    Numbers (multi): [+Add Number]                        │
│                                                          │
│  ━━━━ SECTION: Advanced Notification (v5.0 NEW!) ━━━━   │
│                                                          │
│  Custom Voice/Sound: [ON ▼]                              │
│    P1 (Critical): [🔔 Urgent Alarm ▼]                    │
│    P2 (Important): [🔔 Attention Bell ▼]                 │
│    P3 (Insight):   [🔔 Soft Chime ▼]                    │
│  Voice Level: [Medium ▼] (Low/Medium/High/Max)           │
│                                                          │
│  Critical Alert Behavior:                                │
│    Define Critical: [Buy Box Lost ✅] [Stock Zero ✅]     │
│                     [Budget Spike ✅] [Rating <3.0 ✅]    │
│    Repeat Until Acknowledged: [ON ▼]                     │
│    Repeat Interval: [2] minutes                          │
│                                                          │
│  ━━━━ SECTION: Escalation Chain (v5.0 NEW!) ━━━━━━━━━   │
│                                                          │
│  If Primary Not Acknowledged:                            │
│    Timeout: [15] minutes → escalate to secondary         │
│    Secondary Staff: [Enable ▼]                           │
│    Secondary Contact: [staff@email.com ▼] per role       │
│    ℹ️ Configure staff roles in Users → Staff page          │
│                                                          │
│  No-Response Timeout: [4] hours                          │
│    → then auto-apply strong recommendations              │
│                                                          │
│  Alert Frequency: [Instant for P1, Hourly digest others] │
└─────────────────────────────────────────────────────────┘
```

---

# PAGE 8: 🛡️ SETTINGS (Global)
**Purpose:** System-wide settings

## Main Tab: "Account Settings"
```
┌─────────────────────────────────────────────────────────────┐
│  ━━━━ SECTION: Account Defaults (Level 1 — Fallback) ━━━━   │
│  ℹ️ These apply to ALL products unless Category/Product       │
│     overrides are set                                        │
│                                                              │
│  Default Strategy Mode:  [🤖 Automatic ▼]                   │
│  Default ACoS Target:    [20  ]%                             │
│  Monthly Budget Cap:     [₹ 50000  ]                         │
│  Default Referral %:     [12  ]%                             │
│  Default Shipping Fee:   [₹ 65    ]                          │
│  Default Packaging:      [₹ 25    ]                          │
│  Default GST %:          [5   ]%                             │
│  Default Returns %:      [15  ]%  ← Updated default          │
│  ℹ️ Product-level > Category-level > Account-level            │
│                                                              │
│  ━━━━ SECTION: Profit Cap (v8.0 NEW! — P17) ━━━━━━━━━━━━━   │
│  Account-Level Profit Cap: [OFF ▼]                           │
│  Max Ad Spend as % of True Profit: [30]%                     │
│  ℹ️ "Never spend more than X% of profit on ads"               │
│  ℹ️ Product-level overrides available on Product page          │
│  ℹ️ Different from P14 (payout-based cap)                     │
│                                                              │
│  ━━━━ SECTION: Seasonal Engine (v8.0 UPDATED — H01) ━━━━━━  │
│  Seasonal Health Demand: [⬜ DISABLED ▼] ← Default OFF!      │
│  ℹ️ Winter→immunity, Summer→hydration, Monsoon→infection      │
│  Activation: Requires APPROVAL before each festival/season    │
│  Post-Activation: Monitor ROI automatically                  │
│  [Request Activation →]                                      │
│                                                              │
│  ━━━━ SECTION: Operation Mode ━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  System Mode: [Semi-Auto ▼]                                  │
│  ℹ️ Strong+Weak auto, ask ONLY uncertain/risky/critical       │
│  Options: Manual | Semi-Auto | Full-Auto                     │
│                                                              │
│  ━━━━ SECTION: Marketplace ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Active: [Amazon India ▼]                                    │
│  ℹ️ Future: Flipkart/Meesho (same system, different adapter)  │
│                                                              │
│  ━━━━ SECTION: Partner Sellers (v5.0 NEW!) ━━━━━━━━━━━━━━   │
│  ℹ️ Partner Buy Box win = OUR win (just label seller name)    │
│  Partner Seller IDs:                                         │
│    [+Add Partner] [Seller ID: A1XXXX] [Name: Partner1]       │
│    [+Add Partner] [_______________] [_______________]        │
│  Auto-Sync Rules: [ON ▼] (same partner logic all platforms)  │
│  Alert on Buy Box Lost (non-partner): [ON ▼]                │
│                                                              │
│  ━━━━ SECTION: API Status ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Ads API (v1 Unified): 🟢 Connected | Last token: 2 hrs ago │
│  Ads Reporting (v3):  🟢 Connected                           │
│  SP-API (EU):         🟢 Connected | Last token: 3 hrs ago   │
│    ├── Orders v2026-01-01 ✅                                  │
│    ├── Pricing v2022-05-01 ✅                                 │
│    ├── Feedback v2024-06-01 ✅                                │
│    ├── Inventory v1 ✅                                        │
│    ├── Notifications v1 ✅                                    │
│    └── Feeds v2021-06-30 ✅                                   │
│  AI Layer 1 (Rules): 🟢 Active                               │
│  AI Layer 2 (ML): 🟢 Active (LightGBM 4.6.0 + Prophet 1.3.0)│
│  AI Layer 3 (LLM): 🟢 Active (Gemini 2.5 Flash)             │
│    API Key: [••••••••••] [Change] ℹ️ Optional — L1+L2 if empty│
│  [🔄 Test All Connections]                                    │
└─────────────────────────────────────────────────────────────┘
```

## Advanced Tab: "Protection Settings"
- Budget spike protection: [ON] — threshold: [150]%
- CPC war shield: [ON] — CPC spike: [3x] → pause
- Buy Box monitor: [ON] — lost → reduce bids + auto-price recovery
- Review brake (P09): [ON] — below [3.5]★ → reduce bids [30]% (Customer Feedback API)
- Negative review brake (P10): [ON] — 100% auto via Customer Feedback API themes + aggregate
- Compliance guard: [ON] — health claim blocker
- Survival mode trigger: [Manual ▼]
- **Profit-per-Price Tracker: [ON] — track profit/day at each price point**

## Settings Tab: "System Settings"
- Timezone: Asia/Kolkata
- Currency: INR
- Data retention: [365] days
- Backup frequency: [Daily ▼]
- API credentials: [Edit] (opens secure modal)
- SP-API credentials: [Edit]
- Python version: 3.11 (display only)
- Flask version: 3.1.3 (display only)
- Database: SQLite (display only, file: data/goamrita.db)

## Google Sheet Configuration Tab (v4.0 NEW!):
```
┌─────────────────────────────────────────────────────────────┐
│  ━━━━ DEFAULT SHEET (fallback for all features) ━━━━━━━━━   │
│                                                              │
│  Default Sheet ID:    [1BxiMVs0XRA5nFMdKvBd...]              │
│  Default Webhook URL: [https://script.google.com/macros/...] │
│  Default Secret Key:  [••••••••] [Change]                    │
│  ℹ️ Used when feature-specific Sheet ID is empty              │
│                                                              │
│  ━━━━ PER-FEATURE SHEET CONFIG ━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                              │
│  📋 K06: Amazon Keyword Fetcher                              │
│  ├── Input Sheet ID:  [________] ← empty = default           │
│  ├── Input Tab Name:  [Keyword_Input] ← REQUIRED             │
│  ├── Input Columns:   [A=ASIN, B=Seed, C=Category, D=Status]│
│  ├── Output Sheet ID: [________] ← empty = default           │
│  ├── Output Tab Name: [Keyword_Results] ← REQUIRED           │
│  ├── Output Columns:  [A-J mapping...] ← REQUIRED            │
│  ├── Webhook URL:     [________] ← empty = default           │
│  ├── Schedule: [Daily ▼] Run Time: [02:00] AM IST            │
│  ├── Last Run: 11 Apr, 02:00 AM | ✅ 45 keywords             │
│  └── [▶️ Run Now] [🔄 Test Connection]                       │
│                                                              │
│  📝 K07: Listing Optimization                                │
│  ├── Sheet ID:    [________] ← empty = default               │
│  ├── Tab Name:    [Listing_Optimization] ← REQUIRED          │
│  ├── Columns:     [A-H mapping...] ← REQUIRED                │
│  ├── Webhook URL: [________] ← empty = default               │
│  ├── Apply Mode:  [Recommend Only ▼]                         │
│  │   Options: Recommend Only / Recommend+Draft / Auto-Apply   │
│  ├── Max keywords per update: [5]                            │
│  ├── Allowed locations: ← v8.0 EXPANDED!                     │
│  │   [✅ Backend Keywords] [⬜ Title] [⬜ Bullet Points]      │
│  │   [⬜ Description] [⬜ Search Terms] [⬜ A+ Content]       │
│  │   ℹ️ Covers ALL listing input fields (v8.0 enhanced K07)   │
│  ├── Schedule: [Weekly ▼]                                    │
│  └── [▶️ Run Now]                                            │
│                                                              │
│  💡 K08: Product Opportunities                               │
│  ├── Sheet ID:    [________] ← empty = default               │
│  ├── Tab Name:    [Product_Opportunities] ← REQUIRED         │
│  ├── Columns:     [A-I mapping...] ← REQUIRED                │
│  ├── Webhook URL: [________] ← empty = default               │
│  ├── Auto-push:   [OFF ▼] ← safety default                  │
│  ├── Schedule: [Weekly ▼]                                    │
│  └── [▶️ Run Now]                                            │
│                                                              │
│  📂 M04-B: Category Keywords                                │
│  ├── Sheet ID:    [________] ← empty = default               │
│  ├── Tab Name:    [Category_Keywords] ← REQUIRED             │
│  ├── Columns:     [A=Keyword, B=Category, C=Volume, D=Date] │
│  ├── Auto-push:   [OFF ▼]                                   │
│  └── Schedule: [Weekly ▼]                                    │
│                                                              │
│  📂 M09: BSR Manual Sheet                                    │
│  ├── Sheet ID:    [________] ← empty = default               │
│  ├── Tab Name:    [BSR_Data] ← REQUIRED                     │
│  └── Columns:     [A=ASIN, B=BSR, C=Date]                   │
│                                                              │
│  RULE: Sheet ID empty → Default Sheet ID used                │
│        Tab Name → ALWAYS REQUIRED (no default)               │
│        Columns → ALWAYS REQUIRED (no default)                │
│                                                              │
│  All changes auto-saved ✓                                    │
└─────────────────────────────────────────────────────────────┘
```

## Data Import Tab (v6.0 NEW!):
```
┌─────────────────────────────────────────────────────────────┐
│  ━━━━ UNIVERSAL DATA IMPORT ━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                              │
│  ℹ️ Every import = 2 options. Templates auto-detect format.   │
│                                                              │
│  📥 IMPORT DATA:                                             │
│  ┌──────────────┬──────────┬──────────┬──────────┐          │
│  │ Data Type    │ Template │ Last Import│ Records │          │
│  │ Organic Rank │ [📥 DL]  │ 5 Apr     │ 120     │          │
│  │ BSR Data     │ [📥 DL]  │ 10 Apr    │ 300     │          │
│  │ Amazon Biz   │ [📥 DL]  │ 8 Apr     │ 2,400   │          │
│  │ Amazon Ads   │ [📥 DL]  │ 8 Apr     │ 5,100   │          │
│  │ Keywords     │ [📥 DL]  │ 3 Apr     │ 450     │          │
│  │ Competitor   │ [📥 DL]  │ — never   │ —       │          │
│  │ COGS/Cost    │ [📥 DL]  │ 1 Apr     │ 300     │          │
│  │ Supplier     │ [📥 DL]  │ 1 Apr     │ 12      │          │
│  └──────────────┴──────────┴──────────┴──────────┘          │
│                                                              │
│  [📁 Upload Excel/CSV] [📋 Link Google Sheet]               │
│                                                              │
│  ━━━━ HISTORICAL IMPORT (one-time) ━━━━━━━━━━━━━━━━━━━━━   │
│  Import old platform reports for AI training:                │
│  [📁 Upload Amazon Business Reports (CSV)]                   │
│  [📁 Upload Amazon Ads Reports (CSV)]                        │
│  ⚠️ Tagged as historical data — AI learns but doesn't copy    │
│  Status: 6 months imported | Improvement: ACoS -49%         │
│                                                              │
│  ━━━━ DEDUP STATUS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Last import: "45 new, 12 updates, 8 duplicates skipped"    │
└─────────────────────────────────────────────────────────────┘
```

---

# PAGE 9: 📋 LOGS
**Purpose:** Full transparency — every action logged with AI layer tags

## Main Tab: "Changelog"
- Complete list of all changes made
- Filter by: date, campaign, keyword, action type, **AI layer tag**
- Each row: Date | What Changed | Old → New | Reason | Effect | IQ Score | **Layer Tags**

## Advanced Tab: "Strategy Impact"
- What was done → Effect → IQ Score → Next Action
- Predicted vs Actual comparison
- Best strategies by product/category
- **Permanent Rules list** (proven strategies auto-applied)
- **Price-Profit History** (profit/day at each price point per product)

## Settings Tab: "Log Settings"
- Log retention period
- Export logs (CSV/Excel)
- Auto-cleanup old logs
- Tag filter presets

---

# PAGE 10: 🧠 LEARNING
**Purpose:** AI learning & intelligence dashboard

## Main Tab: "Knowledge Base"
- What worked (sorted by IQ score)
- What failed (sorted by loss)
- Top strategies by product type
- Seasonal patterns learned
- **Permanent Rules (proven & auto-applied daily)**
- **Cross-Learn Suggestions** (apply to similar products)
- **4-Level Learning Overview (v5.0 NEW!):**
  - Software Level IQ: Global score + data points
  - Category Level: Per-category IQ scores
  - Product Level: Per-product top learnings
  - Keyword Level: Per-keyword patterns
- **Cross-Module Learning Status (v5.0 NEW!):**
  - Active weight connections count
  - Recently promoted tiers (Tier 3→2, Tier 2→1)
  - Per-module AI brain status

## Advanced Tab: "AI Controls"
```
┌─────────────────────────────────────────────────────────┐
│  ━━━━ SECTION: AI Layer Status ━━━━━━━━━━━━━━━━━━━━━   │
│                                                          │
│  Layer 1 (Rules):  🟢 Active | Accuracy: 72%            │
│  Layer 2 (ML):     🟢 Active | Accuracy: 81%            │
│    ├── LightGBM 4.6.0: trained on [2,340] data points   │
│    └── Prophet 1.3.0: [6] seasonal patterns learned      │
│  Layer 3 (LLM):   🟢 Active | Accuracy: 76%             │
│    ├── Model: Gemini 2.5 Flash                           │
│    ├── Free Tier: 250 req/day, 10 req/min                │
│    ├── API Key: [Set ✅]                                  │
│    └── Fallback: Ollama (if API down)                     │
│  Combined:         Accuracy: 91%                         │
│                                                          │
│  ━━━━ SECTION: Intelligence Engines ━━━━━━━━━━━━━━━━━   │
│  Intent engine: [ON ▼]                                   │
│  Seasonal demand engine: [ON ▼]                          │
│  Symptom/Ingredient miner: [ON ▼]                        │
│  Dietary cross-pollination: [ON ▼]                       │
│  Problem→Solution engine: [ON ▼]                         │
│  Ayurvedic keyword intelligence: [ON ▼]                  │
│  Category benchmark: [ON ▼]                              │
│  What-If simulator: [ON ▼]                               │
│  LLM Insight layer: [ON ▼] ℹ️ Needs API key              │
│                                                          │
│  ━━━━ SECTION: Decision Tag Analytics ━━━━━━━━━━━━━━━   │
│  [L1 only]: 45 decisions (accuracy 72%)                  │
│  [L1+L2]: 120 decisions (accuracy 85%)                   │
│  [L1+L2+L3]: 35 decisions (accuracy 91%)                 │
│  [PRICE_CHANGE]: 18 decisions (12 success, 6 failed)     │
│  [BID_CHANGE]: 89 decisions (71 success, 18 failed)      │
│  [View Full Analytics →]                                 │
└─────────────────────────────────────────────────────────┘
```

## Settings Tab: "Learning Settings"
- Minimum data for confidence (clicks): [20]
- Learning period (days before using history): [14]
- Auto A/B test duration (days): [7]
- Strategy reuse threshold (IQ score): [70]
- Cross-learn auto-suggest: [ON ▼]
- Permanent rule minimum proven cycles: [2]

---

# PAGE 11: 👥 USERS & ACCOUNTS (UPDATED v7.0!)
**Purpose:** User management, access control, performance tracking, multi-account, staff roles

## Main Tab: "My Accounts"
```
┌─────────────────────────────────────────────────────────────┐
│  ━━━━ SECTION: Seller Accounts ━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  🔍 [Search accounts...]                                     │
│  ☑️ Select All                                               │
│  ┌────────────┬──────────┬──────────┬──────────┐            │
│  │ ☐ Account  │ Market   │ Role     │ Status   │            │
│  │ ☐ GoAmrita │ Amazon IN│ ⭐ Master │ 🟢 Active│            │
│  │ ☐ GoAmrita2│ Flipkart │ Sub      │ 🟡 Setup │            │
│  │ ☐ Partner1 │ Amazon IN│ Partner  │ 🟢 Active│            │
│  └────────────┴──────────┴──────────┴──────────┘            │
│  [+ Add Account] [🔄 Sync All] [⚡ Bulk Action ▼]           │
│  ℹ️ First-fill = master. Master syncs to all sub-accounts.    │
│                                                              │
│  ━━━━ SECTION: Partner Sellers ━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Partner Buy Box win = OUR win (labeled with seller name)    │
│  ┌──────────┬──────────┬──────────┬──────────┐              │
│  │ ☐ Partner│ Market   │ Seller ID│ Sync     │              │
│  │ ☐ Partner1│ Amazon  │ A1XXXX   │ ON ▼     │              │
│  │ ☐ Partner2│ Flipkart│ F2XXXX   │ ON ▼     │              │
│  └──────────┴──────────┴──────────┴──────────┘              │
│  [+ Add Partner] [⚡ Bulk Action ▼]                          │
│                                                              │
│  ━━━━ SECTION: Quick Profile ━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Name: [Msir]    Email: [msir@email.com]                     │
│  WhatsApp: [+91-XXXXX] (optional, future integration)        │
│  [Edit Profile →]                                            │
└─────────────────────────────────────────────────────────────┘
```

## Advanced Tab: "Staff & Access Control" (UPDATED v7.0!)
```
┌─────────────────────────────────────────────────────────────┐
│  ━━━━ SECTION: Staff Management ━━━━━━━━━━━━━━━━━━━━━━━━   │
│  🔍 [Search staff...]  "3 of 5 selected"                     │
│  ☑️ Select All                                               │
│  ┌──────────┬──────────┬──────────┬──────────┬────────┐     │
│  │ ☐ Name   │ Role     │ Modules  │ Accounts │ Score  │     │
│  │ ☐ Msir   │ Acc Admin│ All      │ All      │ --     │     │
│  │ ☐ Ravi   │ Staff    │ Ads,BuyBox│GoAmrita │ 82/100 │     │
│  │ ☐ Priya  │ Staff    │ Pricing  │ GoAmrita │ 75/100 │     │
│  │ ☐ Supplier1│Supplier│ FBA,Stock│ GoAmrita │ 68/100 │     │
│  └──────────┴──────────┴──────────┴──────────┴────────┘     │
│  [+ Add Staff] [⚡ Bulk: Assign Module ▼] [⚡ Bulk: Enable/Disable ▼] │
│                                                              │
│  ━━━━ PER-STAFF CONFIG (click to expand) ━━━━━━━━━━━━━━━   │
│  Module Access:                                              │
│    Ads: [Full Action ▼] BuyBox: [View Only ▼]               │
│    FBA: [No Access ▼] Listing: [Edit ▼]                     │
│  Assigned Accounts: [☑ GoAmrita] [☐ GoAmrita2]              │
│  Assigned Marketplaces: [☑ Amazon] [☐ Flipkart]             │
│  Alert Receive: [ON ▼]                                       │
│  Is Secondary (escalation): [YES/NO ▼]                      │
│  Notify Email: [ravi@email.com]                              │
│  Notify WhatsApp: [+91-XXXXX] (Phase 4)                     │
│                                                              │
│  ℹ️ Each staff can have multiple modules                      │
│  ℹ️ Permission per module: View / Edit / Full Action / No Access │
│  ℹ️ Admin adds staff directly. New sellers → Super Admin approves. │
└─────────────────────────────────────────────────────────────┘
```

## Performance Tab (NEW v7.0!)
```
┌─────────────────────────────────────────────────────────────┐
│  ━━━━ SECTION: Team Performance (Admin View) ━━━━━━━━━━━━  │
│  🔍 [Search staff...]  Filter: [All Roles ▼] [30 Days]      │
│  ┌──────────┬──────────┬──────────┬──────────┬────────┐     │
│  │ Name     │ Score    │ Rank     │ Trend    │ Pending│     │
│  │ Ravi     │ 82/100   │ 👍 Good  │ ↑ Improv │ 2      │     │
│  │ Priya    │ 75/100   │ 👍 Good  │ → Stable │ 5      │     │
│  │ Supplier1│ 68/100   │ 📊 Avg   │ ↓ Declin │ 8      │     │
│  └──────────┴──────────┴──────────┴──────────┴────────┘     │
│                                                              │
│  ━━━━ SECTION: User Self-View (What user sees) ━━━━━━━━━   │
│  Score: 75/100 | Rank: 👍 Good Performer | Trend: → Stable  │
│  "Complete 3 pending tasks to improve score"                 │
│  "1 task due in 30 min ⏰ — delays affect performance"       │
│                                                              │
│  ℹ️ 30-day rolling window. Old delays auto-clear after 31 days. │
│  ℹ️ Rank only — no loss/profit shown to anyone.               │
└─────────────────────────────────────────────────────────────┘
```

## Settings Tab: "Account Settings"
```
┌─────────────────────────────────────────────────────────────┐
│  ━━━━ SECTION: Multi-Account Sync ━━━━━━━━━━━━━━━━━━━━━   │
│  Master Account: [GoAmrita Bhandar ▼]                        │
│  Auto-Sync to Sub-Accounts: [ON ▼]                           │
│  Sync Scope: [Settings ✅] [Rules ✅] [Templates ✅]          │
│  ℹ️ Each sub-account can override after sync                  │
│                                                              │
│  ━━━━ SECTION: Multi-Contact ━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Email Addresses:                                            │
│    Primary: [msir@email.com]                                 │
│    [+ Add Email]                                             │
│  WhatsApp Numbers: [Phase 4 — OFF] (field stored, ready)     │
│    [+ Add Number]                                            │
│  Per-Function Contact:                                       │
│    Ads Alerts: [email1 ▼] (blank = primary)                  │
│    Stock Alerts: [email2 ▼] (blank = primary)                │
│    Price Alerts: [email1 ▼] (blank = primary)                │
│    ℹ️ Leave blank → auto-fills from primary account email     │
│                                                              │
│  ━━━━ SECTION: Performance Config (Admin Only) (v7.0!) ━━━  │
│  Performance Weights:                                        │
│    Tasks on time: [30%] | Recommendations acted: [25%]       │
│    Task speed: [20%] | Priority tasks: [25%]                 │
│  ℹ️ Admin configurable. Sensible defaults pre-set.            │
│                                                              │
│  ━━━━ SECTION: Notification Events (v7.0!) ━━━━━━━━━━━━━   │
│  Configure which events trigger notifications:               │
│  ┌──────────────┬──────────┬──────────┬──────────┐          │
│  │ Event        │ Priority │ Notify   │ Enabled  │          │
│  │ Buy Box Lost │ 🔴 High  │ All Staff│ ✅ ON    │          │
│  │ Stock Low    │ 🟡 Med   │ Supplier │ ✅ ON    │          │
│  │ Task Overdue │ 🔴 High  │ Assigned │ ✅ ON    │          │
│  │ Score < 40   │ 🟡 Med   │ Admin    │ ✅ ON    │          │
│  └──────────────┴──────────┴──────────┴──────────┘          │
│  [+ Add Event Rule]                                          │
│  ℹ️ Any account event can be configured as notification       │
│                                                              │
│  ━━━━ SECTION: Leave Management (v7.0!) ━━━━━━━━━━━━━━━━   │
│  Advance Leave Requirement: [7 days ▼]                       │
│  Emergency Leave: Admin approves retroactively               │
│  Auto-Delete Disabled Users: [12 months ▼]                   │
│  ℹ️ AI learning data preserved even after user deletion       │
└─────────────────────────────────────────────────────────────┘
```

## Audit Trail Tab (NEW v7.0!)
```
┌─────────────────────────────────────────────────────────────┐
│  ━━━━ SECTION: Activity Log (Admin Only) ━━━━━━━━━━━━━━━   │
│  🔍 [Search...] Filter: [User ▼] [Module ▼] [Date Range]    │
│  ┌──────────┬──────────┬──────────┬──────────────────┐      │
│  │ User     │ Module   │ Action   │ Timestamp        │      │
│  │ Ravi     │ Ads      │ Bid ↑ ₹5 │ 11 Apr 09:15 AM │      │
│  │ Priya    │ BuyBox   │ Price ↓5%│ 11 Apr 09:22 AM │      │
│  │ Ravi     │ Ads      │ KW added │ 11 Apr 10:05 AM │      │
│  └──────────┴──────────┴──────────┴──────────────────┘      │
│  ℹ️ Complete history. Preserved even after user deletion.     │
└─────────────────────────────────────────────────────────────┘
```

---

# PAGE 12: 📚 TRAINING (v5.0 NEW!)
**Purpose:** In-app help, guides, and training materials

## Main Tab: "Getting Started"
- Quick start guide
- Video tutorials (if available)
- Feature overview with examples
- FAQ section

## Advanced Tab: "Feature Deep Dives"
- Per-module detailed guides
- AI Learning explanation
- Cross-module learning visualization
- Best practices per feature

## Settings Tab: "Training Settings"
- Show tooltips: [ON ▼]
- Show onboarding for new features: [ON ▼]
- Training mode (safe sandbox): [OFF ▼]

---

# 📝 SIGNUP PAGE (v5.0 NEW!)
```
┌─────────────────────────────────────────────────────────────┐
│  🏠 GoAmrita Ads Intelligence System — Signup                │
│                                                              │
│  ━━━━ STEP 1: Must-Have Info Only ━━━━━━━━━━━━━━━━━━━━━━   │
│                                                              │
│  Full Name:    [__________________]                          │
│  Email:        [__________________]                          │
│  Password:     [__________________]                          │
│  Confirm:      [__________________]                          │
│                                                              │
│  [Create Account →]                                          │
│                                                              │
│  ℹ️ That's it! All other details can be added later           │
│     in Settings after login.                                 │
│  ℹ️ Marketplace setup, API keys, staff — all optional now.    │
│                                                              │
│  Already have account? [Login →]                             │
└─────────────────────────────────────────────────────────────┘
```

---

# ⏰ SMART DYNAMIC SCHEDULING — PER MODULE (v5.0 NEW!)
```
Every module has its own schedule config accessible from its Settings tab:

┌─────────────────────────────────────────────────────────────┐
│  ━━━━ SECTION: Module Schedule ━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                              │
│  Module: [Buy Box Monitor ▼]                                 │
│  Normal Interval: [30] minutes (default)                     │
│  Current State: 🟢 Normal                                    │
│                                                              │
│  Trigger Conditions:                                         │
│  ├── On LOST: Escalate to [5] minutes [ON ▼]                │
│  ├── On DECREASE >20%: Escalate to [10] minutes [ON ▼]      │
│  ├── On INCREASE >50%: Escalate to [15] minutes [OFF ▼]     │
│  └── [+ Add Trigger Condition]                               │
│                                                              │
│  Recovery: Auto-return to normal when: [Condition resolved ▼]│
│  ℹ️ Escalated → take action → monitor → recovered → normal    │
│                                                              │
│  History: Last escalation: 2 days ago (Buy Box lost 2hr)     │
└─────────────────────────────────────────────────────────────┘
```

---

# 🎨 UI DESIGN PRINCIPLES (Msir's Rules Applied)

```
1. Tab Structure: Main → Advanced → Settings (every page)
2. Sections: Light background alternation
3. Helper Text: ℹ️ beside every option
4. Auto-save: "Saved ✓" feedback on every change
5. Defaults: Everything works out-of-box (zero setup)
6. Top→Bottom: Important first, less important below
7. 3-Level Inheritance: visual indicator everywhere
8. AI 3-Column: Your Value | AI Recommends | Last Effect
9. Decision Tags: visible in every relevant screen
10. Permanent Rules: highlighted as proven strategies
11. Keyword Mode badges: [A] [B] [C] always visible
12. Campaign Dropdown: Select existing / Create New / auto-assign
13. Strategy Mode colors: 🟢🟡🔴🤖 consistent everywhere
14. Multi-Account selector in header (v5.0!)
15. Per-module smart scheduling in Settings tab (v5.0!)
16. Easy Signup: must-have only, rest in Settings (v5.0!)
17. Alliance/Staff: role-based alerts + escalation (v5.0!)
18. Partner Seller: win = our win, labeled (v5.0!)
19. Bulk Operations: Search + Select All + Bulk Action on EVERY list (v7.0!)
20. User Bottom Bar: "X pending | Score: XX | Y overdue ⚠️" on ALL pages (v7.0!)
21. Module-based visibility: users see only assigned modules (v7.0!)
22. Admin-level UI: Super Admin sees all, Account Admin sees account, User sees assigned (v7.0!)
```

---

*Web Control Panel Design v8.0 | 11 April 2026*
*12 Pages | 50+ Tabs | API Versions LOCKED | All v9.0 MASTER changes reflected*
*Changes from v7.0: Round 9 UI — G08 Deal/Coupon launch toggle, P17 Profit Cap (account+product), H01 disabled-by-default, A13 Sales Velocity Alert, I31 Anomaly Detection 3-Level, M11 Competitor Launch Alert, I30 Product Health Score dashboard widget, G14 Listing Health Score, W12 Non-Performing Listing diagnosis panel, K07 expanded listing fields*
*Golden Rule: "Automate business > Everything else" — Minimal UI, maximum automation*
