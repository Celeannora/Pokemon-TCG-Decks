# Contributing to Pokémon TCG Decks

Thank you for your interest in contributing! This repository uses an AI-assisted workflow, but human contributions are welcome.

---

## What you can contribute

- **New decks** — Follow the deck structure in `Decks/` and use the PTCGL-importable format
- **Deck improvements** — Update an existing deck's analysis or matchup guide
- **Card database updates** — Run `scripts/fetch_and_categorize_cards.py` after a new set releases
- **Documentation fixes** — Typos, corrections, clarifications
- **Script improvements** — Enhancements to the fetch/categorize script, validate_deck.py, or new utility scripts

---

## Deck submission guidelines

1. Create a folder under `Decks/` named `YYYY-MM-DD_Archetype_Name/`
2. Include all three required files:
   - `decklist.txt` — PTCGL-importable, exactly 60 cards
   - `analysis.md` — card-by-card reasoning, matchup table, weaknesses
   - `matchup_guide.md` — game plan per major matchup
3. Verify every card is Standard-legal (Regulation Mark G or later)
4. Run the validator and confirm it passes:
   ```bash
   python scripts/validate_deck.py Decks/YYYY-MM-DD_Archetype_Name/decklist.txt
   ```
5. Verify the decklist imports cleanly into Pokémon TCG Live

---

## Deck file format

See [README.md](README.md) for the full PTCGL decklist format.

---

## Pull request process

1. Fork the repository
2. Create a branch: `deck/YYYY-MM-DD-archetype-name` or `fix/description`
3. Make your changes
4. Open a pull request — fill out the template
5. A maintainer will review and merge

---

## Code quality (for script contributions)

- Follow PEP 8
- Add docstrings to new functions
- Test locally:
  ```bash
  python scripts/fetch_and_categorize_cards.py
  python scripts/validate_deck.py Decks/<any_deck>/decklist.txt
  ```
- Do not commit the `card_data/` directory after a local test run unless it's a legitimate database update

---

**Maintained by**: Celeannora
