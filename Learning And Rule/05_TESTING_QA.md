# 🧪 05 — Testing & Quality Assurance Rules v1.1
**When to apply:** Before delivering ANY output — code, feature, file, or script

---

## Rule 1: Self-Test Before Delivery
- AI must thoroughly test everything it builds BEFORE giving final output
- User should receive a fine-tuned, working product — not a draft to debug
- Test every feature individually before combining

## Rule 2: Test Against Latest Environment
- Test code/logic as per:
  - Latest OS version (if OS-dependent)
  - Latest browser (if browser-based)
  - Correct language version rules, syntax, logic
- Never test against outdated environments

## Rule 3: Nothing Breaks Existing Features
- Before delivery, ensure:
  - No existing functionality is broken
  - All required data is present
  - Final verification completed
- Avoid incomplete or partially working results — NEVER

## Rule 4: Multi-Angle Testing (Deep Testing)
- Test from EVERY angle:
  - Normal use cases
  - Edge cases (empty input, very large input, special characters)
  - Error scenarios (network failure, API timeout)
  - Boundary conditions
- Goal: No bug, weakness, or future-breaking issue should escape

## Rule 5: Testing Strategy Layers
1. **Automated self-validation** by the tool itself
2. **Functional testing** — each feature against defined goals
3. **Edge case testing** — for robustness
4. **Performance testing** — under realistic loads
5. **Regression testing** — catch issues early after changes

## Rule 6: Real User Simulation
Test realistic situations:
- Slow internet conditions
- Low RAM systems
- Large data inputs
- Multiple concurrent operations

## Rule 7: Pattern-Based Bug Detection
When you find a bug:
- Scan for similar or related issues across the entire system
- Think in terms of pattern-based debugging, not just single-issue fixes
- This reduces repeated testing effort and uncovers hidden bugs early

## Rule 8: Bug Resolution Escalation
If a bug is not resolved after multiple attempts:
- Recommend starting a fresh session/chat
- This helps reset context and avoids corrupted logic chains

---

## 📋 Pre-Delivery Checklist
- [ ] All features individually tested
- [ ] Integration between features tested
- [ ] Edge cases covered
- [ ] No existing functionality broken
- [ ] Tested on correct environment/version
- [ ] Error scenarios handled gracefully
- [ ] Final verification completed

---

## 📝 Testing Notes Structure (How to Write Testing Notes)

### A. Divide Notes into 2 Sections:
1. **Earlier Analysis** — initial attempts (never delete, they contain learning)
2. **Later Analysis (Final Truth)** — always trust this over earlier

### B. Write Notes in PHASES:
- Phase 1 — Input/Read
- Phase 2 — Fetch/Download
- Phase 3 — Process/Interaction
- Phase 4 — Output/Extraction
- Phase 5 — Storage/Integration

### C. Inside Each Phase, Write:
1. **❌ What Failed** — ALL failed methods + exact error + reason (most valuable part!)
2. **✅ What Worked** — exact method, tool, environment, why it worked. Best = primary, others = fallback
3. **⚠️ Care Points** — conditions for success, things that must NOT change, hidden rules
4. **⭐ Best Method** — most reliable, most repeatable. Mark: "This is the method to use in future"

### D. Master Failure List:
- Group failures by type: Network, CORS/security, Tool limitations, Timing, Wrong environment
- Prevents repeating same mistakes

### E. Environment Notes:
- Always mention WHERE it worked (browser/local/etc.) and WHERE it failed

### F. When to Re-Read Notes:
- Before starting any similar task → read Best Methods + Failure List
- When something fails → check same phase in notes
- Before changing approach → check why previous methods failed

---
*Category: Testing & QA | Source: Msir's Universal Rulebook | Updated: 12 April 2026*
