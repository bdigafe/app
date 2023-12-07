import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Recommendation by Rating"
)

@st.cache_data
def load_top_sim(movies):
    sim = pd.read_csv('./data/top_sim.csv')
    return sim

@st.cache_data
def load_movies():
    # Movies: MovieID::Title::Genres
    movies = pd.read_csv(f'./data/movies.dat', sep='::', engine = 'python', encoding="ISO-8859-1", header = None)
    movies.columns = ['MovieID', 'Title', 'Genres']
    return movies

@st.cache_data
def get_movie_samples(sim, movies, sample_size=200):
    df = sim.copy()
    df.fillna(0, inplace=True)
    df['avg_rating'] = df.mean(axis=1)

    # Get top movies by their average rating
    df = df.sort_values(by='avg_rating', ascending=False).head(sample_size)
    
    # Merge with movies to get the movie titles
    df = df.merge(movies, on='MovieID')
    return df[['MovieID', 'Title']]

@st.cache_data
def render_movie_samples(sample_movies):
    st.markdown('## Top 10 Movies by Rating')

    cols = st.columns([2, 2, 2])
    i=1                           
    for _, row in sample_movies.iterrows():
        if (i) % 3 == 0:
            st.write('---')

        url = f"./pages/images/{row.MovieID}.jpg"
        cols[i % 3].image(url)
        cols[i % 3].write(row.Title)
        i += 1

def myIBCF(S, w, t=None):

    # Create a mask with for values w where w is a nan
    wmask = w.copy()
    wmask[wmask.isna()] = 0
    wmask[wmask != 0] = 1

    # Fill all nan values with 0
    wu = w.fillna(0)
    su = S.fillna(0)

    # Compute the weighted average of wi*si
    R = su.multiply(wu, axis=1).sum(axis=1) 
    D = su.multiply(wmask, axis=1).sum(axis=1)
    r = R/D

    # Remove movies that have already been rated
    r.loc[wu > 0] = np.nan

    # return the movie ids with the top 10 ratings
    return r.sort_values(ascending=False)

# Load Movies
movies = load_movies()

# Load the data
sim = load_top_sim(movies)

# Get the movie samples
samples = get_movie_samples(sim, movies)

# Render the samples
render_movie_samples(samples)