---
name: github-project-sync
description: >
  Sync GitHub activity to the project dashboard. Use this skill when the user says
  "sync github", "check github progress", "update dashboard from github",
  "what PRs landed", "what moved on github", "github sync", "pull github activity",
  "check my PRs", or "what shipped this week". Also use when the update-dashboard
  skill runs, to pull GitHub as an additional data source. Trigger whenever the user
  asks about engineering progress on a tracked project and GitHub is the source of truth.
version: 0.1.0
---

# GitHub Project Sync

Pull recent GitHub activity (PRs, issues) and match it to tracked dashboard projects. Surface detected progress as confirmation prompts so the user can approve before the dashboard updates.

## How It Works

1. Fetch recent PRs and issues from the user's GitHub repos
2. Match each item to a tracked dashboard project using title keywords and labels
3. Present matched items as pending progress updates
4. Wait for user confirmation before updating the dashboard

## Step-by-Step Process

### 1. Get the user's tracked projects

Read the current project dashboard artifact to get the list of active projects and their names/keywords. Each project name becomes a search term for matching GitHub activity.

### 2. Fetch recent GitHub activity

Use the GitHub MCP tools to pull recent data. Focus on:

- **Merged PRs** from the last 7 days (primary progress signal)
- **Open PRs** that are in review or recently updated
- **Closed issues** tied to project keywords

Query strategy — for each tracked project, search PRs and issues using the project name and any known keywords or labels. For example, if the project is "Digital Ledger", search for PRs with "ledger" in the title or with a "digital-ledger" label.

### 3. Match activity to projects

Match GitHub items to dashboard projects using these signals (in priority order):

1. **Label match** — PR/issue has a label that matches or contains the project name
2. **Title keyword match** — PR/issue title contains words from the project name
3. **Branch name match** — PR branch name contains the project slug (e.g., `feature/digital-ledger-*`)

When matching, normalize strings: lowercase, strip hyphens/underscores, compare word stems. A PR titled "Add transaction history endpoint for ledger" matches project "Digital Ledger" because it contains "ledger."

If a PR could match multiple projects, pick the strongest match (label > title > branch). If truly ambiguous, include it under both projects and let the user clarify.

### 4. Present progress for confirmation

Group matched items by project and present them as a confirmation prompt. Format:

```
## GitHub Activity → Dashboard Updates

### Digital Ledger
Found 2 merged PRs this week:
- "Add transaction history endpoint" (merged May 25)
- "Ledger UI table component" (merged May 26)

→ Suggested update: Mark "Build transaction history API" milestone as complete?

### [Other Project]
Found 1 merged PR:
- "Fix auth token refresh" (merged May 24)

→ Suggested update: Move "Auth hardening" to 75% complete?
```

Always ask for confirmation. Never auto-update the dashboard.

### 5. Update the dashboard

After the user confirms (or adjusts), update the project dashboard artifact with:
- New milestone completions
- Progress percentage changes
- A note like "Updated from GitHub: 2 PRs merged" in the activity log

## Matching Heuristics

### What counts as progress

- **Merged PR** → strongest signal. A merged PR almost always means forward progress.
- **PR in review** → work is happening but not done. Mention it but don't update milestones.
- **Closed issue** → depends on context. A closed bug might mean a fix shipped.
- **Open PR with recent commits** → active work. Note it but don't count as done.

### What doesn't count

- Draft PRs with no activity
- PRs that were closed without merging (abandoned)
- Bot-generated PRs (dependabot, renovate) unless the user tracks dependency updates

### Confidence levels

- **High confidence**: Label matches a project exactly, or PR title contains 2+ project keywords
- **Medium confidence**: PR title contains 1 project keyword, or branch name matches
- **Low confidence**: Tangential keyword match. Flag these separately as "might be related."

Only auto-suggest dashboard updates for high and medium confidence matches. Show low confidence matches in a separate "possibly related" section.

## Integration with update-dashboard

When the update-dashboard skill runs, it should invoke this skill as one of its data sources. The flow:

1. update-dashboard starts its scan (Slack, email, Cowork sessions)
2. update-dashboard calls github-project-sync to get GitHub activity
3. GitHub results are merged with other data sources
4. Combined progress is presented to the user for confirmation

## Configuration

The user can customize matching by adding keywords to their project entries in the dashboard. For example, a project entry might include:

```
Project: Digital Ledger
GitHub keywords: ledger, transaction-history, digital-ledger
Repos: resaleai/main-app
```

If no keywords are specified, fall back to the project name itself.

## Additional Resources

See `references/github-mcp-tools.md` for details on available GitHub MCP tool calls.
