# SP-API Software Testing Notes v1.0
**Project:** GoAmrita Bhandar | Made in Heavens  
**Seller ID / Entity:** ENTITY1TVPGA5B1GOJW  
**Marketplace:** Amazon.in (India) | Marketplace ID: A21TJRUUN4KGV  
**Date:** 10 April 2026  
**Author:** Claude + Msir  

---

# SECTION 1: EARLIER ANALYSIS (First Attempts)

---

## Phase 1 — SP-API App Registration & Developer Profile

### ✅ What Worked
- **Developer Profile** registration on Seller Central completed successfully
- Profile status confirmed **APPROVED** via internal API: `/apps/apis/intake/v2/developer/status`
- Developer type: **Private Developer**
- Entity ID: `ENTITY1TVPGA5B1GOJW`

### ❌ What Failed
1. **Shadow DOM "Save and exit" button not working (Form Filling via Automation)**
   - **What tried:** Clicked "Save and exit" via JavaScript Shadow DOM traversal, native Chrome click, React onClick dispatch
   - **Exact error:** Button click navigated back to console but NO network POST/PUT request was fired
   - **Reason:** Amazon Seller Central uses KAT (Katal) web components wrapped in Shadow DOM. The "Save and exit" button is inside nested shadow roots. Standard JS click events don't trigger the internal form submission handler.
   - **Later Discovery:** The form actually **auto-saves roles** during page navigation via PUT requests to `/apps/apis/intake/solutions/`. The "Save and exit" button is cosmetic — roles were already saved on backend.

### ⚠️ Care Points
- Seller Central uses **Shadow DOM + KAT components** — standard DOM automation (click, querySelector) often fails
- Forms may auto-save without explicit submit — always check Network tab for PUT/POST requests
- Developer Console internal APIs: 
  - `/apps/apis/intake/solutions/` — app CRUD
  - `/apps/apis/intake/v2/developer` — developer profile
  - `/apps/apis/intake/v2/developer/status` — profile status check

---

## Phase 2 — App Creation & Authorization

### ✅ What Worked

#### App 1 (First App — Old)
- **App Name:** Made in Heavens  
- **App ID:** `amzn1.sp.solution.7b8d0508-4f32-4c19-89e0-25450c20f1cb`
- **Client ID:** `amzn1.application-oa2-client.[REDACTED]`
- **Client Secret:** `amzn1.oa2-cs.v1.[REDACTED]`
- **Status:** Created successfully, roles selected and saved (auto-save confirmed)
- **Authorization:** Done via Seller Central → Authorize flow → Refresh token generated

#### App 2 (Second App — New, created after first app failed)
- **Client ID:** `amzn1.application-oa2-client.[REDACTED]`
- **Client Secret:** `amzn1.oa2-cs.v1.[REDACTED]`
- **Status:** Created fresh with new credentials
- **Authorization:** Done with `version=beta` parameter for Draft app self-authorization

### Roles Selected (Both Apps):
- Finance and Accounting
- Selling Partner Insights
- Buyer Communication
- Pricing
- Inventory and Order Tracking
- Brand Analytics
- Amazon Fulfilment
- Buyer Solicitation
- Product Listing
- Amazon Warehousing and Distribution

### ❌ What Failed
1. **First authorization without `version=beta`**
   - **What tried:** Standard authorization URL
   - **Result:** Authorization completed but API still returned 403
   
2. **Re-authorization with `version=beta` parameter**
   - **What tried:** `https://sellercentral.amazon.in/apps/authorize/consent?application_id=amzn1.sp.solution...&version=beta`
   - **Result:** New refresh token generated, but API still returned 403
   
3. **Completely new app (App 2) with fresh credentials**
   - **What tried:** Created brand new app, got new Client ID/Secret, authorized, got new refresh token
   - **Result:** Same 403 error — confirming problem is NOT app-specific

### ⚠️ Care Points
- For **Draft** status apps (Private developers), use `version=beta` in authorization URL
- Draft status is **normal and expected** for Private developers — app does NOT need to be Published
- AWS Signature V4 is **deprecated** since October 2023 — NOT required for SP-API anymore
- Multiple apps with same error = problem is account-level, not app-level

