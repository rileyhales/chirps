import requests
import os
import datetime
import glob
from PIL import Image
import netCDF4
import numpy
import sys
import logging


def download_chirps_gefs(threddspath):
    # get the parts of the timestamp to put into the url

    urlbase = 'https://data.chc.ucsb.edu/products/EWX/data/forecasts/CHIRPS-GEFS_precip/'

    startday = datetime.datetime.utcnow().strftime("%Y%m%d")
    _5dayend = (datetime.datetime.utcnow() + datetime.timedelta(days=4)).strftime("%Y%m%d")
    _10dayend = (datetime.datetime.utcnow() + datetime.timedelta(days=9)).strftime("%Y%m%d")
    _15dayend = (datetime.datetime.utcnow() + datetime.timedelta(days=14)).strftime("%Y%m%d")

    files_to_download = [
        '05day/precip_mean/data-mean_' + startday + '_' + _5dayend + '.tif',
        '10day/precip_mean/data-mean_' + startday + '_' + _10dayend + '.tif',
        '15day/precip_mean/data-mean_' + startday + '_' + _15dayend + '.tif',
    ]

    for file in files_to_download:
        url = urlbase + file
        filename = os.path.basename(file)
        filepath = os.path.join(threddspath, os.path.split(os.path.split(file)[0])[0] + '_' + filename)

        logging.info('Downloading- ' + file)
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
        except requests.HTTPError as e:
            errorcode = e.response.status_code
            logging.info('\nHTTPError ' + str(errorcode) + ' downloading ' + filename + ' from\n' + url)

    logging.info('Finished Downloads')
    return


def chirpsgefs_tifs_to_netcdfs(threddspath):
    # list the tifs to add to the netcdf
    tifs = glob.glob(os.path.join(threddspath, '*.tif'))
    tifs.sort()

    # make a new netcdf
    logging.info('Making the netcdf')
    nc_filepath = os.path.join(threddspath, 'chirpsgefs_' + datetime.datetime.utcnow().strftime("%Y%m%d") + '.nc4')
    new_nc = netCDF4.Dataset(nc_filepath, 'w')

    # create the variables and dimensions
    new_nc.createDimension('lat', 2000)
    new_nc.createDimension('lon', 7200)
    new_nc.createVariable(varname='lat', datatype='f4', dimensions='lat')
    new_nc.createVariable(varname='lon', datatype='f4', dimensions='lon')

    # create the lat and lon values
    new_nc['lat'][:] = [-50 + (.05 * i) for i in range(2000)]
    new_nc['lon'][:] = [-180 + (.05 * i) for i in range(7200)]

    # Create a variable and copy the values for each tif into the proper variable in the netcdf
    for tif in tifs:
        forecast_type = os.path.basename(tif)[0:2] + 'day'
        logging.info('Adding ' + forecast_type + ' to the netcdf')
        new_nc.createVariable(varname=forecast_type, datatype='f4', dimensions=('lat', 'lon'))
        raster = Image.open(os.path.join(threddspath, tif))
        new_nc[forecast_type][:] = numpy.array(raster)

        # delete the tif once we're done with it
        os.remove(tif)

    new_nc.close()


if __name__ == '__main__':
    # absolute path to the thredds data directory
    threddspath = sys.argv[1]

    # start logging
    logpath = os.path.join(threddspath, 'CHIRPS_GEFS_workflow.log')
    logging.basicConfig(filename=logpath, filemode='w', level=logging.INFO, format='%(message)s')
    logging.info('CHIRPS GEFS Workflow initiated on ' + datetime.datetime.utcnow().strftime("%D at %R"))

    # run the workflow
    download_chirps_gefs(threddspath)
    chirpsgefs_tifs_to_netcdfs(threddspath)
