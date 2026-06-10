---
name: dropbox-bank-statements
description: "Access and parse bank statement PDFs from Carter's Dropbox for financial analysis. Use this skill whenever working with Pinnacle Bank or Chase/JHM-Southwest bank statements, analyzing vendor expenses, tracking spending trends, reconciling accounts, or any task involving the Dropbox bank statement archive. Trigger when the user mentions 'bank statements', 'Dropbox statements', 'Pinnacle statements', 'JHM', 'vendor expenses', 'spending analysis', or references specific accounts like RAI Main, CS Main, WB Main, MB Main, or the Chase Southwest card."
---

# Dropbox Bank Statements

Access and parse L2M LLC / ResaleAI bank statement PDFs stored in Carter's local Dropbox sync folder.

## Dropbox Location

The Dropbox folder must be connected via `request_cowork_directory` with path `~/Dropbox`. Once connected:

- **Host path** (Read/Write/Edit/Glob): `/Users/cartermiller/Library/CloudStorage/Dropbox`
- **Bash sandbox path**: Check the mount list — typically `/sessions/*/mnt/Dropbox`

If you get "Resource deadlock avoided" errors in bash, the files are Dropbox online-only. Ask Carter to download them locally first (right-click > Make Available Offline in Finder), then retry.

## Folder Structure

```
Dropbox/
├── 2025/
│   ├── pinnacle/           # Pinnacle Bank (lowercase p in 2025)
│   │   ├── RAI Main Jan 2025.pdf
│   │   ├── CS Main Jan 2025.pdf
│   │   ├── CS Buy Jan 2025.pdf
│   │   ├── MB Main Jan 2025.pdf
│   │   ├── MB Buy Jan 2025.pdf
│   │   ├── WB Main Jan 2025.pdf
│   │   └── WB Buy Jan 2025.pdf
│   └── JHM-Southwest/      # Chase Southwest credit card
│       └── 20250109-statements-XXXX-.pdf
├── 2026/
│   ├── Pinnacle/           # NOTE: capital P in 2026
│   └── JHM-Southwest/      # May be empty — check 2025 folder for recent
```

**Naming patterns:**
- Pinnacle: `{ACCT} {Month} {Year}.pdf` — e.g., `RAI Main Jan 2025.pdf`
- JHM-Southwest: `{YYYYMMDD}-statements-XXXX-.pdf` — date is statement close date

**Month spellings used:** Jan, Feb, Mar, Apr, May, June, Jul, Aug, Sept, Oct, Nov, Dec
(note: "June" and "Sept" — not "Jun" or "Sep")

## Account Codes

