# Grow24 AI / GoAmrita - Future Module Build Workflow v1.0
**Project Name:** Grow24 AI (formerly GoAmrita)  
**Date:** 15 April 2026  
**Purpose:** Step-by-step workflow for building ALL NEW future modules/features

---

# 1. PURPOSE

This document converts the future-module standards into a practical build process.

It tells AI tools:
- what to read before building
- how to register a module
- how to classify it
- how to define outputs
- how to validate it
- how to avoid disturbing legacy modules
- how to leave a safe handoff for the next AI tool

This applies only to **new future modules/features**.

---

# 2. GOLDEN RULE

```text
Legacy modules stay untouched unless explicitly approved.
New modules must follow the future-module standard fully.
```

Do not rewrite legacy JSON, legacy reports, or legacy dashboard behavior as part of a new future module unless specifically asked.

---

# 3. REQUIRED READING BEFORE BUILD

Before building any new future module, read in this order:

1. `Learning And Rule/QUICK_RECALL.md`
2. `GoAmrita_MASTER_Future_Module_Standard_v1.0.md`
3. `GoAmrita_AI_Only_Development_Protocol_v1.0.md`
4. `GoAmrita_Future_Module_Location_Standard_v1.0.md`
5. `GoAmrita_Future_Data_and_Report_Location_Standard_v1.0.md`
6. `GoAmrita_Future_Dashboard_Code_Location_Standard_v1.0.md`
7. `GoAmrita_Future_Feature_Config_Standard_v1.0.md`
8. `GoAmrita_Future_Data_Collection_Standard_v1.0.md`
9. `GoAmrita_Future_Action_Execution_Standard_v1.0.md`
10. `GoAmrita_Future_Action_Reuse_and_Routing_Standard_v1.0.md`
11. `GoAmrita_Future_Module_Registration_Template_v1.0.md`
12. `GoAmrita_Future_Module_Classification_and_Naming_v1.0.md`
13. `GoAmrita_Future_JSON_Contract_v1.0.md`
14. If dashboard-facing: `GoAmrita_Future_Dashboard_Architecture_v1.0.md`
15. If report-facing: `GoAmrita_Future_Report_Templates_v1.0.md`
16. If registry-facing: `GoAmrita_Future_Report_Registry_Standard_v1.0.md`

---

# 4. BUILD WORKFLOW

## Step 1: Confirm Module Type

Decide whether the work is:
- new future module
- legacy module improvement
- legacy migration wrapper

If it is legacy work, do **not** force the new standard unless explicitly approved.

## Step 2: Register the Module

Create/define feature registration before coding.

Minimum required:
- feature id
- feature key
- feature name
- module group
- business goal
- data goal
- action goal
- input sources
- output files
- dashboard target
- impact metrics
- activity metrics
- approval mode
- risk level
- schedule/freshness

## Step 2A: Choose Correct Code Location

Do not put new production modules in `ClaudeCode/Python`.

For Amazon seller-side modules, create/use the correct folder under:

```text
Grow24_AI/marketplaces/amazon/seller_api/
```

Examples:
- `fba`
- `market_intelligence`
- `pricing_profit`
- `listing_health`
- `ads_optimization`

If the module is launched from `config_features.json`, add `script_dir` with the module folder path.

## Step 2B: Choose Correct Data / Report Output Root

Do not treat `ClaudeCode/Report` as the permanent future report home.

For future Amazon modules, use:

```text
Grow24_AI/data/amazon/reports/
```

Required structure:
- `latest/json/`
- `<dated folder>/json/`
- `latest/excel/` if needed
- `<dated folder>/excel/` if needed
- `latest/html/` if needed
- `<dated folder>/html/` if needed

## Step 2C: Choose Correct Dashboard / Web Code Location

If the task is dashboard/web/server work, do not place new production code in `ClaudeCode/Python`.

Use:

```text
Grow24_AI/core/dashboard/
```

Use marketplace folders only for marketplace-specific adapters/readers, not for shared dashboard UI/server logic.

## Step 2D: Add Correct Feature Config Entry

If the module is launchable from operational controls or scheduler, add/update its `config_features.json` entry using the future config standard.

Minimum expectations:
- stable `id`
- clear `name`
- exact `script`
- correct `script_dir` for `Grow24_AI` modules
- real `category`
- valid `schedule`
- `schedule_time` when needed
- realistic `freshness_hours` when applicable
- true dependency list
- intentional `dashboard_button`, `button_label`, and `button_color`
- `enabled` state

Do not use `config_features.json` as a substitute for report registry or module output contracts.

## Step 2E: Split Goal Into 2 Parts

Before coding, define:
- Part 1 = what data will be collected and what findings will be published
- Part 2 = what action will happen after findings are created

For Part 2, also define:
- whether self-action is allowed
- what setting disables self-action
- what result status is recorded if action is skipped or blocked

