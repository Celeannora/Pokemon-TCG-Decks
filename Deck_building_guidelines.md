# Deck building guidelines

Quick reference for AI assistants. For the full methodology see `Deck_builder_instructions.md`.

---

## Card database lookup

| What you need | Where to look |
|---|---|
| Full file index | `card_data/_INDEX.md` |
| A Pokémon starting with C | `card_data/pokemon/pokemon_c.csv` |
| A Trainer starting with P | `card_data/trainer/trainer_p.csv` |
| An Energy starting with B | `card_data/energy/energy_b.csv` |

**Pattern**: `card_data/{supertype}/{supertype}_{first_letter}.csv`

Files are ≤80KB. Open the specific file you need — do not scan all files.

---

## Deck construction checklist

- [ ] Card database loaded for relevant supertypes
- [ ] Format legality verified for every card (Standard — Regulation Mark G+)
- [ ] Exactly 60 cards confirmed
- [ ] No more than 4 copies of any card (except Basic Energy)
- [ ] ACE SPEC limit respected (max 1 per deck)
- [ ] Radiant limit respected (max 1 per deck)
- [ ] Energy line math validated
- [ ] Evolution lines have proper counts
- [ ] Minimum 3 weaknesses identified
- [ ] Decklist is valid PTCGL import format
- [ ] `scripts/validate_deck.py` passes
- [ ] Deck saved to `Decks/YYYY-MM-DD_Archetype_Name/`

---

## PTCGL decklist format

```
Pokémon: <total_pokemon_count>
<qty> <Card Name> <SET_CODE> <Collector_Number>

Trainer: <total_trainer_count>
<qty> <Card Name> <SET_CODE> <Collector_Number>

Energy: <total_energy_count>
<qty> <Card Name> <SET_CODE> <Collector_Number>

Total Cards: 60
```

Each card line: `<count> <name> <set_code> <number>`

The last two tokens on a card line are **always** the set code and collector number.

---

## Pokémon TCG deck building rules

| Rule | Value |
|---|---|
| Deck size | Exactly 60 cards |
| Max copies per card | 4 (by name, except Basic Energy) |
| Basic Energy | Unlimited copies |
| Prism Star / ACE SPEC | 1 per deck |
| Radiant Pokémon | 1 per deck |
| Format | Standard (Regulation Mark G+) |

---

## Typical card count ranges

| Category | Range | Notes |
|---|---|---|
| Pokémon | 10–20 | Depends on evolution lines |
| Trainer - Supporters | 8–14 | Draw, disruption, boss |
| Trainer - Items | 12–22 | Balls, tools, switch, recovery |
| Trainer - Stadiums | 2–4 | Tech stadiums |
| Energy - Basic | 6–14 | Depends on acceleration |
| Energy - Special | 0–4 | Jet Energy, etc. |

---

## File naming conventions

| Folder / file | Purpose |
|---|---|
| `Decks/YYYY-MM-DD_Archetype/` | Generated deck output |
| `card_data/` | Card database root |
| `card_data/_INDEX.md` | Master index of all card files |
| `Deck_builder_instructions.md` | Full AI methodology |
| `Deck_building_guidelines.md` | This file |
| `Rules_reference.md` | Pokémon TCG rules reference |
| `Changelog.md` | Project change history |
| `scripts/validate_deck.py` | Decklist validator |
| `scripts/fetch_and_categorize_cards.py` | Card database updater |

---

## Output file structure

```
Decks/
└── 2026-03-08_Dragapult_ex/
    ├── decklist.txt        ← PTCGL importable
    ├── analysis.md         ← full reasoning
    └── matchup_guide.md    ← matchup plans
```

---

## When database is not accessible

1. Tell the user the database is unavailable
2. Ask for: card name, supertype, subtypes, HP, types, attacks, abilities, set code, collector number
3. Proceed using user-provided details
4. Note in `analysis.md`: "Card legality user-confirmed"

---

## Version history

| Version | Date       | Notes |
|---------|------------|-------|
| 1.1     | 2026-03-10 | Updated for Regulation Mark G+; added ACE SPEC/Radiant rules; validate_deck.py in checklist |
| 1.0     | 2026-03-08 | Initial quick-reference for AI assistants |

**Last updated**: March 10, 2026 | **Version**: 1.1
