# 📋 GoAmrita Phase Plan v10.0 — MVP-First Approach
**Project Name:** Grow24 AI (formerly GoAmrita)
**Date:** 12 April 2026 | **Status:** DRAFT — Msir will review & finalize
**Source:** 360° Gap Analysis session + MASTER Feature Registry v10.0
**Total Features:** 216 (215 active + W10 redirect) across 12 categories

---

## 🎯 Main Goal
**Business loss decrease, profit increase, automate Amazon business, auto grow day by day**
**Start from most important features so effect on business starts from day 1**

## 📐 Key Decisions
1. **Option B** — Orchestrator/Scheduler = Phase 2 (Phase 1 = straight pipeline, no cross-feature conflicts)
2. **MVP First** — Start with highest business impact features
3. **Auto-First** — Everything auto by default, approval only where AI not confident or risky
4. **Golden Rule** — "Automate business > Everything else"
5. **Philosophy** — Backend = Nuclear Reactor ⚛️ | Frontend = Sweet Shop 🍬

---

## PHASE 1: MVP FOUNDATION
**Goal:** Working pipeline: Data Pull → Analyze → Report → Approve → Execute = business impact from day 1
**Timeline:** Week 1-3

### Phase 1A: Infrastructure (Week 1)
Foundation that ALL features need — build FIRST.

| ID | Feature | Why First |
|----|---------|-----------|
| C01 | OAuth2 Auth Module | Everything needs auth |
| S05 | API Rate Limit Manager | 300+ products = breach without this |
| S06 | Data Validation Layer | Bad data → bad decisions |
| S07 | Token Refresh Failure Handler | Auth fails = everything fails |
| S09 | Attribution Window Config | Prevents premature decisions |
| S10 | Data Freshness Indicator | User knows data age |
| S11 | Conversion Lag Adjustment | Prevents unnecessary cuts |
| S12 | Historical Benchmark/Baseline | "What is our normal?" |
| S13 | Hard Safety Limits | Last line of defense — NEVER crossed |
| S18 | Campaign Naming Convention | Clean data from day 1 |
| E01 | JSON Config System (3-Level) | Settings foundation |
| C22 | 3-Level Account Settings | Inheritance system |
| C23 | Product-Level Overrides | Per-product customization |
| E10 | Multi-Marketplace Support (adapter) | India now, others later |
| C06 | History Storage (SQLite) | All data stored |

**Count: ~15 features**

---

### Phase 1B: Core Pipeline (Week 1-2)
Data pull + analysis engine.

| ID | Feature | Business Impact |
|----|---------|-----------------|
| C02 | Data Pull Engine (Ads API v1 Unified) | Get campaign data |
| C03 | Search Term Report Fetcher | Get search term data |
| C04 | Campaign Performance Report | Get daily metrics |
| C07 | Changelog Tracker | Every change logged |
| C08 | True Profit Calculator | REAL profit per product |
| C10 | Break-even ACoS Calculator | Max ACoS before loss |
| C11 | Smart Bid Ceiling | Max profitable bid |
| I01 | IQ Score Engine | Score recommendations 0-100 |
| I02 | User-Friendly Labels | "Strong Recommend" not "IQ: 87" |
| I04 | Data Confidence Scoring | Low data → conservative |
| I15 | Smart % Calculator | Dynamic bid/budget change % |
| I16 | Profit-Based Waste Detection | Waste = bid × profit |
| I22 | Decision Multi-Tag System | Every decision tagged |
| I25 | 4-Level AI Learning (foundation) | Learning structure ready |
| G01 | TACoS Tracker | True health metric |
| E15 | Report Import Module | Import historical data |
| E16 | Universal Import System | Excel/CSV + Sheet |

**Count: ~17 features**

---

### Phase 1C: Actions & Reporting (Week 2-3)
Recommendations + actions + reports + alerts.

