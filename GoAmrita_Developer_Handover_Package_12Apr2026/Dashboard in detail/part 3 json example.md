Here is the clean contract I recommend for all future modules.

\*\*Goal\*\*  
Every new module writes:  
- `raw output`  
- `impact summary`  
- `activity summary`

Optional:  
- `detail report`  
- `registry entry`

This gives you one standard for dashboards without forcing old modules to change now.

\*\*1. Impact Summary\*\*  
Purpose:  
For Main Dashboard only.  
This should describe business effect, not technical logs.

Suggested structure:  
```json  
{  
"schema\_type": "impact\_summary",  
"schema\_version": "1.0",  
"feature\_id": "M01",  
"feature\_key": "competitor\_tracker",  
"feature\_name": "Competitor Tracker",  
"module\_group": "market\_intelligence",  
"generated\_at": "2026-04-15T10:30:00Z",  
"period": "daily",  
"status": "success",  
"impact\_level": "high",  
"business\_area": \["profit", "buy\_box", "rank", "conversion"],  
"headline": "1 critical buy box risk found, revenue protected on 4 ASINs",  
"summary\_metrics": {  
"profit\_impact\_rs": 0,  
"loss\_prevented\_rs": 2500,  
"waste\_blocked\_rs": 0,  
"revenue\_protected\_rs": 4200,  
"rank\_up\_count": 3,  
"rank\_down\_count": 1,  
"buy\_box\_won\_count": 12,  
"buy\_box\_lost\_count": 1  
},  
"positive\_impacts": \[  
"4 ASINs had low competitor pressure",  
"3 products improved rank"  
],  
"negative\_impacts": \[  
"1 ASIN lost buy box",  
"2 ASINs under pricing pressure"  
],  
"top\_winners": \[  
{  
"entity\_type": "asin",  
"entity\_id": "B0XXXX",  
"label": "Product A",  
"impact\_note": "Rank improved by 5 positions"  
}  
],  
"top\_risks": \[  
{  
"entity\_type": "asin",  
"entity\_id": "B0YYYY",  
"label": "Product B",  
"impact\_note": "No buy box detected"  
}  
],  
"ai\_learning": {  
"new\_rule\_learned": false,  
"rule\_promoted\_count": 0,  
"confidence": 0.82  
},  
"detail\_ref": {  
"raw\_file": "Json/competitor\_tracker\_latest.json",  
"detail\_file": "Json/competitor\_tracker\_20260415\_103000.json"  
}  
}  
```

\*\*Important Rule\*\*  
Impact summary must answer only:  
- what changed in business  
- what value/risk happened  
- who won  
- who is at risk

No retry logs, no stack traces, no scheduler details.

\*\*2. Activity Summary\*\*  
Purpose:  
For Activity Dashboard only.  
This should describe what the system did.

Suggested structure:  
```json  
{  
"schema\_type": "activity\_summary",  
"schema\_version": "1.0",  
"feature\_id": "M01",  
"feature\_key": "competitor\_tracker",  
"feature\_name": "Competitor Tracker",  
"module\_group": "market\_intelligence",  
"generated\_at": "2026-04-15T10:30:00Z",  
"run\_id": "M01\_20260415\_103000",  
"status": "success",  
"run\_mode": "scheduled",  
"duration\_sec": 94,  
"freshness\_hours": 24,  
"input\_sources": \[  
"sp\_product\_ads\_list.json",  
"sp\_advertisedproduct\_daily.json",  
"SP-API Pricing"  
],  
"output\_files": \[  
"Json/competitor\_tracker\_latest.json",  
"Json/competitor\_tracker\_20260415\_103000.json"  
],  
"counts": {  
"items\_scanned": 30,  
"items\_processed": 30,  
"alerts\_generated": 1,  
"approvals\_needed": 0,  
"warnings": 2,  
"errors": 0  
},  
"run\_events": \[  
"Loaded top 30 ASINs",  
"Fetched pricing batches",  
"Saved latest report"  
],  
"warnings\_list": \[  
"1 ASIN returned no buy box"  
],  
"errors\_list": \[],  
"needs\_review": false,  
"review\_items": \[]  
}  
```

