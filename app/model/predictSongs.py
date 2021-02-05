"""
Pass in specific song attributes to get similar suggestions from other artists!
"""

from joblib import load
import os
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model

# Load Models
autoencoder = load_model('autoencoder.h5')
model_1 = load_model('encoder.h5')
model_2 = load('nearestneighbor.joblib')
sub_key = load('sub_key0.joblib')
res_key = load('results_key1.joblib')


def wrangle_data(df):
    """
    Pass user query into wrangle function to normalize numerical values used
     for prediction and strip unused features from query.

    :input: Pandas.DataFrame of Song with 19 features

    return: Pandas.DataFrame with 12 features
    """

    # Copy the incoming df to prevent modifying the source df
    wrangled_df = df.copy()

    # Define the scale_values function to scale the larger values
    def scale_values(val_to_scale, old_min, old_max, new_min, new_max):
        old_range = (old_max - old_min)
        new_range = (new_max - new_min)
        return (((val_to_scale - old_min) * new_range) / old_range) + new_min

    # Scale 'popularity' from range 0-100 to range 0-1
    wrangled_df['popularity'] = wrangled_df['popularity'] / 100

    # Scale 'tempo' from range 0-250 to range 0-1
    # Include checks incase a new range increment is provided
    # WARN: Possible inaccuracy in ranges for values not in fit model
    min_val = min(0, wrangled_df['tempo'].min())
    max_val = max(250, wrangled_df['tempo'].max())
    # Perform scaling
    wrangled_df['tempo'] = wrangled_df['tempo'].apply(lambda x:
                                                      scale_values(x,
                                                                   min_val,
                                                                   max_val,
                                                                   0,
                                                                   1))

    # Scale 'loudness' from range -60-0 to range 0-1
    # WARN: Possible inaccuracy in ranges for values not in fit model
    min_val = min(-60, wrangled_df['loudness'].min())
    max_val = max(0, wrangled_df['loudness'].max())
    # Perform scaling
    wrangled_df['loudness'] = wrangled_df['loudness'].apply(lambda x:
                                                            scale_values(x,
                                                                         min_val,
                                                                         max_val,
                                                                         0,
                                                                         1))

    # Scale 'key' from range 0-11 to range 0-1
    # Include checks incase a new range increment is provided
    min_val = min(0, wrangled_df['key'].min())
    max_val = max(11, wrangled_df['key'].max())
    # Perform scaling
    wrangled_df['key'] = wrangled_df['key'].apply(lambda x:
                                                  scale_values(x,
                                                               min_val,
                                                               max_val,
                                                               0,
                                                               1))

    # Drop columns High Cardinality and Categorical values
    object_hc_cols = ['artists', 'name', 'release_date']
    wrangled_df = wrangled_df.drop(columns=object_hc_cols)

    # Drop columns found to improve the model when removed
    # ADDED `explicit` TO DROPPED COLs. -DF
    improve_drop_cols = ['year', 'duration_ms', 'explicit']
    wrangled_df = wrangled_df.drop(columns=improve_drop_cols)

    return wrangled_df


def get_pred(query_user):
    """
    Take in wrangled data and output predictions.
    DataFrame required

    returns: [List of track IDs]
    """
    step_0_pred = model_1.predict(query_user)
    step_1_pred = model_2.predict(step_0_pred)

    results_id = []

    for i in step_1_pred[1][0]:
        results_id.append(res_key.iloc[sub_key.iloc[i].name]['id'])

    return str(results_id)


# Testing Below: Simulating user input
raw_df = pd.read_csv('data.csv')
track_id = '5oUL6PknwhcBsAD1SU4xQg'
query = wrangle_data(raw_df[raw_df['id'] == track_id])
print(get_pred(query))
