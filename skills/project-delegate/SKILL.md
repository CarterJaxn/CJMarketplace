---
name: project-delegate
description: >
  Draft and send a handoff message when a project next step needs to go to someone else. Use this skill when
  Carter says "delegate this to", "hand this off to", "send this to Griffin/Jackson/Whitney", "assign this to",
  "can you message [person] about", "let [person] know they need to", "ask [person] to", or any variation of
  needing another person to take action on a project task. Also trigger when Carter is reviewing his dashboard
  and identifies something someone else should handle. This skill drafts the message in Carter's voice,
  sends it via Slack (with permission), and updates the dashboard to reflect the delegation.
---

# Delegate Project Task

You are helping Carter hand off a project task to someone else. The goal is to make delegation
frictionless — Carter identifies who needs to do what, you draft the message, send it, and update
the dashboard so Carter isn't still carrying it on his plate.

## Step 1 — Identify the Delegation

Figure out:
1. **What task** needs to be delegated? (Map to a specific next step or milestone on the dashboard)
2. **Who** should it go to?
3. **What channel** — Slack DM, a specific channel, or email?

If Carter didn't specify the person or channel, check the project's context for who's involved:
- **Griffin** — Foreclosure pipeline, Salesforce stuff
- **Jackson** — ResaleAI development, code reviews, PRs
- **Whitney** — Operations, finance, QuickBooks, store management
- **Sarah** — Customer support, Freshchat
- **Connor / Mykaela** — Support team

Use the `slack-routing` skill if unsure which channel.

## Step 2 — Draft the Message

Use the `carter-voice` skill to draft the message. It should:

1. Be warm and casual (that's how Carter communicates)
2. Clearly state what's needed
3. Give enough context that the person can act without asking follow-up questions
4. Include any relevant links, file paths, or references
5. Not be pushy — Carter doesn't micromanage

Example format:
```
Hey [Name]! Quick thing — [context in 1 sentence]. 
Could you [specific ask]? [Any helpful detail or link].
No rush, just whenever you get a chance. Thanks!
```

## Step 3 — Confirm and Send

Show Carter the draft:

```
Here's what I'd send to [Person] via [Channel]:

"[drafted message]"

Want me to send this?
```

Wait for confirmation. Then use `slack_send_message` to send it.

## Step 4 — Update the Dashboard

After sending:

1. Read the dashboard HTML and find the relevant project.
2. Update the next step to indicate it's been delegated:
   - Change the step text to include "(delegated to [Person] — [date])"
   - Or remove it from next steps and add a milestone note
3. If the project is now waiting on someone else, consider changing status to "Blocked" with a note.
4. Add a new next step like "Follow up with [Person] on [task] if no response by [date]"
5. Update `updatedAt` and push to the artifact.

## Important Notes

- Always use the carter-voice skill for drafting. Carter's voice is warm, casual, uses "y'all", says "Hey [Name]!", signs off with a smiley.
- If the person to delegate to isn't on Slack (e.g., an external contact), offer to draft an email instead.
- After delegation, Carter should NOT still feel responsible for the task. The dashboard should reflect that it's in someone else's court.
- If Carter delegates the same task to the same person repeatedly, gently note it: "This is the second time we're pinging Griffin about this — want me to follow up more firmly?"
- Keep the message short. Nobody reads long Slack messages.
