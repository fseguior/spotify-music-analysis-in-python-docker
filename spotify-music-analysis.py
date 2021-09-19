#In[1]

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import spotipy as sp

##from spotipy.oauth2 import SpotifyOAuth

# %%
#Authentication with Spotify

import credentials as cred

scope = 'user-read-recently-played user-library-read'

sp = sp.Spotify(auth_manager=sp.oauth2.SpotifyOAuth(client_id=cred.client_ID, client_secret= cred.client_SECRET, redirect_uri=cred.redirect_url, scope=scope))


# %%

results = sp.current_user_recently_played()
for idx, item in enumerate(results['items']):
   track = item['track']
   print(idx, track['artists'][0]['name'], " – ", track['name'])



## La call a la API trae un Dictionary, en el cual anidado dentro de "items" tenes una lista. En esta lista hay un elemento por cada track escuchado. Cada elemento de esta lista es otro dictionario para el track, que tiene cosas en el root desde el ID, asi como mas dictionarios anidados con data como la de los albums, artistas, etc.


#%%
results = sp.current_user_recently_played()['items']
tracks=list()
for item in results:
    tracks.append(item['track']['id'])
    print(tracks)


#%%

a_feats=sp.audio_features(tracks)
print(a_feats)

type(a_feats[1])


#"danceability","energy","key","loudness","mode", "speechiness", "acousticness","instrumentalness", "liveness", "valence", "tempo"
#%%
featsDF=pd.DataFrame(a_feats)

featsDFClean=featsDF[["danceability","energy","key","loudness","mode", "speechiness", "acousticness","instrumentalness", "liveness", "valence", "tempo"]]


#%%% 
from sklearn.cluster import KMeans

kmeans=KMeans(n_clusters=3)
model=kmeans.fit(featsDFClean)
model

#%%
from sklearn_som.som import SOM
#%%

# Johann Sebastian Bach
urn = 'spotify:artist:5aIqB5nVVvmFsvSdExz408'

artist = sp.artist(urn)
print(artist)


# Ed Sheeran
urn2 = 'spotify:artist:6eUKZXaKkcviH0Ku9w2n3V'

artist2 = sp.artist(urn2)
print(artist2)




# %%

sp.current_user_saved_tracks(limit=100)

# %%
