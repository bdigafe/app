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

DEF_GRID_COLS = 2

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

def render_movies(r, st_parent):

    # Determine the number of columns per row
    grid_cols = def_grid_cols


    cols = st_parent.columns([2] * grid_cols)
    i=1                           
    for _, row in r.iterrows():
        col = cols[i % grid_cols].container(border=True)
        col_image, col_rating= col.columns([1, 1])
 
        # Image
        url = f"./pages/images/{row.MovieID}.jpg"
        try:
            col_image.image(url, width=185)
        except:
            pass
  
        # Title, Genres, and rating
        col_rating.write(f":bold[{row.Title}]")
        col_rating.write(f":bold[{row.Genres}]")
    
        i+=1

# Load Top Movies
movies = load_movies()

# Selection
genre = st.selectbox('Select Genres from the list', movies['Genres'].unique())

# Render recommendation
if st.button('Get Recommendations'):
    top_movies = get_top_movies_by_genre(movies, genre)
    div = st.container(border=False)
    render_movies(top_movies, div)
   
     
# Styling
st.markdown("""
<style>
	.stTabs [data-baseweb="tab-panel"] {
		height: 600px;
        overflow: scroll;
        scrollbar-width: auto;
    }
            
    .block-container {
        padding-top: 2rem;
    }

</style>""", unsafe_allow_html=True)