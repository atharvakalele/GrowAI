# Grow24 AI / GoAmrita - Future Feature Config Standard v1.0
**Project Name:** Grow24 AI (formerly GoAmrita)  
**Date:** 15 April 2026  
**Purpose:** Standard rules for `config_features.json` so future AI tools register and launch features consistently

---

# 1. PURPOSE

`config_features.json` is the operational control file for launchable features.

It tells the system:
- what feature exists
- where its script lives
- how it should run
- whether it appears on dashboard controls
- what it depends on
- how fresh the output should be

This file is not the business-logic home of a module.

It is the **feature control and launch registry**.

---

# 2. CORE RULE

For all new future modules/features:
- module architecture must follow the master future standards
- output files must follow the JSON/report/registry standards
- `config_features.json` must only describe how the feature is launched, scheduled, shown, and controlled

Do not use `config_features.json` as a replacement for:
- module registration documents
- report registry files
- dashboard rendering rules
- module business logic

---

# 3. WHAT `config_features.json` SHOULD CONTROL

`config_features.json` should control:
- feature id/key
- display name
- script file
- script folder location
- args passed to the script
- category
- schedule mode
- schedule time if applicable
- freshness expectation
- dependencies
- self-action setting if the feature can act automatically
- action route/engine if findings should be handed to another reusable action module
- whether dashboard shows a run button
- button label/color
- whether feature is enabled
- alert behavior if the feature detects issues

It should not be used to store:
- raw report payloads
- dashboard card content
- impact summary data
- activity summary data
- registry entries
- permanent business learning/rules

---

# 4. REQUIRED FEATURE ENTRY SHAPE

Every launchable feature entry should follow this structure:

```json
{
  "id": "competitor_tracker",
  "name": "Competitor Tracker",
  "script": "competitor_tracker_v1.0.py",
  "script_dir": "Grow24_AI/marketplaces/amazon/seller_api/market_intelligence",
  "args": [],
  "category": "market_intelligence",
  "schedule": "daily",
  "schedule_time": "09:45",
  "freshness_hours": 24,
  "depends_on": ["import", "pricing"],
  "dashboard_button": true,
  "button_label": "Track Competitors",
  "button_color": "blue",
  "enabled": true,
  "alert_on_issue": true,
  "note": "Tracks competitor pressure and Buy Box risk."
}
```

---

# 5. FIELD RULES

## Required for all future launchable features

- `id`
- `name`
- `script`
- `args`
- `category`
- `schedule`
- `depends_on`
- `dashboard_button`
- `button_label`
- `button_color`
- `enabled`

## Required when applicable

- `script_dir`
  Use this when the script is outside `ClaudeCode/Python`.
  For all new future production modules under `Grow24_AI`, this should normally be present.

- `schedule_time`
  Required when `schedule` uses a daily time-driven run.

- `freshness_hours`
  Required for features whose outputs are expected to stay fresh for a measured period.

- `alert_on_issue`
  Required for monitoring/risk-detection features where the system should raise attention on issues.

- `self_action_enabled`
  Required for future operational features that may take automated follow-up action.
  Default future value should be `true` unless a safety/business rule says otherwise.

- `action_engine`
  Recommended for detector modules that should route findings into an existing reusable action engine.

- `note`
  Recommended whenever a short operational explanation helps future AI tools.

---

# 6. FIELD DEFINITIONS

## `id`

Stable machine key for the feature.

Rules:
- lowercase
- underscore-separated
- no spaces
- do not change casually after adoption

Example:
```text
competitor_tracker
```

## `name`

Human-readable feature name for dashboard/admin views.

Example:
```text
Competitor Tracker
```

## `script`

Exact script filename that launches the feature.

Example:
```text
competitor_tracker_v1.0.py
```

## `script_dir`

Folder path from project root to the script location.

For new future production modules, use the dedicated architecture path such as:

```text
Grow24_AI/marketplaces/amazon/seller_api/<domain_folder>
```

Do not omit `script_dir` for new `Grow24_AI` modules.

## `args`

Default argument list passed to the script when launched from the control system.

Rules:
- use array form
- keep arguments explicit
- do not hide critical operating behavior only in free-text notes

Example:
```json
["--preview"]
```

## `category`

Operational grouping for dashboard, scheduler, and organization.

Prefer stable, architecture-aligned names such as:
- `import`
- `pricing`
- `pricing_profit`
- `market_intelligence`
- `listing_health`
- `ads_optimization`
- `reporting`
- `fba`
- `execution`
- `pipeline`

