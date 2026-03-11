# Scripts

## fetch_and_categorize_cards.py

Fetches all Standard-legal Pokémon TCG cards from the [PokemonTCG/pokemon-tcg-data](https://github.com/PokemonTCG/pokemon-tcg-data) static JSON repository and outputs them as letter-split CSV files in `card_data/`.

> **No API key needed. No rate limits.** Reads static JSON files directly from GitHub.

### Requirements

```bash
pip install requests
```

### Usage

```bash
python scripts/fetch_and_categorize_cards.py
```

### Output structure

```
card_data/
├── _INDEX.md
├── pokemon/
│   ├── pokemon_a.csv
│   ├── pokemon_b.csv
│   └── ...
├── trainer/
│   ├── trainer_a.csv
│   └── ...
└── energy/
    ├── energy_b.csv
    └── ...
```

### CSV columns

| Column | Description |
|--------|-------------|
| `name` | Card name as printed |
| `supertype` | Pokémon, Trainer, or Energy |
| `subtypes` | Comma-separated: Basic, Stage 1, ex, Item, Supporter, etc. |
| `hp` | Hit points (Pokémon only) |
| `types` | Energy types: Fire, Water, Grass, Lightning, etc. |
| `evolves_from` | Name of the Pokémon this card evolves from |
| `abilities` | Formatted as: [Type] Name: Text |
| `attacks` | Formatted as: [Cost] Name Damage — Effect text |
| `weaknesses` | Type and value, e.g. Fire ×2 |
| `resistances` | Type and value, e.g. Grass -30 |
| `retreat_cost` | Number of energy required to retreat |
| `set_code` | PTCGL set code (e.g. SVI, OBF, PAL) |
| `set_name` | Full set name |
| `number` | Collector number within set |
| `rarity` | Card rarity |
| `regulation_mark` | Letter mark for format legality |
| `rules` | Special rules text (ex rules, etc.) |

### Filtering

The script filters by **Regulation Mark** (`G`, `H`, `I`, `J`, …) — **not** the `legalities.standard` field, which is stale after rotations. Basic Energy cards from SVE (no regulation mark) are always included.

Only sets from the Scarlet & Violet series and Mega Evolution series are scanned, avoiding 100+ irrelevant older set files.

### File size

Each CSV file targets ≤80KB for reliable GitHub API access. If a single letter (e.g., Pokémon starting with S) exceeds this, the script automatically splits into `pokemon_s1.csv`, `pokemon_s2.csv`, etc.

### When to re-run

Re-run after any Standard rotation or new set release:

```bash
python scripts/fetch_and_categorize_cards.py
```

If new regulation marks are introduced, add them to `LEGAL_REG_MARKS` in the script.

---

## validate_deck.py

Validates a PTCGL-format `decklist.txt` file for legality and format compliance.

### Usage

```bash
python scripts/validate_deck.py Decks/2026-03-10_Charizard_ex/decklist.txt
```

### Checks performed

- Exactly 60 cards total
- No more than 4 copies of any non-Basic-Energy card
- Section totals match actual card counts
- Valid PTCGL line format (`<count> <name> <set_code> <number>`)
- ACE SPEC violations (more than 1 ACE SPEC card)
- Reports pass/fail with detailed error messages

---

**Data source**: [PokemonTCG/pokemon-tcg-data](https://github.com/PokemonTCG/pokemon-tcg-data)
