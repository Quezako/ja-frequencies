# Priorités d'apprentissage des sources de fréquence

Ce document recense les fichiers CSV/MD du projet, les regroupe par intérêt pédagogique, et propose un ordre d'apprentissage adapté à un deck Anki.

---

## 1. Inventaire des sources principales

### 1.1 Sources média / fiction
- `frequency_list/frequency_list_global.csv` : fréquence globale toutes sources confondues.
- `frequency_list/frequency_list_Anime.csv` : anime.
- `frequency_list/frequency_list_Drama.csv` : drama.
- `frequency_list/frequency_list_Movie.csv` : film.
- `frequency_list/frequency_list_Manga.csv` : manga.
- `frequency_list/frequency_list_Novel.csv` : roman.
- `frequency_list/frequency_list_VideoGame.csv` : jeu vidéo.
- `frequency_list/frequency_list_VisualNovel.csv` : visual novel.
- `frequency_list/frequency_list_WebNovel.csv` : web novel.
- `frequency_list/frequency_list_Audio.csv` : audio/podcasts.

### 1.2 Sources de fréquence multi-corpus et agrégées
- `japanese-word-ranks-main/data/frequency/top25k-all-freq/consolidated.csv` : tableau de fréquence multi-source (top 25k) avec colonnes de corpus variés.
- `japanese-word-ranks-main/data/RIRIKKU_V2/RIRIKKU_CONSOLIDATED_V2.csv` : version RIRIKKU V2, multi-source centrée sur immersion médias/lyrics.
- `japanese-word-ranks-main/data/frequency/selected-freq/RIRIKKU_CONSOLIDATED.csv` : version sélectionnée de RIRIKKU.
- `japanese-word-ranks-main/data/frequency/selected-freq/RIRIKKU_CONSOLIDATED_MODIFIED_V1.csv` : variante modifiée de la sélection RIRIKKU.
- `japanese-word-ranks-main/data/RIRIKKU_V2/RIRIKKU_CONSOLIDATED_V2_other_ranks.csv` : colonnes supplémentaires de rangs par corpus.

### 1.3 Sources JLPT / vocabulaire structuré
- `JLPT/open-anki-jlpt/n5.csv` à `JLPT/open-anki-jlpt/n1.csv` : listes Anki prêtes à l'emploi par niveau JLPT.
- `JLPT/bunpro-voc-jlpt.csv` : vocabulaire Bunpro + niveau JLPT.
- `JLPT/bunpro-jlpt-api.csv` : export API Bunpro avec tags et niveau.
- `JLPT/bunpro-o-vocab-extracted.csv` : extraction vocabulaire Bunpro.
- `JLPT/jlpt_vocab_pedagogical.csv` : vocabulaire JLPT pédagogique.
- `japanese-word-ranks-main/data/kaishi/kaishi_1500.txt` : liste de 1500 mots de démarrage.

### 1.4 Sources kanji et fréquence kanji
- `kanji/jiten_kanji_freq.csv` : fréquence kanji jiten.moe.
- `kanji/Kanji freq FULL.csv` : données kanji étendues avec niveaux, fréquence, Wanikani, RTK, etc.
- `kanji/RTK1&3 Edition numbers compared.csv` : correspondances RTK/RTK3, lectures, mots-clés.
- `kanji/Kanji__00 Wanikani Ult 2.txt` : dataset Wanikani/kanji.
- `japanese-subtitles-word-kanji-frequency-lists-master/kanji_freq_report.txt` : fréquence kanji sous-titres.

### 1.5 Sources de sous-titres et reports
- `japanese-subtitles-word-kanji-frequency-lists-master/README.md` : documentation du corpus sous-titres.
- `japanese-subtitles-word-kanji-frequency-lists-master/word_freq_report.txt` : fréquence mot sous-titres.
- `japanese-subtitles-word-kanji-frequency-lists-master/kanji_freq_report.txt` : fréquence kanji sous-titres.
- `Master frequency lists/Anime - instance_freq_report.txt` : rapport fréquence anime.
- `Master frequency lists/Anime - morph_freq_report.txt` : rapport morphologique anime.
- `Master frequency lists/Game - instance_freq_report.txt` : rapport fréquence jeux.
- `Master frequency lists/Game - morph_freq_report.txt` : rapport morphologique jeux.
- `Master frequency lists/Netflix -  instance_freq_report - No Name (netflix_unidic_3011_no_names_word_freq_report).txt` : rapport Netflix.
- `Master frequency lists/Jp Yomi - Words by Yomi Frequency w_ Kanji Info, Stats.txt` : fréquence kanji Yomi.

