# 💎 Grow24 AI — Healthcare Ads Intelligence System
## MASTER FEATURE REGISTRY v10.0 — "VIBRANIUM EDITION"
**Project Name:** Grow24 AI (formerly GoAmrita)
**Date:** 12 April 2026 | **Total Features:** 216 (215 active + W10 redirect)  
**Vision:** Not just an Ad Tool — a **Healthcare Business Growth Partner**  
**Design:** Backend = Nuclear Reactor ⚛️ | Frontend = Sweet Shop 🍬
**v7.0 Changes:** Price Segment = CORE learning level, Report Import Module, Organic Competition via API, Universal Import Rule, HIGH-WEIGHT Tags, Tech Validated (₹0), Competition = Search Term level
**v8.0 Changes:** User Management System (3-Level Admin, Module Access, Performance Score, Rank Only, Bulk Ops, Audit Trail, Build Philosophy). Version Audit: pandas 3.0.2, Alembic 1.18.4, scipy 1.17.1, Ads v1 Unified Reporting PRIMARY, 3 Gemini options in menu, STRICT BUILD RULE added
**v9.0 Changes:** Feature Expansion Round 9: 15 new features (P17-P18, W11-W12, K09, G13-G15, M11, I29-I32, H11, R16) + 11 existing feature improvements + W10→G09 duplicate cleanup + A13 sales velocity preset
**v10.0 Changes:** 360° Gap Analysis: 33 gaps integrated, 3 new modules (Smart Pricing, FBA, A+), 7 new features, 13 enhancements, 8 design principles, Category 12 (Infrastructure & Safety), Developer TODO + Gap Analysis merged, Orchestrator conflict examples, Auto-First philosophy, naming standardized
**Future Module Standard Note:** For ALL NEW future modules/features, follow `GoAmrita_MASTER_Future_Module_Standard_v1.0.md`. Legacy modules stay unchanged until planned migration.

---

# 📐 ARCHITECTURE PHILOSOPHY

```
USER EXPERIENCE: Like eating sweet 🍬
├── Excel opens automatically every morning
├── Everything auto-filled (AI + IQ + learning)
├── User: LOOK → REVIEW (rare edit) → SUBMIT BACK
├── Maximum 5 minutes daily
├── If user BUSY → system auto-applies strong recommendations
├── WhatsApp summary for on-the-go
├── Web Panel: control center (same code: laptop + server)
└── Browser/OS notifications for real-time alerts

BACKEND POWER: Like nuclear reactor ⚛️
├── 153+ features running silently
├── 3-Layer AI: Rules + ML(LightGBM/Prophet) + LLM(Gemini 2.5 Flash)
├── 4-Level AI Learning: Software→Category→Product→Keyword (v6.0!)
├── Per-Module AI Brain: Each module learns independently (v6.0!)
├── Cross-Module Learning: Weight-based, micro-attribute level (v6.0!)
├── Profit-based calculations (not Amazon's misleading ACoS)
├── Self-learning database (gets smarter daily → permanent rules)
├── Auto A/B testing
├── Multi-marketplace ready (Amazon now, Flipkart/Meesho future)
├── Multi-Account + One Login + Alliance/Staff roles (v6.0!)
├── Smart Dynamic Scheduling: Event-triggered escalation (v6.0!)
├── Ads API + Seller API cross-communication
├── Partner Seller logic (win = our win) (v6.0!)
├── 3-Level Admin: Super Admin → Account Admin → User/Staff (v8.0!)
├── Module-based access control + bulk operations everywhere (v8.0!)
└── All dynamic — nothing hardcoded — future-proof plugin architecture

BUILD PHILOSOPHY (Golden Rule — v8.0!):
├── 🔴 "Automate business > Everything else"
├── Only build what directly BOOSTS or AUTOMATES business
├── Architect features FULLY (strong fundamentals)
├── Build from MINIMUM (start small)
├── Scale on the go (no rewrites needed)
├── Easy to implement, easy to test, easy to scale
├── Phase-wise development (decide phase per feature)
└── If it doesn't boost business → reconsider adding it

DESIGN PRINCIPLES (DNA of every feature — v10.0!):
├── 🔧 P1: SCALEABLE — New marketplace/seller/feature = system doesn't break
├── ⚙️ P2: CONFIGURABLE — Every option in settings, no hardcoding
├── 🤖 P3: AUTO-IMPROVE — System learns every run, gets smarter daily
├── ✅ P4: AUTO-FIRST — Everything auto by default!
│   └── Approval ONLY where: AI not confident OR risky/critical action
│   └── User can switch ANY feature: auto / semi-approval / manual in settings
├── 📋 P5: USER CONTROL — User always has option to change mode per feature
├── 🔌 P6: EXTENSIBLE — User can create custom automation rules (Custom Rule Builder)
├── 💡 P7: AI RECOMMENDS — AI finds patterns, recommends new automation rules
└── 🛡️ P8: SAFETY NETS — Hard limits + auto-rollback + gradual rollout

ACTION PRIORITY CHAIN (for Orchestrator — v10.0!):
  REMOVE > REDUCE > MAINTAIN > INCREASE > EXPAND
```

---

# 🏗️ SYSTEM LAYERS

```
Layer 1: DATA LAYER (Pull + Store + History)
Layer 2: INTELLIGENCE LAYER (3-Layer AI: Rules + ML + LLM)
Layer 3: LEARNING LAYER (4-Level: Software→Category→Product→Keyword) ← NEW v6.0!
Layer 4: DECISION LAYER (Rules + Learning + Prediction + Multi-Tag)
Layer 5: ACTION LAYER (3 Modes: Approval / Semi-Auto / Full-Auto)
Layer 6: REPORT LAYER (Excel + Email + WhatsApp + Web Dashboard)
Layer 7: CONFIG LAYER (Web Panel + JSON + 3-Level Inheritance)
Layer 8: PROTECTION LAYER (Risk + Compliance + Budget Guard)
Layer 9: ALERT LAYER (4 types + Smart Scheduling + Voice + Escalation) ← NEW v6.0!
Layer 10: INTEGRATION LAYER (Webhook + Google Sheets + SP-API)
Layer 11: MARKETPLACE LAYER (Amazon + Flipkart + Meesho adapters)
Layer 12: USER LAYER (3-Level Admin + Module Access + Performance + Bulk Ops) ← UPDATED v8.0!
Layer 13: INFRASTRUCTURE LAYER (Orchestrator + Scheduler + Event Bus + Safety) ← NEW v10.0!
```

---

# 🔒 VERSION LOCK — ALL APIs & LIBRARIES

## 🚨 STRICT BUILD-TIME RULE (UPDATED v8.0!)
```
┌──────────────────────────────────────────────────────────────┐
│  ⛔ MANDATORY FOR ALL DEVELOPMENT — ZERO TOLERANCE:           │
│                                                               │
│  1. USE ONLY the exact versions listed below                  │
│  2. USE ONLY functions/methods from OFFICIAL DOCS of          │
│     THAT EXACT pinned version — no assumptions!               │
│  3. NEVER use deprecated functions from older versions        │
│  4. NEVER use preview/beta functions from newer versions      │
│  5. NEVER mix old API patterns with new API patterns          │
│  6. NEVER assume a function exists — VERIFY from official docs│
│  7. NEVER copy code from internet that uses different version │
│  8. NEVER use any function found online if not in OUR version │
│  9. requirements.txt MUST pin exact versions (==, not >=)     │
│  10. Before coding ANY API/library call:                      │
│      → Open OFFICIAL documentation of OUR pinned version      │
│      → Confirm the method/function EXISTS in that version     │
│      → Confirm the parameters are correct for that version    │
│      → ONLY THEN write the code                               │
│  11. If confused → STOP, read official docs, then code        │
│  12. All versions verified compatible: April 2026 ✅           │
│                                                               │
│  SOURCE OF TRUTH: Only official documentation of pinned       │
│  version. NOT: Stack Overflow, NOT: random blogs, NOT:        │
│  AI training data, NOT: internet code snippets that may       │
│  use a different version's functions.                         │
│                                                               │
│  WHY: One wrong version function = hours of debugging.        │
│  Internet code = often wrong version. Official docs = ONLY    │
│  reliable source. PREVENTION > CURE.                          │
└──────────────────────────────────────────────────────────────┘
```

## Amazon Ads API (UPDATED v8.0!)
```
Campaign Management: Amazon Ads API v1 (Unified)
  ⚠️ v1 = NEWEST! (Complete architectural reboot, NOT older than v3)
  Endpoint: advertising-api-eu.amazon.com
  Covers: All ad types (SP, SB, SD) in single unified API
  
Reporting: Amazon Ads API v1 — Unified Reporting (PRIMARY) ← UPDATED v8.0!
  ⚠️ v1 Unified Reporting = PRIMARY for ALL reports
  Covers: Search Term, Performance, Placement, Impression Share, Click Share
  Benefits: Cross-product combine (SP+SB+SD), 15 months daily, 6 years monthly
  
Reporting Fallback: Ads Reporting API v3 (ONLY if v1 Unified missing specific data)
  ⚠️ v3 will eventually deprecate — use v1 Unified first, v3 ONLY for gaps
  ⚠️ As of April 2026: NO gaps found — v1 Unified covers everything v3 does
```

## Amazon SP-API (Selling Partner API)
```
Region: EU (India = Europe region, NOT Far East!)
Endpoint: sellingpartnerapi-eu.amazon.com

Catalog Items:      v2022-04-01  (product attributes, basic rating/salesRanks)
Pricing:            v2022-05-01  (getCompetitiveSummary, Buy Box, competitor prices)
Orders:             v2026-01-01  (NEWEST! 2 ops vs 10, migration deadline March 2027)
FBA Inventory:      v1           (stock levels)
Feeds:              v2021-06-30  (bulk updates — JSON ONLY, XML deprecated!)
Listings Items:     v2021-08-01  (listing health, attributes)
Notifications:      v1           (ORDER_CHANGE, LISTING_CHANGE, INVENTORY_CHANGE, ANY_OFFER_CHANGED)
Customer Feedback:  v2024-06-01  (NEW! Review insights at ASIN/browse node level, weekly refresh)
Brand Analytics:    v1           (Top search terms, if Brand Registered ✅)
Sales & Traffic:    v2024-04-24  (page views, sessions, conversion, Buy Box % — ASIN+Date level) ← NEW v7.0!
Search Catalog Perf: Brand Analytics (impressions, clicks, cart, purchases — ASIN+search term) ← NEW v7.0!
```

## Python & Libraries (UPDATED v10.1 — Lean Stack!)
```
Python:     3.11.x   (stable)
Flask:      3.1.3    (web dashboard)
openpyxl:   latest   (Excel read/write)
requests:   latest   (API calls)

⚠️ DEFERRED LIBRARIES (NOT planned till Dec 2026):
See DEFERRED_LIBRARIES.md for full list.
Libraries like LightGBM, Prophet, pandas, SQLAlchemy, Alembic,
Gemini, Ollama are FROZEN — do not use without Msir approval.

scipy and numpy: May be recommended where genuinely needed.
Must get Msir approval before integration.
```

## Database
```
Primary: JSON files (data stored in ClaudeCode/Report/*/Json/)
  ├── Zero setup — Python built-in json module
  ├── Simple, works perfectly for current scale
  ├── Backup = file copy
  └── DB (SQLite/PostgreSQL) = DEFERRED, add when data volume demands it
      Requires Msir approval before any DB integration.

```

## Google Sheet Integration
```
Method: Google Apps Script (GAS) Webhook — NO OAuth, NO API Key
  ├── GAS deployed as Web App per sheet
  ├── Python → HTTP POST → GAS → Sheet read/write
  ├── Security: Simple secret key (user-defined string)
  └── Template script provided (gas_webhook_template.js)

Per-Feature Config:
  ├── Sheet ID: [configurable, empty = default Sheet ID]
  ├── Tab Name: [REQUIRED — no default]
  ├── Columns: [REQUIRED — no default]
  ├── Webhook URL: [configurable, empty = default URL]
  └── Schedule: [configurable from menu]

3-Layer Data Architecture:
  Sheet (INPUT/OUTPUT) ←→ SQLite (TRUTH) ←→ Web Panel (CONTROL)
  ├── Sheet: User reads/writes data
  ├── SQLite: System stores/queries (source of truth)
  ├── Web Panel: User configures/monitors/edits
  └── Sync: DB→Sheet incremental push, sheet_synced flag
```

## AI / LLM
```
Layer 3 (LLM): DEFERRED — not planned till Dec 2026
  ├── Gemini 2.5 Flash/Lite/Pro: FROZEN (see DEFERRED_LIBRARIES.md)
  ├── Ollama (local): FROZEN
  ├── System runs 100% on Layer 1 (Rule-Based AI) — handles 80%+ decisions
  └── When genuinely needed → recommend to Msir → approval → integrate
```

## 360° API Coverage Summary
```
Total Features: 216 (215 active)
Fully API-Covered: 163+ (89%)
Gaps with Workarounds: 6
  1. Competitor Price (M01) → Keepa API (~₹500/mo) OR manual sheet
  2. Individual Review Text (P10) → Customer Feedback themes + aggregate
  3. BSR Real-time (M09) → Manual sheet PRIMARY, SP-API fallback
  4. Competitor Keywords (M04) → 4-approach composite (no direct API)
  5. Deep Review Sentiment → Customer Feedback themes (limited)
  6. Historical BSR → Store daily snapshots locally
Cost: ₹0 for all API calls (within free tiers)
```

---

# 🏗️ MULTI-MARKETPLACE ARCHITECTURE

