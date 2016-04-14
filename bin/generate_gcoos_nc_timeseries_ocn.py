#!/usr/bin/python2.7
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

#  Module      : generate_gcoos_nc_timeseries_ocn.py
#  Author      : Felimon Gayanilo (felimon.gayanilo@gcoos.org)
#  Last update : 16 February 2016

#  Required    : numpy,netCDF4,netcdftime,sys,uuid,datetime
#  Usage       : generate_gcoos_nc_timeseries_ocn.py
#  Purpose     : Generate netCDF (classic) in compliance to IOOS standard
#                based on the NCEI recommendations at https://sites.google.com/a/
#                 noaa.gov/ncei-ioos-archive/cookbook?pli=1#TOC-Providing-Data-Integrity 
#                 and in compliance with the NODC Profile Orthogonal specification at
#                 http://www.nodc.noaa.gov/data/formats/netcdf/v1.1/profileOrthogonal.cdl.

#                 Commented variables/attribute are provided for convenience that can 
#                 be added as the need arises. Also, this was written for atmospheric variables.
#                 If modified for oceanographic observations, do not forget to change 
#                 z to refer to 'altitude' and not'depth' for z attributes.

import numpy as np
import netCDF4
from netcdftime import utime
import datetime, pytz
import uuid
import csv
import os

from os import listdir

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
prefix  = 'gcoos_ioos_station_DISL_BSCA_2015_11_ocn'
infiles = in_path+prefix+'.csv'
outfile = out_path+prefix+'.nc'
hdrfile = in_path+prefix+'.hdr'
period  = '2015_11'

# the following will be extracted from a header file (prefix+'.hdr') 
# but listed here abbreviated and for demonstration purposes only (e.g.
# this station reads data .

urn               = 'ioos:station:DISL:BSCA'
url               = 'http://www.mobilebaynep.com/'
description       = 'BSCA: Station Bon Secour, LA'
naming            = 'ioos:station:DISL'
instrument        = 'YSI 6600'
instrument_desc   = 'Salinity calculated from conductivity and water temperature'
wmo               = ''
latitude          = 30.3288
longitude         =-87.8293
verticalPosition  = 0.
timeseries_length = 640

##########################################################################

