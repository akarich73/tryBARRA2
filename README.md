# tryBARRA2

tryBARRA2 is a Python script to bulk download data from
BARRA2 reanalysis data for a specific latitude and longitude for use in 
Wind resource and energy assessments

> BARRA2 provides the Bureau's higher resolution regional atmospheric reanalysis
> over Australia and surrounding regions, spanning 1979-present day time period.
> When completed, it replaces the first version of BARRA (Su et al.,
> doi: 10.5194/gmd-14-4357-2021; 10.5194/gmd-12-2049-2019).
>
>It is produced using the Bureau's data assimilation system for numerical weather
> prediction - 4D variational scheme, and ACCESS as a limited-area dynamical
> coupled atmosphere-land model - Unified Model (UM) and JULES.
>
>The data set includes sub-daily, daily and monthly data for temperature,
> moisture, wind and flux variables at sub-surface, surface, and pressure levels,
> and heights above surface. The vertical levels include many pressure levels and
> several heights above surface.
>
>Data Provider: Bureau of Meteorology
>
>NCI Data Catalogue: https://dx.doi.org/10.25914/1x6g-2v48
>NCI THREDDS Data Server: https://dx.doi.org/10.25914/1x6g-2v48
>License: https://creativecommons.org/licenses/by/4.0/
>Extended Documentation: https://opus.nci.org.au/x/DgDADw

Source: https://thredds.nci.org.au/thredds/fileServer/ob53/BARRA2/README.txt

Data from BARRA2 can be downloaded in netCDF or CSV format from the NCI THREDDS server.

However, BARRA2 is structured with data for each variable saved in separate folders with separate files for each month. 
Therefore, for the purpose of downloading a subset of variables for a specific location, 
a recursive web request is required using the NetcdfSubset Data Access to get subsetted data.

This demonstration script provides examples to recursively download data in csv (for point data) relevant to wind farm resource analysis for
specific locations and time periods. 

The following links provide an example of the urls:

>
>Example URL for NetCDF grid files for ua50m wind speed:
> https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/ua50m/latest/ua50m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_197901-197901.nc?var=ua50m&north=-36&west=140&east=141&south=-37&horizStride=1&time_start=1979-01-01T00:00:00Z&time_end=1979-01-31T23:00:00Z&&&accept=netcdf3
>
>Or as grid points to get CSV files for ua50m wind speed:
>https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/ua50m/latest/ua50m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_197901-197901.nc?var=ua50m&latitude=-36&longitude=140&time_start=1979-01-01T00%3A00%3A00Z&time_end=1979-01-31T23%3A00%3A00Z&timeStride=&vertCoord=&accept=csv

For a full list of BARRA2 variables refer to the BARRA2 FAQ:
https://opus.nci.org.au/pages/viewpage.action?pageId=264241306

Refer to BARRA2 documentation for further details:
https://opus.nci.org.au/pages/viewpage.action?pageId=264241166

## Installation

Download, modify and run the script

## Usage

Modify the following CUSTOMS variables in the main.py file then run. 
Default values for testing are set to the centre of Australia for 2023.

>lat_lon_point = dict(latitude=-23.5527472, longitude=133.3961111)
>
>start_date_time = datetime.strptime("2023-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
end_date_time = datetime.strptime("2023-12-31T23:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
>
>barra2_variables = ["ua50m", "va50m", "ua100m", "va100m", "ua150m", "va150m", "ta50m"]
>
>output_filename_prefix = "demo_project"
>
You can also modify the GLOBALS if needed.

The script will (should) download individual files for each month and variable into the cache directory.
Then it will compile into a single csv file using a join with the first four columns as the key 
['time', 'station', 'latitude[unit="degrees_north"]', 'longitude[unit="degrees_east"]'].

If the individual files have already been downloaded with the same name in the cache directory they will be skipped. 

## Tests

For validation manually download files for latitude=-23.5527472, longitude=133.3961111 for 202301 are saved in the Tests folder.

>>https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/ua50m/latest/ua50m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202301-202301.nc/pointDataset.html
>
>>https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/va50m/latest/va50m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202301-202301.nc/pointDataset.html
>
> >https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/ta50m/latest/ta50m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202301-202301.nc/pointDataset.html

## Roadmap
1) Currently, AUS-11 1hr is implemented. Add option for AUS-22 and AUST-04
2) Implement bulk download for netCDF (for gridded data) 
3) Add download progress bar
4) Multi-location download
5) CLI interface

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Authors and acknowledgment

TJ Bodke

R Gledhill

## References

https://opus.nci.org.au/pages/viewpage.action?pageId=264241166
https://opus.nci.org.au/display/DAE/examples-thredds


## License

Creative Commons Attribution 4.0 International license
https://creativecommons.org/licenses/by/4.0/