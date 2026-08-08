# Data dictionary

## Evidence states

- `observed`: directly visible and recorded.
- `not_visible`: the capture succeeded but the field was not displayed in the
  inspected scope.
- `not_applicable`: the concept does not apply to this plan.
- `blocked`: collection could not inspect the field because access was blocked.
- `ambiguous`: multiple plausible values were visible and could not be resolved.
- `not_collected`: the collection protocol did not attempt this field.

`not_visible` never means that a term does not exist.

## Key derived values

`service_months = paid_months + free_months`

`effective_intro_monthly = upfront_total / service_months`

`renewal_normalized_monthly = renewal_total / renewal_period_months`

`renewal_increase_pct = 100 × (renewal_normalized_monthly /
effective_intro_monthly − 1)`

Calculations use exact decimal arithmetic and are rounded only for publication.
Tax treatment must be comparable between the introductory and renewal amounts
before the increase is calculated. If it is not comparable, the increase state
is `ambiguous` or `not_collected`.

## Disclosure stages

`pricing_page`, `offer_terms`, `cart`, `checkout`, and `after_purchase` identify
the earliest verified stage at which the first renewal amount was visible.
`not_visible` means it was not found in the inspected stages; `not_collected`
means those stages were not inspected.

## Cancellation steps

A step is a deliberate user action after entering the account area: opening a
subscription control, choosing cancel, answering retention prompts, confirming,
or contacting support. Login and optional surveys are recorded in private
notes but are not counted unless they are mandatory to complete cancellation.

