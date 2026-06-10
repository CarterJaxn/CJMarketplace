---
name: freshchat-learn
description: >
  Feedback loop for the Freshchat bot. Reviews recent bot escalations and the human corrections that
  followed, then turns them into new or updated knowledge-base pages so the bot gets smarter over
  time. Use this skill when the user wants to "review what the bot escalated", "improve the bot from
  corrections", "close the loop", "what did the bot miss", "update the KB from yesterday's chats",
  or for a weekly/daily bot review. Proposes KB changes for approval — does not silently rewrite.
---

# Freshchat Learn (Correction Loop)

The bot only improves if every escalation and every human correction teaches it something. This skill is the loop: it looks at where the bot punted or got it wrong, sees how the human actually solved it, and proposes knowledge-base updates so the bot handles it next time.

It is **Phase 3** (continuous improvement). Run it on a cadence — daily during early rollout, weekly once stable.

## What to Review

Cover the period since the last run (default: since yesterday, or since the last `freshchat-learn` entry in `wiki/log.md`). Three buckets:

### 1. Escalations the bot raised

For each `action: escalate` the bot produced, find how the human resolved it (fetch the conversation's later messages via the `freshchat` skill).

- **Resolved with a clean, repeatable answer?** → the bot *should* have known this. Capture it as a new/updated KB pattern so it's HIGH-confidence next time.
- **Needed remote/backend/billing/human judgment?** → the escalation was correct. Confirm the escalation pattern is documented so the bot keeps escalating it (don't accidentally teach it to guess).

### 2. Bot answers that got corrected

Find conversations where the bot (or a human approving the bot's draft) replied, and a human then sent a *different* answer or the customer pushed back. These are the highest-value lessons — the bot was confident and wrong.

- Diagnose *why* the KB pattern misfired: wrong trigger match, stale resolution, missing precondition.
- Propose the specific fix to the pattern (tighten the trigger, add the precondition, downgrade to escalate-only, update the steps).

### 3. New issues with no KB coverage

Topics or problems showing up in chats that don't exist in `wiki/customer-support/` at all. Flag these as coverage gaps and draft starter pages from the human's resolution.

## Producing Updates

Follow the carter-brain schema in `CLAUDE.md`:

- Update existing `wiki/customer-support/` pages in place when the pattern already exists; create new pages (proper frontmatter, `[[wikilinks]]`, `## Related`) only when there's no home for it.
- Search `wiki/index.md` first to avoid duplicates.
- Ground every change in real transcript evidence — cite the `conversation_id`s that motivated it.
- Redact secrets per policy.

**Do not silently rewrite the KB.** Present the proposed changes as a reviewable checklist:

```
PROPOSED KB UPDATES — review before applying
1. UPDATE common-issues.md → add "Day close email duplicate send" row   [conv abc123]
2. NEW   wiki/customer-support/quickbooks-sync-token-expired.md          [conv def456, ghi789]
3. DOWNGRADE name-change-bug pattern to escalate-only on latest POS      [conv jkl012 — bot answered wrong]
```

Apply only what the user confirms. This keeps Carter as curator and the LLM as librarian, per the vault's operating model.

After applying approved changes, update `wiki/index.md` and append to `wiki/log.md`:
`YYYY-MM-DD HH:MM — freshchat-learn <period> → reviewed N escalations / M corrections → K pages updated`

## Output Summary

Report:
- How many escalations and corrections were reviewed
- The proposed-changes checklist (the actual work product)
- Trend signal: are escalations on a topic going down over time? Which topics are now ready to graduate to auto-answer? Feed this back into `freshchat-replay` to re-validate before flipping any topic live.

## Guardrails

- Read-only against customers — this skill reviews and proposes; it never messages customers.
- A correction loop can drift the KB if it overfits to one angry customer. Require a pattern to recur (or be clearly general) before promoting it to HIGH-confidence auto-answer.
- Never teach the bot to handle billing, cancellation, refunds, or account changes autonomously, no matter how clean the correction looks — those stay human-only by policy.

## Related

- `freshchat-autoreply` skill — consumes the improved KB
- `freshchat-replay` skill — re-validate a topic after updates before going live
- `freshchat-mine` skill — the original KB build this loop maintains
- `slack-cs-message` skill — for surfacing notable misses to the CS team
