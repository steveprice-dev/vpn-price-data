# Corrections log

## 2026-10-08: Proton VPN source-series annotation

Affected observations: Proton VPN Plus 24-month records immediately before
and after `2026-09-09T06:39:14Z`. Standard pricing
`https://protonvpn.com/pricing` ($83.76 upfront) was replaced by
`https://protonvpn.com/l/special-partner-offer` ($71.76 upfront).
The interpretation is corrected: this is a source switch, not an observed
same-source price cut. Values and URLs are retained. Monthly analysis starts
a separate series and excludes the difference from price-change statistics.
Evidence: operational snapshots `20260909T045337Z.json` and
`20260909T063956Z.json`; see `data/price-history/source-changes.json`.
Included in `price-history-2026-09-v1`. No earlier snapshot was rewritten.

Corrections will record the date, affected observation ID, old value, corrected
value, reason, evidence, and release containing the correction. Earlier tagged
releases and checksums remain unchanged.


## 2026-10-09: USD scope and Amnezia two-year parser correction

`price-history-2026-09-v2` supersedes v1 for current reporting. USD is the only
active research currency. EUR and GBP test observations are excluded, without
conversion. The earlier v1 release and `feeds/price-tracking/` snapshots remain
archived, with their original hashes, for citations and reproducibility. New
sanitized snapshots are published in `feeds/price-tracking-usd/`; the monthly
index lists the active USD revisions.

The Amnezia parser previously recognized only six-month and annual offers.
The original archived pricing capture at `2026-09-02T04:45:06Z` already displayed
“2 Years $80.00”, alongside “6 Months $30.00” and “1 Year $50.00”. The previous
September 1 capture listed only $28 / six months and $48 / one year. USD snapshots
recover the missed $80 / 24-month row only where the original successful pricing
capture contains it. `captured_at` stays at the original capture time;
`extraction_corrected_at=2026-10-09` and
`extraction_correction=amnezia_24_month_parser_omission` identify the later repair.
Raw HTML stays private; each public row carries the original evidence SHA-256.
No prices are backdated into captures that do not show this offer.

September coverage changes from 124 to 114 month-end plans, and from 88 to 78
comparable USD plans: 73 unchanged, four higher and one lower. The newly recovered
Amnezia plan is excluded from opening-to-closing comparisons because it was not
present at the month's opening. All 29 providers remain visible in coverage;
AirVPN, AzireVPN and Mullvad have no extracted USD offers in this release.

The new plan and the shorter-plan increases were first observed in the same
capture. This timing does not establish why Amnezia raised those prices.
