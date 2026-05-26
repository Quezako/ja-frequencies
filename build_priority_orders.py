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
    """Split strings like 漢字[かな] into (surface, kana)."""
    if not value:
        return ('', '')
    m = re.match(r'^(.*?)\[(.*?)\]$', value)
    if m:
        return (m.group(1).strip(), m.group(2).strip())
    # if no brackets, return as surface and empty kana
    return (value.strip(), '')


def is_kanji(ch: str) -> bool:
    return bool(KANJI_RE.search(ch))


def load_rank_csv(path, word_column='Word', rank_column='Rank'):
    """Load a two-column CSV mapping word->rank (int). Returns dict.
    If file missing, returns empty dict.
    """
    d = {}
    p = Path(path)
    if not p.exists():
        print(f'  rank file not found: {p}')
        return d
    with p.open('r', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.DictReader(f)
        # try to detect a Form column (kana reading) and map it as well
        form_keys = ['Form', 'form', 'Reading', 'reading']
        for row in reader:
            w = row.get(word_column) or row.get(word_column.lower())
            r = row.get(rank_column) or row.get(rank_column.lower())
            if not w:
                continue
            try:
                rnum = int(r) if r and r != '' else None
            except Exception:
                try:
                    rnum = int(float(r))
                except Exception:
                    rnum = None
            # keep the best (smallest) rank if duplicates occur for the same word
            if w in d:
                existing = d.get(w)
                if existing is None:
                    d[w] = rnum
                elif rnum is not None:
                    try:
                        d[w] = min(existing, rnum) if existing is not None else rnum
                    except Exception:
                        d[w] = existing
            else:
                d[w] = rnum
            # also map the kana/form column if present (so lookups by kana work)
            form = None
            for fk in form_keys:
                if fk in row and row.get(fk):
                    form = row.get(fk)
                    break
            if form:
                form = form.strip()
                if form:
                    if form in d:
                        existing = d.get(form)
                        if existing is None:
                            d[form] = rnum
                        elif rnum is not None:
                            try:
                                d[form] = min(existing, rnum) if existing is not None else rnum
                            except Exception:
                                d[form] = existing
                    else:
                        d[form] = rnum
    return d


def load_ririkku_selected(path):
    d = {}
    p = Path(path)
    if not p.exists():
        print(f'  ririkku selected file not found: {p}')
        return d
    with p.open('r', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            w = row.get('Word') or row.get('word') or ''
            if not w:
                continue
            entry = {}
            # capture a handful of useful columns
            for k in row:
                v = row.get(k)
                if v is None or v == '':
                    continue
                try:
                    entry[k] = int(v)
                except Exception:
                    try:
                        entry[k] = int(float(v))
                    except Exception:
                        entry[k] = v
            # canonicalize rank field name if present
            if 'Rank' in row and row.get('Rank'):
                try:
                    entry['RIRIKKU_RANK'] = int(row.get('Rank'))
                except Exception:
                    pass
            d[w] = entry
    return d


def load_ririkku_all(path, extra_fields=None):
    d = {}
    p = Path(path)
    if not p.exists():
        print(f'  ririkku consolidated file not found: {p}')
        return d
    with p.open('r', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            w = row.get('Word') or row.get('word') or ''
            if not w:
                continue
            entry = {}
            for fkey in (extra_fields or []):
                v = row.get(fkey)
                if v is None or v == '':
                    continue
                try:
                    entry[fkey] = int(v)
                except Exception:
                    try:
                        entry[fkey] = int(float(v))
                    except Exception:
                        entry[fkey] = v
            d[w] = entry
    return d


def rank_to_score(rank):
    if not rank or rank <= 0:
        return 0.0
    return 1.0 / float(rank)


def compute_best_score(ranks):
    scores = [rank_to_score(r) for r in (ranks or []) if r]
    return max(scores) if scores else 0.0


def compute_kanji_score(surface: str, kanji_rank_map: dict) -> float:
    if not surface or not kanji_rank_map:
        return 0.0
    scores = []
    for ch in surface:
        if is_kanji(ch):
            rank = kanji_rank_map.get(ch)
            if rank:
                scores.append(rank_to_score(rank))
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


AMBIGUOUS_KANA_SURFACES = {
    'は', 'が', 'を', 'に', 'と', 'も', 'か', 'や', 'ね', 'よ', 'な', 'で', 'さ', 'ぞ', 'だ', 'の',
    'へ', 'す', 'れ', 'う', 'つ', 'い', 'き', 'み', 'し', 'お', 'ん', 'わ', 'く', 'る',
}


def apply_single_kanji_ambiguous_penalty(surface: str, kana: str, score: float, tags: str = '', vocab_order: str = '') -> float:
    if score <= 0.0:
        return score
    # stronger penalty when single-kanji ambiguous reading AND heuristics mark it ambiguous
    if surface and len(surface) == 1 and should_treat_as_ambiguous(surface, kana, tags, vocab_order):
        return score * 0.01
    # moderate penalty for multi-kanji ambiguous readings
    if surface and len(surface) > 1 and should_treat_as_ambiguous(surface, kana, tags, vocab_order):
        return score * 0.2
    return score


def should_treat_as_ambiguous(surface: str, kana: str, tags: str, vocab_order: str) -> bool:
    """Return True if this kanji[kana] pair should be considered ambiguous/rare
    and thus treated conservatively (no kana fallback, strong penalty).
    Heuristics used:
    - if kana is short or in ambiguous set -> True
    - if tags indicate JLPT N1 or JLPT::1 or not Common -> True
    - if vocab_order present and large (rare word) -> True
    """
    if not surface or not any(is_kanji(ch) for ch in surface):
        return False
    kana = (kana or '').strip()
    tags = (tags or '')
    # short kana or canonical ambiguous particles
    if kana in AMBIGUOUS_KANA_SURFACES or len(kana) <= 1:
        return True
    # treat common verbal/kana suffixes as ambiguous when attached to kanji (eg. 為る[する], 刷る[する])
    if kana in {'する', 'そう'}:
        return True
    # tag signals
    if 'JLPT::1' in tags or 'JLPT::N1' in tags or 'JLPT::K1::1' in tags:
        return True
    if 'Common' not in tags:
        # try vocab_order as numeric; treat large numbers as rare
        try:
            vo = int((vocab_order or '').strip())
        except Exception:
            vo = None
        if vo is None or vo > 1000:
            return True
    return False


def has_match(surface: str, maps):
    if not surface:
        return False
    return any(surface in m for m in maps)


def select_surface(surface: str, kana: str, maps, allow_fallback: bool = True):
    if surface and has_match(surface, maps):
        return surface
    if not allow_fallback:
        return surface or kana
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

    # Two-pass: first collect input rows and kana readings per surface
    temp_rows = []
    surface_kana_map = {}
    print(f'Reading input file (collect pass): {INPUT_PATH}')
    with INPUT_PATH.open('r', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.DictReader(f, delimiter=';')
        fieldnames = list(reader.fieldnames or [])
        for idx, row in enumerate(reader, start=1):
            raw_key = row.get('key', '') or row.get('\ufeffkey', '') or ''
            raw_furi = row.get('furi', '') or ''
            surface, kana = split_surface_reading(raw_key)
            if not kana:
                _, kana = split_surface_reading(raw_furi)
            temp_rows.append({'idx': idx, 'row': row, 'surface': surface, 'kana': kana})
            if surface:
                surface_kana_map.setdefault(surface, set()).add(kana or '')

    # compute best kana rank per surface from global_freq
    best_kana_rank = {}
    for surface, kanas in surface_kana_map.items():
        ranks = [global_freq.get(k) for k in kanas if k]
        ranks = [r for r in ranks if r is not None]
        if ranks:
            best_kana_rank[surface] = min(ranks)

    rows = []
    print(f'Processing {len(temp_rows)} input rows (score pass)')
    for entry in temp_rows:
        idx = entry['idx']
        row = entry['row']
        surface = entry['surface']
        kana = entry['kana']
        if any(is_kanji(ch) for ch in (row.get('key','') or row.get('\ufeffkey',''))):
            tags = row.get('tags', '') or ''
            vocab_order = row.get('vocab_order', '') or ''
            is_ambiguous = should_treat_as_ambiguous(surface, kana, tags, vocab_order)
            # detect outlier reading for this surface compared to other kana readings
            outlier_reading = False
            if surface and kana and surface in best_kana_rank:
                kana_rank = global_freq.get(kana)
                best_rank = best_kana_rank.get(surface)
                try:
                    if kana_rank is not None and best_rank is not None and kana_rank > best_rank * 5:
                        outlier_reading = True
                except Exception:
                    outlier_reading = False
            # treat as ambiguous if outlier reading detected
            if outlier_reading:
                is_ambiguous = True
            search_surface = select_surface(
                surface,
                kana,
                [global_freq, *domain_maps, ririkku_selected, consolidated],
                allow_fallback=not is_ambiguous,
            )
            if search_surface != surface and kana:
                print(f'  fallback to kana reading for kanji key={surface} kana={kana} (row {idx})')
        else:
            search_surface = surface or kana
        if not search_surface:
            search_surface = surface

        ririkku_entry = ririkku_selected.get(search_surface, {})
        consolidated_entry = consolidated.get(search_surface, {})
        global_rank = global_freq.get(search_surface)

        general_ranks = [global_rank]
        # include RIRIKKU only when we don't consider this an ambiguous/rare kanji reading
        if not should_treat_as_ambiguous(surface, kana, row.get('tags', ''), row.get('vocab_order', '')):
            r_rank = ririkku_entry.get('RIRIKKU_RANK')
            if r_rank is not None:
                try:
                    kana_rank = global_freq.get(kana) if kana else None
                    surface_rank = global_freq.get(surface)
                    if kana and kana_rank is not None and r_rank < (kana_rank / 5):
                        r_rank = None
                    elif surface_rank is not None and surface_rank > 0 and (surface_rank / r_rank) > 50:
                        r_rank = None
                except Exception:
                    pass
            if r_rank is not None:
                general_ranks.append(r_rank)
        general_score = compute_best_score(general_ranks)
        # increase penalty for outlier readings
        if surface and kana and surface in best_kana_rank:
            kana_rank = global_freq.get(kana)
            best_rank = best_kana_rank.get(surface)
            try:
                if kana_rank is not None and best_rank is not None and kana_rank > best_rank * 5:
                    general_score = apply_single_kanji_ambiguous_penalty(surface, kana, general_score, row.get('tags', ''), row.get('vocab_order', '')) * 0.1
                else:
                    general_score = apply_single_kanji_ambiguous_penalty(surface, kana, general_score, row.get('tags', ''), row.get('vocab_order', ''))
            except Exception:
                general_score = apply_single_kanji_ambiguous_penalty(surface, kana, general_score, row.get('tags', ''), row.get('vocab_order', ''))

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

        # suppress oral/fiction if the kanji surface is much rarer than the kana-based oral/fiction signal
        if any(is_kanji(ch) for ch in surface):
            if general_score > 0:
                if oral_score > general_score * 20:
                    oral_score = 0.0
                if fiction_score > general_score * 20:
                    fiction_score = 0.0
            elif should_treat_as_ambiguous(surface, kana, row.get('tags', ''), row.get('vocab_order', '')):
                oral_score = 0.0
                fiction_score = 0.0

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
