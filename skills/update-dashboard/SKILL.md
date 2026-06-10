---
name: update-dashboard
description: >
  Scan Carter's Slack, email, and Cowork sessions for recent activity related to his tracked projects, then update
  the project dashboard artifact with new progress, milestones, and next steps. Use this skill when Carter says
  "update my dashboard", "refresh my projects", "what's the latest on my projects", "check project status",
  or "sync my dashboard". Also designed to run as a scheduled task every 4 hours to keep the dashboard fresh
  automatically. If you notice Carter discussing project-related work in conversation, proactively offer to
  update the dashboard afterward.
---

# Update Project Dashboard

You are scanning Carter's connected tools for recent project activity and updating his dashboard accordingly.

## Step 1 — Load Current Projects

1. Read the dashboard HTML file (`project-dashboard.html` in the outputs directory).
2. Parse the `DEFAULT_PROJECTS` array to get the current list of tracked projects.
3. Note each project's name, current progress, active milestone, and last `updatedAt` timestamp.

## Step 2 — Scan for Updates

For each active project (status != "Done"), search for recent activity across these sources. Only search sources that are connected/available:

### Slack (if available)
Search Slack for messages mentioning the project name or related keywords from the last 24-48 hours:
- Use `slack_search_public_and_private` with project-related terms
- Check relevant channels (#customer_success, #dev, DMs with Griffin/Jackson/Whitney)
- Look for: decisions made, blockers raised, progress reported, tasks completed

### Email (if available)
Search Gmail for threads related to each project:
- Use `search_threads` with project keywords
- Look for: responses from external parties (Freshworks support, etc.), action items, deadlines

### Cowork Sessions
Use `list_sessions` and `read_transcript` to check recent Cowork sessions:
- Look for sessions whose titles reference the project
- Check for work completed, decisions made, files created

### Current Conversation
Check the current conversation history — Carter may have mentioned progress on something during this chat.

## Step 3 — Assess Changes

For each project, determine:

1. **Should any milestones be marked done?** — Look for evidence that work was completed.
2. **Should the active milestone change?** — If the current active milestone is done, advance to the next one.
3. **Should progress % change?** — Recalculate based on milestones completed vs total. Use this formula as a baseline: `(done_milestones / total_milestones) * 100`, but adjust if some milestones are clearly larger than others.
4. **Should next steps change?** — Remove steps that were completed, add new ones based on what was discovered.
5. **Should status change?** — If a blocker was found, set to "Blocked". If work resumed, set to "In Progress". If everything is done, set to "Done".
6. **Is the project stale?** — If no activity was found and it's been 3+ days, flag it but don't change progress.

## Step 4 — Present Changes to Carter

Show a summary of what changed (or didn't):

```
📊 Dashboard Update Summary

✅ Digital Cash Ledger — No changes (last activity: 2 days ago)
🔄 Freshchat Statistics Import — Progress: 20% → 25%
   • Marked "Draft email to Freshworks" as done (found reply in Gmail)
   • New next step: "Review Freshworks export file"
⚠️ Foreclosure Pipeline — STALE (5 days, no activity)
   • No changes made — want me to break down the blocker?
```

Ask Carter: "These updates look right? I'll push them to the dashboard."

## Step 5 — Update the Dashboard

Once confirmed (or if running as a scheduled task, apply automatically):

1. Update each project's data in the `DEFAULT_PROJECTS` array
2. Set `updatedAt` to the current ISO timestamp for any project that changed
3. Write the updated HTML file
4. Call `mcp__cowork__update_artifact` with id `project-dashboard`

## Step 6 — Follow-up Actions

After updating, check if any of these should happen:
- **Stale projects (3+ days):** Offer to run the `project-unsticker` skill
- **Completed milestones:** Celebrate briefly ("Nice — you knocked out the Freshworks email!")
- **New blockers found:** Offer to help resolve them
- **Projects near completion (>80%):** Call out what's left to finish

## Scheduled Task Mode

When running as a scheduled task (every 4 hours), skip the confirmation step and apply changes automatically.
After updating, if there are stale projects or important changes, send Carter a brief Slack DM or leave a note
in the dashboard's daily focus section. Don't spam him — only notify if something meaningful changed or if a
project has been stale for 3+ days.
