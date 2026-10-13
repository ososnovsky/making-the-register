# Source taxonomy — Event Scanner (`IMP-event-scanner-source-taxonomy.md`)

This is the category level of the source register. It defines where the scanner looks (source categories), how events are labelled in the app (event categories and the social flag), and the shape of every entry in `sources.yaml`. The next step, outside stage 3, is a register-building session that fills this taxonomy with concrete places and links.

| | |
|---|---|
| Run / date | IMP-event-scanner · 30 September 2026 |
| Provenance | Lane C direct (stages 1–2 never ran) |
| Companion artefact | `IMP-event-scanner-idea-brief.md` |
| Scan areas | Full: Rotterdam (including Schiedam), The Hague (including Rijswijk), Delft. Culture-only (source categories 5–8, plus aggregators listing culture): Leiden, Amsterdam, Utrecht |
| Amendments | 1 October 2026: `newsletter` channel and `newsletter_subscribed` field (§5, §6); bookables (§5, §8). 1 October 2026: culture-only scan areas Leiden, Amsterdam, and Utrecht (§2, §5, §7). 3 October 2026 (owner): kids-only sources, events, and bookables excluded (§2, §3, §8); adult-only (18+) ones explicitly in scope in every category (§2); walk-in activities separate from ordinary admission, such as tower climbs, count as bookables (§8); source category `activities` and event category `games-activities` added (§2, §3, §7). 4 October 2026 (owner): men-only and queer-, drag-, or LGBTQ+-centred sources, events, and bookables excluded, retroactively (§2, §3, §8); likely-international flag (§4) |

## 1. Two category systems

- **Source category**: what kind of place or organiser publishes events. Each register entry has one. It organises the register and tells the scanner what to expect.
- **Event category**: what kind of event it is. The scanner assigns one per event, and it drives the app's category toggles.
- They are separate because one source hosts many event types. A bar can run quiz nights, live music, and networking drinks in the same week.
- **Bookables** (§8) are a third kind of record: activities a source offers on request or by appointment, with no fixed date. They use the event categories too, but appear in the app's Bookings view, not the Agenda.

## 2. Source categories (21)

| # | id | Category | Covers | Default social |
|---|---|---|---|---|
| **Aggregators** | | | | |
| 1 | `aggregators` | Listing platforms and city agendas | Platforms listing other organisers' events, e.g. Resident Advisor, Meetup, Eventbrite, Luma, city "uit" agendas. Highest yield; also the main source of duplicates. | Off |
| **Food, drink & nightlife** | | | | |
| 2 | `restaurants` | Restaurants | Supper clubs, tastings, themed dinners | Off |
| 3 | `bars-cafes` | Bars and cafés | Quiz nights, live music, open mics, language cafés | On |
| 4 | `clubs` | Nightclubs | Club nights, DJ events | On |
| **Culture** (also scanned in Leiden, Amsterdam, and Utrecht) | | | | |
| 5 | `theatres-cinemas` | Theatres and cinemas | Performances, comedy, screenings, film festivals | Off |
| 6 | `museums` | Museums | Exhibitions, late openings, tours, talks | Off |
| 7 | `event-venues` | Event venues | Concert halls, multi-purpose and expo venues | Off |
| 8 | `culture-other` | Other culture | Galleries, art spaces, creative studios, dance schools | Off |
| **Sport & outdoors** | | | | |
| 9 | `sports-clubs` | Sports clubs | Clubs and associations: open trainings, social tournaments, club events | On |
| 10 | `sports-venues` | Sports venues | Stadiums, arenas, climbing and sports halls; mostly spectator events | Off |
| 11 | `parks` | Parks | Park programmes and park-managing organisations. Few parks publish their own agenda; most park events arrive via `municipality`, `markets-festivals`, or `aggregators`. | Off |
| **Professional** | | | | |
| 12 | `networking` | Networking organisers | Business clubs, professional and expat business networks, networking-drinks organisers | On |
| 13 | `industry` | Industry events | Conferences, trade fairs, sector meetups, trade associations | On |
| 14 | `coworking-hubs` | Co-working and startup hubs | Co-working spaces, startup and innovation hubs | On |
| 15 | `universities` | Universities and student associations | Public lectures, open events, association events | Off |
| **Community** | | | | |
| 16 | `community-groups` | Community and private groups | Interest-based groups organising their own events; often Instagram- or Telegram-first, so the highest `unfetchable` risk | On |
| 17 | `diaspora-expat` | Expat and diaspora communities | Groups defined by shared origin or expat status, including Ukrainian organisations | On |
| 18 | `libraries-community-centres` | Libraries and community centres | Library events, neighbourhood centres, public workshops | Off |
| 19 | `markets-festivals` | Markets and festivals | Markets, fairs, street and seasonal festivals | Off |
| 20 | `municipality` | Municipal programme | Official municipal channels and public events for Rotterdam, Schiedam, The Hague, Rijswijk, and Delft | Off |
| **Activities** (full scan areas only) | | | | |
| 21 | `activities` | Activity venues | Places you book to play a game or try an activity: escape rooms, shooting ranges open to the public, axe throwing, bowling, karting, laser tag, VR and arcade venues, mini golf. Mostly bookables (§8); some also run dated events (leagues, tournaments, open evenings) | Off |

