# VPN Price Transparency Index

An independent, versioned record of introductory prices and renewal terms for
consumer VPN subscriptions. The project is maintained by Steve Price
([ORCID 0009-0009-6603-6878](https://orcid.org/0009-0009-6603-6878)).

## Status

Version `0.3.0` defines the research contract, 29-provider population,
validation tools, and publication format. Collection takes place in a separate
private repository. Raw pages, screenshots, network details, cookies, and
collection credentials are not part of this public dataset.

The project does not publish a price observation simply because it was
collected. Every record must pass schema validation and the review gate
described in the
[`collection method`](methodology/collection-method.md).

The separate [`feeds/dovpn/latest.json`](feeds/dovpn/latest.json) file is a
validated operational feed for prices shown on the [DoVPN website](https://dovpn.com/).
It is not a substitute for the manually reviewed research dataset. See
[`methodology/operational-feed.md`](methodology/operational-feed.md).

## What this measures

One observation is one provider, one plan, one market, and one UTC capture
time. The fields keep these commonly confused values separate:

- the monthly equivalent shown in advertising;
- the total charged at purchase;
- paid and included free months;
- the effective introductory monthly cost over the full service period;
- the first renewal amount and renewal period;
- the normalized monthly renewal increase;
- refund, tax, disclosure, and cancellation evidence.

Missing evidence is explicit. `not_visible`, `blocked`, `ambiguous`,
`not_collected`, and `not_applicable` never collapse into an empty value or a
claim that a term does not exist.

## Repository map

```text
data/providers.json            Provider population and inclusion basis
data/observations/             Immutable reviewed daily snapshots
data/latest.json               Most recent reviewed snapshot
data/latest.csv                Flat export of the most recent snapshot
data/latest.md                 GitHub-rendered table of the latest snapshot
feeds/dovpn/latest.json        Current automated operational website feed
feeds/dovpn/snapshots/         Versioned operational feed history
schemas/                       JSON Schemas
methodology/                   Collection, field, renewal, and manual protocols
metadata/                      Release and repository-deposit metadata
scripts/validate.py            Contract and leakage checks
scripts/build_exports.py       Deterministic CSV and checksum generation
CHANGELOG.md                   Version history
CORRECTIONS.md                 Public correction ledger
CITATION.cff                   Citation metadata
```

## Validate and rebuild

```bash
python -m pip install -r requirements.txt
python scripts/build_exports.py --check
python scripts/validate.py
python -m unittest discover -s tests
```

## Reuse and citation

Data, schemas, methodology, and original prose are licensed under CC BY 4.0.
Code is licensed under MIT. Cite the exact tagged release or dated snapshot
used. Provider names and trademarks remain the property of their owners.

Corrections are welcome through the correction issue form. A correction must
identify the observation and provide a primary source or reproducible evidence.

The [latest reviewed table](data/latest.md) is generated from the same snapshot
as the JSON and CSV exports. It is empty until the first manual review is
complete; raw automated captures are intentionally not displayed as results.

## Full tracked population and monthly history

[All-provider catalog](feeds/price-tracking/latest.json) publishes sanitized
extractions for **all 29 tracked providers and every extracted plan**, independently
of which providers are featured on DoVPN. [Daily/intraday snapshots](feeds/price-tracking/snapshots)
retain the available history from August 11, 2026. Explicit provider coverage,
missing values, extraction states, source pages, evidence hashes, review flags
and carried-forward states remain visible. These records are **automated and
unreviewed**, not manually verified research. No raw captures or private paths
are published. Trend eligibility means the arithmetic, source and freshness
checks pass; it is not a human verification claim.

[September 2026 frozen release](data/price-history/releases/price-history-2026-09-v1)
contains JSON, CSV, monthly summary and SHA-256 checksums.
The [monthly index](data/price-history/index.json) is the entry point for consumers.
[Methods](methodology/price-history.md) explain eligibility, gaps, source and
extraction changes, renewal calculations, and citation.
The Proton standard-to-partner source switch is documented in the
[source ledger](data/price-history/source-changes.json), and excluded from
same-source price-cut statistics. Earlier snapshots are unchanged.

The daily private exporter publishes full-provider snapshots and builds
completed-month releases. Public CI independently regenerates each release in
check mode. Frozen files cannot silently change.

```sh
python scripts/build_price_history.py --month 2026-09
python scripts/build_price_history.py --check
```

Cite: Price, Steve. *VPN Price Transparency Index: provisional all-provider
price history, September 2026*. Release `price-history-2026-09-v1`. CC BY 4.0.
Identify the exact release, currency, offer context and automated unreviewed
evidence status. No DOI has been assigned to this release.
