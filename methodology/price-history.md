# Monthly provisional all-provider VPN price history

The publisher is Steve Price (ORCID 0009-0009-6603-6878). Data is CC BY 4.0.
The reporting universe is all 29 providers configured in the private collector
and every extracted USD plan from US runners. EUR and GBP test observations
are excluded from active research without conversion. Providers with no USD
extractions remain visible in coverage. Earlier multi-currency v1 files are
archived for reproducibility; the current monthly index points to USD revisions. Coverage rows retain providers
with missing, blocked, ambiguous or carried-forward data. This is not a census
of the VPN market or a representative price index. The records are automated
and unreviewed, with original extraction states and review flags. Trend
eligibility checks arithmetic, source and freshness; it is not human verification.
No automated extraction is relabeled as manually verified research. Raw
captures, checkout URLs, private paths and private notes remain private.

## Unit, files and coverage

A row is one provider's offer in one published snapshot. `snapshot_at` is the
feed generation time; `observed_at` is the underlying capture time. Multiple
intraday snapshots are retained. `freshness_status=current` identifies a current extraction;
`trend_eligible=true` additionally requires a successful pricing source,
reconciled positive total and duration, and no blocking conflict flags; a fallback repeats earlier evidence and is excluded from fresh
price findings. Do not count repeated fallback rows as additional captures.
`source_snapshots` contains each input path and SHA-256 digest. CSV nulls are
empty; JSON nulls are explicit. All times and reporting boundaries are UTC.

Completed months are frozen from the retained snapshot history through the last
calendar day; a release requires a month-end snapshot. Earlier history begins
August 11, 2026. August is partial and has no standalone monthly comparison.
The September release includes 30 days; individual providers may have missing
fresh observations. A snapshot day is not necessarily a fresh capture for every tracked provider.
Monthly summaries report fresh and fallback record counts, snapshot counts,
missing snapshot dates, and per-plan eligible observed days.

## Field definitions and calculations

- `upfront_total`: introductory amount billed, before any tax not included by the source.
- `paid_months`, `free_months`, `service_months`: service length; the latter is their sum when all are known. Lifetime offers stay visible but cannot be normalized into a finite monthly price.
- `effective_intro_monthly`: upfront total divided by service months, including free months.
- `renewal_total`, `renewal_period_months`, `effective_renewal_monthly`: disclosed next billing amount and period, normalized by dividing them. The periods can differ from introductory periods.
- `renewal_total_status`: extraction/disclosure status; missing is not zero. `not_applicable` is used for non-recurring plans.
- `discount_percent`, `advertised_discount_pct_status`: machine-extracted provider claim or derived reference-price comparison, as indicated by the extraction state. Never treated as measured savings against an earlier observed long-term offer.
- `reference_price_total`, `reference_price_basis`: the provider's reference or a monthly-plan equivalent, not proof that customers previously paid that total.
- `source_url`, `source_kind`: actual observed page; partner offers are labeled. Page-level source kind does not establish every visitor's eligibility.
- `series_id`: SHA-256 prefix of provider, plan, country, currency, paid months, free months, billing type, and source URL. All must match for like-for-like introductory price comparisons. Monthly history additionally separates upfront/duration extraction-status changes.
- `evidence_sha256`, `snapshot_path`, `snapshot_sha256`: capture evidence digest and public input provenance.
- `validation_status`, `freshness_status`: original feed quality labels.

Price-change percentage = (new upfront / earlier upfront - 1) × 100, only
within a series. Renewal increase = (normalized renewal monthly / effective
intro monthly - 1) × 100. Calculations use published numbers, rounded at the
output, so tiny rounding differences can occur. Renewal increases are projected
from disclosed terms, not observed future invoices. Reference discount
percentages and historical price-change percentages answer different questions.

## Source changes, gaps and monthly comparisons

The source change ledger documents known discontinuities. On September 9, Proton
VPN collection moved from standard pricing ($83.76/24 months) to a partner
page ($71.76/24 months). That difference is excluded from historical price-cut
statistics. Charts break at every series change and missing fresh day rather
than joining incomparable records or interpolating gaps. Daily chart points
use the final fresh observation of each day; intraday observations and events
remain downloadable and a chart can therefore omit a brief intraday movement.

Monthly endpoint comparisons use the first and last available snapshots in that
month. Both endpoints must be trend eligible and no context/source switch may intervene.
They do not measure within-month volatility. Events follow consecutive eligible
extractions, including intraday captures; a gap means the effective change time is
unknown. No average blends currencies, different durations, or source channels. Endpoint denominators count plans, not providers. Multiple plans from the same provider are not independent observations. All reported movements remain provisional until manually checked.

## Reproducibility, refresh and revisions

`python scripts/build_price_history.py` builds every completed month starting
September 2026. The daily private exporter runs it after sanitized snapshots are
published into the public checkout; the public repository CI independently
rebuilds in `--check` mode. DoVPN downloads the public monthly index and releases
at build time; its scheduled production builds pick up new completed months.
A network failure uses the checked-in accepted release and displays its actual
coverage. No page advances its coverage date merely because it rebuilt.

A frozen release is append-only. Conflicting regeneration fails instead of
rewriting history. Corrections require a new revision identifier, a ledger
entry explaining old/new values and evidence, and a new checksum and citation.
New monthly report pages are generated from the accepted release; editorial
news stories require a separate evidence-based write-up.

Citation: Price, Steve. VPN Price Transparency Index: provisional all-provider
price history, [month year]. Release [release_id]. CC BY 4.0. Include the
observed market and currency, coverage period, release URL and access date.
No DOI is implied. DoVPN earns affiliate revenue on its commercial pages;
research pages contain no affiliate purchase links. No provider response was
requested before this September analysis; corrections can be submitted via
the public repository or steve@dovpn.com.

## Release field structure

Every public snapshot contains a `providers` coverage array with all 29 IDs and
a `records` array with every available plan. Numeric fields preserve a parallel
`_status` (machine_extracted, derived, not_visible, ambiguous, not_applicable,
not_collected, checkout_observed or derived_from_checkout). `sources` and
`policy_sources` retain only page ID, public URL, result, method and content
hash. CSV exports include major quality fields and serialized review-flag lists;
JSON preserves full provenance and extraction states. Month-end `summary.plans`
contains all plans, while `summary.providers` includes every provider regardless
of trend eligibility. No blocked provider disappears from the cohort.

Policy-derived renewal values are useful evidence but should be checked against
the cited policy before publication as a consumer claim. Terms conflicts,
ambiguous reference DOM, missing-duration/total, uncollected checkout facts,
and ambiguous lifetime definitions block price-trend eligibility. Carried
forward rows are downloadable but never plotted as fresh observations.

## Amnezia correction in September v2

The two-year plan was missed by a parser limited to six months and one year.
V2 restores $80 for 24 months from successful archived captures beginning
September 2 at 04:45:06 UTC, alongside the first $30 / six-month and $50 / annual
observations. It does not infer that the new plan caused the shorter-plan rises.
The correction date and reason are explicit in recovered rows. No row is added
before the source first displayed the offer. See `CORRECTIONS.md` for the changed
coverage counts and archived release details.
