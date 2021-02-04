"""Data visualization functions"""

from fastapi import APIRouter, HTTPException
import pandas as pd
import plotly.express as px
import spotipy
from app.ml import sp

router = APIRouter()


@router.get('/viz')
async def viz(url: str):
    """
    Visualize a song's audio features from Spotify!

    ### Path Parameter
    Just copy & paste the song URL into here!
    Format : https://open.spotify.com/track/xxxxxxxxxxxxxxxxxxxxxx

    ### Response
    JSON string to render with [react-plotly.js](https://plotly.com/javascript/react/)
    """
    begin = "https://open.spotify.com/track/"
    if url.startswith(begin) is False:
        raise HTTPException(status_code=404, detail=f'Spotify URL not found')

    # Get track from ID
    track = url[-22:]
    song = sp.audio_features(track)
    feats = {
    'danceability': song[0]['danceability'],
    'energy': song[0]['energy'],
    'key': song[0]['key'],
    'loudness': song[0]['loudness'],
    'mode': song[0]['mode'],
    'speechiness': song[0]['speechiness'],
    'acousticness': song[0]['acousticness'],
    'instrumentalness': song[0]['instrumentalness'],
    'liveness': song[0]['liveness'],
    'valence': song[0]['valence'],
    'tempo': song[0]['tempo']
    }
    
    # Get Track Name
    namesearch = sp.track(track)
    name = namesearch['name']

    # Make Plotly figure
    fig = px.bar(x= feats.keys(), y=feats.values(), title=f'{name} Audio Features')
    # Return Plotly figure as JSON string
    return fig.to_json()
