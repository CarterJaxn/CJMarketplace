---
name: freshchat
description: >
  Query ResaleAI's Freshchat account to look up customer conversations, read message history, and track support issues.
  Use this skill whenever the user wants to search Freshchat conversations, look up what a customer said,
  check the history of a support ticket, find conversations about a specific topic or bug,
  or review recent customer interactions. Also trigger when the user mentions "Freshchat", "chat history",
  "customer messages", "support conversations", or asks things like "what did the customer say",
  "find the conversation about X", or "pull up the chat with [customer name]".
---

# Freshchat Conversation Lookup

This skill lets you query ResaleAI's Freshchat instance to retrieve and review customer support conversations and messages. It's primarily used for looking up customer issues, tracking reported problems, and getting context on what customers have communicated.

## Connection Details

ResaleAI's Freshchat instance:

- **Base URL**: Set via `FRESHCHAT_BASE_URL` environment variable
- **API Key**: Set via `FRESHCHAT_API_TOKEN` environment variable [stored in 1Password — rotate if compromised]

Read credentials from environment variables. Do not hardcode tokens.

## API Basics

All requests go to:

```
${FRESHCHAT_BASE_URL}/{endpoint}
```

Every request needs these headers:

```
Authorization: Bearer <API_KEY>
Accept: application/json
```

Rate limits apply — if you get a 429 response, wait a few seconds and retry. Pagination uses `page` and `items_per_page` query parameters (messages max 50 per page).

## Available Endpoints

Here are the endpoints relevant to conversation lookup:

| What you need | Endpoint | Method | Notes |
|---|---|---|---|
| List/search conversations | `conversations` | GET | Returns conversations with filters |
| Get a specific conversation | `conversations/{conversation_id}` | GET | Returns full conversation object |
| List messages in a conversation | `conversations/{conversation_id}/messages` | GET | Paginated, newest first. `items_per_page` max 50 |
| List users | `users` | GET | Customer/contact records |
| Get a specific user | `users/{user_id}` | GET | Useful after finding a conversation to get customer details |
| List user's conversations | `users/{user_id}/conversations` | GET | All conversations for a specific customer |
| List agents | `agents` | GET | Support agent records |
| List channels | `channels` | GET | Chat channels/topics |
| List groups | `groups` | GET | Agent groups |
| Conversation properties/fields | `conversations/fields` | GET | Custom field definitions |

## Workflow

Follow this general approach when the user asks to look something up:

### 1. Figure out what to search for

The user might give you a customer name, an email, a conversation ID, a topic, or a vague description. Clarify if needed, but often you can infer the right approach:

- **Customer name or email** → Search users first, then get their conversations
- **Conversation ID** → Go directly to that conversation and its messages
- **Topic or keyword** → List recent conversations and scan for relevance
- **"Recent issues"** → List conversations sorted by recent activity

### 2. Make the API calls

Use `curl` in the shell to call the Freshchat API. Here's the pattern:

```bash
API_KEY="<the API key from Connection Details above>"
BASE="${FRESHCHAT_BASE_URL}"

curl -s -H "Authorization: Bearer $API_KEY" \
  -H "Accept: application/json" \
  "$BASE/conversations?page=1&items_per_page=20" | python3 -m json.tool
```

Pipe through `python3 -m json.tool` for readable output, or use `jq` if available.

### 3. Drill into messages

Once you have a conversation ID, fetch its messages:

```bash
curl -s -H "Authorization: Bearer $API_KEY" \
  -H "Accept: application/json" \
  "$BASE/conversations/{conversation_id}/messages?page=1&items_per_page=50" | python3 -m json.tool
```

Messages contain the actual text exchanged between the customer and agents. Each message has `message_parts` with the content, an `actor_id` (who sent it), `actor_type` (user or agent), and a `created_time` timestamp.

### 4. Resolve names

Conversation and message objects reference users and agents by ID. To make the output human-readable:

- Fetch the user with `users/{user_id}` to get their name/email
- Fetch agents with `agents` to map agent IDs to names
- Cache these lookups within the session to avoid redundant calls

### 5. Present the results

Summarize what you found in a clear, readable way. For conversation lookups, include:

- Customer name and email
- When the conversation started and its current status
- A summary of the key messages (paraphrase long exchanges)
- The assigned agent, if any
- Any resolution or last action taken

For issue tracking, focus on extracting the problem description, any error messages the customer reported, and what steps support has taken so far.

## Response Format Gotchas

A few things to watch for when parsing API responses:

- **List endpoints wrap results differently.** `users` returns `{"users": [...]}`, `agents` returns `{"agents": [...]}`, but `messages` returns an array directly at the top level. Always inspect the actual response shape.
- **Message content** is in `message_parts`, which is an array. Each part has a `text` field with the actual content. Some parts may be images or other media — the `type` field tells you.
- **Timestamps** are in ISO 8601 format (UTC).
- **Pagination** — if the response has more pages, increment the `page` parameter. There's no explicit "next page" link; you'll know you've reached the end when fewer items than `items_per_page` come back.
- **Conversation status** values include things like `new`, `assigned`, `resolved`, `reopened`. The exact values depend on your account's configuration.

## Error Handling

| Status | Meaning | Action |
|---|---|---|
| 401 | Invalid or expired token | Ask the user to check/regenerate their API key |
| 403 | Insufficient permissions | The API key may not have access to this resource |
| 404 | Resource not found | Double-check the ID — it might be wrong or deleted |
| 429 | Rate limited | Wait 5-10 seconds and retry |
| 500/503 | Server error | Retry once after a brief wait; if persistent, it's a Freshchat issue |

## Tips

- When searching for a customer, try the `users` endpoint with query parameters first. If the API doesn't support text search, fetch a page of users and filter locally.
- For tracking issues across conversations, look at conversation properties/custom fields — ResaleAI may tag conversations with issue categories or ticket IDs.
- If the user asks about a specific time period, filter conversations by checking `created_time` in the response and paginating as needed.
- Keep API calls minimal — fetch what you need, don't pull everything. Start with small page sizes and only paginate further if the user needs more results.
