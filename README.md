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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

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



