import json
from collections import Counter

from askb_data import askb_list, tier_values, khaled_gifs, khaled_tiers

VALID_TIERS = {"S", "A", "B", "C"}

def build(urls, tiers, series):
    if len(urls) != len(tiers):
        raise SystemExit(
            f"{series}: {len(urls)} urls but {len(tiers)} tiers. Fix the lists first."
        )
    return [
        {"url": u.strip(), "tier": t.strip().upper(), "series": series}
        for u, t in zip(urls, tiers)
    ]

entries = build(askb_list, tier_values, "askb") + build(khaled_gifs, khaled_tiers, "khaled")

# sanity checks
bad = [e for e in entries if e["tier"] not in VALID_TIERS]
if bad:
    raise SystemExit(f"Unexpected tiers: {Counter(e['tier'] for e in bad)}")

seen, deduped = set(), []
for e in entries:
    if e["url"] in seen:
        print("Duplicate skipped:", e["url"])
        continue
    seen.add(e["url"])
    deduped.append(e)

for i, e in enumerate(deduped, start=1):
    e["id"] = i

with open("gifs.json", "w") as f:
    json.dump(deduped, f, indent=2)

print(Counter(e["tier"] for e in deduped), "total:", len(deduped))
