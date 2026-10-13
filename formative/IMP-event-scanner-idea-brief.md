# Idea brief — Event Scanner (`IMP-event-scanner-idea-brief.md`)

Consumed verbatim by Development Pipeline stage 1 (`build-spec-writer`). One item per line; exclusions are explicit in §10.

| | |
|---|---|
| Run / date | IMP-event-scanner · 30 September 2026 |
| Provenance | Lane C direct (stages 1–2 never ran). Decision reason: the owner repeatedly learns about local events only after they happen, if at all, and wants to socialise and meet new people. |
| Flags carried | None (stages 1–2 not run). |
| Companion artefact | `IMP-event-scanner-source-taxonomy.md` — source categories, event categories, and the register entry schema. Where this brief lists categories or fields, the taxonomy doc is the fuller definition. |
| Amendments | 1 October 2026 (owner, during register building): newsletter scanning through a separate, isolated routine, and a Bookings view for activities arranged on request or by appointment. 1 October 2026 (owner): the culture family of sources (theatres and cinemas, museums, event venues, other culture) extended to three culture-only scan areas, Leiden, Amsterdam, and Utrecht, together with the aggregators that list their culture. 3 October 2026 (owner): kids-only sources, events, and bookables are out of scope; adult-only (18+) ones are in scope in every category; walk-in activities separate from ordinary admission (e.g. tower climbs) count as bookables; a 21st source category, activity venues (escape rooms, shooting ranges, bowling, karting and similar; full scan areas only), with its own event category. 4 October 2026 (owner): men-only sources, events, and bookables, and those primarily based on queer, drag, or LGBTQ+ identity or culture, are out of scope (applied retroactively to the register); a per-event "likely international" flag next to the social flag. |

## 1. Concept

A personal web app that shows what is happening in Rotterdam (including Schiedam), The Hague (including Rijswijk), and Delft, plus cultural venues and organisers in Leiden, Amsterdam, and Utrecht, over at least the next 30 days. A weekly automated scan compiles the events from a curated register of local sources: venue websites, aggregators, community channels, and similar. The app displays them as a chronological agenda linked two-way with a map. A separate, isolated routine adds events announced in newsletters the owner has subscribed to. A second view lists bookables: activities that can be arranged on request or by appointment, such as private tastings or workshops. The core value is to stop discovering events after they have happened, and to surface occasions to meet new people.

## 2. Who and why

- **Target user**: the owner — a single person living in Rotterdam who uses the app on phone and laptop to decide what to attend, with a particular interest in events where meeting new people is likely. Occasionally shares the password with a friend.
- **Need**: event information is scattered across venue sites, aggregators, and community channels; the owner finds out too late or never.
- **Why now**: the owner wants to socialise and meet new people more. Also, Claude Code routines make an unattended scanner possible on an existing Claude subscription, without paid API billing.

## 3. Core loop / core value path

1. On Sunday the scan runs automatically with no owner action.
2. The owner opens the app on their phone and enters the password.
3. The agenda lists the coming week's events chronologically; each event is a pin on the map.
4. The owner taps a pin; the agenda scrolls to that event.
5. The owner taps an event title; the map centres on that event's location.
6. The owner taps Directions; Google Maps opens with the event's location.

On-demand variant: the owner presses Scan now → the status shows "scanning" → minutes later the agenda and map show the fresh results.

Bookings variant: the owner switches the view from Agenda to Bookings → the list shows bookable activities with their places on the map → the owner taps a booking link and arranges it on the provider's site.

Slice-1 tracer (walking skeleton): one register source → routine run → ingest endpoint → Supabase → one agenda item plus one pin.

## 4. Features

### Must — scanner

- The scanner runs as a Claude Code routine on the owner's Claude subscription, not inside the web app.
- The routine runs automatically every Sunday (owner-set time, early morning).
- The routine can be triggered on demand through its per-routine API endpoint.
- At the start of every run, the routine reads the source register (`sources.yaml`) from the app repository.
- The routine visits every link of every register entry not flagged `unfetchable`.
- The routine may use web search to locate a register source's agenda or event pages; page fetching is limited to the allowlisted domains (§6).
- Minimum scan horizon: the scan date plus 30 days; the routine follows agenda pagination or month navigation on a source until those 30 days are covered.
- Events beyond 30 days that appear on pages the routine has already fetched are kept; the routine does not navigate further solely to find them.
- Reading uses an escalation ladder, moving down only when the current step yields no usable event data: (1) plain page fetch → (2) headless browser rendering → (3) PDF text extraction → (4) reading images of flyers or posters.
- Fields extracted per event:
  - title, in the original language
  - a one-line English translation, when the source is not in English
  - venue name
  - address
  - city
  - coordinates
  - start date
  - start time
  - end date/time
  - ticket required (yes / no / unknown)
  - price in EUR
  - source page link
  - event category
  - social flag
  - likely-international flag