```
📁 Grow24_AI/
│
├── 📁 core/                         ← MARKETPLACE AGNOSTIC (100% reusable)
│   ├── bid_optimizer.py             ← Same bid logic for any marketplace
│   ├── budget_manager.py            ← Same budget logic
│   ├── iq_engine.py                 ← Same AI scoring
│   ├── profit_calculator.py         ← Same profit math
│   ├── strategy_learner.py          ← Same learning engine
│   ├── decision_tagger.py           ← Multi-tag system for decisions
│   ├── effect_tracker.py            ← Action → Effect → Permanent Rule
│   ├── sheet_manager.py             ← Google Sheet GAS webhook handler ← NEW v5.0!
│   ├── db_manager.py                ← SQLAlchemy DB operations ← NEW v5.0!
│   └── ...all intelligence files
│
├── 📁 marketplaces/                 ← MARKETPLACE SPECIFIC (adapter pattern)
│   ├── base_adapter.py              ← Abstract MarketplaceAdapter class
│   │
│   ├── 📁 amazon/
│   │   ├── 📁 ads_api/              ← Amazon Ads API v1 (Unified) ← UPDATED v4.0!
│   │   │   ├── auth.py              ← OAuth2 LWA (exists ✅)
│   │   │   ├── data_pull.py         ← Campaign/keyword/ad group data (v1 Unified)
│   │   │   ├── campaign_manager.py  ← Campaign CRUD (v1 Unified)
│   │   │   ├── keyword_manager.py   ← Keyword CRUD + lifecycle (v1 Unified)
│   │   │   ├── report_fetcher.py    ← v1 Unified Reporting (PRIMARY) + v3 fallback ← UPDATED v8.0!
│   │   │   └── keyword_fetcher.py   ← K06: Amazon keyword suggestions ← NEW v5.0!
│   │   │
│   │   ├── 📁 seller_api/           ← Amazon SP-API EU endpoint
│   │   │   ├── auth.py              ← SP-API OAuth (exists ✅)
│   │   │   ├── pricing.py           ← Auto Price Update (v2022-05-01)
│   │   │   ├── inventory.py         ← Stock check (FBA Inventory v1)
│   │   │   ├── orders.py            ← Order data, velocity (v2026-01-01) ← UPDATED v4.0!
│   │   │   ├── listings.py          ← Listing health (v2021-08-01)
│   │   │   ├── catalog.py           ← Product catalog + basic rating (v2022-04-01)
│   │   │   ├── returns.py           ← Return reasons, impact analysis
│   │   │   ├── feedback.py          ← Customer Feedback API (v2024-06-01) ← NEW v4.0!
│   │   │   ├── feeds.py             ← Bulk updates JSON only (v2021-06-30)
│   │   │   ├── notifications.py     ← Real-time webhooks (v1)
│   │   │   └── listing_updater.py   ← K07: Listing update via Feeds API ← NEW v5.0!
│   │   │
│   │   ├── amazon_adapter.py        ← Implements MarketplaceAdapter
│   │   └── config/
│   │       ├── api_credentials.json
│   │       ├── sp_api_credentials.json
│   │       └── marketplace_settings.json
│   │
│   └── 📁 flipkart/                 ← FUTURE (same structure)
│       ├── 📁 ads_api/
│       ├── 📁 seller_api/
│       ├── flipkart_adapter.py
│       └── config/
│
├── 📁 ai/                           ← 3-LAYER AI ENGINE + 4-LEVEL LEARNING
│   │                                # DEFERRED — files listed for future reference only
│   ├── layer1_rules.py              ← Rule-based AI (Day 1) ← ACTIVE
│   ├── layer2_ml.py                 ← LightGBM 4.6.0 + Prophet 1.3.0 (Phase 2) ← DEFERRED
│   ├── layer3_llm.py                ← Gemini 2.5 Flash / Ollama (Phase 3, optional) ← DEFERRED
│   ├── merger_engine.py             ← Combines all layer decisions
│   ├── decision_tagger.py           ← Multi-tag per decision
│   ├── effect_tracker.py            ← Track action effects
│   ├── permanent_rule_maker.py      ← Learn → Test → Permanent
│   ├── cross_learner.py             ← Apply learnings to similar products
│   ├── opportunity_finder.py        ← K08: Product gap analysis ← NEW v5.0!
│   ├── learning_engine.py           ← 4-Level learning (Software→Category→Product→Keyword) ← NEW v6.0!
│   ├── module_ai_manager.py         ← Per-module AI brain orchestrator ← NEW v6.0!
│   ├── cross_module_learner.py      ← Weight-based cross-module learning engine ← NEW v6.0!
│   └── micro_attribute_analyzer.py  ← Micro-level attribute effect analysis ← NEW v6.0!
│
├── 📁 web_panel/                    ← Python Flask 3.1.3 (localhost + server)
│   ├── app.py                       ← Flask server
│   ├── templates/                   ← HTML (10 pages, 30+ tabs)
│   ├── static/                      ← CSS/JS
│   └── api/                         ← REST endpoints for AJAX
│
├── 📁 alerts/                       ← ADVANCED ALERT SYSTEM ← NEW v6.0!
│   ├── alert_engine.py              ← 4-type alert engine (event/%/value/time)
│   ├── smart_scheduler.py           ← Dynamic scheduling (normal→escalated→recovery)
│   ├── notification_manager.py      ← Voice, volume, critical repeat, browser/OS
│   ├── escalation_chain.py          ← Primary → Secondary staff escalation
│   └── alert_configs.py             ← Per-module alert configurations
│
├── 📁 users/                        ← USER MANAGEMENT ← UPDATED v8.0!
│   ├── auth.py                      ← Login, signup, approval flow
│   ├── account_manager.py           ← Multi-account, first-fill sync
│   ├── role_manager.py              ← Alliance/Staff roles, module-based permissions ← UPDATED v8.0!
│   ├── admin_hierarchy.py           ← Super Admin → Account Admin → User/Staff ← NEW v8.0!
│   ├── performance_tracker.py       ← 30-day rolling score, rank, trend ← NEW v8.0!
│   ├── audit_trail.py               ← User action logging ← NEW v8.0!
│   ├── leave_manager.py             ← Leave system (7-day advance) ← NEW v8.0!
│   ├── partner_seller.py            ← Partner seller logic (win=our win)
│   └── contact_manager.py           ← Multi-email/WhatsApp, per-function contacts
│
├── 📁 config/                       ← 3-LEVEL INHERITANCE
│   ├── account_settings.json        ← Level 1: Account defaults
│   ├── category_templates.json      ← Level 2: Category overrides (optional)
│   ├── product_settings.json        ← Level 3: Product overrides
│   ├── system_settings.json         ← Global system config
│   ├── optimization_rules.json      ← Bid/budget rules + dynamic %
│   ├── alert_config.json            ← Email/WhatsApp/Browser/OS recipients
│   ├── festival_calendar.json       ← Indian festivals + multipliers
│   ├── salary_cycle.json            ← Monthly budget cycle
│   ├── dayparting_rules.json        ← Initial hour rules (AI learns)
│   ├── cooling_periods.json         ← Days OR Budget (whichever first)
│   ├── keyword_sources.json         ← Google Sheet, CSV, webhook configs
│   ├── compliance_dictionary.json   ← Restricted health terms
│   ├── competitor_tracking.json     ← Competitor ASINs to monitor
│   ├── buybox_config.json           ← Buy Box auto-price settings
│   ├── sheet_configs.json           ← Per-feature Google Sheet ID/Tab/Column mapping ← NEW v5.0!
│   ├── partner_sellers.json         ← Partner seller IDs per marketplace ← NEW v6.0!
│   ├── staff_roles.json             ← Alliance/Staff role definitions ← NEW v6.0!
│   ├── module_schedules.json        ← Per-module smart scheduling config ← NEW v6.0!
│   ├── alert_notification.json      ← Voice, volume, critical, escalation config ← NEW v6.0!
│   ├── learning_weights.json        ← Cross-module learning weight config ← NEW v6.0!
│   ├── access_permissions.json      ← Module-based user permissions ← NEW v8.0!
│   └── performance_config.json      ← Performance weights, thresholds, rank labels ← NEW v8.0!
│
├── 📁 data/
│   ├── 📁 daily_metrics/
│   ├── 📁 search_terms/
│   ├── 📁 changes_log/
│   ├── 📁 reports/
│   ├── 📁 approved_actions/
│   ├── 📁 learning_db/             ← Strategy knowledge base
│   ├── 📁 decision_tags/           ← Tagged decision records
│   ├── 📁 effect_history/          ← Action effect tracking
│   ├── 📁 permanent_rules/         ← Proven rules
│   ├── 📁 price_profit_tracker/    ← Profit per price point
│   ├── 📁 bsr_snapshots/           ← Daily BSR snapshots
│   └── 📁 review_snapshots/        ← Weekly review data snapshots
│
├── 📁 database/                     ← SQLite + SQLAlchemy ← NEW v5.0!
│   ├── goamrita.db                  ← Main SQLite database
│   ├── goamrita.db.backup           ← Daily auto-backup
│   ├── models.py                    ← SQLAlchemy ORM models
│   ├── engine.py                    ← DB engine (SQLite default. PostgreSQL ready if 40+ sellers)
│   └── 📁 migrations/              ← Alembic schema migrations
│       ├── env.py
│       ├── alembic.ini
│       └── 📁 versions/
│
├── 📁 templates/                    ← User-facing templates ← NEW v5.0!
│   └── gas_webhook_template.js      ← GAS script user copies to Google Sheet
│
├── main.py                          ← Master orchestrator
├── daily_run.py                     ← One-click daily pipeline
├── process_approvals.py             ← Process returned Excel
└── setup_auto_open.py               ← Mac scheduler setup
```

### Adapter Pattern (Marketplace Agnostic):
```python
class MarketplaceAdapter:
    """Abstract base — implement per marketplace"""
    def get_campaigns(self): pass
    def update_bid(self, keyword_id, new_bid): pass
    def get_stock(self, asin): pass
    def update_price(self, asin, new_price): pass
    def get_orders(self): pass
    def get_search_terms(self): pass
    def get_buybox_status(self, asin): pass      # NEW v4.0
    def get_review_insights(self, asin): pass     # NEW v4.0
    def get_bsr(self, asin): pass
    def get_keyword_suggestions(self, asin_or_seed): pass  # NEW v5.0
    def update_listing(self, asin, attributes): pass       # NEW v5.0
    def get_partner_sellers(self): pass                     # NEW v6.0
    def check_partner_buybox(self, asin): pass              # NEW v6.0

class AmazonAdapter(MarketplaceAdapter):
    # Uses Amazon Ads API v1 (Unified) + v1 Unified Reporting (PRIMARY) + SP-API EU
    # ⚠️ v1 Unified = NEWEST! Reporting v3 = FALLBACK only if v1 missing data
    # Partner Seller: Buy Box win = OUR win (v6.0)

class FlipkartAdapter(MarketplaceAdapter):
    # Uses Flipkart Ads API + Seller API (FUTURE)
    # Same partner seller logic as Amazon (v6.0)

class MeeshoAdapter(MarketplaceAdapter):
    # Uses Meesho API (FUTURE)
    # Same partner seller logic (v6.0)
```

---

# 🧠 3-LAYER AI ENGINE

## Layer 1: Rule-Based AI (Phase 1 — Day 1)
```
Technology: Pure Python 3.11 logic + math
Cost: ₹0 (zero)
Handles: 80% of all decisions
Examples:
  IF ACoS < 10% AND clicks > 20 → increase bid (dynamic %)
  IF stock < 10 units → switch to Profitable mode
  IF no sale after ₹500 spend → flag as waste
```

## Layer 2: Statistical/ML AI (Phase 2) — DEFERRED
```
⚠️ DEFERRED — LightGBM, Prophet frozen till Dec 2026

Technology: LightGBM 4.6.0 + Prophet 1.3.0 + pandas + numpy + scipy
Cost: ₹0 (runs locally)
Python: 3.11 (stable + best performance)

LightGBM 4.6.0: Best for ad data — handles categorical features (campaign type,
  strategy mode) natively. Faster than scikit-learn for large data.
  Used for: bid prediction, ACoS forecasting, waste detection

Prophet 1.3.0 (Meta): Time series forecasting
  Used for: seasonal demand prediction, sales forecasting, festival planning

scipy 1.17.1: A/B test statistical significance, confidence intervals
```

## Layer 3: LLM AI (Phase 3, OPTIONAL) — DEFERRED
```
⚠️ DEFERRED — Gemini/Ollama frozen till Dec 2026

Gemini 2.5 Flash/Lite/Pro: FROZEN (see DEFERRED_LIBRARIES.md)
Ollama (local): FROZEN
System runs 100% on Layer 1 (Rule-Based AI) — handles 80%+ decisions
When genuinely needed → recommend to Msir → approval → integrate

Used for (FUTURE): Human-language insights, complex pattern explanation
OPTIONAL: Only activates if API key provided
  If no API key → Layer 1+2 handle everything (no problem!)
```

## Layer Independence & Cooperation:
```
┌──────────────────────────────────────────────────────┐
│  CRITICAL DESIGN PRINCIPLE:                           │
│                                                       │
│  Layer 3 absent? → Layer 1+2 handle everything ✅     │
│  Layer 2 not trained? → Layer 1 alone works (Day 1) ✅│
│  All 3 present? → BEST results (3-layer verification) │
│                                                       │
│  Layers HELP each other, NEVER conflict               │
│  Merger Engine resolves disagreements:                 │
│  ├── All 3 agree → HIGH confidence → auto-apply       │
│  ├── 2 of 3 agree → MEDIUM confidence → auto-apply    │
│  ├── All disagree → LOW confidence → ask user          │
│  └── Each layer's accuracy tracked over time           │
└──────────────────────────────────────────────────────┘
```

## Multi-Tag Decision System:
```
Every decision gets MULTIPLE tags:

{
  "decision_id": "D-20260411-001",
  "tags": [
    {"layer": "L1", "rule": "stock_low_price_up"},
    {"layer": "L2", "model": "lightgbm_4.6.0", "prediction": "+8%"},
    {"layer": "L3", "llm": "gemini_2.5_flash", "reasoning": "seasonal demand"},
    {"confidence": 78},
    {"source": "sp_api_inventory"},
    {"strategy": "profitable_mode"}
  ],
  "effect_tags": [
    {"layer": "L1", "accuracy": "CORRECT"},
    {"layer": "L2", "accuracy": "CORRECT"},
    {"layer": "L3", "accuracy": "PARTIAL"}
  ]
}

Track which layer is most accurate over time →
Layer accuracy dashboard in Learning page
```

