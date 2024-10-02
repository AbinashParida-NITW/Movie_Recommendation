import pickle
import pandas as pd
import streamlit as st
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=6aaa51a1b772c752970758a75f16596b'.format(movie_id))  # TMDB API key
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distance = similarities[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movie_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movie_poster

# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarities = pickle.load(open('similarities.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Title of the application
st.title('Movie Recommender System')

# Movie selection and recommendation
selected_movie_name = st.selectbox("Select a movie:", movies["title"].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)  # Creating 5 columns for movie posters and names

    for idx, col in enumerate(cols):
        if idx < len(names):  # Check if the column index is within the number of movies
            with col:
                st.text(names[idx])
                st.image(posters[idx])
else:
    st.write("No Suggestions available.")
