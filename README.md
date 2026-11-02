# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders (Spotify, YouTube) combine two signals: *collaborative filtering* (what people with similar listening histories liked) and *content-based filtering* (how similar a song's own attributes are to what you already like). My version is purely content-based: it has no other users, so it compares each song's attributes to a single taste profile and returns the closest matches. It prioritizes the "vibe" of a song (mood and energy) and the genre, and rewards songs that are *close* to the user's preference rather than simply higher or lower.

### Features

**`Song`** (from `data/songs.csv`): `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`

**`UserProfile`**: `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic` (plus optional `target_valence`)

The most useful features for vibe are `energy`, `mood`, `valence`, and `acousticness`. `tempo_bpm` is on a different scale (60–152) and largely overlaps with energy, so it is left out of the first version.

### Scoring Rule (one song)

For numeric features, score by closeness instead of magnitude:

```
similarity = 1 - |song_value - user_target|     # 1.0 = perfect match, 0.0 = opposite
```

Total score is a weighted sum:

| Component | Points |
|---|---|
| Genre match | +2.0 |
| Mood match | +1.0 |
| Energy similarity | up to +2.0 (`2.0 * (1 - abs(energy - target))`) |
| Valence / acousticness similarity | up to +1.0 each |

Genre is weighted above mood because genre is a coarser, more reliable filter, while mood labels are subjective and a song in another genre can still fit the mood. Energy is weighted as heavily as genre because a closeness score on it separates songs that genre alone cannot.

### Catalog

`data/songs.csv` now has 18 songs. The 8 added songs cover genres and moods missing from the starter set: hip hop, classical, country, EDM, R&B, metal, reggae and folk, with moods such as confident, peaceful, nostalgic, energetic, romantic, angry, uplifting and melancholy.

### Taste Profile

```python
user_profile = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,
    "target_valence": 0.60,
    "likes_acoustic": True,
}
```

This profile separates "chill lofi" from "intense rock" well: energy alone is 0.40 vs 0.91, and genre and mood both differ, so rock songs score near zero. A weakness is that it is narrow, since it describes one kind of listener and can't express a mix such as "chill lofi plus upbeat pop."

### Data Flow

```
Input: user_profile + songs.csv
   |
   v
Process: for each song in the catalog
   score = genre points + mood points + energy/valence/acoustic similarity
   |
   v
Output: sort all (song, score) pairs descending -> top K recommendations
```

### Expected Biases

- **Genre dominance:** with +2.0 for genre, a mediocre song in the favorite genre can outrank a better mood and energy match from another genre (for example, a chill jazz track for a lofi fan).
- **Exact-match labels:** "chill" and "relaxed" are treated as completely different moods even though they sound similar.
- **Small, uneven catalog:** most genres have only one song, so a user whose favorite genre is rare gets a genre bonus on at most one track.
- **Single target value:** a user who likes both calm and high-energy music is scored against one energy number and fits neither.

### Ranking Rule (list of songs)

The scoring rule only judges one song in isolation; a number like 4.3 means nothing by itself. The ranking rule applies the scoring rule to every song in the catalog, sorts by score descending, and returns the top *k*. Both are needed: scoring defines what "good" means, ranking turns those scores into an ordered recommendation list.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` for the default pop / happy / energy 0.8 profile:

```
Loaded songs: 18

Profile: genre=pop, mood=happy, energy=0.8

Top recommendations:

1. Sunrise City by Neon Echo  -  Score: 4.96
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.82 vs target 0.80 (+1.96)

2. Gym Hero by Max Pulse  -  Score: 3.74
     - genre match (+2.0)
     - energy 0.93 vs target 0.80 (+1.74)

3. Rooftop Lights by Indigo Parade  -  Score: 2.92
     - mood match (+1.0)
     - energy 0.76 vs target 0.80 (+1.92)

4. Night Drive Loop by Neon Echo  -  Score: 1.90
     - energy 0.75 vs target 0.80 (+1.90)

5. Concrete Poetry by Verse Theory  -  Score: 1.82
     - energy 0.71 vs target 0.80 (+1.82)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Evaluation Output

Terminal output of `python -m src.main` (top 5 for each profile).

### Original weights (genre 2.0, mood 1.0, energy 2.0)

