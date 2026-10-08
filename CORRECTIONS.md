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