## Action Effect → Permanent Rule Lifecycle:
```
Step 1: ACTION TAKEN (tagged with layers + context)
Step 2: EFFECT MONITORED (3-7 days)
  ├── Track profit per day BEFORE action
  ├── Track profit per day AFTER action
  ├── Track at each price point: price → profit/day → units/day
Step 3: AI JUDGMENT (improved/failed/mixed)
Step 4: AUTO-ADJUST if failed (try different %, try different approach)
Step 5: RE-EVALUATE adjusted action
Step 6: MAKE PERMANENT if proven (save to permanent_rules/)
Step 7: CROSS-LEARN to similar products (suggest, test, then permanent)

KEY: Don't blindly restore after condition changes!
  If price increase worked → KEEP IT even after stock restocked
  If price increase failed → auto-restore + learn "don't do this"
```

---

# 🏗️ 3-LEVEL INHERITANCE SYSTEM

```
LEVEL 1: ACCOUNT (Global Defaults — always exists)
├── Referral %: 12
├── Shipping Fee: ₹65
├── Packaging: ₹25
├── GST %: 5
├── Returns %: 15 (default)
├── Default Strategy: Auto
├── Target ACoS: 20%
└── Applied to: ALL products (ultimate fallback)

LEVEL 2: CATEGORY (Optional Override — not mandatory)
├── "Honey & Sweeteners":
│   ├── Shipping Fee: ₹85 (heavier)
│   ├── Returns %: 8 (less returns)
│   └── Rest: inherits Account
├── "Supplements":
│   ├── Returns %: 20 (higher returns)
│   └── Rest: inherits Account
└── NOT MANDATORY to assign category

LEVEL 3: PRODUCT (Specific Override)
├── Pure Honey 1kg:
│   ├── Shipping Fee: ₹95 (heaviest)
│   └── Rest: inherits Category → Account
└── If no category assigned → directly inherits Account

RESOLUTION: Product > Category > Account
  def get_value(product, field):
      if product[field] is not EMPTY: return product[field]
      elif product.category and category[field] is not EMPTY: return category[field]
      else: return account[field]
```

---

# ⏳ COOLING PERIOD SYSTEM

```
DUAL CONDITION: Days OR Budget — WHICHEVER EXCEEDS FIRST

┌──────────────────┬─────────────┬──────────────────────┐
│ Product Type      │ Days Limit  │ Budget Limit          │
│───────────────────│─────────────│──────────────────────│
│ Low Price (<₹500) │ 10 days     │ ₹500                 │
│ High Price (₹500+)│ 12 days     │ 100% of sale price   │
└──────────────────┴─────────────┴──────────────────────┘

Default Mode: Budget-First (budget usually hits first for expensive products)
Price Threshold: ₹500 (configurable)

Example:
  Honey ₹599 (High) → 12 days OR ₹599 spend (whichever first)
  Sachet ₹49 (Low) → 10 days OR ₹500 spend (whichever first)
```

---

# 🧠 4-LEVEL AI LEARNING SYSTEM (NEW v6.0!)

```
┌──────────────────────────────────────────────────────┐
│          SOFTWARE LEVEL (Global IQ)                   │
│  All sellers + All marketplaces + All data            │
│  Tags: marketplace, category, price_range,            │
│        season, product_type, match_type               │
│  IQ Score: Based on data volume + accuracy            │
│  New seller? → Software learning helps                │
│  New category? → Software + similar category helps    │
├──────────────────────────────────────────────────────┤
│         CATEGORY LEVEL LEARNING                       │
│  Cross-seller, cross-marketplace per category         │
│  "Ayurvedic products behave like THIS"                │
│  Tagged by marketplace (Amazon ≠ Flipkart ≠ Meesho)   │
├──────────────────────────────────────────────────────┤
│         PRODUCT LEVEL LEARNING                        │
│  Specific ASIN/product behavior patterns              │
│  "This honey product converts best with..."           │
│  New keyword? → Product learning helps                │
├──────────────────────────────────────────────────────┤
│         KEYWORD LEVEL LEARNING                        │
│  Individual keyword performance patterns              │
│  "organic honey → morning, phrase match best"         │
│  Ads + Listing modules primarily                      │
└──────────────────────────────────────────────────────┘

4 CORE LEVELS (always): Software → Category → Price Segment → Product  ← UPDATED v7.0!

PRICE SEGMENT (CORE — v7.0 NEW!):
  ├── Budget: <₹199
  ├── Mid: ₹200-499
  ├── Premium: ₹500-999
  ├── Luxury: ₹1000+
  ├── Thresholds: configurable by user
  └── WHY CORE: Same category, different price = VERY different behavior
      "Honey ₹99" vs "Honey ₹599" = different customer, CTR, conversion

EXTENSIBLE LEVELS (as needed):
  ├── Keyword Level (Ads/Listing specific)
  ├── Seller Account Level (LIMITED: daily sales tracking, trends, account health only)
  └── Supplier Level (delivery, quality, reliability — connected
      to product returns/reviews, NOT keyword based)

⚠️ NO SELLER LEVEL — restricts learning, complicates system
⚠️ MARKETPLACE TAG MANDATORY — Amazon/Flipkart/Meesho have
   different price zones, customer segments, competition patterns
```

---

# 🔗 PER-MODULE AI + CROSS-MODULE LEARNING (NEW v6.0!)

## Each Module = Own AI Brain
```
┌────────────────┬──────────────────────────────────────┐
│ Module         │ AI Learns                             │
│────────────────│──────────────────────────────────────│
│ Ads Module     │ Bid patterns, keyword perf, time-of-day│
│ FBA Module     │ Qty prediction, restock timing, warehouse│
│ Sales Monitor  │ Sales patterns, seasonal trends, elasticity│
│ Buy Box Module │ Price sensitivity, competitor behavior  │
│ Listing Module │ Keyword impact on ranking, content opt │
│ Review Module  │ Rating trends, review impact on sales  │
│ Supplier Module│ Delivery time, quality, return rates   │
└────────────────┴──────────────────────────────────────┘

All modules → feed into 4-Level Learning System (tagged)
All modules → benefit from cross-learning (with relevance check)
```

## Cross-Module Learning — Weight-Based Relevance Engine
```
GOLDEN RULE:
  Default = PASS learning to other modules
  Only EXCLUDE when 100% sure no effect
  Passing unnecessarily = no harm (extra calculation)
  Excluding wrongly = missed insight, potential loss ❌

TIER 1: HIGH WEIGHT (direct, proven effect)
  → Auto-pass, full influence
  → Example: Review drop → Ad CTR (direct)

TIER 2: LOW WEIGHT (indirect, maybe, chain effect)
  → Auto-pass, reduced influence
  → System adjusts weight over time based on actual data
  → Example: FBA stock → Listing Ranking (indirect)

TIER 3: ZERO WEIGHT (100% sure, micro-level verified)
  → Don't pass currently
  → System re-evaluates periodically
  → If data shows correlation → auto-promote to Tier 2
  → Very few cases: Ad Bid→Supplier Quality, FBA Qty→Listing Content,
    Buy Box Price→Listing Content, Listing Title→Supplier Delivery

TIER 4: ASK (can't decide)
  → Build time → Developer decides initial tier
  → Runtime → Ask user OR system suggests from data
  → System learns → auto-assigns tier over time

WEIGHT ADJUSTMENT (Self-Learning):
  Initial weight = Developer/Rule assigned
  → data collected → measure actual correlation
  → evidence found → weight auto-adjusts (up or down)
  → strong evidence → tier promotion/demotion
  Example: Day 1 "FBA→Review" = Tier 3, Day 90 data shows 68% 
  correlation → promote to Tier 2, Day 365 → Tier 1
```

## Micro-Level Attribute Analysis
```
⚠️ CRITICAL: Check effects at MICRO-ATTRIBUTE level, NOT broad module

Module Sub-Attributes:
├── Listing: Content (title/bullets/desc), Ranking, Images, A+, Keywords
├── FBA: Stock Level, Delivery Speed, Warehouse, Fees
├── Review: Rating Score, Review Count, Sentiment, Recent Reviews
├── Buy Box: Win Status, Price Position, Competitor Count
├── Ads: Bid, Budget, Keyword Perf, Placement
├── Sales: Volume, Trend, Seasonal Pattern, Conversion Rate
├── Supplier: Quality, Delivery Time, Price, Reliability

"FBA → Listing" = ❌ (WRONG — too broad!)
"FBA → Listing Content" = ❌ (correct, doesn't change words)
"FBA → Listing Ranking" = ✅ (correct, FBA badge improves ranking)

RULE: Always analyze at micro-attribute level before marking ❌
```

## Review/Rating → Ad Prediction
```
Review/Rating data = AI input feature for ad performance prediction
  Rating drops → predict CTR/conversion drop → proactively adjust bids
  Bad reviews → sales drop prediction → FBA stock planning change
  Review themes → keyword relevance assessment
```

---

# 👥 MULTI-ACCOUNT + PARTNER SELLER + USER MANAGEMENT (UPDATED v8.0!)

## Partner Seller Logic
```
Partner seller Buy Box win = OUR win (label seller name only)
Buy Box lost → Alert (not from partner)
Auto-sync partner rules: ON/OFF per platform (default: ON)
Same partner logic on Amazon / Flipkart / Meesho
Configurable: Partner Seller IDs per marketplace
```

## Multi-Account System
```
One login for user — self + partner accounts
One seller can have multiple accounts (same/different marketplace)
First-fill = master (whichever account created first OR filled info first)
Master account data auto-sync to all sub-seller accounts
Each account editable/overridable
Each account = own settings, reports, AI learning
AI learning contributes to software-level (cross-account)
```

## Easy Signup & Approval (UPDATED v8.0!)
```
Staff: Admin adds directly to their account (no self-registration)
Other Sellers: Register on website → Software Super Admin approves
Registration: Only must-have info (name, email, password)
All other details: Update later in Settings
Settings follow UI menu rule: Main / Advanced / Settings
```

## 3-Level Admin Hierarchy (NEW v8.0!)
```
┌─────────────────────────────────────────────────┐
│ LEVEL 1: SOFTWARE SUPER ADMIN 👑                 │
│ ├── GOD mode — across ALL accounts               │
│ ├── Create/delete accounts, approve new sellers   │
│ ├── Access any seller account, override anything  │
│ ├── System-wide configurations                    │
│ └── Can do EVERYTHING in the entire software      │
├─────────────────────────────────────────────────┤
│ LEVEL 2: ACCOUNT ADMIN 🛡️                       │
│ ├── Unlimited admins per account                  │
│ ├── Add/manage staff within their account         │
│ ├── Assign modules, marketplaces, seller accounts │
│ ├── Configure performance weights                 │
│ ├── Approve leaves, manage staff                  │
│ └── Full control within their account boundary    │
├─────────────────────────────────────────────────┤
│ LEVEL 3: USER/STAFF 👤                           │
│ ├── Only assigned modules visible                 │
│ ├── Only assigned seller accounts accessible      │
│ ├── Only assigned marketplaces visible            │
│ ├── Unlimited users per account                   │
│ └── Permission per module: View / Edit / Full Action / No Access │
└─────────────────────────────────────────────────┘
```

## Module-Based Access Control (NEW v8.0!)
```
Each user/staff can be assigned MULTIPLE modules
Permission levels per module: View Only / Edit / Full Action / No Access
Admin assigns: which modules + which seller accounts + which marketplaces

Example:
├── Ravi (Ads Staff)
│   ├── Ads Module: ✅ Full Action
│   ├── Buy Box: 👁️ View Only
│   └── FBA/Settings: ❌ No Access
└── Priya (Pricing Staff)
    ├── Buy Box + Pricing: ✅ Full Action
    └── Ads: 👁️ View Only
```

## Performance Score System (NEW v8.0!)
```
Auto-Calculated Score (out of 100):
├── Tasks completed on time
├── Recommendations acted on
├── Task completion speed (time urgency)
├── Priority tasks done on time
├── New module assigned → auto-includes in performance
├── Any future task type → auto-calculated

30-DAY ROLLING WINDOW:
├── Only last 30 days count
├── Delay stays on account for 30 days → auto-clears
├── Fresh chance every 31st day

VISIBILITY (BOTH admin AND user = RANK ONLY):
├── Score: 75/100
├── Rank: ⭐ Star / 👍 Good / 📊 Average / ⚠️ Needs Improvement
├── Trend: Improving ↑ / Stable → / Declining ↓
├── Call to Action: "Complete 3 pending tasks to improve"
├── Time urgency shown: "1 task due in 30 min ⏰"
├── NO loss/profit attribution — Rank motivates, not blame

WEIGHTS: Admin configurable with sensible defaults
PERFORMANCE TIPS: System recommends what user can do to improve
```

## User Screen Layout (NEW v8.0!)
```
TOP: Pure Work Area
├── Module-based auto tabs/sections (assigned modules only)
├── Focus = work, nothing else

2ND/3RD TAB: Performance (minimal, non-distracting)
├── Score + Rank + Trend
├── Improvement tips (actionable)

BOTTOM BAR (small, always visible):
├── "3 pending | Score: 75 | 1 overdue ⚠️"
├── Motivate to work on time
├── Delay effects on performance shown briefly
```

## User Account Lifecycle (NEW v8.0!)
```
Active → Disabled → Deleted
├── Disabled: Access off, data preserved
├── Admin can delete anytime
├── Auto-delete after 12 months of disabled
├── ⚠️ AI learning data ALWAYS preserved (tagged: "deleted_user")
└── User deletion must NEVER affect AI learning
```

## Leave System (NEW v8.0!)
```
├── 7-day advance leave application → offline time NOT counted
├── No advance leave → offline time COUNTED in performance
├── Emergency: Call admin, admin approves retroactively
```

## Alliance/Staff System (UPDATED v8.0!)
```
Roles: Ads Staff, Pricing Staff, Listing Staff, Supplier, Admin, etc.
Each task/function → assignable to specific role
Each staff → assignable to MULTIPLE modules
Notice/Alert per role (Ads changes → Ads staff, Price → Price staff)
Supplier = role (stock alerts, PO notifications)

Secondary Staff:
├── Enable/Disable per alert type
├── If primary not acknowledged → escalate to secondary
├── Configurable timeout before escalation
```

