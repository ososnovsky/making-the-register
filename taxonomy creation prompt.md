Plain curation session — NOT a pipeline run (don't trigger any Idea, Research, or Development Pipeline skill).

Goal: build the source register `sources.yaml` for my Event Scanner app in this folder, following `IMP-event-scanner-source-taxonomy.md` (in this folder) exactly: source categories (§2), entry schema (§5), channel types and fetch rules (§6), and coverage gate (§7). Scan areas: Rotterdam (including Schiedam), The Hague (including Rijswijk), and Delft.

Work one category family at a time, in the §2 order (aggregators first). For each family:
1. Ask me which places I already know.
2. Search for more.
3. Verify every entry (rules below).
4. Checkpoint: show me the family's entries and wait for my approval before moving on.

Verification rules:
- Never invent a URL, address, or coordinate. Only record what you've actually found and checked.
- Check that every link resolves; script it with curl where possible. Use Chrome only when a page needs rendering or a plain fetch is blocked.
- Never open Instagram or Facebook in Chrome unless I explicitly say so.
- Record the right `channel` and `fetch_status`. Before marking an entry unfetchable, look for alternative channels (website, link-in-bio target, Luma, Meetup, Eventbrite, Telegram).
- Coordinates for fixed venues come from OpenStreetMap Nominatim: at most 1 request per second, with an identifying User-Agent. Never estimate them.
- Anything you couldn't verify goes in `notes` as an open item. Never fill gaps silently.

Keep these files up to date after each approved family:
- `sources.yaml`: the cumulative register.
- `coverage.md`: the §7 table, 20 categories × 3 scan areas, each cell showing the entry count, "none found", or "n/a".
- A small validation script that checks `sources.yaml` against §5 (required fields, allowed values, unique ids). Run it before every checkpoint.

All progress lives in these files, so we can stop after any family and resume in a new session.

Deliverables at the end:
- the complete `sources.yaml`
- the final `coverage.md`
- a list of unverified or unfetchable entries