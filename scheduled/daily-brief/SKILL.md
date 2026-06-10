---
name: daily-brief
description: Summarize my calendar and any unread slack messages
---

Check my Google Calendar for events/meetings, and check Slack for any unread messages and summarize them here.

## Project Staleness Escalation (CRITICAL)

After summarizing calendar and Slack, check the project dashboard for stale projects:

1. Read the project dashboard HTML file from the outputs directory. Parse the `DEFAULT_PROJECTS` array.
2. For each active project, calculate the number of days since `updatedAt`.
3. **If any project has gone 3+ days without progress**, add a section to the brief called **"Stalled Projects"** with the following formatting:
   - Each stalled project name and the exact number of days since last progress
   - This section MUST be rendered in **bright red font** (use bold + emphasis or HTML if supported)
   - Example: "**🔴 Automated Foreclosure Pipeline — NO PROGRESS IN 5 DAYS**"
   - This should be impossible to miss — it goes at the TOP of the brief, before calendar and Slack

4. Also run the sync-to-brief skill to pull the top next steps from the project dashboard into the brief as actionable todos.

The point of the staleness callout is that Carter has ADHD and projects can silently die if nobody flags them. Bright red, exact day count, front and center.