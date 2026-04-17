# Grow24 AI / GoAmrita - AI-Only Development Protocol v1.0
**Project Name:** Grow24 AI (formerly GoAmrita)  
**Date:** 15 April 2026  
**Purpose:** Rules for AI tools working on this project without human developers

---

# 1. PURPOSE

This project should be treated as an **AI-operated development project**.

That means future work will mostly be done by AI tools, not human developers.

So every standard must be written in a way that an AI tool can read, understand, follow, and safely continue without needing hidden human memory.

This document tells every AI tool:
- how to start work
- what files to read first
- what not to touch
- how to create new modules
- how to document work
- how to avoid confusing future AI tools

---

# 2. CORE RULE

**AI tools must not guess the project architecture from old files.**

They must follow the master future standard and companion files for all new work.

Legacy files may be inconsistent. That does not mean future files should copy legacy structure.

---

# 3. AI STARTUP CHECKLIST

Before any AI tool creates or changes a future module, it must read:

1. `GoAmrita_MASTER_Future_Module_Standard_v1.0.md`
2. `GoAmrita_AI_Only_Development_Protocol_v1.0.md`
3. `GoAmrita_Future_Module_Build_Workflow_v1.0.md`
4. `GoAmrita_Future_JSON_Contract_v1.0.md`
5. `GoAmrita_Future_Report_Registry_Standard_v1.0.md`
6. `GoAmrita_Future_Module_Location_Standard_v1.0.md`
7. `GoAmrita_Future_Dashboard_Code_Location_Standard_v1.0.md`
8. `GoAmrita_Future_Feature_Config_Standard_v1.0.md`
9. `GoAmrita_Future_Data_Collection_Standard_v1.0.md`
10. `GoAmrita_Future_Action_Execution_Standard_v1.0.md`
11. `GoAmrita_Future_Action_Reuse_and_Routing_Standard_v1.0.md`

If the work touches dashboards, also read:

6. `GoAmrita_Future_Dashboard_Architecture_v1.0.md`
7. `GoAmrita_Future_Dashboard_Rendering_Rules_v1.0.md`

If the work touches old modules, also read:

8. `GoAmrita_Legacy_Module_Migration_Plan_v1.0.md`

---

# 4. AI WORKING STYLE

Every AI tool must work in small, traceable steps.

Required behavior:
- explain what it is going to change before changing files
- change only the files required for the approved task
- avoid broad refactors
- avoid renaming old files unless explicitly approved
- keep new work separate from legacy work
- create documentation for every new architecture decision
- leave enough notes that the next AI tool can continue safely

Forbidden behavior:
- silently changing legacy modules
- rewriting old JSON into new format without migration approval
- mixing dashboard UI logic directly inside module scripts
- creating new outputs without registry entries
- creating reports that dashboards cannot discover
- using vague file names like `new_report.json` or `final_data.json`
- placing new production modules in `ClaudeCode/Python` when they belong under `Grow24_AI`
- placing new shared dashboard/web production code in `ClaudeCode/Python` when it belongs under `Grow24_AI/core/dashboard`
- adding new future `config_features.json` entries with missing `script_dir`, vague categories, unclear button behavior, or undocumented custom fields
- creating duplicate action/fix functions when a reusable action engine already exists elsewhere in the project

---

# 5. AI MEMORY RULE

AI tools should assume there is **no reliable memory between sessions**.

Therefore, important decisions must be written into project files.

Do not rely on:
- chat history only
- temporary notes
- local assumptions
- memory from another AI tool

If a decision affects future modules, dashboards, reports, JSON contracts, approvals, or migration, it must be documented.

---

# 6. NEW MODULE RULE

Every new module created by an AI tool must produce:

1. Raw Output
2. Impact Summary
3. Activity Summary
4. Report Registry Entry

The module must not directly own dashboard rendering.

Dashboards consume standardized summaries and registry entries.

Every new module should also be thought of in 2 stages:

1. Get Data
2. Take Action

The AI tool must not stop only at detection if the feature is meant to be operational.

It must also define:
- what action follows the finding
- whether self-action is allowed
- how disabled/blocked action is recorded
- whether an existing reusable action engine should be called instead of creating a new action function

---

# 7. AI HANDOFF REQUIREMENT

After creating or changing a future module, the AI tool must document:

- files created
- files changed
- module name
- module purpose
- raw output path
- impact summary path
- activity summary path
- registry entry path
- dashboard target
- approval requirement
- known limitations
- test/validation result

This handoff can be written in the module documentation or a delivery note.

---

# 8. LEGACY SAFETY RULE

Legacy modules are allowed to remain messy for now.

AI tools must not "clean them up" automatically.

For legacy modules:
- observe first
- wrap second
- migrate later
- only change after explicit approval

The first safe bridge is a wrapper that reads old output and creates new standardized summaries.

---

# 9. DASHBOARD SAFETY RULE

AI tools must not make dashboards depend on raw module files.

Correct flow:

```text
Module -> Raw Output
Module -> Impact Summary -> Report Registry -> Strategy Impact Dashboard
Module -> Activity Summary -> Report Registry -> Activity Dashboard
```

Wrong flow:

```text
Module Raw JSON -> Dashboard directly
```

---

# 10. APPROVAL RULE

AI tools must request approval before:

- changing legacy module behavior
- deleting files
- renaming existing files
- changing dashboard architecture
- changing JSON contracts
- changing scheduler/orchestrator behavior
- applying migrations to existing reports

AI tools may proceed without extra approval only for clearly approved new documentation or new future-module files.

---

# 11. FINAL RULE

**This project is AI-maintained, so the architecture must be readable by AI, executable by AI, and safe for the next AI.**

If an AI tool cannot understand a file's purpose quickly, the file is not documented well enough.
