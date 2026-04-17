# Grow24 AI / GoAmrita - MASTER Future Module Standard v1.0
**Project Name:** Grow24 AI (formerly GoAmrita)  
**Date:** 15 April 2026  
**Purpose:** Standard for ALL NEW future modules/features only  
**Status:** ACTIVE for future development | Legacy modules remain unchanged for now

---

# 1. PURPOSE

This document is the **single standard** for all **new future modules/features** built from now onward.

It exists because:
- Current/legacy modules already use different JSON/report structures
- Future work will be handled mainly by AI tools, not human developers
- AI tools need clear written standards because they cannot safely depend on chat memory
- We do **NOT** want to confuse or break existing work
- We want **all new modules** to start following one clean, scalable architecture

## Golden Rule for this document

**Legacy modules stay as-is for now. New modules must follow this standard from day 1.**

Legacy migration will happen later, gradually, in a controlled phase.

## Future Code Location Rule

`ClaudeCode/Python` is the old beta/minimum-working-tool area.

All new future production modules must be created under the dedicated `Grow24_AI` architecture.

For Amazon marketplace modules, use:
```text
Grow24_AI/marketplaces/amazon/
```

For Amazon seller-side SP-API modules, use:
```text
Grow24_AI/marketplaces/amazon/seller_api/
```

If a required domain folder does not exist, the AI tool must create it before adding the module.

Do not place new future production modules in `ClaudeCode/Python` unless explicitly approved for a temporary compatibility bridge.

## Future Data / Report Location Rule

The permanent future data root is:
```text
Grow24_AI/data/
```

For Amazon marketplace reporting, the main future report folder is:
```text
Grow24_AI/data/amazon/reports/
```

`ClaudeCode/Report` is temporary compatibility storage only, not the permanent future storage home.

## Future Dashboard / Web Code Location Rule

Shared dashboard/web production code must not be placed in `ClaudeCode/Python`.

Its permanent future home is:
```text
Grow24_AI/core/dashboard/
```

Marketplace-specific readers/adapters may live under marketplace folders, but shared dashboard server, templates, rendering logic, and dashboard UI code belong under `Grow24_AI/core/dashboard/`.

## Future Feature Config Rule

`config_features.json` is the operational launch/control file for features.

For all new future modules/features, it must use controlled fields, correct `Grow24_AI` script locations, real dependencies, clear dashboard control settings, and `script_dir` when the module script lives outside `ClaudeCode/Python`.

---

# 2. SCOPE

## This document APPLIES TO
- All new future modules
- All new future features
- All new future dashboard-facing reports
- All AI tools working on new future project files

## This document DOES NOT FORCE CHANGES TO
- Existing scripts
- Existing JSON files
- Existing report formats
- Existing dashboard integrations

---

# 3. CORE PHILOSOPHY

This standard follows the MASTER architecture philosophy:

- **Automate business > Everything else**
- **Frontend = simple, business-focused**
- **Backend = powerful, structured, scalable**
- **Main Dashboard = business impact**
- **Activity Dashboard = system activity**
- **Raw outputs can vary**
- **Dashboard-facing outputs must be standardized**

## Key Design Decision

For future modules, we do **NOT** standardize raw internal data first.

Instead, every new module must produce:
1. Raw output
2. Impact Summary
3. Activity Summary
4. Registry Entry

This gives dashboard consistency without forcing every raw JSON to look the same.

## Two-Part Goal Rule

Every future goal/module should be designed in 2 parts:

1. Get Data
2. Take Action

Part 1 must detect, score, and publish findings.

Part 2 must decide whether action is allowed, then either:
- take the action
- or clearly record why action did not run

Self-action should be treated as enabled by default unless a future setting or safety rule disables it.

## Shared Action Reuse Rule

Future modules must not create duplicate action functions when a reusable action engine already exists.

Detector modules may be feature-specific, but action engines should be shared whenever possible.

If a feature finds an issue, it should route to the correct reusable action engine, or clearly record that no suitable engine exists yet.

---

# 4. TWO-DASHBOARD ARCHITECTURE

## Dashboard 1: Main Dashboard
**Purpose:** Show business impact of our intelligence, actions, and automations

This dashboard should answer:
- Did profit increase or decrease?
- Did we prevent loss?
- Did we reduce waste?
- Did rank improve or fall?
- Did Buy Box improve or worsen?
- What business effect did our system create?

### Main Dashboard should show
- Net profit impact
- Loss prevented
- Waste blocked
- Revenue protected
- Rank increase/decrease
- Buy Box impact
- Top winners
- Top risks
- Best action
- Worst action
- AI learning impact

## Dashboard 2: Activity Dashboard
**Purpose:** Show what the system did, ran, failed, created, or needs review

This dashboard should answer:
- Which modules ran?
- Which failed?
- Which reports were created?
- What is pending review?
- What errors/warnings happened?
- What is blocked?

### Activity Dashboard should show
- Run status
- Recent activity feed
- Pending review items
- Latest reports
- Errors/warnings
- Scheduler/infra state
- Execution history

---

