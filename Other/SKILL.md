---
name: amazon-ads-thursday-analysis
description: Every Thursday 9 PM — analyze Budget + Search Term reports, generate Excel approval sheet for GoAmrita Bhandar
---

You are running the weekly Thursday Amazon Ads analysis for GoAmrita Bhandar (India).

OBJECTIVE: Download the Budget report and Search Term report from Amazon Advertising India, analyze them for budget issues, wasted spend, winning search terms, and keyword harvesting opportunities. Generate a professional Excel approval sheet with data-validated dropdown Status columns. Present the file to the user and WAIT for approval before making any changes.

CRITICAL RULES:
1. NEVER make any changes to campaigns, bids, or keywords without explicit user approval
2. SKIP any campaign created in the last 10 days (learning phase) — enforce this in code
3. Use TARGET_ACOS = 25% as the reference for all threshold calculations
4. All suggestions go into an Excel approval sheet with dropdowns: PENDING APPROVAL / APPROVED / SKIP / STRONGLY APPROVED BY ME, YOU JUST REVIEW
5. Treat PENDING APPROVAL same as SKIP when implementing — only APPROVED and STRONGLY APPROVED items get executed
6. MANDATORY FIRST STEP: Before starting ANY work, read PROVEN_METHODS.md from this skill folder. It contains all proven working methods, known broken approaches, edge cases, and column mappings. Follow it strictly — do NOT retry anything listed under "What Doesn't Work".
7. MANDATORY LAST STEP: After completing the session, UPDATE PROVEN_METHODS.md with any new learnings — new things that worked, new things that failed, new edge cases discovered. This file is the living knowledge base. Never skip this update.

STEPS:
1. Call tabs_context_mcp to get browser tab context
2. Mount ~/Downloads using mcp__cowork__request_cowork_directory
3. Navigate to https://advertising.amazon.in/reports?entityId=ENTITY1TVPGA5B1GOJW
4. Download "Sponsored Products Budget report last 7 days" and "Sponsored Products Search term report last 7 days"
5. Wait for files to appear in Downloads, then load with pandas + openpyxl engine
6. Apply 10-day campaign filter (exclude anything created < 10 days ago)
7. Analyze Budget report: ACOS-aware suggestions (capped + low ACOS = increase budget; capped + high ACOS = reduce bids first)
8. Analyze Search Terms: winners (ACOS < 30%, sales > 0, clicks >= 5) → promote to Exact; losers (clicks >= 8 OR spend >= ₹300, zero sales) → negative; high ACOS (2x+ target) → bid down or negate
9. Detect duplicate search terms across campaigns
10. Detect auto-campaign winners for keyword harvesting (auto → manual Exact)
11. Build Excel approval sheet with sheets: Overview, Budget Changes, Negative Keywords, High ACOS Terms, Promote to Exact, Harvest Auto to Exact, Duplicates Alert
12. Add DataValidation dropdowns on all Status columns with 4 options: "PENDING APPROVAL","APPROVED","SKIP","STRONGLY APPROVED BY ME, YOU JUST REVIEW"
13. Save to Downloads folder and present to user via mcp__cowork__present_files
14. WAIT for user approval — do NOT implement anything until user says "approved"
15. After approval: read the approved Excel, implement ONLY APPROVED and STRONGLY APPROVED items using BULK UPLOAD method (see IMPLEMENTATION AUTOMATION below)

IMPLEMENTATION AUTOMATION (after user approves):
Step A — Download current bulk sheet from Amazon Ads:
  1. Navigate to https://advertising.amazon.in/bulksheet/HomePage?entityId=ENTITY1TVPGA5B1GOJW
     (DO NOT use /cm/bulkOperations — broken URL. Use sidebar "Bulk operations" button if direct URL fails.)
  2. In "Create spreadsheet for download": select Sponsored Products, date range = "Last 30 days", click "Create spreadsheet"
  3. Wait for processing → download the generated .xlsx file
  4. Parse with openpyxl to extract all Campaign IDs, Ad Group IDs, Campaign Names, Ad Group Names

