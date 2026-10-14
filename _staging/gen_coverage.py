"""python gen_coverage.py -> writes ../coverage.md from ../sources.yaml and coverage_static.md (hand-written sections)."""
from collections import Counter
from pathlib import Path

import yaml

here = Path(__file__).resolve().parent
root = here.parent
CATS = ["aggregators", "restaurants", "bars-cafes", "clubs", "theatres-cinemas", "museums", "event-venues",
        "culture-other", "sports-clubs", "sports-venues", "parks", "networking", "industry", "coworking-hubs",
        "universities", "community-groups", "diaspora-expat", "libraries-community-centres", "markets-festivals",
        "municipality", "activities"]
entries = yaml.safe_load((root / "sources.yaml").read_text(encoding="utf-8")) or []
cnt = Counter(e["source_category"] for e in entries)
rows = []
for i, c in enumerate(CATS, 1):
    rows.append(f"| {i} | `{c}` | {cnt[c] if cnt[c] else 'none found'} |")
rows.append(f"| | **Total** | **{len(entries)}** |")

nocoords = [e["id"] for e in entries if "venue" not in e and any("Open item: no OpenStreetMap" in (e.get("notes") or "") for _ in [0])]
browser = [e["id"] for e in entries if e.get("reading_hint") == "browser"]
unfetch = [e["id"] for e in entries if e["fetch_status"] == "unfetchable"]
news = sum(1 for e in entries for l in e["links"] if l["channel"] == "newsletter")
book = sum(len(e.get("bookables") or []) for e in entries)

static = (here / "coverage_static.md").read_text(encoding="utf-8")
out = f"""# Coverage — Event Scanner source register (Bratislava)

§7 coverage gate: 21 source categories × 1 scan area (Bratislava, the whole municipality, 17 boroughs). Each cell shows the entry count or "none found". Counts come from `python validate_sources.py`; this file is regenerated from `sources.yaml` by `_staging/gen_coverage.py` (the hand-written sections come from `_staging/coverage_static.md`).

Register status (2026-10-13): first full pass of all 21 categories, built in one unattended curation session; **not yet reviewed by the owner**. {len(entries)} entries, {news} newsletter links (all `newsletter_subscribed: false`), {book} bookables.

| # | Source category | Bratislava |
|---|---|---:|
""" + "\n".join(rows) + f"""

## Open items (generated)

- Entries without coordinates (no OpenStreetMap house-level or named match; marked "Open item" in `notes`): {", ".join(f"`{x}`" for x in nocoords) or "none"}.
- Entries with `reading_hint: browser` (events render client-side, or the site blocks plain fetches): {", ".join(f"`{x}`" for x in browser) or "none"}.
- Entries with `fetch_status: unfetchable`: {", ".join(f"`{x}`" for x in unfetch) or "none"}.

""" + static
(root / "coverage.md").write_text(out, encoding="utf-8")
print("coverage.md written:", len(entries), "entries")
