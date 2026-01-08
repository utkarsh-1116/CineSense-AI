import pickle
import os
from difflib import get_close_matches


#absolute path to project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ML_DIR = os.path.join(BASE_DIR, "..", "ml")

model_path = os.path.join(ML_DIR, "model.pkl")
movies_path = os.path.join(ML_DIR, "movies.pkl")

similarity = pickle.load(open(model_path, "rb"))
movies = pickle.load(open(movies_path, "rb"))

def recommend(movie_title, n=5):
    movie_title = movie_title.strip().lower()

    all_titles = movies['title'].str.lower().tolist()

    # Prefer titles with digits if input has digits
    if any(char.isdigit() for char in movie_title):
        candidate_titles = [
            t for t in all_titles if any(char.isdigit() for char in t)
        ]
    else:
        candidate_titles = all_titles

    # Exact match
    if movie_title in candidate_titles:
        matched_title = movie_title
    else:
        close_matches = get_close_matches(
            movie_title,
            candidate_titles,
            n=1,
            cutoff=0.75
        )

        if not close_matches:
            return ["Movie not found"]

        matched_title = close_matches[0]

    idx = movies[movies['title'].str.lower() == matched_title].index[0]
    print("Matched movie:", movies.iloc[idx].title)

    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    recommendations = []
    for i in scores[1:n+1]:
        recommendations.append(movies.iloc[i[0]].title)

    return recommendations


if __name__ == "__main__":
    print(recommend("terminator"))
