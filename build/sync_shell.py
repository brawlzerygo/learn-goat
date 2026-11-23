#!/usr/bin/env python3
"""Bring the Goat site's shell up to date with the Edison site's (learn-edison/), keeping Goat's own content.

Edison is where the shared look is built: the header, the phone menu, the format switcher, social links and the
styles. This script copies them over so both sites look and work the same (Zack, 2026-11-23: one domain, clean
navigation, a format switcher):
- themes/base.css and themes/index.css are copied as they are; themes/goat.css (Goat's accent color) loads after them.
- index.html is rebuilt from Edison's, swapping in Goat's title, description, canonical, <base href="/goat/">, the
  format pill, the section menus and the script list.
- js/app.js is not copied (it holds Goat's own text); shared code changes there are ported by hand.
Run: python3 build/sync_shell.py   (then check the page; bump ?v= is copied from Edison)
"""
import os, re, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ED = os.path.dirname(ROOT)

for f in ('base.css', 'index.css'):
    shutil.copyfile(os.path.join(ED, 'themes', f), os.path.join(ROOT, 'themes', f))

s = open(os.path.join(ED, 'index.html')).read()
def sub(pat, new, flags=0):
    global s
    s2, n = re.subn(pat, lambda m: new, s, count=1, flags=flags)
    assert n == 1, 'not found: ' + pat[:60]
    s = s2

sub(r'<base href="[^"]*">', '<base href="/goat/">')
sub(r'<title>[^<]*</title>', '<title>Learn Goat Format: Yu-Gi-Oh! as It Was in 2005 | Learn Retro</title>')
sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="A free course for Goat format Yu-Gi-Oh!: lessons from your first summon to tournament decks, every Goat-legal card, deck lists and the April 2005 banlist.">')
sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="https://learnretro.com/goat/">')
sub(r'<!-- Public since[^\n]*-->', '<!-- Public since 2026-11-23 (Zack: launch Goat with the move to learnretro.com/goat/). -->')
s = s.replace("localStorage.getItem('edison:theme')", "localStorage.getItem('goat:theme')")
s = re.sub(r'(<link rel="stylesheet" href="themes/index\.css(\?v=[^"]*)?">)', lambda m: m.group(1) + f'\n<link rel="stylesheet" href="themes/goat.css{m.group(2) or ""}">', s, count=1)
# The format pill: Goat is the current format.
s = s.replace('<div class="fmtsw" data-fmt="edison">', '<div class="fmtsw" data-fmt="goat">')
s = re.sub(r'(<button type="button" class="bfmt" id="fmtbtn"[^>]*>)Edison', r'\1Goat', s, count=1)

# Section menus: Goat's pages (no Library, Rulings, Errata, Know your opponent or duel yet).
menus = '''  <nav class="nav" id="nav" aria-label="Sections">
    <a href="./" data-v="home">Home</a>
    <div class="ndrop"><button type="button" class="ndrop-btn" data-menu="m-learn" data-group="course lesson flashcards rules glossary" aria-haspopup="true" aria-expanded="false">Learn ▾</button></div>
    <div class="ndrop"><button type="button" class="ndrop-btn" data-menu="m-cards" data-group="cards staples banlist" aria-haspopup="true" aria-expanded="false">Cards ▾</button></div>
    <div class="ndrop"><button type="button" class="ndrop-btn" data-menu="m-decks" data-group="deck builder" aria-haspopup="true" aria-expanded="false">Decks ▾</button></div>
    <div class="ndrop"><button type="button" class="ndrop-btn" data-menu="m-play" data-group="simulator" aria-haspopup="true" aria-expanded="false">Play ▾</button></div>
  </nav>
  <div class="ndrop-menu" id="m-learn" role="menu" aria-label="Learn">
    <a href="course/" role="menuitem">Course<small>Step 0, Goat 101 and 201</small></a>
    <a href="flashcards/" role="menuitem">Flashcards<small>Every quiz question, to drill</small></a>
    <a href="rules/" role="menuitem">Rules<small>How a duel works, 2005 rules</small></a>
    <a href="glossary/" role="menuitem">Glossary<small>Every term, in plain words</small></a>
  </div>
  <div class="ndrop-menu" id="m-cards" role="menu" aria-label="Cards">
    <a href="cards/" role="menuitem">Card search<small>All 1,691 Goat-legal cards</small></a>
    <a href="staples/" role="menuitem">Staples<small>Cards most decks play</small></a>
    <a href="banlist/" role="menuitem">Banlist<small>April 2005 list</small></a>
  </div>
  <div class="ndrop-menu" id="m-decks" role="menu" aria-label="Decks">
    <a href="decks/" role="menuitem">All Decks<small>Top and most played decks</small></a>
    <a href="builder/" role="menuitem">Deck builder<small>Build, check and export</small></a>
  </div>
  <div class="ndrop-menu" id="m-play" role="menu" aria-label="Play">
    <a href="simulator/" role="menuitem">Practice board<small>Set up any field and try plays</small></a>
  </div>
'''
sub(r'  <nav class="nav" id="nav".*?(?=  <div class="ssearch")', menus, re.S)

scripts = '''<!-- Card data from YGOPRODeck (the Goat pool and banlist, checked against goatformat.com), built by build/build_data.py -->
<script src="data/cards.js"></script>
<script src="data/decks.js"></script>
<script src="data/meta.js"></script>
<script src="data/lessons-step0.js"></script>
<script src="data/lessons-101.js"></script>
<script src="data/lessons-201.js"></script>
<script src="data/rules.js"></script>
'''
sub(r'<!-- Card data, rulings.*?(?=<script src="js/app\.js)', scripts, re.S)
assert 'edison' not in re.sub(r'data-fmt="edison"|href="/edison/"|<b>Edison</b>', '', s).lower().replace('edisonformat', ''), 'Edison text left in the Goat shell'
open(os.path.join(ROOT, 'index.html'), 'w').write(s)
shutil.copyfile(os.path.join(ROOT, 'index.html'), os.path.join(ROOT, '404.html'))
print('Goat shell synced from Edison: index.html, 404.html, themes/base.css, themes/index.css')