# 5. STANDARD OUTPUT LAYERS FOR EVERY NEW MODULE

Every new future module must produce the following layers:

## Layer 1: Raw Output
- Module-specific internal data
- Can have custom structure
- Used for drill-down, analysis, debugging, advanced usage

## Layer 2: Impact Summary
- Standardized output for Main Dashboard
- Business effect only
- No technical noise
- If AI took or routed action, include one reusable `ai_action_summary`
- Do not create duplicate AI-benefit sections for the same module

## Layer 3: Activity Summary
- Standardized output for Activity Dashboard
- Operational/execution view only
- No business storytelling

## Layer 4: Registry Entry
- Standardized discovery layer
- Tells dashboard what exists, where it is, and where to show it

---

# 6. MANDATORY FLOW FOR EVERY NEW MODULE

Every new module should follow this lifecycle:

```text
Plan -> Register -> Build -> Run -> Save Raw Output -> Save Impact Summary
     -> Save Activity Summary -> Save Registry Entry
```

## Completion Rule

**A new module is NOT complete unless all 4 outputs exist:**
- Raw output
- Impact summary
- Activity summary
- Registry entry

---

# 7. STANDARD MODULE GROUPS

Every new module must declare one `module_group` from this list:

- `core_engine`
- `ads_optimization`
- `market_intelligence`
- `growth_engine`
- `listing_health`
- `pricing_profit`
- `inventory_fba`
- `review_feedback`
- `alerts_protection`
- `automation_control`
- `integration_sync`
- `ai_learning`

These groups are the standard grouping layer for future dashboards, reports, and discovery.

---

# 8. REQUIRED FILE OUTPUT PATTERN

For every new future module, recommended file naming pattern:

## Raw Output
```text
Json/<feature_key>_latest.json
Json/<feature_key>_<timestamp>.json
```

## Impact Summary
```text
Json/impact_<feature_key>_latest.json
Json/impact_<feature_key>_<timestamp>.json
```

## Activity Summary
```text
Json/activity_<feature_key>_latest.json
Json/activity_<feature_key>_<timestamp>.json
```

## Registry
```text
Json/report_registry_latest.json
```

If timestamped versions are stored, the `_latest` version must still exist for simple dashboard reading.

---

# 9. STATUS STANDARDS

All future modules must use these common status values:

## Run/Output Status
- `success`
- `partial`
- `warning`
- `failed`

## Impact Level
- `low`
- `medium`
- `high`
- `critical`

## Run Mode
- `manual`
- `scheduled`
- `event`
- `retry`

These values must be reused across all future modules without inventing new variations unless explicitly approved.

---

# 10. PRIORITY FRAMEWORK

For future modules, dashboard priority should be based on:

```text
priority_score = business_impact + urgency + confidence + strategic_weight
```

## Recommended weights
- Business Impact = 40%
- Urgency = 30%
- Confidence = 20%
- Strategic Weight = 10%

## Priority usage
- Homepage ordering
- Critical card ordering
- Review queue ordering
- Alert prominence

## Suggested score bands
- `90-100` = Critical
- `70-89` = High
- `40-69` = Medium
- `0-39` = Low

---

# 11. FEATURE REGISTRATION REQUIREMENT

Before any new module is built, developer must define:

- Feature ID
- Feature Key
- Feature Name
- Module Group
- Business Goal
- Input Sources
- Output Files
- Dashboard Target
- Impact Metrics
- Activity Metrics
- Approval Mode
- Risk Level
- Schedule / Freshness

No new module should start coding without this registration being defined first.

---

# 12. REQUIRED TEMPLATES FOR FUTURE MODULES

Every future module must follow these 4 standards:

## Companion Reference Files

- `GoAmrita_Future_Dashboard_Architecture_v1.0.md`
- `GoAmrita_Future_Module_Classification_and_Naming_v1.0.md`
- `GoAmrita_Future_Module_Registration_Template_v1.0.md`
- `GoAmrita_Future_Report_Templates_v1.0.md`
- `GoAmrita_Future_Report_Registry_Standard_v1.0.md`
- `GoAmrita_Future_JSON_Contract_v1.0.md`
- `GoAmrita_Future_Module_Build_Workflow_v1.0.md`
- `GoAmrita_Legacy_Module_Migration_Plan_v1.0.md`
- `GoAmrita_Future_Dashboard_Rendering_Rules_v1.0.md`
- `GoAmrita_AI_Only_Development_Protocol_v1.0.md`
- `GoAmrita_Future_Module_Location_Standard_v1.0.md`
- `GoAmrita_Future_Data_and_Report_Location_Standard_v1.0.md`
- `GoAmrita_Future_Dashboard_Code_Location_Standard_v1.0.md`
- `GoAmrita_Future_Feature_Config_Standard_v1.0.md`
- `GoAmrita_Future_Data_Collection_Standard_v1.0.md`
- `GoAmrita_Future_Action_Execution_Standard_v1.0.md`
- `GoAmrita_Future_Action_Reuse_and_Routing_Standard_v1.0.md`

