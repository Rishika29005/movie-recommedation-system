import streamlit as st
import pickle
from helper import recommend

# -----------------------------
# Load saved files
# -----------------------------

movies = pickle.load(open("movie_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(page_title="Movie Recommendation System")

st.title("🎬 Movie Recommendation System")

movie_list = movies["title"].values

selected_movie = st.selectbox(
    "Select a Movie",
    movie_list
)
if st.button("Recommend"):

    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    st.subheader("Recommended Movies")

    # Create 5 equal columns to display movies side by side
    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]

    # Loop through all 5 recommendations and show name + poster in each column
    for col, name, poster in zip(columns, recommended_movie_names, recommended_movie_posters):
        with col:
            st.text(name)           # Movie name
            st.image(poster)        # Movie poster image