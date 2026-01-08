import os
import requests

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


def search_movie(title):
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": title
    }

    response = requests.get(url, params=params, timeout=5)
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data["results"][0] if data.get("results") else None
    except Exception as e:
        print("TMDB error:", e)
        return None



def get_trailer(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/videos"
    params = {"api_key": TMDB_API_KEY}

    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()
    data = response.json()

    for video in data.get("results", []):
        if video["site"] == "YouTube" and video["type"] == "Trailer":
            return video["key"]

    return None
