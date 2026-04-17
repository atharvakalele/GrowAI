# ⚡ QUICK RECALL — Read This BEFORE Every Task v1.0
## 🚨 MANDATORY: Read this file at the start of every session and before every task

---

## 🔴 TOP 5 CRITICAL RULES (Never Skip)

### 1. 📖 OFFICIAL DOCS FIRST
- Before ANY API/service work → read LATEST official documentation
- Never trust old internet info or AI training data
- Check official changelog/migration guides

### 2. 🔢 VERSION CHECK
- Confirm EXACT API version, language version we use
- Only use compatible code for THAT version
- Never mix old/new methods

### 3. 🧪 TEST BEFORE DELIVER
- Test EVERY feature yourself before final output
- Test against correct OS, browser, language version
- Never deliver untested/partial work

### 4. 🔄 360° IMPACT CHECK
- Before ANY change → will it break existing features?
- Weigh pros AND cons
- Small changes = batch, Major changes = step-by-step

### 5. ⚙️ NO HARDCODING
- All values via config/variables
- Version number ALWAYS increases for new versions
- Keep backup before overwriting

### 6. 📁 CORRECT MODULE LOCATION
- `ClaudeCode/Python` = old beta/minimum-working-tool area
- Active dashboard server = `Grow24_AI/core/dashboard/dashboard_server_v1.1.py`
- Active Amazon launchers = `Grow24_AI/core/launchers/amazon/`
- New production modules must go under `Grow24_AI`
- Amazon modules must go under `Grow24_AI/marketplaces/amazon/`
- Amazon seller-side modules must go under `Grow24_AI/marketplaces/amazon/seller_api/`
- If folder does not exist, create it first
- If launched from `config_features.json`, use `script_dir`

### 7. Feature Config = Control Layer Only
- `config_features.json` is the launch/schedule/control file, not module business logic
- New future entries must use correct `Grow24_AI` `script_dir`
- Use real dependencies, clear categories, and intentional dashboard button settings
- Do not invent random new config fields without writing a standard first

### 8. Every Goal = Get Data + Take Action
- Future modules should be designed in 2 parts: first get data, then take action
- Do not stop at "issue found" if the feature is meant to operate
- Self-action should be treated as default `ON` unless disabled by setting or safety rule

### 9. Reuse Existing Action Engines
- Do not create duplicate fix/action functions if a similar one already exists
- Detector modules should route to shared action engines whenever possible
- If an existing action engine needs improvement, extend it safely without breaking old users

### 10. Feature ON/OFF — Dual Control (Option C)
- Every feature MUST have ON/OFF in TWO places: Central Master Control + Feature's Own Settings
- Both must stay in sync (same config source)
- Central panel: quick toggle + schedule/interval visible inline when ON
- Feature page: detailed settings + its own toggle
- New features MUST follow this pattern

---

## 📋 PRE-TASK CHECKLIST (Mental Run Before Every Task)
- [ ] Read official docs for any API/service involved
- [ ] Confirm correct version/endpoint/region
- [ ] ⛔ USE ONLY pinned versions from MASTER v8.0 — NO old/new mixing!
- [ ] ⛔ Verify every function/method exists in OUR pinned version's OFFICIAL DOCS
- [ ] ⛔ NO internet code, NO assumptions — ONLY official docs of OUR exact version
- [ ] ⛔ Check DEFERRED_LIBRARIES.md — do NOT import frozen libraries without approval
- [ ] Plan complete approach before coding
- [ ] Check if this change impacts existing features
- [ ] Know the testing strategy before starting
- [ ] Have backup/rollback plan ready
- [ ] Version number incremented if new version
- [ ] "Automate business > Everything else" — does this feature boost business?
- [ ] Put new production code in `Grow24_AI`, not `ClaudeCode/Python`
- [ ] For Amazon seller modules, use `Grow24_AI/marketplaces/amazon/seller_api/`

---

## 📁 Full Rules Location
All detailed rules are in: `Learning And Rule/` folder
- `01_PRE_PLANNING.md` — Research & Planning
- `02_UI_UX_DESIGN.md` — Interface Design
- `03_FEATURE_IMPLEMENTATION.md` — Building Features
- `04_API_INTEGRATION.md` — API Work (**includes our mistakes**)
- `05_TESTING_QA.md` — Testing Strategy
- `06_CHANGE_MANAGEMENT.md` — Version & Change Control
- `07_ERROR_HANDLING_LOGS.md` — Error & Logging
- `08_AUTOMATION_PERFORMANCE.md` — Automation
- `09_DOCUMENTATION_KNOWLEDGE.md` — Documentation
- `10_AI_SELF_RULES.md` — AI Internal Rules (**includes session mistakes log**)

---

## 🔴 OUR BIGGEST MISTAKES (Never Repeat)
| Mistake | Rule Broken | Lesson |
|---------|-------------|--------|
| Used FE endpoint for India SP-API | Official Docs First | India = EU region, ALWAYS check docs |
| Token truncated during save | Test Before Deliver | Verify full length of saved tokens |
| Sandbox proxy blocks Amazon | Research First | Know environment limitations |
| PostgreSQL in Phase 4 assumed | Ask Before Changing | SQLite forever unless 40+ sellers + Msir approval |

---
*Last Updated: 16 April 2026 | Version: 1.7*
*v1.1: Added STRICT version rule + "Automate business" golden rule to checklist*
*v1.2: Added PostgreSQL rule — SQLite forever unless 40+ sellers + Msir approval*
*v1.3: Added mandatory future module folder/location rule*
*v1.4: Added future feature config control-layer rule*
*v1.5: Added two-part goal rule: get data, then take action*
*v1.6: Added shared action reuse and routing rule*
*v1.7: Added dual control rule (Option C): every feature ON/OFF in central + feature page, with inline schedule*
