# Changelog

## v1.0 — March 8, 2026

### New
- Initial repository for Pokémon TCG deck building
- `card_data/` directory structure with supertype subfolders and letter-split CSVs
- `scripts/fetch_and_categorize_cards.py` fetches Standard-legal cards from pokemontcg.io API
- `Deck_builder_instructions.md` — full AI methodology and workflow
- `Deck_building_guidelines.md` — quick reference for AI assistants
- `Rules_reference.md` — Pokémon TCG rules reference
- `.github/DECK_TEMPLATE/decklist.txt` — PTCGL-importable template
- PTCGL import format for all decklists
- README with full repository documentation

### Design decisions
- Modeled after [MTG-Decks](https://github.com/Celeannora/MTG-Decks) repository structure
- Card data sourced from [Pokémon TCG API](https://pokemontcg.io/) v2
- Max file size ≤80KB per CSV for reliable GitHub API access
- Cards categorized by supertype (Pokémon, Trainer, Energy) instead of MTG types
- Decklist format uses official PTCGL import syntax

---

**Maintained by**: Celeannora | **AI engine**: Perplexity
