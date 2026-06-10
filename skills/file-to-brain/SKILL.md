---
name: file-to-brain
description: >
  File content into Carter's Obsidian second brain vault (~/Carter-brain). Use this skill whenever the user wants to
  save, capture, remember, or file something into their second brain, knowledge base, or vault. Trigger phrases include
  "file this", "save this to my brain", "remember this", "add this to the vault", "capture this", "put this in my brain",
  "log this", "note this down", or any request to persist information, ideas, research, decisions, or learnings into
  the Obsidian vault. Also use when the user says "brain" in the context of storing or organizing information, when they
  ask to "turn this conversation into a note", or when they want to save something they learned during a session.
  Even if the user just says "file it" or "save it" without specifying where — if they have a second brain, this is
  where it goes.
---

# File to Brain

You are the librarian for Carter Miller's Obsidian second brain vault.

## Step 0 — Get access and load the rules

1. Call `request_cowork_directory` with path `~/Carter-brain`. You cannot proceed without this.
2. Read `~/Carter-brain/CLAUDE.md` — this is the source of truth for all vault conventions. Every rule in that file applies here. If anything in this skill conflicts with CLAUDE.md, CLAUDE.md wins.
3. Read `~/Carter-brain/wiki/index.md` — you need this to check for existing pages before creating new ones.

Do all three before writing anything.

## Step 1 — Identify what to file

Look at the conversation context and figure out what the user wants to capture. This might be:

- **Something from this conversation** — research findings, a decision made, an idea discussed, a workflow figured out, a lesson learned
- **A specific thing the user describes** — "remember that Brad's stores use the old WIW integration" or "file this: we decided to switch to Stripe"
- **An artifact or file created in this session** — a document, a script, an analysis
- **External content** — an article, a Slack thread, a meeting summary the user pastes or references

If it's ambiguous what exactly should be filed, ask. But if the user said "file this" after a discussion, capture the key substance of that discussion — don't ask them to repeat it.

## Step 2 — Classify and plan

Based on the content, determine:

### Which layer?

Most ad-hoc captures go to **both** layers:
- A raw capture in `raw/` (the immutable record of what was captured and when)
- One or more wiki pages in `wiki/` (the synthesized, linked knowledge)

For quick factual updates to existing wiki pages (e.g., "update Brad Bishop's page — he now has 20 stores"), you can skip the raw file and just update the wiki page directly. Use judgment.

### Raw file location

| Content type | Path | Example |
|---|---|---|
| Meeting notes | `raw/meetings/YYYY-MM-DD-<slug>.md` | `raw/meetings/2026-05-06-pricing-discussion.md` |
| Article or web content | `raw/articles/YYYY-MM-DD-<slug>.md` | `raw/articles/2026-05-06-zettelkasten-method.md` |
| Customer issue | `raw/customer-issues/YYYY-MM-DD-<slug>.md` | `raw/customer-issues/2026-05-06-store-20945-sync.md` |
| General capture | `raw/daily/YYYY-MM-DD-<slug>.md` | `raw/daily/2026-05-06-stripe-migration-decision.md` |

### Wiki destination

Decide which `wiki/` subdirectory fits best by asking: "What kind of knowledge is this?"

| If it's about... | Put it in... | Type |
|---|---|---|
| A reusable approach | `wiki/projects/` or `wiki/standards/` | `pattern` or `process` |
| A trap or non-obvious behavior | relevant subdirectory | `gotcha` |
| A choice with context | relevant subdirectory | `decision` |
| An idea or framework | `wiki/concepts/` | `concept` |
| A step-by-step procedure | relevant subdirectory | `process` or `workflow` |
| A person, company, or tool | `wiki/entities/` | `entity` |
| Customer support knowledge | `wiki/customer-support/` | varies |
| Accounting or reconciliation | `wiki/bookkeeping/` | varies |
| Personal finance | `wiki/finance/` | varies |
| AI tools, prompts, automation | `wiki/ai-tools/` | varies |
| A creative project or idea | `wiki/creative/` | varies |
| Cross-cutting analysis | `wiki/synthesis/` | `synthesis` |
| A personal convention | `wiki/standards/` | `pattern` or `process` |

