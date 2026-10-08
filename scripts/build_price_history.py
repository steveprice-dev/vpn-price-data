#!/usr/bin/env python3
"""Freeze reproducible monthly analyses of the sanitized operational panel.

Never upgrades automated observations to manually reviewed research.
"""
from __future__ import annotations
import argparse, calendar, csv, hashlib, io, json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTEXT = ('plan_id', 'country_code', 'currency', 'paid_months', 'free_months', 'billing_type', 'source_url')
COLUMNS = ['snapshot_at', 'snapshot_date', 'provider_id', 'provider_name', 'plan_id', 'plan_name', 'country_code', 'currency', 'observed_at', 'upfront_total', 'paid_months', 'free_months', 'service_months', 'effective_intro_monthly', 'effective_renewal_monthly', 'renewal_total', 'renewal_period_months', 'renewal_total_status', 'discount_percent', 'discount_basis', 'reference_price_total', 'reference_price_basis', 'billing_type', 'tax_treatment', 'source_url', 'source_kind', 'series_id', 'evidence_sha256', 'freshness_status', 'validation_status', 'snapshot_path', 'snapshot_sha256', 'trend_eligible', 'manual_review_required', 'intro_total_status', 'service_months_status', 'effective_intro_monthly_status', 'advertised_discount_pct_status', 'review_flags', 'renewal_increase_pct', 'policy_observed_at', 'checkout_observed_at']

def rendered(data):
    return json.dumps(data, indent=2, ensure_ascii=False) + '\n'

def series_id(row):
    return hashlib.sha256(json.dumps([row.get(k) for k in ('provider_id', *CONTEXT)], separators=(',', ':')).encode()).hexdigest()[:20]

