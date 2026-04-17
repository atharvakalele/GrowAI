# Grow24 AI / GoAmrita - Future Action Execution Standard v1.0
**Project Name:** Grow24 AI (formerly GoAmrita)  
**Date:** 15 April 2026  
**Purpose:** Standard for the second half of every future feature/module: decide and take action from detected findings

---

# 1. CORE IDEA

Every future goal should be divided into 2 parts:

1. Get Data
2. Take Action

This document defines **Part 2 = Take Action**.

The action layer starts only after the data layer has already created structured findings/action candidates.

---

# 2. WHAT "TAKE ACTION" MEANS

For any future feature, the second question is:

```text
Now what should the system do?
```

The action layer is responsible for:
- reading findings/action candidates
- deciding whether action is allowed
- executing the allowed fix/workflow
- recording what action was taken
- reporting success, fail, partial, or blocked

---

# 3. ACTION FLOW

Correct future flow:

```text
Get Data
-> publish finding
-> create action candidate
-> check action setting/rules
-> take action if allowed
-> publish action result
```

Wrong future flow:

```text
detect issue
-> silently act
-> no clear finding
-> no action record
```

---

# 4. DEFAULT ACTION RULE

Self-action should be treated as:

```text
enabled by default
```

That means future AI tools should assume:
- system should take action automatically when the action is allowed
- manual-only behavior should happen only when explicitly disabled or blocked by rule

---

# 5. ACTION SETTING RULE

The project should support a setting to enable/disable self-action.

Recommended setting meaning:
- `self_action_enabled = true`
  system may take allowed actions automatically

- `self_action_enabled = false`
  system may still detect and recommend, but must not auto-execute

Default future value:

```text
self_action_enabled = true
```

---

# 6. WHEN AUTO-ACTION IS ALLOWED

Auto-action is allowed only when all of these are true:
- a structured finding exists
- a recommended action exists
- self-action setting is enabled
- module rules allow the action
- no explicit safety block prevents the action

---

# 7. WHEN AUTO-ACTION MUST NOT HAPPEN

Auto-action must not happen when:
- self-action setting is disabled
- the action requires explicit approval by future safety rules
- the finding confidence is too low
- the action would be destructive/high-risk without approval
- required data is incomplete

---

# 8. REQUIRED ACTION OUTPUT

The action layer should publish:
- what finding triggered the action
- what action was attempted
- whether action was auto or manual
- action result: success/fail/partial/skipped/blocked
- reason if skipped or blocked
- business effect if measurable

---

# 9. EXAMPLE

```text
Competitor tracker finds 1 ASIN at risk
-> action candidate says:
   check listing suppression, price, and availability
-> self_action_enabled = true
-> system takes the allowed follow-up action/workflow
-> result is written to activity outputs and dashboard
```

If self-action is off:

```text
Competitor tracker finds 1 ASIN at risk
-> recommendation is still published
-> no auto-execution happens
-> dashboard shows action pending/recommended
```

---

# 10. FUTURE AI TOOL RULE

Future AI tools must not stop at:
- "issue found"
- "1 ASIN risky"
- "recommendation shown"

They must also define:
- what exact action follows
- whether it is auto-action eligible
- what setting controls it
- what result status must be recorded

---

# 11. FINAL RULE

For all new future modules/features:

**Part 2 must always be "Take Action or Clearly Record Why Action Did Not Run."**

Finding an issue is not enough. The system must either act or clearly explain why it did not act.
