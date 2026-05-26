#!/usr/bin/env python3
import csv
import re
from pathlib import Path

ROOT = Path('.')
INPUT_PATH = ROOT / '00-input' / 'anki-full-keys.csv'
OUTPUT_PATH = ROOT / '10-output' / 'anki-priority-orders.csv'
DATA_ROOT = ROOT / '20-data'

FREQ_LIST_DIR = DATA_ROOT / '10-frequency_list'
RIRIKKU_SELECTED = DATA_ROOT / '00-japanese-word-ranks' / 'frequency' / 'selected-freq' / 'RIRIKKU_CONSOLIDATED.csv'
RIRIKKU_ALL = DATA_ROOT / '00-japanese-word-ranks' / 'frequency' / 'top25k-all-freq' / 'consolidated.csv'
KANJI_FREQ = DATA_ROOT / '40-kanji' / 'jiten_kanji_freq.csv'

NEW_COLUMNS = [
    'priority_general',
    'priority_oral',
    'priority_professional',
    'priority_fiction',
    'priority_kanji',
]

KANJI_RE = re.compile(r'[一-龯々〆ヶ]')
BRACKET_RE = re.compile(r'\[.*?\]')


def normalize_surface(value: str) -> str:
    if not value:
        return ''
    value = value.strip()
    value = BRACKET_RE.sub('', value)
    return value.strip()


def split_surface_reading(value: str):
    if not value:
        return '', ''
    value = value.strip()
    match = re.match(r'^(.*?)\[(.*?)\]$', value)
    if match:
        surface = normalize_surface(match.group(1))
        reading = normalize_surface(match.group(2))
        return surface, reading
    return normalize_surface(value), ''


def is_kanji(ch: str) -> bool:
    return bool(KANJI_RE.match(ch))


