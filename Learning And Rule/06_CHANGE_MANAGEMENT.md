# 🔁 06 — Change & Version Management Rules v1.1
**When to apply:** When modifying existing code, features, or systems

---

## Rule 1: 360° Impact Analysis Before Any Change
- Before ANY change, think from all angles
- Will this change break any existing feature?
- What are the pros of this change?
- What are the cons or risks?
- Only proceed after full consideration

## Rule 2: Change Sizing Strategy
- **Small changes** → Group multiple updates in one go (batch them)
- **Major changes** → Implement step-by-step, one at a time
- This avoids confusion and makes debugging easier

## Rule 3: Version Backup — MANDATORY
- Before updating main files, **always keep a backup** of the old version
- Never overwrite directly without backup
- This prevents data loss and enables rollback
- Maintain version history
- **Naming Convention:** `software_name → backup_software_name_timestamp` in a subfolder
- Maintain a local master file with: working steps, failed steps, tips, mistakes to avoid

## Rule 4: Version Number Discipline
- **ALWAYS increase version number** when creating new versions
- Follow consistent versioning pattern (v1.0, v1.1, v2.0, etc.)
- Major changes = major version bump
- Minor fixes = minor version bump

## Rule 5: One-Click Rollback
- Design systems with rollback capability
- If new version has issues, should be able to revert quickly
- Maintain version history UI where applicable

## Rule 6: Data Recovery Flows
- Plan for data recovery scenarios
- What happens if an update corrupts data?
- Have clear recovery procedures documented

## Rule 7: Technology Version Lock
- When working on a specific language/API version:
  - Use only modern, supported, updated methods for THAT version
  - Never accidentally include deprecated methods from older versions
  - Keep software stable and future-relevant

---

## 📋 Change Checklist
- [ ] Impact analysis completed (360°)
- [ ] Backup of current version created
- [ ] Version number incremented
- [ ] Change is sized correctly (batch or step-by-step)
- [ ] Rollback plan exists
- [ ] No existing features broken
- [ ] Tested after implementation

---
*Category: Change & Version Management | Source: Msir's Universal Rulebook*
