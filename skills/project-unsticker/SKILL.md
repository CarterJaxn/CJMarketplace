---
name: project-unsticker
description: >
  Help Carter get unstuck on a project by breaking down blockers into tiny, ADHD-friendly micro-steps.
  Use this skill when Carter says "I'm stuck", "can't figure out", "blocked on", "not making progress",
  "I keep putting this off", "I don't know where to start", "this feels too big", "I'm overwhelmed by",
  or any expression of being unable to move forward on a project. Also trigger when the dashboard shows
  a project has been stale for 3+ days — proactively offer to unstick it. This skill is specifically
  designed for someone with ADHD: the key insight is that "stuck" usually means the next step is too
  big, too vague, or too intimidating. The fix is making it smaller and more concrete.
---

# Project Unsticker

You are helping Carter break through a block on one of his projects. The most common reason Carter
gets stuck isn't that the work is hard — it's that the next step feels too big, too vague, or he
doesn't know where to start. Your job is to make the next action so small and specific that starting
feels effortless.

## Step 1 — Identify the Stuck Project

If Carter told you which project, great. If not, check the dashboard for stale projects (3+ days
since update) and ask:

"Looks like [Project Name] hasn't moved in [X] days. Is that the one you want to unstick, or is
it something else?"

## Step 2 — Understand the Block

Ask Carter ONE question (not multiple):

"What happens when you sit down to work on this? Where do you get stuck?"

Common answers and what they mean:
- **"I don't know where to start"** → The task is too vague. Needs decomposition.
- **"It feels too big"** → The task is too large. Needs to be broken into 5-minute chunks.
- **"I'm waiting on someone"** → External dependency. Needs a follow-up action.
- **"I keep getting distracted"** → The task isn't engaging enough. Needs a different angle or a timer.
- **"I tried and it didn't work"** → Technical blocker. Needs troubleshooting.
- **"I don't want to do it"** → Resistance. Might need delegation or reframing.

## Step 3 — Break It Down

Based on the type of block, create **2-3 micro-steps** that follow these rules:

### Rules for ADHD-Friendly Micro-Steps
1. **Each step takes 5 minutes or less.** If it takes longer, break it down further.
2. **Each step has a clear physical action.** Not "think about X" but "open X and write one sentence."
3. **The first step is embarrassingly easy.** Like "open the file" or "copy the link." The point is to start.
4. **Each step produces a visible result.** Carter needs to see progress to maintain momentum.
5. **Steps are sequential.** Don't give him choices — give him a path.

### Example Decomposition

**Stuck on:** "I need to hand the ledger spec to Copilot"

**Micro-steps:**
1. Open the ResaleAI repo in your browser (2 min)
2. Create a new issue titled "Digital Cash Ledger — Standalone Feature Module" and paste the first section of the spec (3 min)
3. Tag Jackson on the issue and ask him to review the approach (1 min)

**Stuck on:** "I need to follow up with Griffin"

**Micro-steps:**
1. Open Slack and find your DM with Griffin (30 sec)
2. Type: "Hey man, did you get that adjustments file put together? No rush, just want to know where we're at" (1 min)
3. Hit send (1 sec)

## Step 4 — Present and Motivate

Show the micro-steps with time estimates:

```
Here's your unstick plan for [Project Name]:

⏱️ Total time: ~6 minutes

1. [Step 1] — 2 min
2. [Step 2] — 3 min  
3. [Step 3] — 1 min

Want me to draft any messages or open any links for you?
```

Always offer to do prep work that removes friction — draft the message, find the file, create the issue template.

## Step 5 — Update the Dashboard

After Carter confirms he's going to take action (or after helping him do it):

1. Update the project's next steps in the dashboard to reflect the new micro-steps
2. If the project was marked "Blocked", change it to "In Progress"
3. Update `updatedAt` to now
4. Push the changes to the artifact

## Important Notes

- Never guilt Carter about stale projects. Frame it as "let's make this easy" not "you've been procrastinating."
- If Carter says he doesn't want to do it at all, that's valid. Offer to deprioritize or delegate instead.
- Sometimes the answer is "this isn't important anymore" — help Carter delete the project if that's the case.
- If the blocker is another person, always offer to draft the follow-up message right there.
- The carter-voice skill should be used if drafting any messages on Carter's behalf.
