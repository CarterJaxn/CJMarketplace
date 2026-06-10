---
name: weekly-retro
description: >
  Generate a weekly retrospective of Carter's project progress — what moved, what didn't, what's been stale,
  and patterns to watch. Use this skill when Carter says "weekly retro", "what moved this week", "project review",
  "how did my projects do", "weekly summary", "end of week review", or "what did I accomplish this week".
  Also designed to run as a scheduled task on Friday afternoons or Monday mornings. This skill helps Carter
  see the big picture and catch projects that are silently falling behind. If Carter asks "am I making progress",
  "what have I been working on", or "where am I spending my time", this skill can answer that too.
---

# Weekly Project Retrospective

You are generating Carter's weekly project retrospective. The goal is pattern recognition — helping Carter
see what's actually getting done vs what's stalling, so he can make conscious choices about where to
spend his energy.

## Step 1 — Gather Data

1. Read the dashboard HTML file to get current project states.
2. Check Cowork session history (list_sessions) for the past 7 days — look for sessions related to tracked projects.
3. Optionally scan Slack and email for project-related activity in the past week.

## Step 2 — Categorize Each Project

For each tracked project, categorize its week:

- **Moved** ✅ — Progress changed, milestones completed, or meaningful work happened
- **Stale** ⚠️ — No activity detected in the past 7 days
- **Blocked** 🔴 — Known blocker preventing progress
- **Completed** 🎉 — Project hit 100% this week

For projects that moved, note specifically what changed (milestones completed, % increase).
For stale projects, note how many days since last activity.

## Step 3 — Identify Patterns

Look for these patterns across Carter's projects:

- **Avoidance pattern:** Is the same project stale every week? Carter might be avoiding it for a reason.
- **Scatter pattern:** Did Carter touch 5 projects but finish 0 milestones? Might need to focus.
- **Momentum pattern:** Did finishing one thing lead to progress on related projects? Celebrate this.
- **Dependency pattern:** Are multiple projects blocked on the same person or thing?

## Step 4 — Generate the Retro

Format the retrospective like this:

```
# 📊 Weekly Project Retro — [Date Range]

## This Week's Wins
- ✅ [Project]: [What moved] (+X% → Y%)
- ✅ [Project]: [Milestone completed]

## Stale Projects  
- ⚠️ [Project]: No activity in [X] days. Last step was: [step]
- ⚠️ [Project]: No activity in [X] days.

## Blocked
- 🔴 [Project]: Waiting on [person/thing]

## The Numbers
- Projects moved: X / Y
- Milestones completed: X
- Average progress across all projects: X%

## Pattern Watch
[1-2 sentences about any patterns noticed. Keep it observational, not judgmental.]

## Suggested Focus for Next Week
Based on what's stale and what has momentum, here's what I'd prioritize:
1. [Project] — [specific action] (this has been stale the longest)
2. [Project] — [specific action] (close to a milestone, push through)
```

## Step 5 — Deliver

Depending on context:

- **If Carter asked:** Show the retro in conversation.
- **If scheduled task:** File the retro to Carter's brain vault using the `file-to-brain` skill under a "retros" section.
- **Always:** Offer to update the dashboard with any corrections discovered during the review.

## Important Notes

- Keep the tone encouraging. Even if everything is stale, find something positive ("You tracked 3 projects this week — that's the first step").
- The "Pattern Watch" section should be honest but kind. "I notice the Freshchat project has been stale for 3 weeks — is this still a priority?" is better than "You haven't touched Freshchat in 3 weeks."
- If Carter's week was productive, celebrate it genuinely. Momentum matters for ADHD.
- If running as a scheduled task and there's nothing meaningful to report, skip the notification. Don't spam.
