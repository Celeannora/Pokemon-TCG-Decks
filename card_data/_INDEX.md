# Card data index

Last updated: 2026-03-08 09:09 UTC

Data source: [PokemonTCG/pokemon-tcg-data](https://github.com/PokemonTCG/pokemon-tcg-data)

Standard format: Regulation Mark G, H, I, J (and Basic Energy)

## How to find a card

**Pattern**: `card_data/{supertype}/{supertype}_{first_letter}.csv`

**Example**: Charizard ex → `card_data/pokemon/pokemon_c.csv`

**Example**: Professor's Research → `card_data/trainer/trainer_p.csv`

**Example**: Basic Grass Energy → `card_data/energy/energy_b.csv`

---

## Files by supertype

### Energy (38 cards)

| File | Cards | Size |
|------|-------|------|
| `energy/energy_b.csv` | 18 | 1.9 KB |
| `energy/energy_e.csv` | 1 | 0.5 KB |
| `energy/energy_i.csv` | 2 | 0.8 KB |
| `energy/energy_j.csv` | 2 | 0.7 KB |
| `energy/energy_l.csv` | 3 | 1.3 KB |
| `energy/energy_m.csv` | 2 | 0.7 KB |
| `energy/energy_n.csv` | 1 | 0.6 KB |
| `energy/energy_p.csv` | 2 | 0.7 KB |
| `energy/energy_r.csv` | 2 | 1.0 KB |
| `energy/energy_s.csv` | 2 | 0.9 KB |
| `energy/energy_t.csv` | 3 | 1.1 KB |

### Pokemon (3581 cards)

| File | Cards | Size |
|------|-------|------|
| `pokemon/pokemon_a.csv` | 149 | 45.9 KB |
| `pokemon/pokemon_b.csv` | 144 | 41.7 KB |
| `pokemon/pokemon_c.csv` | 287 | 82.0 KB |
| `pokemon/pokemon_d.csv` | 180 | 49.6 KB |
| `pokemon/pokemon_e.csv` | 121 | 37.0 KB |
| `pokemon/pokemon_f.csv` | 149 | 43.6 KB |
| `pokemon/pokemon_g1.csv` | 106 | 36.7 KB |
| `pokemon/pokemon_g2.csv` | 104 | 32.4 KB |
| `pokemon/pokemon_h.csv` | 133 | 41.7 KB |
| `pokemon/pokemon_i.csv` | 92 | 36.9 KB |
| `pokemon/pokemon_j.csv` | 26 | 8.9 KB |
| `pokemon/pokemon_k.csv` | 97 | 30.6 KB |
| `pokemon/pokemon_l.csv` | 145 | 39.3 KB |
| `pokemon/pokemon_m1.csv` | 183 | 62.7 KB |
| `pokemon/pokemon_m2.csv` | 181 | 60.6 KB |
| `pokemon/pokemon_n.csv` | 94 | 23.7 KB |
| `pokemon/pokemon_o.csv` | 46 | 14.7 KB |
| `pokemon/pokemon_p1.csv` | 122 | 35.9 KB |
| `pokemon/pokemon_p2.csv` | 121 | 30.7 KB |
| `pokemon/pokemon_q.csv` | 22 | 6.4 KB |
| `pokemon/pokemon_r.csv` | 129 | 37.9 KB |
| `pokemon/pokemon_s1.csv` | 192 | 53.4 KB |
| `pokemon/pokemon_s2.csv` | 191 | 49.1 KB |
| `pokemon/pokemon_t.csv` | 306 | 96.3 KB |
| `pokemon/pokemon_u.csv` | 8 | 3.2 KB |
| `pokemon/pokemon_v.csv` | 93 | 24.6 KB |
| `pokemon/pokemon_w.csv` | 90 | 28.9 KB |
| `pokemon/pokemon_x.csv` | 6 | 2.1 KB |
| `pokemon/pokemon_y.csv` | 19 | 5.3 KB |
| `pokemon/pokemon_z.csv` | 45 | 13.4 KB |

### Trainer (582 cards)

| File | Cards | Size |
|------|-------|------|
| `trainer/trainer_a.csv` | 40 | 15.4 KB |
| `trainer/trainer_b.csv` | 50 | 14.8 KB |
| `trainer/trainer_c.csv` | 51 | 14.8 KB |
| `trainer/trainer_d.csv` | 23 | 6.8 KB |
| `trainer/trainer_e.csv` | 32 | 8.4 KB |
| `trainer/trainer_f.csv` | 19 | 5.6 KB |
| `trainer/trainer_g.csv` | 26 | 8.2 KB |
| `trainer/trainer_h.csv` | 15 | 5.4 KB |
| `trainer/trainer_i.csv` | 11 | 3.5 KB |
| `trainer/trainer_j.csv` | 18 | 5.5 KB |
| `trainer/trainer_k.csv` | 9 | 3.1 KB |
| `trainer/trainer_l.csv` | 35 | 11.3 KB |
| `trainer/trainer_m.csv` | 25 | 8.5 KB |
| `trainer/trainer_n.csv` | 23 | 5.2 KB |
| `trainer/trainer_o.csv` | 6 | 2.4 KB |
| `trainer/trainer_p.csv` | 68 | 19.6 KB |
| `trainer/trainer_r.csv` | 27 | 8.5 KB |
| `trainer/trainer_s.csv` | 35 | 11.3 KB |
| `trainer/trainer_t.csv` | 52 | 18.3 KB |
| `trainer/trainer_u.csv` | 7 | 2.2 KB |
| `trainer/trainer_v.csv` | 2 | 0.9 KB |
| `trainer/trainer_w.csv` | 5 | 1.5 KB |
| `trainer/trainer_x.csv` | 2 | 0.6 KB |
| `trainer/trainer_y.csv` | 1 | 0.3 KB |

## CSV columns

`name`, `supertype`, `subtypes`, `hp`, `types`, `evolves_from`, `abilities`, `attacks`, `weaknesses`, `resistances`, `retreat_cost`, `set_code`, `set_name`, `number`, `rarity`, `regulation_mark`, `rules`

## Column descriptions

| Column | Description |
|--------|-------------|
| `name` | Card name as printed |
| `supertype` | Pokémon, Trainer, or Energy |
| `subtypes` | Comma-separated: Basic, Stage 1, Stage 2, ex, V, Item, Supporter, etc. |
| `hp` | Hit points (Pokémon only) |
| `types` | Energy types: Fire, Water, Grass, Lightning, Psychic, Fighting, etc. |
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
| `rules` | Special rules text (ex rules, VSTAR Power, etc.) |