## Notification System (UPDATED v8.0!)
```
Default channel: Email (login email)
WhatsApp: Optional field (store now, integrate future phase)
Architecture: WhatsApp-ready, build later

Event-Based Configurable:
├── ANY account event can trigger notification
├── Admin configures: which event, priority, who gets notified
├── Not just tasks — Buy Box lost, stock low, ANY event
├── Smart frequency: low performance → more reminders

Acknowledgement = Task Completion:
├── Don't track notification click time
├── Track TASK COMPLETION TIME only
├── Task complete = auto-acknowledged
```

## Audit Trail (NEW v8.0!)
```
Every user action logged: who, when, what
Preserved even after user deletion
Required for performance calculation
Admin can view complete history
```

---

# ⚡ BULK OPERATIONS — UNIVERSAL PATTERN (NEW v8.0!)

```
APPLIES TO EVERY PAGE, EVERY MODULE — no exceptions:

UI Elements:
├── 🔍 Search Bar: Auto-appear if items > 10
├── 🔍 Advanced Filter: Multi-field filter if items > 50
├── ☑️ Select All / Deselect All checkbox
├── ☑️ Individual checkboxes per row
├── 📊 "X of Y selected" counter
├── ⚡ Bulk Action dropdown (context-specific options)
├── 🖱️ One-Click Apply
└── Instant search (filter as you type)

ADMIN BULK OPERATIONS:
├── Assign modules to multiple users
├── Assign seller accounts to multiple users
├── Assign marketplaces to multiple users
├── Bulk enable/disable users
├── Bulk change permissions
└── Bulk approve/reject leaves

EVERYWHERE ELSE:
├── Products → bulk change category/strategy/settings
├── Keywords → bulk approve/reject/negative
├── Buy Box → bulk enable/disable auto-price
├── FBA → bulk set restock rules
├── Alerts → bulk acknowledge
├── Import → bulk validate/import
└── ANY list with multiple items

GOAL: Time-saving, easy, full control — one click for bulk operations
```

---

# 🔔 ADVANCED ALERT SYSTEM (NEW v6.0!)

## 4 Alert Types per Module
```
1. EVENT-BASED: Buy Box lost, stock zero, budget exhausted
2. PERCENTAGE CHANGE: ACoS +10%, Sales -30%, CTR -50%
3. FIXED VALUE CHANGE: CPC > ₹15, Stock < 10, Rating < 3.5
4. TIME-BASED: No sale in 48hrs, No click in 24hrs
```

## Notification Features
```
├── Custom voice per alert type (different sounds)
├── Voice level configurable (low / medium / high / max)
├── Define which alerts are CRITICAL
├── Critical alerts: REPEAT until acknowledged
├── Browser/System notifications
├── Escalation chain:
│   Alert → Primary user → not acknowledged → Secondary staff (if enabled)
```

## Smart Dynamic Scheduling (per module)
```
Normal Schedule (default, configurable)
    ↓ trigger event detected (lost/increase/decrease condition rules)
Escalated Schedule (aggressive monitoring)
    ↓ take action
Action Monitoring (track effect)
    ↓ recovered / stable
Back to Normal Schedule ✅

Examples:
  Buy Box: 30min → lost → 5min → won back → 30min
  Sales: Weekly → lost for ASIN → Daily → recovered → Weekly
  Top ASIN: Daily → sales decreased → 4 hours → stable → Daily
  Stock: Daily → low alert → 2 hours → restocked → Daily

Each module:
├── Own default schedule (sensible defaults set)
├── Trigger conditions defined (lost/increase/decrease)
├── Thresholds configurable by user
├── Escalation schedule configurable
└── User can edit everything
```

## Multi-Contact Support
```
Multiple emails + WhatsApp numbers per account
Per-function contact optional:
├── If filled → use function-specific contact
├── If BLANK → auto-fill from account-level (reduce user work!)
├── Example: Ads alerts → email1, Stock alerts → email2
WhatsApp: Phase 4 (Last Phase) [OFF by default]
```

---

# 🧩 FUTURE-PROOF PLUGIN ARCHITECTURE (NEW v6.0!)

```
Every NEW feature added to the system automatically gets:
├── 3 Automation Modes (Full-Auto / Semi-Auto / Full Approval)
├── Staff/Role Assignment (who manages this feature)
├── Alert/Notice System (4 types + escalation)
├── Google Sheet Integration (input/output via GAS webhook)
├── AI Learning Integration (4-level, per-module brain)
├── Multi-Account Sync Support
├── Smart Dynamic Scheduling (event-based escalation)
├── UI: Main / Advanced / Settings tabs
└── Cross-Module Learning hooks (weight-based)

FUTURE SCOPE (Phase 4+):
├── FBA Automation (rules → auto send to warehouse, PO to supplier)
│   ├── Product/Category → Supplier mapping (contact info)
│   ├── Alert to supplier + Update PO in Google Sheet
├── Listing Optimization Automation
├── ASIN-wise Sales Monitor (time-period based)
├── Supplier PO Management
├── And ANYTHING else — plugin architecture supports any future feature
```

---

# 📥 REPORT IMPORT MODULE (NEW v7.0!)

```
Import existing platform reports for AI training — cold start solved!

SUPPORTED IMPORTS:
├── Amazon Business Reports (sales, traffic, sessions, conversion)
├── Amazon Ads Reports (campaigns, keywords, search terms, placements)
├── Flipkart/Meesho Reports (future)
├── Any CSV/Excel with proper template

OLD DATA TAGGING:
├── data_source: "imported" vs "live_api"
├── data_age: "historical" (before system) vs "current"
├── reliability: "old_strategy" vs "our_strategy"
├── import_date: when imported
├── original_period: actual date range
├── AI BEHAVIOR: Learn patterns YES, copy old strategy NO
├── Old data weight DECREASES over time automatically
├── COMPARE: "Before our system: ACoS 35%" → "After: ACoS 18%"
```

---

# 🏷️ HIGH-WEIGHT TAGS (NEW v7.0!)

```
7 Auto-Calculated Tags (not CORE levels, but high influence):

1. RATING BAND         Source: Customer Feedback API (auto)
   excellent (4.5+) / good (4.0-4.4) / average (3.5-3.9) / poor (<3.5)

2. COMPETITION DENSITY  Source: Ads Reporting v3 + Brand Analytics (auto)
   ⚠️ Search Term level, NOT ASIN seller count (99% sole seller = irrelevant)
   Based on: Impression Share + Click Share + CPC trend (aggregated across campaigns)

3. PRODUCT LIFECYCLE    Source: System calculates age + trend (auto)
   launch / growth / mature / declining

4. FULFILLMENT TYPE     Source: SP-API Inventory (auto)
   fba / self_ship / mixed

5. SEASONALITY          Source: Manual initially → Prophet learns (auto over time)
   year_round / winter / summer / monsoon

6. SALES VELOCITY       Source: 7-day rolling avg from orders (auto)
   top_seller (>10/day) / steady (3-10) / slow (1-3) / dead_stock (<1)

7. MARKETPLACE          Source: Account config (auto)
   amazon_in / flipkart / meesho

LEARNING MATCH: More tags match = HIGHER confidence
  Core match: Category + Price Segment → base match
  Tag match: +Rating +Fulfillment +Competition → deeper match
  All match: highest confidence → strongest recommendation
```

---

# 📊 ORGANIC COMPETITION MEASUREMENT (NEW v7.0!)

```
API SOURCES (✅ Available!):
├── Search Catalog Performance Report (GET_BRAND_ANALYTICS_SEARCH_CATALOG_PERFORMANCE_REPORT)
│   ├── Impressions per ASIN per search term ✅
│   ├── Clicks per ASIN per search term ✅
│   ├── Cart Adds per ASIN per search term ✅
│   ├── Purchases per ASIN per search term ✅
│   ├── Periods: WEEK / MONTH / QUARTER
│   └── Requires: Brand Registered ✅ (we are!)
│
├── Sales & Traffic Report (GET_SALES_AND_TRAFFIC_REPORT)
│   ├── Page Views per ASIN per date ✅
│   ├── Sessions per ASIN per date ✅
│   ├── Buy Box % per ASIN ✅
│   ├── Conversion Rate per ASIN ✅
│   └── Lookback: 30 days, refresh 72hrs
│
├── Brand Analytics — Top Search Terms
│   ├── Top 3 clicked ASINs per search term ✅
│   ├── Click share + Conversion share ✅
│   └── Requires: Brand Registered ✅
│
├── Manual Rank (Google Sheet / Excel upload)
│   └── ASIN | Keyword | Rank | Date

ORGANIC COMPETITION SCORE FORMULA:
  IF Search Catalog available:
    organic_impression_share × 0.25 + organic_ctr × 0.15 + organic_conversion × 0.15
  + IF Brand Analytics available:
    ba_click_share_rank × 0.15
  + ALWAYS:
    tacos_trend × 0.10 + bsr_trend × 0.10
  + IF Manual Rank available:
    organic_rank_position × 0.10
  = Score (weights auto-normalize based on available sources)
  
  AI learns over time → which source predicts best → weight auto-adjusts
```

---

# 📥 UNIVERSAL IMPORT SYSTEM (NEW v7.0!)

```
RULE: EVERY data import in the system = 2 options ALWAYS

OPTION 1: Excel/CSV Upload
├── Downloadable template from website
├── Column mapping saved after first setup
├── System recommends frequency per data type

OPTION 2: Google Sheet Link (Auto-Sync)
├── Sheet ID + Tab Name + Column Mapping
├── GAS Webhook auto-sync
├── Default frequency set, user can change

TEMPLATE SYSTEM:
├── Row A1: REPORT_ID (auto-detect data type)
│   "RPT_ORGANIC_RANK_V1", "RPT_BSR_V1", "RPT_KEYWORDS_V1", etc.
├── Row 2: Column headers (auto-map to system fields)
├── Row 3+: Data
├── Missing columns → NULL (no error, no block)
├── Extra columns → ignored
├── Data validation: ASIN format, date parseable, numbers are numbers
├── Invalid rows → flagged, not imported, shown to user

DEDUP RULES (ALWAYS, per type):
├── Organic Rank: ASIN + Keyword + Date + Marketplace → UPDATE rank
├── BSR: ASIN + Category + Date + Marketplace → UPDATE BSR
├── Business Report: ASIN + Date → UPDATE metrics
├── Ads Report: Date + Campaign + Keyword + Match → UPDATE metrics
├── Keywords: ASIN + Keyword + Match Type → SKIP
├── Competitor: Our ASIN + Competitor ASIN + Date → UPDATE
├── COGS: ASIN → UPDATE (latest = current cost)
├── Supplier: Supplier Name + Product → UPDATE

PHASE 1 GOOGLE SHEET SETUP:
  1. Download template from website
  2. Import to Google Sheets (File → Import)
  3. Link Sheet ID + Tab in our system
  4. Auto-sync via GAS Webhook
```

---

# 📋 COMPLETE FEATURE REGISTRY (216 Features)

## CATEGORY 1: 🔵 CORE ENGINE (28 Features)

| # | Feature | Description | Priority | Phase |
|---|---------|-------------|----------|-------|
| C01 | OAuth2 Auth Module | Token refresh, caching, auto-rotate | ✅ EXISTS | Done |
| C02 | Data Pull Engine (Ads API v1 Unified) | Campaigns, keywords, ad groups, targets via v1 Unified API | P1 | 1 |
| C03 | Search Term Report Fetcher | Ads Reporting API v3, daily pull | P1 | 1 |
| C04 | Campaign Performance Report | Ads Reporting API v3, daily metrics per campaign | P1 | 1 |
| C05 | Placement Report Fetcher | Top of Search vs Product Page vs Rest (Reporting v3) | P1 | 1 |
| C06 | History Storage (CSV/DB) | Daily snapshots, searchable | P1 | 1 |
| C07 | Changelog Tracker | Every change: before/after/reason/effect/tags | P1 | 1 |
| C08 | True Profit Calculator | Per-product: COGS, fees, GST, returns, shipping fee | P1 | 1 |
| C09 | Dynamic COGS Updater | Raw material price change → auto-adjust targets | P2 | 2 |
| C10 | Break-even ACoS Calculator | Max ACoS where still profitable per product | P1 | 1 |
| C11 | Smart Bid Ceiling | Max profitable bid = profit × conversion rate | P1 | 1 |
| C12 | Negative Keyword Engine | Auto-detect waste terms from search reports **(ENHANCED v10.0):** Cross-campaign cannibalization detection + negative keyword conflict check across campaigns | P1 | 1 |
| C13 | Keyword Lifecycle Manager | Discovery→Testing→Proven→Star→Declining→Retired | P1 | 2 |
| C14 | Campaign Structure Manager | Create/edit campaigns via Ads API v1 Unified | P1 | 2 |
| C15 | Bid Optimizer Engine | Rule-based + profit-based bid adjustments **(ENHANCED v10.0):** Impression Share cap + new campaign learning mode (<14d = conservative) | P1 | 1 |
| C16 | Budget Manager | Calendar + salary cycle + festival multipliers | P1 | 1 |
| C17 | Dayparting + Bid Schedule Engine | AI-learned per-ASIN heatmap **Day+Hour combination**, not fixed hours | P2 | 2 | ← ENHANCED v9.0! |
| C18 | Placement Modifier Engine | TOS vs Product Pages analysis + auto-optimize. **Dynamic modifiers per campaign/product, AI learns best placement** | P2 | 2 | ← ENHANCED v9.0! |
| C19 | Multi-Funnel Campaign System | Auto→Phrase→Exact funnel (selectable per product) | P1 | 2 |
| C20 | Direct Keyword Campaign System | Amazon suggestion → Phrase → Exact (Msir method) | P1 | 1 |
| C21 | Product Strategy Modes | Extra Aggressive/Aggressive/Average/Profitable/Survival/Auto | P1 | 1 |
| C22 | 3-Level Account Settings | Account → Category (optional) → Product inheritance | P1 | 1 |
| C23 | Product-Level Overrides | Per-product settings override category/account | P1 | 1 |
| C24 | Cooling Period System (Dual) | Days OR Budget whichever first (Low: 10d/₹500, High: 12d/100%) | P1 | 1 |
| C25 | Campaign Exclusion (Time-Based) | Exclude campaigns for X days, auto re-enter | P1 | 1 |
| C26 | Category Template System | Category-level cost defaults, product inherits/overrides | P1 | 1 |
| C27 | Shipping Fee Tracker | Per-product shipping fee (not weight — fee changes) | P1 | 1 |
| C28 | Marketplace Adapter Engine | Reusable core + marketplace-specific adapters | P1 | 1 |

