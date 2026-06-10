# Carter's Skills & Plugins

Personal marketplace of Claude Code skills and plugins built by [Carter Miller](https://github.com/CarterJaxn).

These are battle-tested automations I use daily for customer support ops, project management, bookkeeping, and AI development at ResaleAI.

---

## Skills

| Skill | Description |
|-------|-------------|
| [add-project](skills/add-project/) | Add a new project to a dashboard artifact |
| [consolidate-memory](skills/consolidate-memory/) | Reflective pass over memory files — merge duplicates, fix stale facts, prune the index |
| [dropbox-bank-statements](skills/dropbox-bank-statements/) | Access and parse bank statement PDFs from Dropbox for financial analysis |
| [file-to-brain](skills/file-to-brain/) | File content into an Obsidian second brain vault |
| [freshchat](skills/freshchat/) | Query Freshchat to look up customer conversations and track support issues |
| [freshchat-autoreply](skills/freshchat-autoreply/) | The livechat bot's brain — auto-reply engine for Freshchat |
| [freshchat-learn](skills/freshchat-learn/) | Feedback loop for the Freshchat bot |
| [freshchat-mine](skills/freshchat-mine/) | Mine Freshchat conversation history to build a support bot knowledge base |
| [freshchat-replay](skills/freshchat-replay/) | Evaluation harness for the Freshchat bot |
| [freshworks-agent-audit](skills/freshworks-agent-audit/) | Audit Freshworks agent assignment data against actual conversation records |
| [grill-me](skills/grill-me/) | Interview relentlessly about a project idea before diving into implementation |
| [hand-off-task](skills/hand-off-task/) | Delegate a task to Claude Code for execution outside a sandbox |
| [level-up-session](skills/level-up-session/) | Generate leadership program session PDFs with brand-matched layout |
| [milestone-done](skills/milestone-done/) | Update a project dashboard when a milestone or task is completed |
| [project-delegate](skills/project-delegate/) | Draft and send a handoff message when a project step needs to go to someone else |
| [project-unsticker](skills/project-unsticker/) | Break down blockers into tiny, ADHD-friendly micro-steps |
| [qbo-categorize](skills/qbo-categorize/) | Categorize QuickBooks bank-feed transactions using a trained knowledge base |
| [slack-cs-message](skills/slack-cs-message/) | Send a Slack message to a customer success channel |
| [sync-to-brief](skills/sync-to-brief/) | Pull top next steps from a project dashboard into a daily brief |
| [update-dashboard](skills/update-dashboard/) | Scan Slack, email, and sessions for project activity and refresh a dashboard |
| [weekly-retro](skills/weekly-retro/) | Generate a weekly retrospective of project progress and patterns |

## Plugins

Full plugins with skills, commands, and optional MCP servers.

| Plugin | Description |
|--------|-------------|
| [github-dashboard-sync](plugins/github-dashboard-sync/) | Sync GitHub PR and issue activity to a project dashboard |

## Scheduled

Skills designed to run on a cron schedule.

| Skill | Description |
|-------|-------------|
| [daily-brain-ingest](scheduled/daily-brain-ingest/) | Daily ingestion of meetings, Slack, Linear, Gmail, calendar, and sessions into a second brain |
| [daily-brief](scheduled/daily-brief/) | Summarize calendar and unread Slack messages each morning |
| [update-project-dashboard](scheduled/update-project-dashboard/) | Scan for project updates and refresh a dashboard every 4 hours |

---

## Installation

Each skill is a self-contained directory with a `SKILL.md` file. To use one:

1. Copy the skill directory to `~/.claude/skills/<skill-name>/`
2. The skill will be available in your next Claude Code session

For plugins, copy the plugin directory to your plugins location and ensure the `.claude-plugin/plugin.json` manifest is present.
