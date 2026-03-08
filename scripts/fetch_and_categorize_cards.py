#!/usr/bin/env python3
"""
Pokémon TCG Standard Card Data Fetcher — GitHub Static Data Source
Reads card data from PokemonTCG/pokemon-tcg-data (static JSON files on GitHub).
No API key needed. No rate limits. Faster and more reliable.

Data source: https://github.com/PokemonTCG/pokemon-tcg-data/tree/master/cards/en
Set metadata: https://github.com/PokemonTCG/pokemon-tcg-data/blob/master/sets/en.json

IMPORTANT: The legalities.standard field in the upstream JSON data is NOT reliably
updated after format rotations. This script filters by REGULATION MARK instead,
which is the authoritative indicator of Standard legality.

Current Standard format: Regulation Mark G and later (G, H, I, J, …)
Basic Energy cards (from SVE) have no regulation mark and are always legal.

Splits card database by supertype (folder) then first letter of card name.
Target: each file ~80KB max for reliable GitHub API access by AI tools.

File naming: card_data/{supertype}/{supertype}_{letter}.csv

Requirements:
  pip install requests
"""

import requests
import csv
import os
import io
import json
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from collections import defaultdict

# ── Config ───────────────────────────────────────────────────────────────────
RAW_BASE = "https://raw.githubusercontent.com/PokemonTCG/pokemon-tcg-data/master"
SETS_URL = f"{RAW_BASE}/sets/en.json"
CARDS_DIR = "cards/en"

MAX_FILE_SIZE_BYTES = 80 * 1024  # 80 KB target max per CSV
OUTPUT_DIR = "card_data"

# Standard-legal regulation marks (G and later).
# Update this set when a new rotation occurs.
LEGAL_REG_MARKS = {'G', 'H', 'I', 'J'}

# Sets that contain cards which are ALWAYS Standard-legal regardless of
# regulation mark (e.g. Basic Energy from SVE have no mark).
ALWAYS_LEGAL_SETS = {'sve'}

# Only fetch sets from these series (contains all G+ cards).
# This avoids downloading 100+ old set files that can't have legal cards.
CANDIDATE_SERIES = {'Scarlet & Violet', 'Mega Evolution'}

CSV_COLUMNS = [
    'name', 'supertype', 'subtypes', 'hp', 'types', 'evolves_from',
    'abilities', 'attacks', 'weaknesses', 'resistances', 'retreat_cost',
    'set_code', 'set_name', 'number', 'rarity', 'regulation_mark', 'rules'
]


# ── Helpers ──────────────────────────────────────────────────────────────────

def fetch_json(url: str) -> any:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.json()


def format_abilities(abilities: Optional[List[Dict]]) -> str:
    if not abilities:
        return ''
    parts = []
    for a in abilities:
        atype = a.get('type', 'Ability')
        name = a.get('name', '')
        text = a.get('text', '')
        parts.append(f"[{atype}] {name}: {text}")
    return ' | '.join(parts)


def format_attacks(attacks: Optional[List[Dict]]) -> str:
    if not attacks:
        return ''
    parts = []
    for a in attacks:
        cost = ','.join(a.get('cost', []))
        name = a.get('name', '')
        damage = a.get('damage', '')
        text = a.get('text', '')
        s = f"[{cost}] {name}"
        if damage:
            s += f" {damage}"
        if text:
            s += f" — {text}"
        parts.append(s)
    return ' | '.join(parts)


def format_weaknesses(weaknesses: Optional[List[Dict]]) -> str:
    if not weaknesses:
        return ''
    return ', '.join(f"{w.get('type','')} {w.get('value','')}" for w in weaknesses)


def format_resistances(resistances: Optional[List[Dict]]) -> str:
    if not resistances:
        return ''
    return ', '.join(f"{r.get('type','')} {r.get('value','')}" for r in resistances)


def extract_card(card: Dict, set_name: str, ptcgo_code: str) -> Dict:
    return {
        'name':            card.get('name', ''),
        'supertype':       card.get('supertype', ''),
        'subtypes':        ','.join(card.get('subtypes', [])),
        'hp':              card.get('hp', ''),
        'types':           ','.join(card.get('types', [])),
        'evolves_from':    card.get('evolvesFrom', ''),
        'abilities':       format_abilities(card.get('abilities')),
        'attacks':         format_attacks(card.get('attacks')),
        'weaknesses':      format_weaknesses(card.get('weaknesses')),
        'resistances':     format_resistances(card.get('resistances')),
        'retreat_cost':    len(card.get('retreatCost', [])),
        'set_code':        ptcgo_code,
        'set_name':        set_name,
        'number':          card.get('number', ''),
        'rarity':          card.get('rarity', ''),
        'regulation_mark': card.get('regulationMark', ''),
        'rules':           ' | '.join(card.get('rules', [])),
    }