- Any field the source does not state is recorded as `unknown`; the scanner never guesses values.
- Coordinates come from the register entry when the event is at that venue; other addresses are geocoded by the routine using a keyless geocoding service.
- The event category is assigned by the scanner from the fixed event-category list in the taxonomy doc.
- The scanner drops events aimed only at children (children's shows, family shows with age labels such as 4+, children's workshops).
- The scanner drops events that are men-only or primarily based on queer, drag, or LGBTQ+ identity or culture (e.g. queer club nights, drag shows, ballroom/kiki nights, Pride events), also at venues that are otherwise in scope.
- The social flag is assigned per event by the scanner. It starts from the register entry's default and is adjusted by event type (e.g. meetups and networking events flagged; screenings and exhibitions not). Rules are in the taxonomy doc.
- The likely-international flag is assigned per event by the scanner using its best judgement: set when non-local people are likely to be among the audience (e.g. internationals, expats, tourists, or people travelling in from other cities); they need not be the majority. Guidance is in the taxonomy doc.
- Before delivery, the routine merges duplicate events that match on title, date, and venue.
- The routine delivers results only through the app's ingest endpoint (§4 security).
- The routine reports the scan's status as `running` at start and `complete` or `failed` at end.
- The routine delivers a per-source scan report: each source gets `ok`, `no events found`, `unreadable`, or `blocked`.
- Each completed scan replaces the previous scan's events and report entirely. Replacement is per routine: a web scan replaces only web-scan events, and a newsletter scan replaces only newsletter events.
- Each scan also passes the register's bookables (taxonomy §8) to the ingest endpoint, so the app never reads the repository. The routine geocodes a bookable's address only when it is not at the entry's venue, and reports any bookable whose link no longer resolves.

### Must — newsletter scan

- Newsletter events are collected by a second, separate Claude Code routine (the newsletter routine), not by the web scan routine. Keeping them apart limits prompt-injection exposure: the routine that reads email never browses the web, and the routine that browses the web never sees email.
- The owner subscribes to the newsletters listed in the register (channel `newsletter`), and a mail filter applies a dedicated label (e.g. `Newsletters`) to them.
- The newsletter routine reads only messages under that label, received since its previous run; it never searches or opens the rest of the mailbox.
- It extracts the same event fields as the web scan (§4 scanner) and links each event to the provider's web page for it when the email has one, otherwise to the register entry's website. The source shows as "newsletter: <sender>".
- Where a newsletter has a public web archive (e.g. Mailchimp, Substack, Laposta), the web scan fetches the archive like any other page; the newsletter routine then covers only newsletters without one.
- It runs on the same schedule as the web scan, and also on demand.
- It reports a status per sender: `ok`, `no events found`, or `unreadable`.
- It never sends, forwards, replies to, labels, archives, or deletes email.

### Must — web app

- Login is a single password stored as a Vercel environment variable, with a session cookie; there are no user accounts.
- The layout has two parts: an agenda and a map.
- The agenda lists events chronologically.
- Each agenda item shows title, English line, venue, date, time, ticket required, and price.
- Each agenda item shows the social flag when set.
- Each agenda item shows the likely-international flag when set.
- Each agenda item has a Directions link that opens Google Maps at the event's location (deep link; no API key).
- Each agenda item links to the event's source page.
- The map uses Leaflet with OpenStreetMap tiles.
- The map shows one pin per event in the current view.
- Hovering (desktop) or tapping (touch) a pin scrolls the agenda to that event and highlights it.
- Clicking an event title in the agenda centres the map on that event's location. This happens on click only, not on hover.
- A view switch offers Today, Week, Month, and All, each filtering the latest scan: Today = the current date; Week = today plus the next 6 days; Month = today plus the next 29 days; All = every upcoming event in the latest scan, including those beyond 30 days.
- Category toggles filter both agenda and map by event category.
- A social toggle filters both agenda and map to socially flagged events.
- A likely-international toggle filters both agenda and map to events with the likely-international flag.
- A Scan now button triggers the routine through a server-side function; the routine token never reaches the browser.
- A scan status line shows either "scanning since [time]", "last scan [day, time]", or "last scan failed [time]".
- The layout is usable on phone and laptop browsers.
- A view switch toggles between Agenda (dated events) and Bookings (bookables: activities arranged on request or by appointment).
- Each Bookings item shows the activity name, place name, location, a Directions link, and a link to the booking or information page; a short note (e.g. group size, price) when the register gives one.
- In the Bookings view the map shows one pin per bookable's place, with the same two-way pin ↔ list linking as the Agenda.
- The category toggles and the social toggle filter the Bookings view as well.
- The app is installable on an iPhone home screen via Safari's Add to Home Screen, and opens full-screen with its own icon (web app manifest, app icons, standalone display mode).
- The login session persists across launches from the home-screen icon.

