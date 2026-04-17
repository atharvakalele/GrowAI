# 📝 GoAmrita Ads — Discussion Changes Log v7.0
## All Changes Discussed After Blueprint Part 3 (FINAL) and MASTER v2.0
**Date:** 11 April 2026 | **Session:** Discussion Phase (no build yet)
**v4.0 Changes:** Round 6 — 19 new changes (Enterprise Architecture: AI Learning, Multi-Account, Alerts, Extensibility)
**v5.0 Changes:** Round 7 — 11 new changes (Data Intelligence: Report Import, Price Segment CORE, Organic Competition, Universal Import, Tech Validation)
**v6.0 Changes:** Round 8 — 16 new changes (User Management: Access Control, Performance, Admin Hierarchy, Bulk Ops, Build Philosophy)
**v7.0 Changes:** Round 9 — 29 new changes (Feature Expansion: 15 New Features, 11 Improvements, 1 Cleanup, W10→G09 Duplicate Fix)

---

# ROUND 1: Web Panel Feedback (12 changes)

| # | Topic | Old Design | New Design | Impact |
|---|-------|-----------|-----------|--------|
| 1 | **Browser/OS Notifications** | Email only | Browser Push + OS Desktop + Email (user chooses) | 🟡 New Feature |
| 2 | **Dashboard Redesign** | Amazon metrics copy | Strategy Impact Center — NOT Amazon data | 🔴 Major Redesign |
| 3 | **Category-Level COGS** | Product-level only | Account → Category → Product inheritance | 🔴 Architecture |
| 4 | **Default Product Settings** | Basic | Full control list with 11+ settings | 🟡 Detailed |
| 5 | **Auto-Pause Rules** | Unclear | Intelligent pause + Auto Re-Activate | 🟡 Clarified |
| 6 | **Budget Pacing** | Generic | Only advanced/custom pacing | 🟡 Confirmed |
| 7 | **Google Sheet Webhook** | CSV upload only | Google Sheet auto-fetch + Webhook + CSV | 🔴 New Feature |
| 8 | **Amazon API Keywords** | Not detailed | Priority order defined | 🟡 Confirmed |
| 9 | **AI Recommendation Field** | Single input | 3-column: Your Value / AI Recommends / Last Effect | 🔴 Major Enhancement |
| 10 | **Periodic Bid Updates** | Manual only | Manual / Semi-Auto / Full-Auto | 🟡 Detailed |
| 11 | **Zero-Config Install** | Required setup | Everything works out of box | 🟢 Core Principle |
| 12 | **Stock Low Options** | Either/or | BOTH: Option A + Option B | 🟡 Fixed |

---

# ROUND 2: Architecture & AI Deep Dive (19 changes)

| # | Topic | Old Design | New Design | Impact |
|---|-------|-----------|-----------|--------|
| 13 | **Returns % Default** | 3% | **15%** | 🟢 Config |
| 14 | **Weight → Shipping Fee** | Weight field | Shipping Fee field | 🟢 Field Rename |
| 15 | **3-Level Inheritance** | 2-level | **Account → Category → Product** | 🔴 Architecture |
| 16 | **Cooling Period Dual** | Days only | **Days OR Budget whichever first** | 🔴 Logic Change |
| 17 | **Sheet/CSV Match Type** | No match type | Match type column support | 🟢 Feature |
| 18 | **Semi-Auto Corrected** | Strong=auto, Weak=ask | **Strong+Weak BOTH auto, ask ONLY uncertain/risky** | 🟡 Mode Fix |
| 19 | **Multi-Marketplace** | Amazon only | **Adapter pattern** — Flipkart future | 🔴 Architecture |
| 20 | **AI Layer 1 (Rules)** | Basic rules | Pure logic, Day 1, ₹0 | 🟢 Confirmed |
| 21 | **AI Layer 2 (ML)** | Not defined | **LightGBM + Prophet + pandas + numpy + scipy** | 🔴 Tech Decision |
| 22 | **AI Layer 3 (LLM)** | Not defined | **Gemini 2.0 Flash** + Ollama fallback | 🔴 Tech Decision |
| 23 | **Python Version** | Not specified | **Python 3.11** | 🟢 Version Lock |
| 24 | **Layer Independence** | Not defined | Each layer works alone, Layer 3 optional | 🔴 Architecture |
| 25 | **Multi-Tag Decisions** | No tagging | Every decision tagged: layers + source + confidence | 🔴 Core Feature |
| 26 | **Permanent Rule Learning** | Basic learning | Action → Effect → Permanent → Cross-Learn | 🔴 Real AI |
| 27 | **Don't Blindly Restore** | Always restore | Keep if profitable | 🔴 Smart Logic |
| 28 | **Cross-Product Learning** | Not defined | Apply learnings to similar products | 🔴 Intelligence |
| 29 | **Stock Low Option B** | Restock signal | **Auto Price Update via SP-API** | 🔴 New Feature |
| 30 | **SP-API Separate Module** | Not defined | pricing.py, inventory.py, orders.py, etc. | 🔴 New Module |
| 31 | **Ads ↔ Seller Cross-Comm** | Separate systems | Joint decisions | 🔴 Architecture |