## Step 2F: Check Reusable Action Engines First

Before designing a new fix/action function, check whether a reusable action engine already exists.

If a reusable action engine exists:
- route to it
- do not create a duplicate action function

If the existing action engine is not enough:
- extend it safely
- avoid breaking the older feature that already uses it
- document the compatibility decision

## Step 3: Classify the Module

Choose one:
- impact-heavy
- activity-heavy
- mixed

This decides:
- dashboard target
- required summaries
- priority behavior
- review behavior

## Step 4: Define Output Files

For every new module, define:

## Raw output
```text
Json/<feature_key>_latest.json
Json/<feature_key>_<timestamp>.json
```

## Impact summary
```text
Json/impact_<feature_key>_latest.json
Json/impact_<feature_key>_<timestamp>.json
```

## Activity summary
```text
Json/activity_<feature_key>_latest.json
Json/activity_<feature_key>_<timestamp>.json
```

## Registry
```text
Json/report_registry_latest.json
```

## Step 5: Build Raw Output

Raw output can be module-specific.

Rules:
- keep it clear
- keep it stable for the module
- avoid mixing dashboard display logic into raw output

## Step 6: Build Impact Summary

Required if module affects:
- profit
- loss prevention
- waste blocking
- Buy Box
- rank
- conversion
- stock risk
- customer trust
- organic movement
- strategic decisions

Impact summary must answer:
```text
What business impact happened?
```

If the module takes action or routes action, also add one reusable `ai_action_summary` block inside Impact Summary.

Do not create a second duplicate AI benefit section for the same module.

## Step 7: Build Activity Summary

Required if module:
- runs on schedule
- processes data
- calls APIs
- creates reports
- triggers alerts
- creates approvals
- can fail or partially fail

Activity summary must answer:
```text
What system activity happened?
```

## Step 8: Build Registry Entry

Registry entry must define:
- where report files are
- which dashboard should show them
- priority
- review state
- critical state
- display headline

Dashboard discovery must use registry, not hardcoded file guessing, for future modules.

## Step 9: Validate JSON Contracts

Check:
- required fields exist
- schema type is correct
- schema version is present
- allowed values are used
- timestamps are present
- file references are valid
- dashboard visibility matches available summaries

## Step 10: Test Safe Run

At minimum:
- run module with small input if possible
- verify raw output exists
- verify impact summary exists if required
- verify activity summary exists if required
- verify registry entry exists
- verify errors are captured instead of crashing silently

## Step 11: Document Delivery

Final delivery note should mention:
- files created
- output files generated
- test performed
- warnings/limitations
- whether legacy modules were untouched

---

# 5. APPROVAL AND SAFETY WORKFLOW

Every module must define:
- `approval_mode`
- `user_approval_required`
- `auto_action_allowed`
- `risk_level`
- `rollback_required`

## Default for new modules
If unsure:
```text
approval_mode = recommend_only
auto_action_allowed = false
```

Only move to semi-auto or full-auto after explicit approval and safety design.

---

# 6. DASHBOARD WORKFLOW

## Strategy Impact Dashboard
Use Impact Summary only.

Do not read raw output directly for high-level business cards unless explicitly needed.

## Activity Dashboard
Use Activity Summary only.

Do not mix business storytelling into operational run status.

## Registry
Use Registry as the discovery layer.

---

# 7. LEGACY SAFETY WORKFLOW

When building a new future module:
- do not rename existing files
- do not delete existing files
- do not rewrite legacy JSON formats
- do not change legacy dashboard assumptions
- do not migrate old modules unless asked

If a future module needs old data:
- read legacy data as input
- write new standardized output separately
- keep old data unchanged

---

# 8. VALIDATION CHECKLIST

Before marking future module complete:

- [ ] Feature registration exists
- [ ] Module group selected
- [ ] Classification selected
- [ ] Dashboard target selected
- [ ] Raw output written
- [ ] Impact summary written if required
- [ ] Activity summary written if required
- [ ] Registry entry written
- [ ] JSON contract validated
- [ ] Safe failure behavior tested
- [ ] Legacy modules not disturbed
- [ ] Delivery notes written

---

# 9. COMMON MISTAKES TO AVOID

- Building UI directly from raw JSON
- Mixing business impact and activity logs in one file
- Creating custom status values
- Forgetting registry entry
- Changing legacy module output while building a future module
- Making a module auto-action capable without approval/risk design
- Showing technical logs on Strategy Impact Dashboard
- Showing profit storytelling on Activity Dashboard

---

# 10. FINAL RULE

For new future modules:

```text
Plan first.
Register first.
Classify first.
Then build.
```

This prevents architecture drift and protects current work.

---

*Future Module Build Workflow v1.0 | 15 April 2026*  
*For NEW future modules only | Legacy modules remain unchanged until planned migration phase*