\*\*Important Rule\*\*  
Activity summary must answer only:  
- did it run  
- what it read  
- what it created  
- what failed  
- what needs review

No business interpretation here.

\*\*3. Report Registry\*\*  
Purpose:  
One central file the dashboards read.  
This is the discovery layer.

Instead of scanning random files, dashboard reads one registry.

Suggested structure:  
```json  
{  
"schema\_type": "report\_registry",  
"schema\_version": "1.0",  
"generated\_at": "2026-04-15T10:35:00Z",  
"reports": \[  
{  
"feature\_id": "M01",  
"feature\_key": "competitor\_tracker",  
"feature\_name": "Competitor Tracker",  
"module\_group": "market\_intelligence",  
"dashboard\_targets": \["main", "activity"],  
"status": "success",  
"impact\_level": "high",  
"generated\_at": "2026-04-15T10:30:00Z",  
"impact\_summary\_file": "Json/impact\_competitor\_tracker\_latest.json",  
"activity\_summary\_file": "Json/activity\_competitor\_tracker\_latest.json",  
"raw\_file": "Json/competitor\_tracker\_latest.json",  
"priority": 80,  
"show\_on\_home": true  
}  
]  
}  
```

This should be the only file the dashboard needs for discovery.

\*\*4. File Naming Rule\*\*  
For future modules, keep naming predictable.

Recommended:  
- raw file:  
`Json/<feature\_key>\_latest.json`  
- dated raw:  
`Json/<feature\_key>\_<timestamp>.json`  
- impact summary:  
`Json/impact\_<feature\_key>\_latest.json`  
- activity summary:  
`Json/activity\_<feature\_key>\_latest.json`

Example:  
- `competitor\_tracker\_latest.json`  
- `impact\_competitor\_tracker\_latest.json`  
- `activity\_competitor\_tracker\_latest.json`

\*\*5. Field Standards\*\*  
To avoid future confusion, standardize these values everywhere:

Status:  
- `success`  
- `partial`  
- `warning`  
- `failed`

Impact level:  
- `low`  
- `medium`  
- `high`  
- `critical`

Run mode:  
- `manual`  
- `scheduled`  
- `event`  
- `retry`

Needs review:  
- `true`  
- `false`

\*\*6. Which Dashboard Uses What\*\*  
Main Dashboard reads:  
- only `impact summary`

Activity Dashboard reads:  
- only `activity summary`

Registry:  
- tells dashboard what exists and where

Raw files:  
- for deep detail or later drill-down

\*\*7. Minimal Required Fields For Every New Module\*\*  
If you want a strict minimum, every new feature must at least produce:

Impact summary minimum:  
- feature id  
- feature key  
- feature name  
- generated\_at  
- status  
- headline  
- summary\_metrics  
- top\_risks  
- detail\_ref

Activity summary minimum:  
- feature id  
- feature key  
- generated\_at  
- run\_id  
- status  
- duration\_sec  
- input\_sources  
- output\_files  
- counts  
- errors\_list

\*\*8. Good Module Rule\*\*  
Every future module should ask before saving:

Impact side:  
- what business changed?  
- what improved?  
- what got worse?  
- what matters most?

Activity side:  
- what did I do?  
- what did I use?  
- what did I produce?  
- what failed?

\*\*9. Migration Strategy Later\*\*  
When you migrate old modules later:  
- keep old raw JSON untouched  
- add wrapper script or summary builder  
- generate impact summary and activity summary from old output  
- register it in registry

That way migration is safe.

\*\*My Final Recommendation\*\*  
For future modules, make this mandatory:

\- Raw JSON can be custom  
- Impact summary must be standard  
- Activity summary must be standard  
- Registry entry must be standard

That is the cleanest architecture for your master vision.



