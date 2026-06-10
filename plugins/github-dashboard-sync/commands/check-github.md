---
description: Check recent GitHub activity for your tracked projects
argument-hint: [project-name or "all"]
---

Check recent GitHub activity and match it to the user's tracked dashboard projects.

If an argument is provided (`$ARGUMENTS`), filter to just that project. If no argument or "all", check all tracked projects.

Steps:

1. Read the user's current project dashboard artifact to get tracked project names and any configured GitHub keywords.

2. Use the GitHub MCP tools to search for:
   - PRs merged in the last 7 days
   - PRs currently open and in review
   - Issues closed in the last 7 days

   Search using the project name, configured keywords, and known label patterns.

3. Match results to projects using the github-project-sync skill's matching logic (label match > title match > branch match).

4. Present a concise summary grouped by project:
   - What merged (with links)
   - What's in review
   - What issues closed
   - Suggested dashboard updates (with confidence level)

5. Ask the user if they want to apply the suggested updates to their dashboard.

Keep the output scannable. Use short descriptions, not full PR bodies.
