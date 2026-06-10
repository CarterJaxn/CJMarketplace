# Rule logic, knowledge-base schema, and how to update it

## Decision precedence (this is exactly what `categorize.py` implements)

**Category (GL account):**
1. **Bank-account override** — if a `(bank_account, vendor)` pair is in `bank_account_category_overrides`, use that category. (Handles vendors that behave differently in one store's account.)
2. **Exact vendor rule** — case-insensitive match on the vendor name in `vendor_rules`.
3. **Description keyword** — if no vendor match, scan the description for any `description_patterns` keyword (substring match).
4. **Otherwise** — leave uncategorized → goes to `review.csv`.

**Class:**
1. **Account-default L2M** — if the assigned category is in `account_class_rules`, the class is **L2M Services**. (Account is the strongest L2M signal: guaranteed payments, accounting fees, travel, automobile, office/storage rent, auto insurance, interest, furniture.)
2. **Vendor fixed class** — else if the vendor's rule has a fixed class (`L2M Services`, `ResaleAI`, or a specific store), use it. Corporate-only vendors (Tesla, Dropbox, Workable, Intuit, etc.) are fixed to L2M; ResaleAI-only SaaS is fixed to ResaleAI.
3. **Bank-account class** — else use the class of the bank account that paid (the `bank_account_class` map). This is the default for the big shared vendors (`"By bank account (store)"`).
4. **Otherwise** — unknown bank account → flag for review.

Why it's built this way: vendor alone can't decide L2M because the biggest vendors (Amazon, Amex, ADP, Pinnacle) are split across every business. The account a transaction is coded to, plus a known set of corporate-only vendors, is what actually predicts shared overhead. Everything else follows the money — whichever store's account paid it.

## Knowledge-base schema (`QBO_KnowledgeBase_v2.json`)

```json
{
  "version": "v2",
  "bank_account_class": { "1101 80100 Main CSprings": "Cool Springs", ... },
  "account_class_rules": { "6575 Guaranteed Payment-Jack": "L2M Services", ... },
  "bank_account_category_overrides": [
    { "bank_account": "1101 80100 Main CSprings", "vendor": "Pinnacle National Bank", "category": "..." }
  ],
  "description_patterns": [ { "label": "Greko", "keywords": "greko", "category": "6505 Employee Meals" } ],
  "vendor_rules": {
    "amazon": { "display": "AMAZON", "category": "7450 Supplies", "class": "By bank account (store)",
                "cat_confidence": "HIGH", "class_basis": "...", "hist_txns": 2616 }
  }
}
```

Vendor keys are normalized (lowercased, trimmed). `class` is one of the five classes or the
literal string `"By bank account (store)"`.

## How to add/update rules (learning loop)

**A vendor should always get a category + a fixed class** (e.g. a new SaaS tool that's ResaleAI):
```json
"new vendor": {"display":"New Vendor","category":"7810 Computer/Tech Services","class":"ResaleAI","cat_confidence":"HIGH"}
```

**A vendor's class depends on which store paid** (most retail vendors):
set `"class": "By bank account (store)"` — the engine will use the paying account's class.

**A whole account is always shared overhead:** add it to `account_class_rules` with value `"L2M Services"`. This overrides the vendor's class whenever a transaction lands in that account.

**A vendor is miscoded in one specific account only:** add a `bank_account_category_overrides` entry.

After editing, re-run `categorize.py` on a recent batch and skim `run_summary.txt` to sanity-check the class distribution didn't shift unexpectedly.

## Known limits

- **Nameless deposits** (~half of real transactions) have no vendor — they can't be vendor-ruled and will land in review. They need account/description/amount context.
- The five classes and the existing GL accounts are the whole universe — don't create new ones here; that's a QuickBooks chart-of-accounts change.