**Tie-break rules** (one category per entry):

- A group defined by shared origin or expat status → `diaspora-expat`; an interest-based group → `community-groups`.
- Official government channels → `municipality`; a city agenda run by a foundation or platform → `aggregators`.
- A source whose main activity is hosting events → `event-venues`; one whose main activity is something else (food, drink, sport, study) → that category.
- Sports: an organisation of members → `sports-clubs`; a facility → `sports-venues`.
- Activities: a venue whose main business is a bookable game or activity (escape room, bowling, karting, a shooting range open to non-members) → `activities`; a members' club (e.g. a shooting association) → `sports-clubs`; an immersive art or exhibition experience → `culture-other`; a bar or café that also rents out a karaoke room → `bars-cafes`.

**Kids-only exclusion (owner, 3 October 2026):** sources whose public programme is aimed only at children or at families with children (youth and puppet theatres, children's museums, children's festivals, family listing sites) are not recorded. Mixed venues stay; their kids-only events and bookables are skipped (§3, §8).

**Adult-only is in scope (owner, 3 October 2026):** sources, events, and bookables for adults only (18+), such as kink and fetish parties, sex-positive events, burlesque and erotic shows, erotic museums and art, and adult workshops, are recorded in whichever category fits, like any other source; note "18+" in `notes`. Paid sexual services are not events or bookables and are not recorded. Men-only adult events are out (next paragraph).

**Men-only and LGBTQ+-centred exclusion (owner, 4 October 2026):** sources, events, and bookables that are men-only, or whose primary basis is queer, drag, or LGBTQ+ identity or culture (queer clubs and bars, gay cruise bars, LGBTQ+ film or culture festivals, drag shows and drag dinner shows, ballroom and kiki nights, LGBTQ+ heritage institutions, Pride), are not recorded, in every category. Mixed venues stay; such events and bookables there are skipped (§3, §8). Applied retroactively to the register.

## 3. Event categories (app toggles)

Each event gets exactly one: the best fit, or `other`. Events aimed only at children (children's shows, family shows with age labels such as 4+, children's workshops) are dropped by the scanner, not categorised (owner, 3 October 2026). So are men-only events and events primarily based on queer, drag, or LGBTQ+ identity or culture (owner, 4 October 2026; §2).

| # | id | Event category | Includes |
|---|---|---|---|
| 1 | `music-nightlife` | Music & nightlife | Concerts, live music, DJ and club nights |
| 2 | `stage-screen` | Stage & screen | Theatre, comedy, dance performances, film screenings |
| 3 | `exhibitions` | Exhibitions & museums | Exhibitions, tours, late openings |
| 4 | `talks-learning` | Talks & learning | Lectures, panels, workshops, classes |
| 5 | `networking-professional` | Networking & professional | Networking drinks, conferences, industry meetups |
| 6 | `social-community` | Social & community | Meetups, language cafés, community gatherings, quiz nights |
| 7 | `sport` | Sport | Participating and spectating: runs, open trainings, tournaments, matches |
| 8 | `food-drink` | Food & drink | Tastings, supper clubs, food events |
| 9 | `markets-festivals` | Markets & festivals | Markets, fairs, festivals |
| 10 | `games-activities` | Games & activities | Escape rooms, bowling, karting, laser tag, shooting, axe throwing, mini golf, arcade and VR, played for fun; competitive sport and matches stay `sport` |
| 11 | `other` | Other | Anything that doesn't fit the above |

