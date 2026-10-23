"""Validate a teacher-controlled portable record; does not verify truth or detect PII."""
import argparse
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = {'1.0': 'PORTABLE_RECORD_SCHEMA.json', '1.1': 'PORTABLE_RECORD_SCHEMA_V11.json'}


def validate(data):
    if (not isinstance(data, dict) or not isinstance(data.get('schema_version'), str)
            or data.get('schema_version') not in SCHEMAS):
        return {'status': 'invalid_record', 'errors': [{'path': '$', 'constraint': 'supported_schema_version'}]}
    schema = json.loads((ROOT / 'docs' / SCHEMAS[data['schema_version']]).read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    errors = [{'path': '.'.join(str(p) for p in error.absolute_path) or '$',
               'constraint': error.validator} for error in Draft202012Validator(schema).iter_errors(data)]
    return {
        'status': 'valid_structure' if not errors else 'invalid_record',
        'schema_version': data['schema_version'], 'errors': errors,
        'not_verified': ['Accuracy, actual teacher acceptance, personal data in free text and learning outcomes'],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    try:
        with args.input.open(encoding='utf-8') as handle:
            text = handle.read(65537)
        if len(text) > 65536:
            raise ValueError('Oversized input')
        def reject_constant(_):
            raise ValueError('Non-finite JSON')
        data = json.loads(text, parse_constant=reject_constant)
    except (OSError, ValueError, UnicodeError, RecursionError):
        print(json.dumps({'status': 'invalid_input', 'errors': [{'path': '$', 'constraint': 'readable_bounded_json'}]}))
        return 2
    result = validate(data)
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 1 if result['errors'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