def is_standard_legal(card: Dict, set_id: str) -> bool:
    """Determine if a card is Standard-legal based on regulation mark."""
    # Basic Energy from SVE — always legal, no regulation mark
    if set_id in ALWAYS_LEGAL_SETS:
        return True
    reg_mark = card.get('regulationMark', '')
    return reg_mark in LEGAL_REG_MARKS


# ── CSV writing ──────────────────────────────────────────────────────────────

def estimate_csv_size(cards: List[Dict]) -> int:
    if not cards:
        return 0
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=CSV_COLUMNS)
    w.writeheader()
    sample = cards[:min(20, len(cards))]
    w.writerows(sample)
    avg = len(buf.getvalue().encode('utf-8')) / len(sample)
    header = len(','.join(CSV_COLUMNS).encode('utf-8')) + 1
    return int(avg * len(cards) + header)


def split_by_letter(cards: List[Dict], type_name: str) -> List[Tuple[str, List[Dict]]]:
    groups: Dict[str, List[Dict]] = defaultdict(list)
    for c in cards:
        first = c['name'][0].upper() if c['name'] else '0'
        key = first if first.isalpha() else '0'
        groups[key].append(c)

    parts = []
    for letter in sorted(groups.keys()):
        group = groups[letter]
        est = estimate_csv_size(group)
        if est <= MAX_FILE_SIZE_BYTES:
            parts.append((f"{type_name}_{letter.lower()}", group))
        else:
            n = (est // MAX_FILE_SIZE_BYTES) + 1
            per = len(group) // n + 1
            for i in range(n):
                chunk = group[i * per:(i + 1) * per]
                if chunk:
                    parts.append((f"{type_name}_{letter.lower()}{i + 1}", chunk))
    return parts


def write_csv(subdir: str, filename: str, cards: List[Dict]) -> float:
    dirpath = os.path.join(OUTPUT_DIR, subdir)
    os.makedirs(dirpath, exist_ok=True)
    fp = os.path.join(dirpath, f"{filename}.csv")
    with open(fp, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        w.writeheader()
        w.writerows(cards)
    return os.path.getsize(fp) / 1024


def write_index(stats: List[Dict]):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    idx = os.path.join(OUTPUT_DIR, "_INDEX.md")
    by_type = defaultdict(list)
    for s in stats:
        by_type[s['type']].append(s)

    with open(idx, 'w', encoding='utf-8') as f:
        f.write("# Card data index\n\n")
        f.write(f"Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n\n")
        f.write("Data source: [PokemonTCG/pokemon-tcg-data](https://github.com/PokemonTCG/pokemon-tcg-data)\n\n")
        f.write(f"Standard format: Regulation Mark {', '.join(sorted(LEGAL_REG_MARKS))} (and Basic Energy)\n\n")
        f.write("## How to find a card\n\n")
        f.write("**Pattern**: `card_data/{supertype}/{supertype}_{first_letter}.csv`\n\n")
        f.write("**Example**: Charizard ex → `card_data/pokemon/pokemon_c.csv`\n\n")
        f.write("**Example**: Professor's Research → `card_data/trainer/trainer_p.csv`\n\n")
        f.write("**Example**: Basic Grass Energy → `card_data/energy/energy_b.csv`\n\n")
        f.write("---\n\n## Files by supertype\n\n")
        for tn in sorted(by_type.keys()):
            ts = by_type[tn]
            tot = sum(s['cards'] for s in ts)
            f.write(f"### {tn.capitalize()} ({tot} cards)\n\n")
            f.write("| File | Cards | Size |\n|------|-------|------|\n")
            for s in ts:
                f.write(f"| `{s['type']}/{s['filename']}.csv` | {s['cards']} | {s['size_kb']:.1f} KB |\n")
            f.write("\n")
        f.write("## CSV columns\n\n")
        f.write("`" + "`, `".join(CSV_COLUMNS) + "`\n\n")
        f.write("## Column descriptions\n\n")
        f.write("| Column | Description |\n|--------|-------------|\n")
        for col, desc in [
            ('name', 'Card name as printed'),
            ('supertype', 'Pokémon, Trainer, or Energy'),
            ('subtypes', 'Comma-separated: Basic, Stage 1, Stage 2, ex, V, Item, Supporter, etc.'),
            ('hp', 'Hit points (Pokémon only)'),
            ('types', 'Energy types: Fire, Water, Grass, Lightning, Psychic, Fighting, etc.'),
            ('evolves_from', 'Name of the Pokémon this card evolves from'),
            ('abilities', 'Formatted as: [Type] Name: Text'),
            ('attacks', 'Formatted as: [Cost] Name Damage — Effect text'),
            ('weaknesses', 'Type and value, e.g. Fire ×2'),
            ('resistances', 'Type and value, e.g. Grass -30'),
            ('retreat_cost', 'Number of energy required to retreat'),
            ('set_code', 'PTCGL set code (e.g. SVI, OBF, PAL)'),
            ('set_name', 'Full set name'),
            ('number', 'Collector number within set'),
            ('rarity', 'Card rarity'),
            ('regulation_mark', 'Letter mark for format legality'),
            ('rules', 'Special rules text (ex rules, VSTAR Power, etc.)'),
        ]:
            f.write(f"| `{col}` | {desc} |\n")
    print(f"Index written: {idx}")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("Pokémon TCG Card Fetcher — Static GitHub Data Source")
    print(f"Source : PokemonTCG/pokemon-tcg-data")
    print(f"Filter : Regulation Mark {', '.join(sorted(LEGAL_REG_MARKS))} + Basic Energy")
    print(f"Output : {OUTPUT_DIR}/")
    print("=" * 70)

    # 1. Fetch set metadata
    print("\nFetching set metadata...")
    sets_data = fetch_json(SETS_URL)
    set_map = {}
    for s in sets_data:
        set_map[s['id']] = {
            'name': s['name'],
            'series': s.get('series', ''),
            'ptcgo_code': s.get('ptcgoCode', s['id'].upper()),
        }
    print(f"  Found {len(sets_data)} total sets")

    # 2. Identify candidate sets (SV-era, ME-era, and always-legal sets)
    candidate_sets = {}
    for sid, info in set_map.items():
        if info['series'] in CANDIDATE_SERIES or sid in ALWAYS_LEGAL_SETS:
            candidate_sets[sid] = info
    print(f"  {len(candidate_sets)} candidate sets to scan (Scarlet & Violet + Mega Evolution + Energy)")

    # 3. Fetch and filter cards
    all_cards: List[Dict] = []
    for sid in sorted(candidate_sets.keys()):
        url = f"{RAW_BASE}/{CARDS_DIR}/{sid}.json"
        try:
            cards_raw = fetch_json(url)
        except Exception as e:
            print(f"  ⚠ Skipping {sid}: {e}")
            continue
        info = candidate_sets[sid]
        count = 0
        for card in cards_raw:
            if not is_standard_legal(card, sid):
                continue
            processed = extract_card(card, info['name'], info['ptcgo_code'])
            all_cards.append(processed)
            count += 1
        total_in_set = len(cards_raw)
        skipped = total_in_set - count
        print(f"  {sid:<14s} ({info['ptcgo_code']:<6s}) → {count:>4d} legal, {skipped:>4d} skipped  [{info['name']}]")

    print(f"\nTotal Standard-legal cards: {len(all_cards)}")

    # 4. Categorize by supertype
    categorized: Dict[str, List[Dict]] = defaultdict(list)
    for card in all_cards:
        st = card['supertype'].lower()
        if st == 'pokémon':
            st = 'pokemon'
        categorized[st].append(card)

    for cat in categorized:
        categorized[cat].sort(key=lambda x: x['name'].lower())
        seen = set()
        unique = []
        for c in categorized[cat]:
            key = (c['name'], c['set_code'], c['number'])
            if key not in seen:
                seen.add(key)
                unique.append(c)
        categorized[cat] = unique

    for cat in sorted(categorized.keys()):
        print(f"  {cat}: {len(categorized[cat])} unique cards")

    # 5. Export
    print("\nExporting letter-split CSV files...")
    all_stats = []
    for type_name, cards in sorted(categorized.items()):
        if not cards:
            continue
        parts = split_by_letter(cards, type_name)
        print(f"\n  [{type_name}] {len(cards)} cards → {len(parts)} files")
        for filename, part_cards in parts:
            size_kb = write_csv(type_name, filename, part_cards)
            print(f"    {type_name}/{filename}.csv  ({len(part_cards)} cards, {size_kb:.1f} KB)")
            all_stats.append({
                'type': type_name,
                'filename': filename,
                'cards': len(part_cards),
                'size_kb': size_kb,
            })

    write_index(all_stats)

    total_files = len(all_stats)
    total_cards = sum(s['cards'] for s in all_stats)
    max_size = max(s['size_kb'] for s in all_stats) if all_stats else 0
    print("\n" + "=" * 70)
    print("Done!")
    print(f"  Files created : {total_files}")
    print(f"  Total cards   : {total_cards}")
    print(f"  Largest file  : {max_size:.1f} KB")
    print(f"  Output dir    : {OUTPUT_DIR}/")
    print(f"  Reg marks     : {', '.join(sorted(LEGAL_REG_MARKS))}")
    print("=" * 70)


if __name__ == "__main__":
    main()
