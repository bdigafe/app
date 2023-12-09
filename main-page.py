import streamlit as st
from st_pages import Page, Section, add_page_title, show_pages

st.set_page_config(
    page_title="Home",
    layout="wide",
    initial_sidebar_state="expanded",
)

show_pages(
    [
        Page("main-page.py", "Home", "🏠"),
        Page("pages/bygenres.py", "Recommender By Genre"),
        Page("pages/recommender.py", "Recommender By Rating"),
        Section("", )
    ]
)

st.markdown("""
    ## Movie Recommendation Demo
            
    This is a demo of a movie recommendation system.
    The data used in this demo is from the [MovieLens](https://grouplens.org/datasets/movielens/) dataset. The demo is built using [Streamlit](https://streamlit.io/).
            
    ### How to use this demo?
            
    #### Option 1: Select a genre and get your recommendations.
    
    1. Select a genres from the dropdown on the left.
    2. Click the button to get your recommendations.
            
    #### Option 2: Rate some movies and get your recommendations.
            
    1. Rate up to 10 movies. You must rate at least 5 movies.
    2. Click the button to get your recommendations.  
    """)