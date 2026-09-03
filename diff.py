import json
from collections import Counter


with open("data/sections-2017-01-01.json", encoding="utf-8") as f:
    sections_old = json.load(f)
with open("data/sections-2021-04-21.json", encoding="utf-8") as f:
    sections_new = json.load(f)

by_id_old = {s["identifier"]: s for s in sections_old}
by_id_new = {s["identifier"]: s for s in sections_new}

added   = by_id_new.keys() - by_id_old.keys()
removed = by_id_old.keys() - by_id_new.keys()
common  = by_id_old.keys() & by_id_new.keys()

status = {}
for identifier in sorted(common):
    old = by_id_old[identifier]
    new = by_id_new[identifier]

    if old["body"] != new["body"] or old["heading"] != new["heading"]:
        status[identifier] = {"status": "changed"}
    else:
        status[identifier] = {"status": "unchanged"}

for identifier in sorted(added):
    status[identifier] = {"status": "added"}
for identifier in sorted(removed):
    status[identifier] = {"status": "removed"}


print(Counter(v["status"] for v in status.values()))
with open("data/revision-status.json", "w", encoding="utf-8") as f:
    json.dump(status, f, indent=2, ensure_ascii=False)