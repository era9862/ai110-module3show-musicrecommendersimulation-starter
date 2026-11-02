import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: Optional[float] = None

GENRE_POINTS = 2.0
MOOD_POINTS = 1.0
ENERGY_POINTS = 2.0
VALENCE_POINTS = 1.0
ACOUSTIC_POINTS = 1.0


def _profile_to_prefs(user: UserProfile) -> Dict:
    """Converts a UserProfile into the prefs dict used by score_song."""
    prefs = {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
    }
    if user.target_valence is not None:
        prefs["valence"] = user.target_valence
    return prefs


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs for the user, best match first."""
        prefs = _profile_to_prefs(user)
        ranked = sorted(self.songs, key=lambda s: score_song(prefs, asdict(s))[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explains in one string why the song matches the user."""
        _, reasons = score_song(_profile_to_prefs(user), asdict(song))
        return "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Reads the songs CSV into a list of dicts with numeric fields converted."""
    int_fields = ("id", "tempo_bpm")
    float_fields = ("energy", "valence", "danceability", "acousticness")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for key in int_fields:
                row[key] = int(row[key])
            for key in float_fields:
                row[key] = float(row[key])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores one song against user prefs and returns (score, reasons)."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        score += GENRE_POINTS
        reasons.append(f"genre match (+{GENRE_POINTS:.1f})")
    if song["mood"] == user_prefs.get("mood"):
        score += MOOD_POINTS
        reasons.append(f"mood match (+{MOOD_POINTS:.1f})")

    if "energy" in user_prefs:
        pts = ENERGY_POINTS * (1 - abs(song["energy"] - user_prefs["energy"]))
        score += pts
        reasons.append(f"energy {song['energy']:.2f} vs target {user_prefs['energy']:.2f} (+{pts:.2f})")

    if "valence" in user_prefs:
        pts = VALENCE_POINTS * (1 - abs(song["valence"] - user_prefs["valence"]))
        score += pts
        reasons.append(f"valence {song['valence']:.2f} vs target {user_prefs['valence']:.2f} (+{pts:.2f})")

    if "likes_acoustic" in user_prefs:
        target = 1.0 if user_prefs["likes_acoustic"] else 0.0
        pts = ACOUSTIC_POINTS * (1 - abs(song["acousticness"] - target))
        score += pts
        reasons.append(f"acousticness {song['acousticness']:.2f} fits taste (+{pts:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song, then returns the top k as (song, score, explanation)."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
