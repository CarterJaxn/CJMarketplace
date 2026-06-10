---
name: qbo-categorize
description: >-
  Categorize and class L2M LLC's QuickBooks bank-feed transactions using the trained knowledge
  base, and sync new training back into it. Use when Carter processes new/uncategorized QuickBooks
  transactions or does the monthly bookkeeping for L2M LLC or its businesses (Cool Springs,
  Murfreesboro, W Nashville, ResaleAI) — e.g. "categorize my QBO transactions", "run the
  categorizer", "do the books". Pulls the bank feed via Chrome, assigns each transaction a GL
  account (category) and a class, posts confident ones, routes the rest to the review artifact.
  ALSO use to SYNC TRAINING: when Carter clicks "Push to Knowledge Base" or says "sync my QBO
  training" / "merge my training", run scripts/merge_training.py to fold his category+class
  decisions into the knowledge base. Trigger even if he doesn't say "skill" — any L2M/ResaleAI
  bookkeeping or training-sync request belongs here.
---

# QBO Categorize + Class (L2M LLC)

Assign every new QuickBooks transaction a **category** (GL account) and a **class** (which of
the four businesses, or shared overhead), using rules learned from 2024–2026 history.

## Entity / class model

**L2M LLC** is the management company over four businesses, each a QBO **class**:

- **Cool Springs**, **Murfreesboro**, **W Nashville** — the three stores
- **ResaleAI** — the tech company
- **L2M Services** — shared/overhead expenses that serve all four businesses (e.g. owner
  guaranteed payments, accounting fees, corporate software, travel, auto, office/storage rent)

The single most important principle: **L2M is driven by the ACCOUNT plus a set of corporate-only
vendors — not by the big shared vendors.** Amazon, American Express, ADP, Pinnacle, etc. split
across all businesses transaction-by-transaction, so they are classed by *which store's bank
account paid them*, never blanket-assigned to L2M.

## Where everything lives

The canonical knowledge base and engine live in the durable folder
`~/Downloads/ResaleAI-QBO-Automation/`:

- `QBO_KnowledgeBase_v2.json` — **the brain.** Vendor rules (category + class), account→L2M
  rules, bank-account→class map, overrides, and description patterns. This file is the single
  source of truth and is what the learning loop updates.
- `categorize.py` — the deterministic engine that applies the knowledge base.
- A seed copy of the KB ships inside this skill at `assets/QBO_KnowledgeBase_v2.seed.json`.
  If the durable folder or KB is missing on first run, copy the seed there and use it.

If `~/Downloads/ResaleAI-QBO-Automation/` isn't connected, request it before starting.

## Workflow

### 1. Pull the uncategorized transactions from QuickBooks (via Chrome)

Use the Claude in Chrome tools against Carter's logged-in browser.

- Open `https://app.qbo.intuit.com/app/banking` and **confirm the company is "L2M LLC"** (top-left). If it's a different company, stop and tell Carter.
- Go to **Transactions → Bank transactions → the "For review" tab**.
- The bank feeds are split by account. For each account tab (Cool Springs / Murfreesboro / W Nashville / ResaleAI mains, etc.), read the rows. Use `get_page_text` / `read_page`; paginate if there are many.
- Capture for every row: **date, payee/description, amount, and which bank account the feed belongs to** (the account name is the key signal for class).
- Use the **raw Full Bank Description** as the vendor/description text (e.g. "TST*DONUT COUNTR…"), not just QBO's cleaned payee — the engine's keyword patterns (like the Toast `tst*` → Employee Meals rule) depend on the raw text.
- You don't need to filter out transfers, cashed checks, or payroll lines — the engine auto-skips those (they're owned by QuickBooks' native bank rules) and lists them in `skipped.csv`.
- Write them to `transactions.csv` in a new run folder (e.g. `~/Downloads/ResaleAI-QBO-Automation/runs/<YYYY-MM-DD>/transactions.csv`) with columns: `date, vendor, amount, bank_account`. The `bank_account` value should start with the account number (e.g. `1101 80100 Main CSprings`) so it matches the KB — if QBO shows a friendly name, map it to the numbered account.

