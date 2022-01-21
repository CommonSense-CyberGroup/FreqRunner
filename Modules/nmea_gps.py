#!/usr/bin/python3

'''
This module is for the testing and proof of concept for reading raw NMEA data from a GLONASS GPS USB and then processing it to a readable format.
This also will then process the current coordinates and determine the county/zip code (in the US) that the user/device is in.

This script sets environment variables on the system to the current location so other scripts can access them without having to start this script and wait constantly
    FREQ_LOC = full location string
    FREQ_COUNTRY = Country
    FREQ_STATE = State
    FREQ_CITY = City
    FREQ_COUNTY = County
    FREQ_LAT = Latitude
    FREQ_LON = Longitude
    FREQ_UPDATE = Last updated time of coordinates


Updated: 1/21/2022
'''

### IMPORT LIBRARIES ###
import serial
import reverse_geocoder
import logging
import os

### DEFINE VARIABLES ###
#Set up logging
logging_file = 'gps_testing.log'         #Define log file location for windows
logger = logging.getLogger('GPS_Logging')  #Define log name
logger.setLevel(logging.DEBUG)              #Set logger level
fh = logging.FileHandler(logging_file)      #Set the file handler for the logger
fh.setLevel(logging.DEBUG)                  #Set the file handler log level
logger.addHandler(fh)                       #Add the file handler to logging
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')   #Format how the log messages will look
fh.setFormatter(formatter)                  #Add the format to the file handler

tracker = 0 #This keeps track of the seconds before we check on the current state and county

### FUNCTIONS ###
#Function to parse through the received NMEA GPS data from the USB dongle
def parseGPS(data):
    #Set up global variables
    global tracker, state_tracking, county_tracking

    data = str(data).replace("b'", "")
    if "$GPRMC" in data[0:6]:
        sdata = data.split(",")

        #Let the user know if we do not have a signal yet, and setthe env variable
        if sdata[2] == 'V':
            os.environ['FREQ_LOC'] = "no signal"
            #print("FREQ_LOC = ", os.environ.get('FREQ_LOC'))
            return

        #Convert the data in the NMEA string to something we can read (We are leaving a lot of things out, but we won't use them for what we are doing)
        time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
        date = sdata[9][2:4] + "/" + sdata[9][0:2] + "/" + sdata[9][4:6]

        os.environ['FREQ_LOC'] = f'{date} {time}'

        #Search for the county, city, and state with the given coordinates
        country, city, state, county = position_lookup(sdata[3], sdata[4], sdata[5], sdata[6])

        #Set env variables to current location strings so other programs can get them
        os.environ['FREQ_LOC'] = f'{country} {state} {county} {city}'
        os.environ['FREQ_COUNTRY'] = country
        os.environ['FREQ_CITY'] = city
        os.environ['FREQ_STATE'] = state
        os.environ['FREQ_COUNTY'] = county

        #Set the current_location variables to the current county so we know when it changes
        if tracker == 0:
            state_tracking = state
            county_tracking = county
            logger.info("Starting location is %s %s %s", country, state, county)

        if tracker == 86500:
            tracker = 1
            state_tracking == state
            county_tracking = county

        if state != state_tracking or county != county_tracking:
            logger.info("State or county Changed from %s %s to %s %s", state_tracking, county_tracking, state, county)
            state_tracking = state
            county_tracking = county


        #Print the values of env variables so we know that they are set/changing
        #print("FREQ_LOC = ", os.environ.get('FREQ_LOC'))
        #print("FREQ_COUNTRY = ", os.environ.get('FREQ_COUNTRY'))
        #print("FREQ_CITY = ", os.environ.get('FREQ_CITY'))
        #print("FREQ_STATE = ", os.environ.get('FREQ_STATE'))
        #print("FREQ_COUNTY = ", os.environ.get('FREQ_COUNTY'))
        #print("FREQ_LAT = ", os.environ.get('FREQ_LAT'))
        #print("FREQ_LON = ", os.environ.get('FREQ_LON'))
        #print("FREQ_UPDATE = ", os.environ.get('FREQ_UPDATE'), "\n")

        tracker += 1

#Function to get the county, city, and state using the GPS coordinates
def position_lookup(lat, dir_lat, lon, dir_lon):
    #Get the information with the coordinates
    lat_coord = (int(lat[0:2]) + float(lat[2:])/60)
    lon_coord = (int(lon[0:3]) + float(lon[3:])/60)

    #Account for +/- in the lat/lon values when mapping
    if dir_lat == "S":
        lat_coord = -lat_coord
    if dir_lon == "W":
        lon_coord = -lon_coord

    coord = (lat_coord, lon_coord)

    #Set env variables to lat and lon
    os.environ['FREQ_LAT'] = str(lat_coord)
    os.environ['FREQ_LON'] = str(lon_coord)

    current_location = reverse_geocoder.search(coord)

    #Pull out the useful information from the returned information and send it back for display/use
    return current_location[0]["cc"], current_location[0]["name"], current_location[0]["admin1"], current_location[0]["admin2"]


### THE THING ###
if __name__ == '__main__':

    #Set up the serial port to read data from
    ser = serial.Serial("/dev/ttyACM0", baudrate = 9600, timeout = 0.5)

    while True:
        try:
            #Read the serial data and then call the parse function to convert the raw NMEA data into a readable format
            data = ser.readline()
            parseGPS(data)

        except KeyboardInterrupt:
            quit()
