"""Semantic checks shared by public validation and export tests."""
import hashlib
from datetime import datetime
from decimal import Decimal
from urllib.parse import urlsplit


def comparison_checks(feed: dict, provider_ids: set[str]) -> list[str]:
    errors, identities = [], set()
    for row in feed["records"]:
        label = row["offer_key"]
        def fail(message):
            errors.append(f"comparison:{label}: {message}")
        if label in identities:
            fail("duplicate offer")
        identities.add(label)
        if row["provider_id"] not in provider_ids:
            fail("provider outside registry")
        url = urlsplit(row["source_url"])
        if url.scheme != "https" or url.username or url.password or url.query or url.fragment:
            fail("unsafe source URL")
        route = hashlib.sha256(row["source_url"].encode()).hexdigest()[:16]
        expected = ":".join(row[k] for k in ("provider_id", "plan_id", "country_code", "currency")) + ":" + route
        if expected != label:
            fail("offer identity does not match source route")
        if row["service_months"] != row["paid_months"] + row["free_months"]:
            fail("duration mismatch")
        if abs(Decimal(str(row["upfront_total"])) / row["service_months"] - Decimal(str(row["effective_intro_monthly"]))) > Decimal("0.011"):
            fail("introductory arithmetic mismatch")
        if row["upfront_total_status"] == "derived" and row["service_months"] != 1:
            fail("unconfirmed multi-month upfront amount")
        if row["renewal_total"] is None:
            if row["renewal_total_status"] not in {"not_visible", "not_applicable", "ambiguous"}:
                fail("null renewal has numeric status")
            if row["renewal_period_months"] is not None or row["effective_renewal_monthly"] is not None:
                fail("partial renewal data")
        elif row["renewal_total_status"] in {"not_visible", "not_applicable", "ambiguous"}:
            fail("unusable renewal status has a numeric value")
        elif not row["renewal_period_months"] or row["effective_renewal_monthly"] is None:
            fail("incomplete numeric renewal")
        elif abs(Decimal(str(row["renewal_total"])) / row["renewal_period_months"] - Decimal(str(row["effective_renewal_monthly"]))) > Decimal("0.011"):
            fail("renewal arithmetic mismatch")
        if row["billing_type"] == "non_recurring_prepaid" and (row["renewal_total"] is not None or row["renewal_total_status"] != "not_applicable"):
            fail("prepaid renewal conflict")
        if row["renewal_total_status"] == "not_applicable" and row["billing_type"] != "non_recurring_prepaid":
            fail("renewal applicability conflict")
        changed = datetime.fromisoformat(row["materially_changed_at"].replace("Z", "+00:00"))
        observed = datetime.fromisoformat(row["observed_at"].replace("Z", "+00:00"))
        if changed > observed:
            fail("material change postdates observation")
        age = (datetime.fromisoformat(feed["generated_at"].replace("Z", "+00:00")) - datetime.fromisoformat(row["observed_at"].replace("Z", "+00:00"))).total_seconds() / 3600
        if not -1 <= age <= 48:
            fail("record was stale at publication")
    return errors
