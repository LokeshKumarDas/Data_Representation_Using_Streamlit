import streamlit as st 
import utils
import pandas as pd
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
        
    participating_nations = utils.participating_nations(df)
    fig = ex.line(participating_nations, x='Edition', y='No. of Countries')
    st.title('Participating Nations over the years')
    st.plotly_chart(fig)