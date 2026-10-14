"""python patch.py patches.tsv   lines: id<TAB>field<TAB>value
field: hint | soc | addr | notes+ (append to notes) | name
Edits the compact candidate lines in cand/*.txt."""
import glob
import re
import sys

IDX = {"name": 1, "links": 2, "addr": 3, "soc": 4, "hint": 5, "notes": 6, "notes+": 6, "book": 7}
patches = {}
for ln in open(sys.argv[1], encoding="utf-8"):
    if not ln.strip() or ln.startswith("#"):
        continue
    p = ln.rstrip("\n").split("\t")
    patches.setdefault(p[0], []).append((p[1], p[2]))
done = set()
for f in glob.glob("cand/*.txt"):
    L = open(f, encoding="utf-8").read().split("\n")
    changed = False
    for i, ln in enumerate(L):
        eid = ln.split(" |")[0]
        if eid not in patches:
            continue
        parts = [x.strip() for x in re.split(r" \|(?= |$)", ln)]
        while len(parts) < 8:
            parts.append("")
        for field, val in patches[eid]:
            k = IDX[field]
            if field == "notes+":
                parts[k] = (parts[k] + " " + val).strip()
            else:
                parts[k] = val
        L[i] = " | ".join(parts[:7]) + " | " + parts[7] if parts[7] else " | ".join(parts[:7]) + " |"
        done.add(eid)
        changed = True
    if changed:
        open(f, "w", encoding="utf-8").write("\n".join(L))
print("patched", len(done), "missing", set(patches) - done)
