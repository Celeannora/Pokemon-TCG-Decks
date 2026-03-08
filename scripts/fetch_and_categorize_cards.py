#!/usr/bin/env python3
"""
Pokémon TCG Standard Card Data Fetcher - Letter-Split Version
Fetches Standard-legal cards from the pokemontcg.io API v2.
Splits card database by supertype (folder) then first letter of card name.
Target: each file ~80KB max for reliable GitHub API access by AI tools.

File naming convention: {supertype}/{supertype}_{letter}.csv
  e.g. card_data/pokemon/pokemon_c.csv
  If a single letter is still too large: pokemon_s1.csv, pokemon_s2.csv

Requirements:
  pip install requests

Optional: Set POKEMONTCG_API_KEY environment variable for higher rate limits.
  Get a free API key at: https://dev.pokemontcg.io/
"""

import requests
import csv
import os
import io
import json
import time
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from collections import defaultdict


class PokemonCardFetcher:
    """Fetch and categorize Standard-legal Pokémon TCG cards into letter-split CSV files"""

    MAX_FILE_SIZE_BYTES = 80 * 1024  # 80KB target max file size
    API_BASE = "https://api.pokemontcg.io/v2"
    PAGE_SIZE = 250

    CSV_COLUMNS = [
        'name', 'supertype', 'subtypes', 'hp', 'types', 'evolves_from',
        'abilities', 'attacks', 'weaknesses', 'resistances', 'retreat_cost',
        'set_code', 'set_name', 'number', 'rarity', 'regulation_mark', 'rules'
    ]

    def __init__(self, output_dir: str = "card_data"):
        self.output_dir = output_dir
        self.api_key = os.environ.get('POKEMONTCG_API_KEY', '')
        self.session = requests.Session()
        if self.api_key:
            self.session.headers['X-Api-Key'] = self.api_key
            print(f"Using API key for higher rate limits")
        else:
            print("No API key found. Set POKEMONTCG_API_KEY for higher rate limits.")
            print("Get a free key at: https://dev.pokemontcg.io/")

    def fetch_standard_cards(self) -> List[Dict]:
        """Fetch all Standard-legal cards from the API with pagination"""
        print("Fetching Standard-legal cards from pokemontcg.io...")
        all_cards = []
        page = 1

        while True:
            params = {
                'q': 'legalities.standard:legal',
                'pageSize': self.PAGE_SIZE,
                'page': page,
                'orderBy': 'name',
            }

            try:
                response = self.session.get(f"{self.API_BASE}/cards", params=params)
                response.raise_for_status()
                data = response.json()
            except requests.exceptions.RequestException as e:
                print(f"  Error on page {page}: {e}")
                if page == 1:
                    return []
                break

            cards = data.get('data', [])
            if not cards:
                break

            all_cards.extend(cards)
            total = data.get('totalCount', '?')
            print(f"  Page {page}: {len(cards)} cards (total so far: {len(all_cards)}/{total})")

            # Check if we've fetched all pages
            if len(all_cards) >= data.get('totalCount', float('inf')):
                break

            page += 1
            # Rate limiting: be polite to the API
            if not self.api_key:
                time.sleep(1.0)  # 1 second between requests without API key
            else:
                time.sleep(0.1)

        print(f"Fetched {len(all_cards)} Standard-legal cards total")
        return all_cards

    def format_abilities(self, abilities: Optional[List[Dict]]) -> str:
        """Format abilities list into readable text"""
        if not abilities:
            return ''
        parts = []
        for a in abilities:
            ability_type = a.get('type', 'Ability')
            name = a.get('name', '')
            text = a.get('text', '')
            parts.append(f"[{ability_type}] {name}: {text}")
        return ' | '.join(parts)

    def format_attacks(self, attacks: Optional[List[Dict]]) -> str:
        """Format attacks list into readable text with full card text"""
        if not attacks:
            return ''
        parts = []
        for a in attacks:
            cost = ','.join(a.get('cost', []))
            name = a.get('name', '')
            damage = a.get('damage', '')
            text = a.get('text', '')
            attack_str = f"[{cost}] {name}"
            if damage:
                attack_str += f" {damage}"
            if text:
                attack_str += f" — {text}"
            parts.append(attack_str)
        return ' | '.join(parts)

    def format_weaknesses(self, weaknesses: Optional[List[Dict]]) -> str:
        if not weaknesses:
            return ''
        return ', '.join(f"{w.get('type', '')} {w.get('value', '')}" for w in weaknesses)

    def format_resistances(self, resistances: Optional[List[Dict]]) -> str:
        if not resistances:
            return ''
        return ', '.join(f"{r.get('type', '')} {r.get('value', '')}" for r in resistances)

    def extract_card_data(self, card: Dict) -> Dict:
        """Extract relevant data from a single API card object"""
        set_info = card.get('set', {})

        return {
            'name': card.get('name', ''),
            'supertype': card.get('supertype', ''),
            'subtypes': ','.join(card.get('subtypes', [])),
            'hp': card.get('hp', ''),
            'types': ','.join(card.get('types', [])),
            'evolves_from': card.get('evolvesFrom', ''),
            'abilities': self.format_abilities(card.get('abilities')),
            'attacks': self.format_attacks(card.get('attacks')),
            'weaknesses': self.format_weaknesses(card.get('weaknesses')),
            'resistances': self.format_resistances(card.get('resistances')),
            'retreat_cost': len(card.get('retreatCost', [])),
            'set_code': set_info.get('ptcgoCode', set_info.get('id', '')),
            'set_name': set_info.get('name', ''),
            'number': card.get('number', ''),
            'rarity': card.get('rarity', ''),
            'regulation_mark': card.get('regulationMark', ''),
            'rules': ' | '.join(card.get('rules', [])),
        }

    def categorize_cards(self, raw_cards: List[Dict]) -> Dict[str, List[Dict]]:
        """Process raw API cards and categorize by supertype"""
        print("Processing and categorizing cards...")
        categorized = defaultdict(list)

        for card in raw_cards:
            processed = self.extract_card_data(card)
            # Use lowercase supertype as folder name
            supertype = processed['supertype'].lower()
            if supertype == 'pokémon':
                supertype = 'pokemon'  # Filesystem-friendly name
            categorized[supertype].append(processed)

        # Sort each category by name
        for cat in categorized:
            categorized[cat].sort(key=lambda x: x['name'].lower())

        # Deduplicate: keep only one entry per unique (name, set_code, number)
        for cat in categorized:
            seen = set()
            unique = []
            for card in categorized[cat]:
                key = (card['name'], card['set_code'], card['number'])
                if key not in seen:
                    seen.add(key)
                    unique.append(card)
            categorized[cat] = unique

        total = sum(len(v) for v in categorized.values())
        print(f"Processed {total} unique cards into {len(categorized)} supertypes")
        for cat in sorted(categorized.keys()):
            print(f"  {cat}: {len(categorized[cat])} cards")
        return categorized

    def estimate_csv_size(self, cards: List[Dict]) -> int:
        """Estimate CSV file size for a given set of cards"""
        if not cards:
            return 0
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=self.CSV_COLUMNS)
        writer.writeheader()
        sample = cards[:min(20, len(cards))]
        writer.writerows(sample)
        sample_size = len(buf.getvalue().encode('utf-8'))
        avg = sample_size / len(sample)
        header = len(','.join(self.CSV_COLUMNS).encode('utf-8')) + 1
        return int(avg * len(cards) + header)

    def split_by_letter(self, cards: List[Dict], type_name: str) -> List[Tuple[str, List[Dict]]]:
        """
        Split cards by first letter of name.
        If a single letter's file exceeds MAX_FILE_SIZE_BYTES, chunk with numeric suffixes.
        Non-alpha names go into {type}_0.csv.
        """
        letter_groups: Dict[str, List[Dict]] = defaultdict(list)
        for card in cards:
            first = card['name'][0].upper() if card['name'] else '0'
            key = first if first.isalpha() else '0'
            letter_groups[key].append(card)

        parts = []
        for letter in sorted(letter_groups.keys()):
            group = letter_groups[letter]
            estimated = self.estimate_csv_size(group)

            if estimated <= self.MAX_FILE_SIZE_BYTES:
                parts.append((f"{type_name}_{letter.lower()}", group))
            else:
                num_chunks = (estimated // self.MAX_FILE_SIZE_BYTES) + 1
                per_chunk = len(group) // num_chunks + 1
                for i in range(num_chunks):
                    chunk = group[i * per_chunk:(i + 1) * per_chunk]
                    if chunk:
                        parts.append((f"{type_name}_{letter.lower()}{i + 1}", chunk))

        return parts

    def write_csv_file(self, subdir: str, filename: str, cards: List[Dict]) -> float:
        """Write a CSV file and return its size in KB"""
        dirpath = os.path.join(self.output_dir, subdir)
        os.makedirs(dirpath, exist_ok=True)
        filepath = os.path.join(dirpath, f"{filename}.csv")

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.CSV_COLUMNS)
            writer.writeheader()
            writer.writerows(cards)

        return os.path.getsize(filepath) / 1024

    def export_all(self, categorized: Dict[str, List[Dict]]):
        """Export all categorized cards to letter-split CSV files"""
        print("\nExporting letter-split CSV files...")
        all_stats = []

        for type_name, cards in sorted(categorized.items()):
            if not cards:
                continue

            parts = self.split_by_letter(cards, type_name)
            print(f"\n  [{type_name}] {len(cards)} cards -> {len(parts)} files")

            for filename, part_cards in parts:
                size_kb = self.write_csv_file(type_name, filename, part_cards)
                print(f"    {type_name}/{filename}.csv  ({len(part_cards)} cards, {size_kb:.1f} KB)")
                all_stats.append({
                    'type': type_name,
                    'filename': filename,
                    'cards': len(part_cards),
                    'size_kb': size_kb,
                })

        self.export_index(all_stats)
        return all_stats

    def export_index(self, stats: List[Dict]):
        """Write _INDEX.md at root of output_dir"""
        index_file = os.path.join(self.output_dir, "_INDEX.md")
        by_type = defaultdict(list)
        for s in stats:
            by_type[s['type']].append(s)

        with open(index_file, 'w', encoding='utf-8') as f:
            f.write("# Card data index\n\n")
            f.write(f"Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n\n")
            f.write("## How to find a card\n\n")
            f.write("**Pattern**: `card_data/{supertype}/{supertype}_{first_letter}.csv`\n\n")
            f.write("**Example**: Charizard ex (Pokémon, C) -> `card_data/pokemon/pokemon_c.csv`\n\n")
            f.write("**Example**: Professor's Research (Trainer, P) -> `card_data/trainer/trainer_p.csv`\n\n")
            f.write("**Example**: Basic {R} Energy (Energy, B) -> `card_data/energy/energy_b.csv`\n\n")
            f.write("---\n\n")
            f.write("## Files by supertype\n\n")

            for type_name in sorted(by_type.keys()):
                type_stats = by_type[type_name]
                total_cards = sum(s['cards'] for s in type_stats)
                f.write(f"### {type_name.capitalize()} ({total_cards} cards)\n\n")
                f.write("| File | Cards | Size |\n")
                f.write("|------|-------|------|\n")
                for s in type_stats:
                    f.write(f"| `{s['type']}/{s['filename']}.csv` | {s['cards']} | {s['size_kb']:.1f} KB |\n")
                f.write("\n")

            f.write("## CSV columns\n\n")
            f.write("`name`, `supertype`, `subtypes`, `hp`, `types`, `evolves_from`, "
                    "`abilities`, `attacks`, `weaknesses`, `resistances`, `retreat_cost`, "
                    "`set_code`, `set_name`, `number`, `rarity`, `regulation_mark`, `rules`\n\n")
            f.write("## Column descriptions\n\n")
            f.write("| Column | Description |\n")
            f.write("|--------|-------------|\n")
            f.write("| `name` | Card name as printed |\n")
            f.write("| `supertype` | Pokémon, Trainer, or Energy |\n")
            f.write("| `subtypes` | Comma-separated: Basic, Stage 1, Stage 2, ex, V, Item, Supporter, etc. |\n")
            f.write("| `hp` | Hit points (Pokémon only) |\n")
            f.write("| `types` | Energy types: Fire, Water, Grass, Lightning, Psychic, Fighting, etc. |\n")
            f.write("| `evolves_from` | Name of the Pokémon this card evolves from |\n")
            f.write("| `abilities` | Formatted as: [Type] Name: Text |\n")
            f.write("| `attacks` | Formatted as: [Cost] Name Damage — Effect text |\n")
            f.write("| `weaknesses` | Type and value, e.g. Fire ×2 |\n")
            f.write("| `resistances` | Type and value, e.g. Grass -30 |\n")
            f.write("| `retreat_cost` | Number of energy required to retreat |\n")
            f.write("| `set_code` | PTCGL set code (e.g. SVI, OBF, PAL) |\n")
            f.write("| `set_name` | Full set name |\n")
            f.write("| `number` | Collector number within set |\n")
            f.write("| `rarity` | Card rarity |\n")
            f.write("| `regulation_mark` | Letter mark for format legality (H+) |\n")
            f.write("| `rules` | Special rules text (ex rules, VSTAR Power, etc.) |\n")

        print(f"\nIndex written: {index_file}")

    def run(self):
        print("=" * 70)
        print("Pokémon TCG Standard Card Data Fetcher - Letter-Split Mode")
        print(f"Output directory: {self.output_dir}/")
        print(f"API: {self.API_BASE}")
        print("=" * 70)

        all_cards = self.fetch_standard_cards()
        if not all_cards:
            print("ERROR: No cards fetched. Check your internet connection or API key.")
            return

        categorized = self.categorize_cards(all_cards)
        stats = self.export_all(categorized)

        total_files = len(stats)
        total_cards = sum(s['cards'] for s in stats)
        max_size = max(s['size_kb'] for s in stats) if stats else 0

        print("\n" + "=" * 70)
        print("Done!")
        print(f"  Files created : {total_files}")
        print(f"  Total cards   : {total_cards}")
        print(f"  Largest file  : {max_size:.1f} KB")
        print(f"  Output dir    : {self.output_dir}/")
        print("=" * 70)


if __name__ == "__main__":
    fetcher = PokemonCardFetcher()
    fetcher.run()
