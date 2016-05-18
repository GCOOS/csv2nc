#!/usr/bin/python2.7
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

#  Module      : generate_gcoos_nc_timeseries_atm.py
#  Author      : Felimon Gayanilo (felimon.gayanilo@gcoos.org)
#  Last update : 22 February 2016

#  Required    : numpy,netCDF4,netcdftime,sys,uuid,datetime
#  Usage       : generate_gcoos_nc_timeseries_atm.py
#  Purpose     : Generate netCDF (classic) in compliance to IOOS standard
#                based on the NCEI recommendations at https://sites.google.com/a/
#                 noaa.gov/ncei-ioos-archive/cookbook?pli=1#TOC-Providing-Data-Integrity 
#                 and in compliance with the NODC Profile Orthogonal specification at
#                 http://www.nodc.noaa.gov/data/formats/netcdf/v1.1/profileOrthogonal.cdl.

#                 Commented variables/attribute are provided for convenience that can 
#                 be added as the need arises. Also, this was written for atmospheric variables.
#                 If modified for oceanographic observations, do not forget to change 
#                 z to refer to 'depth' and not'altitude' for z attributes.

import numpy as np
import netCDF4
from netcdftime import utime
import datetime, pytz
import uuid
import csv
import os

# establish the date but always refer to the UTC 
datetime.datetime.now(pytz.timezone('US/Central')).isoformat()
dtutcnow = datetime.datetime.utcnow()
dt=datetime.date(dtutcnow.year, dtutcnow.month, dtutcnow.day).isoformat()

#  Set the base time for the NetCDF time variable.
cdftime = utime('hours since 1970-01-01 00:00:00')

##########################################################################
# define the in/out files to use. It is assumed here that the CSV and HDR files
# were pre-generated before running this routine. This can also be made to receive
# these input dynamically (i.e. as a passing paramter; recommended).

# be specific to where the file is, e.g. path ='/var/www/html/data/' if the output
# file is to be generated/stored in that path.

out_path = ''
in_path = ''                   
prefix  = 'gcoos_ioos_station_DISL_BSCA_2015_05_atm'
infiles = in_path+prefix+'.csv'
outfile = out_path+prefix+'.nc'
hdrfile = in_path+prefix+'.hdr'
period  = '2015_06'

# the following will be extracted from a header file
# (prefix+'.hdr') but listed here for demonstration purposes only.
organization      = 'Dauphin Island Sea Laboratory (DISL)'
urn               = 'urn:ioos:station:DISL:BSCA'
url               = 'http://www.mymobilebay.com/stationdata/StationInfo.asp?jday=&property=&chartyear=&StationID=106'
description       = 'Station Bon Secour, LA'
naming            = 'ioos:station:DISL'
instrument        = 'RM Young 61202V, RM Young 41372VC/Analog 1 V Single'
instrument_desc   = 'Atmospheric probe and wind sensor'
wmo               = ''
latitude          = 30.3288
longitude         =-87.8293
verticalPosition  = 3.0
timeseries_length = 880
urnSensor1        = 'urn:ioos:station:DISL:BSCA:airPressure1'
urnSensor2        = 'urn:ioos:station:DISL:BSCA:airTemperature1'

##########################################################################

file = outfile
print 'Please wait, generating %s...\n' % file

