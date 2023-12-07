import streamlit as st
import pandas as pd
import numpy as np
from collections import OrderedDict

# From: https://gist.github.com/davesteele/44793cd0348f59f8fadd49d7799bd306
class LimitedSizeList():
    """Dict with a limited length, ejecting LRUs as needed."""

    def __init__(self, *args, cache_len: int = 10, **kwargs):
        assert cache_len > 0
        self.cache_len = cache_len
        self._list = []

    def __len__(self):
        return len(self._list)
    
    def __contains__(self, key):
        for kv in self._list:
            if kv[0] == key:
                return True
        return False
    
    def __getitem__(self, key):
        return self._get_item(key)
    
    def __setitem__(self, key, value):
        self._set_item(key, value)

    def __delitem__(self, key):
        item  = self._get_item(key)
        if item:
            self._list.remove(item)

    def __iter__(self): 
        return self.list.__iter__()

    def _set_item(self, key, value):
        data = self._list

        item = self._get_item(key)
        if item in data:
           data.remove(kv)

        kv = (key, value)
        data.insert(0, kv)

        while len(data) > self.cache_len:
            data.remove(data[-1])

    def _get_item(self, key):
        val = None
        for kv in self._list:
            if kv[0] == key:
                val = kv[1]
                break
        return kv
    
    def __repr__(self):
        # convert list of key-value pairs to dict
        return repr(dict(self._list))

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🎬"
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

def save_rating(key):
    if not key in st.session_state:
        return
    
    rating = st.session_state[key]
    if rating == 0:
        if key in st.session_state.ratings:
            del st.session_state.ratings[key]
    else:
        st.session_state.ratings[key] = rating
        st.session_state[key] = rating

def render_movie_samples(sample_movies, st_parent):
    i=0                     
    for _, row in sample_movies.iterrows():
        if (i) % 3 == 0:
            div = st_parent.container() 
            cols = div.columns([2, 2, 2]) 

        col = cols[i % 3].container(border=True)
        url = f"./pages/images/{row.MovieID}.jpg"
        try:
            col.image(url, caption=row.Title)
        except:
            pass
  
        # MovieId
        MovieID = row.MovieID
        value = 0
        if MovieID in st.session_state.ratings:
            value = st.session_state.ratings[MovieID]

        # Add Slider
        col.slider(
            label='Rating',
            label_visibility ='hidden',
            min_value=0,
            max_value=5,
            value=value,
            step=1,
            key=MovieID,
            on_change=save_rating(MovieID)
        )
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

# Main code

# Initialize user ratings
if 'ratings' not in st.session_state:
    st.session_state.ratings = LimitedSizeList(cache_len=10)

# Load Movies
movies = load_movies()

# Load the data
sim = load_top_sim(movies)

# Get the movie samples
samples = get_movie_samples(sim, movies)

# Render the samples
st_movies_ratings = st.expander("Select up to 10 movies", expanded=True)
render_movie_samples(samples, st_movies_ratings)

# Get the ratings
st_top_movies = st.expander("Recommendations", expanded=True)

# Indicate number of ratings
st.sidebar.slider(
    label='You have rated',
    min_value=1,
    max_value=10,
    value=len(st.session_state.ratings),
    disabled=True,
    key='num_ratings',
)

st.sidebar.write(st.session_state.ratings)