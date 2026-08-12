#!/usr/bin/env python3
"""Build deterministic latest CSV and checksum files from reviewed snapshots."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBSERVATIONS = ROOT / "data" / "observations"
LATEST_JSON = ROOT / "data" / "latest.json"
LATEST_CSV = ROOT / "data" / "latest.csv"
LATEST_MD = ROOT / "data" / "latest.md"
CHECKSUMS = ROOT / "metadata" / "SHA256SUMS"
OPERATIONAL_LATEST = ROOT / "feeds" / "dovpn" / "latest.json"
OPERATIONAL_SNAPSHOTS = ROOT / "feeds" / "dovpn" / "snapshots"

COLUMNS = [
    "observation_id", "provider_id", "provider_name", "plan_id", "plan_name",
    "market_country", "currency", "captured_at", "advertised_monthly",
    "upfront_total", "paid_months", "free_months", "service_months",
    "effective_intro_monthly", "advertised_discount_pct", "renewal_total",
    "renewal_period_months", "renewal_normalized_monthly", "renewal_increase_pct",
    "renewal_disclosure_stage", "refund_days", "vat_treatment",
    "cancellation_steps", "collection_method", "validation_state", "primary_url",
    "evidence_sha256",
]


def load_latest() -> dict:
    snapshots = sorted(OBSERVATIONS.glob("*.json"))
    if snapshots:
        return json.loads(snapshots[-1].read_text())
    return json.loads(LATEST_JSON.read_text())


def value(record: dict) -> str:
    raw = record.get("value")
    return "" if raw is None else str(raw)


def csv_text(snapshot: dict) -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=COLUMNS, lineterminator="\n")
    writer.writeheader()
    for item in snapshot["observations"]:
        writer.writerow({
            "observation_id": item["observation_id"],
            "provider_id": item["provider_id"],
            "provider_name": item["provider_name"],
            "plan_id": item["plan_id"],
            "plan_name": item["plan_name"],
            "market_country": item["market"]["country_code"],
            "currency": item["market"]["currency"],
            "captured_at": item["captured_at"],
            "advertised_monthly": value(item["pricing"]["advertised_monthly"]),
            "upfront_total": value(item["pricing"]["upfront_total"]),
            "paid_months": value(item["pricing"]["paid_months"]),
            "free_months": value(item["pricing"]["free_months"]),
            "service_months": value(item["pricing"]["service_months"]),
            "effective_intro_monthly": value(item["pricing"]["effective_intro_monthly"]),
            "advertised_discount_pct": value(item["pricing"]["advertised_discount_pct"]),
            "renewal_total": value(item["renewal"]["total"]),
            "renewal_period_months": value(item["renewal"]["period_months"]),
            "renewal_normalized_monthly": value(item["renewal"]["normalized_monthly"]),
            "renewal_increase_pct": value(item["renewal"]["increase_pct"]),
            "renewal_disclosure_stage": item["renewal"]["disclosure_stage"],
            "refund_days": value(item["terms"]["refund_days"]),
            "vat_treatment": item["terms"]["vat_treatment"],
            "cancellation_steps": value(item["cancellation"]["steps"]),
            "collection_method": item["quality"]["collection_method"],
            "validation_state": item["quality"]["validation_state"],
            "primary_url": item["evidence"]["primary_url"],
            "evidence_sha256": item["evidence"]["content_sha256"],
        })
    return output.getvalue()


def markdown_text(snapshot: dict) -> str:
    lines = ["# Latest reviewed VPN price observations", ""]
    if not snapshot["observations"]:
        lines.extend([
            "No manually reviewed observations have been published yet.",
            "",
            "Automated captures remain private until their pricing and terms are verified.",
            "",
        ])
        return "\n".join(lines)
    lines.extend([
        f"Observation date: **{snapshot['observation_date']}**", "",
        "| Provider | Plan | Market | Upfront total | Effective intro/month | Renewal/month | Renewal increase |",
        "|---|---|---:|---:|---:|---:|---:|",
    ])
    for item in snapshot["observations"]:
        pricing = item["pricing"]
        renewal = item["renewal"]
        currency = item["market"]["currency"]
        shown = lambda field: "—" if field["value"] is None else f"{field['value']} {currency}"
        increase = "—" if renewal["increase_pct"]["value"] is None else f"{renewal['increase_pct']['value']}%"
        lines.append(
            f"| {item['provider_name']} | {item['plan_name']} | {item['market']['country_code']} | "
            f"{shown(pricing['upfront_total'])} | {shown(pricing['effective_intro_monthly'])} | "
            f"{shown(renewal['normalized_monthly'])} | {increase} |"
        )
    lines.append("")
    return "\n".join(lines)


def checksum_text() -> str:
    targets = [
        ROOT / "data" / "providers.json",
        LATEST_JSON,
        LATEST_CSV,
        LATEST_MD,
        ROOT / "schemas" / "observation.schema.json",
        ROOT / "schemas" / "providers.schema.json",
        ROOT / "schemas" / "operational-feed.schema.json",
    ] + sorted(OBSERVATIONS.glob("*.json"))
    if OPERATIONAL_LATEST.exists():
        targets.append(OPERATIONAL_LATEST)
    if OPERATIONAL_SNAPSHOTS.exists():
        targets.extend(sorted(OPERATIONAL_SNAPSHOTS.glob("*.json")))
    lines = []
    for path in targets:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(ROOT).as_posix()}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    snapshot = load_latest()
    expected_json = json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n"
    expected_csv = csv_text(snapshot)
    expected_md = markdown_text(snapshot)
    if args.check:
        errors = []
        if LATEST_JSON.read_text() != expected_json:
            errors.append("data/latest.json is not the newest deterministic snapshot")
        if LATEST_CSV.read_text() != expected_csv:
            errors.append("data/latest.csv is stale")
        if LATEST_MD.read_text() != expected_md:
            errors.append("data/latest.md is stale")
        if CHECKSUMS.exists() and CHECKSUMS.read_text() != checksum_text():
            errors.append("metadata/SHA256SUMS is stale")
        if errors:
            raise SystemExit("\n".join(errors))
        return 0
    LATEST_JSON.write_text(expected_json)
    LATEST_CSV.write_text(expected_csv)
    LATEST_MD.write_text(expected_md)
    CHECKSUMS.write_text(checksum_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
