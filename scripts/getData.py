## Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth

client_ID='76547a2039e2480c8c86946d4889c701'
client_SECRET='01eb814818ed4655ac6442e2b75691c1'   
redirect_url='http://localhost:9000'

#Authentication with Spotify
import credentials as cred

scope = 'user-read-recently-played user-library-read'

sp_auth = sp.Spotify(auth_manager=sp.oauth2.SpotifyOAuth(client_id=cred.client_ID, client_secret= cred.client_SECRET, redirect_uri=cred.redirect_url, scope=scope))

##API call, recently played tracks

results = sp_auth.current_user_recently_played()['items']
tracks=list()
for item in results:
    tracks.append(item['track']['id'])

a_feats=sp_auth.audio_features(tracks)

featsDF=pd.DataFrame(a_feats)

featsDF=featsDF[["id","danceability","energy","key","loudness","mode", "speechiness", "acousticness","instrumentalness", "liveness", "valence", "tempo"]]

featsDF

featsCSV=featsDF.to_csv(path_or_buf="/app/data/data.csv", index=False)

print(featsCSV)

