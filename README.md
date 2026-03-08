# Pokémon TCG Deck Repository

## Overview

This repository contains rigorously analyzed, format-legal Pokémon TCG decklists built through AI-assisted optimization. Every deck undergoes exhaustive strategic analysis before publication. All decklists are **PTCGL-importable** — paste directly into Pokémon TCG Live.

**Repository status**: ✅ Fully self-sufficient — contains a complete Standard card database and AI deck-building instructions.

---

## Repository structure

```
Pokemon-TCG-Decks/
├── Decks/                              # All generated decks (never modify manually)
│   └── YYYY-MM-DD_Archetype_Name/
│       ├── decklist.txt                # PTCGL-importable decklist
│       ├── analysis.md                 # Card-by-card reasoning and strategy
│       └── matchup_guide.md            # Matchup-specific game plans
├── card_data/                          # Standard card database (CSV, auto-generated)
│   ├── _INDEX.md                       # File listing and lookup guide
│   ├── pokemon/                        # pokemon_a.csv … pokemon_z.csv
│   ├── trainer/
│   └── energy/
├── scripts/
│   └── fetch_and_categorize_cards.py   # Regenerates card_data/ from static GitHub data
├── Deck_builder_instructions.md        # AI methodology and workflow
├── Deck_building_guidelines.md         # Quick reference for AI assistants
├── Rules_reference.md                  # Pokémon TCG rules reference
├── Changelog.md
└── README.md
```

---

## Card database

All Standard-legal cards are stored in `card_data/`, organized by supertype and split by first letter of card name.

**Data source**: [PokemonTCG/pokemon-tcg-data](https://github.com/PokemonTCG/pokemon-tcg-data) — static JSON files, no API key needed, no rate limits.

- **Standard filter**: Regulation Mark G and later (G, H, I, J) + Basic Energy (always legal)
- **Path format**: `card_data/{supertype}/{supertype}_{letter}.csv`
- **Example**: Charizard ex (Pokémon, starts with C) → `card_data/pokemon/pokemon_c.csv`
- **File size**: Each file targets ≤80KB for reliable GitHub API access
- **Index**: `card_data/_INDEX.md` lists every file with card counts and sizes
- **Columns**: `name`, `supertype`, `subtypes`, `hp`, `types`, `evolves_from`, `abilities`, `attacks`, `weaknesses`, `resistances`, `retreat_cost`, `set_code`, `set_name`, `number`, `rarity`, `regulation_mark`, `rules`

To update after Standard rotation or a new set release:
```bash
pip install requests
python scripts/fetch_and_categorize_cards.py
```

The script reads set metadata from `sets/en.json` and card data from `cards/en/{set_id}.json` directly from [PokemonTCG/pokemon-tcg-data](https://github.com/PokemonTCG/pokemon-tcg-data). It filters by **Regulation Mark** (not the upstream `legalities.standard` field, which is stale after rotations) and exports letter-split CSVs with full card text.

---

## PTCGL decklist format

All decklists use the official Pokémon TCG Live import format:

```
Pokémon: 15
2 Charizard ex OBF 125
2 Charmeleon OBF 27
3 Charmander MEW 4
...

Trainer: 33
4 Professor's Research SVI 190
4 Iono PAL 185
4 Ultra Ball SVI 196
...

Energy: 12
8 Basic {R} Energy SVE 2
4 Reversal Energy PAL 192

Total Cards: 60
```

Line format: `<count> <card_name> <set_code> <collector_number>`

---

## For AI assistants

1. Read `Deck_builder_instructions.md` for the full methodology
2. To look up a card: identify its supertype and first letter, load the matching file from `card_data/`
3. Use `card_data/_INDEX.md` if you are unsure which file to open
4. Save all completed decks to `Decks/` with the standard folder structure

---

## For deck builders (human)

1. Browse `Decks/` organized by date and archetype
2. Copy the contents of `decklist.txt` and paste into PTCGL deck import
3. Read `analysis.md` for detailed card reasoning
4. Consult `matchup_guide.md` for matchup strategies

---

## Format supported

- **Standard** (default — full database support, Regulation Mark G and later)

Only Standard has full card database support. Expanded and other formats require manual legality verification.

---

## Philosophy

Every card choice is strategically justified. Every matchup consideration is rigorously challenged. No deck is published without surviving brutal self-critique.

**Failure is acceptable. Unjustified mediocrity is not.**

---

**Maintained by**: Celeannora
**Last updated**: March 8, 2026
**Version**: 1.2
**Powered by**: [Perplexity AI](https://www.perplexity.ai)
**Card data**: [PokemonTCG/pokemon-tcg-data](https://github.com/PokemonTCG/pokemon-tcg-data)