| ID | Feature | Business Impact |
|----|---------|-----------------|
| C12 | Negative Keyword Engine (+ GAP-5 cannibalization + GAP-7 conflict check) | Stop waste spending |
| C15 | Bid Optimizer (+ impression share cap) | Optimize bids |
| C16 | Budget Manager (calendar + salary cycle) | Smart budgeting |
| C20 | Direct Keyword Campaign System | Msir's method |
| C21 | Product Strategy Modes | 6 modes |
| I17 | Slowly Reduce Bids | Gradual, not hard block |
| I21 | AI Recommendation Field | 3-column output |
| C24 | Cooling Period System | Days OR Budget |
| C25 | Campaign Exclusion (Time-Based) | Exclude for X days |
| C26 | Category Template System | Category defaults |
| C27 | Shipping Fee Tracker | Per-product fees |
| C28 | Marketplace Adapter Engine | Reusable core |
| K01 | Mode A: Amazon API Smart Campaign | Search terms + API |
| K02 | Mode B: Google Sheet/CSV Keywords | User keywords |
| K04 | Smart Match Type Engine | Auto match type |
| K10 | Search Term Graduation Pipeline | Unified flow |
| P01 | Budget Spike Protection | Emergency pause |
| P03 | API Error Fallback | No changes on error |
| P13 | Daily Cashflow Guardian | Budget pacing |
| P15 | Survival Mode | Strict waste blocking |
| R01 | Daily Excel Report (Multi-Tab) + Net Profit | Reports + insights |
| R02 | Action Tabs with Dropdowns | Approve/Reject/Skip |
| R03 | IQ-Based Auto-Fill | Auto-first! |
| R04 | Strategy Impact Tab | Action → Effect |
| R05 | Money Saved Counter | ₹ waste blocked |
| R06 | Day-to-Day Comparison | ↑↓ changes |
| R07 | Week-to-Week Comparison | Trends |
| R09 | Child-Simple Language | Simple language |
| R12 | Full Transparency | WHAT + WHY |
| R17 | Net Profit Dashboard | ONE number: ₹ profit |
| A01 | Priority Alert Engine (+ scoring) | P1/P2/P3 |
| A02 | Email Alerts (Multi-Recipient) | Alerts delivered |
| A03 | Excel Attachment in Email | Report attached |
| A04 | Mac Auto-Open Report | Auto-open |
| A13 | 4-Type Alert (+ intraday comparison) | Smart alerts |
| W01 | 3-Mode Action Engine | Auto/Semi/Manual |
| W02 | Approval Excel Processor | Read Excel → execute |
| W03 | One-Click Daily Pipeline | Single command |
| W06 | Scheduled Optimization Runs | Morning run |

**Count: ~39 features**

**PHASE 1 TOTAL: ~71 features**

---

## PHASE 2: INTELLIGENCE & ORCHESTRATION
**Goal:** Cross-feature brain, SP-API, web panel, advanced protection
**Timeline:** Week 4-7

### Phase 2A: Brain Layer (Week 4) — BUILD FIRST!

> **NOTE:** ML/Statistical libraries (LightGBM 4.6.0, Prophet 1.3.0) and DB libraries (SQLAlchemy 2.0.49) are **DEFERRED**. They are frozen in `DEFERRED_LIBRARIES.md` and will only be added to requirements.txt when Phase 2 build begins.

| ID | Feature | Why |
|----|---------|-----|
| S01 | Central Decision Orchestrator | Conflict resolution |
| S02 | Central Task Scheduler | Unified timing |
| S03 | Cross-Feature Event Bus | Feature communication |
| S04 | Dependency Chain Engine | Execution order |
| S08 | API Failure Recovery & Retry | Robust API handling |
| S14 | Auto-Rollback Engine | Safety for auto-actions |
| S15 | Gradual Rollout Engine | Test before full deploy |
| S16 | System Health Monitor | System status |
| S17 | Alert Fatigue Prevention | Smart alert grouping |
| S19 | Full Audit Trail | Who/why/what changed |
| S20 | Rollback Scope Definition | Clear undo boundaries |

**Count: ~11 features**

### Phase 2B: Advanced Intelligence (Week 4-5)

> **NOTE:** ML features in this sub-phase (I06 Predictive Sales Modeling, I18 Seasonal Demand Predictor, I31 Anomaly Detection, etc.) depend on deferred libraries (LightGBM, Prophet, scipy, pandas, numpy). These features cannot be built until deferred libraries are unfrozen.

