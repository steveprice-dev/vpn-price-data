#!/usr/bin/env python3
"""Validate schemas, calculations, identifiers, and the public-data boundary."""

from __future__ import annotations

import ipaddress
import json
import re
import hashlib
from decimal import Decimal
from pathlib import Path
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
ORCID = "https://orcid.org/0009-0009-6603-6878"


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def validate_schema(instance: dict, schema_path: Path, label: str) -> list[str]:
    validator = Draft202012Validator(load(schema_path), format_checker=FormatChecker())
    return [f"{label}: {'/'.join(map(str, error.path))}: {error.message}" for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))]


def dec(field: dict) -> Decimal | None:
    return None if field["value"] is None else Decimal(str(field["value"]))


def close(left: Decimal, right: Decimal, tolerance: Decimal = Decimal("0.011")) -> bool:
    return abs(left - right) <= tolerance


def semantic_checks(snapshot: dict, provider_ids: set[str]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for item in snapshot["observations"]:
        prefix = item["observation_id"]
        if prefix in seen:
            errors.append(f"duplicate observation_id: {prefix}")
        seen.add(prefix)
        if item["provider_id"] not in provider_ids:
            errors.append(f"{prefix}: provider_id is outside the prespecified population")
        if item["quality"]["validation_state"] != "manually_verified":
            errors.append(f"{prefix}: unreviewed observation crossed the public boundary")
        reviewer = item["quality"]["reviewer_orcid"]
        if reviewer != ORCID:
            errors.append(f"{prefix}: reviewer ORCID is missing or unexpected")
        parsed = urlsplit(item["evidence"]["primary_url"])
        if parsed.query or parsed.fragment:
            errors.append(f"{prefix}: public evidence URL contains query or fragment")
        service = item["pricing"]["service_months"]
        paid = item["pricing"]["paid_months"]
        free = item["pricing"]["free_months"]
        if all(field["state"] == "observed" for field in (service, paid, free)):
            if service["value"] != paid["value"] + free["value"]:
                errors.append(f"{prefix}: service_months does not equal paid_months + free_months")
        upfront = dec(item["pricing"]["upfront_total"])
        effective = dec(item["pricing"]["effective_intro_monthly"])
        if upfront is not None and effective is not None and service["value"]:
            if not close(effective, upfront / Decimal(service["value"])):
                errors.append(f"{prefix}: effective_intro_monthly is inconsistent")
        renewal_total = dec(item["renewal"]["total"])
        renewal_monthly = dec(item["renewal"]["normalized_monthly"])
        renewal_period = item["renewal"]["period_months"]["value"]
        if renewal_total is not None and renewal_monthly is not None and renewal_period:
            if not close(renewal_monthly, renewal_total / Decimal(renewal_period)):
                errors.append(f"{prefix}: renewal_normalized_monthly is inconsistent")
    return errors


def leakage_checks() -> list[str]:
    errors: list[str] = []
    suspicious = re.compile(r"(?i)(api[_-]?key|authorization:|set-cookie:|sessionid|private[_-]?key|scraperapi_key)")
    ipv4 = re.compile(r"(?<![0-9])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![0-9])")
    for path in sorted((ROOT / "data").rglob("*")):
        if not path.is_file():
            continue
        text = path.read_text(errors="replace")
        if suspicious.search(text):
            errors.append(f"{path.relative_to(ROOT)}: possible secret or cookie label")
        for candidate in ipv4.findall(text):
            try:
                ipaddress.ip_address(candidate)
            except ValueError:
                continue
            errors.append(f"{path.relative_to(ROOT)}: public data contains an IPv4 address")
    return errors


def operational_checks(feed: dict, provider_ids: set[str]) -> list[str]:
    errors: list[str] = []
    expected = {"nordvpn", "surfshark", "privadovpn", "expressvpn", "purevpn", "cyberghost", "protonvpn", "pia", "ipvanish", "tunnelbear"}
    actual = [item["provider_id"] for item in feed["records"]]
    if set(actual) != expected or len(actual) != len(set(actual)):
        errors.append("operational feed provider set is incomplete or duplicated")
    for item in feed["records"]:
        prefix = f"operational:{item['provider_id']}"
        if item["provider_id"] not in provider_ids:
            errors.append(f"{prefix}: provider is outside the registry")
        if item["service_months"] != item["paid_months"] + item["free_months"]:
            errors.append(f"{prefix}: service duration does not reconcile")
        if not close(Decimal(str(item["effective_intro_monthly"])), Decimal(str(item["upfront_total"])) / Decimal(item["service_months"])):
            errors.append(f"{prefix}: effective introductory price does not reconcile")
        if (item["discount_percent"] is None) != (item["discount_basis"] is None):
            errors.append(f"{prefix}: discount value and basis are inconsistent")
        reference_values_missing = item["reference_price_total"] is None or item["reference_monthly_equivalent"] is None
        if reference_values_missing != (item["reference_price_basis"] is None):
            errors.append(f"{prefix}: reference price values and basis are inconsistent")
        if not reference_values_missing and not close(
            Decimal(str(item["reference_price_total"])),
            Decimal(str(item["reference_monthly_equivalent"])) * Decimal(item["service_months"]),
        ):
            errors.append(f"{prefix}: reference price total does not reconcile")
        if item["renewal_total"] is None:
            if item["renewal_period_months"] is not None or item["effective_renewal_monthly"] is not None:
                errors.append(f"{prefix}: partial renewal data crossed the boundary")
        elif not close(Decimal(str(item["effective_renewal_monthly"])), Decimal(str(item["renewal_total"])) / Decimal(item["renewal_period_months"])):
            errors.append(f"{prefix}: effective renewal price does not reconcile")
        parsed = urlsplit(item["source_url"])
        if parsed.query or parsed.fragment:
            errors.append(f"{prefix}: source URL contains query or fragment")
        fingerprint_source = {
            key: value for key, value in item.items()
            if key not in {
                "observed_at", "materially_changed_at", "freshness_status",
                "content_fingerprint", "source_url", "evidence_sha256",
                "validation_status",
            }
        }
        expected_fingerprint = hashlib.sha256(
            json.dumps(fingerprint_source, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        if item["content_fingerprint"] != expected_fingerprint:
            errors.append(f"{prefix}: content fingerprint does not match")
    return errors


def main() -> int:
    providers = load(ROOT / "data" / "providers.json")
    errors = validate_schema(providers, ROOT / "schemas" / "providers.schema.json", "providers")
    ids = [item["id"] for item in providers["providers"]]
    if len(ids) != len(set(ids)):
        errors.append("provider IDs are not unique")
    if len(ids) != 29:
        errors.append(f"expected 29 providers in the pre-observation development panel, found {len(ids)}")
    expected_permissioned = {"torguard", "privadovpn", "fastestvpn", "x-vpn"}
    actual_permissioned = {
        item["id"] for item in providers["providers"]
        if item.get("automation_basis") == "permission_reported_by_research_owner"
        and item.get("review_requirement") == "permissioned_manual_review"
    }
    if actual_permissioned != expected_permissioned:
        errors.append("permissioned manual-review provider set does not match the recorded exceptions")
    operational_allowed = {
        item["id"] for item in providers["providers"]
        if item.get("operational_processing") == "automated_validated_allowed"
    }
    if operational_allowed != {"privadovpn"}:
        errors.append("automated operational exception set does not match the recorded permission")
    overlap = set(ids) & {item["id"] for item in providers["watchlist"]}
    if overlap:
        errors.append(f"providers also appear on watchlist: {sorted(overlap)}")
    snapshots = [ROOT / "data" / "latest.json", *sorted((ROOT / "data" / "observations").glob("*.json"))]
    for path in snapshots:
        snapshot = load(path)
        errors.extend(validate_schema(snapshot, ROOT / "schemas" / "observation.schema.json", str(path.relative_to(ROOT))))
        errors.extend(semantic_checks(snapshot, set(ids)))
    operational_paths = [ROOT / "feeds" / "dovpn" / "latest.json", *sorted((ROOT / "feeds" / "dovpn" / "snapshots").glob("*.json"))]
    for path in operational_paths:
        if not path.exists():
            errors.append(f"missing operational feed: {path.relative_to(ROOT)}")
            continue
        feed = load(path)
        errors.extend(validate_schema(feed, ROOT / "schemas" / "operational-feed.schema.json", str(path.relative_to(ROOT))))
        errors.extend(operational_checks(feed, set(ids)))
    errors.extend(leakage_checks())
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated {len(ids)} providers and {len(snapshots)} snapshot file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
