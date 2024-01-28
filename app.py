import streamlit as st
import pandas as pd
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import preprocessor

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
nations = pd.read_csv('nat.csv')
# df = preprocessor.preprocess()
# df = pd.read_csv('athlete_events.csv')
# region_df = pd.read_csv('noc_regions.csv')
st.sidebar.header("Olympic analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis')
)

df = preprocessor.preprocess(df, region_df)
# st.dataframe(df)

if user_menu == 'Medal Tally':
    st.header("Medal tally")
    years, country = helper.country_year_list(df)
    selected_country = st.sidebar.selectbox("Select Country", country)
    selected_year = st.sidebar.selectbox("Select Year", years)
    med = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal tally of year" + str(selected_year))
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title("Medal tally of country" + str(selected_country))
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title("Medal tally of year" + str(selected_year) + " " + str(selected_country))

    st.dataframe(med)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations = helper.nations_over_time(df)
    fig = px.line(nations, x='Year', y='count')
    st.plotly_chart(fig)

if user_menu == 'Country-wise Analysis':
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected = st.sidebar.selectbox("Country", country_list)
    country = helper.year_wise_medaltally(df, selected)
    fig = px.line(country, x='Year', y='Medal')
    st.plotly_chart(fig)
    st.title(selected + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)
    st.title("Top ten athletes ")
    st.table(helper.top_ten_ath_countrywise(df,selected))
