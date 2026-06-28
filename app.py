import streamlit as st
import pickle
import pandas as pd 
import requests

def fetch_poster(movie_id):
    response =requests.get('https://api.themoviedb.org/3/movie/{}?api_key=75b297304e0117813c8d470feb3ba9b5&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']


def recommend(movie):
    movie_index = movies[movies['original_title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)),reverse=True, key=lambda x:x[1])[1:6]

    recommend_movies = []
    recommend_movies_poster =[]
    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        
        recommend_movies.append(movies.iloc[i[0]].original_title)

# fetch poster from API

        recommend_movies_poster.append(fetch_poster(movie_id))
    return recommend_movies,recommend_movies_poster
    
movie_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movie_dict)

import os
import gdown
import pickle
import streamlit as st

# 1. Aapki file ID bilkul sahi hai
file_id = '1nO1yScW3avi5dMnHP4rCjCz-RNz9rfVs'
output = 'similarity.pkl'

# 2. Agar file nahi hai, toh download karenge
if not os.path.exists(output):
    with st.spinner("Recommendation engine load ho raha hai... Isme 1-2 minute lag sakte hain, please wait!"):
        try:
            # Yeh gdown ka sabse naya aur full-proof tarika hai file ID se download karne ka
            gdown.download(id=file_id, output=output, quiet=False)
        except Exception as e:
            st.error(f"Model download karne mein dikkat aayi: {e}")
            st.info("Please check karein ki aapka Google Drive link 'Anyone with the link' par set hai ya nahi.")

# 3. Model ko load karo
if os.path.exists(output):
    similarity = pickle.load(open(output, 'rb'))
else:
    st.error("Similarity file download nahi ho paayi. App aage nahi chal sakti.")

st.title('Movie Recommender System by Anmol kumar sharma')


selected_movie_name = st.selectbox(
    'How would you like to be contactend?',
movies['original_title'].values)


if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
