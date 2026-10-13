"""Validate sources.yaml against the register schema (taxonomy doc §5 and §6).

Usage: python validate_sources.py [path]   (default: sources.yaml next to this script)
Exit code 0 = valid, 1 = errors. Also prints entry counts per source category x city (for
coverage.md) and, when valid, regenerates newsletters.md and bookables.md next to the register.
"""
import re
import sys
from pathlib import Path

import yaml

SOURCE_CATEGORIES = [
    "aggregators", "restaurants", "bars-cafes", "clubs", "theatres-cinemas", "museums",
    "event-venues", "culture-other", "sports-clubs", "sports-venues", "parks", "networking",
    "industry", "coworking-hubs", "universities", "community-groups", "diaspora-expat",
    "libraries-community-centres", "markets-festivals", "municipality", "activities",
]
CITIES = ["rotterdam", "the-hague", "delft", "leiden", "amsterdam", "utrecht"]
# Culture-only scan areas (taxonomy §5): allowed only with these source categories (aggregators
# only when they list culture, which the validator can't check).
CULTURE_ONLY_CITIES = {"leiden", "amsterdam", "utrecht"}
CULTURE_CATEGORIES = {"aggregators", "theatres-cinemas", "museums", "event-venues", "culture-other"}
CHANNELS = {
    "website-agenda", "website", "aggregator-page", "ticketing", "telegram",
    "link-hub", "pdf", "instagram", "facebook", "newsletter", "other",
}
NEVER_FETCHED = {"instagram", "facebook"}
FETCH_STATUSES = {"ok", "unfetchable"}
READING_HINTS = {"fetch", "browser", "pdf", "image"}
EVENT_CATEGORIES = {
    "music-nightlife", "stage-screen", "exhibitions", "talks-learning", "networking-professional",
    "social-community", "sport", "food-drink", "markets-festivals", "games-activities", "other",
}

REQUIRED = {"id", "name", "source_category", "city", "links", "social_default", "fetch_status"}
OPTIONAL = {"venue", "reading_hint", "notes", "newsletter_subscribed", "bookables"}
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# Sanity box around the six scan areas; catches swapped lat/lng, not a geocode.
LAT_RANGE, LNG_RANGE = (51.8, 52.45), (4.0, 5.25)