### 2. Run the engine

```bash
cd ~/Downloads/ResaleAI-QBO-Automation
python3 categorize.py --kb QBO_KnowledgeBase_v2.json --in runs/<date>/transactions.csv --out-dir runs/<date>
```

This writes three files into the run folder:

- `categorized.csv` — import-ready rows the rules handled confidently (date, vendor, amount, bank account, **category**, **class**, confidence, and the basis for each decision)
- `review.csv` — rows that need a human decision (no category rule, low confidence, or unknown bank account). Note these still get a best-guess class from the bank account where possible.
- `skipped.csv` — structural rows (inter-account transfers, cashed checks, payroll funding) that QuickBooks' own bank rules already post at 100%; the engine recognizes and skips these by design so they never clutter review
- `run_summary.txt` — counts, coverage %, skipped count, and class distribution

### 3. Review with Carter

Show `run_summary.txt`, then walk Carter through `review.csv`. For each review item, get his
category + class decision. Keep it tight and ADHD-friendly — batch similar items, suggest the
most likely answer, don't make him stare at a giant table.

### 4. Apply to QuickBooks — only with Carter's explicit OK

Posting/accepting transactions in QBO is a side-effectful action. **Do not accept, categorize,
or import anything in QuickBooks without Carter confirming.** When he says go, either:

- accept each "For review" row in QBO with the assigned category + class, or
- hand him `categorized.csv` to import.

### 5. Learning loop — sync the artifact's training into the KB (one click)

This is what makes the skill get smarter, and it's now one click. In the QBO Transaction Review
artifact, Carter assigns category + class to pending items, clicks **Train**, then clicks
**"⬆️ Push to Knowledge Base"**. That hands the new vendor→{category, class} mappings to you in
chat as a JSON block. When you receive that (or any "sync my QBO training" / "push trainings" /
"merge my training" request):

1. Save the JSON mappings to a file, e.g. `runs/training-<date>.json` (a list of objects with
   `vendor`, `category`, `class`, `scope` ("all" | "bank"), `bankAccount`).
2. Run the merger (it auto-backs-up the KB and is idempotent):
   ```bash
   cd ~/Downloads/ResaleAI-QBO-Automation
   python3 merge_training.py --kb QBO_KnowledgeBase_v2.json --in runs/training-<date>.json
   ```
   scope "all" → a vendor rule (category + class at HIGH confidence); scope "bank" → a
   bank-account category override for that (account, vendor).
3. Report what changed. The next categorization run immediately uses the new rules — done.

Optional housekeeping: every so often, refresh the bundled copies (`cp categorize.py
qbo-categorize/scripts/` and `cp QBO_KnowledgeBase_v2.json qbo-categorize/assets/QBO_KnowledgeBase_v2.seed.json`)
and re-package `qbo-categorize.skill` so a fresh install carries the latest rules.

Manual fallback (no button): edit `QBO_KnowledgeBase_v2.json` directly — add/update the vendor under
`vendor_rules` (use a fixed class only if consistent, else `"By bank account (store)"`); a whole
overhead account goes in `account_class_rules`. Back up first.

See `references/rule-logic.md` for the exact precedence and the knowledge-base schema.

## Guardrails

- **Never** post, accept, or import in QuickBooks without explicit confirmation from Carter.
- Treat `QBO_KnowledgeBase_v2.json` as the source of truth; always back it up before editing.
- Don't invent categories or classes — use the GL accounts and the five classes that already
  exist. If something genuinely doesn't fit, send it to review rather than guessing.
- ~Half of real transactions are nameless deposits with no vendor to key on — expect those in
  the review list; they need account/description context, not a vendor rule.
