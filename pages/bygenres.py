import streamlit as st
import pandas as pd

# Movies column_config
movies_column_config = {
    "image_url" : st.column_config.ImageColumn(label="Title",  width=None, help=None),
    "Title" : st.column_config.TextColumn(label="Title",  width=None, help=None),
}

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🎬"
)

@st.cache_data
def load_movies():
    # Movies: MovieID::Title::Genres
    movies = pd.read_csv(f'./data/movies.dat', sep='::', engine = 'python', encoding="ISO-8859-1", header = None)
    movies.columns = ['MovieID', 'Title', 'Genres']

    # Top 10 Movies for each genre
    df = pd.read_csv('./data/top10_movies.csv')
    df = df.merge(movies, on='MovieID', how='inner', suffixes=("", "_y"),)
    df.sort_values(by=['Genres', 'Rating'], inplace=True)
    
    df['image_url'] = df.apply(lambda m: f"./pages/images/{m.MovieID}.jpg", axis=1)
    return df

@st.cache_data
def get_top_movies_by_genre(df, genre):
    return df[df['Genres'] == genre]

# Load Top Movies
movies = load_movies()

# Selection
genre = st.selectbox('Select Genres', movies['Genres'].unique())

# Render recommendation
if st.button('Get Recommendations'):
    top_movies = get_top_movies_by_genre(movies, genre)
    cols = st.columns([2, 2, 2])
    i=1                           
    for _, row in top_movies.iterrows():
        if (i) % 3 == 0:
            st.write('---')
        try:
            cols[i % 3].image(f'{row.image_url}')
        except:
            pass
        cols[i % 3].write(f'{row.Title}')
        i += 1
     
    