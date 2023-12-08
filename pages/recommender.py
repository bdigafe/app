import streamlit as st
import pandas as pd
import numpy as np
import json

DEBUG = False

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
        kv  = self._get_item(key)
        if kv is not None:
            return True
        
        return False
    
    def __getitem__(self, key):
        kv = self._get_item(key)
        if not kv is None:
            return kv[1]
        return None
    
    def __setitem__(self, key, value):
        self._set_item(key, value)

    def __delitem__(self, key):
        item  = self._get_item(key)
        if item in self._list:
            self._list.remove(item)

    def __iter__(self): 
        return self._list.__iter__()
    
    def _set_item(self, key, value):

        item = self._get_item(key)
        if not item is None:
           self._list.remove(item)

        kv = (key, value)
        self._list.insert(0, kv)

        while len(self._list) > self.cache_len:
            self._list.remove(self._list[-1])

    def _get_item(self, key):
        kv = None
        for kv in self._list:
            if kv[0] == key:
                return kv
    
        return None
    
    def to_dict(self):
        kv = {}
        for i in range(len(self._list)):
            kv[self._list[i][0]] = self._list[i][1]
        return kv
    
    def __repr__(self):
        kv = self.to_dict()
        return json.dumps(kv, indent=4)

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🎬"
)
  
@st.cache_data
def load_top_sim(movies):
    sim = pd.read_csv('./data/top_sim.csv')
    sim.set_index('MovieID', inplace=True)
    return sim

@st.cache_data
def load_movies():
    # Movies: MovieID::Title::Genres
    movies = pd.read_csv(f'./data/movies.dat', sep='::', engine = 'python', encoding="ISO-8859-1", header = None)
    movies.columns = ['MovieID', 'Title', 'Genres']
    return movies

@st.cache_data
def get_movie_samples(sim, movies, sample_size=200):
     # MovieID,Title, Genres, Rating
    sample_movies = pd.read_csv(f'./data/sample_movies.csv', sep=',')
    sample_movies.columns = ['MovieID', 'Title', 'Genres', 'Rating']
    return sample_movies[['MovieID', 'Title', 'Genres']]

def save_rating(key):
    if not key in st.session_state:
        return
    
    rating = st.session_state[key]
    if rating == 0:
        if st.session_state.ratings[key] != None:
            del st.session_state.ratings[key]
    else:
        st.session_state.ratings[int(key)] = rating
    
    st.session_state[key] = rating       

def render_movie_samples(sample_movies, st_parent):
    i=0                     
    for _, row in sample_movies.iterrows():
        if (i) % 3 == 0:
            div = st_parent.container() 
            cols = div.columns([2, 2, 2]) 

        col = cols[i % 3].container(border=True)
        col_image, col_rating= col.columns([1, 1])
 
        # Image
        url = f"./pages/images/{row.MovieID}.jpg"
        try:
            col_image.image(url, width=185)
        except:
            pass
  
        # Title, Genres, and rating
        col_rating.write(f"Title: {row.Title}")
        col_rating.write(f"Genres: {row.Genres}")


        MovieID = row.MovieID
        value = 0
        if MovieID in st.session_state.ratings:
            value = st.session_state.ratings[MovieID]

        # Add Slider
        col_rating.write(f"Your Rating")
        col_rating.slider(
            label=':red[Rating]',
            label_visibility ='hidden',
            min_value=0,
            max_value=5,
            value=value,
            step=1,
            key=MovieID,
            on_change=save_rating,
            args=(row.MovieID, )
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
    r[wu.iloc[:,0] > 0] = np.nan

    # return the movie ids with the top 10 ratings
    return r.sort_values(ascending=False)

def get_user_recommendations(user_ratings, sim):
    # Setup weights matrix
    w = sim.index.to_frame()
    w["Rating"] = np.nan
    w.set_index('MovieID', inplace=True)

    # Add user ratings to the weights matrix
    for k, v in user_ratings.to_dict().items():
        w.loc[k] = v

    # Compute the weighted average of wi*m
    r = myIBCF(sim, w)

    return r 

def render_user_recommendations(r, movies, st_parent):
    # Join with movies to get the movie titles
    r = r.head(10)
    r = r.to_frame()
    r.columns = ['Rating']
    r = r.merge(movies, on='MovieID', how='inner', suffixes=("", "_y"),)
    r.sort_values(by=['Rating'], inplace=True, ascending=False)

    cols = st_parent.columns([2, 2, 2])
    i=1                           
    for _, row in r.iterrows():
        if (i) % 3 == 0:
            st.write('---')
        try:
            cols[i % 3].image(f"./pages/images/{row.MovieID}.jpg")
        except:
            pass
        cols[i % 3].write(f'{row.Title}')
        i += 1

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
st.subheader("Movie recommendations based on your ratings")
st.markdown("Rate the movies below and click on the recommendation tab to get your recommendations.")

tab1, tab2 = st.tabs(["Step 1: Your ratings", "Step 2: Recommendation"])
if not DEBUG:
    render_movie_samples(samples, tab1)
else:
    # debugging
    ratings = LimitedSizeList(cache_len=10)
    ratings[3952] = 5
    ratings[3951] = 4
    ratings[3950] = 3
    r = get_user_recommendations(ratings, sim)

# Get the ratings
if len(st.session_state.ratings) > 5:
    if st.button('Get Recommendations'):
        # Convert ratings to a dataframe
        r = get_user_recommendations(st.session_state.ratings, sim)
        render_user_recommendations(r, movies, tab2)

# Indicate number of ratings
st.sidebar.markdown(f"#### You rated :red[{len(st.session_state.ratings)}] movies out of 10.")
if st.sidebar.button('Clear ratings'):
    for k in st.session_state.ratings:
        st.session_state[k] = 0
    st.session_state.ratings = LimitedSizeList(cache_len=10)
    st.rerun()

# Styling
st.markdown("""
<style>
	.stTabs [data-baseweb="tab-panel"] {
		height: 600px;
        overflow-y: scroll;
    }

</style>""", unsafe_allow_html=True)