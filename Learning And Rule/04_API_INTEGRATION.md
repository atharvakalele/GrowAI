# 🌐 04 — API & Integration Rules v1.0
**When to apply:** When working with ANY API (Amazon SP-API, Ads API, Google APIs, etc.)

---

## Rule 1: Official Docs First — ALWAYS
- **CRITICAL:** Before touching any API, read the LATEST official documentation
- API providers change endpoints, functions, parameters periodically
- Public internet info may reference old/deprecated methods
- Official docs URL should be bookmarked and checked every time

## Rule 2: Correct Endpoint Verification
- Every API has region-specific endpoints
- **NEVER assume** which endpoint to use based on geography alone
- Always verify from official docs which region your marketplace belongs to
- Example lesson: India marketplace → EUROPE region (not Far East!) for Amazon SP-API

## Rule 3: API Version Lock
- Identify the EXACT API version we are using
- Only use methods, functions, and parameters from THAT version
- Never mix methods from different API versions
- Check if any methods are deprecated in our version

## Rule 4: Token & Authentication
- Understand the full auth flow before implementing
- Handle token refresh properly (expiry, caching, rotation)
- Store credentials securely in config files
- Handle long tokens carefully — verify full token is saved (no truncation)
- Set up secret rotation reminders before deadlines

## Rule 5: Error Handling for API Calls
- Always wrap API calls in try-catch/error handling
- Log full error response (status code + body)
- Implement retry logic with backoff for transient errors
- Have fallback strategies for API failures

## Rule 6: Rate Limiting & Throttling
- Respect API rate limits
- Implement throttling in automation scripts
- Log rate limit headers if provided
- Back off when approaching limits

## Rule 7: Test in Sandbox/Test Mode First
- Use sandbox endpoints if available
- Test with minimal data before full-scale operations
- Verify response structure matches documentation

---

## 🔴 API Mistakes We Made (Lessons Learned)

| # | Mistake | Impact | Fix |
|---|---------|--------|-----|
| 1 | Used FE endpoint for India SP-API | 403 errors all day | India = EU region, use `sellingpartnerapi-eu.amazon.com` |
| 2 | Token truncated during save | `invalid_grant` error | Extract long tokens in parts, verify full length |
| 3 | Sandbox proxy blocks Amazon APIs | curl/python failed from sandbox | Use browser fetch or local Terminal for API calls |
| 4 | SP-API CORS in browser | Browser blocks cross-origin | Use Python/local scripts, not browser for SP-API |
| 5 | Mixed up Ads API vs SP-API auth | Different auth headers | Ads: `Authorization: Bearer`, SP-API: `x-amz-access-token` |

---

## 📋 API Integration Checklist
- [ ] Read official documentation (latest version)
- [ ] Confirm correct endpoint for our region/marketplace
- [ ] Verify API version compatibility
- [ ] Set up proper authentication flow
- [ ] Test with minimal request first
- [ ] Implement error handling & logging
- [ ] Handle rate limits
- [ ] Store credentials in config (not hardcoded)
- [ ] Document all API details for future reference

---
*Category: API & Integration | Source: Msir's Universal Rulebook + Session Learnings*