If it relates to an active project (especially ResaleAI), consider putting it under `wiki/projects/<project>/` instead.

### Tags

Pick from the tag taxonomy in CLAUDE.md. You can extend the taxonomy if nothing fits, but check existing tags first. Aim for 2-4 tags per page — enough to find it later, not so many that tags become noise.

## Step 3 — Tell the user what you're going to do

Before writing anything, briefly tell the user your plan. Something like:

> "I'll file this as a decision record in `wiki/projects/resaleai/` about the Stripe migration, tagged with `resaleai`, `decision`, `product`. I'll also create a raw capture. Sound good?"

Keep it to 1-2 sentences. If the user says "just file it" or seems impatient, trust your classification and go — don't force a confirmation loop. The point of auto-organize is that it should usually just work.

## Step 4 — Write the files

### Raw file

Write the raw capture first. Include YAML frontmatter:

```yaml
---
title: "Descriptive title"
type: source
tags: [relevant, tags]
captured: YYYY-MM-DD
captured_from: conversation | slack | meeting | article | manual
---
```

Then write the content. For conversation captures, distill the key substance — don't dump the entire chat. Write it so Carter's future self can understand the context without re-reading the whole conversation. Include:
- **What** was discussed or decided
- **Why** it matters (this is the most important part — raw facts without context are useless)
- **Any action items or follow-ups**

### Wiki pages

Follow the full Ingest operation from CLAUDE.md:

1. For each entity, concept, decision, gotcha, or workflow in the content:
   - Search `wiki/index.md` first. If a matching page exists, **update it** (re-read it first for concurrency safety). If not, **create a new one**.
2. Every wiki page gets proper YAML frontmatter per CLAUDE.md (title, type, tags, sources, created, updated).
3. Every page ends with a `## Related` section with `[[wikilinks]]` to connected pages.
4. Use `[[wikilinks]]` everywhere, never markdown links.
5. One page = one concept. If you're cramming multiple distinct ideas into one page, split them.

### Write for future Carter

The research on second brains is clear: notes that just save raw information get abandoned. The reason this vault is useful is because every page includes **why it matters**. When writing wiki pages:
- Add 1-2 sentences of context about why this knowledge is worth keeping
- Connect it to things Carter already knows (via wikilinks)
- If it's a decision, include the alternatives considered and why they were rejected
- If it's a gotcha, explain what makes it non-obvious

## Step 5 — Update the index and log

1. **Update `wiki/index.md`** — add any new pages to the appropriate section table.
2. **Append to `wiki/log.md`** — one line: `YYYY-MM-DD HH:MM — file-to-brain → <summary of what was filed>. Pages created/updated: <list>.`
3. **If this relates to an active project**, update that project's `_status.md` per the Session Bookkeeping rules in CLAUDE.md.

## Step 6 — Confirm to the user

After filing, tell the user what you did in 1-2 sentences. Include the wiki page paths so they can find them in Obsidian. Example:

> "Filed. Created [[wiki/projects/resaleai/stripe-migration-decision]] and updated [[wiki/entities/jackson-miller]] with the migration context. Raw capture in `raw/daily/2026-05-06-stripe-migration.md`."

## Important rules

These come from CLAUDE.md and are repeated here for emphasis:

- **NEVER edit `raw/` files after creation.** They are immutable.
- **Always re-read a file before editing it** (concurrency awareness).
- **Never write passwords, API keys, or tokens.** Use `[stored in 1Password]` or `[ask Carter]` placeholders.
- **Check `wiki/index.md` before creating** to avoid duplicates.
- **Keep pages atomic** — one concept per page, split if needed.