## CATEGORY 2: 🧠 AI INTELLIGENCE LAYER (34 Features)

| # | Feature | Description | Priority | Phase |
|---|---------|-------------|----------|-------|
| I01 | IQ Score Engine (Backend) | 0-100 score for every recommendation | P1 | 1 |
| I02 | User-Friendly Labels | "Strong Recommend & Approved" etc. (from IQ) | P1 | 1 |
| I03 | Strategy Learning Database | What worked/failed → knowledge base per keyword | P1 | 2 |
| I04 | Data Confidence Scoring | Low data (8 clicks) → don't act aggressively | P1 | 1 |
| I05 | Post-Change Response Monitor | Observe → Analyze → Continue/Reverse/New Strategy **(ENHANCED v10.0):** Auto-Rollback trigger — monitor 48-72hrs, auto-revert if worse | P1 | 2 |
| I06 | Predictive Sales Modeling (Prophet 1.3.0) | Based on history, predict next week performance | P2 | 2 |
| I07 | "What If" Simulator | "If bid +10%, what happens?" → predict before action | P2 | 3 |
| I08 | Intent-Based Keyword Engine | Buying/Research/Problem intent → budget allocation | P2 | 2 |
| I09 | LLM Insight Layer (Gemini 2.5 Flash) | Human-language explanations, optional if API key exists | P2 | 3 |
| I10 | Auto A/B Testing Engine | Try multi methods, keep winning one, auto-rotate | P2 | 2 |
| I11 | Per-Keyword Learning | Individual keyword performance patterns over time | P1 | 2 |
| I12 | Per-Campaign Learning | Campaign-level optimization patterns | P1 | 2 |
| I13 | Per-Account Learning | Account-wide behavior patterns | P2 | 3 |
| I14 | Per-Price-Segment Learning | How different price ranges behave differently | P2 | 3 |
| I15 | Smart % Calculator | Bid/budget change % based on ALL factors dynamically | P1 | 1 |
| I16 | Profit-Based Waste Detection | Not fixed clicks — calculate waste based on bid × profit | P1 | 1 |
| I17 | Slowly Reduce Bids (Not Hard Block) | Gradually reduce bids on bad terms instead of instant block | P1 | 1 |
| I18 | Seasonal Demand Predictor (Prophet 1.3.0) | Winter→immunity, Summer→hydration auto-keyword priority. **Festival prep integration. 30-day advance prediction. Default DISABLED until festival** | P2 | 2 | ← ENHANCED v9.0! |
| I19 | Category Benchmark Engine (LightGBM 4.6.0) | Your ACoS/CTR vs market average → context | P2 | 3 |
| I20 | Returns Velocity Impact | High return **keywords** → lower IQ score even if ACoS good. (Keyword-level. For product-level see I32) | P2 | 2 | ← NOTE v9.0! |
| I21 | AI Recommendation Field | 3-column: Your Value / AI Recommends / Last Effect | P1 | 1 |
| I22 | Decision Multi-Tag System | Every decision tagged with layers + source + confidence | P1 | 1 |
| I23 | Permanent Rule Maker | Proven rules auto-saved, applied next time directly **(ENHANCED v10.0):** AI Logic Recommender — finds patterns, recommends new rules | P1 | 2 |
| I24 | Cross-Product Learner | Apply learnings from product A to similar product B | P2 | 2 |
| I25 | 4-Level AI Learning Engine | Software→Category→Product→Keyword learning hierarchy. 3 core + extensible (Keyword/Account/Supplier). Marketplace tag mandatory. IQ Score per level. **(ENHANCED v10.0):** Learning Tag System {category, marketplace, price_segment} + Decay | P1 | 1 | ← NEW v6.0! |
| I26 | Per-Module AI Brain | Each module (Ads/FBA/Sales/BuyBox/Listing/Review/Supplier) has own dedicated AI learning brain. All feed into 4-level system. | P1 | 2 | ← NEW v6.0! |
| I27 | Cross-Module Learning Engine | Weight-based (Tier 1-4). Default=PASS, exclude only 100% sure. Micro-attribute level analysis. Self-learning weights. Tier promotion/demotion. | P1 | 2 | ← NEW v6.0! |
| I28 | Review → Ad Prediction | Review/Rating as AI input feature for ad performance prediction. Rating drops → predict CTR/conversion drop → proactive bid adjust. | P2 | 2 | ← NEW v6.0! |
| I29 | Supplier Performance Scorer | Score suppliers: delivery time, quality (return rate), reliability, price consistency. Connected to product returns/reviews. | P2 | 3 | ← NEW v9.0! |
| I30 | Product Health Score (Master) | Single 0-100 per PRODUCT: sales velocity + profitability + review health + listing quality + ad efficiency + stock. Priority dashboard for 300+ products. | P1 | 2 | ← NEW v9.0! |
| I31 | Anomaly Detection 3-Level | Product + Account + Campaign level anomaly detection. CPC spikes, click variance, order anomalies. Broader than P01/P02 (specific). | P1 | 2 | ← NEW v9.0! |
| I32 | Return Rate Analyzer + Auto-Action | Product-level return monitoring → threshold → auto-reduce ad spend + root cause (Customer Feedback API). Different from I20 (keyword-level). | P2 | 2 | ← NEW v9.0! |
| I33 | AI Action History + Feedback + Revert | Every AI action logged. User rates 1-5 star. Revert option. Learns from ratings. (NEW v10.0) | TBD |
| I34 | Predictive Customer Segmentation | Retail vs Business customer. Price sensitivity analysis. (NEW v10.0) | TBD |

## CATEGORY 3: 🛡️ PROTECTION & COMPLIANCE (18 Features)

| # | Feature | Description | Priority | Phase |
|---|---------|-------------|----------|-------|
| P01 | Budget Spike Protection | Daily spend > 150% budget → emergency pause | P1 | 1 |
| P02 | CPC Spike Detection (Bidding War Shield) | CPC suddenly 3x → pause/reduce, resume when normal | P1 | 2 |
| P03 | API Error Fallback | If API fails → no changes, alert user | P1 | 1 |
| P04 | Stock-Out Ads Pause | Low stock → Option A: reduce to Profitable mode **(ENHANCED v10.0):** Campaign Resume Logic — old bid? new? slow ramp-up? (GAP-8) | P1 | 2 |
| P05 | Inventory Velocity Pacing | Stock for 10 days, restock in 15 → slow down ads | P2 | 2 |
| P06 | Stock-Low Auto Price Update (SP-API) | Option B: Auto update price via SP-API when stock low | P2 | 2 |
| P07 | Buy Box Monitor & Auto-Price Recovery | Lost Buy Box → configurable bid reduction + auto price decrease (default 5%/30min) + recheck + alert + min floor **(ENHANCED v10.0):** Anti-loop: max attempts, cooldown, competitor price floor | P1 | 2 |
| P08 | Listing Suppression Alert | Suppressed listing → pause ads + alert | P1 | 2 |
| P09 | Review Score Drop Brake | Rating < 3.5★ → reduce bids 30% (via Customer Feedback API v2024-06-01) | P1 | 2 |
| P10 | Negative Review Ad Brake | 100% auto: negative ratio + 1★ spike + themes + Gemini refinement (NO manual, NO ACR API, NO keyword tracking) **(ENHANCED v10.0):** Theme severity: quality=med(40%), health=high(60%), packaging=low(20%) | P1 | 2 |
| P11 | Banned/Medical Claim Shield | Block keywords with compliance risks (cures, guaranteed) | P1 | 2 |
| P12 | Compliance Dictionary | Dynamic dictionary of Amazon health policy restricted words | P2 | 3 |
| P13 | Daily Cashflow Guardian | Monthly budget pacing — don't exhaust in 10 days | P1 | 1 |
| P14 | Cash-Flow Sync (Payout-Based) | "Never spend > 15% of weekly Amazon payout" option | P2 | 3 |
| P15 | Survival Mode | Only high-conversion keywords, strict waste blocking | P1 | 1 |
| P16 | Profit-per-Price Tracker | Track profit/day at each price point → find optimal price | P1 | 2 |
| P17 | Profit % Cap System | Account-level + Product-level cap: "Spend max X% of true profit on ads." Different from P14 (payout-based). True profit calculation. | P1 | 2 | ← NEW v9.0! |
| P18 | Image Quality & Compliance Checker | Auto-check: image count, resolution, white background, infographic presence, Amazon compliance. Alert on issues. | P2 | 2 | ← NEW v9.0! |

## CATEGORY 4: 🎯 COMPETITOR & MARKET INTELLIGENCE (12 Features)

| # | Feature | Description | Priority | Phase |
|---|---------|-------------|----------|-------|
| M01 | Competitor Price Monitor | Daily price tracking of top 5 competitors + **price war pattern detection + auto-protect alert trigger** | P2 | 2 | ← ENHANCED v9.0! |
| M02 | Competitor Stock Monitor | Out of stock detection → grab their traffic | P2 | 2 |
| M03 | Competitor ASIN Targeting | Target competitor product pages with lower ratings. **Data-driven selection: AI learns best targets from conversion data** | P2 | 2 | ← ENHANCED v9.0! |
| M04 | Market Keyword Gap Finder | 4-approach composite (Search Term Reverse + Category Discovery + Amazon Suggestions + Brand Analytics) — NO automation, recommend only, user approval required for every keyword action **(ENHANCED v10.0):** Keyword scoring: SearchVol × Relevance × ConvPotential | P3 | 3 |
| M05 | Dynamic Pricing Intelligence | Price-Ad synergy analysis (price drop = better ACoS) | P3 | 3 |
| M06 | "David vs Goliath" Sniper Mode | Long-tail low-competition keywords big brands ignore | P2 | 2 |
| M07 | Category Benchmark Dashboard | Your metrics vs category average | P3 | 3 |
| M08 | Sole Seller Detection | If only seller for ASIN → reduce/skip ads (why pay?) | P1 | 2 |
| M09 | BSR Trend Tracker | Primary: Manual sheet (ASIN|BSR|DATE), Fallback: SP-API Catalog salesRanks, Support: sales/traffic/CTR data. Keepa REMOVED. **(ENHANCED v10.0):** Signal fusion: BSR(50%) + Sales(25%) + Traffic(15%) + CTR(10%) | P3 | 3 |
| M10 | Impression Share Tracker | Visibility % per keyword → are we visible enough? | P2 | 2 |
| M11 | Competitor Launch Alert | Detect new competitor in your keywords/category → alert before ranking impact. Opposite of M02 (stock-out detection). | P2 | 2 | ← NEW v9.0! |
| M12 | Competitive Budget Intelligence | Monthly budget recommendation: ROAS trend, market opportunity, seasonal, profit headroom. Optimal budget calculator. (NEW v10.0) | TBD |

## CATEGORY 5: 📈 ORGANIC & GROWTH ENGINE (19 Features)

| # | Feature | Description | Priority | Phase |
|---|---------|-------------|----------|-------|
| G01 | TACoS Tracker | Total ACoS (organic + paid) — true health metric | P1 | 1 |
| G02 | Organic Flywheel Detector | Ads → Sales → Rank → Free sales → Less ads needed | P2 | 2 |
| G03 | Organic Rank Phase Detection | Launch/Traction/Momentum/Dominance/Defend phases | P2 | 2 |
| G04 | Auto-Scaling Winners Engine | Star keyword → duplicate campaign + increase budget + expand | P2 | 2 |
| G05 | Subscribe & Save Optimizer | Subscriber keywords → higher LTV → can bid more | P3 | 3 |
| G06 | Bundle/Cross-Sell Intelligence | Products bought together → suggest virtual bundles | P3 | 3 |
| G07 | Virtual Bundle Market Basket | Track co-purchase patterns → AOV increase suggestions | P3 | 3 |
| G08 | New Product Launch Autopilot | Automated 30-day launch sequence (configurable). **Auto Deal/Coupon creation on launch for visibility boost** **(ENHANCED v10.0):** New Product Initial Strategy — initial bid/budget/keyword logic | P2 | 2 | ← ENHANCED v9.0! |
| G09 | New Listing Auto-Campaign | New ASIN detected → auto create optimized campaign in set mode. **(W10 merged here — single source for new ASIN automation)** | P2 | 2 | ← ENHANCED v9.0! |
| G10 | Review Impact Tracker | Rating change → conversion impact → bid adjustment (via Customer Feedback API weekly snapshots, store trend locally) | P2 | 2 |
| G11 | Trust Score System | Review count velocity + rating consistency scoring | P3 | 3 |
| G12 | Listing Conversion AI Advisor | CTR low → "image problem" / Clicks high 0 sales → "price/title" | P2 | 2 |
| G13 | Repeat Purchase Tracker | Track customer reorder patterns per product → predict reorder timing → optimize ads for LTV. Different from G05 (S&S specific). | P2 | 2 | ← NEW v9.0! |
| G14 | Listing Health Score | Single 0-100 score per listing: images + keywords + A+ + description + compliance. Quick view across 300+ products. | P1 | 2 | ← NEW v9.0! |
| G15 | A+ Content Impact Tracker | Measure A+ content effect on conversion → before/after comparison → justify A+ investment. | P2 | 3 | ← NEW v9.0! |
| G16 | Smart Pricing / Repricing Engine (MODULE) | Auto price test. Increase if good CTR+reviews+conversion. Test profit impact. (NEW v10.0) | TBD |
| G17 | FBA Management Module | FBA shipment automation. Purchase order gen. Supplier mapping. (NEW v10.0) | TBD |
| G18 | Purchase & Supply Chain Automation | Product↔Supplier mapping. Sales velocity→auto reorder. Google Sheet gen. (NEW v10.0) | TBD |
| G19 | A+ Content Management Module | A+ optimization. Impact tracking. Before/after. (NEW v10.0) | TBD |