| Code | Entity | Bank | Type |
|------|--------|------|------|
| RAI Main | ResaleAI (L2M LLC DBA ResaleAI) | Pinnacle XXXX | Operating checking |
| CS Main | Cool Springs (Plato's Closet) | Pinnacle | Store checking |
| CS Buy | Cool Springs | Pinnacle | Buy account |
| MB Main | Murfreesboro (Plato's Closet) | Pinnacle | Store checking |
| MB Buy | Murfreesboro | Pinnacle | Buy account |
| WB Main | White Bridge / W Nashville (Plato's Closet) | Pinnacle | Store checking |
| WB Buy | White Bridge | Pinnacle | Buy account |
| JHM-Southwest | Jackson Miller personal | Chase XXXX | Credit card |

## Parsing Statements

Use `pymupdf` (fitz) in the bash sandbox. Install once:
```bash
pip install pymupdf --break-system-packages -q
```

### Pinnacle Bank Format

Pages contain "Credit Transactions" (deposits) and "Debit Transactions" (expenses).
Each transaction line:
```
MM/DD    DESCRIPTION_TEXT    AMOUNT
```

Amounts have no sign — determine debit/credit from the section header. Multi-line descriptions are common.

Key description patterns:
- Card purchases: `VENDOR_NAME CITY ST MMDDYY NNNNNN Card#NNNN`
- ACH/electronic: `PAYEE_NAME  PAYMENT_TYPE REFERENCE_NUMBER`
- Internal transfers: `OLB Transfer from *NNN to *NNN Transfer`
- Payroll: `ADP` prefix lines

### Chase/JHM-Southwest Format

"ACCOUNT ACTIVITY" section with:
```
MM/DD     DESCRIPTION    AMOUNT
```

Payments are negative (with `-` prefix). Purchases are positive.

### Extraction Approach

```python
import fitz, re, json

def extract_all_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    doc.close()
    return text

def parse_pinnacle_debits(text):
    """Extract debit transactions from Pinnacle statement text."""
    transactions = []
    # Find debit section
    for marker in ["Other Debits", "Debit Transactions"]:
        if marker in text:
            text = text[text.index(marker):]
            break
    
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        date_match = re.match(r'^(\d{1,2}/\d{2})\s+(.+)', line)
        if date_match:
            date = date_match.group(1)
            rest = date_match.group(2).strip()
            amount_match = re.search(r'([\d,]+\.\d{2})\s*$', rest)
            if amount_match:
                amount = float(amount_match.group(1).replace(',', ''))
                desc = rest[:amount_match.start()].strip()
                transactions.append({'date': date, 'description': desc, 'amount': amount})
            else:
                # Amount on next line
                desc = rest
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    amt = re.search(r'^([\d,]+\.\d{2})\s*$', next_line)
                    if amt:
                        transactions.append({
                            'date': date, 'description': desc,
                            'amount': float(amt.group(1).replace(',', ''))
                        })
                        i += 1
        i += 1
    return transactions

def parse_chase_purchases(text):
    """Extract purchase transactions from Chase statement text."""
    transactions = []
    in_activity = False
    for line in text.split("\n"):
        line = line.strip()
        if "ACCOUNT ACTIVITY" in line:
            in_activity = True
            continue
        if not in_activity:
            continue
        match = re.match(r'^(\d{2}/\d{2})\s+(.+?)\s+(-?[\d,]+\.\d{2})\s*$', line)
        if match:
            amount = float(match.group(3).replace(',', ''))
            if amount > 0:  # skip payments
                transactions.append({
                    'date': match.group(1),
                    'description': match.group(2).strip(),
                    'amount': amount
                })
    return transactions
```

Always spot-check parsed results against the source PDF — text extraction is messy.

## Vendor Normalization

Bank descriptions are noisy. Common cleanup patterns:

| Raw Pattern | Normalized Vendor |
|-------------|-------------------|
| `GOOGLE *FIBER` | Google Fiber |
| `CHASE CREDIT CRD  EPAY` | Chase Credit Card Payment |
| `STRIPE TRANSFER` | Stripe |
| `ADP *` | ADP (Payroll) |
| `OLB Transfer` | Internal Transfer |
| `MICROSOFT*` | Microsoft |
| `SQSP*` | Squarespace |
| `GITHUB, INC.` | GitHub |
| `SQ *` | Square |
| `PROG HAWAII INS` | Progressive Insurance |
| `FIC *PIC INSURANCE` | PIC Insurance |
| `TERMLY.IO` | Termly |
| `PROPROFS` | ProProfs |
| `SOLARWINDS` | SolarWinds |
| `OPENAI *CHATGPT` | OpenAI |
| `ADOBE` | Adobe |
| `HEROKU*` | Heroku |
| `DOCHUB` | DocHub |

Build and expand this map as you encounter new vendors.

## Analysis Tips

- **Start with Main accounts** — they have recurring vendor expenses (SaaS, utilities, insurance, services)
- **Buy accounts** are primarily customer buy payouts — less useful for vendor expense analysis
- **RAI Main** has the broadest vendor mix (operating account for all of ResaleAI)
- **JHM-Southwest** is Jackson's credit card — some business expenses run through it
- **Exclude** internal transfers (OLB Transfer, Chase Credit Card payments) and payroll (ADP) from vendor expense analysis unless specifically asked
- When comparing across months, normalize vendor names before grouping
- For "expenses cut" analysis: look for vendors present in early months but absent in later months, or vendors with significant spend reduction