def build(month, root=ROOT):
    year, number = map(int, month.split('-'))
    end = f'{month}-{calendar.monthrange(year, number)[1]:02d}'
    paths = sorted((root / 'feeds/price-tracking/snapshots').glob('*.json'))
    rows, sources, coverages = [], [], []
    for path in paths:
        feed = json.loads(path.read_text())
        if feed['generated_at'][:10] > end:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        sources.append({'path': path.relative_to(root).as_posix(), 'sha256': digest})
        coverages.append((feed['generated_at'], feed['providers']))
        for record in feed['records']:
            row = dict(record)
            row.update(snapshot_at=feed['generated_at'], snapshot_date=feed['generated_at'][:10], snapshot_path=path.relative_to(root).as_posix(), snapshot_sha256=digest, observed_at=record['captured_at'], upfront_total=record['intro_total'], discount_percent=record['advertised_discount_pct'], discount_basis='provider_claim_or_parser_derived' if record['advertised_discount_pct'] is not None else None, tax_treatment=record['tax_treatment_claim'])
            # Extraction-method switches must not masquerade as market movements.
            row['series_id'] = hashlib.sha256(json.dumps([record['series_id'], record['intro_total_status'], record['service_months_status']], separators=(',', ':')).encode()).hexdigest()[:20]
            rows.append(row)
    selected = [r for r in rows if r['snapshot_date'].startswith(month)]
    if not selected or max(r['snapshot_date'] for r in selected) != end:
        raise ValueError(f'{month}: no month-end snapshot; release cannot be frozen')
    identity = lambda r: (r['provider_id'], r['plan_id'], r['country_code'], r['currency'])
    events, previous = [], {}
    for row in rows:
        if not row['trend_eligible']:
            continue
        key = identity(row)
        old = previous.get(key)
        if old and (old['series_id'] != row['series_id'] or old['upfront_total'] != row['upfront_total']):
            event_type = 'source_change' if old['source_url'] != row['source_url'] else 'context_change' if old['series_id'] != row['series_id'] else 'price_change'
            events.append({'type': event_type, 'provider_id':row['provider_id'], 'provider_name': row['provider_name'], 'plan_id':row['plan_id'], 'plan_name':row['plan_name'], 'currency':row['currency'], 'detected_at': row['observed_at'], 'previous_observed_at': old['observed_at'], 'old_upfront_total': old['upfront_total'], 'new_upfront_total': row['upfront_total'], 'old_source_url': old['source_url'], 'new_source_url': row['source_url'], 'old_series_id': old['series_id'], 'new_series_id': row['series_id'], 'change_pct': round((row['upfront_total'] / old['upfront_total'] - 1) * 100, 2) if event_type == 'price_change' else None, 'snapshot_path': row['snapshot_path']})
        previous[key] = row
    month_events = [e for e in events if e['detected_at'].startswith(month)]
    first_stamp = min(r['snapshot_at'] for r in selected)
    last_stamp = max(r['snapshot_at'] for r in selected)
    first = {identity(r): r for r in selected if r['snapshot_at'] == first_stamp}
    last = [r for r in selected if r['snapshot_at'] == last_stamp]
    plans = []
    for row in last:
        old = first.get(identity(row))
        plan_events = [e for e in month_events if (e['provider_id'],e['plan_id'],e['currency']) == (row['provider_id'],row['plan_id'],row['currency'])]
        comparable = bool(old and old['series_id'] == row['series_id'] and old['trend_eligible'] and row['trend_eligible'] and not any(e['type'] != 'price_change' for e in plan_events))
        renewal = row['effective_renewal_monthly']
        plans.append({**row, 'start_upfront_total': old['upfront_total'] if old else None, 'endpoint_comparable': comparable, 'endpoint_change_pct': round((row['upfront_total'] / old['upfront_total'] - 1) * 100, 2) if comparable else None, 'renewal_increase_pct': round((renewal / row['effective_intro_monthly'] - 1) * 100, 1) if row['trend_eligible'] and renewal is not None and row['effective_intro_monthly'] and row['renewal_total_status'] in {'machine_extracted','checkout_observed','derived','derived_from_checkout'} else None, 'observed_days': len({r['snapshot_date'] for r in selected if identity(r) == identity(row) and r['trend_eligible']})})
    days = sorted({r['snapshot_date'] for r in selected})
    counts = Counter(r['freshness_status'] for r in selected)
    coverage = max(coverages, key=lambda item:item[0])[1]
    summary = {'month': month, 'period_start': f'{month}-01', 'period_end': end, 'first_snapshot_at': first_stamp, 'last_snapshot_at': last_stamp, 'days_with_snapshots': len(days), 'calendar_days': calendar.monthrange(year, number)[1], 'missing_snapshot_days': [f'{month}-{day:02d}' for day in range(1, calendar.monthrange(year, number)[1] + 1) if f'{month}-{day:02d}' not in days], 'snapshot_count': len({r['snapshot_path'] for r in selected}), 'provider_count': len(coverage), 'plan_count':len(last), 'eligible_plan_count':sum(r['trend_eligible'] for r in last), 'fresh_record_count': counts['current'], 'fallback_record_count': counts['carried_forward'], 'comparable_plan_count': sum(p['endpoint_comparable'] for p in plans), 'endpoint_decrease_count': sum(p['endpoint_change_pct'] is not None and p['endpoint_change_pct'] < 0 for p in plans), 'endpoint_increase_count': sum(p['endpoint_change_pct'] is not None and p['endpoint_change_pct'] > 0 for p in plans), 'endpoint_unchanged_count': sum(p['endpoint_change_pct'] == 0 for p in plans), 'price_change_count': sum(e['type'] == 'price_change' for e in month_events), 'source_change_count': sum(e['type'] == 'source_change' for e in month_events), 'events': month_events, 'providers': coverage, 'plans':plans}
    return {'schema_version':'1.0.0', 'dataset_type':'all_provider_provisional_price_history', 'validation_state':'automated_unreviewed', 'manual_review_required':True, 'release_id':f'price-history-{month}-v1', 'license':'https://creativecommons.org/licenses/by/4.0/', 'creator':{'name':'Steve Price','orcid':'https://orcid.org/0009-0009-6603-6878'}, 'markets':sorted({(r['country_code'] or 'unverified')+'/'+r['currency'] for r in rows}), 'history_start':min(r['snapshot_date'] for r in rows), 'history_end':end, 'methodology_url':'https://github.com/steveprice-dev/vpn-price-data/blob/main/methodology/price-history.md', 'limitations':['All 29 tracked providers; all extracted plans, including records with missing or ambiguous values.', 'Automated unreviewed extraction, not manually verified research or a representative market index.', 'Trend eligibility is an arithmetic/source/freshness gate, not manual confirmation of source accuracy.', 'Fallback rows repeat earlier observations and are excluded from trends.', 'Source, plan, duration, billing type, market, currency or extraction method changes break a series.', 'Discount labels and inferred reference totals do not establish historical savings or provider intent.', 'Derived renewal terms may depend on policy interpretation. No claim about an actual future invoice.', 'No imputation or currency conversion; tax and regional availability can differ.'], 'source_snapshots':sources, 'summary':summary, 'events':events, 'records':rows}