def load_rank_csv(path: Path, word_column: str = 'Word', rank_column: str = 'Rank', delimiter: str = ','):
    print(f'Loading rank file: {path}')
    mapping = {}
    with path.open('r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            key = row.get(word_column)
            rank_value = row.get(rank_column)
            if not key or not rank_value:
                continue
            key = normalize_surface(key)
            try:
                rank = int(rank_value)
            except ValueError:
                continue
            if key and rank > 0:
                existing = mapping.get(key)
                if existing is None or rank < existing:
                    mapping[key] = rank
    print(f'  loaded {len(mapping)} entries from {path.name}')
    return mapping


def load_ririkku_selected(path: Path):
    print(f'Loading RIRIKKU selected frequencies: {path}')
    mapping = {}
    with path.open('r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = normalize_surface(row.get('word', ''))
            if not key:
                continue
            entry = {}
            for col in [
                'RIRIKKU_RANK',
                'RSPEER',
                'cejc_combined_rank',
                'cejc_small_talk_rank',
                'JITEN_DRAMA',
                'ANIME_JDRAMA',
                'YOUTUBE_FREQ_V3',
                'NETFLIX',
            ]:
                value = row.get(col, '')
                try:
                    entry[col] = int(value) if value not in ('', '-1') else None
                except ValueError:
                    entry[col] = None
            mapping[key] = entry
    print(f'  loaded {len(mapping)} RIRIKKU entries')
    return mapping


def load_ririkku_all(path: Path, needed_cols):
    print(f'Loading RIRIKKU consolidated ranks: {path}')
    mapping = {}
    with path.open('r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        available = [col for col in needed_cols if col in headers]
        missing = [col for col in needed_cols if col not in headers]
        if missing:
            print(f'  Warning: missing columns in {path.name}: {missing}')
        for row in reader:
            key = normalize_surface(row.get('word', ''))
            if not key:
                continue
            entry = {}
            for col in available:
                value = row.get(col, '')
                try:
                    entry[col] = int(value) if value not in ('', '-1') else None
                except ValueError:
                    entry[col] = None
            mapping[key] = entry
    print(f'  loaded {len(mapping)} consolidated entries')
    return mapping


def rank_to_score(rank):
    if rank is None or rank <= 0:
        return 0.0
    return 1.0 / rank


def compute_best_score(ranks):
    return max((rank_to_score(r) for r in ranks if r is not None), default=0.0)


def compute_kanji_score(text, kanji_rank_map):
    scores = []
    for ch in text:
        if is_kanji(ch):
            rank = kanji_rank_map.get(ch)
            if rank is not None:
                scores.append(rank_to_score(rank))
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


AMBIGUOUS_KANA_SURFACES = {
    'は', 'が', 'を', 'に', 'と', 'も', 'か', 'や', 'ね', 'よ', 'な', 'で', 'さ', 'ぞ', 'だ', 'の',
    'へ', 'も', 'す', 'れ', 'う', 'つ', 'い', 'き', 'み', 'し', 'お', 'ん', 'わ', 'く', 'か', 'る',
}


def is_ambiguous_kanji_reading(surface: str, kana: str) -> bool:
    if not surface or not any(is_kanji(ch) for ch in surface):
        return False
    kana = kana.strip()
    return kana in AMBIGUOUS_KANA_SURFACES or len(kana) <= 1


def has_match(surface: str, maps):
    if not surface:
        return False
    return any(surface in m for m in maps)


def select_surface(surface: str, kana: str, maps):
    if surface and has_match(surface, maps):
        return surface
    if kana and has_match(kana, maps):
        return kana
    return surface or kana


def assign_order_ids(rows, key, score_key):
    sorted_rows = sorted(
        [row for row in rows if row[score_key] > 0.0],
        key=lambda r: (-r[score_key], r['original_index']),
    )
    order = 1
    for row in sorted_rows:
        row[key] = order
        order += 1
    for row in rows:
        if row.get(key) is None:
            row[key] = ''


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f'Input file not found: {INPUT_PATH}')

    global_freq = load_rank_csv(FREQ_LIST_DIR / 'frequency_list_global.csv', word_column='Word', rank_column='Rank')
    domain_files = [
        'frequency_list_Anime.csv',
        'frequency_list_Drama.csv',
        'frequency_list_Movie.csv',
        'frequency_list_Manga.csv',
        'frequency_list_Novel.csv',
        'frequency_list_VideoGame.csv',
        'frequency_list_VisualNovel.csv',
        'frequency_list_WebNovel.csv',
        'frequency_list_Audio.csv',
    ]
    domain_maps = [load_rank_csv(FREQ_LIST_DIR / fname, word_column='Word', rank_column='Rank') for fname in domain_files]
    kanji_rank = load_rank_csv(KANJI_FREQ, word_column='Kanji', rank_column='Rank')
    ririkku_selected = load_ririkku_selected(RIRIKKU_SELECTED)
    consolidated = load_ririkku_all(RIRIKKU_ALL, ['cejc_meeting_rank', 'cejc_workplace_rank', 'cejc_public_commercial_rank', 'MALTESAA_CSJ'])

    rows = []
    print(f'Reading input file: {INPUT_PATH}')
    with INPUT_PATH.open('r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f, delimiter=';')
        for idx, row in enumerate(reader, start=1):
            raw_key = row.get('key', '') or ''
            raw_furi = row.get('furi', '') or ''
            surface, kana = split_surface_reading(raw_key)
            if not kana:
                _, kana = split_surface_reading(raw_furi)
            if any(is_kanji(ch) for ch in raw_key):
                search_surface = select_surface(surface, kana, [global_freq, *domain_maps, ririkku_selected, consolidated])
                if search_surface != surface and kana:
                    print(f'  fallback to kana reading for kanji key={surface} kana={kana} (row {idx})')
            else:
                search_surface = surface or kana
            if not search_surface:
                search_surface = surface

            ririkku_entry = ririkku_selected.get(search_surface, {})
            consolidated_entry = consolidated.get(search_surface, {})
            global_rank = global_freq.get(search_surface)

            general_ranks = [
                global_rank,
                ririkku_entry.get('RSPEER'),
                ririkku_entry.get('WIKIPEDIA_V2'),
                ririkku_entry.get('ADNO'),
                ririkku_entry.get('CC100'),
                ririkku_entry.get('JITEN_GLOBAL'),
            ]
            if not is_ambiguous_kanji_reading(surface, kana):
                general_ranks.append(ririkku_entry.get('RIRIKKU_RANK'))
            general_score = compute_best_score(general_ranks)

            oral_ranks = [
                ririkku_entry.get('cejc_combined_rank'),
                ririkku_entry.get('cejc_small_talk_rank'),
                ririkku_entry.get('YOUTUBE_FREQ_V3'),
                ririkku_entry.get('NETFLIX'),
                ririkku_entry.get('ANIME_JDRAMA'),
                ririkku_entry.get('JITEN_DRAMA'),
            ]
            oral_score = compute_best_score(oral_ranks)

            professional_ranks = [
                consolidated_entry.get('cejc_meeting_rank'),
                consolidated_entry.get('cejc_workplace_rank'),
                consolidated_entry.get('cejc_public_commercial_rank'),
                consolidated_entry.get('MALTESAA_CSJ'),
            ]
            professional_score = compute_best_score(professional_ranks)

            fiction_ranks = [
                global_rank,
                ririkku_entry.get('ANIME_JDRAMA'),
                ririkku_entry.get('NETFLIX'),
                ririkku_entry.get('JITEN_DRAMA'),
            ]
            for domain_map in domain_maps:
                rank = domain_map.get(search_surface)
                if rank is not None:
                    fiction_ranks.append(rank)
            fiction_score = compute_best_score(fiction_ranks)

            kanji_score = compute_kanji_score(surface, kanji_rank)

            row_data = {**row}
            row_data.update({
                'surface': surface,
                'score_general': general_score,
                'score_oral': oral_score,
                'score_professional': professional_score,
                'score_fiction': fiction_score,
                'score_kanji': kanji_score,
                'priority_general': '',
                'priority_oral': '',
                'priority_professional': '',
                'priority_fiction': '',
                'priority_kanji': '',
                'original_index': idx,
            })
            rows.append(row_data)
            if idx % 2000 == 0:
                print(f'  processed {idx} input rows')

    print(f'Assigning order ids for {len(rows)} rows')
    assign_order_ids(rows, 'priority_general', 'score_general')
    assign_order_ids(rows, 'priority_oral', 'score_oral')
    assign_order_ids(rows, 'priority_professional', 'score_professional')
    assign_order_ids(rows, 'priority_fiction', 'score_fiction')
    assign_order_ids(rows, 'priority_kanji', 'score_kanji')

    output_fields = list(reader.fieldnames or []) + NEW_COLUMNS
    print(f'Writing output file: {OUTPUT_PATH}')
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=output_fields, delimiter=';')
        writer.writeheader()
        for row in rows:
            out = {k: row.get(k, '') for k in output_fields}
            writer.writerow(out)

    print('Done. Output written.')


if __name__ == '__main__':
    main()
