# 🔧 03 — Feature Implementation Rules v1.1
**When to apply:** When adding new features or modifying existing ones

---

## Rule 1: No Hardcoding
- Never hardcode important values
- Everything managed through variables or configuration files
- Developers/admins should be able to adjust settings without changing code

## Rule 2: Decision Before Implementation
- Before implementing, compare all available approaches
- Choose the method that is: fastest, smoothest, and most stable
- Don't waste time on unnecessary experiments
- Choose the effective solution upfront

## Rule 3: Pros & Cons Analysis
- Before any new implementation: weigh pros and cons
- If removing something old: evaluate pros and cons of removal too
- Only after considering both sides → make a 360° decision

## Rule 4: Feature Request Evaluation
When a feature request comes:
- Don't blindly accept it
- First evaluate: Is it actually necessary?
- If yes: think about the RIGHT way to implement it
- Also check: Is there a BETTER alternative than what was requested?
- Implement only after full deliberation

## Rule 5: Configuration & Flexibility
- All important values should be configurable
- Future changes should be easy without touching core code
- Settings, values, preferences → all adjustable from config

## Rule 6: Data Collection Strategy
When data is needed for any goal:
1. First option: Manual scraping (if needed)
2. Second option: Direct download (if available on the site)
3. Third option: API usage (if API exists)
- Compare options → choose fastest, easiest, most reliable path

## Rule 7: Browser Automation (if applicable)
- Use resilient selectors (stable attributes/patterns)
- Implement fallback logic for changed elements
- Maintain alternative navigation paths
- Continuously monitor and auto-adapt to UI changes

## Rule 8: Cross-Platform Compatibility
- Design software to work across devices
- Windows laptop, mobile app, browser extension — should work seamlessly
- Switching devices should not break functionality

## Rule 9: Extensibility & Plugin Support
- Build software so future extensions are easy
- Support for new tools, APIs, third-party integrations
- Consider plugin architecture for scalability
- API hooks for external module support

## Rule 10: Parallel & Sequential Modes
- Offer both parallel and sequential execution options
- Parallel mode: when time-saving is priority
- Sequential mode: when reducing system load is priority
- Let the situation or user decide which mode to use

## Rule 11: Avoid Unnecessary Complexity
- Always prefer simple, proven methods over complicated approaches
- If a simple solution works, don't over-engineer it
- Already working tested code → don't suggest improvements without checking 360° (current benefit/loss vs new benefit/loss)
- Diamond-grade quality = simple + stable + correct, not complex

---
*Category: Feature Implementation | Source: Msir's Universal Rulebook | Updated: 12 April 2026*
