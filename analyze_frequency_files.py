import csv
import hashlib
import os
from pathlib import Path

root = Path(r"d:/03-Downloads/50-freq")

files = []
for path in root.rglob("*.*"):
    if path.suffix.lower() in {".csv", ".md", ".txt"}:
        try:
            size = path.stat().st_size
        except OSError:
            continue
        files.append((path, size))

files.sort(key=lambda x: (x[0].suffix.lower(), x[1], str(x[0])))

summary = []
for path, size in files:
    info = {
        'path': str(path.relative_to(root)),
        'size': size,
        'suffix': path.suffix.lower(),
        'header': None,
        'lines': None,
        'hash': None,
    }
    try:
        with path.open('rb') as f:
            data = f.read()
            info['hash'] = hashlib.sha256(data).hexdigest()
            text = data.decode('utf-8', errors='replace')
            lines = text.splitlines()
            if lines:
                info['header'] = lines[0]
                info['lines'] = len(lines)
    except Exception as e:
        info['header'] = f'ERROR: {e}'
    summary.append(info)

# exact duplicates by size+hash
exact = {}
for info in summary:
    key = (info['size'], info['hash'])
    exact.setdefault(key, []).append(info['path'])

similar = []
# simple similarity by suffix and header
for i, a in enumerate(summary):
    for b in summary[i+1:]:
        if a['suffix'] != b['suffix']:
            continue
        if a['header'] and a['header'] == b['header']:
            if abs(a['size'] - b['size']) < 1000:
                similar.append((a['path'], b['path'], a['header'], a['size'], b['size']))

md = []
md.append('# Frequency and Metadata File Analysis')
md.append('')
md.append('## Files inventoried')
md.append('')
for info in summary:
    md.append(f"- `{info['path']}` ({info['suffix']}, {info['size']} bytes) header: `{info['header']}`")
md.append('')
md.append('## Exact duplicate candidates')
for key, paths in exact.items():
    if len(paths) > 1:
        md.append(f"- {len(paths)} files with size {key[0]} and identical first block:")
        for p in paths:
            md.append(f"  - `{p}`")
md.append('')
md.append('## Similar header files (same suffix and header, size close)')
for a, b, header, sa, sb in similar:
    md.append(f"- `{a}` and `{b}` both start with `{header}` and sizes {sa}/{sb}")

print('\n'.join(md))
