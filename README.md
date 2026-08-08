# VPN Price Transparency Index

An independent, versioned record of the real introductory cost and renewal
terms of consumer VPN subscriptions. The project is maintained by Steve Price
([ORCID 0009-0009-6603-6878](https://orcid.org/0009-0009-6603-6878)).

## Status

Version `0.1.0` establishes the research contract, 20-provider population,
validation tools, and publication format. Automated collection runs in a
separate private repository so raw pages, screenshots, network details,
cookies, and collection credentials cannot leak into this public dataset.

No price observation is published merely because a page was fetched. A record
must pass schema validation and the review gate described in
[`methodology/collection-method.md`](methodology/collection-method.md).

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