```
Loaded songs: 18

=== High-Energy Pop: {'genre': 'pop', 'mood': 'happy', 'energy': 0.9} ===

1. Sunrise City (pop/happy)  -  Score: 4.84
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.82 vs target 0.90 (+1.84)
2. Gym Hero (pop/intense)  -  Score: 3.94
     - genre match (+2.0)
     - energy 0.93 vs target 0.90 (+1.94)
3. Rooftop Lights (indie pop/happy)  -  Score: 2.72
     - mood match (+1.0)
     - energy 0.76 vs target 0.90 (+1.72)
4. Storm Runner (rock/intense)  -  Score: 1.98
     - energy 0.91 vs target 0.90 (+1.98)
5. Neon Overdrive (edm/energetic)  -  Score: 1.88
     - energy 0.96 vs target 0.90 (+1.88)

=== Chill Lofi: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.4, 'valence': 0.6, 'likes_acoustic': True} ===

1. Library Rain (lofi/chill)  -  Score: 6.76
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.35 vs target 0.40 (+1.90)
     - valence 0.60 vs target 0.60 (+1.00)
     - acousticness 0.86 fits taste (+0.86)
2. Midnight Coding (lofi/chill)  -  Score: 6.63
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.42 vs target 0.40 (+1.96)
     - valence 0.56 vs target 0.60 (+0.96)
     - acousticness 0.71 fits taste (+0.71)
3. Focus Flow (lofi/focused)  -  Score: 5.77
     - genre match (+2.0)
     - energy 0.40 vs target 0.40 (+2.00)
     - valence 0.59 vs target 0.60 (+0.99)
     - acousticness 0.78 fits taste (+0.78)
4. Spacewalk Thoughts (ambient/chill)  -  Score: 4.63
     - mood match (+1.0)
     - energy 0.28 vs target 0.40 (+1.76)
     - valence 0.65 vs target 0.60 (+0.95)
     - acousticness 0.92 fits taste (+0.92)
5. Coffee Shop Stories (jazz/relaxed)  -  Score: 3.72
     - energy 0.37 vs target 0.40 (+1.94)
     - valence 0.71 vs target 0.60 (+0.89)
     - acousticness 0.89 fits taste (+0.89)

=== Deep Intense Rock: {'genre': 'rock', 'mood': 'intense', 'energy': 0.92} ===

1. Storm Runner (rock/intense)  -  Score: 4.98
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.91 vs target 0.92 (+1.98)
2. Gym Hero (pop/intense)  -  Score: 2.98
     - mood match (+1.0)
     - energy 0.93 vs target 0.92 (+1.98)
3. Neon Overdrive (edm/energetic)  -  Score: 1.92
     - energy 0.96 vs target 0.92 (+1.92)
4. Iron Requiem (metal/angry)  -  Score: 1.90
     - energy 0.97 vs target 0.92 (+1.90)
5. Sunrise City (pop/happy)  -  Score: 1.80
     - energy 0.82 vs target 0.92 (+1.80)

=== Adversarial: Sad but Energetic: {'genre': 'folk', 'mood': 'sad', 'energy': 0.9} ===

1. Winter Porch Songs (folk/melancholy)  -  Score: 2.82
     - genre match (+2.0)
     - energy 0.31 vs target 0.90 (+0.82)
2. Storm Runner (rock/intense)  -  Score: 1.98
     - energy 0.91 vs target 0.90 (+1.98)
3. Gym Hero (pop/intense)  -  Score: 1.94
     - energy 0.93 vs target 0.90 (+1.94)
4. Neon Overdrive (edm/energetic)  -  Score: 1.88
     - energy 0.96 vs target 0.90 (+1.88)
5. Iron Requiem (metal/angry)  -  Score: 1.86
     - energy 0.97 vs target 0.90 (+1.86)

=== Adversarial: Unknown Genre: {'genre': 'k-pop', 'mood': 'euphoric', 'energy': 0.5} ===

1. Velvet Hours (r&b/romantic)  -  Score: 1.98
     - energy 0.49 vs target 0.50 (+1.98)
2. Dusty Back Road (country/nostalgic)  -  Score: 1.96
     - energy 0.52 vs target 0.50 (+1.96)
3. Island Breeze (reggae/uplifting)  -  Score: 1.84
     - energy 0.58 vs target 0.50 (+1.84)
4. Midnight Coding (lofi/chill)  -  Score: 1.84
     - energy 0.42 vs target 0.50 (+1.84)
5. Focus Flow (lofi/focused)  -  Score: 1.80
     - energy 0.40 vs target 0.50 (+1.80)
```

### Experiment: genre weight halved (1.0), energy weight doubled (4.0)

