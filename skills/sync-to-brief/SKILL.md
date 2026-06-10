---
name: sync-to-brief
description: >
  Pull the top next steps from Carter's project dashboard and inject them into his daily brief as actionable todos.
  Use this skill when Carter says "sync my projects to my brief", "add project todos to my daily brief",
  "put my next steps on today's list", or "what should I work on today". Also trigger automatically after the
  update-dashboard skill runs, or when the daily brief scheduled task runs — this ensures Carter's morning brief
  always includes his most important project actions. If Carter asks "what's on my plate", this skill can also
  surface the answer from his dashboard.
---

# Sync Project Next Steps to Daily Brief

You are pulling the most important next steps from Carter's project dashboard and making sure they show up
in his daily brief. This bridges the gap between "I know what I need to do" and "I actually see it in my
morning routine."

## Step 1 — Read Current Dashboard State

1. Read the dashboard HTML file (`project-dashboard.html` in the outputs directory).
2. Parse the `DEFAULT_PROJECTS` array.
3. Filter to only active projects (status = "In Progress" or "Blocked").
4. Collect all next steps across projects.

## Step 2 — Prioritize

Not all next steps are equal. Rank them by:

1. **Stale projects first** — If a project hasn't been updated in 3+ days, its next step gets priority (this is the thing Carter is avoiding, and seeing it in his brief creates gentle accountability).
2. **Blocked projects** — If something is blocked, the unblocking action should be high priority.
3. **Quick wins** — Steps that can be done in under 10 minutes get a boost (ADHD-friendly: easy wins build momentum).
4. **ResaleAI before side projects** — Work stuff generally takes priority during work hours.

Select the top 3-5 items. Don't overwhelm — Carter's daily brief should feel achievable, not crushing.

## Step 3 — Format for Daily Brief

Format the selected items as a project todos section. The format should match whatever Carter's daily brief
expects. If the daily brief is a scheduled task that generates a summary, add a "Project Todos" section like:

```
## 📋 Project Todos

1. **[Freshchat Stats]** Check if Freshworks support responded to your export request
2. **[Digital Ledger]** Hand the spec to Copilot to build as standalone module  
3. **[Foreclosure Pipeline]** Message Griffin asking for his adjustments file
```

## Step 4 — Deliver

How this gets delivered depends on context:

- **If running inside the daily brief scheduled task:** Add the project todos section to the brief output.
- **If Carter asked directly:** Present the list in the conversation.
- **If running after update-dashboard:** Mention the top 1-2 items as a quick nudge: "By the way, your biggest win today would be [X]."

## Important Notes

- The daily brief scheduled task has session id patterns like "Daily brief" — check recent sessions if needed.
- Don't duplicate items that are already in the daily brief from other sources (calendar, Slack, etc.).
- If ALL projects are stale, lead with empathy not guilt: "Looks like things have been quiet on the project front — want to pick one thing to move forward today?"
- Keep it to 3-5 items max. Carter's ADHD means a shorter, focused list beats a comprehensive one.
