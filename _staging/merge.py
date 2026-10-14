"""python merge.py : assemble ../sources.yaml from cand/<category>.geo.yaml in taxonomy order (fixes MISSING coords)."""
import re
import textwrap
from pathlib import Path

import yaml

here = Path(__file__).resolve().parent
ORDER = ["aggregators", "restaurants", "bars-cafes", "clubs", "theatres-cinemas", "museums", "event-venues",
         "culture-other", "sports-clubs", "sports-venues", "parks", "networking", "industry", "coworking-hubs",
         "universities", "community-groups", "diaspora-expat", "libraries-community-centres", "markets-festivals",
         "municipality", "activities"]


def add_bookable_address(b, addr):
    """After a venue is dropped, give every bookable without an address the entry's address."""
    lines = b.split("\n")
    if "  bookables:" not in lines:
        return b
    i0 = lines.index("  bookables:")
    j = i0 + 1
    while j < len(lines) and (lines[j].startswith("    ") or lines[j] == ""):
        j += 1
    seg = lines[i0 + 1:j]
    new, cur = [], []
    for ln in seg + ["    - name: __end__"]:
        if ln.startswith("    - name:"):
            if cur:
                if not any(c.startswith("      address:") for c in cur):
                    k = len(cur)
                    while k and cur[k - 1] == "":
                        k -= 1
                    cur = cur[:k] + ["      address: '" + addr.replace("'", "''") + "'"] + cur[k:]
                new += cur
            cur = [ln]
        else:
            cur.append(ln)
    lines[i0 + 1:j] = new
    return "\n".join(lines)


def fix(text):
    blocks = re.split(r"(?m)^(?=- id: |\n# )", text)
    out = []
    for b in blocks:
        if "coords: MISSING" in b:
            m = re.search(r"  venue:\n    address: (.*)\n    coords: MISSING\n", b)
            addr = m.group(1).strip("'")
            b = b.replace(m.group(0), "")
            b = add_bookable_address(b, addr)
            add = f"Open item: no OpenStreetMap match for the address '{addr}', so no coordinates; geocode by hand."
            lines = ["    " + ln for ln in textwrap.wrap(add, 92)]
            if "\n  notes: >-\n" in b:
                b = b.rstrip("\n") + "\n" + "\n".join(lines) + "\n"
            else:
                b = b.rstrip("\n") + "\n  notes: >-\n" + "\n".join(lines) + "\n"
        out.append(b)
    return "".join(out)


parts, n = [], 0
for cat in ORDER:
    f = here / "cand" / f"{cat}.geo.yaml"
    if not f.exists():
        continue
    t = fix(f.read_text(encoding="utf-8"))
    n += len(yaml.safe_load(t) or [])
    parts.append(f"# ---------------------------------------------------------------- {cat}\n" + t.lstrip("\n"))
head = ("# Event Scanner source register: Bratislava (the whole municipality, 17 boroughs).\n"
        "# Schema: formative/IMP-event-scanner-source-taxonomy.md §5–§6. Validate with: python validate_sources.py\n"
        "# Kids-only, men-only and LGBTQ+-centred sources are excluded; adult-only (18+) sources are in scope.\n"
        "# Link checks: plain fetch (curl-style) on 2026-10-13 unless a note says otherwise.\n\n")
(here.parent / "sources.yaml").write_text(head + "\n".join(parts) if parts else head + "[]\n", encoding="utf-8")
print("assembled", n, "entries from", len(parts), "categories")
