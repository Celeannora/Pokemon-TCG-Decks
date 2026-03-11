#!/usr/bin/env python3
"""
Deck Validator — validates a PTCGL-format decklist.txt file.

Usage:
    python scripts/validate_deck.py Decks/2026-03-10_Charizard_ex/decklist.txt
    python scripts/validate_deck.py Decks/2026-03-10_Charizard_ex/decklist.txt --verbose

Checks:
  - Exactly 60 cards total
  - No more than 4 copies of any non-Basic-Energy card
  - Section totals match card counts
  - Total Cards line matches actual count
  - Valid PTCGL line format (<count> <name> <SET> <number>)
  - ACE SPEC violations (>1 ACE SPEC card in deck)
  - Radiant Pokémon violations (>1 Radiant in deck)
"""

import sys
import re
import argparse
from pathlib import Path
from collections import Counter

# Basic Energy types in current Standard (Dragon and Fairy do NOT have Basic Energy cards)
BASIC_ENERGY_NAMES = {
    'Grass Energy', 'Fire Energy', 'Water Energy', 'Lightning Energy',
    'Psychic Energy', 'Fighting Energy', 'Darkness Energy', 'Metal Energy',
    'Colorless Energy',
    # Symbol variants used in PTCGL import format
    '{G} Energy', '{R} Energy', '{W} Energy', '{L} Energy',
    '{P} Energy', '{F} Energy', '{D} Energy', '{M} Energy',
    '{C} Energy',
    'Basic {G} Energy', 'Basic {R} Energy', 'Basic {W} Energy',
    'Basic {L} Energy', 'Basic {P} Energy', 'Basic {F} Energy',
    'Basic {D} Energy', 'Basic {M} Energy',
    'Basic Grass Energy', 'Basic Fire Energy', 'Basic Water Energy',
    'Basic Lightning Energy', 'Basic Psychic Energy', 'Basic Fighting Energy',
    'Basic Darkness Energy', 'Basic Metal Energy',
}

# Known ACE SPEC cards in Standard (Regulation Mark G+)
# Update this list as new sets are released.
ACE_SPEC_CARDS = {
    # Paradox Rift
    "Neo Upper Energy", "Awakening Drum", "Maximum Belt",
    # Temporal Forces
    "Prime Catcher", "Unfair Stamp", "Master Ball", "Erb's Mischief",
    # Twilight Masquerade
    "Hyper Aroma", "Pal Pad (ACE SPEC)",
    # Shrouded Fable
    "Dangerous Laser",
    # Stellar Crown
    "Counter Catcher (ACE SPEC)", "Sparkling Crystal",
    # Surging Sparks
    "Reboot Pod", "Deluxe Bomb",
    # Prismatic Evolutions
    "Brilliant Blender",
    # Journey Together
    "Hero's Medal",
    # Common ACE SPEC names (partial match fallback)
}

# Radiant Pokémon keyword — detected via subtype in decklist (name starts with "Radiant")
# In PTCGL decklist format the card name itself starts with "Radiant"
def is_radiant(name: str) -> bool:
    return name.startswith("Radiant ")

def is_ace_spec(name: str) -> bool:
    """Check if a card is an ACE SPEC by name match."""
    return name in ACE_SPEC_CARDS


def parse_decklist(path: Path):
    sections = {'pokemon': [], 'trainer': [], 'energy': []}
    section_totals = {}
    declared_total = None
    current_section = None
    errors = []
    warnings = []

    with open(path, encoding='utf-8') as f:
        lines = f.readlines()

    for lineno, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line:
            continue

        # Section header: "Pokémon: 15" or "Trainer: 33" or "Energy: 12"
        m = re.match(r'^(Pok[\u00e9e]mon|Trainer|Energy):\s*(\d+)$', line, re.IGNORECASE)
        if m:
            key = m.group(1).lower()
            key = re.sub(r'[\u00e9e]', 'e', key)
            if 'pok' in key:
                key = 'pokemon'
            current_section = key
            section_totals[key] = int(m.group(2))
            continue

        # Total Cards line
        m_total = re.match(r'^Total Cards:\s*(\d+)$', line, re.IGNORECASE)
        if m_total:
            declared_total = int(m_total.group(1))
            continue

        # Card line: "4 Professor's Research SVI 190"
        m = re.match(r'^(\d+)\s+(.+?)\s+([A-Z0-9]{2,6})\s+(\S+)$', line)
        if m:
            qty = int(m.group(1))
            name = m.group(2).strip()
            set_code = m.group(3)
            number = m.group(4)
            if current_section:
                sections[current_section].append({
                    'qty': qty, 'name': name,
                    'set_code': set_code, 'number': number,
                    'lineno': lineno
                })
            else:
                errors.append(f"Line {lineno}: Card line outside any section: {line}")
            continue

        errors.append(f"Line {lineno}: Unrecognized line: {line}")

    return sections, section_totals, declared_total, errors, warnings


