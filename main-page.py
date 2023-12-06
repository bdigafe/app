import streamlit as st
from st_pages import Page, add_page_title, show_pages, show_pages_from_config

st.set_page_config(
    page_title="Home",
    layout="wide",
    initial_sidebar_state="expanded",
)

show_pages(
    [
        Page("main-page.py", "Home", "🏠"),
        Page("pages/bygenre.py", "By Genre", "🎬"),
        Page("pages/recommender.py", "By Rating", "🎬"),
    ]
)


show_pages_from_config()

st.markdown("""
    ## Movie Recommendation Demo
            
    This is a demo of a movie recommendation system.
    The data used in this demo is from the [MovieLens](https://grouplens.org/datasets/movielens/) dataset. The demo is built using [Streamlit](https://streamlit.io/).
            
    ### How to use this demo?
            
    #### Option 1: Select a Genre and get your recommendations.
    
    1. Select a genre from the dropdown on the left.
    2. Click the button to get your recommendations.
            
    #### Option 2: Rate a movie and get your recommendations.
            
    1. Rate few movies 
    2. Click the button to get your recommendations.  
    """)