## CATEGORY 6: 🏥 HEALTHCARE SPECIFIC (11 Features)

| # | Feature | Description | Priority | Phase |
|---|---------|-------------|----------|-------|
| H01 | Seasonal Health Demand Engine | Winter→immunity, Summer→hydration, Monsoon→infection. **Default DISABLED. Requires approval before each festival activation. Monitor ROI post-activation** | P1 | 2 | ← ENHANCED v9.0! |
| H02 | Symptom/Ingredient Keyword Miner | Product ingredients → adjacent health search terms | P2 | 3 |
| H03 | Dietary Cross-Pollination Matrix | Lactose-free, sugar-free, plant-based → new keyword clusters | P3 | 3 |
| H04 | Problem→Solution Keyword Engine | "gas issue" → target "natural digestion remedy" | P2 | 2 |
| H05 | Ayurvedic Keyword Intelligence | Traditional terms + Hindi health keywords mining | P2 | 2 |
| H06 | "Easy Win" Low-Competition Finder | Hidden gem keywords big brands ignore in health niche | P2 | 2 |
| H07 | Health Compliance Auto-Guard | Block restricted medical claims from campaigns | P1 | 2 |
| H08 | FBA Deadstock/Overstock Detector | Overstock → push to Aggressive mode to sell before expiry. **+ Review analysis + price adjustment recommendation + auto-campaign escalation** | P2 | 3 | ← ENHANCED v9.0! |
| H09 | Shelf-Life Aware Optimization | Products expiring soon → aggressive clearance mode. **Integrates with H08 for combined deadstock+expiry intelligence** | P3 | 3 | ← ENHANCED v9.0! |
| H10 | Condition-Based Ad Copy Suggestions | Suggest ad angles based on health conditions/seasons | P3 | 3 |
| H11 | Long-Term Storage Fee Avoidance | Predict WHEN FBA storage fees hit per product → alert + auto-action before fees. Different from H08 (quantity-based). | P2 | 2 | ← NEW v9.0! |

## CATEGORY 7: 📊 REPORTING & UI (18 Features)

| # | Feature | Description | Priority | Phase |
|---|---------|-------------|----------|-------|
| R01 | Daily Excel Report (Multi-Tab) | Report tabs (read) + Action tabs (tool reads back) **(ENHANCED v10.0):** Only insights/impact + Net Profit integration + Export design | P1 | 1 |
| R02 | Action Tabs with Dropdowns | Approve/Reject/Skip/Custom for every recommendation | P1 | 1 |
| R03 | IQ-Based Auto-Fill | All recommendations pre-approved based on IQ score | P1 | 1 |
| R04 | Strategy Impact Tab | What done → Effect → IQ → Next action (auto-filled) | P1 | 1 |
| R05 | "Money Saved" Counter | Daily/weekly/monthly savings from waste blocking | P1 | 1 |
| R06 | Day-to-Day Comparison | Color coded ↑↓ with % change | P1 | 1 |
| R07 | Week-to-Week Comparison | Weekly trends and patterns | P1 | 1 |
| R08 | Predicted vs Actual Tracker | What system predicted → what really happened | P2 | 3 |
| R09 | Child-Simple Language | "Keyword making ₹500 profit" not "ACoS 12%" | P1 | 1 |
| R10 | Multi-Account/Agency Mode | Client-wise reporting, white-label Excel | P3 | 4 |
| R11 | Web Dashboard (Strategy Impact Center) | NOT Amazon copy — shows strategy effects, actions needed | P2 | 2 |
| R12 | Full Transparency (Not Black Box) | Every decision: WHAT + WHY + EVIDENCE + RISK + LAYER TAGS | P1 | 1 |
| R13 | User Trust Score Input (Excel/Sheet) | ASIN, reviews, rating input for trust analysis | P3 | 3 |
| R14 | Placement Modifier Recommendations | TOS vs Product Pages auto-analysis column in report | P2 | 2 |
| R15 | Conversion Improvement Suggestions | Based on CTR/CR: improve title, image, review, price | P2 | 2 |
| R16 | Weekly AI Summary Report | Compiled weekly intelligence: all actions taken, auto-approved effects, call to action with reasons. Actionable insights digest. | P2 | 2 | ← NEW v9.0! |
| R17 | Net Profit Dashboard | ONE number: "Today Net Profit: ₹X". Revenue-COGS-Ads-Fees-Returns-GST=NET. Trend+goal. (NEW v10.0) | TBD |
| R18 | Per-Feature ROI Tracking | Per feature: actions, outcomes, ₹ saved/earned. Auto-suggest disable poor. (NEW v10.0, TODO-4) | TBD |

## CATEGORY 8: 🔔 ALERTS & NOTIFICATIONS (14 Features)

| # | Feature | Description | Priority | Phase |
|---|---------|-------------|----------|-------|
| A01 | Priority Alert Engine | P1=urgent/money loss, P2=important, P3=insight **(ENHANCED v10.0):** Priority scoring: Impact(40%)+Urgency(30%)+Confidence(20%)+UserPref(10%) | P1 | 1 |
| A02 | Email Alerts (Multi-Recipient) | Daily/Critical/Weekly/Monthly to different emails | P1 | 1 |
| A03 | Excel Attachment in Email | Full report attached to daily email | P1 | 1 |
| A04 | Mac Auto-Open Report | Cron/launchd opens Excel at set time | P1 | 1 |
| A05 | WhatsApp Summary (India Advantage) | Key metrics + important alerts on WhatsApp | P3 | **4** | ← MOVED to Last Phase v6.0! |
| A06 | WhatsApp Quick Commands | Reply "Approve all" / "Pause campaign X" | P3 | **4** |
| A07 | Smart Notification Content | Context-aware, human-friendly messages | P2 | 2 |
| A08 | Auto-Action on No Response | If no report returned in X hours → auto-apply strong recs | P2 | 2 |
| A09 | Browser Push Notifications | Web panel open → browser popup for real-time alerts | P2 | 2 |
| A10 | OS Desktop Notifications | Python plyer/osascript → system notification even browser closed | P2 | 2 |
| A11 | Advanced Alert Notification | Custom voice per alert type, configurable volume, critical alerts repeat until acknowledged. Browser/System based. | P2 | 2 | ← NEW v6.0! |
| A12 | Alert Escalation Chain | Primary user → not acknowledged → secondary staff/user/supplier. Secondary staff enable/disable per alert type. | P2 | 2 | ← NEW v6.0! |
| A13 | 4-Type Alert Engine | Event-based + % Change + Fixed Value Change + Time-based alerts per module. **Preset: Sales drop >50% in 24hrs → P1 alert (Sales Velocity Alert)** **(ENHANCED v10.0):** Intraday Sales Comparison + Alert Fatigue Prevention | P1 | 2 | ← ENHANCED v9.0! |
| A14 | Smart Dynamic Scheduling | Event-triggered escalation per module. Normal→trigger→escalated→action→recovered→normal. Condition rules (lost/increase/decrease) configurable. | P1 | 2 | ← NEW v6.0! |

## CATEGORY 9: ⚙️ AUTOMATION & WORKFLOW (13 Features)

| # | Feature | Description | Priority | Phase |
|---|---------|-------------|----------|-------|
| W01 | 3-Mode Action Engine (CORRECTED) | Manual / Semi-Auto (strong+weak auto, ask only uncertain/risky) / Full-Auto | P1 | 1 |
| W02 | Approval Excel Processor | Read returned Excel → execute approved actions | P1 | 1 |
| W03 | One-Click Daily Pipeline | Single command runs entire system | P1 | 1 |
| W04 | Automated A/B Testing | Try multi methods, measure, keep winner | P2 | 2 |
| W05 | Auto Budget Redistribution | Move money from losers → winners automatically. **ROAS + TACoS weighted scoring. Modes: Proportional / Winner-takes-all / Threshold. Min floor per campaign. Respects P17 profit cap** | P2 | 2 | ← ENHANCED v9.0! |
| W06 | Scheduled Optimization Runs | Morning data pull + analysis + report generation | P1 | 1 |
| W07 | Funnel Auto-Management | Auto promote keywords through funnel stages | P2 | 2 |
| W08 | Smart Rollback System | One-click undo any change / batch of changes | P2 | 2 |
| W09 | Batch Operations | Apply same action to multiple keywords/campaigns | P2 | 2 |
| W10 | ~~Auto Campaign Creator~~ | **→ See G09.** Merged into G09 (New Listing Auto-Campaign). W10 retained as redirect only. | — | — | ← CLEANUP v9.0! |
| W11 | Dead Campaign Auto-Cleanup | AI auto-detect zero-sale campaigns past threshold → auto-pause/archive/cleanup. Different from C25 (manual exclude). | P2 | 2 | ← NEW v9.0! |
| W12 | Non-Performing Listing Smart Engine | No order in X days (user OR AI defined) → auto-diagnose: Buy Box? Stock? Listing? Price? Reviews? Ads? → trigger relevant existing features. | P1 | 2 | ← NEW v9.0! |
| W13 | Custom Rule Builder | Visual "If THIS→do THIS, else THAT" pipeline. User creates own rules. (NEW v10.0) | TBD |

## CATEGORY 10: 🔌 INTEGRATION & EXTENSIBILITY (19 Features)

| # | Feature | Description | Priority | Phase |
|---|---------|-------------|----------|-------|
| E01 | JSON Config System (3-Level) | Account → Category → Product inheritance, no hardcoding | P1 | 1 |
| E02 | Web Config Panel (Flask 3.1.3) | localhost + server same code, 10 pages, 30+ tabs **(ENHANCED v10.0):** Feature Categorization by business function + Smart Search + Views (TODO-3) | P2 | 2 |
| E03 | Webhook System | HTTP POST endpoint for external tools to push keywords | P2 | 2 |
| E04 | Google Sheets Integration (GAS Webhook) | Auto-fetch keywords via GAS webhook (NO OAuth). Per-feature Sheet ID/Tab/Columns configurable. Default Sheet ID fallback. Tab+Columns always required. | P2 | 2 |
| E05 | Extension/Plugin Module System | **Future-proof:** Every new feature auto-gets 3 automation modes, staff assignment, alerts, sheet integration, AI learning, multi-account sync, smart scheduling. FBA automation, listing automation, ASIN sales monitor, supplier PO — all pluggable. | P3 | 4 | ← ENHANCED v6.0! |
| E06 | Multi-Account Support | **One login for user** — self + partner accounts. First-fill = master, auto-sync to sub-accounts, each editable. One seller can have multiple accounts (same/different marketplace). **(ENHANCED v10.0):** First-Fill Master Sync — first account=MASTER, subs inherit | P3 | 4 | ← ENHANCED v6.0! |
| E07 | White-Label Reports | Custom branding on Excel reports (agency mode) | P3 | 4 |
| E08 | SP-API Full Integration | Inventory, orders (v2026-01-01), pricing (v2022-05-01), listings, returns, feedback (v2024-06-01), notifications via SP-API | P1 | 2 |
| E09 | Ads ↔ Seller Cross-Communication | Ads engine + Seller engine share data for joint decisions | P1 | 2 |
| E10 | Multi-Marketplace Support | Amazon now + Flipkart/Meesho future (adapter pattern). Same partner logic all platforms. | P1 | 1 | ← ENHANCED v6.0! |
| E11 | Partner Seller Logic | Partner Buy Box win = OUR win (label seller name). Alert on lost. Auto-sync ON/OFF per platform. Same logic Amazon/Flipkart/Meesho. | P2 | 2 | ← NEW v6.0! |
| E12 | Alliance/Staff System | Role-based access (Ads Staff, Pricing Staff, Listing Staff, Supplier, Admin). Per-task alerts. Secondary staff enable/disable. | P3 | 3 | ← NEW v6.0! |
| E13 | Easy Signup/Onboarding | Only must-have info at registration. Rest updatable in Settings. Settings follow Main/Advanced/Settings UI rule. | P2 | 2 | ← NEW v6.0! |
| E14 | Multi-Contact Support | Multiple emails + WhatsApp numbers. Per-function contact optional (blank = account auto-fill). | P2 | 2 | ← NEW v6.0! |
| E15 | Report Import Module | Import platform CSV/Excel reports. Tag as old data. AI learns with awareness. Cold start solved. Weight decreases over time. Compare before/after. | P1 | 1 | ← NEW v7.0! |
| E16 | Universal Import System | Every data import = 2 options (Excel/CSV + Google Sheet). Template with REPORT_ID in A1. Auto-detect + auto-map. Dedup always. Validation. Preview. | P1 | 1 | ← NEW v7.0! |
| E17 | Organic Competition Engine | Search Catalog Performance (impressions/clicks/cart/purchases) + Sales & Traffic (page views/sessions) + Brand Analytics + manual rank. Weight-based score formula. | P2 | 2 | ← NEW v7.0! |
| E18 | Universal Search (UI) | Top search for all features/data/settings. Page search + filter + sort. (NEW v10.0) | TBD |
| E19 | Onboarding / First-Run Wizard | Step-by-step: API→import→category→targets→first run. 300+ products. (NEW v10.0, GAP-27) | TBD |

## CATEGORY 11: 🔑 KEYWORD SOURCE MODES & TOOLS (10 Features — v10.0 UPDATED!)

| # | Feature | Description | Priority | Phase |
|---|---------|-------------|----------|-------|
| K01 | Mode A: Amazon API Smart Campaign | AI uses Search Term Report + API keyword recs (default ON) | P1 | 1 |
| K02 | Mode B: Google Sheet/CSV Keywords | User researched keywords, match type by word count logic | P1 | 1 |
| K03 | Mode C: Product Benefit Targeting | AI targets related problems, brands, ingredients (default OFF) | P2 | 2 |
| K04 | Smart Match Type Engine | 1-2 words→Phrase, 3+ words→Exact (when match_type empty) | P1 | 1 |
| K05 | Multi-Mode A/B Testing | Run all modes → compare → keep winner OR run all always | P2 | 2 |
| K06 | Amazon Keyword Fetcher | ASIN/seed keyword → Ads API v1 suggestions → SQLite → Sheet. Input Sheet (status NEW or empty). Schedule configurable. | P2 | 2 |
| K07 | Keyword → Listing Optimizer | Compare fetched keywords vs current listing (SP-API Catalog) → find missing → recommend/draft/auto-apply (configurable). **Covers: Title + Description + Bullet Points/Features + Backend Keywords + all input fields.** Output: Sheet + Web Panel. | P2 | 3 | ← ENHANCED v9.0! |
| K08 | Keyword → Product Opportunity Finder | Cluster analysis across all fetched keywords → find product gaps → Gemini 2.5 Flash insight → push to Sheet. | P3 | 3 |
| K09 | Match Type Migration Engine | AI analyzes existing keywords with historical data → detect wrong match type → recommend migration. Different from K04 (creation-time) and C19 (funnel-based). | P2 | 2 | ← NEW v9.0! |
| K10 | Search Term Graduation Pipeline | Unified: Auto discover→phrase test→exact graduate→auto negative. (NEW v10.0, GAP-10) | TBD |

