"""Public all-provider schema, arithmetic and privacy checks."""
import json, re
from urllib.parse import urlsplit
from jsonschema import Draft202012Validator, FormatChecker

def tracking_checks(root, provider_ids):
 errors=[];schema=json.loads((root/'schemas/price-tracking.schema.json').read_text());validator=Draft202012Validator(schema,format_checker=FormatChecker())
 for path in sorted((root/'feeds/price-tracking').rglob('*.json')):
  data=json.loads(path.read_text());errors.extend(f'{path.name}: {e.message}' for e in validator.iter_errors(data))
  if {p['provider_id'] for p in data['providers']} != provider_ids:errors.append(f'{path.name}: incomplete tracked population')
  seen=set()
  for row in data['records']:
   key=(row['provider_id'],row['plan_id'],row['country_code'],row['currency'])
   if key in seen:errors.append(f'{path.name}: duplicate plan identity {key}')
   seen.add(key)
   if row['provider_id'] not in provider_ids:errors.append(f'{path.name}: unknown provider')
   for source in row['sources']+row['policy_sources']:
    parts=urlsplit(source['url'])
    if parts.scheme!='https' or parts.query or parts.fragment or parts.username:errors.append(f'{path.name}: unsafe source URL')
   if row['trend_eligible']:
    if row['freshness_status']!='current' or row['service_months'] is None or row['service_months']<=0 or row['intro_total'] is None or row['intro_total']<=0 or row['effective_intro_monthly'] is None or abs(row['intro_total']/row['service_months']-row['effective_intro_monthly'])>0.011:errors.append(f'{path.name}: trend eligibility arithmetic/freshness mismatch')
  body=path.read_text()
  if re.search(r'(?i)("(?:blob_path|checkout_url|checkout_evidence_path|private_notes|api_key|cookies|authorization)"|(?:[0-9]{1,3}\.){3}[0-9]{1,3})',body):errors.append(f'{path.name}: private field or IP crossed export boundary')
 return errors
