# GoAmrita Ads Intelligence System — Developer Handover Document v1.0

**Project Name:** Grow24 AI (formerly GoAmrita)
**Date:** 12 April 2026
**Project Owner:** Msir (mahendrasir23@gmail.com)
**Seller:** GoAmrita Bhandar / Made in Heavens
**Entity ID:** ENTITY1TVPGA5B1GOJW
**Marketplace:** Amazon India (amazon.in)
**Products:** 300+ Healthcare / Food / Ayurvedic products

---

# SECTION 1: PROJECT OVERVIEW

## What is this project?

An Amazon Ads Optimization System specifically for healthcare/ayurvedic products on Amazon India. Not just an ad tool — a Healthcare Business Growth Partner that automates advertising decisions using AI.

## Current Status: DESIGN COMPLETE, BUILD NOT STARTED

Everything is in discussion/design phase. 10 rounds of deep discussion completed. No code has been built yet (except API auth tests that work).

## Golden Rule

"Automate business > Everything else." Architect features fully but build from MINIMUM, scale on the go. Fundamentals must be STRONG so scaling later requires NO rewrites.

---

# SECTION 2: CRITICAL RULES — READ BEFORE ANYTHING

## Rule 1: INDIA = EUROPE REGION (NOT Far East!)

This is the #1 bug we already hit. Amazon India marketplace uses the EU region endpoints, NOT Far East.

- Ads API Endpoint: `advertising-api-eu.amazon.com`
- SP-API Endpoint: `sellingpartnerapi-eu.amazon.com`

NEVER use `sellingpartnerapi-fe.amazon.com` — it will return 403.

## Rule 2: STRICT VERSION LOCK — ZERO TOLERANCE

USE ONLY the exact pinned versions listed in Section 4. Before writing ANY code:

1. Open OFFICIAL documentation of the PINNED version
2. Confirm the method/function EXISTS in that version
3. Confirm the parameters are correct for that version
4. ONLY THEN write the code

NEVER use: Stack Overflow code, random blog code, AI training data assumptions, or internet snippets that may use different version functions. ONLY official docs of our pinned version.

## Rule 3: SQLite FOREVER (Unless 40+ Sellers + Msir Approval)

Database is SQLite for ALL phases. PostgreSQL migration ONLY happens if:
- 40+ sellers are actively using the system AND
- Msir explicitly approves the migration

Architecture is ready (SQLAlchemy ORM, 1-line change), but DO NOT plan or build PostgreSQL support. SQLite is the production database.

## Rule 4: No Feature Deprecation Without Approval

NEVER merge, deprecate, delete, or replace any existing feature without Msir's explicit approval. You can IMPROVE existing features or ADD new ones.

## Rule 5: Version Discipline

ALWAYS increment version numbers for new file versions. ALWAYS keep backup before overwriting.

---

# SECTION 3: ALL PROJECT FILES

## Primary Design Documents (LATEST — use these)

| File | Version | Location | Description |
|------|---------|----------|-------------|
| MASTER Feature Registry | v9.0 | `Scheduled/Project Details/GoAmrita_MASTER_Feature_Registry_v9.0.md` | Complete system blueprint — 183 features, architecture, API specs, DB schema, folder structure, build phases |
| WebPanel Design | v8.0 | `Scheduled/Project Details/GoAmrita_WebPanel_Design_v8.0.md` | 12 pages, 50+ tabs, complete UI/UX blueprint |
| Discussion Changes Log | v7.0 | `amazon-ads-thursday-analysis/GoAmrita_Discussion_Changes_v7.0.md` | 167 changes across 10 rounds — full history of all design decisions |

| MASTER Future Module Standard | v1.0 | `GoAmrita_Developer_Handover_Package_12Apr2026/GoAmrita_MASTER_Future_Module_Standard_v1.0.md` | Standard for ALL NEW future modules/features only. Legacy modules stay unchanged until planned migration. |

## Credentials (WORKING — tested 10 April 2026)