```
##### EXPERIMENT: genre weight 2.0 -> 1.0, energy weight 2.0 -> 4.0 #####

=== High-Energy Pop (shifted weights): {'genre': 'pop', 'mood': 'happy', 'energy': 0.9} ===

1. Sunrise City (pop/happy)  -  Score: 5.68
     - genre match (+1.0)
     - mood match (+1.0)
     - energy 0.82 vs target 0.90 (+3.68)
2. Gym Hero (pop/intense)  -  Score: 4.88
     - genre match (+1.0)
     - energy 0.93 vs target 0.90 (+3.88)
3. Rooftop Lights (indie pop/happy)  -  Score: 4.44
     - mood match (+1.0)
     - energy 0.76 vs target 0.90 (+3.44)
4. Storm Runner (rock/intense)  -  Score: 3.96
     - energy 0.91 vs target 0.90 (+3.96)
5. Neon Overdrive (edm/energetic)  -  Score: 3.76
     - energy 0.96 vs target 0.90 (+3.76)

=== Chill Lofi (shifted weights): {'genre': 'lofi', 'mood': 'chill', 'energy': 0.4, 'valence': 0.6, 'likes_acoustic': True} ===

1. Library Rain (lofi/chill)  -  Score: 7.66
     - genre match (+1.0)
     - mood match (+1.0)
     - energy 0.35 vs target 0.40 (+3.80)
     - valence 0.60 vs target 0.60 (+1.00)
     - acousticness 0.86 fits taste (+0.86)
2. Midnight Coding (lofi/chill)  -  Score: 7.59
     - genre match (+1.0)
     - mood match (+1.0)
     - energy 0.42 vs target 0.40 (+3.92)
     - valence 0.56 vs target 0.60 (+0.96)
     - acousticness 0.71 fits taste (+0.71)
3. Focus Flow (lofi/focused)  -  Score: 6.77
     - genre match (+1.0)
     - energy 0.40 vs target 0.40 (+4.00)
     - valence 0.59 vs target 0.60 (+0.99)
     - acousticness 0.78 fits taste (+0.78)
4. Spacewalk Thoughts (ambient/chill)  -  Score: 6.39
     - mood match (+1.0)
     - energy 0.28 vs target 0.40 (+3.52)
     - valence 0.65 vs target 0.60 (+0.95)
     - acousticness 0.92 fits taste (+0.92)
5. Coffee Shop Stories (jazz/relaxed)  -  Score: 5.66
     - energy 0.37 vs target 0.40 (+3.88)
     - valence 0.71 vs target 0.60 (+0.89)
     - acousticness 0.89 fits taste (+0.89)

=== Deep Intense Rock (shifted weights): {'genre': 'rock', 'mood': 'intense', 'energy': 0.92} ===

1. Storm Runner (rock/intense)  -  Score: 5.96
     - genre match (+1.0)
     - mood match (+1.0)
     - energy 0.91 vs target 0.92 (+3.96)
2. Gym Hero (pop/intense)  -  Score: 4.96
     - mood match (+1.0)
     - energy 0.93 vs target 0.92 (+3.96)
3. Neon Overdrive (edm/energetic)  -  Score: 3.84
     - energy 0.96 vs target 0.92 (+3.84)
4. Iron Requiem (metal/angry)  -  Score: 3.80
     - energy 0.97 vs target 0.92 (+3.80)
5. Sunrise City (pop/happy)  -  Score: 3.60
     - energy 0.82 vs target 0.92 (+3.60)

=== Adversarial: Sad but Energetic (shifted weights): {'genre': 'folk', 'mood': 'sad', 'energy': 0.9} ===

1. Storm Runner (rock/intense)  -  Score: 3.96
     - energy 0.91 vs target 0.90 (+3.96)
2. Gym Hero (pop/intense)  -  Score: 3.88
     - energy 0.93 vs target 0.90 (+3.88)
3. Neon Overdrive (edm/energetic)  -  Score: 3.76
     - energy 0.96 vs target 0.90 (+3.76)
4. Iron Requiem (metal/angry)  -  Score: 3.72
     - energy 0.97 vs target 0.90 (+3.72)
5. Sunrise City (pop/happy)  -  Score: 3.68
     - energy 0.82 vs target 0.90 (+3.68)

=== Adversarial: Unknown Genre (shifted weights): {'genre': 'k-pop', 'mood': 'euphoric', 'energy': 0.5} ===

1. Velvet Hours (r&b/romantic)  -  Score: 3.96
     - energy 0.49 vs target 0.50 (+3.96)
2. Dusty Back Road (country/nostalgic)  -  Score: 3.92
     - energy 0.52 vs target 0.50 (+3.92)
3. Island Breeze (reggae/uplifting)  -  Score: 3.68
     - energy 0.58 vs target 0.50 (+3.68)
4. Midnight Coding (lofi/chill)  -  Score: 3.68
     - energy 0.42 vs target 0.50 (+3.68)
5. Focus Flow (lofi/focused)  -  Score: 3.60
     - energy 0.40 vs target 0.50 (+3.60)
```

---

## Experiments You Tried

I halved the genre weight (2.0 -> 1.0) and doubled the energy weight (2.0 -> 4.0). Each song's score is still a sum of non-negative parts, with energy closeness between 0 and the weight, so the math stays valid, but totals are no longer comparable with the original run. The top 1 song did not change for any profile except "Sad but Energetic", where the folk song lost to rock. Lower ranks reshuffled toward songs with matching energy regardless of genre (see Evaluation in the model card). The new results were more *different* than more *accurate*: they helped the energetic-but-sad user and made the pop user's list look more like a rock list. Full output is in Evaluation Output above.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