### 1.6 Notes et documentation interne
- `japanese-word-ranks-main/data/frequency/dataset-catalog.md` : catalogue des sources de corpus et leur utilité.
- `japanese-word-ranks-main/data/frequency/top25k-all-freq/README.md` : guide sur le fichier `consolidated.csv`.
- `japanese-word-ranks-main/data/frequency/selected-freq/SINGLE_RANK.md` : principe du classement RIRIKKU.
- `japanese-word-ranks-main/data/notes/duplicates.md` : analyse des doublons kanji/kana dans RIRIKKU.
- `japanese-word-ranks-main/data/notes/data-mismatch-notes.md` : notes sur incohérences de rangs.
- `japanese-word-ranks-main/data/notes/notes-by-claude.md` : plan et contexte pour une application de lookup.

---

## 2. Regroupement par intérêt pédagogique

### 2.1 Priorité « communication orale quotidienne »
Registres à cibler en premier pour un usage réel : conversation de rue, petits échanges, phrases de base.
- `frequency_list_global.csv`
- colonnes CEJC/CEJC small talk dans `consolidated.csv` / `RIRIKKU_CONSOLIDATED*`
- `YOUTUBE_FREQ_V3`, `NETFLIX`, `ANIME_JDRAMA`, `DD2_MORPHMAN_NETFLIX`, `JITEN_DRAMA`
- listes JLPT débutant (`open-anki-jlpt/n5.csv`, `bunpro-voc-jlpt.csv`)

### 2.2 Priorité « parler en entreprise / registre formel »
- colonnes `cejc_meeting_rank`, `cejc_workplace_rank`, `cejc_public_commercial_rank` dans `consolidated.csv` et `RIRIKKU_CONSOLIDATED*`
- `MALTESAA_CSJ` (parole académique/formelle) dans les fichiers RIRIKKU
- vocabulaire de service, de meeting et de bureau à extraire selon ces champs

### 2.3 Priorité « fiction, immersion et médias »
Registres spécifiques du projet : anime, drama, films, jeux, romans, visual novels, web novels.
- `frequency_list_Anime.csv`
- `frequency_list_Drama.csv`
- `frequency_list_Movie.csv`
- `frequency_list_Manga.csv`
- `frequency_list_Novel.csv`
- `frequency_list_VideoGame.csv`
- `frequency_list_VisualNovel.csv`
- `frequency_list_WebNovel.csv`
- `frequency_list_Audio.csv`
- `japanese-subtitles-word-kanji-frequency-lists-master/*`
- `Master frequency lists/*.txt`

### 2.4 Priorité « écriture et lecture »
Vocabulaire de lecture, dictionnaire, écrit formel et corpora web.
- `BCCWJ_LUW`, `BCCWJ_SUW` dans `consolidated.csv`
- `WIKIPEDIA_V2`, `ADNO`, `CC100`, `MALTESAA_NWJC` dans `consolidated.csv`
- `KUUUUBE_JMDICT_FREQ` dans `consolidated.csv`
- `kanji/Kanji freq FULL.csv`
- `kanji/jiten_kanji_freq.csv`

### 2.5 Priorité « apprentissage des kanji »
- `kanji/jiten_kanji_freq.csv`
- `kanji/Kanji freq FULL.csv`
- `kanji/RTK1&3 Edition numbers compared.csv`
- `kanji/Kanji__00 Wanikani Ult 2.txt`
- `japanese-subtitles-word-kanji-frequency-lists-master/kanji_freq_report.txt`

### 2.6 Priorité « listes hébergées / JLPT »
- tous les fichiers dans `JLPT/`
- `japanese-word-ranks-main/data/kaishi/kaishi_1500.txt`

### 2.7 Documentation et notes utiles
- `japanese-word-ranks-main/data/frequency/dataset-catalog.md`
- `japanese-word-ranks-main/data/frequency/top25k-all-freq/README.md`
- `japanese-word-ranks-main/data/frequency/selected-freq/SINGLE_RANK.md`
- `japanese-word-ranks-main/data/notes/duplicates.md`
- `japanese-word-ranks-main/data/notes/data-mismatch-notes.md`

---

## 3. Ordre d'apprentissage recommandé

