""" Queries for PostgreSGL """

# create artist table
CREATE_ARTIST_TABLE = """
    CREATE TABLE IF NOT EXISTS artist (
        id varchar(22) PRIMARY KEY,
        name varchar(100),
        genres json,
        popularity integer,
        track_id varchar(22)
    );
"""

# track table
CREATE_TRACK_TABLE = """
    CREATE TABLE IF NOT EXISTS track (
        id varchar(22) PRIMARY KEY,
        name varchar(100),
        release_date date,
        popularity integer,
        duration integer,
        explicit boolean,
        danceability real,
        energy real,
        key integer,
        loudness real,
        mode integer,
        speechiness real,
        acousticness real,
        instrumentalness real,
        liveness real,
        valence real,
        tempo real,
        artist_id varchar(22)
    );
"""

#insert or do nothing
INSERT_ARTIST = """
    INSERT INTO artist (id, name, genres, popularity, track_id)
    VALUES(%s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING;
"""


INSERT_TRACK = """
    INSERT INTO track (id, name, release_date, popularity,
    duration, explicit, danceability, energy, key, loudness,
    mode, speechiness, acousticness, instrumentalness,
    liveness, valence, tempo, artist_id)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING;
"""
