#!/bin/python3

'''
This is a test script (to really only be used in prod once before being ripped apart to create another)
We will use selenium to web scrape radioreference.com for download CSV files for everything in the US
General Idea:
##1 - Scrape initial scanner/freq data off of RadioReference
-Selenium log into RR
-Then while logged in, cycles through each county to download all of the frequencies
	URL like: https://www.radioreference.com/apps/db/?action=csv&ctid=270 (where # at the end changes)
-Then while still logged in, goes and downloads all of the trunked system data
	Freq URL like: https://www.radioreference.com/apps/db/?action=csv&sid=6616&opt=sites
	Talkgroup URL like: https://www.radioreference.com/apps/db/?action=csv&sid=6616&opt=tg
-Script will keep increasing numbers for downloads until it sees a message on the screen that shows "Invalid"
	Example: https://www.radioreference.com/apps/db/?sid=50000&tab=reports
-If we ever get a page that says "Please Login", we will then re-login and try the page again to download
********
I am going to have to go through and re-name these files so I know wtf I am looking at.......
To do this we can browse to a page that coresponds with the file name, (ie file ctid_270.csv and then browse to https://www.radioreference.com/apps/db/?ctid=270). We can then scrape the page title out of the HTML
    and rename the file accordingly
This will need done with ALL files that were grabbed!
'''

### IMPORT LIBRARIES ###
import os
import time
from os.path import dirname
from selenium import webdriver
import glob
import csv
import selenium
import getpass

### DEFINE VARIABLES ###
#Get username and password to log into RadioReference. DO NOT store them locally
username = input("Username: ")
password = getpass.getpass()

#Define selenium options and set up driver
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": "H:\\Radio_Scanner Info\\SDR and Scanners\\Scanner Downloads\\New_Pull"}
options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(executable_path=f'{dirname(__file__)}/chromedriver.exe', chrome_options=options)

### FUNCTIONS ###
def ctid_rename_file():
    files = glob.glob("H:\\Radio_Scanner Info\\SDR and Scanners\\Scanner Downloads\\CTID\\*.csv")

    for file in files:
        to_renmae = file.split(".")[0].split("_")[1]

        rename_site = f'https://www.radioreference.com/apps/db/?ctid={to_renmae}'
        driver.get(rename_site)
        time.sleep(1)

        #Get the name of the county and state from the webpage
        new_name = driver.find_element_by_class_name("px12").text()
        print(new_name)
        input()
        #rename the associated file appropriately
        os.rename(file, new_name)

def sid_rename_file():
    files = glob.glob("H:\\Radio_Scanner Info\\SDR and Scanners\\Scanner Downloads\\SID\\*.csv")

    for file in files:
        to_renmae = file.split(".")[0].split("_")[1]

        rename_site = f'https://www.radioreference.com/apps/db/?sid={to_renmae}'
        driver.get(rename_site)
        time.sleep(1)

        #Get the name of the county and state from the webpage
        new_name = ""

        #rename the associated file appropriately
        os.rename(file, new_name)

#Decoder to replace gross unicode characters with "" in a single value
def my_encoder(input):
    #encode() method
    strencode = input.encode("ascii", "ignore")
    
    #decode() method
    strdecode = strencode.decode()
    return strdecode

### THE THING ###
if __name__ == '__main__':
    try:
        driver.get("https://www.radioreference.com/login/")
        time.sleep(1)

        uname = driver.find_element_by_name("username")
        psswd = driver.find_element_by_name("password")

        uname.send_keys(username)
        psswd.send_keys(password)

        driver.find_element_by_xpath('//button[normalize-space()="Login"]').click()
        time.sleep(2)

        print("Logged in... Starting to download things...")

        '''
        #Get the County information
        i = 1
        while i <= 50000:
            print("Working on County # ", i, end='\r')
            site = f'https://www.radioreference.com/apps/db/?action=csv&ctid={i}'
            driver.get(site)
            time.sleep(2)
            i += 1
        '''

        #Get the Trunk System information
        with open("H:\\Radio_Scanner Info\\SDR and Scanners\\Scanner Downloads\\New_Pull\\tracking.csv", "w", newline='') as tracker:
            writer = csv.writer(tracker)
            headers = ["Location", "System", "ID#"]
            writer.writerow(headers)

            #Iterate through the downloads and put identifiers to the system in the tracking sheet
            i = 1
            while i <= 50000:
                print("Working on System # ", i, end='\r')
                site = f'https://www.radioreference.com/apps/db/?action=csv&sid={i}&opt=sites'
                tg = f'https://www.radioreference.com/apps/db/?action=csv&sid={i}&opt=tg'
                info = f'https://www.radioreference.com/apps/db/?sid={i}'


                driver.get(site)
                driver.get(tg)
                driver.get(info)

                try:
                    element1 = driver.find_element_by_class_name("px12")
                    element2 = driver.find_element_by_class_name("rrtable")

                    outline = [my_encoder(element1.text), my_encoder(element2.text), i]
                    writer.writerow(outline)

                except selenium.common.exceptions.NoSuchElementException:
                    file1 = f'H:\\Radio_Scanner Info\\SDR and Scanners\\Scanner Downloads\\New_Pull\\trs_site_{i}.csv'
                    file2 = f'H:\\Radio_Scanner Info\\SDR and Scanners\\Scanner Downloads\\New_Pull\\trs_tg_{i}.csv'
                    os.remove(file1)
                    os.remove(file2)

                i += 1


    except KeyboardInterrupt:
        quit()
