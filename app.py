#Libraries that i am going to use
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#reading the file
df_Arg = pd.read_csv('df_Arg.csv')

#creating a sidebar
st.sidebar.header('Spotify Analysis')
st.sidebar.image('arg.jpeg')
st.sidebar.write('Visualizing Spotify Data of Argentina from 2017-2021.')
st.sidebar.markdown('Made By Lobna Hegazy')

#creating a dropdown with a list of choices
visualization_type = st.selectbox(
  'Select A Choice', 
  [
  'Select A Choice',
  'Overview Of Data',
  'Trend of Artist Popularity Over the Years',
  'Top 5 Artist By Total Streams In Year',
  'Top 5 Songs From 2017-2021',
  'Top 10 Artists From 2017-2021',
  'Top 10 Artist Streams Over Time',
  'Year-over-Year Growth',
  'Average Streams by Year',
  'Rate Of Streams',
  ]
)

#using if/else to help when picking a choice to show its visualization


#Visualizing top 10 artists from 2017-2020
if visualization_type == 'Top 10 Artists From 2017-2021':
    df_filtered = df_Arg[df_Arg['year'].between(2017, 2021)]
    top_artists = df_filtered['artist'].value_counts().head(10)
    top_artists_df = pd.DataFrame(top_artists).reset_index()
    top_artists_df.columns = ['artist', 'count']
    st.bar_chart(top_artists_df.set_index('artist'))

#visualizing the top 10 artists streams over time
elif visualization_type == 'Top 10 Artist Streams Over Time':
  df_filtered = df_Arg[df_Arg['year'].between(2017, 2021)]
  top_artists = df_filtered['artist'].value_counts().head(10).index
  df_top_artists = df_filtered[df_filtered['artist'].isin(top_artists)]

  selected_artist = st.selectbox('Select an Artist', top_artists)
  artist_data = df_top_artists[df_top_artists['artist'] == selected_artist]
  clm = st.selectbox('Select Column', ['streams'])
  plt.figure(figsize=(12, 6))
  sns.lineplot(data=artist_data, x='year', y=clm, marker='o')
  plt.xlabel('Year')
  plt.ylabel(clm.capitalize())
  plt.title(f'{selected_artist} - {clm.capitalize()} Over the Years (2017-2021)')
  plt.grid(True)
  st.pyplot(plt)



#visualizing top 5 songs from 2017-2021
elif visualization_type =='Top 5 Songs From 2017-2021':
  top_5_songs = df_Arg['title'].value_counts().head(5).index
  top_5_data = df_Arg[df_Arg['title'].isin(top_5_songs)]
  top_5_streams = top_5_data.groupby('title')['streams'].sum().reset_index()
  top_5_streams_sorted = top_5_streams.sort_values(by='streams', ascending=False)
  top_5_streams_sorted.set_index('title').plot(kind='pie', y='streams', figsize=(10, 6), autopct='%1.1f%%')
  plt.title('Top 5 Songs by Streams')
  st.pyplot(plt)

#seeing average streams per year
elif visualization_type == 'Average Streams by Year':
  plt.figure(figsize=(10, 6))
  sns.barplot(data=df_Arg, x='year', y='average_streams')
  plt.title('Average Streams by Year')
  plt.xlabel('Year')
  plt.ylabel('Average Streams')
  plt.xticks(rotation=45)
  plt.tight_layout()
  st.pyplot(plt)

#seeing rate of streams through the years
elif visualization_type == 'Rate Of Streams':
  st.write('Increases each year')
  figsize = (6,6)
  plt.figure(figsize=figsize)
  sns.lineplot(x='year',y='streams',data=df_Arg)
  print(df_Arg['streams'].max())
  st.pyplot(plt)

#seeing how the streams grew over the years (%)
elif visualization_type == 'Year-over-Year Growth':
  st.write('Shows The Growth Of Streams Per Year.')
  yearly_streams = df_Arg.groupby('year')['streams'].sum().reset_index()
  yearly_streams['growth'] = yearly_streams['streams'].pct_change() * 100
  plt.figure(figsize=(12, 6))
  plt.xlabel('Year')
  plt.ylabel('Year-over-Year Growth (%)')
  plt.title('Year-over-Year Growth in Streams')
  plt.xticks(rotation=45)
  plt.grid(True)
  st.bar_chart(data=yearly_streams, x='year', y='growth')

#Overview of data
elif visualization_type == 'Overview Of Data':
  st.write('Maximum Number Of Streams Per Year')
  max_streams_per_year = df_Arg.groupby('year')['streams'].max().reset_index()
  st.write(max_streams_per_year)

  avg_streams_per_year = df_Arg.groupby('year')['streams'].mean().reset_index()
  st.write('Average Number of Streams Per Song Per Year')
  st.write(avg_streams_per_year)

  st.write('Top 10 Artists')
  top_10_Artists = df_Arg['artist'].value_counts().head(10)
  st.write(top_10_Artists)

  st.write('Top 10 Songs')
  top_10_songs = df_Arg['title'].value_counts().head(10)
  st.write(top_10_songs)

  st.write('Data that is used:')
  st.write(df_Arg)

#seeing the trend of an artist per year
elif visualization_type =='Trend of Artist Popularity Over the Years':
  selected_artist = st.selectbox('Select Artist', df_Arg['artist'].unique())
  artist_trend = df_Arg[df_Arg['artist'] == selected_artist].groupby('year')['streams'].sum().reset_index()
  st.write(f'Trend of {selected_artist}\'s Popularity Over the Years')
  st.line_chart(artist_trend.set_index('year')['streams'])

#seeing the streams of top 5 artists of each year
elif visualization_type == 'Top 5 Artist By Total Streams In Year':
    selected_year = st.selectbox('Select Year', df_Arg['year'].unique())
    st.write(f'Top 5 Artists by Total Streams in {selected_year}')
    top_artists = df_Arg[df_Arg['year'] == selected_year] \
                .groupby('artist')['streams'] \
                .sum() \
                .nlargest(5) \
                .reset_index()
    st.bar_chart(top_artists.set_index('artist')['streams'])