def validate(entries):
    errors = []
    seen = set()
    for i, e in enumerate(entries):
        where = f"entry {i}"
        if not isinstance(e, dict):
            errors.append(f"{where}: not a mapping")
            continue
        where = f"entry {i} ({e.get('id', '?')})"

        for f in sorted(REQUIRED - e.keys()):
            errors.append(f"{where}: missing required field '{f}'")
        for f in sorted(e.keys() - REQUIRED - OPTIONAL):
            errors.append(f"{where}: unknown field '{f}'")

        eid = e.get("id")
        if eid is not None:
            if not isinstance(eid, str) or not SLUG.match(eid):
                errors.append(f"{where}: id is not a lowercase slug")
            elif eid in seen:
                errors.append(f"{where}: duplicate id")
            else:
                seen.add(eid)

        if "name" in e and not (isinstance(e["name"], str) and e["name"].strip()):
            errors.append(f"{where}: name must be non-empty text")
        if "source_category" in e and e["source_category"] not in SOURCE_CATEGORIES:
            errors.append(f"{where}: invalid source_category '{e['source_category']}'")
        if "city" in e and e["city"] not in CITIES:
            errors.append(f"{where}: invalid city '{e['city']}'")
        elif e.get("city") in CULTURE_ONLY_CITIES and e.get("source_category") not in CULTURE_CATEGORIES:
            errors.append(f"{where}: city '{e['city']}' is culture-only; '{e.get('source_category')}' not allowed")
        if "social_default" in e and not isinstance(e["social_default"], bool):
            errors.append(f"{where}: social_default must be true/false")
        if "fetch_status" in e and e["fetch_status"] not in FETCH_STATUSES:
            errors.append(f"{where}: invalid fetch_status '{e['fetch_status']}'")
        if "reading_hint" in e and e["reading_hint"] not in READING_HINTS:
            errors.append(f"{where}: invalid reading_hint '{e['reading_hint']}'")
        if "notes" in e and not isinstance(e["notes"], str):
            errors.append(f"{where}: notes must be text")

        links = e.get("links")
        channels = []
        if "links" in e:
            if not isinstance(links, list) or not links:
                errors.append(f"{where}: links must be a non-empty list")
                links = []
            for j, link in enumerate(links):
                lw = f"{where} link {j}"
                if not isinstance(link, dict):
                    errors.append(f"{lw}: not a mapping")
                    continue
                for f in sorted(link.keys() - {"url", "channel", "note"}):
                    errors.append(f"{lw}: unknown field '{f}'")
                url = link.get("url")
                if not (isinstance(url, str) and re.match(r"^https?://\S+$", url)):
                    errors.append(f"{lw}: url missing or not http(s)")
                ch = link.get("channel")
                if ch not in CHANNELS:
                    errors.append(f"{lw}: invalid channel '{ch}'")
                else:
                    channels.append(ch)
                if ch == "other" and not link.get("note"):
                    errors.append(f"{lw}: channel 'other' needs a note")
                if "note" in link and not isinstance(link["note"], str):
                    errors.append(f"{lw}: note must be text")

        subscribed = e.get("newsletter_subscribed")
        if "newsletter" in channels:
            if not isinstance(subscribed, bool):
                errors.append(f"{where}: has a newsletter link, needs newsletter_subscribed true/false")
        elif "newsletter_subscribed" in e:
            errors.append(f"{where}: newsletter_subscribed without a newsletter link")

        # §5/§6: unfetchable exactly when no link is fetchable; a newsletter counts once subscribed.
        status = e.get("fetch_status")
        if channels and len(channels) == len(links or []) and "other" not in channels:
            fetchable = any(c not in NEVER_FETCHED and (c != "newsletter" or subscribed is True)
                            for c in channels)
            if not fetchable and status != "unfetchable":
                errors.append(f"{where}: no fetchable link, must be 'unfetchable'")
            if fetchable and status == "unfetchable":
                errors.append(f"{where}: has a fetchable link, must not be 'unfetchable'")

        if "bookables" in e:
            bk = e["bookables"]
            if not isinstance(bk, list) or not bk:
                errors.append(f"{where}: bookables must be a non-empty list")
                bk = []
            for j, b in enumerate(bk):
                bw = f"{where} bookable {j}"
                if not isinstance(b, dict):
                    errors.append(f"{bw}: not a mapping")
                    continue
                for f in sorted({"name", "link", "event_category"} - b.keys()):
                    errors.append(f"{bw}: missing required field '{f}'")
                for f in sorted(b.keys() - {"name", "link", "event_category", "social", "address", "note"}):
                    errors.append(f"{bw}: unknown field '{f}'")
                if "link" in b and not (isinstance(b["link"], str) and re.match(r"^https?://\S+$", b["link"])):
                    errors.append(f"{bw}: link not http(s)")
                if "event_category" in b and b["event_category"] not in EVENT_CATEGORIES:
                    errors.append(f"{bw}: invalid event_category '{b['event_category']}'")
                if "social" in b and not isinstance(b["social"], bool):
                    errors.append(f"{bw}: social must be true/false")
                if "venue" not in e and not b.get("address"):
                    errors.append(f"{bw}: entry has no venue, so the bookable needs an address")

        if "venue" in e:
            v = e["venue"]
            if not isinstance(v, dict):
                errors.append(f"{where}: venue must be a mapping")
            else:
                for f in sorted(v.keys() - {"address", "coords"}):
                    errors.append(f"{where}: unknown venue field '{f}'")
                if not (isinstance(v.get("address"), str) and v["address"].strip()):
                    errors.append(f"{where}: venue.address missing")
                c = v.get("coords")
                if not (isinstance(c, list) and len(c) == 2
                        and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in c)):
                    errors.append(f"{where}: venue.coords must be [lat, lng]")
                elif not (LAT_RANGE[0] <= c[0] <= LAT_RANGE[1] and LNG_RANGE[0] <= c[1] <= LNG_RANGE[1]):
                    errors.append(f"{where}: venue.coords {c} outside scan-area box (swapped?)")
    return errors


