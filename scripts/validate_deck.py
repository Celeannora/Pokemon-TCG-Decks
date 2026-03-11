#!/usr/bin/env python3
"""
Deck Validator — validates a PTCGL-format decklist.txt file.

Usage:
    python scripts/validate_deck.py Decks/2026-03-10_Charizard_ex/decklist.txt

Checks:
  - Exactly 60 cards total
  - No more than 4 copies of any non-Basic-Energy card
  - Section totals match card counts
  - Total Cards: line matches computed total
  - Valid PTCGL line format (<count> <name> <SET> <number>)
  - ACE SPEC violations (>1 total ACE SPEC copy in deck)
"""

import sys
import re
from pathlib import Path
from collections import Counter

BASIC_ENERGY_NAMES = {
    'Grass Energy', 'Fire Energy', 'Water Energy', 'Lightning Energy',
    'Psychic Energy', 'Fighting Energy', 'Darkness Energy', 'Metal Energy',
    # With type symbol variants (PTCGL brace notation)
    '{G} Energy', '{R} Energy', '{W} Energy', '{L} Energy',
    '{P} Energy', '{F} Energy', '{D} Energy', '{M} Energy',
    '{C} Energy',
    'Basic {G} Energy', 'Basic {R} Energy', 'Basic {W} Energy',
    'Basic {L} Energy', 'Basic {P} Energy', 'Basic {F} Energy',
    'Basic {D} Energy', 'Basic {M} Energy',
    'Basic Grass Energy', 'Basic Fire Energy', 'Basic Water Energy',
    'Basic Lightning Energy', 'Basic Psychic Energy',
    'Basic Fighting Energy', 'Basic Darkness Energy', 'Basic Metal Energy',
}

# Known ACE SPEC card names. Expand as new ACE SPECs are released.
ACE_SPEC_NAMES = {
    "Master Ball",
    "Hero's Cape",
    "Neo Upper Energy",
    "Reboot Pod",
    "Sparkling Crystal",
    "Prime Catcher",
    "Unfair Stamp",
    "Survival Brace",
    "Maximum Belt",
    "Deluxe Bomb",
    "Scoop Up Cyclone",
    "Hyper Aroma",
    "Brilliant Blender",
    "Megaton Blower",
    "Tera Staple",
    "Secret Box",
    "Legacy Energy",
    "Gold Potion",
    "Computer Search",
    "Life Dew",
}

# Fallback heuristic: if card name contains these strings it is likely ACE SPEC
ACE_SPEC_KEYWORDS = ['ACE SPEC']


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
        if not line or line.startswith('#'):
            continue

        # Section header: "Pokémon: 15" or "Trainer: 33" or "Energy: 12"
        m = re.match(r'^(Pok[\xe9e]mon|Trainer|Energy):\s*(\d+)$', line, re.IGNORECASE)
        if m:
            key = m.group(1).lower().replace('\xe9', 'e')
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


def validate(path_str: str):
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

    # Total Cards: header cross-check
    if declared_total is not None and declared_total != total:
        msg = f"Total Cards: line declares {declared_total} but counted {total}"
        errors.append(msg)
        print(f"  \u274c {msg}")

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
    ace_spec_total = 0
    ace_spec_found = []
    for name, count in card_counts.items():
        is_ace = (name in ACE_SPEC_NAMES or
                  any(k.lower() in name.lower() for k in ACE_SPEC_KEYWORDS))
        if is_ace:
            ace_spec_total += count
            ace_spec_found.append((name, count))
    if ace_spec_total > 1:
        msg = (f"ACE SPEC violation: {ace_spec_total} total ACE SPEC copies "
               f"({', '.join(f'{c}x {n}' for n, c in ace_spec_found)})")
        errors.append(msg)
        print(f"  \u274c {msg}")
    else:
        label = f" ({ace_spec_found[0][0]})" if ace_spec_found else " (none)"
        print(f"  \u2705 ACE SPEC limit respected{label}")

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
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_deck.py <path/to/decklist.txt>")
        sys.exit(1)
    validate(sys.argv[1])
