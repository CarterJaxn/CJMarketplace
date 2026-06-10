---
name: update-project-dashboard
description: Scan Slack, email, and Cowork sessions for project updates and refresh Carter's project dashboard every 4 hours
---

You are running Carter Miller's project dashboard update. Your job is to scan his connected tools for recent activity related to his tracked projects and update the dashboard artifact.

## What to do

1. **Read the dashboard HTML file.** Look for `project-dashboard.html` in the outputs directory. Parse the `DEFAULT_PROJECTS` JavaScript array to get the current list of tracked projects.

2. **For each active project (status != "Done"), search for recent activity:**

   - **Slack:** Use `slack_search_public_and_private` to search for messages mentioning each project name or related keywords from the last 4-6 hours. Check #customer_success, #dev, and relevant DMs.
   - **Email:** Use `search_threads` to find email threads related to each project.
   - **Cowork Sessions:** Use `list_sessions` and `read_transcript` to check recent sessions whose titles reference tracked projects.

3. **For each project, assess:**
   - Should any milestones be marked done? (Look for evidence work was completed)
   - Should progress % change? (Recalculate based on milestones: done/total * 100)
   - Should next steps change? (Remove completed ones, add new ones discovered)
   - Should status change? (Blocked if blocker found, In Progress if work resumed)

4. **Apply staleness color rules based on time since last progress (`updatedAt`):**
   - **Default (no special color)** — last progress within 24 hours, project is active
   - **Orange** — no movement for 24+ hours. Set a visual indicator (e.g., orange border or background on the project card)
   - **Red** — no movement for 2+ days (48+ hours). Set a red visual indicator on the project card
   - These colors should be encoded in the project data so the dashboard HTML renders them visually

5. **Update the dashboard:**
   - Modify the `DEFAULT_PROJECTS` array in the HTML with any changes
   - Set `updatedAt` to the current ISO timestamp for any project that changed
   - Add a `stalenessColor` field to each project: `null` (active), `"orange"` (24h+), or `"red"` (48h+)
   - Write the updated HTML file
   - Call `mcp__cowork__update_artifact` with id `project-dashboard` and the updated HTML path

6. **If anything meaningful changed or a project has been stale 3+ days**, leave a brief note. Don't spam — only flag important changes.

## Current tracked projects
- **Automated Foreclosure Pipeline** (side project) — Building Griffin's pre-foreclosure lead enrichment pipeline
- **Digital Cash Ledger** (ResaleAI) — Replacing paper cash ledger with digital feature in ResaleAI app
- **Freshchat Statistics Import** (ResaleAI) — Daily export of Freshchat conversations to Google Drive with visual statistics
- **CounterPoint AI Dashboard** (side project) — AI-native project management dashboard for John (political campaigns, via Mary/Obvious Consulting). Multi-session build. Current milestone: discovery meeting with John, then Granola ingest, Claude walkthrough, daily brief, then dashboard build.

## Important
- This runs automatically every 4 hours. Apply changes without asking for confirmation.
- Don't change things unless you have evidence. "No updates found" is a valid outcome.
- Always update the `updatedAt` timestamp for any project you modify.
- Carter has ADHD — if you surface next steps, make them specific and actionable, not vague.
- The staleness color system is critical — it creates visual urgency so stale projects can't hide.