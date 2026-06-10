---
name: hand-off-task
description: >
  Delegate a task to Claude Code for execution outside the Cowork sandbox — on the user's
  real filesystem with full git, shell, and toolchain access. Use this skill whenever the
  user needs work done that Cowork can't handle: code changes, PRs, refactors, running
  tests, deploying, scripts that touch local files, or anything requiring real shell access.
  Trigger phrases include "delegate this to Claude Code", "hand this off", "I need this
  done in my repo", "can you make a PR for this", "run this outside the sandbox",
  "do this in Claude Code", or any task where the user clearly needs filesystem/git access
  that Cowork doesn't have. Also trigger when the user describes a coding task and you
  realize mid-conversation that it requires access you don't have.
---

# Delegate to Claude Code

You're creating a task brief that a separate Claude Code session will pick up and execute
on the user's actual machine — with full filesystem, git, shell, and toolchain access.
Your job is to be the "project manager": gather all relevant context, write a clear and
comprehensive brief, and hand it off so Claude Code can hit the ground running without
needing to ask follow-up questions.

## Why this exists

Cowork runs in an isolated sandbox. It's great for research, drafting, and working with
connected tools (Slack, Freshchat, Grafana, etc.), but it can't touch the user's repos,
run their test suite, or make commits. This skill bridges that gap: you do the context
gathering and planning here, then hand off a ready-to-execute task brief.

## Workflow

### Step 1: Understand the task

Ask the user what they need done. Get clarity on:

- **What**: The specific outcome (e.g., "fix the auth bug", "add a new API endpoint")
- **Where**: Which repo or directory to work in
- **Acceptance criteria**: How will they know it's done? Tests passing? PR opened?
- **Constraints**: Anything Claude Code should know — branch conventions, style guides,
  don't-touch zones, etc.

If the user already described the task in conversation, extract these from context rather
than re-asking.

### Step 2: Gather context from connected tools

This is where Cowork earns its keep. Before writing the brief, proactively pull relevant
context from whatever tools are connected. Think about what a developer would want to
know before starting the task:

- **Slack**: Search for relevant threads — design decisions, prior discussion of the
  feature/bug, deployment notes. Use `slack_search_public_and_private` with good keywords.
- **Freshchat**: If this relates to a customer-reported issue, pull the conversation to
  understand the exact symptoms and repro steps.
- **Grafana**: If the task involves a production error or performance issue, pull logs and
  metrics to include error messages, stack traces, and timing data.
- **Granola**: Search meeting transcripts for relevant discussions or decisions.
- **Google Drive**: Check for relevant design docs, specs, or RFCs.
- **Gmail**: Check for relevant email threads (e.g., external vendor requirements).

Don't pull from every tool blindly — use judgment about what's relevant. A simple refactor
doesn't need Freshchat history. A customer-facing bug fix probably does.

Summarize what you found and present it to the user before including it in the brief.
They may want to add, remove, or correct things.

### Step 3: Write the task brief

Create a markdown file that gives Claude Code everything it needs. The brief should be
self-contained — Claude Code won't have access to your conversation history or connected
tools.

Structure the brief like this:

```markdown
# Task: [Clear, actionable title]

## Objective
[1-2 sentence summary of what needs to be done]

## Working Directory
[Path to the repo or directory, e.g., ~/code/resaleai-api]

## Context
[Background information gathered from connected tools and conversation.
Include Slack discussion summaries, Freshchat customer reports, Grafana
error logs, design doc excerpts — whatever Claude Code needs to
understand the WHY behind the task.]

## Requirements
[Specific, numbered list of what the output should include]

## Acceptance Criteria
[How to verify the task is complete — tests to run, behavior to check]

## Constraints
- [Branch to work from, e.g., "branch off main"]
- [Style/convention notes]
- [Files or areas to avoid touching]
- [Any other guardrails]

## Additional Notes
[Anything else relevant — links, related PRs, known gotchas]
```

### Step 4: Create the handoff files

Write exactly one file — no READMEs, no shell scripts, no summaries, no extras.

**`task-[descriptive-slug].md`** — The full task brief from Step 3.

Write this file to `~/cowork-tasks/` — this is the relay watch folder. If the user
has the `cowork-relay.sh` daemon running, it will automatically pick up the task file
and run it with Claude Code in the correct working directory.

Create the directory if it doesn't exist (use bash: `mkdir -p ~/cowork-tasks`).

### Step 5: Present to the user

Show the user:
1. A summary of the task brief (don't dump the whole thing — they can read the file)
2. Let them know the task file was dropped into `~/cowork-tasks/`
3. If the relay daemon is running, it'll be picked up automatically
4. If not, they can run it manually: `cd [working-dir] && claude < ~/cowork-tasks/task-[slug].md`

Also provide a computer:// file link so they can review the full brief.

## Tips for writing great task briefs

- **Be specific about file paths.** "Fix the auth middleware" is vague. "Fix the JWT
  validation in `src/middleware/auth.ts` that's returning 401 for valid tokens" gives
  Claude Code a clear starting point.

- **Include error messages verbatim.** If there's a stack trace or error log from
  Grafana/Freshchat, paste it in. Don't paraphrase errors.

- **Quote relevant Slack context.** Don't just say "the team discussed this."
  Include the key quotes so Claude Code has the actual information.

- **Set scope boundaries.** If this is a targeted fix, say "only modify files in
  `src/auth/`" so Claude Code doesn't go on a refactoring adventure.

- **Mention the test strategy.** "Run `npm test -- --grep auth` to verify" is much
  better than "make sure tests pass."

## Edge cases

- **User doesn't know the repo path**: Ask them. If they're unsure, suggest they run
  `pwd` in their project directory and come back with the path.

- **Task is vague**: Push back gently and ask clarifying questions. A vague brief will
  lead to a vague result. Better to spend an extra minute here than waste a Claude Code
  session.

- **Multiple repos involved**: Create separate task briefs for each repo. Don't try to
  cram a cross-repo change into one brief.

- **User wants to iterate**: The brief is just a markdown file — they can edit it before
  running. Encourage them to tweak it if something's not quite right.