| File | Description |
|------|-------------|
| `amazon-ads-thursday-analysis/api_credentials.json` (v2.1) | Ads API OAuth2 — ACTIVE AND WORKING |
| `amazon-ads-thursday-analysis/sp_api_credentials.json` | SP-API credentials — Authorized |

## Stable Backup

| Folder | Contents |
|--------|----------|
| `amazon-ads-thursday-analysis/STABLE_BACKUP_v8.0/` | Backup of MASTER v8.0, WebPanel v7.0, Discussion v6.0 (before Round 9 changes) |

## Learning & Rules

| File | Description |
|------|-------------|
| `amazon-ads-thursday-analysis/Learning And Rule/QUICK_RECALL.md` (v1.2) | Mandatory pre-task checklist — READ FIRST every session |
| `amazon-ads-thursday-analysis/Learning And Rule/01_PRE_PLANNING.md` through `10_AI_SELF_RULES.md` | Detailed rules across 10 categories |

## Earlier Versions (Reference only — DO NOT use for building)

All v1.0 through v8.0 files exist in `amazon-ads-thursday-analysis/` folder. Use only the LATEST versions listed above.

---

# SECTION 4: LOCKED TECH STACK

## APIs — ALL VERIFIED WORKING

```
AMAZON ADS API:
  Campaign Management: Ads API v1 (Unified) — NEWEST, complete architectural reboot
    Endpoint: advertising-api-eu.amazon.com
    Profile ID: 42634532240933

  Reporting PRIMARY: Ads API v1 — Unified Reporting
    Covers: Search Term, Performance, Placement, Impression Share, Click Share
    Benefits: Cross-product combine (SP+SB+SD), 15 months daily, 6 years monthly

  Reporting FALLBACK: Ads Reporting API v3
    Use ONLY if v1 Unified missing specific data (as of April 2026: NO gaps found)

AMAZON SP-API:
  Region: EU (India = Europe region, NOT Far East!)
  Endpoint: sellingpartnerapi-eu.amazon.com
  
  Catalog Items:       v2022-04-01
  Pricing:             v2022-05-01 (getCompetitiveSummary, Buy Box)
  Orders:              v2026-01-01 (NEWEST! migration deadline March 2027)
  FBA Inventory:       v1
  Feeds:               v2021-06-30 (JSON ONLY, XML deprecated!)
  Listings Items:      v2021-08-01
  Notifications:       v1 (ORDER_CHANGE, LISTING_CHANGE, INVENTORY_CHANGE, ANY_OFFER_CHANGED)
  Customer Feedback:   v2024-06-01 (review insights, weekly refresh)
  Brand Analytics:     v1
  Sales & Traffic:     v2024-04-24
  Search Catalog Perf: Brand Analytics API
```

## Python & Libraries — LEAN STACK (Phase 1)

```
Python:      3.11.x    (3.11.15 latest patch)
Flask:       3.1.3     (web panel)
openpyxl:    latest    (Excel report generation)
requests:    latest    (HTTP/API calls)
```

See `DEFERRED_LIBRARIES.md` for frozen libraries list (LightGBM, Prophet, scipy, pandas, numpy, SQLAlchemy, Alembic — all deferred to Phase 2+).

Pin exact versions in requirements.txt using `==`.

## Database

```
Engine: JSON files (DB deferred)
File:   data/*.json
ORM:    Not needed for Phase 1 (SQLAlchemy deferred)

SQLite/PostgreSQL: DEFERRED — will evaluate when data volume requires it
```

## Google Sheets Integration

```
Method: Google Apps Script (GAS) Webhook — NO OAuth, NO API Key
  GAS deployed as Web App per sheet
  Python → HTTP POST → GAS → Sheet read/write
  Security: Simple secret key (user-defined string)
```

---

# SECTION 5: SYSTEM ARCHITECTURE

## Design Philosophy