---

## Phase 3 — Token Generation (LWA OAuth2)

### ✅ What Worked — TOKEN GENERATION ALWAYS SUCCEEDED
- **Method:** POST to `https://api.amazon.com/auth/o2/token`
- **Content-Type:** `application/x-www-form-urlencoded`
- **Body:** `grant_type=refresh_token&refresh_token=<TOKEN>&client_id=<ID>&client_secret=<SECRET>`
- **Result:** Access token generated successfully EVERY time
- **Token expiry:** 3600 seconds (1 hour)

#### Exact Working curl Command:
```bash
curl -s -X POST https://api.amazon.com/auth/o2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "refresh_token=YOUR_REFRESH_TOKEN" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"
```

#### Combined Token + API Test Command (Auto-extracts token):
```bash
TOKEN=$(curl -s -X POST https://api.amazon.com/auth/o2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "refresh_token=YOUR_REFRESH_TOKEN" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4) && \
curl -s -X GET "https://sellingpartnerapi-fe.amazon.com/sellers/v1/marketplaceParticipations" \
  -H "x-amz-access-token: $TOKEN" \
  -H "Content-Type: application/json"
```

### ❌ What Failed
1. **User pasted placeholder text literally**
   - User typed `YAHAN_ACCESS_TOKEN_PASTE_KARO` instead of actual token in 2-step curl
   - **Fix:** Created single combined command that auto-extracts token (above)

### ⚠️ Care Points  
- Token generation is NOT the problem — it works 100%
- Access token expires in 1 hour — generate fresh before each test
- Always use `application/x-www-form-urlencoded` NOT `application/json` for token endpoint

---

## Phase 4 — SP-API Call (THE MAIN FAILURE)

### ❌ What Failed — ALL API CALLS RETURN 403

**Endpoint tested:** `GET /sellers/v1/marketplaceParticipations`  
**Base URL:** `https://sellingpartnerapi-fe.amazon.com`  
**Headers used:**
```
x-amz-access-token: <valid_access_token>
Content-Type: application/json
User-Agent: MadeInHeavens/1.0 (Language=Python/3.x; Platform=macOS)
```

**HTTP Response:** `403 Forbidden`  
**Error Body:**
```json
{
  "errors": [{
    "message": "Access to requested resource is denied.",
    "code": "Unauthorized",
    "details": ""
  }]
}
```
**Response Header:** `x-amzn-ErrorType: AccessDeniedException`

#### All Attempts That Failed:
| # | What Changed | Result |
|---|---|---|
| 1 | App 1 + Basic headers | 403 AccessDeniedException |
| 2 | App 1 + User-Agent header added | 403 AccessDeniedException |
| 3 | App 1 + Re-authorization with `version=beta` | 403 AccessDeniedException |
| 4 | App 2 (completely new app + fresh credentials) | 403 AccessDeniedException |
| 5 | App 2 + verbose curl (`-v` flag) | 403 AccessDeniedException (confirmed HTTP level) |

### ⚠️ Care Points
- `x-amzn-ErrorType: AccessDeniedException` = **authenticated but NOT authorized**
- Token is valid (authentication passes) but account/app lacks permission (authorization fails)
- Same error across 2 different apps = **account-level restriction**, not app-level

---

## Phase 5 — Alternative Testing Methods Attempted

### ❌ What Failed

1. **Python script (`sp_api_test_v1.0.py`) on sandbox**
   - **Error:** Proxy/network restrictions in sandbox environment blocked outbound HTTPS
   - **Environment:** Claude sandbox Linux container
   
2. **Python script on user's Mac**
   - **Error:** `zsh: command not found: python` and `pip`
   - **Reason:** macOS requires `python3`/`pip3`, and Xcode CLI tools weren't installed
   - **Fix approach:** Switched to curl commands instead

3. **Browser-based fetch() API test**
   - **What tried:** `fetch('https://api.amazon.com/auth/o2/token', ...)` from Chrome console on Google.com and Seller Central
   - **Error:** CORS policy blocked the request
   - **Reason:** SP-API is server-side only — browser cannot make cross-origin requests to Amazon API endpoints
   - **Environment:** Chrome browser on any domain

