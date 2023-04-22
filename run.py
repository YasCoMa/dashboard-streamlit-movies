import streamlit as st
import pandas as pd
import plotly.express as px

from analysis_eda import DashboardEda
from analysis_inference import DashboardInference
from analysis_actors import DashboardActors

def run_UI():
    st.set_page_config(
        page_title="Movies Dataset Analysis",
        page_icon="🎬",
        menu_items={
            'Report a bug': "https://github.com/YasCoMa/dashboard-streamlit-movies/issues/new/choose",
            'About': """            
         If you're seeing this, we would love your contribution! If you find bugs, please reach out or create an issue on our 
         [GitHub](https://github.com/YasCoMa/dashboard-streamlit-movies) repository. If you find that this interface doesn't do what you need it to, you can create an feature request 
         at our repository or better yet, contribute a pull request of your own. 
    
         Dashboard Creator: Yasmmin Martins
        """
        }
    )
    st.sidebar.title('Movies Dataset Analysis')
    st.sidebar.write("""
            ## About
            
            This tool performs a series of exploration analysis in the movies dataset: 
            - General analysis using a world map, votes distribution and missing columns (data quality)
            - Insights inferred from data analysis about the gross, budget and overall score.  
            - Actors and movie network analysis showing the hubs (movie stars) according to the movies in a score range
            - Analysis of most successful writers and directors 
        """)
        
    movies_data_raw = pd.read_csv("https://raw.githubusercontent.com/danielgrijalva/movie-stats/7c6a562377ab5c91bb80c405be50a0494ae8e582/movies.csv")
    movies_data = movies_data_raw
    movies_data.dropna()
    
    main = st.container()
    with main:
        tab1, tab2, tab3 = st.tabs(["General metrics", "Inferences", "Actor network"])
        with tab1:
            st.header("General Analysis")
            obj = DashboardEda()
            obj.eda_UI(movies_data, movies_data_raw)
        
        with tab2:
            st.header("Inferences with variables")
            obj = DashboardInference()
            obj.inference_UI(movies_data)
        
        with tab3:
            st.header("Actors network")
            obj = DashboardActors()
            obj.actors_UI(movies_data)
        
if __name__ == '__main__':
    run_UI()    