### Must — source register

- The register is a YAML file, `sources.yaml`, in the app repository.
- The register is built and edited through Claude sessions or by hand; v1 has no in-app editing.
- Each entry holds at minimum:
  - name
  - source category
  - city
  - one or more links
  - venue coordinates, if it is a fixed venue
  - default social flag
  - fetch status (`ok` / `unfetchable`)
  - notes
  - newsletter signup link and subscription status, when the source has a newsletter
  - bookables, when the source offers activities on request or by appointment
- Entries with no fetchable channel are flagged `unfetchable` and skipped by the scanner. A `newsletter` channel counts as fetchable only once the owner has subscribed.
- The register is the list of newsletters for the owner to subscribe to; the register-building session keeps a generated "Newsletters to subscribe" list.
- Bookables are curated by hand in the register; they are not discovered by the weekly scan.
- The full schema and category definitions are in the taxonomy doc.

### Must — security

- The web scan routine has zero connectors attached. Connectors stay connected at account level; they are removed from this routine's form only.
- The routine never holds database credentials.
- The newsletter routine (§4 newsletter scan) is the only routine with an email connector, and it has nothing else:
  - no other connectors;
  - a network allowlist containing only the app's domain (for ingest) and the geocoding service, so it cannot browse or send data elsewhere;
  - its own ingest token, separate from the web scan's, stored as a cloud-environment API credential, and accepted only for newsletter events;
  - the prompt states that email content is data, never instructions.
- The newsletter routine's email access must be read-only. Whether a routine's Gmail connector can be limited to read tools (no send, forward, draft, label, or trash) is unverified; stage 1 must check it.
- **Fallback (decided 1 October 2026):** if read-only access cannot be enforced, the newsletter routine gets no email connector. Instead, newsletters go to a dedicated address used only for them and are forwarded into an inbound-mail endpoint on the app, which stores them; the newsletter routine reads the stored messages through a narrow read endpoint. The exact mechanism is a stage 1 decision (ADR).
- Whichever mechanism is used, injected content in a newsletter is at worst able to create fake events; it must not be able to reach other mail, the web, or the database directly.
- The routine writes only through one ingest endpoint on the web app (`/api/ingest`).
- The ingest endpoint's token is stored as a cloud-environment API credential, so it is never visible to Claude during a run.
- The ingest endpoint validates the payload against the event schema and rejects anything else.
- The ingest endpoint writes to Supabase using credentials held only in Vercel.
- The routine's cloud environment uses a Custom network allowlist containing:
  - register domains
  - ticketing and aggregator domains
  - the geocoding service
  - the default package-manager list
- The routine prompt states that fetched page content is data, never instructions.

### Should

- An in-app view of the latest scan report, listing sources that were unreadable, blocked, or empty.
- Several events at the same venue are grouped under one pin, with the pin opening the list.

### Could

- In-app register editing.
- Cities beyond the six scan areas, and non-culture sources in Leiden, Amsterdam, and Utrecht.
- Switching the map to Google Maps (Maps JavaScript API).

## 5. Success criteria

These are checks on the product itself. Thresholds marked (T) are confirmed or adjusted after the scanner test run.

