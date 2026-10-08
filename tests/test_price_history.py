import importlib.util, pathlib, tempfile, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('history',ROOT/'scripts/build_price_history.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class MonthlyHistory(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=mod.build('2026-09')
 def test_full_population_and_gap_states(self):
  s=self.data['summary'];self.assertEqual(s['provider_count'],29);self.assertEqual(s['plan_count'],124);self.assertEqual(s['days_with_snapshots'],30);self.assertGreater(s['fallback_record_count'],0)
  self.assertTrue(all(not r['trend_eligible'] for r in self.data['records'] if r['freshness_status']=='carried_forward'))
 def test_proton_switch_cannot_be_a_price_cut(self):
  events=[e for e in self.data['summary']['events'] if e['provider_id']=='protonvpn'];self.assertEqual(len(events),1);self.assertEqual(events[0]['type'],'source_change');self.assertIsNone(events[0]['change_pct'])
  plan=next(p for p in self.data['summary']['plans'] if p['provider_id']=='protonvpn' and p['plan_id']=='vpn-plus-24-month');self.assertFalse(plan['endpoint_comparable']);self.assertIsNone(plan['endpoint_change_pct'])
 def test_report_uses_september_not_later_prices(self):
  self.assertTrue(all(r['snapshot_date']<='2026-09-30' for r in self.data['records']))
  self.assertEqual(self.data['summary']['comparable_plan_count'],88)
  self.assertEqual(self.data['summary']['endpoint_decrease_count'],1)
  self.assertEqual(self.data['summary']['endpoint_increase_count'],4)
 def test_incomplete_month_is_rejected(self):
  with tempfile.TemporaryDirectory() as directory:
   with self.assertRaises(ValueError):mod.build('2026-10',pathlib.Path(directory))
 def test_rebuild_matches_frozen_release(self):mod.write_month('2026-09',check=True)
