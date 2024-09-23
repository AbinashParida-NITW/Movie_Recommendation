import pickle
import pandas as pd
import streamlit as st
import requests
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase initialization check and setup
if not firebase_admin._apps:
    cred = credentials.Certificate('movie-recommend-4e602-firebase-adminsdk-xhaf5-db5cae781e.json')  # actual path
    firebase_admin.initialize_app(cred)

# Initialize Firestore DB
db = firestore.client()

# Firebase configuration for REST API Authentication

def firebase_auth_login(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_config['apiKey']}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        st.sidebar.error("Login failed. Please check your credentials and try again.")
        return None

def firebase_auth_register(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={firebase_config['apiKey']}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        st.sidebar.error("Registration failed. Please try again.")
        return None

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=6aaa51a1b772c752970758a75f16596b'.format(movie_id))  #  TMDB API key
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

# Sidebar for User Authentication
st.sidebar.title("Authentication")
auth_option = st.sidebar.selectbox("Choose an option", ["Login", "Register"])

email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

if auth_option == "Login":
    if st.sidebar.button("Login"):
        user = firebase_auth_login(email, password)
        if user:
            st.sidebar.success("Logged in successfully!")
            st.session_state['user'] = user  # Store user session

elif auth_option == "Register":
    if st.sidebar.button("Register"):
        user = firebase_auth_register(email, password)
        if user:
            st.sidebar.success("Registration successful! You can now log in.")
        else:
            st.sidebar.error("Registration failed. Please try again.")

# Check if user is logged in
if 'user' not in st.session_state:
    st.warning("Please log in or Register to use the recommender system.")
else:
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
