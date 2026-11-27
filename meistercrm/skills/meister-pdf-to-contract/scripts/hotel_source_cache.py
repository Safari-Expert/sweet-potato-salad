"""Inventory source bytes and cache page-indexed PDF extraction, never rate decisions.

JOB: {"version":1,"root":"...","cache_dir":"...", "paths":["relative.pdf"],
      "extract_pdf":true,"mode":"plain","min_text_chars":30,"max_pdf_bytes":104857600}
paths is optional: omitted means a recursive inventory of regular files. All paths
must remain within root. Cache and report destinations must be outside source root.
The caller must additionally enforce a non-synced local workspace/cache dedicated
to this client; do not share a hash cache between clients or stage in Google Drive.
See references/general/client-folder-operations.md for the operational boundary.
PDF extraction uses installed pypdf; mode is plain or layout. No OCR, network,
archive expansion, source mutation, supplier classification or review certification.
CLI: python hotel_source_cache.py JOB --output REPORT
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path

from _hotel_common import distinct_paths, load_json, write_json

SCHEMA_VERSION = 1


def _digest(path):
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def _canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'),
                      allow_nan=False).encode('utf-8')


def _outside(path, root):
    if path == root or path.is_relative_to(root):
        raise ValueError('Cache/report destinations must be outside the source root')


def _sources(root, paths):
    if paths is not None:
        if not isinstance(paths, list) or not all(isinstance(p, str) and p for p in paths):
            raise ValueError('paths must contain nonblank relative paths')
        found = []
        for value in paths:
            rel = Path(value)
            if rel.is_absolute() or '..' in rel.parts or rel.drive:
                raise ValueError('Source paths must be relative and remain inside root')
            candidate = root / rel
            if not candidate.resolve().is_relative_to(root):
                raise ValueError('Source resolves outside root')
            # No following even in-root symbolic links: the inventory keeps identity explicit.
            if any(p.is_symlink() or (hasattr(p, 'is_junction') and p.is_junction())
                   for p in [candidate, *candidate.parents] if p != root and p.is_relative_to(root)):
                raise ValueError('Source symbolic links and junctions are not followed')
            found.append(candidate)
        if len(set(found)) != len(found):
            raise ValueError('Duplicate source path supplied')
        return sorted(found), []
    found, errors = [], []

    def onerror(exc):
        errors.append({'path': str(exc.filename), 'error': type(exc).__name__})

    for folder, dirs, files in os.walk(root, followlinks=False, onerror=onerror):
        for name in list(dirs):
            path = Path(folder) / name
            if path.is_symlink() or (hasattr(path, 'is_junction') and path.is_junction()):
                dirs.remove(name)
                errors.append({'path': str(path.relative_to(root)), 'error': 'link_not_followed'})
        for name in files:
            path = Path(folder) / name
            if path.is_symlink():
                errors.append({'path': str(path.relative_to(root)), 'error': 'link_not_followed'})
            else:
                found.append(path)
    return sorted(found), errors


def _parse_pdf(data, mode, min_chars):
    from pypdf import PdfReader
    reader = PdfReader(io.BytesIO(data))
    if reader.is_encrypted:
        raise ValueError('Encrypted PDF requires a separately authorized readable source')
    pages = []
    for index, page in enumerate(reader.pages, 1):
        text = page.extract_text(extraction_mode=mode) or ''
        annotations, annotation_errors = [], []
        for reference in page.get('/Annots', []):
            try:
                item = reference.get_object()
                annotations.append({key[1:]: str(item[key]) for key in ('/Subtype', '/Contents', '/T', '/Subj') if key in item})
            except Exception as exc:
                annotation_errors.append(type(exc).__name__)
        pages.append({'page': index, 'text': text, 'annotations': annotations,
                      'annotation_errors': annotation_errors,
                      'low_text': len(text.strip()) < min_chars})
    if not pages:
        raise ValueError('PDF has no pages')
    return {'page_count': len(pages), 'pages': pages}


def _valid_payload(payload):
    if not isinstance(payload, dict) or type(payload.get('page_count')) is not int:
        return False
    pages = payload.get('pages')
    return (isinstance(pages, list) and len(pages) == payload['page_count'] > 0 and
            all(isinstance(p, dict) and p.get('page') == i and isinstance(p.get('text'), str)
                and type(p.get('low_text')) is bool and isinstance(p.get('annotations'), list)
                and isinstance(p.get('annotation_errors'), list) for i, p in enumerate(pages, 1)))


def _safe_cache_entry(cache, target):
    # Cache artifacts are owned files, never aliases to source or external files.
    if target.is_symlink() or target.resolve().parent != cache:
        raise ValueError('Cache entry must remain directly inside cache_dir without links')
    if target.exists() and (not target.is_file() or target.stat().st_nlink != 1):
        raise ValueError('Cache entry must be a regular file without hardlinks')


def _cached_pdf(path, source_hash, cache, settings):
    import pypdf
    descriptor = {'schema_version': SCHEMA_VERSION, 'source_sha256': source_hash,
                  'parser': 'pypdf', 'parser_version': pypdf.__version__, **settings}
    key = hashlib.sha256(_canonical(descriptor)).hexdigest()
    target = cache / f'{key}.json'
    _safe_cache_entry(cache, target)
    try:
        stored = load_json(target)
        payload = stored.get('payload')
        if (stored.get('descriptor') == descriptor and stored.get('cache_key') == key
                and _valid_payload(payload)
                and stored.get('payload_sha256') == hashlib.sha256(_canonical(payload)).hexdigest()):
            return payload, target, True
    except (OSError, ValueError, TypeError, AttributeError):
        pass
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != source_hash:
        raise ValueError('Source changed during extraction')
    payload = _parse_pdf(data, settings['mode'], settings['min_text_chars'])
    if not _valid_payload(payload):
        raise ValueError('Invalid extractor result')
    _safe_cache_entry(cache, target)
    write_json(target, {'cache_key': key, 'descriptor': descriptor, 'payload': payload,
                       'payload_sha256': hashlib.sha256(_canonical(payload)).hexdigest()}, protected=[path])
    return payload, target, False


def run_job(job):
    if not isinstance(job, dict) or type(job.get('version')) is not int or job['version'] != 1:
        raise ValueError('Expected version 1 job')
    if set(job) - {'version','root','cache_dir','paths','extract_pdf','mode','min_text_chars','max_pdf_bytes'}:
        raise ValueError('Unknown source-cache job field')
    root, cache = Path(job['root']).resolve(), Path(job['cache_dir']).resolve()
    if not root.is_dir():
        raise ValueError('root must be an existing directory')
    _outside(cache, root)
    if cache.exists() and not cache.is_dir():
        raise ValueError('cache_dir must be a directory')
    extract = job.get('extract_pdf', True)
    if type(extract) is not bool:
        raise ValueError('extract_pdf must be boolean')
    mode = job.get('mode', 'plain')
    minimum, maximum = job.get('min_text_chars', 30), job.get('max_pdf_bytes', 104857600)
    if mode not in ('plain', 'layout') or type(minimum) is not int or minimum < 0 or type(maximum) is not int or maximum <= 0:
        raise ValueError('Invalid extraction options')
    paths, errors = _sources(root, job.get('paths'))
    records, hashes = [], {}
    for path in paths:
        record = {'path': str(path.relative_to(root)), 'semantic_review': 'not_performed'}
        try:
            if not path.is_file():
                raise ValueError('Source is not a regular file')
            initial = path.stat()
            digest = _digest(path)
            if (initial.st_size, initial.st_mtime_ns) != (path.stat().st_size, path.stat().st_mtime_ns):
                raise ValueError('Source changed during inventory')
            record.update(size_bytes=initial.st_size, sha256=digest, status='inventoried')
            hashes.setdefault(digest, []).append(record['path'])
            if path.suffix.lower() == '.pdf' and extract:
                if initial.st_size > maximum:
                    raise ValueError('PDF exceeds the configured extraction size limit')
                payload, entry, hit = _cached_pdf(path, digest, cache, {'mode': mode, 'min_text_chars': minimum})
                if _digest(path) != digest:
                    raise ValueError('Source changed while reading cache or extracting')
                record.update(status='extracted', cache_hit=hit, cache_path=str(entry),
                              page_count=payload['page_count'],
                              low_text_pages=[p['page'] for p in payload['pages'] if p['low_text']],
                              annotation_error_pages=[p['page'] for p in payload['pages'] if p['annotation_errors']])
        except Exception as exc:
            record.update(status='error', error=f'{type(exc).__name__}: {exc}')
        records.append(record)
    return {'version': 1, 'root': str(root), 'records': records, 'scan_errors': errors,
            'duplicate_groups': [v for v in hashes.values() if len(v) > 1],
            'status': 'review' if errors or any(r['status']=='error' or r.get('low_text_pages') or r.get('annotation_error_pages') for r in records) else 'complete',
            'scope': 'Byte inventory and extraction only; duplicate bytes do not establish contract applicability or semantic review.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('job', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        job = load_json(args.job)
        _outside(args.output.resolve(), Path(job['root']).resolve())
        cache = Path(job['cache_dir']).resolve()
        _outside(args.output.resolve(), cache)
        distinct_paths([args.output], [args.job])
        report = run_job(job)
        write_json(args.output, report, protected=[args.job])
        print(json.dumps({'status': report['status'], 'files': len(report['records'])}))
        return 0 if report['status'] == 'complete' else 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f'{exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
