# Grow24 AI / GoAmrita - Legacy Module Migration Plan v1.0
**Project Name:** Grow24 AI (formerly GoAmrita)  
**Date:** 15 April 2026  
**Purpose:** Safe future migration plan for existing/legacy modules and reports

---

# 1. PURPOSE

This document defines how existing/legacy modules should be migrated later to the future dashboard/report standard.

It exists to prevent accidental damage to current work.

Current decision:
- Do not change legacy modules now
- Do not rewrite legacy JSON now
- Do not confuse developers currently working on legacy modules
- Migrate later using a safe wrapper-first approach

---

# 2. GOLDEN RULE

```text
Legacy raw JSON stays unchanged until explicit migration approval.
```

Migration must start with wrappers, not rewrites.

---

# 3. WHAT COUNTS AS LEGACY

A module/report is legacy if:
- it existed before the future-module standard
- it writes custom JSON without impact/activity summaries
- it is already used by the current dashboard
- another developer may be working on it
- changing its output could break current workflows

Examples may include:
- existing import outputs
- existing buy box reports
- existing stock reports
- existing listing reports
- existing action reports
- existing scheduler logs
- existing dashboard JSON assumptions

---

# 4. MIGRATION PHILOSOPHY

Do **not** force old modules into the new standard immediately.

Instead:
1. Preserve old raw outputs
2. Add wrapper summaries beside them
3. Add registry entries
4. Let future dashboards read the wrapper layer
5. Only later consider raw cleanup if truly needed

This protects current work and allows gradual adoption.

---

# 5. MIGRATION PHASES

## Phase 0: Freeze and Observe

Goal:
- understand existing outputs
- avoid changes
- document what each legacy module creates

Actions:
- list legacy files
- identify consumers
- identify dashboard dependencies
- identify business meaning of each file

No code rewrite.

## Phase 1: Wrapper Summary Layer

Goal:
- generate future-standard summaries from legacy raw JSON

Actions:
- read legacy JSON as input
- create `impact_<feature_key>_latest.json` if business impact exists
- create `activity_<feature_key>_latest.json` if run/activity exists
- do not modify legacy raw JSON

## Phase 2: Registry Integration

Goal:
- make legacy module discoverable by future dashboards

Actions:
- create registry entry
- point registry to legacy raw file + wrapper summaries
- mark migration note: `legacy_wrapped`

## Phase 3: Dashboard Readiness

Goal:
- future dashboards can show migrated legacy module via standard summaries

Actions:
- verify Strategy Impact Dashboard reads impact summary
- verify Activity Dashboard reads activity summary
- verify old dashboard still works if needed

## Phase 4: Optional Raw Cleanup

Goal:
- only if approved, slowly clean raw structure

Actions:
- create new raw version
- keep backup
- keep old compatibility if needed
- test all consumers

This phase requires explicit approval.

---

# 6. MIGRATION ORDER RECOMMENDATION

Migrate low-risk modules first.

Recommended order:

## 1. Report-only modules
- safest
- no execution risk

## 2. Monitor modules
- buy box, stock, listing health, competitor
- mostly read/report behavior

## 3. Scheduler/log modules
- activity-focused
- good candidates for activity summary

## 4. Recommendation modules
- action report, rule engine outputs
- need impact + review state

## 5. Execution/action modules
- highest risk
- migrate last
- requires rollback/safety review

---

# 7. LEGACY WRAPPER RULES

Wrapper should:
- read legacy output
- create standard summary
- create/update registry entry
- record source legacy file
- record migration status

Wrapper should NOT:
- rewrite legacy raw JSON
- delete legacy file
- rename legacy file
- change old dashboard assumptions
- change current developer workflow

---

# 8. MIGRATION STATUS VALUES

Use these values in registry notes or migration metadata:

- `legacy_unmapped`
- `legacy_reviewed`
- `legacy_wrapped`
- `dashboard_ready`
- `raw_cleanup_candidate`
- `fully_migrated`

---

# 9. LEGACY WRAPPER METADATA

Each wrapper summary should include in `notes` or `detail_ref`:

```json
{
  "migration_status": "legacy_wrapped",
  "legacy_source_file": "Json/example_legacy_file.json",
  "legacy_output_unchanged": true,
  "wrapper_generated_at": "2026-04-15T12:00:00Z"
}
```

---

# 10. APPROVAL REQUIREMENTS

No approval needed for:
- reading legacy JSON
- creating separate wrapper summaries
- creating registry entries that do not affect old dashboard

Approval required for:
- changing legacy JSON shape
- renaming legacy files
- deleting legacy files
- changing existing dashboard behavior
- changing action/execution behavior
- changing scheduler behavior

---

# 11. VALIDATION CHECKLIST

Before marking legacy module migrated:

- [ ] legacy raw file unchanged
- [ ] wrapper impact summary created if needed
- [ ] wrapper activity summary created if needed
- [ ] registry entry created
- [ ] migration status recorded
- [ ] old dashboard behavior not broken
- [ ] future dashboard can read wrapper
- [ ] no legacy file renamed/deleted
- [ ] approval obtained if any legacy behavior changed

---

# 12. COMMON MISTAKES TO AVOID

- rewriting old raw JSON first
- assuming all legacy modules need both summaries
- mixing raw cleanup with dashboard wrapper work
- changing current dashboard behavior without approval
- migrating execution modules before report-only modules
- deleting old files after wrapper creation
- treating wrapper migration as full refactor

---

# 13. FINAL RULE

```text
Wrap first. Prove safe. Migrate slowly.
```

This is the safe path for legacy module migration.

---

*Legacy Module Migration Plan v1.0 | 15 April 2026*  
*Legacy modules remain unchanged until planned migration approval*
