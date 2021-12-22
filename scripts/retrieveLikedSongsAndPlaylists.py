#!/usr/bin/env python
# coding: utf-8

# # Imports

# In[ ]:


## Import Libraries
import pandas as pd
import numpy as np
import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth
import credentials as cred
import sys
from pathvalidate import ValidationError, validate_filename, sanitize_filename
import os


# ## Aux Functions

# In[ ]:


def convertMillisecondsToMinutesAndSeconds(duration_ms):
    seconds, milliseconds = divmod(duration_ms, 1000)
    minutes, seconds = divmod(seconds, 60)

    # round up based on milliseconds remainder being at least 500
    seconds = (seconds+1 if milliseconds>=500 else seconds)
    
    
    return(f'{int(minutes):02d}:{int(seconds):02d}')
    


# # Main

# ## Authentication

# In[ ]:


scope = 'user-read-recently-played user-library-read'

sp_auth = sp.Spotify(auth_manager=sp.oauth2.SpotifyOAuth(client_id=cred.client_ID, client_secret= cred.client_SECRET, redirect_uri=cred.redirect_url, scope=scope))


# ## Set Market to Argentina (Change if needed)

# In[ ]:


market='AR'


# ## Create MyPlaylists Subfolder

# In[ ]:


likedSongsPath='./LikedSongs'
myPlaylistsPath='./MyPlaylists'

os.makedirs(likedSongsPath, exist_ok=True)
os.makedirs(myPlaylistsPath, exist_ok=True)


# ## Liked Songs

# In[ ]:


## Batch Handling
batch=1
batch_size = 20


# First Batch
results = sp_auth.current_user_saved_tracks(limit=batch_size, offset=0, market=market)['items']

# Dataframe lists
artists = list()
songs = list()
albums = list()
typeOfAlbum = list()
track_numbers = list()
release_dates = list()
duration_ms = list()

while results != []:
    for item in results:
        artists.append(f"{item['track']['artists'][0]['name']}")
        songs.append(f"{item['track']['name']}")
        albums.append(f"{item['track']['album']['name']}")
        typeOfAlbum.append(f"{item['track']['album']['album_type'].capitalize()}")
        release_dates.append(f"{item['track']['album']['release_date']}")
        track_numbers.append(f"{item['track']['track_number']}")
        duration_ms.append(f"{convertMillisecondsToMinutesAndSeconds(item['track']['duration_ms'])}")
    
    # Read next batch until it's empty                       
    batch=batch+1
    results = sp_auth.current_user_saved_tracks(limit=batch_size, offset=batch_size*(batch-1), market='AR')['items']

# Create DataFrame
data = {'Artist': artists,
        'Song': songs,
        'Album': albums,
        'TypeOfAlbum': typeOfAlbum,
        'TrackNumber': track_numbers,
        'AlbumReleaseDate': release_dates,
        'Duration': duration_ms }                 
df = pd.DataFrame(data)
                           
# Print DataFrame
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
    display(df)


# ### Save dataframe to csv

# In[ ]:


df.to_csv(f"{likedSongsPath}/LikedSongs.csv")


# # Get Playlists

# In[ ]:


## Batch Handling
batch=1
batch_size = 20

# First batch
results = sp_auth.current_user_playlists(limit=batch_size, offset=0)['items']

# Dataframe lists
id = list()
playlists = list()
owners = list()
tracks = list()

while results != []:
    for item in results:
        id.append(f"{item['id']}")
        playlists.append(f"{item['name']}")
        owners.append(f"{item['owner']['display_name']}")
        tracks.append(f"{item['tracks']['total']}")
                      
    # Read next batch until it's empty                       
    batch=batch+1 
    results = sp_auth.current_user_playlists(limit=batch_size, offset=batch_size*(batch-1))['items']

# Create DataFrame
data = {'ID': id,
        'Playlist': playlists,
        'Owner': owners,
        'Tracks': tracks}                 
df = pd.DataFrame(data)

# Print DataFrame                         
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
    display(df)


# ### Save dataframe to csv

# In[ ]:


df.to_csv(f"{myPlaylistsPath}/PlaylistsOverview.csv")


# ## Get each Playlist contents

# In[ ]:


df_playlist = df[['ID','Playlist']].copy()
df_playlist


# In[ ]:


for index, row in df.iterrows():
    results = sp_auth.playlist(playlist_id=row['ID'],market=market)['tracks']['items']

    # Dataframe lists
    artists = list()
    songs = list()
    albums = list()
    typeOfAlbum = list()
    track_numbers = list()
    release_dates = list()
    duration_ms = list()

    for item in results:
        artists.append(f"{item['track']['artists'][0]['name']}")
        songs.append(f"{item['track']['name']}")
        albums.append(f"{item['track']['album']['name']}")
        typeOfAlbum.append(f"{item['track']['album']['album_type'].capitalize()}")
        release_dates.append(f"{item['track']['album']['release_date']}")
        track_numbers.append(f"{item['track']['track_number']}")
        duration_ms.append(f"{convertMillisecondsToMinutesAndSeconds(item['track']['duration_ms'])}")

    # Create DataFrame
    data = {'Artist': artists,
            'Song': songs,
            'Album': albums,
            'TypeOfAlbum': typeOfAlbum,
            'TrackNumber': track_numbers,
            'AlbumReleaseDate': release_dates,
            'Duration': duration_ms }                 
    df = pd.DataFrame(data)

    
    playlists_name = row['Playlist']
    try:
        validate_filename(row['Playlist'])
    except ValidationError as e:
        playlists_name = sanitize_filename(row['Playlist'])
                           
                           
    df.to_csv(f"{myPlaylistsPath}/{playlists_name}.csv")
    print(f"{playlists_name}.csv has been saved...")

