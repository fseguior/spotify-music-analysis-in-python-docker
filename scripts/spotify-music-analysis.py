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


#results = sp.current_user_recently_played()
#for idx, item in enumerate(results['items']):
#   track = item['track']
#   print(idx, track['artists'][0]['name'], " – ", track['name'])


## La call a la API trae un Dictionary, en el cual anidado dentro de "items" tenes una lista. En esta lista hay un elemento por cada track escuchado. Cada elemento de esta lista es otro dictionario para el track, que tiene cosas en el root desde el ID, asi como mas dictionarios anidados con data como la de los albums, artistas, etc.


#%%
results = sp.current_user_recently_played()['items']
tracks=list()
for item in results:
    tracks.append(item['track']['id'])
    print(tracks)


#%%

a_feats=sp.audio_features(tracks)

featsDF=pd.DataFrame(a_feats)

featsDF=featsDF[["id","danceability","energy","key","loudness","mode", "speechiness", "acousticness","instrumentalness", "liveness", "valence", "tempo"]]

featsDF


#%%
featsDF.loc[ : ,featsDF.columns != 'id']

#%%% 
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering

kmeans=KMeans(n_clusters=4)
model=kmeans.fit(featsDF.loc[ : ,featsDF.columns != 'id'])
model

#%%


model.cluster_centers_
#%%
model.fit_predict(featsDF.loc[ : ,featsDF.columns != 'id'])
#%%
featsDF["clusterLabel"] = model.labels_
featsDF

#%%
print(model2)


#%%
aggCluster=AgglomerativeClustering(n_clusters=4)
model2=aggCluster.fit(featsDF.loc[ : ,featsDF.columns != 'id'])

featsDF["clusterLabel2"] = model2.labels_
featsDF


#%%
plt.scatter(featsDF["acousticness"], featsDF["instrumentalness"], c=featsDF["clusterLabel"])

#%%
plt.scatter(featsDF["acousticness"], featsDF["instrumentalness"], c=featsDF["clusterLabel2"])


#%%
featsArray=np.array(featsDF)
featsArray

#%%
from sklearn_som.som import SOM

spotify_som = SOM(m=3, n=1, dim=11)
modelSOM=spotify_som.fit(featsArray)

#%%
spotify_som.predict(featsArray)

featsLabel=["danceability","energy","key","loudness","mode", "speechiness", "acousticness","instrumentalness", "liveness", "valence", "tempo"]

#
fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(5,7))
x = featsArray[:,0]
y = featsArray[:,1]
colors = ['red', 'green', 'blue']

ax[0].scatter(x, y)
ax[0].title.set_text('Actual Classes')



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