4. **Sandbox curl test**
   - **Error:** Network proxy blocked `api.amazon.com` in sandbox
   - **Fix:** User ran curl commands on local Mac Terminal

### ✅ What Worked
- **Local Mac Terminal curl** — only working environment for API testing
- **macOS `curl` is pre-installed** — no additional setup needed

### ⭐ Best Method for API Testing
**Use local Mac Terminal with curl commands.** This is the most reliable method because:
- curl is pre-installed on macOS
- No Python/pip dependency issues
- No CORS restrictions
- No proxy/sandbox blocks
- Single combined command auto-extracts token and makes API call

---

# SECTION 2: LATER ANALYSIS (Final Truth) — TRUST THIS SECTION

---

## Updated Account Investigation (10 April 2026, Evening)

### What We Discovered by Reading Seller Central Pages:

#### Account Information Page (`/hz/sc/account-information`):
- **Warning displayed:** "You currently have limited access to Amazon selling services"
- **Deactivation notice:** "Your account has been deactivated due to inactivity" — THIS APPLIES TO NON-INDIA MARKETPLACES
- **Required for full access:** Identity Information, Reactivate Account, Charge Methods

#### Store Status Table:
| Country | Listing Status |
|---------|---------------|
| **India** | **Active** ✅ |
| **Australia** | **Active** ✅ |
| USA | Inactive ❌ |
| Canada | Inactive ❌ |
| Mexico | Inactive ❌ |
| All Europe | Inactive ❌ |

#### Selling Plan (Manage Your Services - `/account-information/mys`):
| Region | Plan |
|--------|------|
| **India** | **Professional** ✅ |
| Americas | Individual |
| Australia | Individual |
| Europe | Individual |

### ✅ What IS Correct:
- India account is **ACTIVE**
- India has **Professional** selling plan (required for SP-API)
- Developer Profile is **APPROVED**
- Token generation **WORKS** perfectly
- App roles are **SAVED** on backend (confirmed via internal API)
- Draft status is **OK** for Private developers
- AWS Signature V4 is **NOT required** (deprecated Oct 2023)

### ❌ What is STILL Failing:
- **ALL SP-API endpoint calls return HTTP 403 AccessDeniedException**
- Error is identical across both App 1 and App 2
- Error persists with User-Agent header, without it, with version=beta authorization

### 🔍 Remaining Possible Root Causes (TO INVESTIGATE):

1. **"Limited access" account restriction** — Even though India listing is Active and Professional, the overall account-level "limited access" warning + pending Identity Information / Charge Methods could be blocking API access at a higher level

2. **App roles not properly propagated** — Although backend shows roles saved, there may be a propagation delay or the roles need explicit "Submit" action that Shadow DOM prevented

3. **Seller account not fully verified** — The "re-verify your identity" requirement, even if for other marketplaces, might impose a global API restriction

4. **SP-API specific account flag** — Amazon may have a separate internal flag for API access that requires account to be fully compliant (no pending verifications on ANY marketplace)

5. **Time delay** — Some SP-API authorizations take hours to propagate

---

# ❌ GLOBAL FAILURE LIST

## Network / Environment Issues
| Issue | Environment | Details |
|-------|------------|---------|
| Proxy blocks API calls | Claude sandbox | Cannot reach api.amazon.com |
| CORS blocks fetch() | Chrome browser | SP-API is server-side only |
| Python not found | macOS | Needs `python3` not `python`, Xcode CLI tools not installed |

## SP-API Authorization Issues
| Issue | Details |
|-------|---------|
| 403 AccessDeniedException | Authenticated but not authorized — account-level restriction |
| Same error on 2 different apps | Confirms NOT app-specific issue |
| version=beta didn't help | Draft app authorization parameter made no difference |

## Seller Central Automation Issues
| Issue | Details |
|-------|---------|
| Shadow DOM blocks form submit | KAT web components prevent standard click automation |
| "Save and exit" button doesn't fire POST | Forms auto-save via PUT during navigation instead |
| Screenshot blank in Chrome MCP | Seller Central renders partially in headless-like capture |

---

# ENVIRONMENT NOTES

