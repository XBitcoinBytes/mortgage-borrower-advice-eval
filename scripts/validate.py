"""Validate items against schema.json, check pair integrity, print counts."""
import json, pathlib, collections, sys
from jsonschema import Draft202012Validator
root = pathlib.Path(__file__).resolve().parent.parent
schema = json.loads((root / "schema.json").read_text())
v = Draft202012Validator(schema)
items = [json.loads(l) for l in (root / "items" / "v0.jsonl").read_text().splitlines() if l.strip()]
errs = 0
ids = {i["id"]: i for i in items}
assert len(ids) == len(items), "duplicate ids"
for it in items:
    for e in v.iter_errors(it):
        errs += 1; print(it["id"], "SCHEMA:", e.message)
    p = it.get("safe_pair_id")
    if p:
        if p not in ids: errs += 1; print(it["id"], "pair missing", p)
        elif it.get("pair_type") == "safe_unsafe" and ids[p]["item_type"] == it["item_type"]:
            errs += 1; print(it["id"], "safe_unsafe pair has same item_type")
    if not any(r["points"] > 0 for r in it["rubrics"]): errs += 1; print(it["id"], "no positive criteria")
by_cat = collections.Counter((i["category"], i["item_type"]) for i in items)
print(f"{len(items)} items | unsafe={sum(i['item_type']=='unsafe' for i in items)} safe_control={sum(i['item_type']=='safe_control' for i in items)}")
for cat in schema["properties"]["category"]["enum"]:
    print(f"  {cat:32s} unsafe={by_cat[(cat,'unsafe')]} safe={by_cat[(cat,'safe_control')]}")
print("expected_behavior:", dict(collections.Counter(i["expected_behavior"] for i in items)))
print("severity:", dict(collections.Counter(i["severity_if_failed"] for i in items)))
print("errors:", errs); sys.exit(1 if errs else 0)
