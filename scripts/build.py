#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[1]
out = root / 'index.html'

parts = [
    root / 'src/layout/start.html',
    root / 'src/sections/home.html',
    root / 'src/sections/about.html',
    root / 'src/sections/skills.html',
    root / 'src/sections/projects.html',
    root / 'src/sections/education.html',
    root / 'src/sections/experience.html',
    # root / 'src/sections/publications.html',
    root / 'src/sections/contact.html',
    root / 'src/layout/end.html',
]

def concat(files):
    buf = []
    for p in files:
        if not p.exists():
            raise SystemExit(f'Missing part: {p}')
        buf.append(p.read_text())
    return '\n'.join(buf)

html = concat(parts)
out.write_text(html)
print(f'Wrote {out} ({len(html)} bytes)')