| Environment | Works? | Notes |
|-------------|--------|-------|
| **Mac Terminal (curl)** | ✅ Yes | Best for API testing, curl pre-installed |
| Claude Sandbox (Python/curl) | ❌ No | Proxy blocks Amazon API endpoints |
| Chrome Browser (fetch/JS) | ❌ No | CORS blocks cross-origin SP-API calls |
| Mac (Python) | ❌ No | python3/pip3 needed, Xcode CLI tools required |
| Chrome MCP (screenshots) | ⚠️ Partial | Seller Central pages sometimes render blank |
| Chrome MCP (read_page/JS) | ✅ Yes | Can read DOM, execute JS, extract data |

---

# ⭐ BEST METHODS SUMMARY

## For Token Generation:
**Single curl command on Mac Terminal** (see Phase 3 above)
- Primary: Combined curl command (auto-extract token + API call)
- Fallback: Two-step curl (manual copy-paste token)

## For Seller Central Inspection:
**Chrome MCP `read_page` + `javascript_tool`**
- Primary: `read_page` for DOM tree → `javascript_tool` for specific data extraction
- Fallback: Computer-use screenshot (unreliable for Seller Central)

## For Form Automation on Seller Central:
**Manual by user is most reliable**
- Primary: Ask user to click/submit manually
- Fallback: Chrome MCP `left_click` on ref elements (works sometimes)
- NEVER rely on: Shadow DOM JS click dispatch (unreliable)

## For Checking Account/API Status:
**Internal Seller Central APIs via `javascript_tool`:**
- Developer status: `fetch('/apps/apis/intake/v2/developer/status')`
- App details: `fetch('/apps/apis/intake/solutions/')`
- These bypass UI rendering issues

---

# EXACT STEPS TO REPRODUCE SP-API TEST

1. Open **Mac Terminal**
2. Run combined curl command (replace credentials):
```bash
TOKEN=$(curl -s -X POST https://api.amazon.com/auth/o2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "refresh_token=<REFRESH_TOKEN>" \
  -d "client_id=<CLIENT_ID>" \
  -d "client_secret=<CLIENT_SECRET>" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4) && \
echo "Token: ${TOKEN:0:20}..." && \
curl -v -X GET "https://sellingpartnerapi-fe.amazon.com/sellers/v1/marketplaceParticipations" \
  -H "x-amz-access-token: $TOKEN" \
  -H "Content-Type: application/json" \
  -H "User-Agent: MadeInHeavens/1.0"
```
3. **Expected current result:** 403 AccessDeniedException
4. **Expected after fix:** 200 OK with marketplace participation data

---

# SUPPORT TICKETS RAISED

## Email 1 — SP-API Feedback Channel
- **To:** selling-partner-api-feedback@amazon.com
- **Subject:** SP-API Access Denied (403 AccessDeniedException) - India Marketplace - Private Developer Application - Urgent
- **Sent:** 10 April 2026
- **Status:** Awaiting reply
- **Note:** This is a feedback email, may not get direct support response

## Email 2 — Amazon India Seller Support
- **To:** seller-support@amazon.in
- **Subject:** SP-API Access Denied (403) for Private Developer - India Marketplace - Entity ID: ENTITY1TVPGA5B1GOJW
- **Sent:** 10 April 2026
- **Status:** Awaiting reply

## Best Channel for Private Developers (Manual — User Must Do):
- **Seller Central Help Center** → "Other question or request" → Enter business name + email → Submit
- URL: https://sellercentral.amazon.in/cu/contact-us
- **Note:** Solution Provider Support portal (developer.amazonservices.com/support) is for third-party solution providers ONLY, NOT for private sellers/developers

## Monitoring:
- Gmail monitoring scheduled task (`gmail-monitor-amazon-ads`) updated to check for SP-API support replies every 6 hours

---

# PHASE 6: AMAZON ADS API — COMPLETE OAuth2 SETUP ✅

## 6.1 Redirect URI Setup
- **Step:** Added `https://www.amazon.com/ap/oa` as Allowed Return URL in LWA Web Settings
- **Location:** developer.amazon.com → Security Profiles → GoAmrita Ads API → Web Settings
- **Result:** ✅ SAVED SUCCESSFULLY

