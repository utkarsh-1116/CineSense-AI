from flask import Flask, request, jsonify
from flask_cors import CORS
from recommender import recommend
from tmdb import search_movie, get_trailer


app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Movie Recommendation API is running 🚀"

@app.route("/recommend")
def recommend_api():
    movie = request.args.get("movie")
    if not movie:
        return jsonify({"error": "Movie title required"}), 400

    recommendations = recommend(movie)
    results = []

    for title in recommendations:
        data = search_movie(title)
        if not data:
            continue

        trailer_key = get_trailer(data["id"])

        results.append({
            "title": title,
            "overview": data.get("overview", ""),
            "backdrop": (
                f"https://image.tmdb.org/t/p/original{data['backdrop_path']}"
                if data.get("backdrop_path") else ""
            ),
            "trailer": trailer_key
        })

    return jsonify({
        "movie": movie,
        "results": results
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
