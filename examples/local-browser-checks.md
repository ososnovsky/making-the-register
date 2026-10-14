# Local browser checks (backfill)

Checks the cloud sessions could not complete: the sites block headless or datacentre browsers (Vercel or Cloudflare challenges, municipal bot checks, IP blocks). Rows marked "discovery" or "lead" have no entry yet: add one only if the check turns up a working source, per the register rules. None of them blocks the next curation step. Hand this file to a **local** Claude Code session with Chrome; it is written as that session's prompt.

---

## Prompt for the local session

Plain curation task, not a pipeline run. In this repo, `sources.yaml` is the source register for the Event Scanner app; follow `formative/IMP-event-scanner-source-taxonomy.md` §5, §6, and §8. For each open item below, open the page in Chrome (normal, non-headless, no login), then update the named entry in `sources.yaml` (or in the staging file named, if it has not been merged yet):

- Replace the generic link with the real agenda/events page if one exists (`channel: website-agenda`).
- Record a newsletter signup if there is one (`channel: newsletter`, `newsletter_subscribed: false`; public archive → separate `website` link).
- Record bookables per §8 (group or private tours, workshops on request, with price and group size when stated). Ticketed tours on fixed dates are events, not bookables.
- Keep `reading_hint: browser` if events only appear after rendering.
- In `notes`, replace "local Chrome check pending" with what you found and "checked in Chrome <date>".
- Never invent a URL or value; anything still unclear stays an open item in `notes`.
- Never open Instagram or Facebook.

Then run `python validate_sources.py`, tick the item here (move it to "Done"), and hand Dyma a commit message.

## Open items

(none: all done 2026-10-04)

## Done

Checked in local Chrome on 2026-10-04 (plain fetch from a home IP also tried; never bypassed a security warning).

