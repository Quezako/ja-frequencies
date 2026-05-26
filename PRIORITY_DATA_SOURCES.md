# Sources de données pour les colonnes de priorité

Ce document décrit les fichiers `20-data/` utilisés par `build_priority_orders.py` pour calculer les ordres d’apprentissage.

## Colonnes ajoutées

- `priority_general`
- `priority_oral`
- `priority_professional`
- `priority_fiction`
- `priority_kanji`

## Sources utilisées

### priority_general
- `20-data/10-frequency_list/frequency_list_global.csv`
- `20-data/00-japanese-word-ranks/frequency/selected-freq/RIRIKKU_CONSOLIDATED.csv`

Pourquoi : cette colonne doit refléter l’importance générale du mot, en combinant une fréquence globale globale avec le classement RIRIKKU multi-source.

### priority_oral
- `20-data/00-japanese-word-ranks/frequency/selected-freq/RIRIKKU_CONSOLIDATED.csv`
  - `cejc_combined_rank`
  - `cejc_small_talk_rank`
  - `YOUTUBE_FREQ_V3`
  - `NETFLIX`
  - `ANIME_JDRAMA`
  - `JITEN_DRAMA`

Pourquoi : ces colonnes donnent un signal fort du vocabulaire oral et des médias parlés, utile pour la conversation naturelle et l’immersion.

### priority_professional
- `20-data/00-japanese-word-ranks/frequency/top25k-all-freq/consolidated.csv`
  - `cejc_meeting_rank`
  - `cejc_workplace_rank`
  - `cejc_public_commercial_rank`
  - `MALTESAA_CSJ`

Pourquoi : cette colonne cible le vocabulaire formel et professionnel en entreprise, réunion et service client.

### priority_fiction
- `20-data/10-frequency_list/frequency_list_Anime.csv`
- `20-data/10-frequency_list/frequency_list_Drama.csv`
- `20-data/10-frequency_list/frequency_list_Movie.csv`
- `20-data/10-frequency_list/frequency_list_Manga.csv`
- `20-data/10-frequency_list/frequency_list_Novel.csv`
- `20-data/10-frequency_list/frequency_list_VideoGame.csv`
- `20-data/10-frequency_list/frequency_list_VisualNovel.csv`
- `20-data/10-frequency_list/frequency_list_WebNovel.csv`
- `20-data/10-frequency_list/frequency_list_Audio.csv`
- `20-data/00-japanese-word-ranks/frequency/selected-freq/RIRIKKU_CONSOLIDATED.csv`
  - `ANIME_JDRAMA`
  - `NETFLIX`
  - `JITEN_DRAMA`

Pourquoi : ces listes reflètent le vocabulaire des fictions, médias et genres à immersion (anime, drama, romans, jeux, audio).

### priority_kanji
- `20-data/40-kanji/jiten_kanji_freq.csv`

Pourquoi : cette colonne donne un ordre en fonction de la fréquence des kanji composants du mot, utile pour prioriser l’apprentissage des caractères.

## Remarques

- Le script `build_priority_orders.py` génère un ordre `1, 2, 3...` pour chaque colonne en fonction du score de fréquence calculé.
- Si un mot n’est trouvé dans aucune source pertinente, la colonne reste vide.
- Les entrées du dossier `00-input/` sont enrichies dans `10-output/`.