---

# ROUND 3: Final Refinements (11 changes)

| # | Topic | Old Design | New Design | Impact |
|---|-------|-----------|-----------|--------|
| 32 | **High Price Cooling** | 10 days | **12 days** | 🟢 Config |
| 33 | **Smart Match Type** | Manual | Auto by word count: 1-2→Phrase, 3+→Exact | 🟡 Smart Logic |
| 34 | **Campaign = Dropdown** | Text input | Dropdown select | 🟢 UX Fix |
| 35 | **Fetch Interval** | Not defined | Minute interval for Google Sheet | 🟢 Feature |
| 36 | **3 Keyword Modes** | Single source | A: API Smart, B: Sheet/CSV, C: Product Benefit | 🔴 Major Feature |
| 37 | **Mode C Detail** | Not defined | Product Benefit Targeting | 🔴 Healthcare AI |
| 38 | **Multi-Mode A/B Test** | Not defined | Run all modes → compare → keep winner | 🟡 Feature |
| 39 | **Gemini Flash Confirmed** | Under discussion | Gemini 2.0 Flash confirmed | 🟢 Confirmed |
| 40 | **Layer Tag Tracking** | Not defined | Track per-tag accuracy in dashboard | 🟡 Analytics |
| 41 | **Profit-per-Price Tracking** | Not defined | Track profit/day at each price point | 🔴 New Feature |
| 42 | **Effect = profit/day** | Basic tracking | Track per-day profit BEFORE and AFTER | 🟡 Enhancement |

---

# ROUND 4: API Version Lock & Feature Revisions (21 changes)

