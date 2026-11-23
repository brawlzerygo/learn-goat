# Goat course outline (OK'd by Zack 2026-11-23; all 21 lessons drafted the same day)

Settled with Zack (2026-11-23): Step 0 + Goat 101 + Goat 201; all Edison site features but the duel engine
(cards + banlist, flashcards + glossary, rules page, decks + builder + practice board); goatformat.com's standard
(April 2005 TCG list unchanged, pool as of Aug 17, 2005: TLM in, EXU and CRV out); decks: the top and most played
ones first, more later.

## Step 0: How to play Yu-Gi-Oh! (new wording, more hands-on than Edison's)
0.1 The goal: Life Points, the Deck, three ways to win
0.2 Reading a card: monsters, Spells, Traps, Fusion monsters
0.3 The field and the six phases
0.4 Summoning: Normal, Tribute, Set, Flip, Special, Fusion
0.5 Battle: positions, attacks, damage, direct attacks
0.6 Spells, Traps, chains and Spell Speed
0.7 A practice turn, played step by step on the board

## Goat 101: the format
1 Welcome to 2005: what Goat is, the name, why people still play it
2 How a Goat match works: the 2005 rules (first player draws, the Fusion Deck, deck sizes, best of three, siding)
3 Reading 2005 card text: "Magic Card", "remove from play", old wording vs today
4 The card pool and the banlist
5 The staples: the cards almost every deck plays
6 The power monsters: Black Luster Soldier - Envoy, Chaos Sorcerer, Breaker, Thousand-Eyes Restrict
7 Your first Goat game, turn by turn

## Goat 201: playing to win
8 Rules that trip people up: priority, triggers on a chain, the Damage Step, the June 2005 flip rule
9 Card advantage: trading one for one, and getting ahead
10 Goat Control
11 Chaos Turbo and Chaos Control
12 Warriors and the aggro decks
13 Burn, Empty Jar and the lockdown decks
14 Side decking and picking your deck

## Episodes
- Ep 1: Step 0 + lesson 1 (How to Play Goat Format, beginner's guide)
- Ep 2: Goat 101 (lessons 2-7, ending on the full game)
- Ep 3: Goat 201 (lessons 8-14); deck guides can be cut out as their own videos later

## Build
- Repo: learn-edison/goat/ (its own git repo like hub/), published to brawlzerygo/learn-goat at goat.learnretro.com
  via publish.sh --site goat (needs the Namecheap CNAME goat). Hub keeps "Coming soon" until launch.
- Data: YGOPRODeck API (format=goat, ban_goat), checked against goatformat.com's pool and list; art cached in img/.
