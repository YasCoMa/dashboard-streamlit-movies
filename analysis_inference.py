import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import math

class DashboardInference:
    def format(self, v):
        return "{:.2f}".format(v)    
    
    def sec1_predictability(self, moviedb):
        sec1 = st.container()
        with sec1:
            #fil = moviedb[ ['score', 'budget', 'gross', 'runtime'] ]
            fil = moviedb[ ['score', 'gross', 'runtime'] ]
            
            st.markdown("### Correlation among numerical variables ")
            st.write("According to the plot, we can see that movies with high score tend to return a large gross to the company, which was expected. Another relationship in this dataset is that long movies have more samples with scores in the 7 to 9, which means that the few long movies are well receiveid by the customers. The only movies that we can see as two outlier samples with more than 300 minutes are Little Dorrit (1987, score 7.3) and The Best of Youth (2003, score 8.5). The first was produced by United Kingdom while the last is from Italy.")
            
            fig=sns.pairplot(fil)
            st.pyplot(fig)
    
    def sec2_runtimeRange_by_score(self, moviedb):
        sec2 = st.container()
        with sec2:
            #fil = moviedb[ ['score', 'budget', 'gross', 'runtime'] ]
            fil = moviedb[ ['score', 'runtime'] ]
            newdf=pd.DataFrame()
            scores=[]
            ranges=[]
            for i in fil.index:
                flag=True
                sc=fil.loc[i, 'runtime']
                if(sc<=90):
                    ranges.append('Short')
                elif(sc>90 and sc<=120):
                    ranges.append('Medium')
                elif(sc>120):
                    ranges.append('Long')
                else:
                    flag=False 
                
                if(flag):
                    scores.append( fil.loc[i, 'score'] )
                
            newdf['Runtime Ranges'] = ranges
            newdf['Scores Distribution'] = scores
            
            st.markdown("### Score distribution according to runtime categories ")
            st.write("Here it was considered Short those with less than 90 minutes, medium from 90 to 120 minutes, and long those having more than 2 hours.")
            
            fig = px.box(newdf, x="Runtime Ranges", y="Scores Distribution")
            st.plotly_chart(fig)
    
    def sec3_scoreRange_by_gross_budget(self, moviedb):
        sec3 = st.container()
        with sec3:
            #fil = moviedb[ ['score', 'budget', 'gross', 'runtime'] ]
            
            st.markdown("### Budget and Gross distribution according to score categories ")
            st.write("Here it was considered Low those with score lower than 3, medium from 4 to 6, and High those having more than 7.")
            
            countries = ['All']+list( moviedb['country'].unique() )
            country = st.selectbox("Select a Country", tuple(countries), index=0)
            
            fil1 = moviedb[ ['score', 'budget', 'country'] ]
            if(country!='All'):
                fil1 = fil1.query("country=='"+country+"'")
                
            newdf1 = pd.DataFrame()
            scores=[]
            ranges=[]
            for i in fil1.index:
                flag=True
                sc=fil1.loc[i, 'score']
                if(sc<=3):
                    ranges.append('Low')
                elif(sc>=4 and sc<=6):
                    ranges.append('Medium')
                elif(sc>=7):
                    ranges.append('High')
                else:
                    flag=False 
                
                if(flag):
                    scores.append( fil1.loc[i, 'budget'] )
                
            newdf1['Score Ranges'] = ranges
            newdf1['Budget Distribution'] = scores
            
            fig = px.box(newdf1, x="Score Ranges", y="Budget Distribution")
            st.plotly_chart(fig)
                
            fil2 = moviedb[ ['score', 'gross', 'country'] ]
            if(country!='All'):
                fil2 = fil2.query("country=='"+country+"'")
                
            newdf2 = pd.DataFrame()
            scores=[]
            ranges=[]
            for i in fil2.index:
                flag=True
                sc=fil2.loc[i, 'score']
                if(sc<=3):
                    ranges.append('Low')
                elif(sc>=4 and sc<=6):
                    ranges.append('Medium')
                elif(sc>=7):
                    ranges.append('High')
                else:
                    flag=False 
                
                if(flag):
                    scores.append( fil2.loc[i, 'gross'] )
                
            newdf1['Score Ranges'] = ranges
            newdf1['Gross Distribution'] = scores
            
            fig = px.box(newdf1, x="Score Ranges", y="Gross Distribution")
            st.plotly_chart(fig)
    
    def sec4_profit_by_company(self, moviedb):
        sec4 = st.container()
        with sec4:
            #fil = moviedb[ ['score', 'budget', 'gross', 'runtime'] ]
            fil = moviedb[ ['company', 'country', 'budget', 'gross'] ]
            fil['Company-Country']=fil['company']+' - '+fil['country']
            fil['Profit']=fil.loc[:,'gross']-fil.loc[:,'budget']
            
            st.markdown("### Companies and their profits (mean gross - mean budget) ")
            crit = st.selectbox("Select an ordering criteria", tuple(['Top 10 Highest', 'Top 10 Lowest']), index=0)
            
            filt = fil[ ['Company-Country', 'Profit'] ].groupby(['Company-Country'], as_index=False).mean().dropna()
            
            if(crit=='Top 10 Highest'):
                filt=filt.sort_values(by='Profit', ascending=False)
            if(crit=='Top 10 Lowest'):
                filt=filt.sort_values(by='Profit', ascending=True)
            
            filt = filt.iloc[:10, :]
            fig = px.line(filt, x='Company-Country', y="Profit")
            st.plotly_chart(fig)
    
    def sec5_budgetGross_by_company(self, moviedb):
        sec5 = st.container()
        with sec5:
            #fil = moviedb[ ['score', 'budget', 'gross', 'runtime'] ]
            fil = moviedb[ ['company', 'country', 'budget', 'gross'] ]
            fil.dropna()
            fil['Company-Country']=fil['company']+' - '+fil['country']
            newdf=pd.DataFrame()
            ide={}
            y={}
            typ={}
            for t in ['budget', 'gross']:
                y[t]={}
                typ[t]=[]
                for i in fil.index:
                    y[t][ fil.loc[i, 'Company-Country'] ] = math.log10( fil.loc[i, t]) 
                
            y['gross'] = dict(sorted(y['gross'].items(), key=lambda item: item[1], reverse=True) )
            x=list(y['gross'].keys())[:10]
            y1=[]
            for i in x:
                y1.append(y['budget'][i])
            y2=list(y['gross'].values())[:10]
            
            st.markdown("### Top 10 Companies with their gross and budget (log10 scale) ")
            
            fig = go.Figure(data=[
                go.Bar(name='Budget', x=x, y=y1 ),
                go.Bar(name='Gross', x=x, y=y2 )
            ])
            fig.update_layout(barmode='group')
            
            st.plotly_chart(fig)
    
    def sec6_budgetGrossRutime_by_year(self, moviedb):
        sec6 = st.container()
        with sec6:
            st.markdown("### Evolution of metrics across the years ")
            
            col1, col2 = st.columns([6,6])
            with col1:      
                fields = ['Budget', 'Gross', 'Runtime']
                field = st.selectbox("Select a Field", tuple(fields), index=0)
            with col2:      
                aggs = ['Min', 'Max', 'Mean']
                agg = st.selectbox("Select a Field", tuple(aggs), index=0)
            
            #fil = moviedb[ ['score', 'budget', 'gross', 'runtime'] ]
            fil = moviedb[ ['runtime', 'budget', 'gross', 'year'] ]
            fil.dropna()
            y=[]
            x=[]
            for i in fil.index:
                y.append( fil.loc[i, field.lower()] )
                
                year = fil.loc[i, 'year']
                prefix=str(year)[:3]
                prefix2 = prefix[:2]+str( int(prefix[-1])+1 )+'0'
                if( int(prefix+'0')<=year and int(prefix+'5')>year ):
                    x.append(prefix+'0 - '+prefix+'5')
                elif int(prefix+'5')<=year and int(prefix2)>year :
                    x.append(prefix+'5 - '+prefix2)
                
            newdf=pd.DataFrame()
            newdf['Year Ranges'] = x
            newdf[field.capitalize()] = y
            #print(newdf)
            filt = eval("newdf.groupby('Year Ranges', as_index=False)."+agg.lower()+"()")
            fig = px.bar(filt, x='Year Ranges', y=field.capitalize())
            #fig=sns.barplot(data=filt, x='Year Ranges', y=field.capitalize())
            st.plotly_chart(fig)
            
    def inference_UI(self, moviedb):
        mapc = st.container()
        with mapc:
            self.sec1_predictability(moviedb)
            st.divider()
            self.sec2_runtimeRange_by_score(moviedb)
            st.divider()
            self.sec3_scoreRange_by_gross_budget(moviedb)
            st.divider()
            self.sec4_profit_by_company(moviedb)
            st.divider()
            self.sec5_budgetGross_by_company(moviedb)
            st.divider()
            self.sec6_budgetGrossRutime_by_year(moviedb)
            
