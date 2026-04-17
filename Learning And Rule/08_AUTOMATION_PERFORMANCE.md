# ⚡ 08 — Automation & Performance Rules v1.1
**When to apply:** When building automated workflows, scheduled tasks, or optimizing performance

---

## Rule 1: Automate Repetitive Work
- Identify repetitive workflows and automate them
- Schedule automated runs at appropriate intervals
- Reduce manual effort wherever possible

## Rule 2: Self-Improving Automation
After each automation run:
- Record what worked ✅
- Record what failed ❌
- Update workflow to only use proven steps next time
- This ensures: faster execution, better performance, future-proof workflows

## Rule 3: Timer & Auto-Run System
- Add auto-run timer feature (minutes, hours intervals)
- Timer should survive system restarts
- Implement Smart Resume: automatically resume scheduled tasks after restart
- Maintain last execution state

## Rule 4: Parallel vs Sequential Execution
- Offer both modes:
  - **Parallel** — save time, run same-type tasks simultaneously
  - **Sequential** — reduce system load, run one at a time
- Let user or situation decide which mode

## Rule 5: Continuous Improvement Workflow
- Even if a workflow works today, platforms can change anytime
- If any step fails: try alternative approaches, don't stop at failure
- After each run: record successes and failures
- Continuously update the process for better results

## Rule 6: Self-Improving Record System
- Track what worked and what failed in local files
- Files like: `execution_record.txt` or `success_fail_log.txt`
- Next time: use last successful code/logic as default
- Avoid repeating failed approaches

## Rule 7: Performance Optimization
- Minimize unnecessary operations
- Cache results where applicable
- Batch operations when possible
- Monitor resource usage

## Rule 8: Smart Failure Counter & Auto-Update Logic
When automation uses a fallback method, apply this decision system:

| Scenario | What Happens | Action |
|----------|-------------|--------|
| **One-time glitch** | Step fails → fallback used → next run works fine | Log only, NO skill/workflow change |
| **Recurring failure** | Same step fails multiple times in same situation | Promote fallback to primary, add changelog, notify in summary |
| **Recovery** | Step works normally again | Clear its failure flag |

**Rules:**
- Failed 1 time → monitor only, no change
- Failed multiple times in same situation → auto-update: fallback becomes primary
- If fallback also fails → think 360° deeply, list all possible solutions, choose best for long-term
- If step works normally this run → clear its flag from failure log
- User always sees what changed in run summary

**Goal:** One-time glitch = logged but unchanged ✅ | Recurring failure = auto-updated ✅ | Recovery = flag clears naturally ✅

---
*Category: Automation & Performance | Source: Msir's Universal Rulebook | Updated: 12 April 2026*