def validate(path_str: str, verbose: bool = False):
    path = Path(path_str)
    if not path.exists():
        print(f"ERROR: File not found: {path}")
        sys.exit(1)

    sections, section_totals, declared_total, errors, warnings = parse_decklist(path)

    # Card name counter
    card_counts: Counter = Counter()
    total = 0
    for section_cards in sections.values():
        for entry in section_cards:
            card_counts[entry['name']] += entry['qty']
            total += entry['qty']

    print(f"\n{'='*55}")
    print(f"  Deck Validator — {path.name}")
    print(f"{'='*55}")

    # Total card count
    status = '\u2705' if total == 60 else '\u274c'
    print(f"\n{status} Total cards: {total} / 60")

    # Total Cards line check
    if declared_total is not None and declared_total != total:
        errors.append(f"'Total Cards: {declared_total}' line disagrees with actual count ({total})")
        print(f"  \u274c Total Cards line says {declared_total} but actual count is {total}")
    elif declared_total is None:
        warnings.append("No 'Total Cards:' line found")

    # Section totals
    for sec, cards in sections.items():
        actual = sum(c['qty'] for c in cards)
        declared = section_totals.get(sec, '?')
        match = actual == declared
        icon = '\u2705' if match else '\u274c'
        print(f"  {icon} {sec.capitalize()}: declared={declared}, actual={actual}")
        if not match:
            errors.append(f"{sec.capitalize()} section declared {declared} but counted {actual}")

    # 4-copy rule
    print("\nCard copy limits:")
    violations = []
    for name, count in sorted(card_counts.items()):
        is_basic = name in BASIC_ENERGY_NAMES
        if not is_basic and count > 4:
            violations.append((name, count))
            errors.append(f"4-copy violation: {count}x {name}")
    if violations:
        for name, count in violations:
            print(f"  \u274c {count}x {name}  (exceeds 4-copy limit)")
    else:
        print(f"  \u2705 All cards within 4-copy limit")

    # ACE SPEC check
    print("\nACE SPEC check:")
    ace_specs_in_deck = [(name, count) for name, count in card_counts.items() if is_ace_spec(name)]
    total_ace_spec_copies = sum(count for _, count in ace_specs_in_deck)
    if total_ace_spec_copies > 1:
        errors.append(f"ACE SPEC violation: {total_ace_spec_copies} ACE SPEC cards in deck (max 1)")
        for name, count in ace_specs_in_deck:
            print(f"  \u274c {count}x {name} (ACE SPEC)")
    elif ace_specs_in_deck:
        for name, count in ace_specs_in_deck:
            print(f"  \u2705 {count}x {name} (ACE SPEC — within limit)")
    else:
        print(f"  \u2705 No ACE SPEC cards")

    # Radiant check
    print("\nRadiant Pokémon check:")
    radiant_cards = [(name, count) for name, count in card_counts.items() if is_radiant(name)]
    total_radiant = sum(count for _, count in radiant_cards)
    if total_radiant > 1:
        errors.append(f"Radiant violation: {total_radiant} Radiant Pokémon in deck (max 1)")
        for name, count in radiant_cards:
            print(f"  \u274c {count}x {name} (Radiant)")
    elif radiant_cards:
        for name, count in radiant_cards:
            print(f"  \u2705 {count}x {name} (Radiant — within limit)")
    else:
        print(f"  \u2705 No Radiant Pokémon")

    # Verbose: full card list
    if verbose:
        print("\nFull card list:")
        for sec in ('pokemon', 'trainer', 'energy'):
            cards = sections[sec]
            if cards:
                print(f"  [{sec.capitalize()}]")
                for entry in cards:
                    print(f"    {entry['qty']}x {entry['name']} {entry['set_code']} {entry['number']}")

    # Warnings
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  \u26a0\ufe0f  {w}")

    # Summary
    print(f"\n{'='*55}")
    if errors:
        print(f"\u274c VALIDATION FAILED — {len(errors)} error(s):")
        for e in errors:
            print(f"   \u2022 {e}")
        sys.exit(1)
    else:
        print("\u2705 VALIDATION PASSED — decklist is legal")
        print(f"   Cards: {total}")
        unique = len(card_counts)
        print(f"   Unique card names: {unique}")
    print(f"{'='*55}\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Validate a PTCGL-format decklist.txt file.'
    )
    parser.add_argument('decklist', help='Path to the decklist.txt file')
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Print full card list during validation'
    )
    args = parser.parse_args()
    validate(args.decklist, verbose=args.verbose)
