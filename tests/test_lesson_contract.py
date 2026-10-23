import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('checker', ROOT / 'scripts/check_lesson_contract.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class ContractChecks(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'tests/fixtures/lesson_contract.json').read_text(encoding='utf-8'))

    def codes(self):
        return {item['code'] for item in checker.check(self.data)['errors']}

    def test_valid_independent_route_budgets(self):
        result = checker.check(self.data)
        self.assertFalse(result['errors'])
        self.assertEqual([v['minutes'] for v in result['route_totals'].values()], [40, 40])
        self.assertTrue(result['not_verified'])

    def test_overrun_only_in_fallback_is_caught(self):
        self.data['plans'][1]['timeline'][0]['minutes'] += 1
        self.assertIn('time_exceeded', self.codes())

    def test_goal_drift(self):
        self.data['plans'][1]['learning_goal'] = 'Make a poster instead of interpreting data'
        self.assertIn('goal_mismatch', self.codes())

    def test_offline_plan_cannot_require_internet(self):
        self.data['plans'][1]['resources'].append('internet')
        self.assertIn('unavailable_resource', self.codes())

    def test_requested_exit_ticket_is_not_optional(self):
        del self.data['plans'][1]['deliverables']['exit_ticket']
        self.assertIn('missing_deliverable', self.codes())

    def test_empty_worksheet_is_not_delivered(self):
        self.data['plans'][0]['deliverables']['worksheet'] = ' '
        self.assertIn('empty_deliverable', self.codes())

    def test_invalid_time_does_not_silently_pass(self):
        for value in [True, -1, 0, '10', float('nan'), float('inf')]:
            with self.subTest(value=value):
                candidate = copy.deepcopy(self.data)
                candidate['plans'][0]['timeline'][0]['minutes'] = value
                codes = {e['code'] for e in checker.check(candidate)['errors']}
                self.assertIn('invalid_step_time', codes)

    def test_missing_or_duplicate_route(self):
        self.data['plans'][1]['id'] = 'A'
        self.assertIn('missing_or_duplicate_route', self.codes())

    def test_malformed_input_does_not_crash(self):
        for value in [None, [], {}, {'plans': [None, 1]}, {'plans': {'A': {}}}]:
            with self.subTest(value=value):
                self.assertTrue(checker.check(value)['errors'])

    def test_huge_integer_budget_is_a_validation_error(self):
        self.data['available_minutes'] = 10 ** 1000
        self.assertIn('invalid_time_budget', self.codes())

    def test_huge_integer_step_is_a_validation_error(self):
        self.data['plans'][0]['timeline'][0]['minutes'] = 10 ** 1000
        self.assertIn('invalid_step_time', self.codes())

    def test_finite_steps_cannot_produce_an_infinite_json_total(self):
        self.data['available_minutes'] = 1e308
        self.data['plans'][0]['timeline'] = [
            {'activity': 'a', 'minutes': 1e308}, {'activity': 'b', 'minutes': 1e308},
        ]
        result = checker.check(self.data)
        self.assertIn('invalid_total_time', {e['code'] for e in result['errors']})
        json.dumps(result, allow_nan=False)


if __name__ == '__main__':
    unittest.main()
