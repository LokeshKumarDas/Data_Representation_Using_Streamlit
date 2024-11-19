import pandas as pd
import numpy as np

def preprocessor(df, region_info):
    df = df[df['Season'] == 'Summer']
    df = df.merge(region_info, on='NOC', how='left')
    df.drop_duplicates(inplace = True)
    df.drop(columns='Season', axis=1)
    df.drop_duplicates(['Year', 'region'])
    df = pd.concat([df, pd.get_dummies(df['Medal'], dtype=int)], axis=1)
    df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    
    return df

def Medal_Tally(data, year, country):
    
    flag_year =0
    flag_country =0

    if year == 'Overall':
        flag_year = 1
    else:
        data = data[data['Year'] == year]

    if country == 'Overall':
        pass
    else:
        flag_country = 1
        data = data[data['region'] == country]

    if (flag_year&flag_country):
        data = data.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().    sort_values('Year', ascending=True).reset_index()
    else:
        data = data.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().  sort_values('Gold', ascending=False).reset_index()

    data['Total Medals'] = data['Gold'] + data['Silver'] + data['Bronze']
    
    return data

def lists(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years = ['Overall'] + years
    
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country = ['Overall'] + country

    return years, country

def analyse_over_time(df, x):
    
    df_for_each_year = df.drop_duplicates(['Year', x])['Year'].value_counts().reset_index().sort_values('Year')
    df_for_each_year.rename(columns={'count':x, 'Year': 'Edition'}, inplace=True)

    return df_for_each_year