def csv_text(data):
    output = io.StringIO(newline='')
    writer = csv.DictWriter(output, fieldnames=COLUMNS, lineterminator='\n')
    writer.writeheader()
    writer.writerows({k:r.get(k) for k in COLUMNS} for r in data['records'])
    return output.getvalue()

def write_month(month, check=False):
    data = build(month)
    directory = ROOT / 'data/price-history/releases' / data['release_id']
    files = {'data.json': rendered(data), 'data.csv': csv_text(data), 'summary.json': rendered(data['summary'])}
    files['SHA256SUMS'] = ''.join(f'{hashlib.sha256(value.encode()).hexdigest()}  {name}\n' for name,value in files.items())
    if check:
        for name, value in files.items():
            if not (directory / name).exists() or (directory / name).read_text() != value:
                raise ValueError(f'{directory.name}/{name}: missing or differs from deterministic sources')
    else:
        directory.mkdir(parents=True, exist_ok=True)
        for name,value in files.items():
            path = directory / name
            if path.exists() and path.read_text() != value:
                raise ValueError(f'refusing to rewrite immutable release {path}; issue a documented revision')
            path.write_text(value)
    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--month')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--as-of', default=datetime.now(timezone.utc).strftime('%Y-%m-%d'))
    args = parser.parse_args()
    months = [args.month] if args.month else sorted({json.loads(p.read_text())['generated_at'][:7] for p in (ROOT/'feeds/price-tracking/snapshots').glob('*.json') if '2026-09' <= json.loads(p.read_text())['generated_at'][:7] < args.as_of[:7]})
    releases = []
    for month in months:
        data = write_month(month, args.check)
        releases.append({'id': data['release_id'], 'month': month, 'period_end': data['history_end'], 'path': f"data/price-history/releases/{data['release_id']}", 'sha256': hashlib.sha256(rendered(data).encode()).hexdigest(), 'provider_count': data['summary']['provider_count']})
    # Index every already-frozen month; --month must not erase other releases.
    entries = []
    for path in sorted((ROOT/'data/price-history/releases').glob('*/data.json')):
        data = json.loads(path.read_text())
        entries.append({'id':data['release_id'], 'month':data['summary']['month'], 'period_end':data['history_end'], 'path':path.parent.relative_to(ROOT).as_posix(), 'sha256':hashlib.sha256(path.read_bytes()).hexdigest(), 'provider_count':data['summary']['provider_count']})
    index = rendered({'schema_version':'1.0.0', 'dataset_type':'all_provider_provisional_price_history', 'releases':entries})
    index_path = ROOT/'data/price-history/index.json'
    if args.check:
        if index_path.read_text() != index: raise ValueError('price-history index is stale')
    else:
        index_path.write_text(index)
    print(f'Validated {len(releases)} completed monthly release(s).')

if __name__ == '__main__':
    main()
