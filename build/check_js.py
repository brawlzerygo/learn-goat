"""Syntax-check every inline <script> in index.html and every data/*.js file with node --check.
Run before publishing: python3 build/check_js.py  (exits 1 on any error). Added 2026-11-22 after an apostrophe in a
single-quoted flashcard broke the live site."""
import re, subprocess, sys, tempfile, glob, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bad = 0
html = open(os.path.join(root, 'index.html')).read()
for i, sc in enumerate(re.findall(r'<script>(.*?)</script>', html, re.S)):
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as f: f.write(sc)
    r = subprocess.run(['node', '--check', f.name], capture_output=True, text=True); os.unlink(f.name)
    if r.returncode: bad += 1; print(f'index.html script {i}:', r.stderr.split('\n')[1][:200], r.stderr.split('\n')[4] if len(r.stderr.split('\n'))>4 else '')
for p in sorted(glob.glob(os.path.join(root, 'data', '*.js'))) + sorted(glob.glob(os.path.join(root, 'js', '**', '*.js'), recursive=True)):
    r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
    if r.returncode: bad += 1; print(os.path.relpath(p, root), r.stderr[:300])
print('JS syntax: ' + ('OK' if not bad else f'{bad} file(s) with errors')); sys.exit(1 if bad else 0)
