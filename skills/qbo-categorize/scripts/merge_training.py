#!/usr/bin/env python3
"""
Merge training decisions (from the QBO Transaction Review artifact) into the
knowledge base. This closes the learning loop: when Carter trains a vendor in
the artifact and clicks "Push to Knowledge Base", the artifact hands the new
mappings to Claude, which runs this to fold them into QBO_KnowledgeBase_v2.json.

Input: a JSON file containing a list of trainings, each:
  {"vendor": "...", "category": "7450 Supplies", "class": "Cool Springs",
   "scope": "all" | "bank", "bankAccount": "1106 80100 Buy CSprings"}

Rules:
  - scope "all"  -> vendor rule (applies to the vendor on every account)
  - scope "bank" -> bank-account category override for (bankAccount, vendor)
Always backs up the KB first. Idempotent: re-merging the same training is a no-op.

Usage: python3 merge_training.py --kb QBO_KnowledgeBase_v2.json --in trainings.json
"""
import argparse, json, datetime, shutil, os

def norm(s): return str(s).strip().lower() if s else ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kb", default="QBO_KnowledgeBase_v2.json")
    ap.add_argument("--in", dest="infile", required=True)
    args = ap.parse_args()

    with open(args.infile) as f:
        data = json.load(f)
    trainings = data if isinstance(data, list) else data.get("trainings", [])
    if not trainings:
        print("No trainings found in input."); return

    with open(args.kb) as f:
        kb = json.load(f)
    kb.setdefault("vendor_rules", {})
    kb.setdefault("bank_account_category_overrides", [])

    # backup
    bak = args.kb.replace(".json", "") + ".bak-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".json"
    shutil.copyfile(args.kb, bak)

    added = updated = overrides = 0
    changes = []
    for t in trainings:
        vendor = (t.get("vendor") or "").strip()
        category = (t.get("category") or "").strip()
        klass = (t.get("class") or "").strip()
        scope = (t.get("scope") or "all").strip().lower()
        bank = (t.get("bankAccount") or "").strip()
        if not vendor or not category:
            continue
        vn = norm(vendor)
        if scope == "bank" and bank:
            # account-specific category override
            ov = kb["bank_account_category_overrides"]
            existing = next((o for o in ov if norm(o.get("vendor","")) == vn and o.get("bank_account","") == bank), None)
            if existing:
                existing["category"] = category
            else:
                ov.append({"bank_account": bank, "vendor": vendor, "category": category})
                overrides += 1
            changes.append(f"override: {vendor} @ {bank} -> {category}")
        # always (re)assert a vendor rule carrying the class too
        exists = vn in kb["vendor_rules"]
        prev = kb["vendor_rules"].get(vn, {})
        kb["vendor_rules"][vn] = {
            "display": vendor,
            "category": category,
            "class": klass or prev.get("class", "By bank account (store)"),
            "cat_confidence": "HIGH",
            "class_basis": "trained (review artifact)",
            "hist_txns": prev.get("hist_txns", 0),
            "recurring": prev.get("recurring", False),
            "trained_at": datetime.datetime.now().isoformat(timespec="seconds"),
        }
        if exists: updated += 1
        else: added += 1
        changes.append(f"{'updated' if exists else 'new'}: {vendor} -> {category} | {klass or '(by account)'}")

    with open(args.kb, "w") as f:
        json.dump(kb, f, indent=1)

    print(f"Merged {len(trainings)} training(s) into {os.path.basename(args.kb)}")
    print(f"  vendor rules: {added} new, {updated} updated | overrides added: {overrides}")
    print(f"  backup: {os.path.basename(bak)}")
    print("  changes:")
    for c in changes:
        print("   -", c)

if __name__ == "__main__":
    main()
