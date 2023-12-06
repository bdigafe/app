import streamlit as st

st.set_page_config(
    page_title="Movie Recommendation Demo"
)

st.markdown("""
    ## Movie Recommendation Demo
            
    This is a demo of a movie recommendation system.
    The data used in this demo is from the [MovieLens](https://grouplens.org/datasets/movielens/) dataset.
    
    The demo is built using [Streamlit](https://streamlit.io/).
            
    ### How to use this demo?
            
    #### Option 1: Select a Genre and get your recommendations.
    
    1. Select a genre from the dropdown on the left.
    2. Click the button to get your recommendations.
    3. Enjoy!
            
    #### Option 2: Rate a movie and get your recommendations.
    1. Rate few movies 
    2. Click the button to get your recommendations.
            
    """)