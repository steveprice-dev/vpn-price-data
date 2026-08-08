# Collection method

## Research question

How do the displayed price, immediate payment, service duration, renewal terms,
tax disclosure, refund window, and cancellation path of consumer VPN plans
change over time and across fixed markets?

## Unit and panel

One observation represents one provider, one named plan, one country market,
and one UTC capture time. The initial panel is prespecified in
`data/providers.json`; inclusion does not imply endorsement or ranking.

The 25-provider development panel is fixed before the first reviewed price
observation. Providers whose published terms prohibit automated monitoring are
excluded from the panel rather than placed in a daily manual queue. The dated
decision record and permission path are published in
`methodology/automation-eligibility.md`.

The first automated GitHub-hosted runner is a discovery and change-detection
stream. Its country is not assumed from the runner label. A public US or
Netherlands observation requires a verified country vantage point or a manual
local capture. A generic `EU` proxy is not recorded as the Netherlands and is
insufficient for a VAT conclusion.

## Collection layers

1. A direct, rate-limited fetch records the final public URL, HTTP result,
   content hash, capture time, and immutable private evidence.
2. A proxy may be used only when configured for a provider, the requested
   country is verifiable, and a per-run cost ceiling is set. Proxy use is
   recorded; it never silently replaces a direct result.
3. Automated parsing creates draft values. A fetch failure is recorded as a
   failure, not as evidence that a plan disappeared.
4. Checkout, renewal visibility, tax, and cancellation claims require manual
   verification where the public page is insufficient.
5. Only manually verified, schema-valid observations are exported. Public
   files contain facts, source URLs, and hashes, not raw HTML, cookies,
   screenshots with personal data, IP addresses, or credentials.

## Schedule

The intended Black Friday 2026 panel is collected daily from August through
the first week after Cyber Monday. Scheduled jobs run away from the top of the
hour because GitHub warns that high-load schedules can be delayed or dropped.
An absent scheduled run remains a gap; it is never backfilled with an assumed
price.

## Black Friday comparison

The ordinary-price baseline is computed from reviewed observations before a
prespecified sale window. Provider discount claims are recorded but not used
as the study's reference price. Analysis compares actual payable totals and
normalized monthly costs with the provider's own earlier observations.

Candidate findings are not preregistered conclusions. Claims such as a raised
reference price, an unchanged pre-sale offer, or an unusually large renewal
increase are published only when the dated observations support them.

## Limitations

Displayed prices can vary by affiliate route, cookies, account history,
payment method, device, experiment, and tax location. The dataset describes
the specified capture conditions, not every customer's price. A public page
does not prove the final checkout total, and support documentation does not
prove the number of cancellation steps in a real account.