1. **Mots de base et grammaire courante**
   - champs JLPT (`open-anki-jlpt`, `bunpro-*`, `jlpt_vocab_pedagogical.csv`)
   - mots très fréquents de `frequency_list_global.csv`
   - fonctionnels, particules, auxiliaires

2. **Conversation quotidienne / oral natif**
   - `cejc_small_talk_rank`
   - `YOUTUBE_FREQ_V3`, `NETFLIX`, `ANIME_JDRAMA`, `JITEN_DRAMA`
   - phrases courantes de la rue, expressions d'usage

3. **Registre formel / professionnel**
   - `cejc_meeting_rank`, `cejc_workplace_rank`
   - `MALTESAA_CSJ`
   - vocabulaire de bureau, service client, réunions, transport public

4. **Fiction et immersion ludique**
   - `frequency_list_Anime.csv`, `frequency_list_Manga.csv`, `frequency_list_Novel.csv`, `frequency_list_VideoGame.csv`, `frequency_list_VisualNovel.csv`, `frequency_list_WebNovel.csv`
   - vocabulaire média/genre spécifique, termes narratifs, émotionnels, slang

5. **Lecture et corpus écrits**
   - `BCCWJ_LUW`, `WIKIPEDIA_V2`, `ADNO`, `CC100`, `KUUUUBE_JMDICT_FREQ`
   - termes littéraires, techniques, encyclopédiques

6. **Kanji et fréquence de caractères**
   - `jiten_kanji_freq.csv`, `Kanji freq FULL.csv`, `RTK1&3 Edition numbers compared.csv`, `Kanji__00 Wanikani Ult 2.txt`
   - opposition kanji / kana pour prioriser l'apprentissage d'un caractère

7. **Affinage / rare**
   - corpus spécialisés (`MALTESAA_NWJC`, `NAROU`, certains rapports Netflix/Game)
   - mots peu fréquents ou propres au registre très spécifique

---

## 4. Remarques sur les doublons et versions

- Analyse rapide des fichiers CSV/MD/TXT a montré **aucun doublon exact** détecté dans les sources listées.
- Il existe en revanche plusieurs variantes d'un même dataset :
  - `RIRIKKU_CONSOLIDATED.csv`, `RIRIKKU_CONSOLIDATED_MODIFIED_V1.csv`, `RIRIKKU_CONSOLIDATED_V2.csv`, `RIRIKKU_CONSOLIDATED_V2_other_ranks.csv`
  - `frequency_list_global.csv` vs `frequency_list_*.csv` (mêmes colonnes, domaines différents)
  - `Master frequency lists/*.txt` sont des rapports de fréquence, pas des CSV standard.
- `japanese-word-ranks-main/data/notes/duplicates.md` indique des doublons internes entre formes kanji et kana dans `RIRIKKU_CONSOLIDATED.csv`. Pour un deck Anki, il est préférable de conserver les deux formes et de lier les entrées plutôt que de les fusionner automatiquement.

---

## 5. Champs Anki recommandés

Pour faciliter le filtrage et le tri par priorité, ajoute ces champs au deck :
- `Source` : nom du fichier ou du dataset (`RIRIKKU_CONSOLIDATED`, `ANIME`, `NETFLIX`, `JLPT`, etc.)
- `Register` : `oral`, `formel`, `business`, `fiction`, `écrit`, `audio`, `jeu`, etc.
- `Media` : `anime`, `drama`, `film`, `manga`, `roman`, `jeu`, `web novel`, `audio`, `web`, `wiki`
- `DatasetRank` : rang de fréquence dans la source principale
- `LearningPriority` : `high`, `medium`, `low` (ou `BASIC/COMMON/FLUENT/ADVANCED`)
- `JLPTLevel` : `N5` à `N1` si applicable
- `KanjiPriority` : fréquence kanji / kanji courant / kanji rare
- `Context` : `small talk`, `meeting`, `home`, `school`, `transport`, `public`, `workplace`
- `FictionPriority` : `oui` / `non` / `genre-specific`
- `Form` : `kanji`, `kana`, `mixed`
- `Note` : commentaire libre sur la source ou le registre

---

## 6. Script d'analyse ajouté

- `analyze_frequency_files.py` : script Python à la racine qui inventorie les fichiers CSV/MD/TXT et détecte les doublons exacts / variantes de sources.

> Ce fichier est une synthèse de l'inventaire et des priorités d'apprentissage. Il peut servir de base de tri pour enrichir un deck Anki avec des tags et des champs de registre.
