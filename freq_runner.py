'''
TITLE: FreqRunner
BY:
    Common Sense Cyber Group
    Some Guy they call Scooter

Version: 1.0.1

License: MIT

Created: 1/19/2022
Updated: 1/19/2022

Purpose:
    -This script is the backbone to the an automated Raspberry Pi Police Scanner. It utilizes an NMEA GPS unit to get the current location and format it nicely, then parses through downloaded RadioReference 
    frequencies to pull out emergency and trunked radio systems. The user has a UI (django) that allows them to remotely control the system (in a car for example, using a phone or tablet connecting to an ad-hoc network)

Considerations:
    -This script / class is intended to be called from the Django framework that displays the user UI (but can also be tested independently here)
    -The GPS script that is included in this software suite runs on its own, and must be running for this scanner to work properly. The GPS script sets/updates an environment variables that are referenced by this script
    -The data (csv files) has to be pulled down manually and minor changes made. This means that this scanner is only as up to date as the last info pull from RedioReference (and requires an account for the proper info to be pulled.)

To Do / Notes:
    -Do we want to look at putting the CSV contents into a DB in Django? Or should we just still keep it is csv files to parse?
    -EVENTUALLY, look at setting an "All" button in the GUI that will use either rx.py or multi_rx.py in OP25 to scan the channels instead of only the one the user picks (actual scanner functionality)
    -Do we need to split out parsing for trunked and non-trunked CTID or can we do it all at once? (sort by 'Mode' column)

'''

### IMPORT LIBRARIES ###
import time
import csv
import os

### CLASSES AND FUNCTIONS ###
class freq_runner:
    def __intit__(self):
        #Define the user channel list and now playing at startup
        self.user_channel_list = []
        self.now_playing = ""

        #Define file paths to CSV files for parsing through
        self.system_locations = ""
        self.ctid_locations = ""

        #Begin checking the location
        self.check_location()

    #Function to check location and do things based on where we are
    def check_location(self):
        #First we need to see what the current location is at the time of starting (once we have signal)
        while True:
            if os.environ['FREQ_LOC'] == "no signal":

                #Set location text for display on page
                self.current_location = "Acquiring GPS Signal"

                #Set channel list for display on page
                self.user_channel_list = []

                #Update the user page
                self.update_user_page()

                #Wait and try to get the GPS info again
                time.sleep(1)

            else:
                self.current_location = os.environ['FREQ_LOC']
                break

        #Now we have to check the location constantly (default is every 30sec) to see if our current location has changed
        while True:
            time.sleep(30)

            #If no GPS signal, let the user know and clear the user channel list for the screen
            if os.environ['FREQ_LOC'] == "no signal":

                #Set location text for display on page
                self.current_location = "Acquiring GPS Signal"

                #Set channel list for display on page
                self.user_channel_list = []

                #Update the user page
                self.update_user_page()

                pass

            #If location is the same, do nothing
            if os.environ['FREQ_LOC'] == self.current_location:

                #Set location text for display on page
                self.current_location = os.environ['FREQ_LOC']

            #If location has changed, update the user channel list to display on the screen by parsing the files with the new location
            if os.environ['FREQ_LOC'] != self.current_location:

                #Set location text for display on page
                self.current_location = os.environ['FREQ_LOC']

                #Set notification text for user to see
                self.user_notification = "GPS Location Has Changed!"


                #Parse through the csv files with the new location to make the list
                #CTID First
                self.parse_ctid()

                #Now SIDs
                self.parse_sid()

                #Update the list on the user interface
                self.update_user_page()

    #Function to update the user page in the GUI
    def update_user_page(self):
        #This will eventually change. For now, just print the updated variables
        print(self.user_notification)
        print(self.current_location)
        print(self.user_channel_list)
        print(os.environ['FREQ_UPDATE'])

    #Function to parse the CTID (non-system) info to show channels nearby
    def parse_ctid(self):
        #Open the frequency list file
        with open ("full_emergency_ctid.csv", 'r') as cf:
            ctid_master = csv.DictReader(cf)

            #Parse through the file and find the rows that we need to add to the user list
            for row in ctid_master:
                if row["Country"] == os.environ["FREQ_COUNTRY"] and row["State/Territory"] == os.environ["FREQ_STATE"] and row["County"] == os.environ["FREQ_COUNTY"]:

                    #Create the row item to show to the user
                    channel_row_title = f'{row["Agency/Category"]}, {row["Description"]} - {row["Tag"]}'
                    self.user_channel_list.append(channel_row_title)
                    
                    #Now that we have a row that matches the current location, start to work out the system type, and set up the info to build the config file
                    if row["Model"] == "AM":
                        print()
                    if row["Model"] == "AME":
                        print()
                    if row["Model"] == "DMR":
                        print()
                    if row["Model"] == "DMRE":
                        print()
                    if row["Model"] == "EDACS":
                        print()
                    if row["Model"] == "FM":
                        print()
                    if row["Model"] == "FME":
                        print()
                    if row["Model"] == "FMN":
                        print()
                    if row["Model"] == "FMNE":
                        print()
                    if row["Model"] == "iDEN":
                        print()
                    if row["Model"] == "LTR":
                        print()
                    if row["Model"] == "Mode":
                        print()
                    if row["Model"] == "Motorola":
                        print()
                    if row["Model"] == "MPT-1327":
                        print()
                    if row["Model"] == "NXDN":
                        print()
                    if row["Model"] == "NXDNE":
                        print()
                    if row["Model"] == "OpenSky":
                        print()
                    if row["Model"] == "Other":
                        print()
                    if row["Model"] == "P25":
                        print()
                    if row["Model"] == "P25E":
                        print()
                    if row["Model"] == "Project 25":
                        print()
                    if row["Model"] == "SmarTrunk":
                        print()
                    if row["Model"] == "Telm":
                        print()
                    if row["Model"] == "TETRA":
                        print()
                    if row["Model"] == "USB":
                        print()

    #Function to parse the SID (System) info to show channels nearby
    def parse_sid(self):
        #Defince list of IDs that we will need to parse through and get information
        sids_to_parse = []

        #First gather the files that we want to actually get channel info from
        with open (self.system_locations, 'r') as sf:
            sid_master = csv.DictReader(sf)

            for row in sid_master:
                if row["Country"] == os.environ['FREQ_COUNTRY']:
                    if row["State"] == os.environ['FREQ_STATE']:
                        if row["County"] == os.environ['FREQ_COUNTY']:
                            sids_to_parse.append(row["ID"])

            #Close the master file to stay clean
            sf.close()

        #Now parse through the files that pertain to our location. If the site has more than one tower/location, get the one that is closest to us
        for id in sids_to_parse:
            for root, directories, file in os.walk(self.system_locations):
                for item in file:
                    #First the site file
                    if f'site_{id}' in item:

                        #Check to see how many lines are in the file. If more than 1, we need to see which tower/station is closer and add that to the config file for OP25
                        print()

    #Function for doing maths on GPS location data in order to see which coordinates in a list are nearest our current location - https://stackoverflow.com/questions/59736682/find-nearest-location-coordinates-in-land-using-python
    def geo_maths(self):
        print()


### THE THING ###
if __name__ == '__main__':

    #Run FreqRunner - Only used for standalone testing. This whole class will be called from the Django page files in production
    freq_runner()