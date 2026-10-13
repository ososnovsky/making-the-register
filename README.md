# Making the register

A kit for building a curated register of local event sources (venues, aggregators, community groups, newsletters, bookable activities) with Claude Code. The included register covers Rotterdam, The Hague, and Delft, plus culture venues in Leiden, Amsterdam, and Utrecht. Use it as a worked example for your own city.

## What's here

| File | Role |
|---|---|
| `formative/IMP-event-scanner-source-taxonomy.md` | The rulebook: source categories (§2), entry schema (§5), channels and fetch rules (§6), coverage gate (§7), bookables (§8) |
| `formative/IMP-event-scanner-idea-brief.md` | Background: the app this register feeds |
| `taxonomy creation prompt.md` | The prompt that started the original session |
| `_staging/agent-brief.md` | Brief used for sub-agents researching one category family |
| `_staging/geocode.py` | Fills `coords: TODO` via OpenStreetMap Nominatim |
| `validate_sources.py` | Checks `sources.yaml` against §5; regenerates `newsletters.md` and `bookables.md` |
| `sources.yaml` | The register (example data) |
| `coverage.md`, `newsletters.md`, `bookables.md`, `local-browser-checks.md` | Coverage table and generated or working lists |

Requires Python 3 with PyYAML (`pip install pyyaml`).

## Adapting it to your city

1. Set your scan areas in the taxonomy (§2, §5, §7), in `CITIES` and the `LAT_RANGE`/`LNG_RANGE` box in `validate_sources.py`, and in `taxonomy creation prompt.md`. Review the scope rules in taxonomy §2 and §8 too; they reflect the original owner's preferences.
2. Replace `<your-email>` in `_staging/` with your contact address (Nominatim requires an identifying User-Agent).
3. Move the example register files somewhere out of the way, for example `example/`, and start a fresh `sources.yaml`.
4. Open Claude Code in this folder and give it the prompt in `taxonomy creation prompt.md`.
