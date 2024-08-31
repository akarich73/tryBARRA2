'''
tryBARRA2 is a demonstration Python script to bulk download data from BARRA2 reanalysis data
for a specific latitude and longitude. Refer to the readme for more details.
'''
# -*- coding: utf-8 -*-

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# -----------------------------------------------------------------------------
# Metadata
# -----------------------------------------------------------------------------
__author__ = 'TJ Bodke; R Gledhill'
__contact__ = 'github'
__copyright__ = 'Copyright (c) 2024, XXX'
__license__ = 'CC BY 4.0'
__date__ = '2024-08-22'
__version__ = '0.2024.8.22'

# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------

import os
import pathlib
import glob
import requests
import pandas as pd
from datetime import datetime, timedelta
import calendar

# -----------------------------------------------------------------------------
# GLOBALS
# -----------------------------------------------------------------------------

# base thredds url for BARRA2 11km 1hour reanalysis data
thredds_base_url_csv = "https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/{var}/latest/{var}_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_{year}{month:02d}-{year}{month:02d}.nc"

# output file format todo add list of output format options
point_output_format = "csv_file"
# grid_output_format = "netcdf3"

# relative directory for caching downloaded files
cache_dir = 'cache'
output_dir = 'output'

# -----------------------------------------------------------------------------
# CUSTOMS
# -----------------------------------------------------------------------------

# set location todo implement grid netCDF download
lat_lon_point = dict(latitude=-23.5527472, longitude=133.3961111)
# lat_lon_bbox = dict(north=-23.0, west=133.0, east=134.0, south=-24)

# set time ref https://stackoverflow.com/questions/17594298/date-time-formats-in-python
start_date_time = datetime.strptime("2023-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
end_date_time = datetime.strptime("2023-03-31T23:00:00Z", "%Y-%m-%dT%H:%M:%SZ")

# set list of BARRA2 variables to download default list is eastward wind (ua*), northward wind (va*), and air temperature at 50m (ta50m)
# barra2_variables = ["ua50m", "va50m", "ua100m", "va100m", "ua150m", "va150m", "ta50m"]
# optional limited variables to test
barra2_variables = ["ua50m", "va50m", "ta50m"]

# set output file custom name prefix to indicate a device or project location for the downloaded data
output_filename_prefix = "demo_project"


# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------

def create_dir(directory):
    '''Function to create directory if it doesn't exist

    Args:
        directory (str): relative directory

    Returns:
        Directory
    '''
    try:
        os.makedirs(directory)
        print(directory + ' directory created')
    except FileExistsError:
        print(directory + ' directory already exists')
        pass


def download_file(url, out_filename):
    '''Function to bulk download

    Args:
        url (str): url for file download
        out_filename (str): filename for download
    '''

    if not os.path.exists(out_filename):
        print(f"Downloading {url}")
        response = requests.get(url)
        with open(out_filename, 'wb') as f:
            f.write(response.content)

# -----------------------------------------------------------------------------
# RUNTIME PROCEDURE
# -----------------------------------------------------------------------------
def main():
    """runtime for tryBARRA2"""

    # create cache_dir if not exist
    create_dir(cache_dir)

    # generate list of months from input start and end datetime for url file loop
    # ref: https://stackoverflow.com/questions/17594298/date-time-formats-in-python
    dates = pd.date_range(start=start_date_time, end=end_date_time, freq='MS').to_pydatetime().tolist()

    # Loop through each variable and then each month between start and end datetime to download the relevant data
    for var in barra2_variables:
        # Loop through each month as each BARRA2 file is saved by month
        for date in dates:
            year = date.year
            month = date.month
            time_start = date.isoformat() + 'Z'
            # Get the number of days in the current month
            days_in_month = calendar.monthrange(year, month)[1]
            time_end = (date + timedelta(days=days_in_month) + timedelta(hours=-1)).isoformat() + 'Z'

            # update thredds_base_url and set as url for request
            url = thredds_base_url_csv.format(var=var, year=year, month=month)

            # add url parameters
            url += f'?var={var}&latitude={lat_lon_point['latitude']}&longitude={lat_lon_point['longitude']}&time_start={time_start}&time_end={time_end}&accept={point_output_format}'
            out_filename = os.path.join(cache_dir,
                                        f'{output_filename_prefix}_{var}_{time_start[:10]}_{time_end[:10]}.csv')

            if os.path.exists(out_filename):
                print('File already exists for ' + out_filename)
            else:
                print('Downloading and caching files for ' + out_filename)
                download_file(url, out_filename)

    # Loop through each variable and join the csv files

    # initiate dataframe for combined csv results
    df_combined = pd.DataFrame()

    for var in barra2_variables:

        # glob all csv files for the current project and var
        csv_files = pathlib.Path(cache_dir).glob(f'*{output_filename_prefix}_{var}*.csv')

        # concat csv files for the same var
        df_var_csv_concat = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)

        if df_combined.empty:
            df_combined = df_var_csv_concat
        else:
            # Otherwise, merge the current variable DataFrame with the combined DataFrame
            df_combined = df_combined.join(df_var_csv_concat.set_index(
                ['time', 'station', 'latitude[unit="degrees_north"]', 'longitude[unit="degrees_east"]']),
                on=['time', 'station', 'latitude[unit="degrees_north"]', 'longitude[unit="degrees_east"]'])

    # create dir for combined output if not exist
    create_dir(output_dir)

    # export combined to csv
    df_combined.to_csv(
        os.path.join(output_dir, f"{output_filename_prefix}_combined_{start_date_time.strftime("%Y%m%d")}_{end_date_time.strftime("%Y%m%d")}.csv"))


if __name__ == '__main__':
    main()
