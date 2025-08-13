# My Criterion – Movie Recommender System

**My Criterion** is a content-based movie recommender system trained on the TMDB dataset.  
It suggests movies similar to the one you select, using textual content analysis (e.g., genres, descriptions, keywords).  
The app is built with **Streamlit** for an interactive and easy-to-use interface.

---

## Features
- **Content-based recommendations** – Suggests movies similar to your choice.
-  **Streamlit UI** – Simple, interactive, and responsive.
-  **Movie Posters** – Automatically fetches posters from TMDB.
-  **Fast & Lightweight** – Works locally without a heavy backend.

---

## How to run it?

### 1. Clone the Repository

### 2. Install Dependencies

Make sure you have Python 3.9+ installed, then run:

pip install -r requirements.txt

### 3. Run the Application

streamlit run app.py

Your browser will open at: http://localhost:8501



## How It Works

1. Loads a dataset of movies from TMDB.

2. Uses content-based filtering with CountVectorizer and cosine similarity.

3. Finds movies most similar to the selected one.

4. Displays recommendations with movie posters.


## Dataset
The project uses The Movie Database (TMDB) dataset.
You will need a TMDB API key to fetch additional posters or update the dataset.
Get your API key from: https://www.themoviedb.org/

## License
This project is licensed under the MIT License – feel free to modify and share.


## Acknowledgments
 
Streamlit – For building the web UI.
TMDB – For movie data and posters.
scikit-learn – For vectorization and similarity calculations.