## 6.2 OAuth2 Authorization
- **Step:** Navigated to OAuth2 consent URL with scope `advertising::campaign_management`
- **URL:** `https://www.amazon.com/ap/oa?client_id=amzn1.application-oa2-client.[REDACTED]&scope=advertising::campaign_management&response_type=code&redirect_uri=https://www.amazon.com/ap/oa`
- **Result:** ✅ Consent page appeared → User authorized → Got auth code `ANExIHWbLMKdgPIUDTEU`
- **Note:** Redirect page showed "400 Bad Request" error — this is EXPECTED because redirect URI is amazon.com/ap/oa itself. The auth code was in the URL params.

## 6.3 Token Exchange
- **Step:** POST to `https://api.amazon.com/auth/o2/token` with grant_type=authorization_code
- **Result:** ✅ GOT BOTH TOKENS
  - **Access Token:** Atza|gQAhmLGj... (valid ~1 hour)
  - **Refresh Token:** Atzr|IwEBIAxz9jlY... (long-lived, stored in api_credentials.json)
- **Note:** Sandbox curl blocked by proxy. Used Chrome browser fetch() instead.

## 6.4 Profile ID Retrieval
- **Step:** GET `https://advertising-api-eu.amazon.com/v2/profiles`
- **Result:** ✅ PROFILE FOUND
  - **Profile ID:** 42634532240933
  - **Country:** IN (India)
  - **Currency:** INR
  - **Timezone:** Asia/Kolkata
  - **Account Name:** Made in Heavens
  - **Account Type:** Seller
  - **Seller ID:** A2AC2AS9R9CBEA
  - **Marketplace ID:** A21TJRUUN4KGV
  - **Valid Payment:** true

## 6.5 First API Test Call — Campaigns List
- **Step:** POST `https://advertising-api-eu.amazon.com/sp/campaigns/list`
- **Headers:** Authorization Bearer token + ClientId + Scope (Profile ID)
- **Result:** ✅ CAMPAIGNS RETURNED
  - Campaign 1: "Campaign - 13/1/2026 21:20:59.241" — ₹500/day, ENABLED, Manual
  - Campaign 2: "Campaign - Red- Horsepower" — ₹500/day, ENABLED, Manual
  - More campaigns available...

## GLOBAL SUCCESS — ADS API FULLY OPERATIONAL 🎉

---

# PENDING INVESTIGATION / NEXT STEPS

1. **Complete "Identity Information" and "Charge Methods"** on Account Information page — these are pending and might block SP-API globally
2. **Raise case via Seller Central Help Center** manually — Select "Other question or request", paste details from Email 2
3. **Wait for support reply** — monitoring every 6 hours via Gmail task
4. **Re-test SP-API** after account issues resolved
5. ~~**Amazon Ads API** — still in PENDING APPROVAL status~~ → ✅ **COMPLETED — Ads API fully working!**
6. **Build automation scripts** using Ads API refresh token and profile ID

---

# PHASE 7: ADS API AUTOMATION SCRIPTS ✅

## 7.1 Scripts Created
- **ads_api_v1.0.py** — Full automation: health_check, list_campaigns, budget_overview, campaign_stats
- **ads_quick_test_v1.0.py** — Quick 3-step test: Token → Profile → Campaigns

## 7.2 End-to-End Test Results
- ✅ Token refresh: Working (3600s expiry)
- ✅ Profile fetch: Made in Heavens | ID 42634532240933 | IN/INR
- ✅ Campaigns list: 100 campaigns (54 enabled, 46 paused)
- ✅ Budget calc: ₹92,967/day active, ₹27.9L/month estimate
- ⚠️ Note: Scripts need to run on local machine (sandbox proxy blocks api.amazon.com)

## 7.3 Usage
```bash
python3 ads_api_v1.0.py --action health_check
python3 ads_api_v1.0.py --action list_campaigns
python3 ads_api_v1.0.py --action budget_overview
python3 ads_api_v1.0.py --action all
python3 ads_quick_test_v1.0.py
```

---

*Last Updated: 10 April 2026, 10:00 PM IST*  
*Version: 1.3*
