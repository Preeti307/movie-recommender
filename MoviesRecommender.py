
# import streamlit as st
# import pickle
# import pandas as pd
# import requests

# # Load data
# movies = pickle.load(open('movies.pkl', 'rb'))

# # Load similarity
# similarity = pickle.load(open('similarity.pkl', 'rb'))

# # 🔥 OMDb API function (poster fetch)
# def fetch_poster(movie_name):
#     api_key = "d219815b"
#     url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    
#     data = requests.get(url).json()
#     print(data)   # 👈 DEBUG

#     if data['Response'] == 'True':
#         return data['Poster']
#     else:
#         return "https://via.placeholder.com/300x450?text=No+Image"

# # 🔥 Recommendation function (updated)
# def recommend(movie):
#     index = movies[movies['title'] == movie].index[0]
#     distances = similarity[index]
    
#     movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

#     recommended_movies = []
#     recommended_posters = []

#     for i in movie_list:
#         movie_title = movies.iloc[i[0]].title
        
#         recommended_movies.append(movie_title)
#         recommended_posters.append(fetch_poster(movie_title))

#     return recommended_movies, recommended_posters

# # 🎨 UI
# st.title("🎬 Movie Recommender System")

# selected_movie = st.selectbox(
#     "Select a movie",
#     movies['title'].values
# )

# # 🔥 Button click
# if st.button('Recommend'):
#     names, posters = recommend(selected_movie)

#     col1, col2, col3, col4, col5 = st.columns(5)

#     with col1:
#         st.image(posters[0])
#         st.caption(names[0])

#     with col2:
#         st.image(posters[1])
#         st.caption(names[1])

#     with col3:
#         st.image(posters[2])
#         st.caption(names[2])

#     with col4:
#         st.image(posters[3])
#         st.caption(names[3])

#     with col5:
#         st.image(posters[4])
#         st.caption(names[4])


import os
import requests
import streamlit as st
import pickle
import pandas as pd

# 🔥 Google Drive File ID
file_id = "1jeYgyI8hEg2xXU8KzrH938WweQYk6fGK"

# 🔥 Function to download large file properly
def download_file():
    URL = "https://drive.google.com/uc?export=download"
    session = requests.Session()

    response = session.get(URL, params={'id': file_id}, stream=True)

    # Handle large file confirmation
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            params = {'id': file_id, 'confirm': value}
            response = session.get(URL, params=params, stream=True)

    with open("similarity.pkl", "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

# 🔥 Download file only if not exists
if not os.path.exists("similarity.pkl"):
    download_file()

# 🔥 Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# 🔥 OMDb API function (poster fetch)
def fetch_poster(movie_name):
    api_key = "d219815b"
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"

    data = requests.get(url).json()

    if data.get('Response') == 'True':
        return data.get('Poster')
    else:
        return "https://via.placeholder.com/300x450?text=No+Image"

# 🔥 Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_title))

    return recommended_movies, recommended_posters

# 🎨 UI
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

# 🔥 Button click
if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0])
        st.caption(names[0])

    with col2:
        st.image(posters[1])
        st.caption(names[1])

    with col3:
        st.image(posters[2])
        st.caption(names[2])

    with col4:
        st.image(posters[3])
        st.caption(names[3])

    with col5:
        st.image(posters[4])
        st.caption(names[4])