```
USER EXPERIENCE:  Like eating sweet (simple outside, complex inside)
BACKEND:          Like nuclear reactor (powerful, hidden)
DATA:             JSON files (TRUTH) — DB deferred
SETTINGS:         3-Level: Account -> Category -> Product (inheritance)
AI:               3-Layer: Rules -> ML -> LLM (each layer adds intelligence)
LEARNING:         4-Level: Software -> Category -> Price Segment -> Product
ADMIN:            3-Level: Super Admin -> Account Admin -> User/Staff
```

## Folder Structure

The complete folder structure is in MASTER v9.0 (Section: MULTI-MARKETPLACE ARCHITECTURE). Key directories:

```
GoAmrita_Ads_System/
├── core/           — Marketplace-agnostic logic (100% reusable)
├── marketplaces/   — Amazon adapter (+ future Flipkart/Meesho)
├── ai/             — 3-Layer AI Engine + 4-Level Learning
├── web_panel/      — Flask 3.1.3 (localhost + server same code)
├── alerts/         — 4-type alert engine + smart scheduler
├── users/          — User management, roles, performance
├── config/         — 3-Level inheritance JSON configs
├── data/           — Daily metrics, snapshots, learning data
├── database/       — SQLite + SQLAlchemy + Alembic migrations
└── templates/      — GAS webhook template for users
```

## 3-Layer AI Engine

```
Layer 1: Rule-Based (Phase 1, Day 1, cost ₹0)
  Pure Python logic. Handles 80% of decisions.

Layer 2: ML/Statistical (Phase 2) — DEFERRED
  LightGBM + Prophet. Handles patterns, predictions.
  Libraries frozen — see DEFERRED_LIBRARIES.md

Layer 3: LLM (Phase 3, OPTIONAL) — DEFERRED
  Gemini 2.5 Flash API / Ollama local / Skip entirely
  3 options in config menu. System works 100% without it.
  LLM integration deferred until Phase 3.

Merger Engine: Combines all 3 layer outputs into final recommendation.
  Conflict resolution: Higher confidence wins.
  IQ Score (0-100) assigned to every recommendation.
```

## 4-Level Learning

```
Level 1: Software Level    — Global patterns across all accounts
Level 2: Category Level    — Healthcare vs Honey vs Supplements
Level 3: Price Segment     — How ₹200-500 products behave vs ₹500+
Level 4: Product Level     — Individual product patterns
```

## Marketplace Adapter Pattern

```python
class MarketplaceAdapter:   # Abstract base
class AmazonAdapter:        # Amazon Ads API v1 + SP-API EU
class FlipkartAdapter:      # FUTURE
class MeeshoAdapter:        # FUTURE
```

Core logic is 100% marketplace-agnostic. Only adapters change per marketplace.

---

# SECTION 6: 183 FEATURES (11 Categories)

Complete feature tables with descriptions, priorities, and phase assignments are in MASTER v9.0. Summary:

| # | Category | Count | Examples |
|---|----------|-------|---------|
| 1 | Core Engine (C) | 28 | OAuth, Data Pull, Bid Optimizer, Budget Manager, Funnel System |
| 2 | AI Intelligence (I) | 32 | IQ Score, Learning, Predictions, Anomaly Detection, Product Health Score |
| 3 | Protection & Compliance (P) | 18 | Budget Spike, CPC Shield, Buy Box Recovery, Profit Cap, Image Compliance |
| 4 | Market Intelligence (M) | 11 | Competitor Price/Stock, ASIN Targeting, Competitor Launch Alert |
| 5 | Growth Engine (G) | 15 | TACoS, Flywheel, Launch Autopilot, Listing Health Score, Repeat Purchase |
| 6 | Healthcare Specific (H) | 11 | Seasonal Demand, Ayurvedic Keywords, Deadstock, Storage Fee |
| 7 | Reporting (R) | 16 | Daily Excel, Strategy Impact, Weekly AI Summary |
| 8 | Alerts (A) | 14 | 4-Type Engine, Smart Scheduling, Escalation Chain |
| 9 | Automation (W) | 12 | 3-Mode Action, A/B Testing, Budget Redistribution, Non-Performing Listing |
| 10 | Integration (E) | 17 | JSON Config, Web Panel, Webhooks, Multi-Account, Staff System |
| 11 | Keywords (K) | 9 | 3 Modes (API/Sheet/Benefit), Match Type, Listing Optimizer, Migration |