---

# 🏗️ CATEGORY 12: INFRASTRUCTURE & SAFETY (NEW v10.0)
**Feature Count:** 20 | **Purpose:** Foundation infrastructure, safety nets, orchestration

| ID | Feature Name | Description | Phase |
|----|-------------|-------------|-------|
| S01 | Central Decision Orchestrator | Collects all feature outputs, detects conflicts, resolves using priority+risk+confidence, outputs single FINAL action queue. Logs WHY. (from TODO-1, GAP-1) | TBD |
| S02 | Central Task Scheduler | Unified scheduler for ALL features. register_task, pause, run_now, smart_batching, dependency_check, failure_retry, web_panel_config. (GAP-2) | TBD |
| S03 | Cross-Feature Event Bus | Pub/sub event system. Feature A publishes, Feature B subscribes. Orchestrator manages queue + execution order. (from TODO-2, GAP-3) | TBD |
| S04 | Dependency Chain Engine | Defines execution order. C08 MUST before P17, C10 before C15. Prevents wrong-data decisions. (GAP-4) | TBD |
| S05 | API Rate Limit Manager | Dedicated rate limiter + queue for Ads API + SP-API. Smart batching. 300+ products need this. (GAP-15) | TBD |
| S06 | Data Validation Layer | Validate API data before processing. ACoS=99999%? Flag anomaly. Input sanity checks. (GAP-18) | TBD |
| S07 | Token Refresh Failure Handler | Refresh fails → alert + graceful degradation + manual intervention. (GAP-17) | TBD |
| S08 | API Failure Recovery & Retry | Exponential backoff, max retries, partial batch failure tracking. Resume from failure. (GAP-16) | TBD |
| S09 | Attribution Window Config | 7d/14d click attribution setting. Prevents premature negative marking. (GAP-9) | TBD |
| S10 | Data Freshness Indicator | "Last sync: 2 min ago". Warns on stale data. (GAP-11) | TBD |
| S11 | Conversion Lag Adjustment | Recent 2-3 days incomplete → estimate likely final value. Prevents unnecessary cuts. (GAP-12) | TBD |
| S12 | Historical Benchmark / Baseline | Rolling 30-day avg per product as baseline. Compare today vs baseline. (GAP-13) | TBD |
| S13 | Hard Safety Limits | Absolute max bid, max budget/day, max price decrease %. NEVER crossed. Last defense. (EN-7) | TBD |
| S14 | Auto-Rollback Engine | Every auto-action tagged. Monitor 48-72hrs. Worse by >X% → auto-revert + notify. (GAP-28) | TBD |
| S15 | Gradual Rollout Engine | New rule → test 5 products (3d) → expand 50 → all. Auto-stop if negative. (GAP-29) | TBD |
| S16 | System Health Monitor | All features green/yellow/red. Last run, API quota, DB size, failed tasks. (GAP-32) | TBD |
| S17 | Alert Fatigue Prevention | Group alerts, digest mode, suppression. P1 never suppressed. Daily max. (GAP-31) | TBD |
| S18 | Campaign Naming Convention | Enforce pattern: {Type}_{Product}_{Match}_{Strategy}. In C14. (GAP-24) | TBD |
| S19 | Full Audit Trail | Enhanced C07: who, why, before/after, approval chain. Multi-user. (GAP-25) | TBD |
| S20 | Rollback Scope Definition | Enhanced W08: last action/hour/day scope. Partial rollback. Conflicts. (GAP-26) | TBD |

---

# 🎯 ORCHESTRATOR CONFLICT EXAMPLES (NEW v10.0)

## Action Priority Chain
REMOVE > REDUCE > MAINTAIN > INCREASE > EXPAND

### Conflict 1: P07 vs P17
- P07: "Drop price — Buy Box lost" | P17: "Profit cap breach!"
- **RESOLUTION:** Risk-based — Buy Box revenue vs profit cap loss

### Conflict 2: C12 vs C15
- C15: "ACoS 35%, reduce bid" | C12: "Duplicate, NEGATIVE it"
- **RESOLUTION:** C12 wins. Remove > Reduce. C15 skips.

### Conflict 3: G04 vs C12
- G04: "Star keyword — expand" | C12: "Duplicate — negative!"
- **RESOLUTION:** Source tag. G04_expansion → C12 skip. No tag → C12 act.

### Zero Impression Diagnostic
Low Impression → Orchestrator checks: C15(bid) → P13(budget) → P07(buybox) → P08(suppressed) → P04(stock) → K09(match) → M06(competition) → I04(relevance)

| # | Conflict | Winner | Rule |
|---|----------|--------|------|
| 1 | P07 vs P17 | Orchestrator | Risk-based |
| 2 | C12 vs C15 | C12 | Remove > Reduce |
| 3 | G04 vs C12 | Source tag | Intentional > Accidental |
| 4 | Any vs S13 | S13 ALWAYS | Safety > Everything |

---
# 📛 NAMING STANDARDS (v10.0)
| Term | Use For | Example |
|------|---------|---------|
| Engine | Core processing logic | Bid Optimizer Engine |
| Module | Group of related features | FBA Module |
| Feature | Individual capability | Budget Spike Protection |
| System | End-to-end workflow | 4-Level AI Learning System |
| Layer | Architectural level | Data Layer, Intelligence Layer |

---

# 🔍 DETAILED FEATURE SPECIFICATIONS (v4.0 NEW!)

## P07 — Buy Box Monitor & Auto-Price Recovery (REVISED v4.0)
```
API Source: SP-API Pricing v2022-05-01 (getCompetitiveSummary)
Real-time: SP-API Notifications v1 (ANY_OFFER_CHANGED)
Coverage: ✅ 100% — No gaps

LOGIC:
  Buy Box Lost →
    1. Reduce ad bids (configurable %, default 50%)
    2. Alert user: "Buy Box lost! Competitor at ₹X"
    3. Start Auto Price Decrease cycle (if enabled)

AUTO PRICE DECREASE CYCLE:
  Default: 5% decrease every 30 minutes
  → Recheck Buy Box status after each decrease
  → Alert user on every decrease
  → Stop when: Buy Box regained OR minimum price floor reached
  
MENU CONFIGURATION:
  ├── Buy Box Lost Bid Reduction %    [default: 50%]    configurable
  ├── Auto Price Decrease %           [default: 5%]     configurable
  ├── Decrease Interval (minutes)     [default: 30]     configurable
  ├── Minimum Price Floor             [cost + 10%]      configurable
  ├── Alert on every decrease         [default: ON]     configurable
  ├── Auto Price Decrease Enabled     [default: OFF]    configurable (safety)
  └── Real-time Notification          [default: ON]     configurable
```

## P09 — Review Score Drop Brake (CONFIRMED v4.0)
```
API Source: Customer Feedback API v2024-06-01
Refresh: Weekly
Coverage: ✅ 100% — avg_rating available

LOGIC:
  IF avg_rating < 3.5★ → reduce bids 30%
  Fully automatic, no manual intervention needed
```

## P10 — Negative Review Ad Brake (REVISED v4.0)
```
API Source: Customer Feedback API v2024-06-01
Coverage: 🟢 85% auto, 100% automatic (NO manual)

⚠️ REMOVED in v4.0:
  ✗ "Side effects" keyword tracking — REMOVED
  ✗ ACR API approval plan — REMOVED (will NOT apply)
  ✗ Manual flag via Web Panel — REMOVED

LOGIC (100% Automatic):
  Condition A: negative_ratio > 30% (1★+2★/total) → 60% bid reduction
  Condition B: 1★ spike detected (this week vs last 4 weeks) → 40% reduction
  Condition C: Critical negative themes (Amazon AI-generated) → 50% reduction
  Condition D: negative_ratio > 20% (moderate) → 25% reduction
  
  Layer 3 Refinement (optional):
    Gemini 2.5 Flash analyzes themes → adjust ±10%
    
  ALL automatic. Zero manual. ₹0 cost.
```

## G10 — Review Impact Tracker (CONFIRMED v4.0)
```
API Source: Customer Feedback API v2024-06-01
Method: Store weekly snapshots → calculate trend locally
Coverage: ✅ 90% — weekly granularity (not daily)

LOGIC:
  rating_change = this_week_avg - last_week_avg
  IF significant drop → correlate with conversion/sales data → adjust bids
```

## M04 — Market Keyword Gap Finder (REVISED v4.0)
```
⚠️ NO AUTOMATION — Recommend only, user approval required for ALL keyword actions

4-APPROACH COMPOSITE:

Approach A: Search Term Report Reverse Engineering (FREE)
  Source: Ads Reporting API v3
  Logic: High impression + low click terms = competitor-strong keywords
  Action: Adjust bid strategy on OUR existing keywords
  + NEW: Inform user → "Optimize listing against these keywords"

Approach B: Category Keyword Discovery (FREE)
  Source: SP-API Catalog Items v2022-04-01
  ⚠️ VERY CAREFUL — Wide category = risky
  ✗ NEVER auto-use for ads without user approval
  ✓ Show to user for approval ONLY
  ✓ Push to Google Sheet for "New Product Opportunity"
  Configuration (all in menu):
    ├── Google Sheet ID: [configurable]
    ├── Tab Name: [default: "Category Keywords", configurable]
    ├── Column mapping: [configurable]
    ├── Auto-push frequency: [default: Weekly, configurable]
    └── Push enabled/disabled: [default: OFF, configurable]

Approach C: Amazon Suggested Keywords (FREE)
  Source: Ads API v1 Unified — Keyword Suggestions endpoint
  Logic: Input ASIN → get suggestions → compare with active keywords

Approach D: Brand Analytics Data (FREE, Brand Registered ✅)
  Source: SP-API Brand Analytics v1
  Logic: Top search terms → compare with our keywords

WEB PANEL TABS:
  Tab 1: "For Ads" (A + C + D results) → Approve → then add to campaigns
  Tab 2: "Listing Optimization" (A reverse) → Suggestions to optimize listing
  Tab 3: "Category Keywords" (B) → ⚠️ Warning: "Wide, review carefully"
  Tab 4: "New Product Opportunities" (B) → Auto-push to configured Google Sheet
```

## M09 — BSR Trend Tracker (REVISED v4.0)
```
⚠️ Keepa API REMOVED — will NOT use

PRIORITY ORDER:
  1st (PRIMARY): Manual Sheet uploaded by user
     Format: ASIN | BSR | DATE
     If data given → use this
  
  2nd (FALLBACK): SP-API Catalog Items v2022-04-01 (salesRanks)
     If manual not given → auto fetch
     Store daily snapshots → calculate trend
  
  3rd (SUPPORT): Sales + Traffic + CTR data
     Used to validate/support BSR trend analysis
     
LOGIC:
  BSR improving → organic growing → can reduce ad spend
  BSR dropping → organic declining → may need more ads
  Combined with sales/traffic/CTR → stronger decision signal
```

## K06 — Amazon Keyword Fetcher (NEW v5.0!)
```
API Source: Ads API v1 (Unified) — /keywords/suggestions endpoint
Database: SQLite (keyword_suggestions table)
Sheet: Input + Output via GAS Webhook

INPUT (Google Sheet):
  Columns: ASIN | Seed Keyword/Product Name | Category | Status
  Filter: Status = "NEW" OR EMPTY (both trigger processing)
  At least ONE of ASIN or Seed Keyword required
  If ASIN given → API uses ASIN (more accurate)
  If only Seed Keyword → API uses keyword
  If BOTH → ASIN primary + Seed combo

OUTPUT (Google Sheet):
  Columns: Source ASIN | Source Seed | Suggested Keyword | Match Type |
           Est. Search Volume | Bid Recommendation | Relevance Score |
           Use For (Ads/Listing/Both/New Product) | Date | Status

PROCESS:
  1. Read Input Sheet via webhook (filter NEW/empty)
  2. For each row → Ads API v1 /keywords/suggestions
  3. Store ALL results in SQLite (dedup by source_asin + keyword)
  4. Batch write to Output Sheet via webhook (50-100 rows/POST)
  5. Update Input Sheet status → "DONE"

PERFORMANCE:
  ├── API Rate: Max 5 req/sec (safe margin)
  ├── Batch writes: 50-100 rows per POST (not row-by-row!)
  ├── GAS latency: Cold 2-5s, Warm 0.5-2s
  ├── Schedule: Configurable from menu (default: Daily 2:00 AM IST)
  └── Retry: Exponential backoff on 429 (rate limit)

CONFIG (per-feature, in menu):
  ├── Input Sheet ID:  [empty = default]
  ├── Input Tab Name:  [REQUIRED]
  ├── Input Columns:   [REQUIRED]
  ├── Output Sheet ID: [empty = default]  
  ├── Output Tab Name: [REQUIRED]
  ├── Output Columns:  [REQUIRED]
  ├── Webhook URL:     [empty = default]
  └── Schedule:        [configurable: Manual/6hr/12hr/Daily/2day/Weekly/Custom]
```