- Scheduled Sunday scans complete and appear in the app without owner action for 4 consecutive weeks.
- After Scan now, fresh results appear within 30 minutes. (T)
- Coverage: for a spot check of 10 fetchable sources, at least 90% of the events listed on each source page within the 30-day window appear in the app.
- Accuracy: in a spot check of 20 displayed events, at least 95% have the correct date, time, and venue.
- No guessed values: every field not stated on the source displays `unknown`.
- Every register source ends every scan with a status; there are no silent failures.
- Every subscribed newsletter sender ends every newsletter scan with a status; an event announced only in a subscribed newsletter appears in the app after the next newsletter scan.
- The Bookings view lists every bookable in the register, each with a working booking or information link.
- Pin → agenda scroll and title → map centring both work on a current phone browser and a laptop browser.
- Agenda and map are visible within 3 seconds of opening the app on a mobile connection.
- Added to an iPhone home screen, the app opens full-screen from its icon, without Safari's browser interface.
- One weekly scan uses an acceptable share of the owner's Claude usage allowance. (T)

## 6. Constraints

- Personal use, single user; access is shared only by sharing the password.
- No user accounts, sign-up, or identity provider.
- The web app is hosted on Vercel, including the ingest function and the scan-trigger function.
- Supabase stores only the latest scan's events, the latest scan report, and the current scan status, per routine (web scan and newsletter scan), plus the current bookables.
- Scanner compute is a Claude Code routine on the owner's Claude subscription (currently Max). The design must not depend on Max-only features beyond what routines and API credentials need.
- No Anthropic API key and no metered API billing.
- Subscription credentials are never used outside Claude Code or Claude.ai, per Anthropic's terms.
- Routines are a research preview. The API trigger ships under a dated beta header, and its shape may change.
- Routines are subject to a daily run cap per account, in addition to subscription usage limits.
- Map tiles are Leaflet + OpenStreetMap: no map API key, OpenStreetMap attribution displayed, and use stays within OpenStreetMap's tile usage policy.
- Directions use a Google Maps deep link with no API key.
- Geography is six scan areas. Three are full scan areas, covering every source category: Rotterdam (including Schiedam), The Hague (including Rijswijk), and Delft. Three are culture-only, covering only the culture source categories (`theatres-cinemas`, `museums`, `event-venues`, `culture-other`) plus aggregators that list culture: Leiden, Amsterdam, and Utrecht, each the municipality alone. Each event and register entry is tagged with one of these areas; its address keeps the actual municipality.
- The minimum scan horizon is 30 days; events listed further ahead on fetched pages are kept.
- No history is kept; previous scans are overwritten.
- The scanner never logs in to any third-party site.
- There is no automated collection from Instagram or Facebook (Meta terms; login-walled).
- The UI is in English; event titles appear in their original language plus a one-line English translation.
- European conventions: metric units, EUR, day-month dates, and 24-hour times.
- Target: no recurring cost beyond the existing Claude subscription (Vercel and Supabase free tiers).
- Native-ready: the scanner, ingest endpoint, and Supabase data layer must not depend on the web frontend, so a future native iPhone app can read the same data without changes to them.
- The frontend is an installable web app (PWA) in v1.
- Built through the owner's Development Pipeline.

## 7. Assumptions & risks

