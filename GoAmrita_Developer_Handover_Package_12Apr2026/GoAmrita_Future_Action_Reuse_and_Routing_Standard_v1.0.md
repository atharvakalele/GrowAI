# Grow24 AI / GoAmrita - Future Action Reuse and Routing Standard v1.0
**Project Name:** Grow24 AI (formerly GoAmrita)  
**Date:** 15 April 2026  
**Purpose:** Prevent duplicate action functions and define how detector modules should route findings into existing action engines

---

# 1. CORE RULE

Future modules must **not create duplicate act functions** when a similar reusable action already exists in another feature/module.

Correct rule:
- detection may be feature-specific
- action should be shared/reused whenever possible

---

# 2. DETECTOR VS ACTION ENGINE

Future architecture should separate:

## Detector

Detector modules answer:
- what happened?
- what item is affected?
- what action is recommended?

Examples:
- competitor tracker
- listing health detector
- stock monitor
- pricing gap detector

## Action Engine

Action engines answer:
- how do we fix it?
- can we act automatically?
- what exact workflow should run?

Examples:
- price optimizer
- stock restock executor
- FBA shipment creator
- listing recovery workflow

---

# 3. NO DUPLICATE ACTION RULE

If a detector module finds an issue, it must first check:

```text
Does a reusable action engine already exist for this kind of fix?
```

If yes:
- call/reuse that action engine
- do not build a duplicate action function

If no:
- record that no suitable reusable action engine exists
- only then design a new action engine if really needed

---

# 4. SAFE IMPROVEMENT RULE

If the existing action engine is not sufficient:
- improve the existing engine carefully
- keep backward compatibility
- do not break the older feature that already uses it
- do not silently change business behavior without documenting it

Wrong:
- competitor module creates its own new price-decrease function

Correct:
- competitor module routes to existing pricing action engine
- if required, pricing engine is extended safely

---

# 5. ACTION ROUTING RULE

Detector modules should publish an action route along with the finding.

That route should answer:
- what action family is needed?
- which reusable action engine should be called?
- is auto-action allowed?

Example action families:
- `pricing`
- `listing_recovery`
- `stock_recovery`
- `fba_replenishment`
- `ads_response`

---

# 6. COMPETITOR TRACKER EXAMPLE

If Competitor Tracker finds a critical issue:

It should not directly invent a new fix function.

It should route by issue type:

- price too high / Buy Box lost due to price
  -> route to pricing action engine

- listing suppression suspected
  -> route to listing recovery/listing health action engine

- availability/stock problem suspected
  -> route to stock/FBA action engine

- competitor pressure found but no safe action engine exists
  -> record finding and mark action as blocked/pending

---

# 7. CURRENT PROJECT REALITY

As of now, the migrated Competitor Tracker mostly does:
- detect
- summarize
- publish dashboard/report outputs
- recommend exact next action

It does **not yet fully route and execute all critical findings through shared action engines**.

That is the next integration direction.

---

# 8. REQUIRED OUTPUT FOR ROUTED ACTIONS

When a detector module creates a routed action candidate, it should record:
- source detector module
- affected entity/item
- issue type
- recommended action
- target action engine
- auto-action eligibility
- final action result

---

# 9. FUTURE AI TOOL RULE

Before creating any new act/fix function, the AI tool must check for existing reusable actions in:
- pricing/action modules
- listing/health modules
- stock/restock modules
- FBA modules
- execution/approval modules

If a similar reusable action already exists, reuse it.

---

# 10. FINAL RULE

For future modules:

**Many modules may detect problems, but action engines should be reused, not duplicated.**

Detector modules should route findings into existing action engines whenever possible.
