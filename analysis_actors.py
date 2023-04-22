import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import json
import os

import imdb
from streamlit_agraph import agraph, Node, Edge, Config

class DashboardActors:
    def format(self, v):
        return "{:.2f}".format(v)    
    
    def sec1_top10_actors_scores(self, moviedb):
        
        sec1 = st.container()
        with sec1:
            st.markdown("### Top 10 movie stars in high scored movies")
            st.write("Here it was considered high those having more than 7.")
            
            countries = ['All']+list( moviedb['country'].unique() )
            country = st.selectbox("Select a Country", tuple(countries), index=0, key=2)
            
            fil1 = moviedb[ ['score', 'star', 'country'] ]
            if(country!='All'):
                fil1 = fil1.query("country=='"+country+"'")
            dat={}
            for i in fil1.index:
                flag=True
                sc=fil1.loc[i, 'score']
                if(sc>=7):
                    star=fil1.loc[i, 'star']
                    if( not star in dat.keys() ):
                        dat[star] = 0
                    dat[star]+=1
                else:
                    flag=False 
            dat = dict(sorted(dat.items(), key=lambda item: item[1], reverse=True) )
            
            x = list(dat.keys())[:10]
            y = list(dat.values())[:10]
            fig = go.Figure(data=[
                go.Scatter(x=x, y=y, text=y )
            ])
            fig.update_traces(hoverinfo='text', mode='lines+markers')
            fig.update_layout(xaxis_title="Actors", yaxis_title="Number of Movies", yaxis_range=[10, 22] )
            st.plotly_chart(fig)  
    
    def sec2_top10_writers_gross(self, moviedb):
        
        sec2 = st.container()
        with sec2:
            st.markdown("### Most successful writers according to the gross")
            
            fil1 = moviedb[ ['gross', 'writer', 'country'] ]
            fil1=fil1.sort_values(by='gross', ascending=False)
            dat={}
            for i in fil1.index:
                sc=fil1.loc[i, 'gross']
                writer=fil1.loc[i, 'writer']
                if( not writer in dat.keys() ):
                    dat[writer] = 0
                dat[writer]+=1
            dat = dict(sorted(dat.items(), key=lambda item: item[1], reverse=True) )
                
            x = list(dat.keys())[:10]
            y = list(dat.values())[:10]
            fig = go.Figure(data=[
                go.Scatter(x=x, y=y, text=y )
            ])
            fig.update_traces(hoverinfo='text', mode='lines+markers')
            fig.update_layout(xaxis_title="Writers", yaxis_title="Number of Movies", yaxis_range=[10, 40])
            st.plotly_chart(fig)
    
    def sec3_top10_directors_gross(self, moviedb):
        
        sec3 = st.container()
        with sec3:
            st.markdown("### Most successful directors according to the gross")
            
            fil1 = moviedb[ ['gross', 'director', 'country'] ]
            fil1=fil1.sort_values(by='gross', ascending=False)
            dat={}
            for i in fil1.index:
                sc=fil1.loc[i, 'gross']
                director=fil1.loc[i, 'director']
                if( not director in dat.keys() ):
                    dat[director] = 0
                dat[director]+=1
            dat = dict(sorted(dat.items(), key=lambda item: item[1], reverse=True) )
                
            x = list(dat.keys())[:10]
            y = list(dat.values())[:10]
            fig = go.Figure(data=[
                go.Scatter(x=x, y=y, text=y )
            ])
            fig.update_traces(hoverinfo='text', mode='lines+markers')
            fig.update_layout(xaxis_title="Directors", yaxis_title="Number of Movies", yaxis_range=[10, 40])
            st.plotly_chart(fig)
    
    def sec4_build_network(self, moviedb):
        sec4 = st.container()
        with sec4:
            st.markdown("### Actor and movie network")
            st.write("Network seeds correspond to movies with score above 8, the actors are retrieved using IMDB python package.")
            
            dat={}
            if(os.path.isfile('high_scored_imdb_info.json')):
                with open('high_scored_imdb_info.json','r') as f:
                    dat=json.load(f)
            else:
                ia = imdb.IMDb()
                #new_score_rating = st.slider(label = "Choose a score range:", min_value = 1.0, max_value = 10.0, value = (8.0, 10.0), key="net_slider")
                #filtered = moviedb[ moviedb['score'].between(*new_score_rating) ]
                filtered = moviedb
                dat={}
                for i in filtered.index:
                    movie=filtered.loc[i, 'name']
                    star=filtered.loc[i, 'star']
                    dat[movie]={ 'star' : star }
                
                for m in dat.keys():
                    items = ia.search_movie(m)
                    mobj=ia.get_movie(items[0].movieID)
                    dat[m]['id'] = items[0].movieID
                    
                    actors=set()
                    cast=[]
                    for c in mobj['cast']:
                        p=ia.get_person(c.personID)
                        
                        img=''
                        if('headshot' in p.keys()):
                            img=p['headshot']
                        
                        movies=[]
                        if('filmography' in p.keys()):
                            col='actor'
                            if( 'actress' in p['filmography'].keys() ):
                                col='actress'
                            if( col in  p['filmography'].keys() ):
                                for i in p['filmography'][col]:
                                    movies.append(i['title'])
                        cast.append( { 'id': c.personID, 'name': c['name'], 'img': img, 'movies': movies } )
                        actors.add(c['name'])
                        
                    dat[m]['cast'] = cast
                    dat[m]['actors'] = actors
                with open('high_scored_imdb_info.json', 'w') as f:
                    json.dump(dat, f)
            
            nset=set()
            eset=set()
            nodes=[]
            edges=[]
            for m in dat.keys():
                id_=dat[m]['id']
                if(not id_ in nset):
                    nset.add(id_)
                    nodes.append( Node(id=id_, label=m, size=20, color="#37AA20") )
                
                i=0
                for p in dat[m]['cast']:
                    pid=p['id']
                    if(not pid in nset):
                        nset.add(pid)
                        if(p["headshot"]!=''):
                            nodes.append( Node(id=pid, label=p['name'], size=30, shape="circularImage", image=p["headshot"] ) )
                        else:
                            nodes.append( Node(id=pid, label=p['name'], size=25, color="#7EA7EA" ) )
                            
                    ide=id_+'-'+pid
                    if(not ide in eset):
                        eset.add(ide)
                        edges.append( Edge(source=pid,  label="acted_in", target=id_ ) )
                    
                    j=0
                    for k in dat[m]['cast']:
                        kid=k['id']
                        if(not kid in nset):
                            nset.add(kid)
                            if(k["headshot"]!=''):
                                nodes.append( Node(id=kid, label=k['name'], size=30, shape="circularImage", image=k["headshot"] ) )
                            else:
                                nodes.append( Node(id=kid, label=k['name'], size=25, color="#7EA7EA" ) )
                        
                        ide=id_+'-'+kid
                        if(not ide in eset):
                            eset.add(ide)
                            edges.append( Edge(source=kid,  label="acted_in", target=id_ ) )
                            
                        ide=pid+'-'+kid
                        if(i<j):
                            if(not ide in eset):
                                eset.add(ide)
                                edges.append( Edge(source=kid,  label="coworker", target=pid ) )
                        j+=2
                    i+=1
            
            config = Config(width=750, height=950, directed=True,  physics=True,  hierarchical=False )

            return_value = agraph(nodes=nodes, edges=edges, config=config)
    
    def sec4_build_network_v2(self, moviedb):
        sec4 = st.container()
        with sec4:
            st.markdown("### Actor and movie network")
            st.write("Network seeds correspond to movies with score in the chosen range. Green nodes are movies and the blue ones represent actors or actresses. The Hub nodes of actors are marked in red color, meaning the stars that participated in many movies.")
            
            new_score_rating = st.slider(label = "Choose a score range:", min_value = 1.0, max_value = 10.0, value = (8.0, 10.0), key="net_slider")
            filtered = moviedb[ moviedb['score'].between(*new_score_rating) ]
            star_hubs={}
            dat={}
            for i in filtered.index:
                movie=filtered.loc[i, 'name']
                star=filtered.loc[i, 'star']
                if(str(star)!="nan"):
                    dat[movie]={ 'star' : star }
                    if(not star in star_hubs.keys()):
                        star_hubs[star]=0
                    star_hubs[star]+=1
                    
            star_hubs = dict(sorted(star_hubs.items(), key=lambda item: item[1], reverse=True) )
            starsh=list(star_hubs.keys())[:20]
            
            with st.expander("Top 20 hubs list"):
                for s in starsh:
                    st.markdown("- "+s+" - Degree: "+str(star_hubs[s]))
            
            nset=set()
            eset=set()
            nodes=[]
            edges=[]
            for m in dat.keys():
                id_=m
                if(not id_ in nset):
                    nset.add(id_)
                    nodes.append( Node(id=id_, label=m, size=20, color="#37AA20") )
                
                pid=dat[m]['star']
                if(not pid in nset):
                    color="#7EA7EA"
                    if(pid in starsh):
                        color='#BD3059'
                    nset.add(pid)
                    nodes.append( Node(id=pid, label=dat[m]['star'], size=25, color=color ) )
                        
                ide=id_+'-'+pid
                if(not ide in eset):
                    eset.add(ide)
                    edges.append( Edge(source=pid,  label="acted_in", target=id_ ) )
            
            config = Config(width=750, height=950, directed=True,  physics=True,  hierarchical=False )

            return_value = agraph(nodes=nodes, edges=edges, config=config)
            
    def actors_UI(self, moviedb):
        mapc = st.container()
        with mapc:
            #self.sec4_build_network(moviedb)
            self.sec4_build_network_v2(moviedb)
            st.divider()
            self.sec1_top10_actors_scores(moviedb)
            st.divider()
            self.sec2_top10_writers_gross(moviedb)
            st.divider()
            self.sec3_top10_directors_gross(moviedb)