## A. Feature Registration Template
Purpose:
- Planning layer before build
- Defines identity, business purpose, dependencies, outputs, dashboard placement, safety

## B. Impact Summary Template
Purpose:
- Main Dashboard output
- Must explain business effect only

## C. Activity Summary Template
Purpose:
- Activity Dashboard output
- Must explain execution/system activity only

## D. Registry Entry Template
Purpose:
- Dashboard discovery layer
- Must tell system what reports exist and where to show them

---

# 13. IMPACT SUMMARY RULES

Impact Summary is for the **Main Dashboard only**.

It must answer:
- What changed in business?
- What improved?
- What got worse?
- What value was protected, gained, or lost?
- Which entities are top winners or top risks?
- If AI took action, what benefit came from that action?

## AI Action Benefit Rule
- Future modules must reuse one standard `ai_action_summary` block inside Impact Summary
- Dashboard must reuse the existing AI benefit area for that module
- Do not create separate duplicate cards, duplicate sections, or repeated benefit storytelling for the same module
- Summary card may show one short AI benefit number
- Detail area may show item-level AI action details

## Impact Summary must NOT focus on
- Stack traces
- Retry logs
- Scheduler mechanics
- Technical system chatter
- Infra/internal processing detail

---

# 14. ACTIVITY SUMMARY RULES

Activity Summary is for the **Activity Dashboard only**.

It must answer:
- Did the module run?
- What inputs did it use?
- What files did it create?
- What warnings/errors happened?
- Does anything need review?
- Is anything blocked?

## Activity Summary must NOT focus on
- Profit storytelling
- Strategic conclusions
- Business impact interpretation
- Commercial recommendations unless explicitly needed for review

---

# 15. REGISTRY RULES

Registry Entry is the **dashboard discovery layer**.

Dashboards should use registry-based discovery for future modules instead of hardcoding file names.

## Registry should define
- Feature identity
- Report file paths
- Visibility (Main / Activity / Both)
- Section placement
- Priority score
- Critical state
- Review state
- Headline/badge/sort guidance

## Registry should be the source of truth for
- Which future module reports exist
- Which should show on home
- Which should show first
- Which need review

---

# 16. DASHBOARD TARGET RULE

Every new module must declare one of:
- `main`
- `activity`
- `both`

## Meaning
- `main` = business impact only
- `activity` = system activity only
- `both` = feature publishes both summaries and appears in both dashboards

---

# 17. APPROVAL / SAFETY RULE

Every new module must explicitly define:
- `approval_mode`
- `user_approval_required`
- `auto_action_allowed`
- `risk_level`
- `rollback_required`

This is mandatory even for “report-only” modules, because safety intent must be explicit.

---

# 18. LEGACY COMPATIBILITY RULE

This is one of the most important rules in this document.

## Current decision
- Existing modules remain unchanged for now
- Existing JSON/report formats remain unchanged for now
- Existing developers should not be disturbed/confused

## Standard applies only to
- New future modules
- New future reports
- New future dashboard integrations

---

# 19. FUTURE MIGRATION RULE FOR LEGACY MODULES

When old modules are migrated later, follow this order:

1. Keep raw legacy JSON unchanged initially
2. Create wrapper summaries first
3. Create registry entries for those modules
4. Verify dashboard works with wrapper layer
5. Only later consider raw-format cleanup if needed

## Important
Do **NOT** start legacy migration by rewriting old raw JSON first.

First add a wrapper summary layer, then migrate gradually.

---

# 20. MINIMUM REQUIRED FIELDS FOR FUTURE MODULES

At minimum, every future module must define:

## Identity
- `feature_id`
- `feature_key`
- `feature_name`
- `module_group`

## Dashboard
- `dashboard_targets`
- `main_dashboard_section`
- `activity_dashboard_section`

## Metrics
- `impact_metrics`
- `activity_metrics`

## Safety
- `approval_mode`
- `risk_level`

## Files
- Raw output path
- Impact summary path
- Activity summary path
- Registry entry

---

# 21. TEAM WORKING RULE

All future developers and AI tools working in this project should follow this rule:

```text
If module is legacy -> do not force new standard unless asked.
If module is new -> follow this standard fully.
```

This avoids confusion, protects current work, and keeps future architecture clean.

---

# 22. SHORT DEVELOPER CHECKLIST

Before building any new future module, confirm:

- [ ] This is a NEW module, not a legacy modification
- [ ] Feature registration is defined
- [ ] Module group is selected
- [ ] Dashboard target is selected
- [ ] Raw output path is defined
- [ ] Impact summary path is defined
- [ ] Activity summary path is defined
- [ ] Registry entry plan is defined
- [ ] Approval/risk mode is defined
- [ ] Priority logic is defined

If these are not defined, the module is not ready to build.

---

# 23. FINAL RULE

**From now onward, every new future module must be built in a way that it can be discovered, understood, and displayed without custom dashboard hacking.**

That is the purpose of this standard.

---

*MASTER Future Module Standard v1.0 | 15 April 2026*  
*Applies to NEW modules only | Legacy modules remain unchanged until planned migration phase*
