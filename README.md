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
