#!/bin/python3

'''
This script is used to parse through the downloaded files, and then pull the header name out of the HTML web page in order to name them appropriately. That way we know what 
the location is for the given file.
'''

### IMPORT LIBRARIES ###
from os import rename
import os
import time
import getpass
from os.path import dirname
from selenium import webdriver
import selenium
import glob

### DEFINE VARIABLES ###
#Get username and password to log into RadioReference. DO NOT store them locally
username = "username"
password = "password"

#Define selenium options and set up driver
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": "H:\\Radio_Scanner Info\\SDR and Scanners\\Scanner Downloads\\SID"}
options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(executable_path=f'{dirname(__file__)}/chromedriver.exe', chrome_options=options)

### FUNCTIONS ###
def ctid_rename_file():
    files = glob.glob("H:\\Radio_Scanner Info\\SDR and Scanners\\Scanner Downloads\\CTID\\*.csv")

    for file in files:
        if "ctid_" in file:
            to_renmae = file.split(".")[0].split("_")[2]

            rename_site = f'https://www.radioreference.com/apps/db/?ctid={to_renmae}'
            driver.get(rename_site)
            time.sleep(1)

            #Get the name of the county and state from the webpage
            try:
                element = driver.find_element_by_class_name("px12")
            
                new_name = element.text
                new_name = new_name.replace(">", "-").replace("]", "").replace("[", "").replace("/", "")

                #rename the associated file appropriately
                os.rename(file, f'H:\\Radio_Scanner Info\\SDR and Scanners\\Scanner Downloads\\CTID\\{new_name}.csv')
            except FileExistsError:
                os.rename(file, f'H:\\Radio_Scanner Info\\SDR and Scanners\\Scanner Downloads\\CTID\\{new_name}_{to_renmae}.csv')
            except selenium.common.exceptions.NoSuchElementException:
                os.remove(file)

            except:
                pass

def sid_rename_file():
    files = glob.glob("H:\\Radio_Scanner Info\\SDR and Scanners\\Scanner Downloads\\SID\\*.csv")

    for file in files:
        if "trs_" in file:
            to_renmae = file.split(".")[0].split("_")[3]

            rename_site = f'https://www.radioreference.com/apps/db/?sid={to_renmae}'
            driver.get(rename_site)
            time.sleep(1)

            #Get the name of the county and state from the webpage
            try:
                element = driver.find_element_by_class_name("px12")
            
                new_name = element.text
                new_name = new_name.replace(">", "-").replace("]", "").replace("[", "").replace("/", "").replace(":", "").replace('"', "").replace("*", "").replace("?", "")
                #rename the associated file appropriately
                if "_tg_" in file:
                    try:
                        os.rename(file, f'H:\\Radio_Scanner Info\\SDR and Scanners\\Scanner Downloads\\SID\\{new_name}_tg.csv')
                    except FileExistsError:
                        try:
                            os.rename(file, f'H:\\Radio_Scanner Info\\SDR and Scanners\\Scanner Downloads\\SID\\{new_name}_{to_renmae}.csv')
                        except FileExistsError:
                            os.rename(file, f'H:\\Radio_Scanner Info\\SDR and Scanners\\Scanner Downloads\\SID\\{new_name}_{to_renmae}_{to_renmae}.csv')

                else:
                    try:
                        os.rename(file, f'H:\\Radio_Scanner Info\\SDR and Scanners\\Scanner Downloads\\SID\\{new_name}_site.csv')
                    except FileExistsError:
                        try:
                            os.rename(file, f'H:\\Radio_Scanner Info\\SDR and Scanners\\Scanner Downloads\\SID\\{new_name}_{to_renmae}.csv')
                        except FileExistsError:
                            os.rename(file, f'H:\\Radio_Scanner Info\\SDR and Scanners\\Scanner Downloads\\SID\\{new_name}_{to_renmae}_{to_renmae}.csv')
            except selenium.common.exceptions.NoSuchElementException:
                os.remove(file)

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

        #Start renaming
        #ctid_rename_file()
        while True:
            sid_rename_file()


    except KeyboardInterrupt:
        quit()
