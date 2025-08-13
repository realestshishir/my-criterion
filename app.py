import streamlit as st
import pickle
import numpy as np
import pandas as pd
import requests
import os
import nltk
import ast
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000, stop_words='english')
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
from sklearn.metrics.pairwise import cosine_similarity


API_KEY = "2edbcad2b001748a309c76768cdcce6e"  # your TMDB API key
BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="My Criterion: Movie Recommender System")

# -------------------------
# Load Movies
# -------------------------
try:
    movies_df = pickle.load(open('movies.pkl', 'rb'))
except Exception as e:
    st.error(f"Could not load 'movies.pkl': {e}")
    st.stop()

if isinstance(movies_df, pd.DataFrame) and 'title' in movies_df.columns:
    movies_titles = movies_df['title'].values
else:
    st.error("'movies.pkl' is not in the expected format.")
    st.stop()

# -------------------------
# Load Similarity Matrix
# -------------------------

if not os.path.exists("similarity.pkl"):
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies_df['tags']).toarray()
    similarity = cosine_similarity(vectors)
    with open("similarity.pkl", "wb") as f:
        pickle.dump(similarity, f)
else:
    with open("similarity.pkl", "rb") as f:
        similarity = pickle.load(f)
# -------------------------
# Load Posters Dictionary
# -------------------------
try:
    posters_dict = pickle.load(open('posters.pkl', 'rb'))
except Exception as e:
    posters_dict = {}
    st.warning(f"Could not load 'posters.pkl': {e}")

# -------------------------
# Fetch Poster Function
# -------------------------
def fetch_poster_by_title(title):
    """Get poster URL from local posters.pkl or TMDB fallback."""
    if title in posters_dict and posters_dict[title]:
        return posters_dict[title]

    search_url = f"{BASE_URL}/search/movie"
    params = {"api_key": API_KEY, "query": title}
    try:
        response = requests.get(search_url, params=params)
        data = response.json()
        if data.get("results"):
            poster_path = data["results"][0].get("poster_path")
            if poster_path:
                return POSTER_BASE + poster_path
    except Exception:
        pass
    return "https://via.placeholder.com/300x450?text=No+Image"

# -------------------------
# Recommend Function
# -------------------------
def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for idx, _ in movies_list:
        title = movies_df.iloc[idx].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster_by_title(title))

    return list(zip(recommended_movies, recommended_posters))

# -------------------------
# UI
# -------------------------
st.title('My Criterion: Movie Recommender System')

selected_movie_name = st.selectbox('Pick a movie for recommendations:', movies_titles)

if st.button('Recommend'):
    recs = recommend(selected_movie_name)
    if not recs:
        st.warning(f"No recommendations found for '{selected_movie_name}'.")
    else:
        st.subheader("Recommended Movies:")
        cols = st.columns(len(recs))
        for col, (title, poster) in zip(cols, recs):
            with col:
                st.image(poster)
                st.caption(title)
