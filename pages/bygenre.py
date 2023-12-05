import streamlit as st
import pandas as pd

# Movies column_config
movies_column_config = {
    "image_url" : st.column_config.ImageColumn(label="Title",  width=None, help=None),
    "Title" : st.column_config.TextColumn(label="Title",  width=None, help=None),
}

st.set_page_config(
    page_title="Movie Recommender"
)

@st.cache_data
def load_movies():
    # Movies: MovieID::Title::Genres
    movies = pd.read_csv(f'./data/movies.dat', sep='::', engine = 'python', encoding="ISO-8859-1", header = None)
    movies.columns = ['MovieID', 'Title', 'Genres']

    # Top 10 Movies for each genre
    df = pd.read_csv('./data/top10_movies.csv')
    df = df.merge(movies, on='MovieID', how='inner', suffixes=("", "_y"),)
    
    df['image_url'] = df.apply(lambda m: f'<a href="./images/{m.MovieID}.jpg">{m.Title}</a>', axis=1)
    return df

@st.cache_data
def get_top_movies_by_genre(df, genre):
    return df[df['Genres'] == genre]

# Load Top Movies
movies = load_movies()

# Title
st.header('Movie Recommender')

# Selection
st.subheader('Step 1: Select a Genre')
genre = st.selectbox('', movies['Genres'].unique())

# Button to trigger the recommendation
st.subheader('Step 2: Click to get your recommendations')

# Render recommendation
if st.button('Get Recommendations'):
    top_movies = get_top_movies_by_genre(movies, genre)
    for i, row in top_movies.iterrows():
        st.image(f'{row["image_url"]}')
        st.write(f'{row["Title"]}')
        st.write('---')
     
    