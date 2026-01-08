import pandas as pd
import ast
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Get current file directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build absolute paths
movies_path = os.path.join(BASE_DIR, "tmdb_5000_movies.csv")
credits_path = os.path.join(BASE_DIR, "tmdb_5000_credits.csv")

# Load datasets
movies = pd.read_csv(movies_path)
credits = pd.read_csv(credits_path)


#merge datasets
movies = movies.merge(credits, on="title")

movies = movies[['title', 'overview', 'genres', 'keywords', 'cast', 'crew']]


def extract_names(text):
    """Extract 'name' from list of dictionaries"""
    return [i['name'] for i in ast.literal_eval(text)]

def extract_cast(text):
    """Extract top 3 cast members"""
    cast_list = []
    for i in ast.literal_eval(text)[:3]:
        cast_list.append(i['name'])
    return cast_list

def extract_director(text):
    """Extract director from crew"""
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            return [i['name']]
    return []

movies['genres'] = movies['genres'].apply(extract_names)
movies['keywords'] = movies['keywords'].apply(extract_names)
movies['cast'] = movies['cast'].apply(extract_cast)
movies['crew'] = movies['crew'].apply(extract_director)

movies['overview'] = movies['overview'].fillna('')

movies['tags'] = (
    movies['overview'] +
    movies['genres'].apply(lambda x: " ".join(x)) + ' ' +
    movies['keywords'].apply(lambda x: " ".join(x)) + ' ' +
    movies['cast'].apply(lambda x: " ".join(x)) + ' ' + 
    movies['crew'].apply(lambda x: " ".join(x))
)

final_df = movies[['title', 'tags']]


#Tf- Idf vectorizer
vectorizer = TfidfVectorizer(
    max_features=5000,
    stop_words='english'
)

#train vector on movie tags
vectors = vectorizer.fit_transform(final_df['tags'])

#compute cosine similarity
similarity = cosine_similarity(vectors)



ML_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(ML_DIR, "model.pkl")
vectorizer_path = os.path.join(ML_DIR, "vectorizer.pkl")
movies_path = os.path.join(ML_DIR, "movies.pkl")

with open(model_path, "wb") as f:
    pickle.dump(similarity, f)

with open(vectorizer_path, "wb") as f:
    pickle.dump(vectorizer, f)

with open(movies_path, "wb") as f:
    pickle.dump(final_df, f)

print("✅ Model trained and files saved.")