Try:
    # NCEI supports on the netCDF4 classic (as of 2016-01-31)
    nc = netCDF4.Dataset(file,'w',format='NETCDF4_CLASSIC')
    
    # create dimensions
    ts = nc.createDimension('timeSeries',None)
    
    # Add global attributes as per the template
    nc.ncei_template_version    = 'NCEI_NetCDF_TimeSeries_Orthogonal_Template_v2.0'
    nc.featureType              = 'timeSeries'
    nc.title                    = 'GCOOS netCDF Data for '+urn+' for the period '+period
    nc.summary                  = period+' time series data for '+urn+' platform served via GCOOS Data Portal. The uuid was generated using the uuid python module, invoking the command uuid.uuid4().'
    nc.keywords                 = 'EARTH SCIENCE>OCEANS>OCEAN CIRCULATION>OCEAN CURRENTS,EARTH SCIENCE>TERRESTRIAL HYDROSPHERE>WATER QUALITY/WATER CHEMISTRY>CHLOROPHYLL,EARTH SCIENCE>OCEANS>OCEAN CHEMISTRY>OXYGEN,EARTH SCIENCE>OCEANS>COASTAL PROCESSES>SEA SURFACE HEIGHT,EARTH SCIENCE>OCEANS>SEA SURFACE TOPOGRAPHY>SEA SURFACE HEIGHT,EARTH SCIENCE>OCEANS>SALINITY/DENSITY>SALINITY,EARTH SCIENCE>OCEANS>OCEAN TEMPERATURE>WATER TEMPERATURE'
    nc.keywords_vocabulary      = 'GCMD Science Keywords Version 8.1'
    nc.Conventions              = 'CF1.6, ACDD-1.3'
    # the filename is a unique identification and will be used as the file id
    nc.id                       = prefix
    nc.naming_authority         = naming
    # assume the version to be original, change if otherwise.
    nc.history                  = 'V1 '+dt
    nc.source                   = 'LDN SOS endpoint'
    nc.processing_level         = 'Data ingested as provided.'
    nc.comment                  = 'Data generated from GCOOS tables.'
    nc.acknowledment            = ''
    nc.license                  = 'Creative Common (CC) 0'
    nc.standard_name_vocabulary = 'CF Standard Name Table v33'
    nc.date_ceated              = 'Created:'+dt
    nc.creator_name             = '<your name here>'
    nc.creator_email            = '<your official email here>'
    nc.creator_url              = '<your official URL here>'
    nc.institution              = 'Gulf of Mexico Coastal Ocean Observing System (GCOOS)'
    nc.project                  = 'Gulf of Mexico Coastal Ocean Observing System (GCOOS)'
    nc.publisher_name           = 'Gulf of Mexico Coastal Ocean Observing System (GCOOS)'
    nc.publisher_email          = 'info@gcoos.org'
    nc.publisher_url            = 'data.gcoos.org'
    #nc.geospatial_bounds        = ''
    #nc.geospatial_bounds_crs    = ''
    #nc.geospatial_bounds_vertical_crs = ''
    nc.geospatial_lat_min       = latitude
    nc.geospatial_lat_max       = latitude
    nc.geospatial_lon_min       = longitude
    nc.geospatial_lon_max       = longitude
    nc.geospatial_vertical_min  = verticalPosition
    nc.geospatial_vertical_max  = verticalPosition
    nc.geospatial_vertical_positive = 'up'
    #nc.time_coverage_start      = '00:00'
    #nc.time_coverage_end        = '23:59' 
    #nc.time_coverage_duration   = ''
    #nc.time_coverage_resolution = ''
    nc.uuid                     = str(uuid.uuid4())
    nc.sea_name                 = 'Gulf of Mexico'
    nc.creator_type             = 'institution'
    nc.creator_institution      = 'Gulf of Mexico Coastal Ocean Observing System (GCOOS)'
    nc.publisher_type           = 'institution'
    nc.publisher_institution    = 'Gulf of Mexico Coastal Ocean Observing System (GCOOS)'
    nc.institution              = 'Texas A&M University'
    nc.program                  = 'NOAA IOOS'
    nc.contributor_name         = organization
    nc.contributor_role         = 'Local Data Node'
    nc.geospatial_lat_units     = 'degrees_north' 
    nc.geospatial_lon_units     = 'degrees_east'
    nc.geospatial_vertical_units = 'EPSG:4979'
    nc.date_modified            = dt
    nc.date_issued              = '' 
    nc.date_metadata_modified   = dt
    nc.product_version          = 'Ver. 1.0'
    nc.platform                 = urn
    nc.platform_vocabulary      = 'CF Standard Name Table v33, GCMD Earth Science Keywords. Version 8.1'
    nc.instrument               = ''
    nc.instrument_vocabulary    = 'GCMD Earth Science Keywords. Version 8.1'
    nc.cdm_data_type            = 'Station'
    nc.metadata_link            = ''
    nc.references               = ''
    
    #  variable attributes #
    timeseries                  = nc.createVariable('timeSeries','i',('timeSeries'))
    timeseries.long_name        = description
    timeseries.cf_role          = 'timeseries_id'
    
    times                       = nc.createVariable('time','d',('time','timeSeries'))
    times.long_name             = 'Time'
    times.standard_name         = 'time'
    times.units                 = 'seconds since 1970-01-01 00:00:00 UTC'
    times.calendar              = 'julian'
    times.axis                  = 'T'
    times.ancillary_variables   = ''
    times.comment               = ''
    
    lat                         = nc.createVariable('lat','d',('timeSeries'))
    lat.long_name               = 'Latitude'
    lat.standard_name           = 'latitude'
    lat.units                   = 'degrees_north'
    lat.axis                    = 'Y'
    lat.valid_min               = -90.00
    lat.valid_max               = 90.00
    #lat._FillValue              = fill_value=-999.
    lat.ancillary_variables     = ''
    lat.comment                 = ''
    
    lon                         = nc.createVariable('lon','d',('timeSeries'))
    lon.long_name               = 'Longitude'
    lon.standard_name           = 'longitude'
    lon.units                   = 'degrees_east'
    lon.axis                    = 'X'
    lon.valid_min               = -180.00
    lon.valid_max               = 180.00
    #lat._FillValue              = fill_value=-999.
    lon.ancillary_variables     = ''
    lon.comment                 = ''
    
    z                           = nc.createVariable('z','d',('timeSeries'),fill_value=-999.)
    z.long_name                 = "Altitude"
    z.standard_name             = "altitude"
    z.units                     = "m"
    z.axis                      = "Z"
    z.positive                  = "up"
    #z.valid_min                 = 0.0
    #z.valid_max                 = 0.0
    #z._FillValue                = fill_value=-999.
    z.ancillary_variables       = ""
    z.comment                   = ""
    
    # create a loop to define all the instruments in the platform, assumed here to have only one sensor of each type
    instrument                        = nc.createVariable('instrument1','c',())
    instrument.long_name              = 'Air Pressure Sensor'
    instrument.instrument_vocabulary  = 'GCMD Science Keywords Version 8.1'

    #instrument.make_model             = ''
    #instrument.serial_number          = ''
    #instrument.calibration_date       = ''
    #instrument.factory_calibrated     = ''
    #instrument.user_calibrated        = ''
    #instrument.calibration_report     = ''
    #instrument.accuracy               = ''
    #instrument.valid_range            = ''
    #instrument.precision              = ''
    #instrument.comment                = ''
    instrument.ioos_code              = urnSensor1
    
    instrument                        = nc.createVariable('instrument2','c',())
    instrument.long_name              = 'Thermometers'
    instrument.instrument_vocabulary  = 'GCMD Science Keywords Version 8.1'

    #instrument.make_model             = ''
    #instrument.serial_number          = ''
    #instrument.calibration_date       = ''
    #instrument.factory_calibrated     = ''
    #instrument.user_calibrated        = ''
    #instrument.calibration_report     = ''
    #instrument.accuracy               = ''
    #instrument.valid_range            = ''
    #instrument.precision              = ''
    #instrument.comment                = ''
    instrument.ioos_code              = urnSensor2

    # add all the all the rest of the sensors
    
    platform                    = nc.createVariable('platform','c',('timeSeries'))
    platform.long_name          = description
    platform.comment            = ''
    platform.call_sign          = ''
    platform.ncei_code          = '147F, 3614'
    platform.wmo_code           = wmo
    platform.imo_code           = ''
    platform.ioos_code          = urn
    
    crs                         = nc.createVariable('crs','i',())
    crs.grid_mapping_name       = 'latitude_longitude'
    crs.epsg_code               = 'EPSG:4326'
    crs.semi_major_axis         = 6378137
    crs.inverse_flattening      = 298.257223563
    
    obs1                        = nc.createVariable('air_pressure','d',('timeSeries'),fill_value=-999.)
    obs1.long_name              = 'air pressure'
    obs1.standard_name          = 'air_pressure'
    obs1.ncei_name              = 'air_pressure'
    obs1.units                  = 'mbar'
    obs1.scale_factor           = 1.
    obs1.add_offset             = 0.
    #obs1._FillValue             = fill_value=-999.
    obs1.missing_value          = -999.
    obs1.valid_min              = 700.
    obs1.valid_max              = 1040.
    obs1.coordinates            = 'time lat lon'
    obs1.coverage_content_type  = 'physicalMeasurement'
    obs1.grid_mapping           = 'crs'
    obs1.source                 = 'GCOOS LDN upload/SOS.'
    obs1.references             = url
    obs1.cell_methods           = 'time: point lat: point lon: point'
    obs1.ancillary_variables    = 'instrument platform'
    obs1.platform               = 'platform'
    obs1.instrument             = 'instrument1'
    obs1.comment                = ''
    
    obs2                        = nc.createVariable('air_temperature','d',('timeSeries'),fill_value=-999.)
    obs2.long_name              = 'air_temperature'
    obs2.standard_name          = 'air_temperature'
    obs2.ncei_name              = 'air_temperature'
    obs2.units                  = 'Celsius'
    obs2.scale_factor           = 1.
    obs2.add_offset             = 0.
    #obs2._FillValue             = fill_value=-999.
    obs2.missing_value          = -999.
    obs2.valid_min              = -10.
    obs2.valid_max              = 40.
    obs2.coordinates            = 'time lat lon'
    obs2.coverage_content_type  = 'physicalMeasurement'
    obs2.grid_mapping           = 'crs'
    obs2.source                 = 'GCOOS LDN upload/SOS.'
    obs2.references             = url
    obs2.cell_methods           = 'time: point lat: point lon: point'
    obs2.ancillary_variables    = 'instrument platform'
    obs2.platform               = 'platform'
    obs2.instrument             = 'instrument2'
    obs2.comment                = ''
    
    obs3                        = nc.createVariable('dew_point_temperature','d',('timeSeries'),fill_value=-999.)
    obs3.long_name              = 'dew_point_temperature'
    obs3.standard_name          = 'dew_point_temperature'
    obs3.ncei_name              = 'dew_point_temperature'
    obs3.units                  = 'Celsius'
    obs3.scale_factor           = 1.
    obs3.add_offset             = 0.
    #obs3._FillValue             = fill_value=-999.
    obs3.missing_value          = -999.
    obs3.valid_min              = -10.
    obs3.valid_max              = 40.
    obs3.coordinates            = 'time lat lon'
    obs3.coverage_content_type  = 'physicalMeasurement'
    obs3.grid_mapping           = 'crs'
    obs3.source                 = 'GCOOS LDN upload/SOS.'
    obs3.references             = url
    obs3.cell_methods           = 'time: point lat: point lon: point'
    obs3.ancillary_variables    = 'instrument platform'
    obs3.platform               = 'platform'
    obs3.instrument             = 'instrument3'
    obs3.comment                = ''
    
    obs4                        = nc.createVariable('relative_humidity','d',('timeSeries'),fill_value=-999.)
    obs4.long_name              = 'relative humidity'
    obs4.standard_name          = 'relative_humidity'
    obs4.ncei_name              = 'relative_humidity'
    obs4.units                  = '%'
    obs4.scale_factor           = 1.
    obs4.add_offset             = 0.
    #obs4._FillValue             = fill_value=-999.
    obs4.missing_value          = -999.
    obs4.valid_min              = 0.
    obs4.valid_max              = 105.
    obs4.coordinates            = 'time lat lon'
    obs4.coverage_content_type  = 'physicalMeasurement'
    obs4.grid_mapping           = 'crs'
    obs4.source                 = 'GCOOS LDN upload/SOS.'
    obs4.references             = url
    obs4.cell_methods           = 'time: point lat: point lon: point'
    obs4.ancillary_variables    = 'instrument platform'
    obs4.platform               = 'platform'
    obs4.instrument             = 'instrument4'
    obs4.comment                = ''
    
    obs5                        = nc.createVariable('wind_speed','d',('timeSeries'),fill_value=-999.)
    obs5.long_name              = 'wind speed'
    obs5.standard_name          = 'wind_speed'
    obs5.ncei_name              = 'wind_speed'
    obs5.units                  = 'm s-1'
    obs5.scale_factor           = 1.
    obs5.add_offset             = 0.
    #obs5._FillValue             = fill_value=-999.
    obs5.missing_value          = -999.
    obs5.valid_min              = 0.
    obs5.valid_max              = 150.
    obs5.coordinates            = 'time lat lon'
    obs5.coverage_content_type  = 'physicalMeasurement'
    obs5.grid_mapping           = 'crs'
    obs5.source                 = 'GCOOS LDN upload/SOS.'
    obs5.references             = url
    obs5.cell_methods           = 'time: point lat: point lon: point'
    obs5.ancillary_variables    = 'instrument platform'
    obs5.platform               = 'platform'
    obs5.instrument             = 'instrument5'
    obs5.comment                = ''
    
    obs6                        = nc.createVariable('wind_speed_of_gust','d',('timeSeries'),fill_value=-999.)
    obs6.long_name              = 'wind speed of gust'
    obs6.standard_name          = 'wind_speed_of_gust'
    obs6.ncei_name              = 'wind_speed_of_gust'
    obs6.units                  = 'm s-1'
    obs6.scale_factor           = 1.
    obs6.add_offset             = 0.
    #obs6._FillValue             = fill_value=-999.
    obs6.missing_value          = -999.
    obs6.valid_min              = 0.
    obs6.valid_max              = 250.
    obs6.coordinates            = 'time lat lon'
    obs6.coverage_content_type  = 'physicalMeasurement'
    obs6.grid_mapping           = 'crs'
    obs6.source                 = 'GCOOS LDN upload/SOS.'
    obs6.references             = url
    obs6.cell_methods           = 'time: point lat: point lon: point'
    obs6.ancillary_variables    = 'instrument platform'
    obs6.platform               = 'platform'
    obs6.instrument             = 'instrument6'
    obs6.comment                = ''
    
    obs7                        = nc.createVariable('wind_to_direction','d',('timeSeries'),fill_value=-999.)
    obs7.long_name              = 'wind to direction'
    obs7.standard_name          = 'wind_to_direction'
    obs7.ncei_name              = 'wind_to_direction'
    obs7.units                  = 'degrees_true'
    obs7.scale_factor           = 1.
    obs7.add_offset             = 0.
    #obs7._FillValue             = fill_value=-999.
    obs7.missing_value          = -999.
    obs7.valid_min              = 0.
    obs7.valid_max              = 360.
    obs7.coordinates            = 'time lat lon'
    obs7.coverage_content_type  = 'physicalMeasurement'
    obs7.grid_mapping           = 'crs'
    obs7.source                 = 'GCOOS LDN upload/SOS.'
    obs7.references             = url
    obs7.cell_methods           = 'time: point lat: point lon: point'
    obs7.ancillary_variables    = 'instrument platform'
    obs7.platform               = 'platform'
    obs7.instrument             = 'instrument7'
    obs7.comment                = ''
    
    # Read/Write the data matrix from a CSV file
    
    data = np.genfromtxt(infiles,dtype=[('date','S10'),('time','S8'),\
    ('air_pressure','f8'),('air_temperature','f8'),('dew_point_temperature','f8'),\
    ('relative_humidity','f8'),('wind_speed','f8'),('wind_speed_of_gust','f8'),\
    ('wind_to_direction','f8')],delimiter=",",skip_header=1)
    

    for i in range(0,timeseries_length):
        year   = int(data[i][0].split('-')[0])
        month  = int(data[i][0].split('-')[1])
        day    = int(data[i][0].split('-')[2])
        hour   = int(data[i][1].split(':')[0])
        minute = int(data[i][1].split(':')[1])
        second = int(data[i][1].split(':')[2])
    
        dateobj = datetime.datetime(year,month,day,hour,minute,second)
        time = cdftime.date2num(dateobj)
        times[i] = rountd(time*3600)
        
        timeseries[i]=i+1
        lon[i] = longitude
        lat[i] = latitude
        z[i] = verticalPosition
    
        obs1[i] = data[i][2]
        obs2[i] = data[i][3]
        obs3[i] = data[i][4]
        obs4[i] = data[i][5]
        obs5[i] = data[i][6]
        obs6[i] = data[i][7]
        obs7[i] = data[i][8]
    
    nc.close()
except:
    print "Error in file: "+outfile+". \n"
    os.remove(outfiles)