def counts(entries):
    table = {cat: {city: 0 for city in CITIES} for cat in SOURCE_CATEGORIES}
    for e in entries:
        if isinstance(e, dict) and e.get("source_category") in table and e.get("city") in CITIES:
            table[e["source_category"]][e["city"]] += 1
    return table


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("sources.yaml")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    entries = data if data is not None else []
    if not isinstance(entries, list):
        print("ERROR: top level must be a list of entries")
        return 1

    errors = validate(entries)
    for err in errors:
        print(f"ERROR: {err}")

    table = counts(entries)
    print(f"\n{len(entries)} entries. Counts ({' / '.join(CITIES)}):")
    for cat, row in table.items():
        if any(row.values()):
            print(f"  {cat:30}" + "".join(f" {row[c]:3}" for c in CITIES))
    if not errors:
        n_news, n_book = write_lists(entries, path.parent)
        print(f"\nWrote newsletters.md ({n_news}) and bookables.md ({n_book}).")
    print("VALID" if not errors else f"INVALID: {len(errors)} error(s)")
    return 1 if errors else 0


def cell(text):
    return str(text or "").replace("|", "\\|").replace("\n", " ")


def write_lists(entries, folder):
    """Regenerate newsletters.md and bookables.md from the register (single source of truth)."""
    header = "<!-- Generated by validate_sources.py from sources.yaml. Do not edit; edit sources.yaml. -->\n\n"
    news = []
    for e in entries:
        for link in e.get("links") or []:
            if link.get("channel") == "newsletter":
                news.append((e, link))
    todo = [x for x in news if not x[0].get("newsletter_subscribed")]
    lines = [header + "# Newsletters\n",
             f"{len(news)} newsletters, {len(todo)} still to subscribe. After subscribing, label the mails "
             "`Newsletters` and set `newsletter_subscribed: true` on the entry in `sources.yaml` "
             "(plus `fetch_status: ok` if the newsletter is its only fetchable link).\n",
             "| Subscribed | Source | City | Signup page | Note |", "|---|---|---|---|---|"]
    for e, link in sorted(news, key=lambda x: (bool(x[0].get("newsletter_subscribed")), x[0]["city"], x[0]["name"])):
        lines.append(f"| {'yes' if e.get('newsletter_subscribed') else '**no**'} | {cell(e['name'])} | {e['city']} "
                     f"| {link['url']} | {cell(link.get('note'))} |")
    (folder / "newsletters.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    book = [(e, b) for e in entries for b in e.get("bookables") or []]
    lines = [header + "# Bookables\n",
             f"{len(book)} activities you can arrange on request or by appointment (taxonomy §8).\n",
             "| Activity | Place | City | Category | Where | Note | Book / info |", "|---|---|---|---|---|---|---|"]
    for e, b in sorted(book, key=lambda x: (x[0]["city"], x[1]["event_category"], x[0]["name"])):
        where = b.get("address") or (e.get("venue") or {}).get("address", "")
        lines.append(f"| {cell(b['name'])} | {cell(e['name'])} | {e['city']} | {b['event_category']} "
                     f"| {cell(where)} | {cell(b.get('note'))} | {b['link']} |")
    (folder / "bookables.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(news), len(book)


if __name__ == "__main__":
    sys.exit(main())
