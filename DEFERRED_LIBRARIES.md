# 🚫 Deferred Libraries — DO NOT Integrate Without User Approval
**Created:** 14 April 2026
**Decision By:** Msir
**Status:** FROZEN until further notice (not planned till Dec 2026)

---

## ⛔ RULE: ZERO TOLERANCE

```
┌──────────────────────────────────────────────────────────────┐
│  These libraries are NOT part of Grow24 AI until Msir        │
│  explicitly approves integration.                            │
│                                                              │
│  ❌ DO NOT import, install, or write code using these        │
│  ❌ DO NOT plan features that depend on these                │
│  ❌ DO NOT add to requirements.txt                           │
│  ❌ NOT PLANNED to integrate until at least Dec 2026         │
│                                                              │
│  ✅ CAN recommend if genuinely needed — but ONLY after       │
│     Msir approval before any integration                     │
└──────────────────────────────────────────────────────────────┘
```

---

## 📋 Deferred Library List

### ML / Machine Learning Libraries
| # | Library | Version (was planned) | Was For | Why Deferred |
|---|---------|----------------------|---------|--------------|
| 1 | **LightGBM** | 4.6.0 | Bid prediction, ACoS forecasting, waste detection (AI Layer 2) | Rule-based AI (Layer 1) handles 80%+ decisions. ML not needed now |
| 2 | **Prophet** | 1.3.0 (Meta) | Seasonal demand prediction, sales forecasting, festival planning | Not needed until data volume justifies ML predictions |

### Database / ORM Libraries
| # | Library | Version (was planned) | Was For | Why Deferred |
|---|---------|----------------------|---------|--------------|
| 3 | **SQLAlchemy** | 2.0.49 | Database ORM (DB-agnostic) | JSON files working fine. DB when data volume demands it |
| 4 | **Alembic** | 1.18.4 | DB schema migrations | No DB = no migrations needed |

### LLM / AI Libraries
| # | Library | Version (was planned) | Was For | Why Deferred |
|---|---------|----------------------|---------|--------------|
| 5 | **Gemini 2.5 Flash** | Google API | LLM Layer 3 — insights, ad copy analysis, recommendations | Layer 1 (rules) sufficient for current needs |
| 6 | **Gemini 2.5 Flash-Lite** | Google API | LLM Layer 3 — bulk classification, tagging | Same as above |
| 7 | **Gemini 2.5 Pro** | Google API | LLM Layer 3 — deep analysis, complex reasoning | Same as above |
| 8 | **Ollama** | Local LLM | LLM fallback (local, free) | No LLM needed currently |

### Data Processing (Large-scale)
| # | Library | Version (was planned) | Was For | Why Deferred |
|---|---------|----------------------|---------|--------------|
| 9 | **pandas** | 3.0.2 | Data manipulation at scale | Python built-in `json` + `csv` modules sufficient for current scale |

**Total Deferred: 9 libraries**

---

## ✅ What IS Allowed (Currently Active)

| Library | Used In | Status |
|---------|---------|--------|
| **Flask** 3.1.3 | Dashboard server | ✅ Active, in code |
| **openpyxl** | Excel report creation/reading | ✅ Active, in code |
| **requests** | API calls (Ads + SP-API) | ✅ Active, in code |
| **Python 3.11 built-ins** | json, os, datetime, urllib, smtplib, etc. | ✅ Always available |

---

## 🟡 Allowed to Recommend (Need Approval Before Use)

| Library | When to Recommend | Notes |
|---------|-------------------|-------|
| **scipy** | A/B test significance calculation | Msir said: recommend where needed |
| **numpy** | Heavy numerical calculations | Msir said: recommend where needed |
| **Any new library** | When genuinely needed for a feature | Must get Msir approval FIRST |

---

## 🔄 How to Reactivate

1. Developer identifies genuine need for a deferred library
2. Recommend to Msir with: WHY needed + WHAT feature + WHAT alternative exists
3. Msir approves → move library from this list to active
4. Update MASTER docs + requirements.txt
5. Only THEN write code using it

---

*Created: 14 April 2026 | Frozen until: Dec 2026 minimum*
*Decision: Msir — keep project lean, add libraries only when proven need*
