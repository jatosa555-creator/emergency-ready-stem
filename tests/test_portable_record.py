import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('portable_validator', ROOT / 'scripts/validate_portable_record.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PortableChecks(unittest.TestCase):
    def setUp(self):
        self.sample = json.loads((ROOT / 'docs/SAMPLE_PORTABLE_RECORD_V11.json').read_text(encoding='utf-8'))

    def test_existing_version_remains_supported(self):
        old = json.loads((ROOT / 'docs/SAMPLE_PORTABLE_RECORD.json').read_text(encoding='utf-8'))
        self.assertFalse(module.validate(old)['errors'])

    def test_new_sample_has_explicit_proposed_decision(self):
        self.assertEqual(self.sample['teacher_decision_status'], 'proposed')
        self.assertFalse(module.validate(self.sample)['errors'])

    def test_decision_status_cannot_be_omitted(self):
        del self.sample['teacher_decision_status']
        self.assertTrue(module.validate(self.sample)['errors'])

    def test_observed_document_requires_a_locator(self):
        self.sample['observations'] = [{'statement': 'Visible in supplied work', 'status': 'document-observed'}]
        self.assertTrue(module.validate(self.sample)['errors'])
        self.sample['observations'][0]['source_reference'] = 'teacher-supplied worksheet, item 2'
        self.assertFalse(module.validate(self.sample)['errors'])

    def test_unknown_fields_cannot_be_silently_stored(self):
        self.sample['student_names'] = ['DO_NOT_STORE']
        result = module.validate(self.sample)
        self.assertTrue(result['errors'])
        self.assertNotIn('DO_NOT_STORE', json.dumps(result))

    def test_teacher_certification_is_not_a_review_status(self):
        self.sample['quality_review']['status'] = 'safety-certified'
        self.assertTrue(module.validate(self.sample)['errors'])

    def test_malformed_record_has_consistent_error(self):
        for value in [None, [], {}, {'schema_version': '99'}, {'schema_version': []}, {'schema_version': {}}]:
            self.assertTrue(module.validate(value)['errors'])


if __name__ == '__main__':
    unittest.main()
