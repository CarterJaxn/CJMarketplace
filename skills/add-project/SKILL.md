---
name: add-project
description: >
  Add a new project to Carter's project dashboard artifact. Use this skill whenever Carter says "add a project",
  "new project", "track this project", "start tracking", "put this on my dashboard", "I'm working on something new",
  or describes a new initiative he wants to monitor. Also trigger when Carter mentions starting something and you
  sense it should be tracked — proactively offer to add it. This skill interviews Carter to understand scope,
  generates milestones and next steps, then pushes the project to his live dashboard artifact.
---

# Add Project to Dashboard

You are helping Carter add a new project to his project management dashboard. Carter has ADHD, so your job is to
extract enough detail to build useful milestones and next steps WITHOUT overwhelming him. The interview should feel
like a quick conversation, not a form.

## Step 1 — Core Questions (ask all at once)

Use AskUserQuestion to ask these 3 questions simultaneously:

1. **What is this project?** — One-line description of what you're building/doing.
2. **What does "done" look like?** — How will you know this project is finished?
3. **Category** — Is this a ResaleAI project or a Side Project?

## Step 2 — Follow-up Questions (based on answers)

Based on what Carter said, ask 2-3 targeted follow-ups. Pick from these depending on what's still unclear:

- **What have you already done?** (so we don't list completed work as future milestones)
- **Who else is involved?** (Griffin, Jackson, Whitney, etc. — helps identify delegation opportunities)
- **What's the first thing you need to do?** (this becomes the immediate next step)
- **Any deadline or target date?**
- **What's blocking you right now, if anything?**

Don't ask all of these — just the ones that matter based on the project type. If Carter already gave enough detail in step 1, you might only need 1 follow-up.

## Step 3 — Generate Milestones and Next Steps

Based on the interview, create:

- **5-7 milestones** — sequential phases of the project. Mark completed ones with `done: true`, the current one with `active: true`, and future ones with both `false`. Milestones should be concrete and verifiable (not "make progress on X").
- **2-3 next steps** — specific, actionable items Carter can do RIGHT NOW. These should be small enough to start in under 5 minutes. Think ADHD-friendly: not "build the feature" but "open the repo and create the feature branch."
- **Progress %** — estimate based on how many milestones are done vs total.
- **Status** — "Not Started", "In Progress", "Blocked", or "Done" based on what Carter said.

## Step 4 — Show Carter and Confirm

Present the project card to Carter in a clear format:

```
📋 [Project Name]
Category: ResaleAI / Side Project
Status: [status] | Progress: [X]%

Milestones:
✅ Done milestone
🔹 Active milestone  
⚪ Future milestone

Next Steps:
→ Step 1
→ Step 2
→ Step 3
```

Ask: "Does this look right? Want to change anything before I add it to the dashboard?"

## Step 5 — Update the Dashboard

Once confirmed:

1. Read the current dashboard HTML file. The dashboard artifact has id `project-dashboard`. Read the HTML file from Carter's outputs directory — look for `project-dashboard.html`.

2. Find the `const DEFAULT_PROJECTS = [...]` array in the HTML.

3. Add the new project object to the array. Format:
```json
{
  "id": "kebab-case-name",
  "name": "Project Name",
  "category": "resaleai" or "side",
  "status": "In Progress",
  "progress": 25,
  "milestones": [
    { "text": "Milestone text", "done": true, "active": false },
    { "text": "Active milestone", "done": false, "active": true },
    { "text": "Future milestone", "done": false, "active": false }
  ],
  "nextSteps": [
    "First actionable step",
    "Second actionable step"
  ],
  "updatedAt": "<current ISO timestamp>"
}
```

4. Write the updated HTML file back.

5. Call `mcp__cowork__update_artifact` with id `project-dashboard` and the updated HTML path.

6. Confirm to Carter: "Added [Project Name] to your dashboard! Your daily focus will include it next time you open it."

## Important Notes

- Always generate an `id` in kebab-case from the project name (e.g., "Digital Cash Ledger" → "digital-cash-ledger")
- The `updatedAt` field should be the current ISO timestamp
- If Carter is describing something from a previous conversation, check Cowork sessions for additional context before asking questions he may have already answered
- Keep the interview fast — Carter will disengage if it feels like bureaucracy