Step B — Build bulk upload spreadsheet (Python + openpyxl):
  ```python
  NUM_COLS = 53  # Amazon bulk sheet has 53 columns for Sponsored Products
  HEADER = ['Product','Entity','Operation','Campaign Id','Ad Group Id',
            'Portfolio Id','Ad Id','Keyword Id','Product Targeting Id',
            'Campaign Name','Ad Group Name','Campaign Name (Informational only)',
            'Ad Group Name (Informational only)','Portfolio Name (Informational only)',
            'Start Date','End Date','Targeting Type','State','Daily Budget',
            'Budget Type','Daily Budget','SKU','ASIN','Eligibility Status (Informational only)',
            'Reason for ineligibility (Informational only)','Ad Group Default Bid',
            'Ad Group Default Bid Adjustment','Bid','Keyword Text','Match Type',
            'Bidding Strategy','Placement Type','Percentage','Campaign Bidding Strategy',
            'Match Type','Negative Keyword Text','Product Targeting Expression',
            'Resolved Product Targeting Expression (Informational only)',
            'In-budget amount percentage for out-of-budget campaigns','Impression Share',
            'Budget Rule Name','Budget Rule Type','Budget Rule Amount','Budget Rule Duration',
            'Budget Rule Start Date','Budget Rule End Date','Budget Rule Recurrence',
            'Budget Rule Performance Threshold','Budget Rule Suggested Budget',
            'Budget Rule Last Evaluated Date','Budget Rule Last Increased Date',
            'Created Date','Last Updated Date']
  
  def make_row(col_vals):
      row = [None] * NUM_COLS
      row[0] = 'Sponsored Products'
      for k, v in col_vals.items():
          row[k] = v
      return row
  
  # Budget change:  make_row({1:'Campaign', 2:'Update', 3:cid, 9:campaign_name, 20:budget_val})
  # Negative keyword: make_row({1:'Negative Keyword', 2:'Create', 3:cid, 4:agid, 17:'enabled', 28:search_term, 31:'Negative Exact'})
  # New exact keyword: make_row({1:'Keyword', 2:'Create', 3:cid, 4:agid, 17:'enabled', 27:5.0, 28:search_term, 31:'Exact'})
  ```
  Use find_campaign_id() with partial matching (first 25 chars) for long campaign names.
  Use find_adgroup_id() to match ad group within the campaign, fallback to first ad group.
  Log any campaigns NOT found — report these to user for manual review.

Step C — Save and present:
  1. Save as `UPLOAD_THIS_GoAmrita_BulkChanges_<N>rows.xlsx` in Downloads folder
  2. The "UPLOAD_THIS_" prefix tells the user which file to upload
  3. Navigate browser to Bulk Operations upload page
  4. Tell user: "Downloads folder में UPLOAD_THIS_... file select करो, Choose file click करो, upload करो"
  NOTE: Chrome MCP file_upload and JS DataTransfer injection are BLOCKED by Amazon security.
        The user MUST manually click "Choose file" and select the file. This is the ONE manual step.

Step D — After user confirms upload:
  1. Take screenshot of Bulk Operations page to check processing status
  2. Wait for "Complete" status
  3. Check for any errors in the processing results
  4. Report final summary to user

FULL INSTRUCTIONS: Read the SKILL.md file at the task's skill directory for complete code and detailed steps.

PROVEN WORKING:
- Always use pandas + openpyxl engine to read Excel (raw openpyxl = 1 row only)
- Click download icon on Reports page sends file to Mac ~/Downloads/
- Campaign not found in console → remove "Active status: Enabled" filter chip
- Budget edit: search campaign → "..." menu → Edit settings → change budget → Save
- Bulk upload is MUCH faster than one-by-one UI changes (92 changes in 1 file vs hours of clicking)
- File naming with "UPLOAD_THIS_" prefix helps user identify the correct file
- Amazon bulk sheet column indices: Entity=1, Operation=2, CampaignId=3, AdGroupId=4, CampaignName=9, State=17, Budget=20, Bid=27, KeywordText=28, MatchType=31

NEVER DO:
- Download via Chrome sandbox / XHR / fetch / curl → CORS errors
- Use advertising.amazon.in/cm/bulkOperations → broken URL (use /bulksheet/HomePage instead)
- Make changes without approval
- Touch campaigns created < 10 days ago
- Try Chrome MCP file_upload on Amazon Ads → always returns "Not allowed"
- Try JS DataTransfer/base64 injection on Amazon file inputs → blocked by security
- Use integer keys as **kwargs in Python (use dict parameter instead)