| # | Topic | Old Design | New Design | Impact |
|---|-------|-----------|-----------|--------|
| 43 | **Ads API Version** | "API v3" | **Ads API v1 (Unified)** + **Reporting v3** | 🔴 Critical Fix |
| 44 | **Gemini Version** | 2.0 Flash | **Gemini 2.5 Flash** (2.0 DEPRECATED!) | 🔴 Critical Fix |
| 45 | **Orders API Version** | Generic | **SP-API Orders v2026-01-01** | 🔴 Critical Fix |
| 46 | **Customer Feedback API** | Not in blueprint | **v2024-06-01** — review insights | 🔴 New API |
| 47 | **feedback.py Added** | Not in structure | `seller_api/feedback.py` | 🟡 New File |
| 48 | **SP-API Feeds** | Not specified | **v2021-06-30 — JSON ONLY** | 🟢 Version Lock |
| 49 | **SP-API Notifications** | Not detailed | **v1** — 4 event types | 🟢 Version Lock |
| 50 | **Library Version Lock** | Not exact | Python 3.11, Flask 3.1.3, LightGBM 4.6.0, etc. | 🟢 Version Lock |
| 51 | **P09 Source** | Generic | Customer Feedback API v2024-06-01 | 🟡 API Source |
| 52 | **P10 REVISED** | Manual + ACR + keyword | **100% auto, NO manual, NO ACR, NO keyword tracking** | 🔴 Major Revision |
| 53 | **G10 Source** | Generic | Customer Feedback API weekly snapshots | 🟡 API Source |
| 54 | **M09 BSR REVISED** | Keepa mentioned | **Manual sheet PRIMARY, SP-API fallback, Keepa REMOVED** | 🔴 Major Revision |
| 55 | **P07 Buy Box REVISED** | Simple pause | **Configurable bid reduction + auto price decrease cycle** | 🔴 Major Revision |
| 56 | **M04 Keyword Gap REVISED** | Generic | **4-approach, NO automation, approval required** | 🔴 Major Revision |
| 57 | **360° API Check** | Not done | 135/150 covered (90%), 6 gaps with workarounds | 🟢 Verification |
| 58 | **Brand Registered** | Not confirmed | **Confirmed ✅** | 🟢 Confirmed |
| 59 | **notifications.py** | Not in structure | `seller_api/notifications.py` | 🟡 New File |
| 60 | **feeds.py** | Not in structure | `seller_api/feeds.py` | 🟡 New File |
| 61 | **buybox_config.json** | Not in config | `config/buybox_config.json` | 🟡 New Config |
| 62 | **bsr_snapshots/** | Not in data | `data/bsr_snapshots/` | 🟡 New Folder |
| 63 | **review_snapshots/** | Not in data | `data/review_snapshots/` | 🟡 New Folder |

---

# ROUND 5: Keyword Fetcher, Database & Sheet Architecture (v3.0 NEW!)

| # | Topic | Old Design | New Design | Impact |
|---|-------|-----------|-----------|--------|
| 64 | **K06: Amazon Keyword Fetcher** | Not in blueprint | **ASIN/seed → Ads API v1 suggestions → SQLite → Sheet. Schedule configurable. Status filter: NEW or EMPTY.** | 🔴 New Feature |
| 65 | **K07: Listing Optimizer** | Not in blueprint | **Fetched keywords vs current listing → find missing → recommend/draft/auto-apply (configurable)** | 🔴 New Feature |
| 66 | **K08: Product Opportunity** | Not in blueprint | **Cluster analysis → product gaps → Gemini 2.5 Flash insight → Sheet** | 🔴 New Feature |
| 67 | **Status Filter** | Not defined | **"NEW" OR EMPTY** (both trigger processing) | 🟢 Logic Rule |
| 68 | **3-Layer Data Architecture** | Sheet only | **Sheet (input/output) + SQLite (truth) + Web Panel (control)** | 🔴 Architecture |
| 69 | **Database Choice** | No database | **SQLite + SQLAlchemy 2.0.x ORM** (DB-agnostic, migrate to PostgreSQL = 1 line) | 🔴 Tech Decision |
| 70 | **Alembic Migrations** | Not defined | **Alembic 1.13.x** for schema versioning | 🟢 Tech Decision |
| 71 | **GAS Webhook Security** | Not defined | **Simple secret key** (user-defined string, no OAuth) | 🟢 Confirmed |
| 72 | **K06 Schedule** | Not defined | **Configurable from menu** (Manual/6hr/12hr/Daily/2day/Weekly/Custom) | 🟢 Config |
| 73 | **K07 Apply Mode** | Not defined | **Configurable: Recommend Only (default) / Draft / Auto-Apply** | 🟡 Feature |
| 74 | **K07 Safety: Backend Only** | Not defined | **Default: Backend keywords only** (Title/Bullets optional, requires enable) | 🟡 Safety |
| 75 | **K07 Max Keywords** | Not defined | **Max 5 keywords per listing update** (configurable) | 🟢 Safety Limit |
| 76 | **K07 Rollback** | Not defined | **7-day rollback window** for listing changes | 🟢 Safety |
| 77 | **Per-Feature Sheet Config** | Single Sheet config | **Each feature: own Sheet ID, Tab, Columns, Webhook URL. Empty = default.** | 🔴 Architecture |
| 78 | **Default Sheet ID** | Not defined | **Single default Sheet ID used when feature-specific is empty** | 🟢 Config |
| 79 | **Tab + Column REQUIRED** | Not defined | **Tab Name and Column mapping ALWAYS required (no defaults)** | 🟢 Rule |
| 80 | **SQLite DB Schema** | Not defined | **6 tables: keyword_suggestions, listing_recommendations, product_opportunities, sync_status, sheet_configs + more** | 🔴 Schema |
| 81 | **sheet_manager.py** | Not in structure | `core/sheet_manager.py` — GAS webhook handler | 🟡 New File |
| 82 | **db_manager.py** | Not in structure | `core/db_manager.py` — SQLAlchemy operations | 🟡 New File |
| 83 | **keyword_fetcher.py** | Not in structure | `ads_api/keyword_fetcher.py` — K06 | 🟡 New File |
| 84 | **listing_updater.py** | Not in structure | `seller_api/listing_updater.py` — K07 | 🟡 New File |
| 85 | **opportunity_finder.py** | Not in structure | `ai/opportunity_finder.py` — K08 | 🟡 New File |
| 86 | **gas_webhook_template.js** | Not in project | `templates/gas_webhook_template.js` — user copies to Sheet | 🟡 New File |
| 87 | **database/ folder** | Not in structure | `database/goamrita.db + models.py + engine.py + migrations/` | 🔴 New Folder |
| 88 | **sheet_configs.json** | Not in config | `config/sheet_configs.json` — per-feature Sheet mapping | 🟡 New Config |
| 89 | **Batch Write Strategy** | Not defined | **50-100 rows per webhook POST** (not row-by-row) | 🟢 Performance |
| 90 | **API Rate Limit** | Not defined | **Max 5 req/sec** for keyword suggestions (safe margin) | 🟢 Performance |
| 91 | **DB Sync Strategy** | Not defined | **DB = truth, Sheet = display, incremental push via sheet_synced flag** | 🟡 Architecture |
| 92 | **Feature Count** | 150 | **153** (K06 + K07 + K08 added) | 🟢 Count |

---

# ROUND 6: Enterprise Architecture — AI Learning, Multi-Account, Alerts, Extensibility (v4.0 NEW!)

| # | Topic | Old Design | New Design | Impact |
|---|-------|-----------|-----------|--------|
| 93 | **Partner Seller Logic** | Not defined | Partner Buy Box win = OUR win, label seller name, alert on lost. Auto-sync ON/OFF per platform. Same logic on Amazon/Flipkart/Meesho. | 🔴 Architecture |
| 94 | **4-Level AI Learning** | Per-product learning only | **4-Level Hierarchy: Software (Global IQ) → Category → Product → Keyword.** NO seller level. Each level tagged: marketplace, category, price_range, season, product_type. IQ Score based on data volume + accuracy. | 🔴 Architecture |
| 95 | **Extensible Learning Levels** | Fixed levels | **3 core levels always (Software→Category→Product) + extensible** as needed: Keyword Level, Seller Account Level (daily sales monitoring, trends), Supplier Level (delivery, quality, NOT keyword-based but connected to product returns/reviews). | 🔴 Architecture |
| 96 | **Cross-Module AI Learning** | No cross-module | **Each module has OWN AI brain** (Ads AI, FBA AI, Sales AI, Buy Box AI, Listing AI, Review AI, Supplier AI). All feed into 4-Level Learning system (tagged). **Default = PASS learning to other modules.** Only exclude if 100% sure no effect. MAYBE = PASS (safe side). Passing unnecessarily = no harm. Excluding wrongly = missed insight. | 🔴 Architecture |
| 97 | **Cross-Learning Relevance Engine** | Not defined | **Weight-based system: Tier 1 (HIGH, direct) → auto-pass full influence. Tier 2 (LOW, indirect) → auto-pass reduced weight. Tier 3 (ZERO, 100% sure no effect, micro-level verified) → don't pass but re-evaluate periodically. Tier 4 (ASK) → developer at build time / user at runtime.** Weights auto-adjust based on actual data correlation. Tier promotion/demotion over time. | 🔴 Architecture |
| 98 | **Micro-Level Attribute Analysis** | Broad module-level | **Every module divided into sub-attributes** (e.g., Listing → Content vs Ranking vs Images). Effect check at micro-attribute level, NOT broad module level. "FBA→Listing Content" = ❌ but "FBA→Listing Ranking" = ✅. 360° angle required. | 🔴 Architecture |
| 99 | **Marketplace Tag in Learning** | Not tagged | **Marketplace tag mandatory** in software-level learning. Amazon/Flipkart/Meesho have different price zones, customer segments, competition patterns. Learning apply matches marketplace tag. | 🟡 Enhancement |
| 100 | **Review → Ad Prediction** | Not connected | **Review/Rating data = AI input feature** for ad performance prediction. Rating drops → predict CTR/conversion drop → proactively adjust bids. | 🟡 Enhancement |
| 101 | **Multi-Contact Support** | Single email | **Multiple emails + WhatsApp numbers.** Per-function contact optional — **if blank, auto-fill from account level** (reduce user work, full control). Per-function example: Ads alerts → email1, Stock alerts → email2. | 🟡 Enhancement |
| 102 | **WhatsApp → Last Phase** | Phase 3 | **Move to Phase 4 (Last Phase)** [OFF by default]. | 🟢 Config |
| 103 | **Multi-Account + One Login** | Single account | **One login for user** — self + partner accounts. One seller can have multiple accounts (same/different marketplace). **First-fill = master** — whichever account created first or filled first = sync source. Auto-sync to all sub-seller accounts. Each account editable/overridable. | 🔴 Architecture |
| 104 | **Easy Signup** | Not defined | **Only must-have info during registration** (name, email, password). All other details updatable in Settings later. Settings follow UI menu rule (Main/Advanced/Settings). | 🟢 Config |
| 105 | **Alliance/Staff System** | Not defined | **Role-based access:** Ads Staff, Pricing Staff, Listing Staff, Supplier, etc. Each task/function assignable to specific role. Notice/Alert per role. **Secondary staff enable/disable per alert type** — if primary not acknowledged, escalate to secondary. | 🔴 Architecture |
| 106 | **Smart Dynamic Scheduling** | Static schedule | **Event-based dynamic auto-run per module.** Normal schedule (default) → trigger event (lost/increase/decrease condition rules defined) → escalated schedule → take action → monitor → recovered → back to normal. Example: Buy Box every 30min → lost → every 5min → won back → 30min again. Each module configurable, defaults set. | 🔴 Architecture |
| 107 | **Alert Types — 4 Categories** | Basic alerts | **4 alert types per module:** Event-based (Buy Box lost, stock zero), Percentage change (ACoS +10%, Sales -30%), Fixed value change (CPC > ₹15, Stock < 10), Time-based (no sale in 48hrs). | 🟡 Enhancement |
| 108 | **Alert Notification System** | Basic notifications | **Custom voice per alert type, configurable volume level (low/med/high/max). Define critical notices. Critical alerts repeat until acknowledged.** Escalation chain: Primary user → not acknowledged → Secondary staff/user/supplier (if enabled). Browser/system notification. | 🔴 Architecture |
| 109 | **Per-Module AI** | Central AI only | **Each module has OWN dedicated AI learning.** Ads AI (bid patterns, keyword performance), FBA AI (qty prediction, restock timing), Sales Monitor AI (seasonal trends), Buy Box AI (price sensitivity), Listing AI (keyword impact on ranking), Review AI (rating trends on sales). All feed into 4-Level system. | 🔴 Architecture |
| 110 | **UI Tab Rule — Every Module** | Some pages only | **Main/Advanced/Settings tab structure applies to EVERY module.** Main = frequent work (clean), Advanced = rare required, Settings = module-specific defaults. | 🟢 Config |
| 111 | **Future-Proof Plugin Architecture** | Basic extensibility | **Every new feature automatically gets:** 3 automation modes (Full/Semi/Approval), Staff/Role assignment, Alert/Notice system, Google Sheet integration, AI Learning integration (4-level), Multi-account sync, Smart dynamic scheduling. Future scope: FBA automation, Listing optimization automation, ASIN-wise sales monitor, supplier PO management, anything. | 🔴 Architecture |

---

# ROUND 7: Data Intelligence — Report Import, Price Segment, Organic Competition, Universal Import (v5.0 NEW!)

| # | Topic | Old Design | New Design | Impact |
|---|-------|-----------|-----------|--------|
| 112 | **Report Import Module** | No historical data | **Import platform CSV/Excel reports (Amazon Business, Ads, Flipkart).** Tag as "old/historical" data. AI learns but with awareness — old data weight decreases over time. Compare before/after our system. Cold start solved! | 🔴 Architecture |
| 113 | **Price Segment = CORE Level** | Not in hierarchy | **CORE learning level added: Software → Category → Price Segment → Product.** Budget <₹199, Mid ₹200-499, Premium ₹500-999, Luxury ₹1000+. Configurable thresholds. Price fundamentally changes everything. | 🔴 Architecture |
| 114 | **Seller Account Level — Limited** | Removed in R6 | **Keep as EXTENSIBLE but LIMITED:** daily total sales tracking (up/down), week/month trends, account health. NOT deep product/keyword level. Auto-activates with 2+ sellers. | 🟡 Enhancement |
| 115 | **Tech Stack Validated** | Not verified | **✅ 100% capable, no switch needed.** Python 3.11 (#1 for AI/ML), LightGBM (Microsoft, industry standard), Prophet (Meta), SQLite→PostgreSQL (proven path), Flask (right-sized). Used by Amazon, Flipkart, Uber, Spotify for bigger problems. | 🟢 Confirmed |
| 116 | **All Tools FREE** | Not confirmed | **₹0 Phase 1-3.** All open source (MIT/BSD/Public Domain). Gemini free tier sufficient. Phase 4: ₹500-2000/mo (server only). | 🟢 Confirmed |
| 117 | **HIGH-WEIGHT Tags** | Not defined | **7 auto-calculated tags:** Rating Band, Competition Density, Product Lifecycle, Fulfillment Type (FBA/Self), Seasonality, Sales Velocity (7-day avg), Marketplace. Tags = flexible, extensible. Core levels = stable, fundamental. | 🔴 Architecture |
| 118 | **Competition = Search Term Level** | ~~ASIN seller count~~ | **ASIN seller count REMOVED** (99% sole seller, irrelevant). Competition measured at **search term level** — aggregated across all campaigns. Ads Reporting v3 (Impression Share, Click Share, CPC trend) + Brand Analytics (top 3 ASINs). | 🔴 Architecture |
| 119 | **Organic Competition — API Found!** | "No API available" | **✅ API available!** Search Catalog Performance Report (impressions, clicks, cart adds, purchases per ASIN per search term). Sales & Traffic Report (page views, sessions, conversion). Brand Analytics (top search terms). Manual rank via Google Sheet fallback. Weight-based score formula with auto-normalize. | 🔴 Architecture |
| 120 | **Universal Import Rule** | Per-feature import | **EVERY data import = 2 options always:** (1) Excel/CSV upload (recommended frequency per type), (2) Google Sheet link (auto-sync, default frequency). ALWAYS ignore duplicates (dedup by unique key). Templates downloadable from website. A1 = REPORT_ID for auto-detect. Column headers → auto-map. Phase 1: user imports Excel template to Google Sheet then links. | 🔴 Architecture |
| 121 | **Template System** | Not defined | **Every import/export type has downloadable template.** Row A1 = REPORT_ID (system auto-detects data type). Row 2 = column headers (auto-map). Missing columns → NULL (no error). Extra columns → ignored. Data validation before import. Preview: "45 new, 12 updates, 8 skipped." | 🟡 Enhancement |
| 122 | **Export/Report System** | Not detailed | **⏳ DEFERRED — will discuss deeply in separate round.** Major concern, needs dedicated discussion. | 🟡 Deferred |

---

# ROUND 8: User Management — Access Control, Performance, Admin Hierarchy, Bulk Ops, Build Philosophy (v6.0 NEW!)

| # | Topic | Old Design | New Design | Impact |
|---|-------|-----------|-----------|--------|
| 123 | **Module-Based Access Permission** | Basic staff roles | **Per-user module assignment with permission levels: View Only / Edit / Full Action / No Access.** Each staff can be assigned multiple modules. Admin decides who sees/manages what. | 🔴 Architecture |
| 124 | **3-Level Admin Hierarchy** | Single admin | **Software Super Admin (GOD mode, all accounts, all settings) → Account Admin (unlimited per account, manage users/modules/marketplaces within account) → User/Staff (only assigned modules/accounts/marketplaces).** | 🔴 Architecture |
| 125 | **User Registration & Approval** | Not defined | **Admin adds staff to their account directly. Other sellers register on website but ONLY Software Super Admin can approve.** Everything in control, no unauthorized access. | 🔴 Architecture |
| 126 | **Performance Score — 30-Day Rolling Window** | Not defined | **Auto-calculated performance based on: tasks on time, recommendations acted on, task completion time, priority tasks on time.** Any new module assigned → auto-includes in performance. 30-day rolling window — delay stays on account for 30 days then auto-clears. Admin configurable weights with sensible defaults. | 🔴 Architecture |
| 127 | **Performance Visibility — Rank Only** | ~~Loss shown to user, Profit to admin~~ | **BOTH admin and user see RANK ONLY (e.g., 75/100).** No loss/profit attribution to users. Score + Rank + "what to do to improve" — that's it. Minimal, motivating, non-distracting. | 🔴 Architecture |
| 128 | **User Screen Layout** | Not defined | **TOP = Pure work area (module-based auto tabs/sections). Performance on 2nd/3rd tab or bottom. Bottom bar: "3 pending \| Score: 75 \| 1 overdue ⚠️".** Show time urgency, delay effects on performance. Motivate to work on time. Keep SHORT — don't distract from work. | 🟡 Enhancement |
| 129 | **Notification System — Event-Based Configurable** | Task assigned/due/overdue only | **Any account event can trigger notification. Admin configures: which event, which priority/urgency, who gets notified.** Not just tasks — Buy Box lost, stock low, any event. Smart frequency: performance-based (low score = more reminders). | 🟡 Enhancement |
| 130 | **Reminder Channels** | Email only | **Default = Email (login email). WhatsApp number = optional field (store now, integrate in future phase).** Architecture ready for WhatsApp, build later. | 🟢 Config |
| 131 | **Acknowledgement = Task Completion** | Track notification click time | **Don't track notification acknowledge time. Track TASK COMPLETION TIME only.** Web/system notifications can be acknowledged, email can't — so universal metric = when task was completed. Task complete = auto-acknowledged. | 🟡 Enhancement |
| 132 | **Leave System** | Not defined | **7-day advance leave application required → offline time NOT counted in performance. No advance leave → offline time COUNTED.** Emergency = call admin, admin approves. | 🟢 Config |
| 133 | **User Account Lifecycle** | Not defined | **Active → Disabled (access off, data preserved) → Deleted.** Admin can delete anytime. Auto-delete after 12 months of disabled. **AI learning data ALWAYS preserved** — user delete must NOT affect AI learning. | 🟡 Enhancement |
| 134 | **Bulk Operations — Universal Pattern** | Not defined | **EVERY page, EVERY module: Search (auto if >10 items), Select All/Individual checkboxes, Bulk Action dropdown, One-Click Apply, Selected count.** Admin bulk: assign modules/accounts/marketplaces to multiple users. Applies everywhere — products, keywords, alerts, imports, users, ALL lists. | 🔴 Architecture |
| 135 | **Audit Trail** | Not defined | **Every user action logged: who, when, what.** Preserved even after user deletion. Required for performance calculation and accountability. | 🟡 Enhancement |
| 136 | **Performance Trend** | Not defined | **Improving ↑ / Stable → / Declining ↓ shown to both admin and user.** Smart notification: low performance → more reminders, high → fewer. Auto-escalation if consistently low. | 🟡 Enhancement |
| 137 | **Grace Period** | ~~7 days default~~ | **REMOVED.** Performance counts from Day 1. Keep it simple. | 🟢 Config |
| 138 | **🔴 BUILD PHILOSOPHY (Golden Rule)** | Not defined | **"Automate business > Everything else."** Architect features fully but build from MINIMUM, scale on the go. Fundamentals must be STRONG so scaling later requires NO rewrites. Easy to implement, easy to test, easy to scale. If a feature doesn't directly BOOST or AUTOMATE business → reconsider. Phase-wise development starting from this round. | 🔴 Architecture |

---

# ROUND 9: Feature Expansion — New Features, Improvements, Duplicate Cleanup (v7.0 NEW!)

## 🟢 IMPROVE — Existing Feature Description Enhancements (11 changes)

| # | Topic | Old Description | New Description | Impact |
|---|-------|----------------|----------------|--------|
| 139 | **C17 Dayparting + Bid Schedule** | "AI-learned per-ASIN heatmap, not fixed hours" | "Dayparting + Bid Schedule — AI-learned per-ASIN heatmap **Day+Hour combination**, not fixed hours" | 🟡 Enhancement |
| 140 | **C18 Placement Modifier + Dynamic** | "TOS vs Product Pages analysis + auto-optimize" | "Placement Modifier Engine — TOS vs Product Pages analysis + **dynamic modifiers per campaign/product, AI learns best placement**" | 🟡 Enhancement |
| 141 | **M01 Price Monitor + War Detection** | "Daily price tracking of top 5 competitors" | "Competitor Price Monitor — Daily tracking + **price war pattern detection + auto-protect alert trigger**" | 🟡 Enhancement |
| 142 | **M03 ASIN Targeting + Data-Driven** | "Target competitor product pages with lower ratings" | "Competitor ASIN Targeting — **Data-driven** selection, target pages with lower ratings, **higher price, poor reviews. AI learns best targets**" | 🟡 Enhancement |
| 143 | **G08 Launch Autopilot + Deal/Coupon** | "Automated 30-day launch sequence (configurable)" | "New Product Launch Autopilot — 30-day launch sequence + **auto-apply Deal/Coupon if available on launch**" | 🟡 Enhancement |
| 144 | **K07 Listing Optimizer + More Fields** | "Compare keywords vs listing → recommend" | "Keyword → Listing Optimizer — Compare keywords vs listing → **Backend + Description (unlimited) + Features/Bullets + all input fields. Recommend/draft/auto-apply**" | 🟡 Enhancement |
| 145 | **H08 Deadstock + Smart Actions** | "Overstock → push to Aggressive mode" | "FBA Deadstock/Overstock Detector — Detect + **review analysis + price adjustment suggestion + auto-run campaign + escalation**" | 🟡 Enhancement |
| 146 | **H09 Shelf-Life + H08 Integration** | "Expiring → aggressive clearance mode" | "Shelf-Life Aware Optimization — Expiring → **clearance mode + integrates with H08 for combined dead/overstock actions**" | 🟡 Enhancement |
| 147 | **W05 Budget Redistribution + Smart** | "Move money from losers → winners" | "Auto Budget Redistribution — **ROAS + TACoS scoring. Modes: Conservative/Balanced/Aggressive/AI. Min floor. Respects P17 cap**" | 🟡 Enhancement |
| 148 | **H01 Seasonal + Festival Control** | "Winter→immunity, Summer→hydration" | "Seasonal Health Demand — **Default DISABLED. Activates with approval before festival. Monitor ROI after**" | 🟡 Enhancement |
| 149 | **I18 Seasonal Predictor + Festival** | "Auto-keyword priority" | "Seasonal Demand Predictor (Prophet) — **Festival prep integration. 30-day advance prediction. Disabled default**" | 🟡 Enhancement |

## 🟢 PRESET — Alert Configuration Addition (1 change)

| # | Topic | Old Design | New Design | Impact |
|---|-------|-----------|-----------|--------|
| 150 | **A13 Sales Velocity Alert Preset** | Generic 4-type alert engine | **Add default alert preset: "Sales drop >50% in 24hrs → P1 Critical alert"** as pre-configured rule in A13 | 🟢 Config |

## 🟣 NEW — Genuinely New Features (15 changes)

| # | Topic | New Feature ID | Description | Impact |
|---|-------|---------------|-------------|--------|
| 151 | **Profit % Cap System** | **P17** | Account level + Product level cap: "Spend max X% of true profit on ads." Different from P14 (payout-based). | 🔴 Architecture |
| 152 | **Dead Campaign Auto-Cleanup** | **W11** | AI auto-detect zero-sale campaigns → auto-pause/cleanup. Different from C25 (manual exclude). | 🔴 Architecture |
| 153 | **Match Type Migration** | **K09** | AI analyzes existing keywords with historical data → detect wrong match type → migrate. Different from K04 (creation-time) and C19 (funnel). | 🔴 Architecture |
| 154 | **Repeat Purchase Tracker** | **G13** | Track customer reorder patterns per product → predict reorder timing → optimize ads for LTV. Different from G05 (S&S specific). | 🟡 Enhancement |
| 155 | **Listing Health Score** | **G14** | Single 0-100 score per listing: images + keywords + A+ + description + compliance. Quick view across 300 products. | 🔴 Architecture |
| 156 | **A+ Content Impact Tracker** | **G15** | Measure A+ content effect on conversion → before/after comparison → justify A+ investment. | 🟡 Enhancement |
| 157 | **Competitor Launch Alert** | **M11** | Detect new competitor in your keywords/category → alert before ranking impact. Opposite of M02 (stock-out). | 🟡 Enhancement |
| 158 | **Supplier Performance Scorer** | **I29** | Score suppliers: delivery time, quality (return rate), reliability, price consistency. Connected to product returns/reviews. | 🟡 Enhancement |
| 159 | **Long-Term Storage Fee Avoidance** | **H11** | Predict WHEN FBA storage fees hit per product → alert + auto-action before fees. Different from H08 (quantity). | 🟡 Enhancement |
| 160 | **Product Health Score (Master)** | **I30** | Single 0-100 per PRODUCT: sales velocity + profitability + review health + listing quality + ad efficiency + stock. Priority dashboard for 300 products. | 🔴 Architecture |
| 161 | **Anomaly Detection 3-Level** | **I31** | Product + Account + Campaign level anomaly detection. CPC spikes, click variance, order anomalies. Broader than P01/P02. | 🔴 Architecture |
| 162 | **Weekly AI Summary Report** | **R16** | Compiled weekly intelligence: all actions, auto-approved effects, call to action with reasons. Actionable insights. | 🟡 Enhancement |
| 163 | **Image Quality & Compliance** | **P18** | Auto-check: image count, resolution, white background, infographic, Amazon compliance. Alert on issues. | 🟡 Enhancement |
| 164 | **Return Rate Analyzer + Auto-Action** | **I32** | Product-level return monitoring → threshold → auto-reduce ad spend + root cause (Customer Feedback API). Different from I20 (keyword-level). | 🔴 Architecture |
| 165 | **Non-Performing Listing Smart** | **W12** | No order in X days (user OR AI defined) → auto-diagnose: Buy Box? Stock? Listing? Price? Reviews? Ads? → trigger existing features. | 🔴 Architecture |

## 🧹 CLEANUP — Duplicate Fix (2 changes)

| # | Topic | Old State | New State | Impact |
|---|-------|----------|----------|--------|
| 166 | **W10 → G09 Merge** | W10 and G09 were duplicates: both "New ASIN → auto create campaign" | **W10 description: "→ See G09 (merged, was duplicate)". G09 keeps as primary.** No logic lost — W10 had no unique logic beyond G09. | 🟢 Cleanup |
| 167 | **G09 Description Update** | "New ASIN detected → auto create campaign in set mode" | "New Listing Auto-Campaign — New ASIN detected → auto create **optimized** campaign in set strategy mode" | 🟢 Cleanup |

## ⏭️ DEFERRED TO NEXT ROUND (noted, not implemented)

| Topic | Reason |
|---|---|
| Feature categorization, grouping, filter, search on website | Cross-cutting requirement — needs Decision Engine discussion first |
| Cross-feature data passing architecture | Cross-cutting requirement — needs orchestration layer |
| Smart logic that improves over time per feature | Cross-cutting requirement — tied to learning engine |
| Importance + critical event-based auto-sorting | Cross-cutting requirement — needs priority framework |

---

# SUMMARY STATISTICS

| Category | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | Total |
|----------|----|----|----|----|-----|-----|-----|-----|-----|-------|
| 🔴 Architecture/Critical | 4 | 11 | 3 | 8 | 8 | 12 | 6 | 6 | 8 | **66** |
| 🟡 Enhancements/New Files | 5 | 1 | 3 | 7 | 8 | 4 | 3 | 7 | 18 | **56** |
| 🟢 Config/Confirmations | 3 | 7 | 5 | 6 | 13 | 3 | 2 | 3 | 3 | **45** |
| **Total** | **12** | **19** | **11** | **21** | **29** | **19** | **11** | **16** | **29** | **167** |

---

# DOCUMENTS UPDATED

| Document | Old Version | New Version | Status |
|----------|------------|------------|--------|
| MASTER Feature Registry | v8.0 (153+ features) | **v9.0 (168+ features)** | ✅ Updated |
| Web Panel Design | v7.0 | **v8.0** | ✅ Updated |
| Discussion Changes Log | v6.0 (138 changes) | **v7.0 (167 changes)** | ✅ Updated |

---

*Discussion Changes Log v7.0 | 11 April 2026*
*167 Changes | 9 Discussion Rounds | All captured in updated blueprints*
*Round 9: 15 new features + 11 improvements + 1 preset + 2 cleanup = 29 changes*
*Note: Export/Report system deferred to separate deep-dive discussion*
*Note: Cross-cutting requirements (orchestration, data passing, auto-sorting) deferred to Round 10*
*Golden Rule: "Automate business > Everything else" — Architect fully, build minimum, scale on go*