| Assumption / risk | Cheapest test / watch signal |
|---|---|
| A weekly scan of the full register fits within subscription usage without crowding out the owner's other Claude work | Test run: check usage before and after at claude.ai/settings/usage |
| Scan duration is acceptable for on-demand use | Test run: time from fire to `complete` |
| Routines (research preview) change or are withdrawn | Watch Claude Code release notes. Fallbacks: Desktop scheduled task (laptop must be on), or an API key (metered cost) |
| The daily routine run cap limits on-demand scans (reported at launch as 5 per day on Pro and 15 on Max) | Check remaining runs at claude.ai/code/routines |
| Claude Code's page-fetch tool may or may not obey the environment allowlist | Test run: fetch one off-list domain and check the transcript for a 403 |
| The allowlist blocks redirects to unlisted domains (ticket shops, link hubs) | Review 403 `host_not_allowed` entries in the first transcripts; extend the list |
| Instagram/Facebook-only groups are unreachable | Register alternative channels: website, link-in-bio target, Luma/Meetup/Eventbrite, or Telegram. Public Telegram previews (`t.me/s/<channel>`) verified fetchable on 30 Sept 2026. No alternative → `unfetchable` |
| Instagram bios are behind a login wall for cloud IPs (sandbox test on 30 Sept 2026 was redirected to login, but that IP was already rate-limited, so it's inconclusive) | Include one Instagram profile in the test run and accept whatever a single plain fetch returns |
| Sources publish events incompletely; this is the real coverage bottleneck | Measure coverage against source pages, not against reality (§5) |
| Extraction errors, especially Dutch date and time formats | Accuracy spot check (§5) |
| Prompt injection via fetched pages | Zero connectors, narrow ingest door, and allowlist cap the worst case at fake events in the agenda |
| Prompt injection via newsletter email, e.g. an instruction to read or forward other mail | Separate newsletter routine, label-only reading, a narrow allowlist, and its own ingest token. Stage 1 must verify that the email connector can be read-only; if not, use the inbound-mail fallback (§4 security) |
| The routine's Gmail connector cannot be scoped to one label, so the routine could technically read the whole mailbox | Prompt instruction plus label-scoped search queries; if that is judged too weak at stage 1, use the inbound-mail fallback |
| Newsletters arrive as image-only or heavily templated HTML | The reading ladder (§4) applies to email bodies too; unreadable senders are flagged in the newsletter scan report |
| Bookables go stale (offer withdrawn, page moved) | The web scan checks each bookable's link and reports dead links in the scan report |
| JavaScript-rendered, PDF, or image-only agendas | Reading ladder (§4); anything still unreadable is flagged in the scan report |
| The ingest token leaks | Validation limits damage to fake events; regenerate the token |
| Supabase free-tier projects may pause when inactive (threshold unverified) | Verify at stage 1; weekly writes may or may not count as activity |
| iPhone home-screen mode may occasionally drop the login session (unverified) | Watch in daily use; with a single password, re-login takes seconds |
| OpenStreetMap tile policy is exceeded if the app is ever shared widely | Switch to a tile provider with a free-tier key |
| Geocoding service rate limits | Coordinates stored in register entries keep geocoding calls to one-off addresses |
| Stages 1–2 never ran, so no alternative ideas were screened | Accepted: self-directed, low-cost build |

## 8. Novelty & familiar structure

- **What's genuinely novel**: a personal event radar built on the owner's own curated source list. That list includes community groups and small venues that aggregators miss. An AI agent reads whatever format each source publishes, and a "social" flag filters for meeting people rather than for content. The two-way agenda ↔ map linking is a small but real usability gain. Honestly sized: an incremental personal utility, not a new category.
- **The proven structure it stands on**: event aggregators and city "uit" agendas (curated listings); RSS readers (a curated source list fetched on a cadence); list-plus-map split views (property and travel search); and scrape-and-display pipelines.

## 9. Visual & audio surface (hints, not a design brief)

- Desktop: agenda on the left and map on the right, side by side.
- Phone: agenda and map stacked or switchable, with the linking behaviour preserved.
- Clean and minimal; information density over decoration.
- A persistent scan status line.
- An Agenda / Bookings switch next to the Today / Week / Month / All view switch; Bookings items are visually distinct from dated events (no date column).
- The social flag as a distinct icon on agenda items and pins.
- The likely-international flag as its own distinct icon on agenda items and pins.
- Optional: pin colour by event category.
- No audio.
- Asset needs: an app icon for the iPhone home screen, in the sizes the web app manifest and iOS require, plus icons for the social and likely-international flags and event categories.

## 10. Out of scope

- Storing or browsing past scans.
- User accounts, sign-up, or multiple users.
- Manual entry of events.
- Scraping Instagram, Facebook, or any login-walled site.
- The scanner logging in anywhere.
- Buying tickets or booking.
- Notifications (push, email, or messaging).
- Sending, forwarding, replying to, or deleting email; reading any mail outside the newsletter label.
- Subscribing to newsletters on the owner's behalf (the owner subscribes by hand).
- Discovering bookables automatically; they are curated in the register.
- Calendar sync or export.
- Personalised recommendations or ranking beyond category toggles and the social flag.
- Cities beyond the six scan areas in v1, and non-culture sources in Leiden, Amsterdam, and Utrecht.
- Google Maps JavaScript API in v1.
- A native mobile app in v1; the architecture must allow one later (§6).
- Tracking whether the owner attends events.
- Offline use.
- An Anthropic API key or any metered model billing.
- Public or shareable event listings for other users.
- Kids-only events, sources, and bookables (programmes aimed only at children or families with children).
- Men-only events, sources, and bookables, and those primarily based on queer, drag, or LGBTQ+ identity or culture.