## `schedule`

Execution mode for the feature.

Allowed future values should stay simple:
- `manual`
- `daily`
- `hourly`
- `disabled`

If legacy entries use other forms, do not rewrite them without approval.
New future entries should use these controlled values.

## `schedule_time`

Clock time for daily runs.

Rules:
- use `HH:MM` 24-hour format
- include only when meaningful

## `freshness_hours`

Maximum acceptable age of output before it is considered stale.

Rules:
- use number
- match the actual business need
- do not guess unrealistic freshness values

Examples:
- `0.5`
- `2`
- `24`

## `depends_on`

Array of feature ids that should run before this feature.

Rules:
- always reference feature ids, not script names
- keep dependencies minimal and real
- avoid circular dependencies

## `dashboard_button`

Whether the dashboard should show a direct run/control button for this feature.

Use:
- `true` for operator-triggered features
- `false` for hidden/internal features when appropriate

## `button_label`

Short action label shown on dashboard controls.

Rules:
- make it clear and short
- describe action, not architecture
- avoid vague labels like `Run Feature`

## `button_color`

Visual intent for the control button.

Use controlled values only:
- `blue` for standard run/check actions
- `green` for preview/create/report-type safe actions
- `orange` for approval/execution/risk-sensitive actions
- `red` for high-risk execution actions

Do not invent many new colors without updating the dashboard control standard.

## `enabled`

Whether the feature is active for control/scheduling.

Use boolean only.

## `alert_on_issue`

Whether the system should raise attention when the feature detects risk/issues.

Recommended for:
- listing health
- competitor monitoring
- pricing risk
- stockout risk
- Buy Box risk

## `self_action_enabled`

Whether the feature is allowed to auto-act after findings are created.

Use:
- `true` when self-action is allowed
- `false` when feature should only detect/recommend

Default future value:
```text
true
```

## `action_engine`

Names the reusable action engine this detector feature should call when relevant.

Examples:
- `price_optimizer`
- `listing_recovery`
- `stock_restock`
- `fba_auto`

This field helps future AI tools avoid creating duplicate action functions.

## `note`

Short operational note for future AI tools and operators.

Keep it concise.

---

# 7. NEW FUTURE RULES FOR AI TOOLS

When an AI tool adds a new future feature to `config_features.json`, it must:

1. Confirm the module already has a planned architecture and registration.
2. Use the correct `Grow24_AI` script location.
3. Add `script_dir` for the module folder.
4. Use a real category, not a vague placeholder.
5. Define real dependencies only if needed.
6. Set a realistic `freshness_hours`.
7. Use button colors intentionally.
8. Keep naming stable and machine-friendly.
9. Avoid copying messy legacy patterns into new entries.

---

# 8. WHAT FUTURE AI TOOLS MUST NOT DO

Do not:
- create a new future production feature entry without `script_dir` when the script is under `Grow24_AI`
- point new production entries back into `ClaudeCode/Python`
- use `config_features.json` to store report file paths as the main registry system
- invent many custom fields with no documented standard
- create duplicate features with nearly identical ids
- use unclear categories like `misc`
- use vague labels like `Run`, `Do Work`, or `Execute`

---

# 9. RELATIONSHIP TO OTHER STANDARDS

`config_features.json` answers:
- how to launch the feature
- how to schedule the feature
- how to expose the feature in operational controls

It does **not** replace:

- `GoAmrita_MASTER_Future_Module_Standard_v1.0.md`
  overall future architecture

- `GoAmrita_Future_Module_Location_Standard_v1.0.md`
  where new production module code belongs

- `GoAmrita_Future_Data_and_Report_Location_Standard_v1.0.md`
  where outputs belong

- `GoAmrita_Future_Dashboard_Code_Location_Standard_v1.0.md`
  where dashboard/web code belongs

- `GoAmrita_Future_JSON_Contract_v1.0.md`
  how module outputs are shaped

- `GoAmrita_Future_Report_Registry_Standard_v1.0.md`
  how dashboards discover report outputs

---

# 10. LEGACY SAFETY RULE

Current legacy entries may remain mixed or inconsistent for now.

Do not rewrite all old entries immediately just to match this standard.

Use this document for:
- all new future feature entries
- approved updates to existing entries
- migration planning for old entries later

---

# 11. FINAL RULE

For all new future modules/features, `config_features.json` must be treated as the **operational feature control file** only.

It must launch the correct script from the correct `Grow24_AI` folder, with controlled fields, stable naming, real dependencies, and clear dashboard control behavior.
