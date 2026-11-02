# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

---

## 2. Intended Use  

**Goal:** Suggest the top 5 songs from a small catalog that match a user's favorite genre, mood and energy level.

**Intended use:**
- Classroom exploration of how a content-based recommender works.
- Showing *why* a song was picked, using the reasons printed with each score.

**Not intended for:**
- Real users or a real music app. The catalog has only 18 songs.
- Judging songs or artists.
- Learning from listening history. It has no memory of what anyone played.

**Assumptions:** The user has one stable taste and can describe it with a genre, a mood and an energy number.

---

## 3. How the Model Works  

The recommender compares every song in the catalog to a simple taste profile (favorite genre, favorite mood, and a target energy level) and gives each song a score out of about 5 points.

- A song earns **2 points** if its genre matches the user's favorite genre and **1 point** if its mood matches.
- For energy, the song earns up to **2 points** based on how *close* its energy is to the user's target. A song with exactly the target energy gets the full 2 points, and the further away it is, the fewer points it gets. Higher energy is not automatically better.
- If the profile also includes a target valence (how positive the song sounds) or a preference for acoustic music, closeness on those earns up to 1 extra point each.

Every point is recorded with a short reason, such as "genre match (+2.0)", so each recommendation can be explained. The songs are then sorted from highest to lowest score and the top few are shown. The scoring step judges one song at a time, and the ranking step puts all the judged songs in order.

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

- The catalog has **18 songs** in `data/songs.csv`. I added 8 to the 10 starter songs.
- Each song has: genre, mood, energy, tempo (BPM), valence, danceability and acousticness.
- Genres include pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip hop, classical, country, EDM, R&B, metal, reggae and folk.
- **Limits:** Most genres have only one song. The songs are made up, with no lyrics, language, artist popularity or listening data. Tempo is not used in scoring.

---

## 5. Strengths  

- Works well for clear tastes like "chill lofi" or "intense rock". The top results matched my intuition.
- Closeness scoring on energy puts quiet songs first for quiet-music fans and loud songs first for loud-music fans.
- Every result comes with reasons, so it is easy to see why a song ranked where it did.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly.

The biggest weakness I found is that the system trusts labels exactly as written. For the "Sad but Energetic" profile (folk, mood "sad", energy 0.9), no song in the catalog has the mood "sad", so the mood point was never awarded to anyone. The top result was a quiet, low-energy folk song (energy 0.31) because genre alone gave it 2 points, even though the user asked for very energetic music. Similarly, "chill" and "relaxed" count as unrelated moods, even though they sound alike. The catalog is also tiny, with one song for most genres, so a user whose favorite genre appears once can get only one genre-matched recommendation. A user with conflicting tastes (sad and energetic) is effectively served only by whichever signal the weights favor.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected.

I tested five profiles: **High-Energy Pop**, **Chill Lofi**, **Deep Intense Rock**, and two adversarial ones, **Sad but Energetic** (folk, "sad", energy 0.9) and **Unknown Genre** (k-pop, "euphoric", energy 0.5). The full terminal output for each is in the README under Evaluation Output.

**Does it feel right?** Mostly yes. Chill Lofi returned the two lofi/chill tracks, then a lofi "focused" track, an ambient chill track and a relaxed jazz track, which is how I would build a study playlist. Deep Intense Rock put the rock track first, which is correct.

**What surprised me:** Gym Hero (a pop track with an "intense" mood) is second for Happy Pop users. It is not happy, but it is pop (+2 points) and has very high energy, so it scores well on two of the three checks. The system never asks whether a song *feels* happy, only whether its labels match, and a genre match is worth twice a mood match. That is why a workout song keeps appearing for people who only wanted happy pop. It also shows up for the rock profile, because "intense" matches and its energy is close.

**Comparing profiles**
- *High-Energy Pop vs Chill Lofi:* Pop gives pop, indie pop and high-energy tracks; Lofi gives quiet, acoustic tracks. The two lists share no songs, because energy and acousticness point in opposite directions. That is the intended behavior.
- *High-Energy Pop vs Deep Intense Rock:* Both want very high energy, so Gym Hero, Neon Overdrive and Storm Runner appear in both. The first place changes (Sunrise City vs Storm Runner) because of the genre and mood points. Energy decides who is *eligible* and genre and mood decide who is *first*.
- *Chill Lofi vs Deep Intense Rock:* These are opposites, with no overlap. Lofi scores are higher (about 6.8 vs 5.0) only because that profile also asks about valence and acousticness, which add extra points, so scores should not be compared across profiles.
- *Sad but Energetic vs Deep Intense Rock:* Both end up with high-energy songs in 2nd to 5th place (Storm Runner, Gym Hero, Neon Overdrive, Iron Requiem). The sad profile gets the quiet folk song first only because of the genre bonus. The conflict is resolved by the genre label, not by what the user wanted.
- *Unknown Genre vs the others:* With no genre or mood matches possible, the list is decided by energy alone, and the scores are all close (1.80 to 1.98). The system still returns confident-looking results when it has nothing to go on.

**Weight experiment (genre 2.0 -> 1.0, energy 2.0 -> 4.0):** The #1 song stayed the same for Pop, Lofi, Rock and Unknown Genre. For Sad but Energetic it changed from the folk song to Storm Runner, which fits the user's stated energy better. Lower ranks mostly reshuffled toward energy matches, such as Rooftop Lights moving closer to Gym Hero for the pop profile. Overall the change made the results different, not clearly better: it fixed the adversarial case but gave up some genre loyalty for everyone else.

---

## 8. Future Work  

1. Treat similar moods as partial matches (for example "chill" and "relaxed") instead of all-or-nothing.
2. Add more songs, so each genre has several, and add tempo to the score.
3. Re-rank the top list so it is not all the same genre, and let a user list more than one favorite genre or mood.

---

## 9. Personal Reflection

**Biggest learning moment:** A recommender can look smart with very simple rules. Seeing "Gym Hero" show up for happy-pop fans showed me that a label match can beat what a song actually feels like. The weights are choices, and each one decides who gets served well.

**AI tools:** An AI assistant helped with the code, the extra songs and the first draft of the write-ups, which saved a lot of time. I still had to check its work. The starter `main.py` import failed under `python -m src.main` until it was fixed. Pytest wasn't installed, so the tests were checked by hand. I also had to check that claims in these docs matched the real terminal output, for example score ranges. *(Edit this section so it describes your own experience in your own words.)*

**What surprised me:** Adding up a few points and sorting them already feels like a recommendation. The results sound reasonable even though the system understands nothing about music. It can also fail quietly. A profile with an unknown genre still returned five confident-looking songs.

**What I would try next:** Use partial mood matches, add tempo and danceability to the score, grow the catalog, and test profiles with two tastes at once.
