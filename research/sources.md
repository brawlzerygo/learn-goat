# Goat format: research notes (v1, 2026-11-23)

Facts in our own words, each with its source. Nothing here is copied text. Card names and banlist entries are facts.

## Sources read
| Source | URL | Used for |
|---|---|---|
| goatformat.com, What is Goat | https://www.goatformat.com/whatisgoat.html | name, history, community standard |
| goatformat.com, Card pool | https://www.goatformat.com/cardpool.html | legal sets, promos, banlist |
| goatformat.com, Rules | https://www.goatformat.com/rules.html | how rulings are applied |
| goatformat.com, Basics (Goat rules 1-20) | https://www.goatformat.com/basics.html | rules that differ from today |
| goatformat.com, Decks / tier lists | https://www.goatformat.com/decks.html, /home/category/tier-list | archetypes |
| goatformat.com, Chaos Turbo | https://www.goatformat.com/chaos-turbo.html | a sample list (Worlds 2020) |
| YGOPRODeck, An Introduction to Goat Format | https://ygoprodeck.com/an-introduction-to-goat-format/ | versions of the format, deck families, the June 2005 position rule |
| YGOPRODeck API v7 | https://ygoprodeck.com/api-guide/ | card data: `format=goat`, `banlist_info.ban_goat` |
| Blocked this run | yugipedia.com (403), formatlibrary.com (JS only) | try again via the browser pane if needed |

## What Goat is
- A format played in summer 2005, named for how popular Scapegoat was; the signature deck, Goat Control, paired Scapegoat with Metamorphosis. Konami doesn't support it; players keep it alive. (whatisgoat)
- The card pool never changes, decks are cheap next to modern play, and games are slow and control-heavy with a lot of reading the opponent. (YGOPRODeck intro)
- Still active in 2026: a yearly World Championship, Obelisk and PWCQ events, Chaos Turbo the most played deck per goatformat.com news (Oct 2026). (goatformat.com home)

## Card pool (community standard)
- Every card legal at premier events on August 17, 2005 (the SJC Indianapolis pool; the same as US Nationals and SJC Seattle). The Lost Millennium is in; Exarion Universe and Cybernetic Revolution are out. (cardpool, whatisgoat)
- Sets: LOB, SDY/SDK, MRD, MRL/SRL, PSV, SDJ/SDP, LON, LOD, PGD, MFC, DCR, SYE/SKE, IOC, AST, SOD, DB1, RDS, FET, DR1, TLM, SD1-SD4, DB2, plus promos (JMP up to Archfiend of Gilfer, SP1 up to Embodiment of Apophis; full list on cardpool). (cardpool)
- Other versions exist: pre-June 2005 (no TLM), Exarion (adds EXU and CT2, played in the 2012-2016 revival), Post-CRV (only SJC Boston 2005). The Pre-Exarion one is the standard. (YGOPRODeck intro)

## Banlist: the TCG list of April 2005, unchanged (cardpool)
- Forbidden (17): Chaos Emperor Dragon - Envoy of the End, Fiber Jar, Magical Scientist, Makyura the Destructor, Witch of the Black Forest, Yata-Garasu, Butterfly Dagger - Elma, Change of Heart, Confiscation, Dark Hole, Harpie's Feather Duster, Mirage of Nightmare, Monster Reborn, Painful Choice, Raigeki, The Forceful Sentry, Imperial Order.
- Limited (41): Black Luster Soldier - Envoy of the Beginning, Breaker the Magical Warrior, Cyber Jar, Dark Magician of Chaos, D.D. Warrior Lady, Exodia the Forbidden One + the four limbs, Exiled Force, Injection Fairy Lily, Jinzo, Morphing Jar, Protector of the Sanctuary, Reflect Bounder, Sacred Phoenix of Nephthys, Sangan, Sinister Serpent, Tribe-Infecting Virus, Twin-Headed Behemoth, Card Destruction, Delinquent Duo, Graceful Charity, Heavy Storm, Lightning Vortex, Mage Power, Mystical Space Typhoon, Pot of Greed, Premature Burial, Snatch Steal, Swords of Revealing Light, United We Stand, Call of the Haunted, Ceasefire, Deck Devastation Virus, Magic Cylinder, Mirror Force, Reckless Greed, Ring of Destruction, Torrential Tribute.
- Semi-Limited (15): Abyss Soldier, Dark Scorpion - Chick the Yellow, Manticore of Darkness, Marauding Captain, Night Assailant, Vampire Lord, Creature Swap, Emergency Provisions, Level Limit - Area B, Nobleman of Crossout, Reinforcement of the Army, Upstart Goblin, Good Goblin Housekeeping, Gravity Bind, Last Turn.
- To check: the page also shows the list as an image; compare it with the text, and with YGOPRODeck's `ban_goat` data.

