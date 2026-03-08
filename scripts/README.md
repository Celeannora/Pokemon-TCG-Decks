# Scripts

## fetch_and_categorize_cards.py

Fetches all Standard-legal Pokémon TCG cards from the [Pokémon TCG API](https://pokemontcg.io/) (v2) and outputs them as letter-split CSV files in `card_data/`.

### Requirements

```bash
pip install requests
```

### Usage

```bash
python scripts/fetch_and_categorize_cards.py
```

### Optional: API key

Set the `POKEMONTCG_API_KEY` environment variable for higher rate limits:

```bash
export POKEMONTCG_API_KEY=your-api-key-here
python scripts/fetch_and_categorize_cards.py
```

Get a free API key at: https://dev.pokemontcg.io/

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

The script queries `legalities.standard:legal` from the API, so only Standard-legal cards are included. After Standard rotation, simply re-run the script to get the updated legal card pool.

### File size

Each CSV file targets ≤80KB for reliable GitHub API access. If a single letter (e.g., Pokémon starting with S) exceeds this, the script automatically splits into `pokemon_s1.csv`, `pokemon_s2.csv`, etc.

---

**Data source**: [Pokémon TCG API](https://pokemontcg.io/) v2