| ID | Feature |
|----|---------|
| C05 | Placement Report Fetcher |
| C09 | Dynamic COGS Updater |
| C13 | Keyword Lifecycle Manager |
| C14 | Campaign Structure Manager (+ multi-ASIN) |
| C17 | Dayparting + Bid Schedule Engine |
| C18 | Placement Modifier Engine |
| C19 | Multi-Funnel Campaign System |
| I03 | Strategy Learning Database |
| I05 | Post-Change Monitor + Auto-Rollback |
| I06 | Predictive Sales Modeling (Prophet) |
| I08 | Intent-Based Keyword Engine |
| I10 | Auto A/B Testing Engine |
| I11 | Per-Keyword Learning |
| I12 | Per-Campaign Learning |
| I18 | Seasonal Demand Predictor |
| I20 | Returns Velocity Impact |
| I23 | Permanent Rule Maker + AI Recommender |
| I24 | Cross-Product Learner |
| I26 | Per-Module AI Brain |
| I27 | Cross-Module Learning Engine |
| I28 | Review → Ad Prediction |
| I30 | Product Health Score |
| I31 | Anomaly Detection 3-Level |
| I32 | Return Rate Analyzer |
| I33 | AI Action History + Feedback + Revert |

**Count: ~25 features**

### Phase 2C: Protection & Competition (Week 5-6)

| ID | Feature |
|----|---------|
| P02 | CPC Spike Detection |
| P04 | Stock-Out Ads Pause (+ resume logic) |
| P05 | Inventory Velocity Pacing |
| P06 | Stock-Low Auto Price Update |
| P07 | Buy Box Monitor (+ anti-loop) |
| P08 | Listing Suppression Alert |
| P09 | Review Score Drop Brake (+ resume) |
| P10 | Negative Review Brake (+ theme severity + resume) |
| P11 | Banned/Medical Claim Shield |
| P16 | Profit-per-Price Tracker |
| P17 | Profit % Cap System |
| P18 | Image Quality Checker |
| M01 | Competitor Price Monitor |
| M02 | Competitor Stock Monitor |
| M03 | Competitor ASIN Targeting |
| M06 | David vs Goliath Sniper |
| M08 | Sole Seller Detection |
| M10 | Impression Share Tracker |
| M11 | Competitor Launch Alert |
| M12 | Competitive Budget Intelligence |

**Count: ~20 features**

### Phase 2D: Growth & Automation (Week 6-7)

| ID | Feature |
|----|---------|
| G02 | Organic Flywheel Detector |
| G03 | Organic Rank Phase Detection |
| G04 | Auto-Scaling Winners |
| G08 | New Product Launch Autopilot (+ initial strategy) |
| G09 | New Listing Auto-Campaign |
| G10 | Review Impact Tracker |
| G12 | Listing Conversion AI Advisor |
| G13 | Repeat Purchase Tracker |
| G14 | Listing Health Score |
| H01 | Seasonal Health Demand |
| H04 | Problem→Solution Keywords |
| H05 | Ayurvedic Keyword Intelligence |
| H06 | Easy Win Finder |
| H07 | Health Compliance Guard |
| H11 | Long-Term Storage Fee Avoidance |
| W04 | Automated A/B Testing |
| W05 | Auto Budget Redistribution |
| W07 | Funnel Auto-Management |
| W08 | Smart Rollback (+ scope) |
| W09 | Batch Operations |
| W11 | Dead Campaign Cleanup |
| W12 | Non-Performing Listing Engine |
| K03 | Mode C: Product Benefit Targeting |
| K05 | Multi-Mode A/B Testing |
| K06 | Amazon Keyword Fetcher |
| K09 | Match Type Migration |
| R18 | Per-Feature ROI Tracking |

**Count: ~27 features**

### Phase 2E: Web Panel & Integrations (Week 6-7)

| ID | Feature |
|----|---------|
| E02 | Web Config Panel (Flask) (+ feature categorization) |
| E03 | Webhook System |
| E04 | Google Sheets Integration (GAS) |
| E08 | SP-API Full Integration |
| E09 | Ads ↔ Seller Cross-Communication |
| E11 | Partner Seller Logic |
| E13 | Easy Signup/Onboarding |
| E14 | Multi-Contact Support |
| E17 | Organic Competition Engine |
| E18 | Universal Search (UI) |
| E19 | Onboarding Wizard |
| R11 | Web Dashboard |
| R14 | Placement Recommendations |
| R15 | Conversion Suggestions |
| R16 | Weekly AI Summary |
| A07 | Smart Notification Content |
| A08 | Auto-Action on No Response |
| A09 | Browser Push Notifications |
| A10 | OS Desktop Notifications |
| A11 | Advanced Alert Notification |
| A12 | Alert Escalation Chain |
| A14 | Smart Dynamic Scheduling |

**Count: ~22 features**

**PHASE 2 TOTAL: ~105 features**