**Total: 183 features (182 active + W10 redirect to G09)**

### Round 9 Changes (Latest)

- 15 NEW features: P17, P18, W11, W12, K09, G13, G14, G15, M11, I29, I30, I31, I32, H11, R16
- 11 IMPROVED features: C17, C18, M01, M03, G08, G09, K07, H08, H09, W05, H01
- 1 PRESET: A13 (Sales Velocity Alert)
- 1 CLEANUP: W10 merged into G09

---

# SECTION 7: BUILD PHASES

## Phase 1: FOUNDATION (Week 1-2) — 45 Features

Goal: Working system that pulls data, analyzes, generates report, takes actions.

```
Core: C01-C08, C10-C12, C15-C16, C20-C28
Intelligence: I01-I04, I15-I17, I21-I22, I25
Protection: P01, P03, P13, P15
Growth: G01
Reporting: R01-R07, R09, R12
Alerts: A01-A04
Automation: W01-W03, W06
Config: E01, E10
Keywords: K01-K02, K04

Deliverable: System runs daily → Excel report → User reviews → Approves → Executes
Tech: Python 3.11, pandas 3.0.2, SQLAlchemy 2.0.49, SQLite, Amazon Ads API v1
```

## Phase 2: INTELLIGENCE (Week 3-4) — 66+ Features

Goal: Smart decisions, learning, competitor awareness, SP-API integration, per-module AI.

```
Adds: ML Layer (LightGBM + Prophet), SP-API, Web Panel (Flask), 
      Per-Module AI, Cross-Module Learning, All v9.0 new features
NOTE: ML/Statistical libraries (LightGBM, Prophet, scipy, pandas, numpy) are DEFERRED.
      Will be added to requirements.txt only when Phase 2 build begins.

Deliverable: Self-learning + competitor tracking + web panel + smart scheduling
Tech adds: Flask 3.1.3, SP-API EU (ML libraries deferred — see DEFERRED_LIBRARIES.md)
```

## Phase 3: ADVANCED AI (Week 5-6) — 33+ Features

Goal: Predictions, simulations, LLM insights, alliance/staff system.

```
Adds: What-If Simulator, Gemini 2.5 Flash, Supplier Scorer, A+ Tracking
NOTE: LLM tech (Gemini/Ollama) is DEFERRED. Will evaluate when Phase 3 begins.

Deliverable: Predictive engine + LLM insights + staff roles
Tech adds: Gemini 2.5 Flash API / Ollama (DEFERRED — see DEFERRED_LIBRARIES.md)
```

## Phase 4: ENTERPRISE (Future)

Goal: Multi-account, agency mode, WhatsApp alerts.
Database: SQLite continues. PostgreSQL ONLY if 40+ sellers + Msir approval.

---

# SECTION 8: PENDING WORK — ROUND 10 (NOT YET DONE)

These items were identified and deferred. They need to be discussed and designed before/during build.

## 8.1 Cross-Feature Orchestration (CRITICAL — THE BIG GAP)

### Problem

182 features exist but operate independently. There is no central orchestrator that resolves conflicts when multiple features recommend conflicting actions simultaneously.

### What EXISTS already (engine parts)

```
1. 3-Layer AI (layer1 + layer2 + layer3 + merger_engine) — per-feature decision
2. IQ Score System (I01) — per-recommendation scoring 0-100
3. 4-Level Learning (I25) + Per-Module Brain (I26) + Cross-Module (I27)
4. Effect Tracker (I05) + Permanent Rule Maker (I23)
5. 3-Mode Action Engine (W01) — Manual/Semi-Auto/Full-Auto
6. Alert Engine (A13) + Smart Scheduler (A14)
```

