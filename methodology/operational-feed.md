# Operational website feed

The `feeds/dovpn/` files are a sanitized, machine-validated view of the US/USD
offers displayed on DoVPN. They exist so reader-facing prices, totals, plan
durations, included months and renewal disclosures can be refreshed without
publishing private captures.

This feed is distinct from `data/latest.json`. The research dataset contains
only manually reviewed observations. An operational record is labelled
`automated_validated` and must not be cited as if a researcher manually checked
the day's checkout.

## Publication rules

An operational record is published only when it:

- matches the prespecified provider, plan family, US market and USD currency;
- comes from a current capture and contains the core introductory-cost fields;
- reconciles the full charge, service duration and effective monthly cost;
- retains an HTTPS provider source and its content digest; and
- stays within automated continuity checks against the last accepted record.

If a new candidate fails those checks, the feed retains the last known good
record and marks it accordingly. `renewal_total_status` distinguishes a genuinely
unavailable renewal amount from a plan where renewal is not applicable, while
`billing_type` records whether the selected offer is recurring or prepaid.
Consumers should not interpret a null renewal amount without these fields.
Missing renewal or refund information is never converted into a claim that the
term does not exist.

`discount_basis` distinguishes a provider-displayed percentage from one
calculated from the recorded reference total. `reference_price_basis`
distinguishes a provider-displayed full-plan comparison total from a total
derived by multiplying the provider's current monthly plan by the promotional
service duration. These basis fields prevent a derived comparison from being
presented as a checkout charge.

Raw HTML, screenshots, cookies, network details, checkout paths, runner
metadata and internal review notes remain private. The public operational feed
contains only the commercial facts needed to explain an offer and reproduce
the displayed comparison.

## Website use

The advertised monthly equivalent is useful for comparing plans of different
lengths, but long plans are normally charged upfront. A consuming page should
therefore show the monthly equivalent together with the total due, paid and
included months, renewal terms when available, market, currency and observation
date. The provider checkout remains authoritative.
