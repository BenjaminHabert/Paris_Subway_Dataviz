"""
This module makes it easy to load / save files from the `data/` directory.
In particular we add functions to load frames from a .tif movie
"""
import os

import numpy as np
import pandas as pd

this_folder = os.path.dirname(__file__)
DATA_FOLDER = os.path.abspath(os.path.join(this_folder, '../data'))
print('[files.py]: data folder is: ' + DATA_FOLDER)


def inventory():
    """Print the list of files in the directory (goes into subfolders).
    Example
    -------
    >>> inventory()
    raw/
    raw/movie8.tif
    processed/
    processed/movie8_tracks.csv
    """
    for root, dirs, files in os.walk(DATA_FOLDER):
        local_root = root.replace(DATA_FOLDER, '')
        for file in files:
            print(os.path.join(local_root, file))


def create_abspath(relative_path, create_folders=True):
    """Return absolute path in the data/ folder."""
    if os.path.isabs(relative_path):
        raise ValueError('Can only save in a subfolder of ' + DATA_FOLDER)
    else:
        absolute_path = os.path.join(DATA_FOLDER, relative_path)
        if create_folders:
            os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
    return absolute_path



def _validate_dataframe_file_extension(absolute_path):
    """Return file extension if valid."""
    _, extension = os.path.splitext(absolute_path)
    valid_extensions = ['.csv', '.pickle']
    if extension not in valid_extensions:
        error_info = '\n'.join([
            'Cannot process file: ' + absolute_path,
            'Possible extensions are: ' + str(valid_extensions)
        ])
        raise ValueError(error_info)
    return extension


def save_dataframe(df, relative_path):
    """Save pandas dataframe as csv in the `data/` folder."""
    absolute_path = create_abspath(relative_path)
    extension = _validate_dataframe_file_extension(absolute_path)

    print('Saving dataframe to: ' + absolute_path)
    if extension == '.csv':
        df.to_csv(absolute_path, index=False, sep=',')
    elif extension == '.pickle':
        df.to_pickle(absolute_path)


def load_dataframe(relative_path):
    """Load pandas dataframe from path relative do data/ folder."""
    absolute_path = create_abspath(relative_path)
    extension = _validate_dataframe_file_extension(absolute_path)

    print('Loading dataframe from: ' + absolute_path)
    if extension == '.csv':
        return pd.read_csv(absolute_path)
    elif extension == '.pickle':
        return pd.read_pickle(absolute_path)
