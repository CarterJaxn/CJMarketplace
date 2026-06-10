---
name: freshworks-agent-audit
description: >
  Audit Freshworks livechat agent assignment data by comparing a spreadsheet export against
  actual conversation records in the Freshworks inbox. Use this skill whenever the user wants
  to verify agent assignment accuracy, check if livechat analytics are capturing agent data
  correctly, audit the "Assigned Agent name" field in a Freshworks export, or investigate
  gaps between who actually handled chats and what the reporting system recorded. Also use
  when the user mentions checking conversation IDs against Freshworks, verifying livechat
  data, or auditing support chat assignments.
---

# Freshworks agent assignment audit

This skill walks through a complete audit of Freshworks livechat agent assignment data. The core problem it solves: Freshworks exports often show empty "Assigned Agent name" fields even though agents actively responded to and resolved those conversations. This skill helps you prove that gap with data.

## Why this matters

Without accurate agent assignment data, teams can't track workload distribution, measure agent performance, or hold anyone accountable for response quality. The export may show zero assignments while agents are handling hundreds of chats. This skill produces a verified, presentation-ready report showing exactly how big the gap is.

## Overview of the workflow

The audit has five phases:

1. **Get the spreadsheet** — find and parse the Freshworks export from Google Drive
2. **Analyze the data** — identify which columns are empty, count conversations per agent, and quantify the gap
3. **Sample conversations** — pick a proportional random sample across all agents (aim for 40+)
4. **Verify in Freshworks** — navigate to each conversation in Chrome and confirm agent activity vs. assignment status
5. **Generate the report** — build a visual dashboard showing the gap with verification results

## Phase 1: Get the spreadsheet

The user will either provide a Google Sheet name, a file ID, or upload a CSV directly.

**If it's a Google Sheet**, use the Google Drive connector to search for and download the file:
- Search by name using `search_files`
- Download the content using `download_file_content` or `read_file_content`
- The content typically comes back as base64-encoded CSV — decode it with Python

**If it's an uploaded CSV**, read it directly from the uploads directory.

Parse the CSV with Python's `csv.DictReader`. The key columns to look for in a Freshworks agent response export are:
- `First response by` — who first replied to the customer
- `Resolution action performed by` — who resolved/closed the conversation
- `Assigned Agent name` — the field we're auditing (likely empty)
- `Conversation id` — the unique ID for each chat
- `Agent Name` — may also be empty
- `Group Assigned At` — may also be empty

**Watch out for scientific notation.** Google Sheets sometimes corrupts long numeric conversation IDs (like `1.07571E+15`). Count how many IDs are affected. You can still work with the non-corrupted ones — there should be plenty for sampling.

## Phase 2: Analyze the data

Run a Python script to extract these metrics:
- Total rows and unique conversation IDs (rows may exceed unique conversations since one chat can have multiple agent interactions)
- For each potentially-empty column (`Agent Name`, `Group Assigned At`, `Assigned Agent name`), count how many rows have non-empty values
- For `First response by`, count responses per agent and deduplicate by conversation ID to get unique conversations per agent
- Same for `Resolution action performed by`

This gives you the "what the system recorded" side of the story. If `Assigned Agent name` is 0% populated but `First response by` shows active agents, you've found the gap.

## Phase 3: Sample conversations

Create a proportional random sample of conversation IDs across all agents who appear in the `First response by` column. The goal is at least 40 conversations, distributed roughly in proportion to each agent's share of the workload.

Use Python with `random.seed(42)` for reproducibility. For each agent, calculate their share of total unique conversations and allocate sample slots accordingly. Make sure every agent gets at least 1 sample (even agents with very few conversations).

Filter out any conversation IDs that were corrupted by scientific notation — you need clean numeric IDs to build Freshworks URLs.

## Phase 4: Verify in Freshworks

This is the most time-intensive phase. For each sampled conversation ID, you need to:

1. **Navigate to the conversation URL.** The pattern is:
   ```
   https://{workspace}.myfreshworks.com/crm/messaging/a/{account_id}/inbox/2/0/conversation/{conversation_id}
   ```
   The user should provide or confirm their workspace URL. You can usually get it from the first conversation you open.

2. **Wait for the page to load** (3 seconds is usually enough).

3. **Take a screenshot** and examine it for:
   - **Who responded** — agent names appear above their messages on the right side
   - **Who resolved** — "Resolved by [Agent Name]" appears at the bottom of the conversation
   - **Assignment status** — look at the header area just below the conversation title. If it says "Add group / Add agent" with clickable links, NO agent was assigned. If it shows an agent name instead of "Add agent", an agent WAS assigned.

4. **Log the result** — for each conversation, record:
   - Conversation ID
   - Customer name/account
   - Who responded (from the chat messages)
   - Who resolved
   - Whether an agent was assigned (yes/no)
   - If assigned, who

Work through conversations in batches by agent. Keep a running tally of verified conversations and their results.

**Important edge case:** You may occasionally find a conversation where an agent IS assigned in Freshworks but the spreadsheet still shows the field as empty. This is actually a stronger finding — it means the export itself is broken, not just the assignment workflow. Flag these cases prominently in the report.

## Phase 5: Generate the report

Build a presentation-ready visual using the `show_widget` visualization tool (or create an HTML artifact). The report should include:

**Metric cards** (top row):
- Total conversations in the dataset
- Number of active agents
- Assignment rate (likely 0%)
- Verification sample size (e.g., "46/46")

**Side-by-side comparison:**
- "What actually happened" — agents actively handled X conversations
- "What the system recorded" — 0 agent assignments

**Horizontal bar chart** showing conversations handled per agent (deduplicated), using Chart.js. Include a second dataset showing "assigned in system" (likely all zeros) to make the contrast visual.

**Verification details** — break down the sample count per agent (e.g., "Carter Miller: 22/22, Mykaela Elliott: 10/10")

**Notable findings** — highlight any conversations where assignment existed in Freshworks but was missing from the export

**Impact statement** — explain what this means for analytics (can't track workload, can't measure performance, etc.)

## Tips for a smooth audit

- Start Chrome verification early — it's the bottleneck. The data parsing and analysis can be done in minutes.
- If Chrome disconnects mid-verification, you can pick up where you left off. Just track which conversations you've already checked.
- The user may want to present these findings to leadership. Keep the visual clean and professional — metric cards, clear labels, and a verification badge build credibility.
- If the dataset is very large (thousands of conversations), a sample of 40-50 is statistically meaningful. You don't need to check every single one.
