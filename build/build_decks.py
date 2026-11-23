#!/usr/bin/env python3
"""Build data/decks.js (window.GOAT_DECKS) from build/decks/decks.txt (lists typed from goatformat.com guides).
Each deck: name, tier, by (credit), src (URL), note, main/extra/side as passcodes. A deck whose Main Deck isn't 40-60
cards, or that names a card not in data/cards.js, or breaks the banlist, is reported and left out (no guessing)."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
txt = open(os.path.join(ROOT, 'build/decks/decks.txt')).read()
cards = json.loads(open(os.path.join(ROOT, 'data/cards.js')).read().split('=', 1)[1].rstrip(';\n'))
by = {c['n'].lower(): c for c in cards}
lim = {'F': 0, 'L': 1, 'S': 2}
out = []
for block in txt.split('\n@ ')[1:]:
    head, *lines = block.strip().split('\n')
    name, tier, credit, src, note = [x.strip() for x in (head + ' |').split('|')[:5]]
    d = {'name': name, 'tier': tier, 'by': credit, 'src': src, 'note': note, 'main': [], 'extra': [], 'side': []}
    bad = []
    for ln in lines:
        m = re.match(r'(F |S )?(\d+) (.+)$', ln.strip())
        if not m: continue
        c = by.get(m.group(3).strip().lower())
        if not c: bad.append('unknown card ' + m.group(3)); continue
        zone = {'F ': 'extra', 'S ': 'side'}.get(m.group(1), 'main')
        d[zone] += [c['id']] * int(m.group(2))
    if not 40 <= len(d['main']) <= 60: bad.append('main deck has %d cards' % len(d['main']))
    cnt = {}
    for i in d['main'] + d['extra'] + d['side']: cnt[i] = cnt.get(i, 0) + 1
    for i, n in cnt.items():
        c = next(x for x in cards if x['id'] == i)
        if n > lim.get(c.get('b'), 3): bad.append('%s: %d copies' % (c['n'], n))
    if bad: print('LEFT OUT', name, '-', '; '.join(bad)); continue
    print('ok', name, len(d['main']))
    out.append(d)
open(os.path.join(ROOT, 'data/decks.js'), 'w').write('window.GOAT_DECKS=' + json.dumps(out, separators=(',', ':')) + ';\n')
print(len(out), 'decks')