file = outfile
print 'Please wait, generating %s...\n' % file
try:
    # NCEI supports on the netCDF4 classic (as of 2016-01-31)
    nc = netCDF4.Dataset(file,'w',format='NETCDF4_CLASSIC')
    
    # create dimensions
    ts = nc.createDimension('timeSeries',None)
    
    # Add global attributes as per the template
    nc.ncei_template_version    = 'NCEI_NetCDF_TimeSeries_Orthogonal_Template_v2.0'
    nc.featureType              = 'timeSeries'
    nc.title                    = 'GCOOS netCDF Data for '+urn+' for the period '+period
    nc.summary                  = '2016-11 time series data for '+urn+' platform served via GCOOS Data Portal. The uuid was generated using the uuid python module, invoking the command uuid.uuid4().'
    nc.keywords                 = 'GCOOS,ocean observing,sensors'
    nc.Conventions              = 'CF Standard Name Table v26, GCMD Earth Science Keywords. Version 5.3.3'
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
    nc.standard_name_vocabulary = 'CF Standard Name Table v26'
    nc.date_ceated              = 'Created:'+dt
    nc.creator_name             = 'Felimon Gayanilo'
    nc.creator_email            = 'felimon.gayanilo@gcoos.org'
    nc.creator_url              = 'https://www.linkedin.com/in/felimon-gayanilo-56728418'
    nc.institution              = 'Gulf of Mexico Coastal Ocean Observing System (GCOOS)'
    nc.project                  = ''
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
    nc.geospatial_vertical_positive = 'down'
    #nc.time_coverage_start      = '00:00'
    #nc.time_coverage_end        = '23:59' 
    #nc.time_coverage_duration   = ''
    #nc.time_coverage_resolution = ''
    nc.uuid                     = str(uuid.uuid4())
    nc.sea_name                 = 'Gulf of Mexico, United States of America'
    nc.creator_type             = 'institution'
    nc.creator_institution      = 'Gulf of Mexico Coastal Ocean Observing System (GCOOS)'
    nc.publisher_type           = 'institution'
    nc.publisher_institution    = 'Gulf of Mexico Coastal Ocean Observing System (GCOOS)'
    nc.program                  = 'NOAA IOOS'
    nc.contributor_name         = ''
    nc.contributor_role         = ''
    nc.geospatial_lat_units     = 'degrees_north' 
    nc.geospatial_lon_units     = 'degrees_east'
    nc.geospatial_vertical_units = 'EPSG:4979'
    nc.date_modified            = dt
    nc.date_issued              = '' 
    nc.date_metadata_modified   = dt
    nc.product_version          = 'Ver. 1.0'
    nc.platform                 = urn
    nc.platform_vocabulary      = 'CF Standard Name Table v26, GCMD Earth Science Keywords. Version 5.3.3'
    nc.instrument               = ''
    nc.instrument_vocabulary    = 'CF Standard Name Table v26, GCMD Earth Science Keywords. Version 5.3.3'
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
    z.long_name                 = "Depth"
    z.standard_name             = "depth"
    z.units                     = "m"
    z.axis                      = "Z"
    z.positive                  = "down"
    #z.valid_min                 = 0.0
    #z.valid_max                 = 0.0
    #z._FillValue                = fill_value=-999.
    z.ancillary_variables       = ""
    z.comment                   = ""
    
    instrument                 = nc.createVariable('instrument','c',('timeSeries'))
    instrument.long_name       = instrument
    instrument.comment         = instrument_desc
    
    platform                    = nc.createVariable('platform','c',('timeSeries'))
    platform.long_name          = urn,' ',description
    platform.comment            = ''
    platform.call_sign          = ''
    platform.ncei_code          = '147F, 3614'
    platform.wmo_code           = wmo
    platform.imo_code           = ''
    
    crs                         = nc.createVariable('crs','i',())
    crs.grid_mapping_name       = 'latitude_longitude'
    crs.epsg_code               = 'EPSG:4326'
    crs.semi_major_axis         = 6378137
    crs.inverse_flattening      = 298.257223563
    
    obs1                        = nc.createVariable('sea_water_speed','d',('timeSeries'),fill_value=-999.)
    obs1.long_name              = 'sea water speed'
    obs1.standard_name          = 'sea_water_speed'
    obs1.ncei_name              = 'sea_water_speed'
    obs1.units                  = 'cm s-1'
    obs1.scale_factor           = 1.
    obs1.add_offset             = 0.
    #obs1._FillValue             = fill_value=-999.
    obs1.missing_value          = -999.
    obs1.valid_min              = 0.
    obs1.valid_max              = 30.
    obs1.coordinates            = 'time lat lon z'
    obs1.coverage_content_type  = 'physicalMeasurement'
    obs1.grid_mapping           = 'crs'
    obs1.source                 = 'GCOOS LDN upload/SOS.'
    obs1.references             = url
    obs1.cell_methods           = 'time: point lat: point lon: point z: point'
    obs1.ancillary_variables    = 'instrument platform'
    obs1.platform               = 'platform'
    obs1.instrument             = 'instrument'
    obs1.comment                = ''
    
    obs2                        = nc.createVariable('direction_of_sea_water_velocity','d',('timeSeries'),fill_value=-999.)
    obs2.long_name              = 'direction of sea water velocity'
    obs2.standard_name          = 'direction_of_sea_water_velocity'
    obs2.ncei_name              = 'direction_of_sea_water_velocity'
    obs2.units                  = 'degrees_true'
    obs2.scale_factor           = 1.
    obs2.add_offset             = 0.
    #obs2._FillValue             = fill_value=-999.
    obs2.missing_value          = -999.
    obs2.valid_min              = 0.
    obs2.valid_max              = 360.
    obs2.coordinates            = 'time lat lon z'
    obs2.coverage_content_type  = 'physicalMeasurement'
    obs2.grid_mapping           = 'crs'
    obs2.source                 = 'GCOOS LDN upload/SOS.'
    obs2.references             = url
    obs2.cell_methods           = 'time: point lat: point lon: point z: point'
    obs2.ancillary_variables    = 'instrument platform'
    obs2.platform               = 'platform'
    obs2.instrument             = 'instrument'
    obs2.comment                = ''
    
    obs3                        = nc.createVariable('upward_sea_water_velocity','d',('timeSeries'),fill_value=-999.)
    obs3.long_name              = 'upward sea water velocity'
    obs3.standard_name          = 'upward_sea_water_velocity'
    obs3.ncei_name              = 'upward_sea_water_velocity'
    obs3.units                  = 'cm s-1'
    obs3.scale_factor           = 1.
    obs3.add_offset             = 0.
    #obs3._FillValue             = fill_value=-999.
    obs3.missing_value          = -999.
    obs3.valid_min              = 0.
    obs3.valid_max              = 30.
    obs3.coordinates            = 'time lat lon z'
    obs3.coverage_content_type  = 'physicalMeasurement'
    obs3.grid_mapping           = 'crs'
    obs3.source                 = 'GCOOS LDN upload/SOS.'
    obs3.references             = url
    obs3.cell_methods           = 'time: point lat: point lon: point z: point'
    obs3.ancillary_variables    = 'instrument platform'
    obs3.platform               = 'platform'
    obs3.instrument             = 'instrument'
    obs3.comment                = ''
    
    obs4                        = nc.createVariable('eastward_sea_water_velocity','d',('timeSeries'),fill_value=-999.)
    obs4.long_name              = 'eastward_sea_water_velocity'
    obs4.standard_name          = 'eastward_sea_water_velocity'
    obs4.ncei_name              = 'eastward_sea_water_velocity'
    obs4.units                  = 'cm s-1'
    obs4.scale_factor           = 1.
    obs4.add_offset             = 0.
    #obs4._FillValue             = fill_value=-999.
    obs4.missing_value          = -999.
    obs4.valid_min              = 0.
    obs4.valid_max              = 30.
    obs4.coordinates            = 'time lat lon z'
    obs4.coverage_content_type  = 'physicalMeasurement'
    obs4.grid_mapping           = 'crs'
    obs4.source                 = 'GCOOS LDN upload/SOS.'
    obs4.references             = url
    obs4.cell_methods           = 'time: point lat: point lon: point z: point'
    obs4.ancillary_variables    = 'instrument platform'
    obs4.platform               = 'platform'
    obs4.instrument             = 'instrument'
    obs4.comment                = ''
    
    obs5                        = nc.createVariable('northward_sea_water_velocity','d',('timeSeries'),fill_value=-999.)
    obs5.long_name              = 'northward sea water velocity'
    obs5.standard_name          = 'northward_sea_water_velocity'
    obs5.ncei_name              = 'northward_sea_water_velocity'
    obs5.units                  = 'cm s-1'
    obs5.scale_factor           = 1.
    obs5.add_offset             = 0.
    #obs5._FillValue             = fill_value=-999.
    obs5.missing_value          = -999.
    obs5.valid_min              = 0.
    obs5.valid_max              = 30.
    obs5.coordinates            = 'time lat lon z'
    obs5.coverage_content_type  = 'physicalMeasurement'
    obs5.grid_mapping           = 'crs'
    obs5.source                 = 'GCOOS LDN upload/SOS.'
    obs5.references             = url
    obs5.cell_methods           = 'time: point lat: point lon: point z: point'
    obs5.ancillary_variables    = 'instrument platform'
    obs5.platform               = 'platform'
    obs5.instrument             = 'instrument'
    obs5.comment                = ''
    
    obs6                        = nc.createVariable('mass_concentration_of_chlorophyll_in_sea_water','d',('timeSeries'),fill_value=-999.)
    obs6.long_name              = 'mass concentration of chlorophyll in sea water'
    obs6.standard_name          = 'mass_concentration_of_chlorophyll_in_sea_water'
    obs6.ncei_name              = 'mass_concentration_of_chlorophyll_in_sea_water'
    obs6.units                  = 'ug L-1'
    obs6.scale_factor           = 1.
    obs6.add_offset             = 0.
    #obs6._FillValue             = fill_value=-999.
    obs6.missing_value          = -999.
    obs6.valid_min              = 0.
    obs6.valid_max              = 500.
    obs6.coordinates            = 'time lat lon z'
    obs6.coverage_content_type  = 'physicalMeasurement'
    obs6.grid_mapping           = 'crs'
    obs6.source                 = 'GCOOS LDN upload/SOS.'
    obs6.references             = url
    obs6.cell_methods           = 'time: point lat: point lon: point z: point'
    obs6.ancillary_variables    = 'instrument platform'
    obs6.platform               = 'platform'
    obs6.instrument             = 'instrument'
    obs6.comment                = ''
    
    obs7                        = nc.createVariable('mole_concentration_of_dissolved_oxygen_in_sea_water','d',('timeSeries'),fill_value=-999.)
    obs7.long_name              = 'mole concentration of dissolved oxygen in sea water'
    obs7.standard_name          = 'mole_concentration_of_dissolved_oxygen_in_sea_water'
    obs7.ncei_name              = 'mole_concentration_of_dissolved_oxygen_in_sea_water'
    obs7.units                  = 'ug L-1'
    obs7.scale_factor           = 1.
    obs7.add_offset             = 0.
    #obs7._FillValue             = fill_value=-999.
    obs7.missing_value          = -999.
    obs7.valid_min              = 0.
    obs7.valid_max              = 20.
    obs7.coordinates            = 'time lat lon z'
    obs7.coverage_content_type  = 'physicalMeasurement'
    obs7.grid_mapping           = 'crs'
    obs7.source                 = 'GCOOS LDN upload/SOS.'
    obs7.references             = url
    obs7.cell_methods           = 'time: point lat: point lon: point z: point'
    obs7.ancillary_variables    = 'instrument platform'
    obs7.platform               = 'platform'
    obs7.instrument             = 'instrument'
    obs7.comment                = ''
    
    obs8                        = nc.createVariable('sea_surface_height_above_sea_level','d',('timeSeries'),fill_value=-999.)
    obs8.long_name              = 'sea surface height above sea level'
    obs8.standard_name          = 'sea_surface_height_above_sea_level'
    obs8.ncei_name              = 'sea_surface_height_above_sea_level'
    obs8.units                  = 'm'
    obs8.scale_factor           = 1.
    obs8.add_offset             = 0.
    #obs8._FillValue             = fill_value=-999.
    obs8.missing_value          = -999.
    obs8.valid_min              = -10.
    obs8.valid_max              = 10.
    obs8.coordinates            = 'time lat lon z'
    obs8.coverage_content_type  = 'physicalMeasurement'
    obs8.grid_mapping           = 'crs'
    obs8.source                 = 'GCOOS LDN upload/SOS.'
    obs8.references             = url
    obs8.cell_methods           = 'time: point lat: point lon: point z: point'
    obs8.ancillary_variables    = 'instrument platform'
    obs8.platform               = 'platform'
    obs8.instrument             = 'instrument'
    obs8.comment                = ''
    
    obs9                        = nc.createVariable('sea_water_practical_salinity','d',('timeSeries'),fill_value=-999.)
    obs9.long_name              = 'sea water practical salinity'
    obs9.standard_name          = 'sea_water_practical_salinity'
    obs9.ncei_name              = 'sea_water_practical_salinity'
    obs9.units                  = 'psu'
    obs9.scale_factor           = 1.
    obs9.add_offset             = 0.
    #obs9._FillValue             = fill_value=-999.
    obs9.missing_value          = -999.
    obs9.valid_min              = 0.
    obs9.valid_max              = 38.
    obs9.coordinates            = 'time lat lon z'
    obs9.coverage_content_type  = 'physicalMeasurement'
    obs9.grid_mapping           = 'crs'
    obs9.source                 = 'GCOOS LDN upload/SOS.'
    obs9.references             = url
    obs9.cell_methods           = 'time: point lat: point lon: point z: point'
    obs9.ancillary_variables    = 'instrument platform'
    obs9.platform               = 'platform'
    obs9.instrument             = 'instrument'
    obs9.comment                = ''
    
    obs10                        = nc.createVariable('sea_water_temperature','d',('timeSeries'),fill_value=-999.)
    obs10.long_name              = 'sea water temperature'
    obs10.standard_name          = 'sea_water_temperature'
    obs10.ncei_name              = 'sea_water_temperature'
    obs10.units                  = 'Celsius'
    obs10.scale_factor           = 1.
    obs10.add_offset             = 0.
    #obs10._FillValue             = fill_value=-999.
    obs10.missing_value          = -999.
    obs10.valid_min              = -10.
    obs10.valid_max              = 35.
    obs10.coordinates            = 'time lat lon z'
    obs10.coverage_content_type  = 'physicalMeasurement'
    obs10.grid_mapping           = 'crs'
    obs10.source                 = 'GCOOS LDN upload/SOS.'
    obs10.references             = url
    obs10.cell_methods           = 'time: point lat: point lon: point z: point'
    obs10.ancillary_variables    = 'instrument platform'
    obs10.platform               = 'platform'
    obs10.instrument             = 'instrument'
    obs10.comment                = ''
    
    obs11                        = nc.createVariable('sea_water_turbidity','d',('timeSeries'),fill_value=-999.)
    obs11.long_name              = 'sea water turbidity'
    obs11.standard_name          = 'sea_water_turbidity'
    obs11.ncei_name              = 'sea_water_turbidity'
    obs11.units                  = 'NTU'
    obs11.scale_factor           = 1.
    obs11.add_offset             = 0.
    #obs11._FillValue             = fill_value=-999.
    obs11.missing_value          = -999.
    obs11.valid_min              = 400.
    obs11.valid_max              = 680.
    obs11.coordinates            = 'time lat lon z'
    obs11.coverage_content_type  = 'physicalMeasurement'
    obs11.grid_mapping           = 'crs'
    obs11.source                 = 'GCOOS LDN upload/SOS.'
    obs11.references             = url
    obs11.cell_methods           = 'time: point lat: point lon: point z: point'
    obs11.ancillary_variables    = 'instrument platform'
    obs11.platform               = 'platform'
    obs11.instrument             = 'instrument'
    obs11.comment                = ''
    
    # Read/Write the data matrix from a CSV file
    
    data = np.genfromtxt(infiles,dtype=[('date','S10'),('time','S8'),\
    ('sea_water_speed','f8'),('direction_of_sea_water_velocity','f8'),\
    ('upward_sea_water_velocity','f8'),('eastward_sea_water_velocity','f8'),\
    ('northward_sea_water_velocity','f8'),('mass_concentration_of_chlorophyll_in_sea_water','f8'),\
    ('mole_concentration_of_dissolved_oxygen_in_sea_water','f8'),\
    ('sea_surface_height_above_sea_level','f8'),('sea_water_practical_salinity','f8'),\
    ('sea_water_temperature','f8'),('sea_water_turbidity','f8'),\
    ('depth','f8')],delimiter=",",skip_header=1)
    
    lon[:]               = longitude
    lat[:]               = latitude
    
    for i in range(0,timeseries_length):
        year   = int(data[i][0].split('-')[0])
        month  = int(data[i][0].split('-')[1])
        day    = int(data[i][0].split('-')[2])
        hour   = int(data[i][1].split(':')[0])
        minute = int(data[i][1].split(':')[1])
        second = int(data[i][1].split(':')[2])
    
        dateobj = datetime.datetime(year,month,day,hour,minute,second)
    
        time = cdftime.date2num(dateobj)
    
        times[i] = round(time*3600)
        z[i] = data[i][13]
    
        obs1[i] = data[i][2]
        obs2[i] = data[i][3]
        obs3[i] = data[i][4]
        obs4[i] = data[i][5]
        obs5[i] = data[i][6]
        obs6[i] = data[i][7]
        obs7[i] = data[i][8]
        obs8[i] = data[i][9]
        obs9[i] = data[i][10]
        obs10[i] = data[i][11]
        obs11[i] = data[i][12]
    
    nc.close()
except:
    print "Error on file: " + outfile + ". \n"
    os.remove(outfile)
