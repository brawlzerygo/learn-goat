#!/usr/bin/env python3
"""Build the Goat site's card data (data/cards.js, data/meta.js) and art (img/<id>.webp).

Source: the YGOPRODeck API v7. Two of its views disagree, so the pool is their union by card name:
cardinfo.php?format=goat&misc=yes (build/raw/goat_cards.json) and every card whose misc_info formats list "GOAT" in
the full list cardinfo.php?misc=yes (build/raw/all_cards.json). Checked 2026-11-23: the filter alone missed Blade
Knight; the formats list alone missed Red-Eyes Black Dragon, Flame Swordsman and others. Pass --fetch to download
both again. Its Goat pool and its Goat banlist (banlist_info.ban_goat) were checked on 2026-11-23 against
goatformat.com/cardpool.html: the same 17 Forbidden, 41 Limited and 15 Semi-Limited cards (the TCG list of April 2005).

Art: a card already in the Edison site's img/ (same passcode, same 421x614 WebP) is copied from there; the rest are
downloaded once from YGOPRODeck's image server (paced well under its 20 requests a second) and converted with cwebp.
Never hotlinked.

Usage: python3 build/build_data.py [--fetch] [--images]
"""
import json, os, shutil, subprocess, sys, tempfile, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDISON_IMG = os.path.join(os.path.dirname(ROOT), 'img')
RAW = os.path.join(ROOT, 'build/raw/goat_cards.json')
API = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?format=goat&misc=yes'
ALL = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?misc=yes'
RAW_ALL = os.path.join(ROOT, 'build/raw/all_cards.json')
UA = {'User-Agent': 'learnretro-goat-builder'}
BAN = {'Forbidden': 'F', 'Limited': 'L', 'Semi-Limited': 'S'}


def kind(c):
    f = c.get('frameType', '')
    if f in ('spell', 'trap', 'normal', 'effect', 'ritual', 'fusion'):
        return f
    return 'effect'


def main():
    args = set(sys.argv[1:])
    if '--fetch' in args or not os.path.exists(RAW):
        os.makedirs(os.path.dirname(RAW), exist_ok=True)
        data = urllib.request.urlopen(urllib.request.Request(API, headers=UA), timeout=60).read()
        open(RAW, 'wb').write(data)
        data = urllib.request.urlopen(urllib.request.Request(ALL, headers=UA), timeout=120).read()
        open(RAW_ALL, 'wb').write(data)
    cards = json.load(open(RAW))['data']
    names = {c['name'] for c in cards}
    if os.path.exists(RAW_ALL):
        for c in json.load(open(RAW_ALL))['data']:
            if 'GOAT' in ((c.get('misc_info') or [{}])[0].get('formats') or []) and c['name'] not in names:
                cards.append(c); names.add(c['name'])
    out = []
    for c in sorted(cards, key=lambda c: c['name']):
        k = kind(c)
        r = {'id': c['id'], 'n': c['name'], 'k': k, 'tx': c.get('desc', '')}
        if k in ('spell', 'trap'):
            r['sub'] = c.get('race', '')
        else:
            r['a'] = c.get('attribute')
            r['r'] = c.get('race')
            r['lv'] = c.get('level')
            r['atk'] = str(c.get('atk', '?')) if c.get('atk') is not None else '?'
            r['def'] = str(c.get('def', '?')) if c.get('def') is not None else '?'
            tl = [t for t in (c.get('typeline') or []) if t != c.get('race')]
            r['ab'] = ' '.join(tl) or ('Normal' if k == 'normal' else 'Effect')
            if 'Flip' in (c.get('type') or ''):
                r['flip'] = 1
        b = BAN.get((c.get('banlist_info') or {}).get('ban_goat'))
        if b:
            r['b'] = b
        out.append(r)
    os.makedirs(os.path.join(ROOT, 'data'), exist_ok=True)
    with open(os.path.join(ROOT, 'data/cards.js'), 'w') as f:
        f.write('window.GOAT_CARDS=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n')
    meta = {'built': time.strftime('%Y-%m-%d'), 'cards': len(out),
            'sources': ['https://ygoprodeck.com/api-guide/', 'https://www.goatformat.com/cardpool.html']}
    with open(os.path.join(ROOT, 'data/meta.js'), 'w') as f:
        f.write('window.GOAT_META=' + json.dumps(meta) + ';\n')
    print('cards', len(out), {v: sum(1 for r in out if r.get('b') == v) for v in 'FLS'})

    if '--images' in args:
        os.makedirs(os.path.join(ROOT, 'img'), exist_ok=True)
        copied = fetched = 0
        for c in cards:
            dst = os.path.join(ROOT, 'img/%d.webp' % c['id'])
            if os.path.exists(dst):
                continue
            src = os.path.join(EDISON_IMG, '%d.webp' % c['id'])
            if os.path.exists(src):
                shutil.copyfile(src, dst); copied += 1; continue
            url = c['card_images'][0]['image_url']
            data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
            with tempfile.NamedTemporaryFile(suffix='.jpg') as tf:
                tf.write(data); tf.flush()
                subprocess.run(['cwebp', '-quiet', '-q', '88', '-resize', '421', '614', tf.name, '-o', dst], check=True)
            fetched += 1
            time.sleep(0.1)
        print('art copied from Edison', copied, 'downloaded', fetched)


if __name__ == '__main__':
    main()
