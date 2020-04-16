import os
import glob
from .app import Chirps as App


def get_forecast_netcdf_names():
    threddspath = App.get_custom_setting('thredds_path')
    netcdfs = glob.glob(os.path.join(threddspath, '*.nc4'))

    reference = {}
    for nc in netcdfs:
        file = os.path.basename(nc)
        if file.startswith('chirpsgefs'):
            reference['gefs'] = os.path.basename(file)

    return reference
