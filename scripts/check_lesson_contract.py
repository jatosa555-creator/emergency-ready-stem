"""Check structured lesson constraints; not pedagogy, policy or safety validation."""
import argparse
import json
import math
from pathlib import Path


def check(data):
    errors = []

    def error(code, path, detail):
        errors.append({'code': code, 'path': path, 'detail': detail})

    def text(value):
        return isinstance(value, str) and bool(value.strip())

    def positive_number(value):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            return False
        try:
            return math.isfinite(value) and value > 0
        except (OverflowError, ValueError):
            return False

    def strings(value, path, allow_empty=False):
        if not isinstance(value, list) or (not value and not allow_empty):
            error('invalid_list', path, 'Expected a list of nonempty strings')
            return set()
        if any(not text(v) for v in value):
            error('invalid_list_item', path, 'Entries must be nonempty strings')
            return set()
        if len(set(value)) != len(value):
            error('duplicate_entry', path, 'List entries must be unique')
        return set(value)

    if not isinstance(data, dict):
        error('invalid_document', '$', 'Expected an object')
        return {'status': 'needs_revision', 'errors': errors, 'route_totals': {},
                'not_verified': ['No valid lesson object was supplied']}
    if data.get('contract_version') != '1.0':
        error('invalid_version', 'contract_version', 'Expected 1.0')
    goal = data.get('learning_goal')
    if not text(goal):
        error('missing_goal', 'learning_goal', 'An explicit goal is required')
    budget = data.get('available_minutes')
    if not positive_number(budget):
        error('invalid_time_budget', 'available_minutes', 'Expected finite positive minutes')
    allowed = strings(data.get('available_resources'), 'available_resources', True)
    required = strings(data.get('required_deliverables'), 'required_deliverables', True)
    plans = data.get('plans')
    if not isinstance(plans, list):
        error('invalid_plans', 'plans', 'Expected Plan A and Plan B')
        plans = []
    ids = []
    totals = {}
    for index, plan in enumerate(plans):
        path = f'plans[{index}]'
        if not isinstance(plan, dict):
            error('invalid_plan', path, 'Expected a plan object')
            continue
        plan_id = plan.get('id')
        if plan_id not in ('A', 'B'):
            error('invalid_plan_id', path + '.id', 'Expected A or B')
        else:
            ids.append(plan_id)
        if not text(plan.get('learning_goal')) or plan.get('learning_goal') != goal:
            error('goal_mismatch', path + '.learning_goal', 'Explicit goal differs from contract')
        resources = strings(plan.get('resources'), path + '.resources', True)
        for resource in sorted(resources - allowed):
            error('unavailable_resource', path + '.resources', resource)
        deliverables = plan.get('deliverables')
        delivered = set()
        if not isinstance(deliverables, dict):
            error('invalid_deliverables', path + '.deliverables', 'Expected ID to copy-ready content mapping')
        else:
            for key, content in deliverables.items():
                if not text(key) or not text(content):
                    error('empty_deliverable', path + '.deliverables', 'ID and actual content are required')
                else:
                    delivered.add(key)
        for item in sorted(required - delivered):
            error('missing_deliverable', path + '.deliverables', item)
        steps = plan.get('timeline')
        total = 0
        valid_timing = isinstance(steps, list) and bool(steps)
        if not valid_timing:
            error('missing_timeline', path + '.timeline', 'Expected nonempty timed steps')
        else:
            for step_index, step in enumerate(steps):
                step_path = path + f'.timeline[{step_index}]'
                if not isinstance(step, dict) or not text(step.get('activity')):
                    error('invalid_step', step_path, 'Expected an activity with minutes')
                    valid_timing = False
                    continue
                minutes = step.get('minutes')
                if not positive_number(minutes):
                    error('invalid_step_time', step_path + '.minutes', 'Expected finite positive minutes')
                    valid_timing = False
                else:
                    total += minutes
        if valid_timing:
            if not positive_number(total):
                error('invalid_total_time', path + '.timeline', 'Total minutes is outside the finite numeric range')
            else:
                totals[str(index)] = {'plan': plan_id, 'minutes': total}
            if positive_number(total) and positive_number(budget) and total > budget + 1e-9:
                error('time_exceeded', path + '.timeline', f'{total} exceeds {budget}')
    if len(plans) != 2 or sorted(ids) != ['A', 'B']:
        error('missing_or_duplicate_route', 'plans', 'Exactly one A and one B are required')
    return {
        'status': 'checked_structural_constraints' if not errors else 'needs_revision',
        'errors': errors,
        'route_totals': totals,
        'not_verified': [
            'Semantic equivalence and educational quality',
            'Deliverable content quality or references',
            'Physical safety, real material stock and household access',
            'Actual classroom learning or well-being outcomes',
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    try:
        with args.input.open(encoding='utf-8') as handle:
            text = handle.read(131073)
        if len(text) > 131072:
            raise ValueError('Input exceeds the supported size')
        def reject_constant(_):
            raise ValueError('Non-finite JSON literals are not supported')
        data = json.loads(text, parse_constant=reject_constant)
    except (OSError, ValueError, UnicodeError, RecursionError):
        print(json.dumps({'status': 'invalid_input', 'error': 'Input unreadable, invalid JSON or too large'}))
        return 2
    result = check(data)
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 1 if result['errors'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
