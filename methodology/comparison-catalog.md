# Multi-plan comparison catalog

`feeds/dovpn/comparison/latest.json` is a separate operational export for comparing monthly, annual and longer paid plans. It does not change the ten-record featured feed or constitute a manually reviewed research release.

Version 1 covers accepted records for the ten featured providers plus Windscribe and Mullvad. Coverage depends on successful captures. It is not a complete market inventory. Surfshark and ExpressVPN currently lack monthly records in the captured catalog. Free plans are excluded from this paid-plan calculation catalog and can be described separately from provider documentation.

## Evidence and selection

Each offer identifies the provider, plan, observed country, currency, source URL, capture time and evidence hash. Source route is part of offer identity: a partner landing page is not silently merged with a standard public offer. US observations in EUR remain US/EUR observations; they are not UK prices or a currency conversion.

Records pass arithmetic, market, age, extraction-state and unresolved-flag checks before export. Upfront totals for longer plans require a displayed total or checkout observation; a one-month total may equal its displayed monthly charge. `upfront_total_status` distinguishes these cases. Automated checkout observation does not imply an independent human review.

New records must come from the current capture and be no older than 48 hours at generation. Rejected and carried-forward observations stay outside this catalog. Consumers must check age again at use time, because a saved JSON file can become stale. Generation time is not a replacement for each record's observation time. `materially_changed_at` retains the earlier date when a recapture changes only its observation timestamp or evidence hash; it advances when offer terms change. It cannot postdate the observation.

## Billing and uncertainty

`paid_months + free_months = service_months`. The monthly equivalent is a comparison unit; `upfront_total` is the initial payment. Renewal amount, interval and status remain separate. A missing renewal amount is unknown, not zero. Non-recurring prepaid coverage ends after its included period; the catalog makes no promise of another purchase at the same price.

Refund ambiguity is represented by a null amount and explicit status. Specific payment-method exclusions are retained where supported. Tax presentation is recorded, but a displayed price may exclude tax that depends on checkout details. Confirm final terms with the provider before purchase.

## Publication boundary

The export uses an explicit field allowlist. It excludes raw captures, private paths, IP addresses, identity documents, credentials, cookies, checkout session URLs and internal review notes. Source URLs contain no query strings or fragments. Timestamped snapshots are immutable; checksum files cover both the schema and exported snapshots.

This catalog supports operational comparisons. Versioned research releases still require their own review, method, population, correction record and publication gate.
