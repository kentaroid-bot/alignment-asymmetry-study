"""Verify the exact observation subset cited by the published paper; no model calls."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    manifest = json.loads((ROOT / 'docs/artifact-manifest.json').read_text())
    snapshot = manifest['observation_snapshot']
    errors = []
    outputs = 0
    for name, expected in snapshot['sha256'].items():
        path = ROOT / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            errors.append(name)
        if '/outputs/' in name:
            outputs += 1
    if outputs != snapshot['receipts']:
        errors.append('receipt_count')
    for name, expected in manifest['sha256'].items():
        path = ROOT / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            errors.append(name)
    print(json.dumps({'captured_at': snapshot['captured_at'],
                      'documented_receipts': outputs, 'errors': errors,
                      'scope': 'Hash identity of documented observations and artifacts; social validity is not established.'},
                     ensure_ascii=False))
    if errors:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
