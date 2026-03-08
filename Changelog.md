# Changelog

## v1.2 — March 8, 2026

### Fixed
- **Critical: Standard legality filter now uses Regulation Mark G+ instead of stale `legalities.standard` field**
  - The upstream `legalities.standard` in pokemon-tcg-data is NOT updated after format rotations
  - SWSH-era cards (Reg Mark D/E/F) were incorrectly included as “Standard Legal”
  - Now filters by `regulationMark ∈ {G, H, I, J}` which is the authoritative indicator
  - Basic Energy from SVE (no regulation mark) handled as always-legal
- Only scans Scarlet & Violet + Mega Evolution series sets (avoids downloading 100+ irrelevant old set files)
- Rules_reference.md corrected from “H and later” to “G and later”
- Added missing set codes: JTG, DRI, BLK, WHT, MEG, PFL, ASC, PAF
- README filter description updated to explain why we don’t trust `legalities.standard`

---

## v1.1 — March 8, 2026

### Changed
- **Data source switched** from pokemontcg.io API to [PokemonTCG/pokemon-tcg-data](https://github.com/PokemonTCG/pokemon-tcg-data) static JSON files
  - No API key needed, no rate limits, no HTTP pagination overhead
  - Reads `sets/en.json` for set metadata and `ptcgoCode` mapping
  - Reads `cards/en/{set_id}.json` for card data per set
- `scripts/fetch_and_categorize_cards.py` fully rewritten for the new data source
- README updated with new data source references
- Same CSV output format, same letter-split logic, same file structure — downstream compatibility preserved

---

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
- Max file size ≤80KB per CSV for reliable GitHub API access
- Cards categorized by supertype (Pokémon, Trainer, Energy) instead of MTG types
- Decklist format uses official PTCGL import syntax

---

**Maintained by**: Celeannora | **AI engine**: Perplexity
