## How this pass was built

- **No owner checkpoints:** the owner asked for all 21 categories to be built in one run and validated at the end, so no family was approved yet and no "what do you know" questions were asked. Judgement calls are listed below and in each entry's `notes`.
- **Discovery sources** (systematic first, then open searches): the Visit Bratislava places directory and services directory (tours, tastings, boat and water-sport operators), GoOut venue and city pages (venue lists with addresses), OpenStreetMap via Overpass (theatres, cinemas, museums, galleries, community centres, libraries, sports and activity venues, coworking), Wikidata, the borough and city websites, Meetup city pages, and targeted web searches in Slovak and English.
- **Verification:** every link was fetched on 2026-10-13 (plain fetch, with curl as a fallback; `_staging/verify.py`). Dead domains, parked or for-sale pages and gambling takeovers were dropped (see the rejected table). RA, Astorka and Hlava 22 block plain fetches (403/429) and were kept; RA renders in Chrome (15 upcoming events checked on 2026-10-13).
- **Addresses and coordinates:** addresses come from the source's own site where `notes` says "own site", otherwise from the Visit Bratislava place page or from OpenStreetMap, and the note says which. Coordinates are from OpenStreetMap Nominatim (house-number match, or the venue's own named OSM object on the same street). Where neither matched, `venue` is omitted and the entry carries an "Open item" note; nothing was estimated.
- **Tooling** (kept in `_staging/`): `build.py` (compact candidate lines to schema YAML), `geocode.py`, `verify.py`, `merge.py`, `nl_pass.py` (newsletter links), `gen_coverage.py`; candidate lines live in `_staging/cand/`.

## Carry-over rules (from the example register, adapted)

- Sweep depth: lean to inclusion; the owner prefers removing entries later over missing them.
- Hijacked or parked domains are never recorded (gambling, casino, parking, for-sale pages).
- Own site beats directories for addresses.
- Hidden prices stay as "price in the booking flow".
- Kids-only, men-only and LGBTQ+-centred sources are out; adult-only (18+) is in. Mixed venues stay.
- BASH is not used; Luma has no usable Bratislava city page (the `luma.com/bratislava` calendar is empty).
- Newsletters: every signup page found by `nl_pass.py` is recorded with `newsletter_subscribed: false`; `newsletters.md` lists them.
- Bookables: tours, tastings, workshops and escape rooms recorded where a page showed them; many have "price in the booking flow".

## Judgement calls made without the owner

- **Tour and tasting operators with no venue** (from the Visit Bratislava services directory) are recorded as `culture-other` (guided tours), `restaurants` (tastings), or `activities` (boats, water sports); their bookables carry a "meeting point on booking" address.
- **Borough sites** are `municipality` entries (all 17 boroughs, plus the city and STaRZ); Karlova Ves is missing because its website did not resolve.
- **Professional match calendars** (Slovan football, hockey, basketball) are `sports-clubs`; stadiums and halls are `sports-venues`.
- **P*AKT** hosts an LGBTQ+-centred series (Drama Queer); the venue stays (mixed), the scanner skips those events. **Red Cat Cabaret** is an erotic cabaret and is recorded as 18+.
- **Cinema City** is two entries (Aupark, Eurovea); the third site (VIVO!) was not recorded because its address was not checked.
- **Ukrainian community:** UKC, SME SPOLU (Ukrainian-Slovak house, Ovručská 5) and ADRA's community centre are `diaspora-expat`; their events carry the likely-Ukrainian flag at scan time.
- **Meetup groups** are `aggregator-page` links with `reading_hint: browser` (Meetup pages need rendering).

## Rejected sources (don't re-research)

| Source | Why | Date |
|---|---|---|
| Baracuda (baracuda.sk) | domain now a Thai-massage site | 2026-10-13 |
| prezilsompeklo.sk, tripland.sk | title shows an online casino | 2026-10-13 |
| bratislavskygasparko.sk, dom kultúry Ružinov (OSM website) | casino pages on the domain; kids-only in the first case | 2026-10-13 |
| dsihk.sk, hotdock.sk, impacthub.sk | for sale or not resolving | 2026-10-13 |
| rubixlab.com | redirects to a gambling site | 2026-10-13 |
| fuga.forumabsurdum.sk, theroom.sk, undeadarena.com, mojaradost.sk | hosting placeholder pages (Fuga is recorded via GoOut; Radosť via GoOut) | 2026-10-13 |
| crimecase.sk, ripbunker.sk, escapezone.sk, x-quests.sk, marsarena.sk, paintballzahorska.sk | domains do not resolve | 2026-10-13 |
| asylum.sk, puzzler.sk | connection refused / invalid certificate | 2026-10-13 |
| cunovo.sk | domain for sale (the borough site is cunovo.eu) | 2026-10-13 |
| prasnabasta.sk | redirects to a parked page | 2026-10-13 |
| luma.com/bratislava | calendar "test" with no events | 2026-10-13 |
| inyourpocket.com events page | "0 events" | 2026-10-13 |
| fienta.com | no Bratislava filter found | 2026-10-13 |
| ESN Slovakia | national organisation seated in Banská Bystrica, no Bratislava agenda | 2026-10-13 |
| Bratislavské bábkové divadlo, Rozprávkový Gašparko, BIBIANA, LeavingRoom, Rodinné centrum Ráčik, Family Garden, Istra Centrum | kids-only or family-only | 2026-10-13 |
| Apollon Gay Club, Pride, Drama Queer (as a source) | LGBTQ+-centred | 2026-10-13 |
| SODA Gallery, Foajé cinema | parked or spam redirect | 2026-10-13 |
| Isadore Community Hub (isadore.sk) | domain now a cycling-clothing shop | 2026-10-13 |
| Dungeon Pub (dungeonpub.sk) | page is an empty stub | 2026-10-13 |

## Leads for the next session

- Resolve the open items above (coordinates by hand; browser checks for the Meetup, Mareena, SME SPOLU, BISLA, BlaBla entries).
- Find or confirm: Subclub website, Neptune Club, Pink Whale own site, Impact Hub Bratislava, British Chamber of Commerce site, Karlova Ves borough site, Slovak Academy of Sciences site (savba.sk did not resolve from this machine), Cinema City VIVO!, TIPOS Aréna / Ondrej Nepela Arena site.
- Backfill thin categories: bars and cafés with event programmes, restaurants with themed dinners, hobby and sports clubs open to non-members, Slovak-language community groups.
- Bookables to chase on existing entries: backstage tours (SND, Philharmonic), group tours at the museums beyond the Devín Castle lecture (25 EUR for groups up to 40, on request), workshops at galleries.
- Subscribe to the newsletters in `newsletters.md` and tick `newsletter_subscribed`.