| # | Entry id | Result |
|---|---|---|
| 1 | `foam` | agenda /nl/programme; newsletter panel (?form=general); bookables: adult group tour €100/h, private tour €25 pp (min €625); plain fetch still 429 |
| 2 | `stadsarchief-amsterdam` | agenda /stadsarchief/agenda/ (dates); newsletter via homepage (mailinglijst); bookable: group tour €95 per group (max 20); plain fetch still 403 |
| 3 | `museumnacht-amsterdam` | programme /programma (221 items, 7 Nov 2026); footer newsletter; Museumdag (museumdag.amsterdam/dag-programma) kept as a second agenda link, not its own entry |
| 4 | `amsterdam-burlesque-revue` | "Upcoming" list renders; plain fetch 200 but the list is client-side, so `reading_hint: browser` stays |
| 5 | (discovery) | The Moods Bar: last Partyflock party 2017 (stays rejected); Eros Society has its own site eros-society.com, NL/BE-wide, no upcoming dates (noted on `club-sahara`); no TIWYA page on Partyflock |
| 6 | (discovery) | gayrotterdam.nl: untrusted TLS certificate in Chrome too; rejected |
| 7 | (discovery) | events.musicofourdesire.com: blocked by NordVPN as potential phishing; not visited, never link |
| 8 | `de-nieuwe-anita` | site back up; agenda in plain HTML (dates on item pages); Mailchimp newsletter + public archive; Smut Slam 25 Oct 2026; `reading_hint: fetch` |
| 9 | `paradiso` | full programme renders, 25 items per scroll (obfuscated endpoints, month filter has no URL); newsletter needs a Mijn Paradiso account |
| 10 | `muziekgebouw-aan-t-ij` | agenda /nl/agenda renders; newsletter page confirmed (form behind cookie consent); plain fetch still redirected by the CDN |
| 11 | `podium-aan-zee` | own agenda /agenda/ works in plain fetch (embedded JSON); footer newsletter; address confirmed; `reading_hint` dropped |
| 12 | (discovery) | Waalse Kerk Den Haag: new entry `waalse-kerk-den-haag` (agenda + newsletter); Noorderkerk Den Haag: congregation site only, rejected |
| 13 | `rotterdam-orgelstad` | agenda loads (plain fetch too); no newsletter; iCal link empty |
| 14 | `remastered-rotterdam` | no agenda or newsletter; group and private-showing packages recorded as bookables; plain fetch works |
| 15 | `goethe-institut-amsterdam` | old page 404; agenda now /ins/nl/nl/ver.cfm; newsletter /ins/nl/nl/new.html; no bookables; plain fetch still 403 |
| 16 | `de-galerie-rotterdam` | agenda, newsletter, address (Witte de Withstraat 17A) and coords added; plain fetch works |
| 17 | `de-galerie-den-haag` | agenda, newsletter, address (Noordeinde 69-71) and coords added; plain fetch works |
| 18 | `vak-delft` | kept: lunch concerts, Saturdance drop-ins, exhibitions (client-side agenda); newsletter; address and coords added |
| 19 | `studio-adc` | bookables recorded (group workshops 60/90/120 min, private lessons); agenda page has no dated items |
| 20 | `impakt` | agenda moved to /nl/whats-on/ (client-side); Mailchimp newsletter; group tours bookable |
| 21 | `doctor-watsons-rotterdam` | €149 per escape room, min. age 14 (own FAQ); 8 more bookables (tastings, cocktail workshop, murder mystery, VR, mobile game); address conflict noted |
| 22 | `bowling-scheveningen` | pages render; lane and shuffleboard prices only inside the booking flow (open item); arcade page has no details |
| 23 | `amaze-vr-den-haag` | prices unchanged; arcade minimum age now 10; no newsletter |
| 24 | `hogeschool-rotterdam` | agenda works (26 activities, mostly open days and study-choice sessions, plus conferences and lectorate events); site is slow but plain fetch from a home IP returns 200 with the items; `reading_hint` dropped; no newsletter |
| 25 | `mkb-rotterdam-rijnmond` | month view renders (7 October events); JSON feed `wp-json/community/events` (377 items, 2022–2027) added; `reading_hint` dropped |
| 26 | `ai010` | /events lists the 15 Oct congress and an archive of past PizzAI meetups; plain HTML now has it; `reading_hint` dropped; "Word lid" goes to a WhatsApp community, no newsletter |
| 27 | `bluecity` | list renders (9 items, 10 Nov to 3 Dec); Mailchimp newsletter `eepurl.com/dOAACH` added; `reading_hint: browser` stays |
| 28 | `erasmus-centre-for-entrepreneurship` | /events and /en/events show a loading error in Chrome too; the nav no longer links an events page; open item, removal candidate if it stays broken |
| 29 | `youngship-rotterdam` | calendar empty, last event Oct 2024, no Rotterdam items in the global feed: **propose removal** |
| 30 | `buzz-business-networking` | own site loads (no Cloudflare check) and plain fetch is 200; /events (Eventbrite feed) and its JSON feed added; homepage link dropped; "women-only" claim not supported by the site (open item) |
| 31 | `jci-haaglanden` | calendar renders (7 items to Dec); iCal export added (plain fetch works); only the LOKAAL Netwerkborrels are open to non-members; `reading_hint` dropped |
| 32 | `female-ventures-delft-the-hague` | events render per city tab; Delft/The Hague JSON feed (feed/1292) added; 2 items (15 Oct Delft, 24 Oct Den Haag); `reading_hint` dropped |
| 33 | `technet-delft` | meetings render (20 Oct, 17 Nov, no year); members-only, non-members by invitation; browser still needed |
| 34 | `asser-institute` | list renders (9 items with type tags; public lectures vs paid courses); /api/event gives 500 to plain fetch; browser stays |
| 35 | `the-hague-tech` | /events opens a Wix members' sign-up wall; homepage block links /event-details pages carrying the full date with year |
| 36 | `social-club-den-haag` | Eventbrite: "Nothing planned right now", last event Feb 2026; news page stays the main source |
| 37 | `repair-cafe-rotterdam-noord` | agenda renders and is now in plain HTML (11 Jul, 12 Sep, 10 Oct, 14 Nov); venue Ruivenstraat 81 (contact page) and coords (PDOK) added; `reading_hint` dropped |
| 38 | `tantra-speed-date-rotterdam` | city page omits the 1 Nov Rotterdam date even when rendered; event page confirms 1 Nov 18:30 Salsability Club; `reading_hint` dropped; stale-link open item stays |
| 39 | `tantra-speed-date-den-haag` | city page links only the next date (17 Oct); postcode 2564 XS confirmed; venue and coords (PDOK) added |
| 40 | `meetup-besquare-rotterdam-socializing-made-fun-easy` | besquare.social/en/events shows only 10 activities (a subset of Meetup), so not linked |
| 41 | `accueil-la-haye` | calendar renders (many weekly items); newsletter has no public signup (only infolettre@ address); membership €45/household; members-only status is an open item |
| 42 | `de-chinese-brug` | agenda's only item is from Mar 2023, news stops Dec 2023, aimed at Chinese-speaking seniors: **propose removal**; `reading_hint` dropped |
| 43 | `netherlands-india-association` | active but low volume (15 Aug and 12 Dec 2026 events, €45 gala), both at De Duinpan, De Zilk (outside the scan areas); /events link added |
| 44 | `maitri-foundation` | events list fine in plain fetch from a home IP (200); 2 upcoming (17 Oct concert, 18 Oct Garba Night); `reading_hint` dropped |
| 45 | `wijkz-den-haag` | /activiteiten and stadsdeel "Activiteiten" blocks are empty in Chrome too; no event data: **propose removal** (or keep as placeholder) |
| 46 | `brandersfeesten-schiedam` | site loads (200 from home IP); programme page added as agenda; 2026 edition passed (25–27 Sep); `reading_hint` dropped |
| 47 | `markthal-rotterdam` | /events renders article cards but lags (newest 1 Sep); homepage stays the better source |
| 48 | `bibliotheek-rotterdam` | /activiteiten renders 233 results (= JSON); newsletter link added (footer, needs a KB login account); `reading_hint` dropped |
| 49 | `topsportcentrum-rotterdam` | "Evenementen" is venue-hire marketing; no event list anywhere; `reading_hint` dropped; fixtures link still an open item |
| 50 | `stadion-woudestein` | Vrouwen programme page has no fixtures list (only a pre-season image); home ground Woudestein confirmed by a 2 Oct match report |
| 51 | `sportcentrum-west` | rooster is in plain HTML (`reading_hint` dropped); webshop blocked by NordVPN (self-signed certificate), not bypassed |
| 52 | `zwemcentrum-rotterdam` | two-week rooster renders and is in plain HTML (`reading_hint` dropped); aqua prices confirmed (2026 tariff PDF); SWIMR training and adult lessons added as bookables; no e-mail newsletter (monthly "Nieuwsbrief" news posts only); webshop domain not readable by the extension |
| 53 | `sportcentrum-feijenoord` | rooster in plain HTML (`reading_hint` dropped); aqua classes and adult lessons (women's and men's groups) confirmed; prices confirmed; private-lesson price still open |
| 54 | `sportcentrum-de-wilgenring` | rooster in plain HTML (`reading_hint` dropped); aqua, Fifty Fit, PiYoChi, adult lessons on it; aqua and squash prices confirmed |
| 55 | `zwembad-ijsselmonde` | rooster in plain HTML (`reading_hint` dropped); aquabootcamp, aquajoggen, Fit & Soepel, adult lessons A/B/C, women's and 60+ groups; prices confirmed |
| 56 | `zwembad-hoogvliet` | closed for renovation until about March 2027 (rooster all "Gesloten"); renovation page added as `website` link; bookables suspended until reopening; `reading_hint` dropped |
| 57 | `sportcentrum-de-rozenburcht` | rooster in plain HTML (`reading_hint` dropped); SWIMR and adult lessons added as a bookable (SWIMR prices from the tariff PDF; adult-lesson price not listed); aqua and snorkelling prices confirmed |
| 58 | `skateland-rotterdam` | /events/ archive is empty ("Geen berichten gevonden"); homepage carries the dated events list in plain HTML, now the `website-agenda` link; WordPress JSON event list added; nothing announced after Aug 2026; `reading_hint` dropped |
| 59 | `hc-rotterdam` | agenda renders in Chrome as month accordions (Oct 2026–Jul 2027), mostly internal club items (Super Sunday club days public); Clinics & Events shop category still empty; `reading_hint: browser` stays |
| 60 | `rotterdam-atletiek` | calendar is an embedded Google Calendar; public iCal feed found and added (`other`, plain fetch works); upcoming: Herfstwerpen 10 Oct, Wintercross series, Tryout Games 19 Dec |
| 61 | `rv-nautilus` | news renders client-side (FOYS), club news only, no public events; 2026 fees confirmed (seniors €450, juniors €315, €75 registration, no extra instruction cost) |
| 62 | `diergaarde-blijdorp` | "Nu in Blijdorp" holds no items right now (Chrome and plain HTML alike); Blijdorp Colleges page has a dated agenda (last Sunday monthly, free with admission), added as `website-agenda`; `reading_hint` dropped |
| 63 | `vroesenpark` | Uitagenda location page lists no events now (description only); location pages list events in plain HTML when there are any (checked against ss-rotterdam), so `reading_hint` dropped |
| 64 | `kralingse-bos` | same: no events listed now, only related articles; `reading_hint` dropped |
| 65 | `zuiderpark-rotterdam` | same: no events listed now (festival articles only); `reading_hint` dropped |
| 66 | `dakpark-rotterdam` | agenda is an AJAX-loaded ICS Calendar month view (renders in Chrome, not in plain HTML; `reading_hint: browser` stays); Oct 2026 items include bat spotting, Senioren Fit Festival, soup evening; Mailchimp form on the agenda page |
| 67 | `gemeente-den-haag-zwembaden-sportverhuur` | timetable renders (50 per view, up to 16 Oct 2026); data via obfuscated bot-protected fetch endpoints, so `reading_hint: browser` stays; new activity types noted (Aquabootcamp, Verbeter je Zwemslag, Zwangerschapszwemmen) |
| 68 | `haagsche-rugby-club` | calendar renders; public Outlook iCal feed found and added (`other`, plain fetch); content mostly internal meetings and room bookings, HRC Touch evenings the main open item |
| 69 | `rijswijkse-golfclub` | calendar is a Google Calendar; public iCal added (member competitions mostly); clinic page: group clinics on request, lesson rates confirmed, regular-clinic list empty; beginners' course price still not shown |
| 70 | `zuiderpark-den-haag` | still maintained: iCal feed (needs redirect follow to /feed.ics/) has 151 items into Dec 2026 (Circus Up 16–18 Oct, Wintercafé 23 Dec); added as `other`; Chrome list view opens on July 2026 |
| 71 | (discovery) | polonyna.nl: working, Rotterdam-based Ukrainian choir; Vite single-page app (plain HTML empty); six dated free concerts in 2026 (Laurenskerk, De Doelen, Fenix, Dokhuis, Hillevliet, Lutherse kerk Delft); "upcoming" block still shows 12 Sep 2026; proposed entry below |
| 72 | (discovery) | nlcares.nl: working; dated volunteer activities per city (Rotterdam and Den Haag segments, 20+ open activities each: cooking for neighbours, bingo with seniors, gardening, walking language class); JS-only; joining needs an account; proposed entries below |
| 73 | (discovery) | The Social Hub The Hague / Delft: no public events page (sitemap has only "meetings-and-events" venue hire per city; events live in the guests' app); reject |
| 74 | (discovery) | Jong Management: kring pages (kring-den-haag, -rotterdam, -delft) list dated meetings (e.g. Art The Hague 15 Oct, Kerstdiner 9 Dec 2026), but sign-up is for members ("open to members from Rotterdam and Delft"); members-only, reject (or note under coverage) |
| 75 | `villa-ockenburgh-theater` | agenda is a WeTicket embed; shbo.weticket.io (plain HTML works) is now the `website-agenda`, JouwWeb page demoted to `website`; newsletter form confirmed (SHBO, Filmclub, Theater lists); `reading_hint` dropped |
| 76 | `sporten-in-delft` | SBG app renders in Chrome: dated sessions with time, age range and address (signup needs an account); mostly recurring, many senior or child sessions; `reading_hint: browser` stays |
| 77 | `studio-unshaped` | /events is not an agenda but a private-party workshop offer (added as a bookable, with the €70/€50 workshops); /book (course starts, prices) replaces it as a `website` link; no dated public events; `reading_hint` dropped |
| 78 | `jalan-jalan-festival` | opens in Chrome (Cloudflare only blocks curl); /programma/ added as `website-agenda` (2026 edition 21–23 Aug, marked past); 2027 not announced; no newsletter |
| 79 | `pasar-malam-rijswijk` | opens in Chrome; 7–8 Nov 2026 confirmed with hours (dates page added as `website-agenda`); programme page still shows a March 2026 edition, so twice yearly |
