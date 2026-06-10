# GitHub Dashboard Sync

Automatically sync GitHub PR and issue activity to your Cowork project dashboard. No more manually telling Claude what you shipped — it sees your merged PRs and suggests dashboard updates for you to confirm.

## What It Does

- Pulls recent PRs and issues from your GitHub repos via the GitHub MCP
- Matches activity to your tracked dashboard projects using PR titles, labels, and branch names
- Surfaces detected progress as confirmation prompts (never auto-updates)
- Integrates with the existing update-dashboard skill as an additional data source

## Components

| Component | Name | Purpose |
|-----------|------|---------|
| Skill | github-project-sync | Core logic for fetching, matching, and presenting GitHub activity |
| Command | /check-github | Manually check GitHub activity for a project or all projects |
| MCP | GitHub (Copilot) | Connects to GitHub's MCP endpoint for repo/PR/issue access |

## Setup

1. Install the plugin in Cowork
2. When prompted, authenticate with GitHub (OAuth via the GitHub MCP)
3. That's it — the skill will automatically be available when your dashboard updates

## Usage

**Manual check:**
Say "check github" or "what PRs landed this week" to trigger a scan.

**Automatic sync:**
When the update-dashboard skill runs (manually or on schedule), it will pull GitHub data alongside Slack and email.

**Project-specific:**
Say "check github for digital ledger" to see activity for just one project.

## Customizing Project Matching

For best results, add GitHub keywords to your dashboard project entries:

```
Project: Digital Ledger
GitHub keywords: ledger, transaction-history, digital-ledger
Repos: resaleai/main-app
```

If no keywords are set, the plugin matches using the project name.

## Requirements

- GitHub MCP connection (authenticated via OAuth on install)
- A Cowork project dashboard artifact with tracked projects
