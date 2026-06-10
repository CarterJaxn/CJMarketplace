---
name: slack-cs-message
description: >
  Send a Slack message to the #customer_success channel on behalf of Carter.
  Use this skill whenever the user wants to post a message to the customer success channel,
  share an update with the CS team, notify customer success about something,
  relay information to #customer_success, or says things like "send this to CS",
  "post in customer success", "let the CS team know", "message customer_success",
  or "update the support channel". Also trigger when the user asks to share Freshchat
  conversation summaries, customer issue updates, or any information with the CS team via Slack.
---

# Send Message to #customer_success

This skill sends a Slack message to ResaleAI's `#customer_success` channel as Carter. The channel is used for all things customer success — issue updates, customer reports, team coordination.

## Channel Details

- **Channel**: #customer_success
- **Channel ID**: `C7G40M45Q`
- **Purpose**: All things customer success

Always use channel ID `C7G40M45Q` — no need to search for it.

## How to Send

Use the `slack_send_message` tool with these parameters:

- `channel_id`: `C7G40M45Q`
- `message`: The message content (supports Slack markdown)

That's it. The message posts as Carter automatically since his Slack account is connected.

## Important: Draft vs. Send

There are two tools available, and which one to use depends on whether Carter has seen the message:

- **`slack_send_message`** — Use when Carter has explicitly approved the message content, or when he's told you exactly what to say. This sends immediately.
- **`slack_send_message_draft`** — Use when you're composing the message yourself (e.g., summarizing something, writing an update). This saves a draft in Carter's Slack so he can review before sending. Prefer this when in doubt.

The general rule: if Carter typed or confirmed the exact text, send it. If you're generating the text, draft it.

## Message Formatting

Slack supports standard markdown:

- **Bold**: `**text**`
- *Italic*: `_text_`
- `Code`: `` `code` ``
- ~~Strikethrough~~: `~text~`  (single tilde in Slack)
- Blockquotes: `>text`
- Links: `[text](url)`
- Code blocks: ` ```language\ncode\n``` `
- Tables: standard markdown table syntax with `|` delimiters — do NOT escape the structural `|` characters

Messages are limited to 5000 characters per text element. If the content is longer, break it into multiple messages.

## Threading

To reply in a thread instead of posting a new message:

- Set `thread_ts` to the parent message's timestamp
- Optionally set `reply_broadcast` to `true` to also show the reply in the main channel

## Common Patterns

### Posting a quick update
Carter says something like "tell CS that the pricing bug is fixed" — compose a clear, professional message and send it directly since Carter stated the intent clearly.

### Sharing a Freshchat summary
Carter asks to summarize a Freshchat conversation and share it with CS — compose the summary and use `slack_send_message_draft` since you're generating the content. Carter can review before it goes out.

### Replying to an existing thread
If Carter references a specific conversation in the channel, use `slack_read_channel` with channel ID `C7G40M45Q` to find the relevant message timestamp, then reply in-thread.

## Tone

Messages should sound like Carter — professional but not stiff. Keep it concise and direct. No need for formal greetings or signatures in Slack. Match the casual-but-informative tone typical of internal Slack channels.