## 4. Social flag rules

**Definition:** an event where talking to strangers is part of the format, not merely possible.

The scanner applies these in order; the first rule that matches decides:

1. **Participatory format signals → on.** English: networking, meetup, language exchange, workshop, class, social, community night, open training, group run, supper club, quiz. Dutch: borrel, netwerkborrel, taalcafé, workshop, meetup.
2. **Audience format signals → off.** Screening, exhibition, lecture, concert, performance, match (spectating).
3. **Event category defaults → on** for `networking-professional` and `social-community`.
4. **Otherwise → the source's default social flag** (§2).

### Likely-international flag (owner, 4 October 2026)

**Definition:** an event where non-local people are likely to be among the audience, for example internationals, expats, tourists, or people travelling in from other cities. They need not be the majority: the flag means "likely present", not "mainly for them". The app has a toggle for it (brief §4).

The scanner sets it per event using its best judgement; there is no register field and no fixed rule list. Typical signals: the event is presented or held in English (or another non-Dutch language), it is organised by or for an international or expat community, it is aimed at tourists or visitors, or it has a wide draw (an international or national festival, a touring act with a following beyond the city, a large venue's headline show). A Dutch-language neighbourhood event for a local audience is off. When unsure, leave it off.

## 5. Register entry schema (`sources.yaml`)

| Field | Required | Type | Notes |
|---|---|---|---|
| `id` | Yes | slug | Unique, e.g. `example-jazz-cafe` |
| `name` | Yes | text | The name as the source presents itself |
| `source_category` | Yes | one of §2 ids | Exactly one |
| `city` | Yes | `rotterdam` / `the-hague` / `delft` / `leiden` / `amsterdam` / `utrecht` | The scan area, not the municipality: Schiedam → `rotterdam`, Rijswijk → `the-hague`. The actual municipality stays in `venue.address`. `leiden`, `amsterdam`, and `utrecht` are culture-only: allowed only with the culture source categories (`theatres-cinemas`, `museums`, `event-venues`, `culture-other`) and with `aggregators` that list culture; they cover the municipality alone |
| `links` | Yes | list of {`url`, `channel`, `note`} | At least one. `channel` is one of the §6 channel types; `note` is optional |
| `venue` | No | {`address`, `coords` [lat, lng]} | Only for fixed venues; omit for organisers who move around |
| `social_default` | Yes | true / false | Starts from the §2 default for the category; override per entry |
| `fetch_status` | Yes | `ok` / `unfetchable` | `unfetchable` when no link is fetchable: every link is a never-fetched channel (§6), or a `newsletter` the owner hasn't subscribed to |
| `reading_hint` | No | `fetch` / `browser` / `pdf` / `image` | Lets the scanner start at the right step of the reading ladder. Set by hand from scan reports |
| `newsletter_subscribed` | If the entry has a `newsletter` link | true / false | Set by the owner after subscribing. Starts as `false` |
| `bookables` | No | list of bookables (§8) | Activities offered on request or by appointment |
| `notes` | No | text | e.g. "agenda only in Dutch", "programme published monthly" |

Example entries (fictional):

```yaml
- id: example-jazz-cafe
  name: Example Jazz Café
  source_category: bars-cafes
  city: rotterdam
  links:
    - url: https://example.nl/agenda
      channel: website-agenda
    - url: https://example.nl/nieuwsbrief
      channel: newsletter
      note: no public archive
  venue:
    address: Voorbeeldstraat 1, Rotterdam
    coords: [51.920, 4.480]
  social_default: false
  fetch_status: ok
  newsletter_subscribed: false
  bookables:
    - name: Private jazz workshop
      link: https://example.nl/workshops
      event_category: talks-learning
      note: groups of 6–12, €35 pp

- id: example-community-group
  name: Example Community Group
  source_category: community-groups
  city: the-hague
  links:
    - url: https://t.me/s/examplegroup
      channel: telegram
    - url: https://www.instagram.com/examplegroup/
      channel: instagram
      note: reference only, never fetched
  social_default: true
  fetch_status: ok
```

## 6. Channel types and fetch rules

| Channel | Fetched? | Notes |
|---|---|---|
| `website-agenda` | Yes | A dedicated agenda or events page; preferred starting point |
| `website` | Yes | Homepage; used when there is no agenda page |
| `aggregator-page` | Yes | The source's page on a listing platform; use a city/date-filtered URL where the platform allows |
| `ticketing` | Yes | A ticket shop or box-office page |
| `telegram` | Yes | Public channel preview only (`t.me/s/<channel>`) |
| `link-hub` | Yes | Linktree-style pages, used only to reach other links |
| `pdf` | Yes | A published programme file |
| `newsletter` | Via the inbox, once subscribed | `url` is the signup page. Read by the separate newsletter routine (brief §4), never by the web scan. Note in `note` whether a public web archive exists; if it does, add the archive as its own `website` link so the web scan reads it |
| `instagram` | **No** | Recorded for reference only |
| `facebook` | **No** | Recorded for reference only |
| `other` | Case by case | Describe it in `note` |

**Rules:**

- When an entry has several fetchable links, the scanner visits them in this order: `website-agenda` → `aggregator-page` / `ticketing` → `telegram` → `link-hub` → `website` → `pdf`.
- The scanner never logs in and never fetches `instagram` or `facebook` links.
- An entry with only never-fetched links gets `fetch_status: unfetchable` and is skipped.
- The web scan skips `newsletter` links. An entry whose only fetchable link is a `newsletter` is `ok` once `newsletter_subscribed` is true, and `unfetchable` until then.
- Record a newsletter whenever a source announces events by email, even if it also has an agenda page: newsletters sometimes carry events the website doesn't.

## 7. Coverage gate for the register-building session

The register is "complete enough for v1" when:

- Every source category × scan area pair has at least one entry, or an explicit note saying "none found" or "not applicable": 21 × 3 = 63 cells for the full scan areas, plus 5 × 3 = 15 cells for the culture categories and aggregators in Leiden, Amsterdam, and Utrecht (78 cells). The other categories in those three are "n/a".
- Every entry has at least one fetchable link, or is marked `unfetchable`.
- Every fixed venue has coordinates.
- Every `newsletter` link appears in the "Newsletters to subscribe" list in `coverage.md`.
- Every bookable has a link that resolves.

Suggested order for the session: aggregators first (highest yield per entry), then places the owner already knows, then the remaining categories in the order of §2.

## 8. Bookables

**Definition:** an activity a source offers on request or by appointment, with no fixed public date. Also (owner, 3 October 2026): a walk-in activity you can do on any opening day at a time of your choice, when it is separate from ordinary admission to the venue itself, such as a church-tower climb. A visit whose activity *is* the venue's admission (a museum ticket, the Domtoren, Euromast) is not a bookable. Examples: a private wine tasting, a workshop for a group, a guided tour on request, a karaoke room, an escape room. An ordinary table reservation, ticket sale, or corporate venue hire is not a bookable, and neither is an activity for children only, such as a children's party or school programme (owner, 3 October 2026), nor one that is men-only or primarily based on queer, drag, or LGBTQ+ identity or culture (owner, 4 October 2026).

Bookables are curated by hand in the register. Each scan passes them to the app, which lists them in the Bookings view (brief §4).

| Field | Required | Type | Notes |
|---|---|---|---|
| `name` | Yes | text | The activity as the source names it |
| `link` | Yes | url | The booking page, or the page with booking information |
| `event_category` | Yes | one of §3 ids | Drives the category toggles in the Bookings view |
| `social` | No | true / false | Defaults to the entry's `social_default` |
| `address` | If the entry has no `venue` | text | Where the activity takes place, when that's not the entry's venue |
| `note` | No | text | Group size, price, how to book (e.g. "by email"), language |

An entry may have bookables even when it has no dated events. Such an entry still needs at least one link and a `fetch_status`; when its only purpose is the bookable, note that in `notes`.
