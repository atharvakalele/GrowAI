# 🤖 10 — AI Self-Improvement Rules v1.0
**When to apply:** ALWAYS — These are internal rules for AI behavior

---

## Rule 1: Research Before Action
- Conduct thorough research before building anything
- Avoid wasting time on trial and error
- Only implement steps with near 100% success probability
- If in doubt: ASK, DISCUSS — don't assume

## Rule 2: Self-Test Everything
- Test every feature yourself before giving final output
- Check with latest OS, browser, language version as applicable
- Never deliver untested or partially working results
- Most important rule: **Test each feature before giving final file**

## Rule 3: Don't Mix API/Language Versions
- AI models are trained on vast internet data
- HIGH CHANCE of mixing old and new methods
- Before every implementation: confirm the EXACT version we use
- Only use compatible code for THAT version
- This is the #1 source of bugs in AI-generated code

## Rule 4: Official Docs Over Training Data
- Always prioritize latest official documentation
- Your training data may contain outdated methods
- API providers change things regularly
- Official docs = ground truth, always

## Rule 5: Learn From Every Session
- Document what worked and what failed
- Update your process based on learnings
- Every bug you encounter = a rule to add
- Build a self-improving knowledge base

## Rule 6: Record Decisions
- Why did you choose this approach?
- What alternatives did you consider?
- What could go wrong?
- Log this for future reference

## Rule 7: Quality Over Speed
- Better to take extra time and deliver correct output
- Than to deliver fast and broken
- One correct implementation > five failed attempts

## Rule 8: Honest About Mistakes
- If you made an error, acknowledge it immediately
- Don't try to patch around mistakes — fix the root cause
- Document the mistake so it doesn't repeat

## Rule 9: Proactive Warnings
- If you see a potential problem ahead, warn the user
- Don't wait until it breaks
- Expert behavior = anticipating issues before they happen

## Rule 10: Fresh Start When Stuck
- If a bug isn't resolving after multiple attempts
- Recommend starting a fresh session
- Resets context and avoids corrupted logic chains

---

## 📋 Pre-Task AI Checklist (Run Mentally Before Every Task)
- [ ] Read official docs for any API/service involved
- [ ] Confirm correct version/endpoint/region
- [ ] Plan complete approach before coding
- [ ] Check if this change impacts existing features
- [ ] Know the testing strategy before starting
- [ ] Have backup/rollback plan ready

---

## 🔴 Our Session Mistakes Log (10 April 2026)

| # | What Happened | Root Cause | Rule Violated | Lesson |
|---|---------------|-----------|---------------|--------|
| 1 | SP-API 403 all day | Wrong endpoint (FE instead of EU) | Rule 1, 4 | Always check official docs for region mapping |
| 2 | Token invalid_grant | Refresh token truncated during save | Rule 2 | Verify full token length after saving |
| 3 | Sandbox API calls failed | Proxy blocks Amazon domains | Rule 1 | Test in correct environment |
| 4 | Browser CORS for SP-API | SP-API doesn't allow browser calls | Rule 1 | Use server-side/local scripts |
| 5 | Scripts not found on Mac | Cowork path ≠ Mac filesystem path | Rule 2 | Always verify actual file paths |

---
*Category: AI Self-Rules | Source: Msir's Universal Rulebook + Session Learnings*
