import pickle
import requests

# Load the preprocessed movie list (DataFrame with movie_id, title, etc.)
movies = pickle.load(open('movie_list.pkl', 'rb'))

# Load the precomputed similarity matrix (cosine similarity between movies)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# OMDb API key - get yours free from https://www.omdbapi.com/apikey.aspx
OMDB_API_KEY = "6a55f5f0"


def fetch_poster(movie_title):
    """
    Fetches the poster image URL for a given movie title using the OMDb API.
    NOTE: OMDb searches by movie TITLE (not by TMDB movie_id like before),
    so we pass the title here instead of an id.
    """
    # Build the OMDb request URL using the movie title and API key
    # 't=' parameter searches OMDb by exact/closest title match
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"

    try:
        # Send GET request to OMDb API
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes (4xx/5xx)
        data = response.json()       # Parse the JSON response

        # OMDb returns Response: "False" if the movie/title is not found
        # and the poster field is sometimes "N/A" if no poster exists
        poster_url = data.get('Poster')

        if data.get('Response') == 'True' and poster_url and poster_url != 'N/A':
            # OMDb already returns a full, ready-to-use poster URL
            full_path = poster_url
        else:
            # Fallback placeholder image if movie not found or poster missing
            full_path = "https://via.placeholder.com/500x750?text=No+Poster+Available"

        return full_path

    except requests.exceptions.RequestException:
        # Handle network errors, timeouts, or invalid responses gracefully
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"


def recommend(movie_name):
    """
    Takes a movie name as input and returns the top 5 recommended
    movie names along with their poster URLs.
    """
    # Find the index of the selected movie in the movies DataFrame
    movie_index = movies[movies['title'] == movie_name].index[0]

    # Get the similarity scores of the selected movie with all other movies
    distances = similarity[movie_index]

    # Sort movies based on similarity score in descending order
    # enumerate() pairs each score with its index before sorting
    # We skip the first item (index 0) since that is the movie itself
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]  # Take only the next top 5 most similar movies

    recommended_movie_names = []  # List to store recommended movie titles
    recommended_movie_posters = []  # List to store corresponding poster URLs

    # Loop through the top 5 similar movies
    for i in movies_list:
        # Get the movie title (used directly for OMDb lookup, no movie_id needed)
        title = movies.iloc[i[0]].title

        # Fetch poster using OMDb API (searched by title)
        recommended_movie_posters.append(fetch_poster(title))

        # Add the movie title to the result list
        recommended_movie_names.append(title)

    return recommended_movie_names, recommended_movie_posters