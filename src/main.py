"""
Command line runner for the Music Recommender Simulation.

Runs the recommender for several taste profiles (including adversarial
ones) and then repeats them with shifted weights as a sensitivity experiment.
"""

from src import recommender
from src.recommender import load_songs, recommend_songs

PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.4,
                   "valence": 0.6, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92},
    # Adversarial: conflicting preferences (high energy but sad mood)
    "Adversarial: Sad but Energetic": {"genre": "folk", "mood": "sad", "energy": 0.9},
    # Adversarial: genre and mood that do not exist in the catalog
    "Adversarial: Unknown Genre": {"genre": "k-pop", "mood": "euphoric", "energy": 0.5},
}


def show(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Prints the top k recommendations for one profile."""
    print(f"=== {name}: {user_prefs} ===\n")
    for rank, (song, score, explanation) in enumerate(recommend_songs(user_prefs, songs, k), start=1):
        print(f"{rank}. {song['title']} ({song['genre']}/{song['mood']})  -  Score: {score:.2f}")
        for reason in explanation.split("; "):
            print(f"     - {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    for name, prefs in PROFILES.items():
        show(name, prefs, songs)

    # Experiment: halve genre weight, double energy weight
    print("##### EXPERIMENT: genre weight 2.0 -> 1.0, energy weight 2.0 -> 4.0 #####\n")
    recommender.GENRE_POINTS = 1.0
    recommender.ENERGY_POINTS = 4.0
    for name, prefs in PROFILES.items():
        show(name + " (shifted weights)", prefs, songs)


if __name__ == "__main__":
    main()
