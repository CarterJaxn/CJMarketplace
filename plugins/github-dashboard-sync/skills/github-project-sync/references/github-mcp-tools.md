# GitHub MCP Tools Reference

The GitHub MCP server (via `https://api.githubcopilot.com/mcp/`) provides tools for interacting with GitHub repositories. When these tools are available, use them to query PR and issue data.

## Common Tool Patterns

### Searching for PRs

Search for pull requests by keywords, labels, or state. Typical parameters:
- `repo` or `owner/repo` — the repository to search
- `state` — "open", "closed", "merged", or "all"
- `labels` — filter by label names
- `sort` — "created", "updated", "popularity"
- `direction` — "asc" or "desc"
- `since` — ISO date to filter by last update

### Searching for Issues

Similar to PRs but for issues. Filter by:
- `state` — "open" or "closed"
- `labels` — filter by label names
- `assignee` — filter by assigned user
- `since` — ISO date

### Getting PR Details

Fetch a specific PR to see:
- Title, body, labels, branch names
- Merge status and merge date
- Files changed (useful for understanding scope)
- Review status

## Usage Tips

- Always check what tools are actually available from the GitHub MCP before calling them. Tool names and parameters may vary.
- When searching, use broad queries first, then filter in post-processing. It's better to get too many results and filter than to miss relevant PRs.
- Cache results within a session to avoid redundant API calls.
- Respect rate limits — batch queries where possible.

## Fallback

If the GitHub MCP tools are not connected or unavailable, inform the user and suggest they:
1. Connect the GitHub MCP via plugin settings
2. Or manually share PR links for the sync
