# Manual collection protocol

This protocol covers facts that a server-side fetch cannot establish reliably.

## Prepare one market session

1. Use a fresh browser profile with no VPN-provider cookies, affiliate
   parameters, logged-in account, or extensions that rewrite prices.
2. Record date/time in UTC, physical country, network basis, browser version,
   language, currency, and whether tax location was selected explicitly.
3. Open the canonical pricing URL from `data/providers.json`, not a DoVPN or
   affiliate link. Preserve the final clean URL without query parameters.
4. Capture full-page evidence privately. Do not include personal information,
   IP addresses, payment data, cookies, or subscription credentials.

## Pricing and checkout

1. Record every consumer VPN-only plan shown, with the provider's exact plan
   name. Keep bundled identity, storage, antivirus, and dedicated-IP add-ons
   separate.
2. Record displayed monthly equivalent, upfront total, paid months, free
   months, discount claim, reference price, refund period, and tax wording.
3. Follow the purchase path to the last screen before payment. Do not complete
   a purchase unless the account is intentionally part of the cancellation
   study.
4. Record the earliest stage where the first renewal amount and duration are
   visible. If absent, use `not_visible`; do not guess from the monthly list
   price.
5. Recalculate service months, effective introductory monthly price, renewal
   monthly price, and comparable renewal increase using the data dictionary.

Repeat separately for a US session and a local Netherlands session. Do not
label a region-level EU proxy as Netherlands evidence.

## Cancellation study

1. Use only a subscription the researcher is authorized to manage.
2. Record purchase channel because web, Apple, and Google subscriptions have
   different cancellation paths.
3. Start after login and count required deliberate actions using the data
   dictionary. Record mandatory chat, email, retention prompts, and waiting
   periods.
4. Capture evidence privately before and after cancellation. Redact account
   IDs, email, payment details, IP addresses, and support-agent personal data.
5. Confirm the subscription status and service end date. A help article alone
   is not a tested step count.

## Review and publication

Enter one record per provider, plan, market, and capture time. Run validation,
inspect derived values, and compare against the private evidence. Publish only
after setting `quality.validation_state` to `manually_verified` and recording
the reviewer ORCID.

