# Scripts

## fetch_and_categorize_cards.py

Fetches all Standard-legal Pokémon TCG cards from the static
[PokemonTCG/pokemon-tcg-data](https://github.com/PokemonTCG/pokemon-tcg-data)
repository and outputs them as letter-split CSV files in `card_data/`.

No API key needed. No rate limits.

### Requirements

```bash
pip install requests
```

### Usage

```bash
python scripts/fetch_and_categorize_cards.py
```

### Filtering

The script filters by **regulation mark**, not by the upstream `legalities.standard`
field (which is stale after format rotations).

- **Standard-legal**: Regulation Marks G, H, I, J
- **Always-legal**: Basic Energy from `sve` (no regulation mark)
- **Series scanned**: Scarlet & Violet + Mega Evolution (avoids downloading 100+ irrelevant old set files)

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
| `regulation_mark` | Letter mark for format legality (G, H, I, J, …) |
| `rules` | Special rules text (ex rules, VSTAR Power, etc.) |

### File size

Each CSV file targets ≤80KB for reliable GitHub API access. If a single letter
(e.g., Pokémon starting with S) exceeds this, the script automatically splits
into `pokemon_s1.csv`, `pokemon_s2.csv`, etc.

---

## validate_deck.py

Validates a PTCGL-format `decklist.txt` file against Standard deck-building rules.

### Usage

```bash
python scripts/validate_deck.py Decks/2026-03-10_Archetype_Name/decklist.txt
```

### Checks performed

- Exactly 60 cards total
- No more than 4 copies of any non-Basic-Energy card
- Section totals match card counts
- `Total Cards:` line matches computed total
- Valid PTCGL line format (`<count> <name> <SET> <number>`)
- ACE SPEC violation detection (> 1 total ACE SPEC copy)

---

**Data source**: [PokemonTCG/pokemon-tcg-data](https://github.com/PokemonTCG/pokemon-tcg-data)
