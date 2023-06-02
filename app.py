import streamlit as st
import pickle
import pandas as pd

table = pd.read_pickle('table.pkl')
ratings = pd.read_pickle('ratings.pkl')

def recommend(movie, min_rating_count = 50):
    user_rating = table[movie]
    similar_movies = table.corrwith(user_rating)
    corr_movies = pd.DataFrame(similar_movies, columns=['Correlation'])
    corr_movies.dropna(inplace=True)
    corr_movies = corr_movies.join(ratings['rating_numbers'], how='left', lsuffix='_left', rsuffix='_right')
    final = corr_movies[corr_movies['rating_numbers'] > min_rating_count].sort_values('Correlation', ascending=False)
    return final.iloc[1:6]

movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
st.title('Movie Recommendation System')

movie_name = st.selectbox(
    "Select the movie you want recommendations for. Or search its name in the search bar",
    movies['title'].unique()
)

if st.button('Recommend'):
    recommendation = recommend(movie_name)
    for i in recommendation.index:
        st.write(i)