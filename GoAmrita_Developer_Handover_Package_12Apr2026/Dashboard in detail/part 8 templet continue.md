Yes. This is the final piece that ties everything together.

Without the registry, even standardized summaries will stay scattered.    
With the registry, dashboards can auto-discover all future modules cleanly.

So this should be the 4th template.

\*\*Registry Entry Template\*\*  
Purpose:  
Tell the system:  
\- what reports exist  
\- where they are  
\- which dashboard should use them  
\- how important they are  
\- how they should be shown

This is not raw module output.    
This is the dashboard discovery layer.

\*\*1. Human-Friendly Registry Template\*\*  
\`\`\`md  
\# Report Registry Entry

\#\# 1\. Identity  
\- Feature ID:  
\- Feature Key:  
\- Feature Name:  
\- Module Group:

\#\# 2\. Report Availability  
\- Raw output file:  
\- Impact summary file:  
\- Activity summary file:  
\- Detail report file:  
\- Latest generated at:

\#\# 3\. Dashboard Visibility  
\- Show on Main Dashboard: Yes / No  
\- Show on Activity Dashboard: Yes / No  
\- Show on Homepage: Yes / No  
\- Main Dashboard section:  
\- Activity Dashboard section:

\#\# 4\. Importance  
\- Status:  
\- Impact level:  
\- Priority score:  
\- Strategic weight:  
\- Is critical: Yes / No

\#\# 5\. Display Rules  
\- Headline to show:  
\- Badge/color:  
\- Sort order:  
\- Collapse by default: Yes / No  
\- Pin to top when:

\#\# 6\. Review / Action State  
\- Needs review: Yes / No  
\- Needs approval: Yes / No  
\- Has warnings: Yes / No  
\- Has errors: Yes / No

\#\# 7\. Notes  
\- Dashboard note:  
\- Developer note:  
\- Migration note:  
\`\`\`

\*\*2. Strict JSON Registry Template\*\*  
\`\`\`json  
{  
  "schema\_type": "registry\_entry",  
  "schema\_version": "1.0",

  "feature\_id": "",  
  "feature\_key": "",  
  "feature\_name": "",  
  "module\_group": "",

  "files": {  
    "raw\_output": "",  
    "impact\_summary": "",  
    "activity\_summary": "",  
    "detail\_report": ""  
  },

  "generated\_at": "",

  "dashboard\_visibility": {  
    "show\_on\_main": true,  
    "show\_on\_activity": true,  
    "show\_on\_home": true,  
    "main\_section": "",  
    "activity\_section": ""  
  },

  "importance": {  
    "status": "success",  
    "impact\_level": "medium",  
    "priority\_score": 50,  
    "strategic\_weight": 5,  
    "is\_critical": false  
  },

  "display\_rules": {  
    "headline": "",  
    "badge": "",  
    "sort\_order": 50,  
    "collapse\_by\_default": false,  
    "pin\_to\_top\_when": \[\]  
  },

  "review\_state": {  
    "needs\_review": false,  
    "needs\_approval": false,  
    "has\_warnings": false,  
    "has\_errors": false  
  },

  "notes": {  
    "dashboard\_note": "",  
    "developer\_note": "",  
    "migration\_note": ""  
  }  
}  
\`\`\`

\*\*3. Central Registry File\*\*  
You can keep one file like:  
\- \`report\_registry\_latest.json\`

Inside it:  
\`\`\`json  
{  
  "schema\_type": "report\_registry",  
  "schema\_version": "1.0",  
  "generated\_at": "2026-04-15T12:00:00Z",  
  "entries": \[  
    {  
      "feature\_id": "M01",  
      "feature\_key": "competitor\_tracker",  
      "feature\_name": "Competitor Tracker",  
      "module\_group": "market\_intelligence",  
      "files": {  
        "raw\_output": "Json/competitor\_tracker\_latest.json",  
        "impact\_summary": "Json/impact\_competitor\_tracker\_latest.json",  
        "activity\_summary": "Json/activity\_competitor\_tracker\_latest.json",  
        "detail\_report": "Json/competitor\_tracker\_20260415\_120000.json"  
      },  
      "generated\_at": "2026-04-15T12:00:00Z",  
      "dashboard\_visibility": {  
        "show\_on\_main": true,  
        "show\_on\_activity": true,  
        "show\_on\_home": true,  
        "main\_section": "Critical Business Risks",  
        "activity\_section": "Module Run Table"  
      },  
      "importance": {  
        "status": "success",  
        "impact\_level": "high",  
        "priority\_score": 84,  
        "strategic\_weight": 9,  
        "is\_critical": true  
      },  
      "display\_rules": {  
        "headline": "1 buy box threat detected",  
        "badge": "critical",  
        "sort\_order": 10,  
        "collapse\_by\_default": false,  
        "pin\_to\_top\_when": \["buy\_box\_lost\_count \> 0"\]  
      },  
      "review\_state": {  
        "needs\_review": true,  
        "needs\_approval": false,  
        "has\_warnings": true,  
        "has\_errors": false  
      },  
      "notes": {  
        "dashboard\_note": "Show in main risk block",  
        "developer\_note": "",  
        "migration\_note": "Legacy modules not yet migrated"  
      }  
    }  
  \]  
}  
\`\`\`

\*\*4. Registry Rules\*\*  
This registry should be the only dashboard discovery source.

Meaning:  
\- dashboard should not guess files  
\- dashboard should not hardcode feature paths  
\- dashboard should read registry and render from it

That is the clean architecture.

\*\*5. Registry Responsibilities\*\*  
The registry should answer:  
\- what reports exist  
\- which are latest  
\- which matter most  
\- where to show them  
\- what needs attention first

\*\*6. Suggested Display Badge Values\*\*  
To keep UI consistent:  
\- \`success\`  
\- \`warning\`  
\- \`failed\`  
\- \`critical\`  
\- \`review\`  
\- \`info\`

\*\*7. Suggested Sort Logic\*\*  
For homepage:  
1\. \`is\_critical \= true\`  
2\. higher \`priority\_score\`  
3\. newer \`generated\_at\`  
4\. \`needs\_review \= true\`

That will keep important modules on top automatically.

\*\*8. Final Architecture\*\*  
So for all future modules:

\- Raw JSON  
  module-specific  
\- Impact Summary  
  main dashboard  
\- Activity Summary  
  activity dashboard  
\- Registry Entry  
  discovery \+ ordering \+ placement

This is the full clean system.

\*\*9. Team Rule\*\*  
I would define this very clearly:

A future module is not complete unless it provides:  
\- raw output  
\- impact summary  
\- activity summary  
\- registry entry

That one rule will keep your architecture stable.

\*\*10. Best Next Documentation Set\*\*  
Now you effectively have the full future standard:

1\. Feature Registration Template  
2\. Impact Summary Template  
3\. Activity Summary Template  
4\. Registry Entry Template

That is enough to start building future modules in a disciplined way without touching legacy modules yet.

