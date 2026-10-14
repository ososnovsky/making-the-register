"""Build entries from compact candidate files.
Usage: python build.py cand/<category>.txt  -> cand/<category>.yaml  (coords: TODO for venues)
Line format (blank lines and # comments ignored), fields separated by ' | ':
 id | name | links | address | social | hint | notes | bookables
 links: 'url@a ; url@n~note ; ...'  codes: a website-agenda, w website, g aggregator-page, t ticketing,
        n newsletter, p pdf, h link-hub, tg telegram, o other (needs ~note), i instagram, f facebook
 social: 1 / 0 / - (category default)    hint: fetch|browser|pdf|image|-
 bookables: 'name ~ link ~ evcat ~ note [~ address] ;; ...'  evcat codes mn ss ex tl np sc sp fd mf ga ot
 A line starting with '## <name>' sets a comment header for the following entries."""
import re, sys, textwrap
from pathlib import Path

CH = {"a": "website-agenda", "w": "website", "g": "aggregator-page", "t": "ticketing", "n": "newsletter",
      "p": "pdf", "h": "link-hub", "tg": "telegram", "o": "other", "i": "instagram", "f": "facebook"}
EV = {"mn": "music-nightlife", "ss": "stage-screen", "ex": "exhibitions", "tl": "talks-learning",
      "np": "networking-professional", "sc": "social-community", "sp": "sport", "fd": "food-drink",
      "mf": "markets-festivals", "ga": "games-activities", "ot": "other"}
SOC_ON = {"bars-cafes", "clubs", "sports-clubs", "networking", "industry", "coworking-hubs",
          "community-groups", "diaspora-expat"}

def q(s):
    s = s.strip()
    if re.search(r"^[\s\-?:,\[\]{}#&*!|>'\"%@`]|: | #|[:#]$", s):
        return "'" + s.replace("'", "''") + "'"
    return s

def folded(text, indent):
    lines = textwrap.wrap(text.strip(), 96 - indent)
    return "\n".join(" " * indent + l for l in lines)

def build(src):
    cat = Path(src).stem
    out = []
    for raw in Path(src).read_text(encoding="utf-8").splitlines():
        raw = raw.rstrip()
        if not raw.strip() or raw.startswith("# "): continue
        if raw.startswith("##"):
            out.append(f"\n# {raw.lstrip('# ').strip()}\n"); continue
        f = [x.strip() for x in re.split(r" \|(?= |$)", raw)]
        f += [""] * (8 - len(f))
        eid, name, links, addr, soc, hint, notes, book = f[:8]
        L = ["- id: " + eid, "  name: " + q(name), "  source_category: " + cat, "  city: bratislava", "  links:"]
        chans = []
        for part in links.split(" ; "):
            m = re.match(r"(\S+)@(\w+)(?:~(.*))?$", part.strip())
            assert m, f"{eid}: bad link {part!r}"
            url, code, note = m.groups()
            ch = CH[code]; chans.append(ch)
            L += [f"    - url: {url}", f"      channel: {ch}"]
            if note:
                L += ["      note: >-", folded(note, 8)]
        sub = "newsletter" in chans
        fetchable = any(c not in ("instagram", "facebook", "newsletter") for c in chans)
        vb = addr.startswith("VB:")
        if vb: addr = addr[3:].strip()
        if addr:
            L += ["  venue:", "    address: " + q(addr), "    coords: TODO"]
        default = cat in SOC_ON
        s = default if soc in ("", "-") else soc == "1"
        L.append(f"  social_default: {'true' if s else 'false'}")
        L.append(f"  fetch_status: {'ok' if fetchable else 'unfetchable'}")
        if hint and hint != "-": L.append("  reading_hint: " + hint)
        if sub: L.append("  newsletter_subscribed: false")
        if book:
            L.append("  bookables:")
            for b in book.split(" ;; "):
                p = [x.strip() for x in b.split(" ~ ")]
                assert len(p) >= 3, f"{eid}: bad bookable {b!r}"
                L += ["    - name: " + q(p[0]), "      link: " + p[1], "      event_category: " + EV[p[2]]]
                if len(p) > 3 and p[3]: L += ["      note: >-", folded(p[3], 8)]
                if len(p) > 4 and p[4]: L.append("      address: " + q(p[4]))
        if addr.startswith("OSM:"):
            notes = (notes + " " if notes else "") + "Address source: OpenStreetMap (Nominatim)."
        elif vb:
            notes = (notes + " " if notes else "") + "Address source: Visit Bratislava place page."
        elif addr:
            notes = (notes + " " if notes else "") + "Address source: own site."
        if notes:
            L += ["  notes: >-", folded(notes, 4)]
        out.append("\n".join(L))
    dst = Path(src).with_suffix(".yaml")
    dst.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{dst}: {sum(1 for o in out if o.startswith('- id'))} entries")

if __name__ == "__main__":
    for s in sys.argv[1:]: build(s)
