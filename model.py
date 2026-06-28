import pandas as pd
import pickle
import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------------
# Load processed dataset
# -----------------------------------

DATA_PATH = r"C:\Users\RISHIKA\Movie Recommendation System\main project\processed_movies.csv"

movies = pd.read_csv(DATA_PATH)

# -----------------------------------
# Convert text into vectors
# -----------------------------------

cv = CountVectorizer(
    max_features=5000,
    stop_words="english"
)

vectors = cv.fit_transform(movies["tags"]).toarray()

# -----------------------------------
# Calculate similarity
# -----------------------------------

similarity = cosine_similarity(vectors)

# -----------------------------------
# Save files
# -----------------------------------

SAVE_PATH = r"C:\Users\RISHIKA\Movie Recommendation System\main project"

pickle.dump(
    movies,
    open(os.path.join(SAVE_PATH, "movie_list.pkl"), "wb")
)

pickle.dump(
    similarity,
    open(os.path.join(SAVE_PATH, "similarity.pkl"), "wb")
)

# -----------------------------------
# Recommendation Function
# -----------------------------------

def recommend(movie_name):

    movie_name = movie_name.lower()

    movies["title_lower"] = movies["title"].str.lower()

    if movie_name not in movies["title_lower"].values:
        print("Movie not found!")
        return

    index = movies[movies["title_lower"] == movie_name].index[0]

    distances = list(enumerate(similarity[index]))

    distances = sorted(
        distances,
        reverse=True,
        key=lambda x: x[1]
    )

    print("\nTop 5 Recommended Movies:\n")

    for movie in distances[1:6]:
        print(movies.iloc[movie[0]].title)

print("Model created successfully!")

recommend("Avatar")