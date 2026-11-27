"""Small shared IO primitives for the offline hotel helpers; no client state."""
from __future__ import annotations

import json
import os
import re
import tempfile
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path


def decimal_value(value):
    """Accept lossless finite numbers; callers decide allowed signs and rounding."""
    if isinstance(value, bool) or not isinstance(value, (str, int, Decimal)):
        raise ValueError('Use decimal strings or integers, not binary floats/booleans')
    if isinstance(value, str) and (not value or value.strip() != value):
        raise ValueError('Expected a nonblank decimal value without surrounding spaces')
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError('Invalid decimal value') from exc
    if not result.is_finite():
        raise ValueError('Numeric values must be finite')
    return result


def iso_date(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise ValueError('Expected an ISO YYYY-MM-DD calendar date')
    return date.fromisoformat(value)


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def _constant(value):
    raise ValueError(f'Nonfinite JSON number: {value}')


def load_json(path):
    with Path(path).open(encoding='utf-8-sig') as handle:
        return json.load(handle, parse_float=Decimal, parse_constant=_constant,
                         object_pairs_hook=_object)


def distinct_paths(outputs, inputs=()):
    """Reject aliases/hardlinks to inputs and collisions between output files."""
    outputs = [Path(p).resolve() for p in outputs]
    inputs = [Path(p).resolve() for p in inputs]
    for i, target in enumerate(outputs):
        if target.exists() and not target.is_file():
            raise ValueError(f'Output must be a file: {target}')
        for other in inputs + outputs[:i]:
            if target == other or (target.exists() and other.exists() and target.samefile(other)):
                raise ValueError('Output path aliases an input or another output')
    return outputs


def _json_default(value):
    if isinstance(value, Decimal):
        return str(decimal_value(value))
    if isinstance(value, (date, Path)):
        return str(value)
    raise TypeError(f'Not JSON serializable: {type(value).__name__}')


def write_json(path, value, protected=()):
    """Replace one explicit local output atomically; never touch input aliases."""
    target, = distinct_paths([path], protected)
    data = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False,
                      default=_json_default) + '\n'
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f'.{target.name}.', suffix='.tmp',
                                             dir=target.parent)
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8', newline='\n') as handle:
            handle.write(data)
        distinct_paths([target], protected)
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
