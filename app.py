import streamlit as st 
import utils
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as ex

region_info = pd.read_csv('noc_regions.csv')
df = pd.read_csv('athlete_events.csv')

df = utils.preprocessor(df, region_info)

st.sidebar.title('Olympics Analysis')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)

# st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years,countries = utils.lists(df)
    select_year = st.sidebar.selectbox('Select Year', years)
    select_country = st.sidebar.selectbox('Select Country', countries)
    if (select_year=='Overall')&(select_country=='Overall'):
        st.title(f'Performance of all countries over years in Olympics')
    elif (select_year=='Overall')&(select_country!='Overall'):
        st.title(f'Overall performance of {select_country} in Olympics across years')
    elif (select_year!='Overall')&(select_country=='Overall'):
        st.title(f'Olympics result for year: {select_year}')
    elif (select_year!='Overall')&(select_country!='Overall'):
        st.title(f'Performance of {select_country} in Olympics {select_year}')
        
    Medal_Tally = utils.Medal_Tally(df, select_year, select_country)
    st.table(Medal_Tally)
    
if user_menu == 'Overall Analysis':
    st.title('Top Statistics')
    editions = df['Year'].unique().shape[0] -1
    cities = df['City'].unique().shape[0] 
    sports = df['Sport'].unique().shape[0] 
    events = df['Event'].unique().shape[0] 
    athletes = df['Name'].unique().shape[0] 
    nations = df['region'].unique().shape[0] 
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)
        
    participating_nations_over_time = utils.analyse_over_time(df, 'region')
    fig = ex.line(participating_nations_over_time, x='Edition', y='region')
    st.title('Participating Nations over the years')
    st.plotly_chart(fig)
    
    events_over_time = utils.analyse_over_time(df, 'Event')
    fig = ex.line(events_over_time, x='Edition', y='Event')
    st.title('Events over the years')
    st.plotly_chart(fig)
    
    athletes_over_time = utils.analyse_over_time(df, 'Name')
    fig = ex.line(athletes_over_time, x='Edition', y='Name')
    st.title('Athletes over the years')
    st.plotly_chart(fig)
    
    st.title('No. of Events over time considering every sport')
    fig, ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    pivot_table = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int)
    ax = sns.heatmap(pivot_table, annot=True)
    st.pyplot(fig)
    
    st.title('Top Medalist')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    sport_selected = st.selectbox('Select a Sport', sport_list)
    top_medalist = utils.most_successful(df, sport_selected)
    st.table(top_medalist)