## K07 — Keyword → Listing Optimizer (NEW v5.0!)
```
Source: K06 results (SQLite keyword_suggestions table)
Listing Data: SP-API Catalog Items v2022-04-01
Database: SQLite (listing_recommendations table)

LOGIC:
  1. Read fetched keywords for an ASIN from SQLite
  2. Read current listing data via SP-API (title, bullets, description, backend)
  3. Compare: which keywords MISSING from listing?
  4. Categorize:
     ├── "Add to Title" → high volume, not in title
     ├── "Add to Bullets" → medium volume, not in bullets
     ├── "Add to Backend" → low volume but relevant
     └── "Already Present" → skip
  5. Write recommendations to Sheet + Web Panel

OUTPUT (Google Sheet):
  Columns: ASIN | Keyword | Current Location | Recommended Location |
           Priority | Est. Search Volume | Reason | Date

APPLY MODE (configurable):
  ├── Recommend Only (default ✅) → Sheet + Web Panel display
  ├── Recommend + Draft → SP-API Feeds draft, user reviews in Seller Central
  └── Auto-Apply (⚠️ Advanced) → SP-API Feeds v2021-06-30 auto-submit
      ├── ⚠️ WARNING: Changes live listing!
      ├── Requires explicit enable + confirmation
      ├── Max keywords per update: [5] (configurable, safety)
      ├── Default: Backend only (safest)
      └── Rollback window: [7] days

CONFIG (per-feature, in menu):
  ├── Sheet ID / Tab / Columns: [configurable]
  ├── Apply Mode: [Recommend Only / Draft / Auto-Apply]
  ├── Max keywords per listing update: [5]
  ├── Allowed locations: [✅ Backend] [⬜ Title] [⬜ Bullets]
  └── Schedule: [Weekly default]
```

## K08 — Keyword → Product Opportunity Finder (NEW v5.0!)
```
Source: K06 all fetched keywords (SQLite keyword_suggestions table)
AI: Gemini 2.5 Flash (Layer 3) for analysis
Database: SQLite (product_opportunities table)

LOGIC:
  1. Analyze ALL fetched keywords across all ASINs
  2. Find keyword clusters where:
     ├── High search volume
     ├── We have NO product targeting this
     ├── Related to our category (healthcare/ayurvedic)
     └── Low competition signals
  3. Gemini 2.5 Flash: "These keywords suggest demand for [X] we don't sell"
  4. Score and rank opportunities
  5. Push to Sheet

OUTPUT (Google Sheet):
  Columns: Keyword Cluster | Related Keywords | Est. Monthly Volume |
           Suggested Product Type | Competition Level | Our Relevance |
           AI Reasoning | Priority Score (1-100) | Date

CONFIG (per-feature, in menu):
  ├── Sheet ID / Tab / Columns: [configurable]
  ├── Schedule: [Weekly default]
  └── Auto-push enabled: [OFF default]
```

## SQLite Database Schema (NEW v5.0!)
```sql
-- ORM: SQLAlchemy 2.0.x | Migration: Alembic 1.13.x
-- Engine: SQLite (ALL phases). PostgreSQL only if 40+ sellers + Msir approval

-- K06: Keywords fetched from Amazon API
CREATE TABLE keyword_suggestions (
    id INTEGER PRIMARY KEY,
    source_asin TEXT,
    source_seed TEXT,
    keyword TEXT NOT NULL,
    match_type TEXT,
    search_volume INTEGER,
    bid_recommendation REAL,
    relevance_score REAL,
    use_for TEXT,          -- 'ads' / 'listing' / 'both' / 'new_product'
    status TEXT DEFAULT 'new',
    fetched_date DATE,
    sheet_synced BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_asin, keyword)
);

-- K07: Listing optimization recommendations
CREATE TABLE listing_recommendations (
    id INTEGER PRIMARY KEY,
    asin TEXT NOT NULL,
    keyword TEXT NOT NULL,
    current_location TEXT,      -- title/bullets/backend/none
    recommended_location TEXT,
    priority TEXT,
    reason TEXT,
    applied BOOLEAN DEFAULT FALSE,
    sheet_synced BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- K08: Product opportunities
CREATE TABLE product_opportunities (
    id INTEGER PRIMARY KEY,
    keyword_cluster TEXT,
    related_keywords TEXT,
    monthly_volume INTEGER,
    product_type TEXT,
    competition TEXT,
    relevance TEXT,
    ai_reasoning TEXT,
    priority_score INTEGER,
    sheet_synced BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- v6.0 NEW: Learning system tables
CREATE TABLE ai_learning (
    id INTEGER PRIMARY KEY,
    level TEXT NOT NULL,          -- 'software' / 'category' / 'product' / 'keyword'
    module TEXT NOT NULL,         -- 'ads' / 'fba' / 'sales' / 'buybox' / 'listing' / 'review' / 'supplier'
    marketplace_tag TEXT,
    category_tag TEXT,
    product_tag TEXT,
    keyword_tag TEXT,
    learning_data TEXT NOT NULL,  -- JSON: pattern, confidence, sample_size
    iq_score REAL,
    proven BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- v6.0 NEW: Cross-module learning weights
CREATE TABLE learning_weights (
    id INTEGER PRIMARY KEY,
    source_module TEXT NOT NULL,
    source_attribute TEXT NOT NULL,  -- micro-level attribute
    target_module TEXT NOT NULL,
    target_attribute TEXT NOT NULL,
    tier INTEGER DEFAULT 4,          -- 1=HIGH, 2=LOW, 3=ZERO, 4=ASK
    weight REAL DEFAULT 0.0,
    data_correlation REAL,
    last_evaluated TIMESTAMP,
    auto_promoted BOOLEAN DEFAULT FALSE
);

-- v6.0 NEW: Module schedules (smart dynamic)
CREATE TABLE module_schedules (
    id INTEGER PRIMARY KEY,
    module TEXT NOT NULL,
    normal_interval_seconds INTEGER NOT NULL,
    escalated_interval_seconds INTEGER,
    current_state TEXT DEFAULT 'normal',  -- 'normal' / 'escalated' / 'monitoring'
    trigger_condition TEXT,               -- JSON: condition rules
    last_run TIMESTAMP,
    next_run TIMESTAMP
);

-- v6.0 NEW: Users and accounts
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    admin_level TEXT DEFAULT 'user',  -- 'super_admin' / 'account_admin' / 'user' ← UPDATED v8.0!
    status TEXT DEFAULT 'active',     -- 'active' / 'disabled' / 'pending_approval' ← NEW v8.0!
    disabled_at TIMESTAMP,            -- for 12-month auto-delete tracking ← NEW v8.0!
    whatsapp TEXT,                     -- optional, future integration ← NEW v8.0!
    grace_period_days INTEGER DEFAULT 0, -- REMOVED grace period, kept field for future ← v8.0!
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE seller_accounts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    marketplace TEXT NOT NULL,
    seller_id TEXT NOT NULL,
    is_master BOOLEAN DEFAULT FALSE,
    settings TEXT,               -- JSON: account-specific settings
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE partner_sellers (
    id INTEGER PRIMARY KEY,
    account_id INTEGER REFERENCES seller_accounts(id),
    partner_seller_id TEXT NOT NULL,
    partner_name TEXT,
    auto_sync BOOLEAN DEFAULT TRUE,
    marketplace TEXT NOT NULL
);

CREATE TABLE staff_roles (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    role_name TEXT NOT NULL,      -- 'ads_staff' / 'pricing_staff' / 'listing_staff' / 'supplier'
    modules TEXT,                 -- JSON: assigned modules (multiple per user)
    module_permissions TEXT,      -- JSON: {module: "view"/"edit"/"full_action"/"no_access"} ← NEW v8.0!
    assigned_accounts TEXT,       -- JSON: assigned seller account IDs ← NEW v8.0!
    assigned_marketplaces TEXT,   -- JSON: assigned marketplace IDs ← NEW v8.0!
    is_secondary BOOLEAN DEFAULT FALSE,
    notify_email TEXT,
    notify_whatsapp TEXT
);

-- User Performance Tracking ← NEW v8.0!
CREATE TABLE user_performance (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    date DATE NOT NULL,
    tasks_total INTEGER DEFAULT 0,
    tasks_on_time INTEGER DEFAULT 0,
    recommendations_total INTEGER DEFAULT 0,
    recommendations_acted INTEGER DEFAULT 0,
    priority_tasks_total INTEGER DEFAULT 0,
    priority_tasks_on_time INTEGER DEFAULT 0,
    avg_completion_time_mins REAL,
    score REAL,                   -- 0-100 calculated score
    UNIQUE(user_id, date)
);

-- Audit Trail ← NEW v8.0!
CREATE TABLE audit_trail (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action_type TEXT NOT NULL,    -- 'task_complete' / 'recommendation_acted' / 'setting_changed' etc.
    module TEXT,                  -- which module
    details TEXT,                 -- JSON: action details
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Leave Tracking ← NEW v8.0!
CREATE TABLE user_leaves (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    leave_date DATE NOT NULL,
    applied_date DATE NOT NULL,
    is_advance BOOLEAN,          -- TRUE if applied 7+ days before
    approved_by INTEGER REFERENCES users(id),
    is_emergency BOOLEAN DEFAULT FALSE
);

-- Campaigns, Keywords, Decisions, etc. (existing features → DB)
-- ... (schema expands as features are built)

-- Sync tracking
CREATE TABLE sync_status (
    id INTEGER PRIMARY KEY,
    feature TEXT NOT NULL,       -- 'K06' / 'K07' / 'K08' / 'M04' etc.
    last_sync_time TIMESTAMP,
    rows_synced INTEGER,
    status TEXT                  -- 'success' / 'error'
);

-- Per-feature sheet configs (also in JSON, DB for runtime)
CREATE TABLE sheet_configs (
    id INTEGER PRIMARY KEY,
    feature TEXT NOT NULL,
    sheet_id TEXT,
    webhook_url TEXT,
    secret_key TEXT,
    tab_name TEXT NOT NULL,
    column_mapping TEXT NOT NULL,  -- JSON string
    schedule TEXT,
    enabled BOOLEAN DEFAULT TRUE
);
```

---

# 🏗️ BUILD PHASES (UPDATED v6.0)

## Phase 1: FOUNDATION (Week 1-2) — 45 Features + SQLite Setup
**Goal:** Working system that pulls data, analyzes, generates report, takes actions

Core: C01-C08, C10-C12, C15-C16, C20-C28
Intelligence: I01-I04, I15-I17, I21-I22, **I25** (4-Level learning foundation)
Protection: P01, P03, P13, P15
Growth: G01
Reporting: R01-R07, R09, R12
Alerts: A01-A04
Automation: W01-W03, W06
Config: E01, E10
Keywords: K01-K02, K04

**Deliverable:** System runs daily → generates Excel → user reviews → submits → executes
**Tech:** Python 3.11, pandas 2.2.x, numpy 2.4.4, SQLAlchemy 2.0.x, Alembic 1.13.x, SQLite, Amazon Ads API v1 (Unified), Ads Reporting API v3

## Phase 2: INTELLIGENCE (Week 3-4) — 66+ Features
**Goal:** Smart decisions, learning, competitor awareness, health-specific, SP-API, per-module AI

Core: C05, C09, C13-C14, C17-C19
Intelligence: I05-I06, I08, I10-I12, I18, I20, I23-I24, **I26-I28**, **I30-I32** (per-module AI, cross-module learning, review→ad prediction, product health score, anomaly detection, return rate)
Protection: P02, P04-P06, P07-P12, P16, **P17-P18** (profit cap, image compliance)
Market: M01-M03, M06, M08, M10, **M11** (competitor launch alert)
Growth: G02-G04, G08-G10, G12, **G13-G14** (repeat purchase, listing health score)
Health: H01, H04-H07, **H11** (storage fee avoidance)
Reporting: R11, R14-R15, **R16** (weekly AI summary)
Alerts: A07-A10, **A11-A14** (advanced alerts, escalation, smart scheduling)
Automation: W04-W05, W07-W10, **W11-W12** (dead campaign cleanup, non-performing listing engine)
Integration: E02-E04, E08-E09, **E11, E13-E14** (partner seller, easy signup, multi-contact)
Keywords: K03, K05, K06, **K09** (match type migration)

**Deliverable:** Self-learning + competitor tracking + SP-API + web panel + K06 + **per-module AI + cross-learning + smart scheduling + partner seller + easy signup + v9.0 new features**
**Tech adds:** LightGBM 4.6.0, Prophet 1.3.0, scipy 1.17.0, Flask 3.1.3, SP-API EU

## Phase 3: ADVANCED AI (Week 5-6) — 33+ Features
**Goal:** Predictions, simulations, deeper insights, LLM integration, alliance/staff

Intelligence: I07, I09, I13-I14, I19, **I29** (supplier scorer)
Protection: P12, P14
Market: M04-M05, M07, M09
Growth: G05-G07, G11, **G15** (A+ content impact)
Health: H02-H03, H08-H10
Reporting: R08, R13
Keywords: K07, K08
Integration: **E12** (Alliance/Staff system)

**Deliverable:** Predictive engine + What-If simulator + LLM insights + full health intelligence + K07 + K08 + **staff roles/permissions + supplier scoring + A+ tracking**
**Tech adds:** Gemini 2.5 Flash API / Ollama

## Phase 4: ENTERPRISE (Future) — 12+ Features
**Goal:** Scale to multi-account, integrations, agency mode, WhatsApp
**Database:** SQLite continues. PostgreSQL ONLY if 40+ sellers + Msir approval ← UPDATED v10.0!

Reporting: R10
Alerts: **A05** (WhatsApp — MOVED from Phase 3!), A06
Config: E05-E07
**Future Plugins:** FBA automation, Listing optimization automation, ASIN-wise sales monitor, Supplier PO management

**Phase TBD (v10.0 NEW):** Phase assignments for new v10.0 features (S01-S20, I33-I34, M12, G16-G19, R17-R18, W13, E18-E19, K10) are marked TBD. See separate document: GoAmrita_Phase_Plan_v10.0.md

---

*MASTER Feature Registry v10.0 | 12 April 2026*
*216 Features / 215 active (33 new in v10.0, 13 enhancements) | 12 Categories | 4 Build Phases | API Versions LOCKED*
*Changes from v9.0: Round 10 — 360° Gap Analysis: 33 gaps integrated, 3 new modules (Smart Pricing, FBA, A+), 7 new features, 13 enhancements, 8 design principles, Category 12 (Infrastructure & Safety), Developer TODO + Gap Analysis merged, Orchestrator conflict examples, Auto-First philosophy, naming standardized*
