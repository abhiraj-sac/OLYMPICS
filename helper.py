import numpy as np


def medal_tally(df):
    medal_tally = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    sums = medal_tally.groupby(['region'], as_index=False).agg(Gold=('Gold', 'sum'), Silver=('Silver', 'sum'),
                                                               Bronze=('Bronze', 'sum')).sort_values('Gold',
                                                                                                     ascending=False)
    sums['total'] = sums['Gold'] + sums['Silver'] + sums['Bronze']
    # x['Gold'] = x['Gold'].astype('int')
    # x['Silver'] = x['Silver'].astype('int')
    # x['Bronze'] = x['Bronze'].astype('int')
    # x['total'] = x['total'].astype('int')
    return sums


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return years, country


def fetch_medal_tally(df, year, country):
    medal_tally = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_tally
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_tally[medal_tally['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_tally[medal_tally['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_tally[(medal_tally['Year'] == int(year)) & (medal_tally['region'] == country)]
    if flag == 1:
        x = temp_df.groupby(['Year'], as_index=False).agg(Gold=('Gold', 'sum'), Silver=('Silver', 'sum'),
                                                          Bronze=('Bronze', 'sum')).sort_values('Year')
    else:
        x = temp_df.groupby(['region'], as_index=False).agg(Gold=('Gold', 'sum'), Silver=('Silver', 'sum'),
                                                            Bronze=('Bronze', 'sum')).sort_values('Gold',
                                                                                                  ascending=False)
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')
    return x


def nations_over_time(df):
    nation_over_time = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().sort_values()
    nation_over_time = nation_over_time.reset_index()
    return nation_over_time


def year_wise_medaltally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def top_ten_ath_countrywise(temp_df,country):
    country = temp_df[temp_df['region'] == country]
    c = country.groupby(['Name'], as_index=False).agg(Gold=('Gold', 'sum'), Silver=('Silver', 'sum'),
                                                      Bronze=('Bronze', 'sum')).sort_values('Gold', ascending=False)
    c['total'] = c['Gold'] + c['Silver'] + c['Bronze']
    c = c.sort_values('total', ascending=False).head(10)
    return c['Name']