---

## PHASE 3: ADVANCED AI & NEW MODULES
**Goal:** ML predictions, LLM, new modules (Pricing, FBA, A+), advanced features
**Timeline:** Week 8-10

> **NOTE:** LLM features (I09 Gemini Insight Layer, I07 What-If Simulator) are **DEFERRED**. Gemini API / Ollama integration will only be evaluated when Phase 3 build begins. System works 100% without LLM layer.

| ID | Feature |
|----|---------|
| I07 | "What If" Simulator |
| I09 | LLM Insight Layer (Gemini) |
| I13 | Per-Account Learning |
| I14 | Per-Price-Segment Learning |
| I19 | Category Benchmark Engine |
| I29 | Supplier Performance Scorer |
| I34 | Predictive Customer Segmentation |
| P12 | Compliance Dictionary |
| P14 | Cash-Flow Sync (Payout) |
| M04 | Market Keyword Gap Finder |
| M05 | Dynamic Pricing Intelligence |
| M07 | Category Benchmark Dashboard |
| M09 | BSR Trend Tracker |
| G05 | Subscribe & Save Optimizer |
| G06 | Bundle/Cross-Sell Intelligence |
| G07 | Virtual Bundle Market Basket |
| G11 | Trust Score System |
| G15 | A+ Content Impact Tracker |
| G16 | Smart Pricing / Repricing Engine (MODULE) |
| G17 | FBA Management Module |
| G18 | Purchase & Supply Chain Automation |
| G19 | A+ Content Management Module |
| H02 | Symptom/Ingredient Keyword Miner |
| H03 | Dietary Cross-Pollination Matrix |
| H08 | FBA Deadstock/Overstock Detector |
| H09 | Shelf-Life Aware Optimization |
| H10 | Condition-Based Ad Copy |
| R08 | Predicted vs Actual Tracker |
| R13 | User Trust Score Input |
| K07 | Keyword → Listing Optimizer |
| K08 | Keyword → Product Opportunity |
| E12 | Alliance/Staff System |
| W13 | Custom Rule Builder |
| GAP-20 | Portfolio-Level Management |
| GAP-21 | Brand vs Non-Brand Strategy |
| GAP-22 | Multi-Ad-Type (SP Brands, Display) |
| GAP-23 | Bulk Historical Import |

**PHASE 3 TOTAL: ~37 features**

---

## PHASE 4: ENTERPRISE (Future)

| ID | Feature |
|----|---------|
| R10 | Multi-Account/Agency Mode |
| A05 | WhatsApp Summary |
| A06 | WhatsApp Quick Commands |
| E05 | Extension/Plugin Module System |
| E06 | Multi-Account Support (+ master sync) |
| E07 | White-Label Reports |

**PHASE 4 TOTAL: 6 features**

---

## 📊 SUMMARY

| Phase | Focus | Features | Timeline |
|-------|-------|----------|----------|
| **1A** | Infrastructure | ~15 | Week 1 |
| **1B** | Core Pipeline | ~17 | Week 1-2 |
| **1C** | Actions & Reporting | ~39 | Week 2-3 |
| **2A** | Brain Layer | ~11 | Week 4 |
| **2B** | Advanced Intelligence | ~25 | Week 4-5 |
| **2C** | Protection & Competition | ~20 | Week 5-6 |
| **2D** | Growth & Automation | ~27 | Week 6-7 |
| **2E** | Web Panel & Integrations | ~22 | Week 6-7 |
| **3** | Advanced AI + Modules | ~37 | Week 8-10 |
| **4** | Enterprise | 6 | Future |
| **TOTAL** | | **~219** | |

> **Footnote:** Phase 2 and Phase 3 have deferred tech dependencies. ML libraries (LightGBM, Prophet, scipy, pandas, numpy), DB libraries (SQLAlchemy, Alembic), and LLM tech (Gemini/Ollama) are frozen in `DEFERRED_LIBRARIES.md`. These will only be unfrozen and added to requirements.txt when their respective phase build begins. Phase 1 runs entirely on the lean stack: Python 3.11, Flask, openpyxl, requests + JSON files.

---

## 🎯 Msir Action Required
1. Review this phase plan
2. Confirm or adjust feature phase assignments
3. Tell which features to build FIRST
4. Phase plan will then be locked in MASTER v10.0

---
*Phase Plan v10.0 | 12 April 2026 | Source: 360° Analysis Session*
