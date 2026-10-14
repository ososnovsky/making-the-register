# Research brief — Event Scanner source register, culture family

You are curating entries for `sources.yaml`, the source register of a personal event-scanner app.
Project folder (READ-ONLY for you): the root of this repo

Read first:
1. `formative/IMP-event-scanner-source-taxonomy.md` — §2 categories, §5 entry schema, §6 channels and fetch rules, §8 bookables. Follow exactly.
2. `coverage.md` and `examples/coverage.md` — "Carry-over rules" (BASH, Luma, newsletters, bookables, hijacked domains, rate limits), "Leads for later families", and "Rejected sources (don't re-research)".
3. `sources.yaml` — existing entries (none yet in a fresh register; the worked example in `examples/sources.yaml` shows the style). Match their style (notes wording, `Address source:`, "Dates in HTML"). Never duplicate an existing source: if a place already exists (e.g. under restaurants), report it as "already in register" and suggest any extra links/bookables for it instead.

Do NOT edit anything in the project folder. Write only to your output files (paths given in your task).

## Scan areas
`bratislava` only: the whole municipality, all 17 boroughs (Staré Mesto, Ružinov, Vrakuňa, Podunajské Biskupice, Nové Mesto, Rača, Vajnory, Karlova Ves, Dúbravka, Lamač, Devín, Devínska Nová Ves, Záhorská Bystrica, Petržalka, Jarovce, Rusovce, Čunovo). NOT places outside the municipality (e.g. Stupava, Senec, Pezinok). Culture categories and all other categories are in scope.

## Category boundaries (one per entry)
- `theatres-cinemas`: venues whose programme is mainly theatre, cabaret, comedy, dance performance, or film; comedy clubs; cinemas (incl. chains like Pathé, one entry per cinema); film festivals.
- `event-venues`: concert halls, pop venues, multi-purpose and expo halls (main activity = hosting events of mixed kinds).
- `museums`: museums. `culture-other`: galleries, art spaces, creative studios, dance schools, immersive/experience venues.
- `aggregators`: a listing platform or city agenda that lists other organisers' events.
Borderline cases: pick per the rule, and flag in your report.

## Verification rules (strict)
- Never invent a URL or address. Record only what you fetched and checked.
- Check every link with curl (`curl -sL -o /dev/null -w "%{http_code} %{url_effective}" -A "Mozilla/5.0 (EventScanner register curation; contact dsosnovsky@gmail.com)" URL`, and fetch the body to confirm events/dates are present). Space requests to any one domain (≥2 s apart); DJGuide blocks fast clients.
- Check each page's `<title>`: a domain now serving gambling/casino/parking/for-sale content is never recorded (note it in the report).
- Plain fetch first. If a page needs rendering (shell only, no events in HTML), use the headless browser helper the lead curator names in your task, if any; otherwise record the entry with `reading_hint: browser` and say in `notes` "events not in plain HTML; browser check pending". Sites that block headless browsers go to `local-browser-checks.md` via the lead curator.
- Never open Instagram or Facebook. You may record an IG/FB URL as a reference-only link only if the source's own site links to it.
- Before an entry would be `unfetchable`, look for alternative channels (website, link-in-bio, Luma, Meetup, Eventbrite, Telegram).
- Do NOT geocode (no Nominatim). For fixed venues write the full street address and leave coords as `coords: TODO`. The lead curator geocodes centrally.
- For every source: look for a newsletter signup (add `channel: newsletter` link + `newsletter_subscribed: false`; public archive → separate `website` link). Look for bookables per §8 (group workshops, tours on request, backstage tours, private screenings — NOT tickets, table reservations, or corporate hire).
- BASH (bash.social) is dropped as a channel: don't look for BASH pages.
- Kids-only is out (owner, 2026-10-03): don't record sources aimed only at children or families with children, nor kids-only bookables (children's parties, kids' workshops, school programmes). Mixed venues stay.
- Adult-only is a normal type (owner, 2026-10-03): include 18+ sources when they come up and note "18+" in `notes`; no separate 18+ searches. Paid sexual services are not events or bookables.
- Men-only and LGBTQ+-centred are out (owner, 2026-10-04): don't record sources, events, or bookables that are men-only or primarily based on queer, drag, or LGBTQ+ identity or culture (queer clubs and bars, drag shows, ballroom/kiki nights, LGBTQ+ festivals, Pride). Mixed venues stay.
- Walk-in activities separate from ordinary admission (e.g. a church-tower climb) also count as bookables (owner, 2026-10-03); ordinary museum/venue admission does not.
- Bookables are a priority (owner, 2026-10-03): for every source, find group/private tours, workshops on request, tastings, with price, group size, and how to book. Don't leave "details not checked".
- Anything unverified → `notes` as an open item. Never fill gaps silently.
- Web-search budget: at most the number of searches given in your task. Prefer systematic directories over open searches.

## Sweep depth (owner rule): proper, exhaustive, lean to inclusion
1. Owner-named places (given in your task).
2. Systematic lists: find the Slovak/Bratislava equivalents of a city culture agenda with venue directories, a cinema listing site, concert and theatre listing sites, and theatre-sector directories; Wikipedia lists of theatres/cinemas in Bratislava (sk and en) (as a discovery aid only — verify each venue's own site).
3. Open searches (in Slovak and English) per borough or area.
No count targets. Include small venues (fringe theatres, comedy rooms, filmhuizen, student theatres open to the public).

## Output
1. `<prefix>-entries.yaml`: a YAML list of entries in §5 schema (same field order and style as sources.yaml; use `>-` folded notes). Group by borough with comment headers. Every note ends with `Address source: <site>.` for venues. Note the check date (2026-10-01) only if it differs.
2. `<prefix>-report.md` with:
   - Sources covered for discovery and how completely (e.g. "<cinema listing site> Bratislava cinema list: all 20 checked").
   - Rejected candidates table (source, city, reason) — closed, no events, hijacked, out of area, duplicate.
   - Open items (browser checks pending, BASH candidates, unclear category).
   - Leads for other families/categories (museums, event-venues, culture-other, and anything for non-culture families), with URL if verified.
   - Already-in-register places, with suggested extra links/bookables.
Return a short summary (counts per city, top open items) as your final message.

## Museums addendum (checkpoint 2)
- Category `museums`, default `social_default: false`. Include every museum open to the public with any events, exhibitions agenda, late openings, talks, tours or workshops — large and small (house museums, university museums, castles that operate as museums, science centres). Lean to inclusion.
- Best link: the museum's activities/agenda page (Slovak: "program", "podujatia", "kalendár", "aktuálne"; English: "what's on", "events"), not the exhibitions overview, unless that's all there is. Record both if both carry dates.
- Bookables (§8) are common here: guided tours on request for groups (Slovak: e.g. "prehliadka na objednávku", "skupinová prehliadka"; English: "guided tour on request"), private tours, workshops for groups. Record them with link and price/group size if stated. Ticketed public tours on fixed dates are events, not bookables.
- Systematic sources: find the Slovak/Bratislava equivalents of a national museum directory, the city culture agenda's museum list, Wikipedia lists of museums in Bratislava (discovery only), and the Museum Night / Night of Museums and Galleries organisers (an organiser entry — category museums, no venue).
- Already in sources.yaml: check before adding (e.g. a museum that is already a cinema or venue entry; mention it, don't duplicate — suggest extra links instead).
