---
name: freshchat-mine
description: >
  Mine ResaleAI's Freshchat conversation history to build the support bot's knowledge base.
  Pulls resolved conversations over a time window, extracts question→resolution pairs grouped by
  cf_topic, and writes structured knowledge pages into the carter-brain vault. Use this skill when
  the user wants to "train the bot", "build the knowledge base", "mine chat history", "extract
  resolutions from Freshchat", "refresh the support KB", or when starting/refreshing the livechat
  bot project. Also trigger for "what do we already know how to answer" or "turn our chat history
  into knowledge".
---

# Freshchat Knowledge Mining

This skill turns ResaleAI's historical Freshchat conversations into a structured, queryable knowledge base that powers the livechat bot. It reads what your team has *actually resolved* and distills it into reusable resolution patterns.

It is **Phase 1** of the livechat bot build. Run it once to seed the knowledge base, then re-run monthly to keep it fresh as new issues and resolutions appear.

## Connection Details

Use the same Freshchat connection as the `freshchat` skill — base URL, Bearer token, headers, and rate-limit behavior are all defined there. Do not re-paste the API key; read it from the `freshchat` skill or the `FRESHCHAT_API_TOKEN` environment variable.

- **Base URL**: `${FRESHCHAT_BASE_URL}`
- **Bulk extract pattern**: `POST /reports/raw` → poll `GET /reports/raw/{extract_id}` → download signed S3 zip. (The `GET /conversations` list endpoint is plan-gated and returns 403 — do NOT rely on it. Use Reports/Raw for bulk.)

The existing `scripts/freshchat-stats/freshchat_stats.py` already implements the full 3-phase extract (bulk events → hydrate conversations → fetch messages). **Reuse it** rather than rewriting the API client — it handles pagination, the agent-ID map, and the S3 download.

## What to Mine

The signal lives in **resolved** conversations: a customer asked something, an agent solved it. That pairing is exactly what the bot needs.

### Step 1 — Pull the window

Default window: **last 6 months** (override if the user specifies). Use Reports/Raw with these confirmed-valid events:

- `Conversation-Created` — to find conversations and their `cf_topic`
- `Conversation-Resolved` — to filter to the ones that reached resolution
- `Message-Sent` — the full transcript content

Cross-reference created↔resolved on `conversation_id` and keep only conversations that resolved.

### Step 2 — Hydrate transcripts

For each resolved conversation, fetch `GET /conversations/{id}/messages` (paginated, 50/page max). You need the full back-and-forth, with `actor_type` (`user` vs `agent`) and `created_time` so you can reconstruct who said what in order.

### Step 3 — Extract resolution patterns

Group conversations by `cf_topic` (the 27 ResaleAI dropdown values: Backstock, Bin labels, Buys, DRS initials, POS Scanner, License info, Error message/Outage, Install/Update, Day close email, Texting, Fivestars, When I Work, Homebase, Constant Contact, Quickbooks, Reports/KPIs, Goals or Comps, Settings, RAI Sync, Employees, Customer page, Notes/Tasks, Bounceback, Flex, Shopify/CamRAI, Billing, New signup/Demo, Cancellation).

For each topic, distill recurring patterns into entries with this shape:

- **Trigger** — how the customer phrases the problem (paraphrase several real openings)
- **Diagnosis** — what the agent checked to confirm it
- **Resolution** — the steps the agent took that worked
- **Confidence signal** — what makes this safe to auto-answer vs. what means escalate (e.g. "if on latest POS, escalate to Jackson")
- **Frequency** — roughly how often this came up (drives bot priority)
- **Source conversations** — a few representative `conversation_id`s for traceability

Collapse near-duplicate conversations into one pattern. A topic that appears 40 times with the same fix becomes ONE high-confidence entry, not 40.

## Writing to the Brain

Follow the carter-brain schema in `CLAUDE.md` exactly. Knowledge pages live in `wiki/customer-support/`.

- **One pattern = one page**, or extend the existing `common-issues.md` issue log for lightweight ones. Heavier playbooks get their own page (like the existing `name-change-bug.md`, `when-i-work-deactivation-issue.md`).
- Every page needs YAML frontmatter: `title`, `type: pattern` (or `gotcha`), `tags`, `sources` (point at the raw conversations or the stats dataset), `created`, `updated`.
- Cross-link with `[[wikilinks]]` and end with a `## Related` section.
- **Never invent resolutions.** Only write what the transcripts actually show worked. If a "resolution" is just the agent saying "let me escalate", that's an escalation pattern, not an answer — tag it so the bot knows to hand off.
- Before creating a page, search `wiki/index.md` to avoid duplicates. Update existing pages rather than spawning near-duplicates.
- Redact any secrets (store credentials, tokens) per the secrets policy.

After writing, update `wiki/index.md` and append to `wiki/log.md`:
`YYYY-MM-DD HH:MM — freshchat-mine <window> → N patterns across M topics, K pages created/updated`

## Output Summary

End by reporting to the user:

- How many resolved conversations were analyzed, over what window
- A topic-by-topic breakdown: how many patterns, and which are high-confidence (safe to auto-answer) vs. escalate-only
- Coverage gaps — topics with too few examples to answer confidently (these need either more data or a human-authored KB page)
- Which pages were created/updated

The coverage breakdown directly feeds `freshchat-autoreply`: it's the map of what the bot can and can't safely handle.

## Tips

- Resolved-but-reopened conversations are gold for *gotchas* — the first answer didn't stick. Capture why.
- TeamViewer / remote-session resolutions usually can't be automated (they required hands-on access). Tag these "escalate — needs remote session".
- Weight recent conversations higher; product behavior changes (e.g. POS version fixes) make old resolutions stale.

## Related

- `freshchat` skill — the API client / connection details
- `freshchat-autoreply` skill — consumes this knowledge base to answer chats
- `freshchat-learn` skill — feeds new corrections back into these pages
- `scripts/freshchat-stats/freshchat_stats.py` — reusable extract pipeline