### What is MISSING

```
Central Decision Orchestrator — when multiple features fire simultaneously:

Example conflict:
  P07 says: "Drop price to recover Buy Box"
  P17 says: "Profit cap hit — stop ad spend"
  W05 says: "Redistribute budget TO this product"
  H08 says: "Deadstock detected — go aggressive"
  
  → Currently: All 4 execute independently (WRONG)
  → Needed: One orchestrator decides priority, resolves conflict, outputs FINAL action
```

### Approach discussed

- NOT a single file — it's a layer that sits between feature outputs and action execution
- Takes ALL feature signals → evaluates priority, risk, confidence → outputs final action queue
- Must handle: conflict resolution, global priority, risk assessment
- Design in Round 10, build in Phase 2 (Phase 1 has no cross-feature conflicts)

## 8.2 Feature Categorization/Grouping on Website

### Problem

182 features — user cannot navigate this on the web panel. Need smart categorization, filtering, searching, grouping.

### Direction from Msir

"Deep think and decide yourself so user have no pain." Developer has free hand to design the best UX for feature navigation.

### Suggested approach

- Group by business function (not technical category)
- Smart search across all features
- "Most Used" / "Recommended" / "All" views
- Quick enable/disable toggles
- Feature dependency warnings

## 8.3 Cross-Feature Data Passing Architecture

### Problem

Feature A's output needs to become Feature B's input. Currently no pipeline architecture for this.

### Direction from Msir

"Think and decide yourself."

### Examples

```
H08 (Deadstock detected) → output → W05 (Budget redistribute) input
G10 (Review Impact) → output → C15 (Bid Optimizer) input factor
P07 (Buy Box lost) → output → A13 (Alert) + P06 (Price update) inputs
I30 (Product Health Score) → output → W12 (Non-Performing diagnosis) input
```

### Suggested approach

- Event-driven architecture (publish/subscribe pattern)
- Features publish events: `{ feature: "H08", event: "deadstock_detected", asin: "...", data: {...} }`
- Other features subscribe to relevant events
- Orchestrator layer manages event queue and priority

## 8.4 Smart Learning Per Feature

### Problem

4-Level AI Learning exists for overall system, but per-feature effectiveness tracking is missing. "Is feature H08 actually helpful? Is P07 making things better or worse?"

### Suggested approach

- Track per-feature: actions taken, outcomes, success rate, false positive rate
- Auto-disable features with consistently poor outcomes
- Surface effectiveness scores in admin dashboard

## 8.5 Importance + Critical Event Auto-Sorting

### Problem

When many alerts fire simultaneously, which one should the user see first? Need a priority framework.

### Suggested approach

- Priority scoring: Business Impact (weight 40%) + Urgency (30%) + Confidence (20%) + User Preference (10%)
- Auto-sort all alerts, recommendations, dashboard items by this score
- P1 (Critical) always on top, with escalation

## 8.6 Export/Report System (DEFERRED — Needs Deep Discussion)

Report tabs, export formats, scheduling, templates. This was deferred from Round 8 and needs a dedicated discussion round. Current design has basic R01-R16 features but the detailed export architecture (format options, scheduling, template system, email delivery) is not finalized.

---

# SECTION 9: KEY DECISIONS LOG

