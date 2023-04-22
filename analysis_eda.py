import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

class DashboardEda:
    def format(self, v):
        return "{:.2f}".format(v)    
    
    def sec1_mapCountMovies(self, moviedb):
        cc={}
        df=pd.read_csv('coord_countries.tsv', sep='\t')
        for i in df.index:
            cc[ df.iloc[i, 3] ] = [ df.iloc[i, 1], df.iloc[i, 2] ]
        
        sec1 = st.container()
        with sec1:
            fil = moviedb[ ['name', 'year', 'country'] ].groupby('country').count()
            countries = list(fil.index)
            count = list(fil['year'])
            
            fil2 = moviedb[ ['score', 'country'] ].groupby('country').mean()
            avg_score = list( fil2['score'].apply( self.format ) )
            text = [ "movies - Avg Score: "+str(i) for i in avg_score ]
            
            st.markdown("### Countries and their number of films produced ")
            map_ui = go.Figure(
            data = {
                'type':'choropleth',
                'locationmode':'country names',        
                'locations': countries,
                'colorscale':'Portland',            
                'text': text,
                'z': count,                  
                'colorbar':{'title':'Number of movies produced by each country'}
            },     
            layout = {
              'geo':{
                  'scope':'world'
              }  
            })
            map_ui.update_layout(
                autosize=False,
                margin = dict(
                        l=0,
                        r=0,
                        b=0,
                        t=0,
                        pad=4,
                        autoexpand=True
                    ),
                    width=800,
                #     height=400,
            )
            st.plotly_chart(map_ui)
    
    def drawVotesDistribution(self, filtered):
        votes = list(filtered['votes'])
        res = pd.Series(votes, name="Number of Votes")
        fig = plt.figure(figsize=(10, 4))
        plt.xlabel('Votes')
        plt.ylabel('Frequency')
        #sns.distplot(res)
        fig=px.histogram(res, x="Number of Votes")
        st.plotly_chart(fig)
    
    def drawColumnMissing(self, filtered):
        x=[]
        y=[]
        cols=filtered.columns
        for c in cols:
            cnt = len(filtered[ filtered[c].isna() ])
            if(cnt>0):
                x.append( c.capitalize().replace('_',' ') )
                y.append(cnt)
                
        res=pd.DataFrame()
        res['Columns'] = x
        res['Count'] = y
        #fig = plt.figure( figsize=(10, 4) )
        fig = px.bar(res, x='Columns', y='Count')
        st.plotly_chart(fig)
    
    def sec2_columnQuality(self, moviedb_raw):
        sec1 = st.container()
        with sec1:
            st.markdown("### Filtering data to check quality ")
            
            moviedb = pd.read_csv("https://raw.githubusercontent.com/danielgrijalva/movie-stats/7c6a562377ab5c91bb80c405be50a0494ae8e582/movies.csv")
            moviedb.dropna()
            genre_list = moviedb['genre'].unique().tolist()
            genre_list.append('All')
            new_score_rating = st.slider(label = "Choose a score range:", min_value = 1.0, max_value = 10.0, value = (5.0, 10.0))
            new_genre_list = st.multiselect('Choose Genre:', genre_list, default = ['All'])
            filtered = moviedb[ moviedb['score'].between(*new_score_rating) ]
            
            if(not 'All' in new_genre_list):
                filtered = filtered[ filtered['genre'].isin(new_genre_list) ]
            else:
                new_genre_list = ['All']
            
            st.markdown("#### User Votes Distribution ")
            self.drawVotesDistribution(filtered)
              
            st.markdown("#### Missing Values by Column ")
            self.drawColumnMissing   (filtered)         
                        
            st.markdown("#### Filtered Data ")
            st.dataframe(filtered, width = 800)

    def eda_UI(self, moviedb, movies_data_raw):
        mapc = st.container()
        with mapc:
            self.sec1_mapCountMovies(moviedb)
            st.divider()
            self.sec2_columnQuality(movies_data_raw)
