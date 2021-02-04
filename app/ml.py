"""Machine learning functions"""

import logging
import random
import json
import datetime

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator
import psycopg2
from os import getenv
from dotenv import load_dotenv
from app.queries import *


log = logging.getLogger(__name__)
router = APIRouter()


load_dotenv()
dbname = getenv("DB")
user = getenv("USER")
password = getenv("PASSWORD")
host = getenv("HOST")
SPOTIFY_ID = getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET = getenv("SPOTIFY_CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_ID,
                                                            client_secret=SPOTIFY_SECRET))


conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
curs = conn.cursor()

class SongURL(BaseModel):
    """ URL to song methods """
    x1: str = Field(..., example='https://open.spotify.com/track/1oqrEcuxbzibmFx8Ebn4Z6')

    def create_tables(self):
        """ Create tables if not created """
        curs.execute(CREATE_ARTIST_TABLE)
        curs.execute(CREATE_TRACK_TABLE)
        conn.commit()

    def get_data(self):
        """ Insert into db"""
        track_id = self.x1[-22:]
        searchsong = sp.track(track_id)

        feats = sp.audio_features(track_id)

        artist_id = searchsong['artists'][0]['id']
        searchart = sp.artist(artist_id)

        track_values = ((track_id), (searchsong['name']), (searchsong['album']['release_date']),
            (searchsong['popularity']), (searchsong['duration_ms']), (searchsong['explicit']),
            (feats[0]['danceability']), (feats[0]['energy']), (feats[0]['key']), (feats[0]['loudness']), (feats[0]['mode']),
            (feats[0]['speechiness']), (feats[0]['acousticness']), (feats[0]['instrumentalness']), (feats[0]['liveness']),
            (feats[0]['valence']), (feats[0]['tempo']), (artist_id)
        )
        artist_values = ((artist_id), (searchart['name']), (json.dumps(searchart['genres'])), (searchart['popularity']), (track_id))

        curs.execute(INSERT_ARTIST, artist_values)
        curs.execute(INSERT_TRACK, track_values)
        conn.commit()

    def to_df(self):
        """ DB to DF for predicting
        i have more columns than they used in model, will wait for their final
        """
        track_id = self.x1[-22:]
        data = f"'{track_id}'"
        query = ("""
        SELECT t.*, a.name AS artists
        FROM track AS t
        INNER JOIN artist AS a
        ON t.id = a.track_id
        WHERE t.id=%s;""" % data)
        df = pd.read_sql(sql=query, con=conn, parse_dates=['release_date'])
        df['year'] = df['release_date'].apply(lambda x: int(x.year) if x.date else x)
        df['explicit'] = df['explicit'].apply(lambda x:1 if True else 0)
        
        return df

    def return_id(self):
        """ Get just track id """
        track_id = self.x1[-22:]
        return track_id

    def artist_info(self):
        """ Return artist information"""
        track_id = self.x1[-22:]
        data = f"'{track_id}'"
        art_quer = ("SELECT name, genres FROM artist WHERE track_id=%s;" % data)
        curs.execute(art_quer)
        return curs.fetchall()
    
    def track_info(self):
        """ Return track information """
        track_id = self.x1[-22:]
        data = f"'{track_id}'"
        tra_quer = ("SELECT name, release_date FROM track WHERE id=%s;" % data)
        curs.execute(tra_quer)
        return curs.fetchall()

    def return_url(self, track):
        """ Return Spotify link back to user """
        begin = "https://open.spotify.com/track/"
        return str(begin + track)



@router.post('/predict')
async def predict(url: SongURL):
    """
    Copy & Paste a song URL from Spotify to get new music recommendations!

    ### Request Body
    - `x1`: Spotify song URL
    Format : https://open.spotify.com/track/xxxxxxxxxxxxxxxxxxxxxx

    ### Response
    - `prediction`: boolean, at random
    - `predict_proba`: float between 0.5 and 1.0, 
    representing the predicted class's probability

    """
    url.get_data()
    
    df = url.to_df()

    return {
        'artist': url.artist_info(),
        'genres': url.track_info(),
        'song title': url.return_url("jdkhvfdjhvfjd"),
    }