| Decision | What was decided | Round |
|----------|-----------------|-------|
| India = EU Region | SP-API + Ads API both use EU endpoints | R4 |
| Ads API v1 Unified | v1 is NEWEST (not older). v3 Reporting = fallback only | R4 |
| Orders API v2026-01-01 | NEWEST version, migration deadline March 2027 | R4 |
| Feeds JSON Only | XML deprecated in Feeds API | R4 |
| Feature vs Engine | Features = capabilities, Engine = decision brain. Both exist in system | R9 |
| No Feature Deprecation | Never merge/delete existing features without approval | R9 |
| W10 merged into G09 | Duplicate feature cleanup (only approved merge) | R9 |
| SQLite Forever | PostgreSQL ONLY if 40+ sellers + Msir approval | R10 |
| Build Minimum | Architect fully, build minimum, scale on go | R8 |
| Orchestrator = Phase 2 | Design now, build when cross-feature conflicts appear | R10 |
| 3 Gemini Options | API key / Ollama local / Skip — system works without LLM | R8 |
| GAS Webhook | NO OAuth for Google Sheets — simple webhook approach | R3 |
| Customer Feedback API | For reviews — NOT ACR API, NOT keyword-level tracking | R4 |

---

# SECTION 10: KNOWN MISTAKES — NEVER REPEAT

| Mistake | What happened | Lesson |
|---------|---------------|--------|
| Used FE endpoint for India | SP-API returned 403 | India = EU region, ALWAYS |
| Token truncated during save | Refresh token was cut off | Verify full length after save |
| Sandbox blocks Amazon | Development sandbox can't reach Amazon APIs | Test in real environment |
| Assumed PostgreSQL for Phase 4 | Was planning PostgreSQL migration | SQLite forever unless 40+ sellers |
| Tried to deprecate features | Merged/removed features without approval | NEVER without Msir approval |
| Called features "Engines" | Created naming confusion | Stick to existing naming convention |

---

# SECTION 11: CONTACTS & CREDENTIALS QUICK REFERENCE

```
Project Owner: Msir (mahendrasir23@gmail.com)
Seller Account: Made in Heavens / GoAmrita Bhandar

Ads API:
  Client ID: amzn1.application-oa2-client.b03d9d747f9542819e4afb87dec416f0
  Profile ID: 42634532240933
  Entity ID: ENTITY1TVPGA5B1GOJW
  Endpoint: https://advertising-api-eu.amazon.com
  Status: ACTIVE AND WORKING (tested 10 April 2026)

SP-API:
  App ID: amzn1.sp.solution.7b8d0508-4f32-4c19-89e0-25450c20f1cb
  LWA Client ID: amzn1.application-oa2-client.b74e1978a1814ae489576428b22e3292
  Endpoint: https://sellingpartnerapi-eu.amazon.com
  Secret Rotation Deadline: 2026-10-07
  Status: Authorized

Full credentials: See api_credentials.json and sp_api_credentials.json
```

---

# SECTION 12: HOW TO START BUILDING

## Step 1: Read these files (in order)

1. `Learning And Rule/QUICK_RECALL.md` — Mandatory rules
2. `GoAmrita_MASTER_Feature_Registry_v9.0.md` — Complete blueprint
3. `GoAmrita_WebPanel_Design_v8.0.md` — UI/UX design
4. `GoAmrita_Discussion_Changes_v7.0.md` — All design decisions history

## Step 2: Start with Phase 1

Phase 1 features are the foundation. No ML, no LLM, no web panel needed. Just:

```
1. OAuth2 auth (already working — C01)
2. Data pull from Ads API v1 Unified (C02-C05)
3. True profit calculation (C08, C10, C11)
4. Rule-based AI decisions (Layer 1 only)
5. IQ Score + Merger (I01, I02, I04, I15)
6. Daily Excel report generation (R01-R07)
7. User approval flow (W01-W02)
8. Execute approved actions (bid changes, budget changes)
```

## Step 3: Test with real data

Use the working credentials to pull actual campaign data from GoAmrita's Amazon account. Test with real numbers.

## Step 4: Before Phase 2 — Design the Orchestrator

Before building Phase 2 features (which run simultaneously), design the Cross-Feature Orchestrator. This is critical for Phase 2 to work correctly.

---

*Developer Handover Document v1.0 | 12 April 2026*
*Project: GoAmrita Healthcare Ads Intelligence System*
*Status: Design Complete (v9.0) | Build: Not Started | Pending: Round 10 items (Section 8)*
