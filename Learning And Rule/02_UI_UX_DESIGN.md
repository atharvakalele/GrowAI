# 🎨 02 — UI/UX & Design Rules v1.0
**When to apply:** When building or modifying any user interface

---

## Rule 1: Clean & Professional Interface
- Interface must be smooth, professional, and trustworthy
- Remove unnecessary elements — keep it simple
- User should feel comfortable and confident while using the software

## Rule 2: Tab-Based Menu Structure
Split interface into multiple tabs:
1. **Main Tab** — Most frequently used options, quick access controls
2. **Advanced Tab** — Important but less frequently used settings
3. **Settings/Default Tab** — Rarely changed configurations, defaults at bottom
4. Additional tabs as needed based on situation

## Rule 3: Section Layout Design
- Organize options into clear sections inside each tab
- Use light background variations per section
- Middle sections slightly different background to separate from top/bottom
- Visual spacing between blocks
- Flow: top → bottom (most important → least important)
- If too many options, break into logical groups

## Rule 4: Helper Text
- Add short helper text beside each option
- Keep UI self-explanatory — user shouldn't need external documentation

## Rule 5: Auto-Save System
- Remove manual Save buttons where possible
- Enable auto-save on change
- Show small confirmation text like: "Saved ✓" near the changed setting
- Benefit: Faster workflow, no extra clicks

## Rule 6: Start/Stop Controls
- Provide clear Start and Stop buttons for processes
- User should always feel in control

## Rule 7: Default Settings
- Pre-set important values as defaults
- API keys, secrets, common settings should be pre-configured
- Software should be ready-to-use immediately after install
- Menu can have many options, but common ones should be pre-selected

## Rule 8: Progress Visibility
- Show automation progress via popup, badge, or icon
- Give user options to choose WHERE they see progress notifications
- Options: same site, popup menu, different tab, badge on icon
- All options controllable from settings menu

## Rule 9: Mode Options
Provide multiple operation modes:
- **Fully Automated** — Everything runs automatically
- **Assistant Mode** — Software asks for user input when needed
- **Smart Mode (Hybrid)** — Auto-handles clear tasks, asks approval only for uncertain decisions

## Rule 10: Feature ON/OFF — Dual Control (Option C)
Every feature MUST have ON/OFF toggle in TWO places:
1. **Central Master Control Panel** — Dashboard home page, all features listed as switchboard
   - Quick ON/OFF toggle per feature
   - Schedule/interval setting visible right next to toggle (when ON)
   - One glance = see what's running and what's not
2. **Feature's Own Settings Page** — Detailed settings + its own ON/OFF toggle
   - Full configuration options
   - Toggle here also syncs back to central panel

**Both MUST stay in sync** — toggle from either place updates same config.
**Why:** User needs quick overview (central) AND detailed control (feature page).
**Schedule inline:** When user turns ON a feature in central panel, schedule/interval option should appear right there — no need to go into feature page just to set timing.

---
*Category: UI/UX Design | Source: Msir's Universal Rulebook | Updated: 16 April 2026*