## Rules that differ from today (basics, rules)
- Rulings are applied the way a 2005 head judge would, even where today's rules differ. Anything not listed works as it does now.
- The first player draws on turn 1 (opens with 6). They still can't attack that turn (to confirm against the 2005 rulebook).
- The Extra Deck was the Fusion Deck: Fusion monsters only, no size limit then. No Synchro, Xyz, Pendulum, Link; no Extra Monster Zone.
- Main Deck: 40 minimum; the 2005 rules set no maximum (simulators cap at 60). Side Deck 0 or 15.
- One face-up Field Spell for the whole field; a new one destroys the old.
- Priority: after a summon or chain resolves, the turn player may use a fast effect or an Ignition effect before the opponent responds.
- A replay is a new attack declaration.
- SEGOC: earlier triggers go on the chain before later ones.
- Damage Step: six sub-steps, one chain per sub-step, and only monster effects that negate activations can be used in it.
- Matches are best of three, played to two wins, no match draws.
- 0 ATK vs 0 ATK: both destroyed. A Life Point cost can't take you to 0 (except Chain Energy).
- June 2005 change: a monster turned face-down by a card effect no longer uses up its once-per-turn position change, which is what lets Goat Control flip Magician of Faith and others again. (YGOPRODeck intro)
- Old card words: "remove from play" = banish; "Magic" = Spell on early prints.

## Decks (goatformat.com tier list 2018, usage based; news 2026)
- Top: Goat Control, Thunder Dragon Chaos (Chaos Turbo). High: Chaos Control, Anti-Meta Warriors, Reasoning Gate Combo. Mid: Burn, Chaos Recruiter, Empty Jar, Flip Control.
- goatformat.com has about 80 deck guides (Lockdown, Control, Aggro, Combo) with lists; DuelingBook deck links for current event lists.

## Data plan
- Cards and art: YGOPRODeck API `format=goat` and `banlist_info.ban_goat` (cache, download art once into our img/, never hotlink), checked against the goatformat.com pool and banlist.
- No downloadable lists on goatformat.com; deck lists would be typed in from its guides/event coverage, credited.

## Second pass (2026-11-23)
- goatformat.com/whygoat.html: calls Goat the most popular historical format; pitch = resource and card-advantage play,
  deck variety, a fixed pool, a non-profit community. gettingintogoat.html: rules, watch games, Discord, tier list,
  build, play on DuelingBook's Goat room, review replays.
- goatformat.com/basics.html rule 2: Side Deck must be 0 or 15 (rarely enforced); rule 19 implies the 6-card hand limit.
- goatworld.community/wiki/game-rules: 8000 LP, 5-card hand, Main 40-60, Fusion Deck 0-15, hand limit 6. It
  contradicts itself on the first-turn draw, so it is not used as a source.
- wikiformat.com (Italian fan site), Goat turn phases: first player draws, hand limit 6, six-step Damage Step.
- Conflicts: Fusion Deck size (goatformat.com: no limit in 2005; goatworld: 0-15). We follow goatformat.com and note
  that simulators may cap it.
- **Settled by Zack (2026-11-23): the player going first can't attack on turn 1** (no Battle Phase that turn). Was open: No source read so far says either way (searches turned
  up only NeoGoat, a modern variant, where they can't). Lessons avoid the point until it is sourced; candidates: the
  2005 rulebook (version 5 or 6), goatformat.com's rulings pages, DuelingBook's Goat room behaviour.

## Third pass: decks and strategy (2026-11-23)
- Deck guides read on goatformat.com: goat-control, chaos-control, chaos-turbo, flip-control, warrior, chaos-recruiter,
  zombie, burn, lockdown-burn, empty-jar, reasoning-gate-otk (lists in build/decks/decks.txt; Flip Control's lists
  print 46 cards, so it is left out).
- Strategy: goatformat.com/home/introduction-to-goat-format-power-cards-part-2, /home/can-i-play-3-of-a-flip,
  /home/dust-tornado-vs-snatch-steal, /home/four-steps-for-better-side-decking-in-goat-format,
  /home/transition-sidedecking-for-goat-format, /home/sidedecking-for-alt-win-burn-combo-in-goat-format,
  /home/goat-format-tier-list (2020: A Chaos Turbo, Chaos Control, Goat Control, Angel Chaos Control, Dimension
  Fusion Turbo, Flip Control; B Reasoning Gate, Library FTK, Empty Jar, Beatdown, PACMAN, Burn; C Soul Control, Heavy
  Slump Chaos, Chaos Recruiter, Spell Canceller Warrior, Spirits, Gravekeeper's; D Zombies, Skill Drain Burn,
  Beastdown; E Rescue Cat, Ben Kei, Cyber-Stein, Exodia). The 2021 list is images only, not read.
- YGOPRODeck intro: Goat Control is the deck for new players; more than +1 in a turn is rare and decisive.
