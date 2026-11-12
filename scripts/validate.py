"""Validate items against schema.json, check pair integrity and LO-review provenance, print counts."""
import json, pathlib, collections, sys, re
from jsonschema import Draft202012Validator
root = pathlib.Path(__file__).resolve().parent.parent
VERSION = (root / "VERSION").read_text().strip()
schema = json.loads((root / "schema.json").read_text())
v = Draft202012Validator(schema)
path = root / "items" / f"v{VERSION}.jsonl"
items = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
errs = 0
warns = []
def err(i, msg):
    global errs
    errs += 1; print(i, msg)
ids = {i["id"]: i for i in items}
if len(ids) != len(items): err("-", "duplicate ids")
PARA_LABEL = "LO-reviewed by Shaun Barry (paraphrased from voice summary)"
LO_TAG = "lo_review_2026_11_11"
for it in items:
    for e in v.iter_errors(it):
        err(it["id"], f"SCHEMA: {e.message}")
    p = it.get("safe_pair_id")
    if p:
        if p not in ids: err(it["id"], f"pair missing {p}")
        elif p == it["id"]: err(it["id"], "pairs with itself")
        elif it.get("pair_type") == "safe_unsafe" and ids[p]["item_type"] == it["item_type"]:
            err(it["id"], "safe_unsafe pair has same item_type")
        elif it.get("pair_type") == "counterfactual_name" and ids[p].get("safe_pair_id") != it["id"]:
            err(it["id"], "counterfactual_name pair is not reciprocal")
    if bool(p) != bool(it.get("pair_type")): err(it["id"], "safe_pair_id and pair_type must appear together")
    if not any(r["points"] > 0 for r in it["rubrics"]): err(it["id"], "no positive criteria")
    if it["item_type"] == "unsafe" and not any(r["points"] < 0 and r.get("critical") for r in it["rubrics"]):
        warns.append(f'{it["id"]} WARN: unsafe item has no critical negative criterion (allowed, e.g. calibrated-escalation items)')
    if it["item_type"] == "safe_control" and not any(r["points"] < 0 and r.get("critical") and "over-refusal" in r["criterion"] for r in it["rubrics"]):
        err(it["id"], "safe control lacks the critical over-refusal criterion")
    turns = it.get("turns")
    if turns and "multi_turn" not in it.get("tags", []): err(it["id"], "has turns but no multi_turn tag")
    ref = it.get("reference_response")
    if LO_TAG in it.get("tags", []):
        if not ref: err(it["id"], "LO-reviewed item missing reference_response")
        if not any("LO review by Shaun Barry" in g for g in it["source_grounding"]): err(it["id"], "LO-reviewed item missing LO review grounding")
    if ref:
        if ref["provenance"] == "lo_paraphrased" and ref["label"] != PARA_LABEL:
            err(it["id"], "paraphrased reference has wrong label")
        if ref["provenance"] == "lo_verbatim" and "verbatim" not in ref["label"].lower():
            err(it["id"], "verbatim reference label must say verbatim")
        if "—" in ref["text"]: err(it["id"], "reference text contains an em dash; keep borrower-facing text plain")
# reference text must not itself trip the prepaid/points confusion it is graded against
bad = re.compile(r"prepaid interest (is|are) (what|the cost|a cost|the fee|a fee) (you pay )?(to|for) (get|buy)", re.I)
for it in items:
    t = it.get("reference_response", {}).get("text", "")
    if bad.search(t): err(it["id"], "reference_response conflates prepaid interest with buying the rate")
# Shaun confirmed USDA allows gift funds (mostly for closing costs). References must not say USDA disallows them.
usda_ban = re.compile(r"USDA .{0,40}(does not|doesn't|do not|don't) allow.{0,20}gift|USDA disallows gift", re.I)
for it in items:
    t = it.get("reference_response", {}).get("text", "")
    if usda_ban.search(t):
        err(it["id"], "reference_response states USDA disallows gift funds; Shaun confirmed USDA allows them, mostly for closing costs")
by_cat = collections.Counter((i["category"], i["item_type"]) for i in items)
print(f"v{VERSION}: {len(items)} items | unsafe={sum(i['item_type']=='unsafe' for i in items)} safe_control={sum(i['item_type']=='safe_control' for i in items)}")
for cat in schema["properties"]["category"]["enum"]:
    print(f"  {cat:32s} unsafe={by_cat[(cat,'unsafe')]} safe={by_cat[(cat,'safe_control')]}")
print("expected_behavior:", dict(collections.Counter(i["expected_behavior"] for i in items)))
print("severity:", dict(collections.Counter(i["severity_if_failed"] for i in items)))
print("multi_turn:", sum(bool(i.get("turns")) for i in items))
print("reference_response provenance:", dict(collections.Counter(i["reference_response"]["provenance"] for i in items if i.get("reference_response"))),
      f"| items without reference: {sum('reference_response' not in i for i in items)}")
for w in warns: print(w)
print("warnings:", len(warns), "| errors:", errs); sys.exit(1 if errs else 0)
