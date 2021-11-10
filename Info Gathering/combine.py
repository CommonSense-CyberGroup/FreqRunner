#!/bin/python3

'''
This script is used for combining all of the downloaded files into a single master file (ctid, sid, and tg) as well as creating key columns so all of the data can be correlated
'''

### IMPORT LIBRARIES ###
import csv
from os.path import dirname
import glob

### FUNCTIONS ###
#Function to parse through and combine the CTID (county freq) files
def ctid_combine():
    #Parse the county files first
        county_files = glob.glob("H:\\Radio_Scanner Info\\SDR and Scanners\\Scanner Downloads\\CTID\\*.csv")

        #Open the master file to write to
        with open ("H:\Radio_Scanner Info\SDR and Scanners\Scanner Downloads\\ctid_master.csv", "a+", newline='', encoding='utf-8') as citd_master:
            citd_writer = csv.writer(citd_master)

            #Get the info from the saved file name
            for file in county_files:
                name = file.split("\\")[5]

                try:
                    country = name.split("-")[0]
                except:
                    pass
                try:
                    state_terr = name.split("-")[1]
                except:
                    pass
                try:
                    county = name.split("-")[2].replace(".csv", "")
                except:
                    pass

                #Read the contents of the file and set it to write
                with open (file, "r", encoding='utf-8') as county_read_file:
                    county_reader = csv.DictReader(county_read_file)
                    #Since there are gross unicode characters, we have to sanitize them first before we can try and output them
                    try:
                        for row in county_reader:
                            outline = [my_encoder(row["Frequency Output"]), my_encoder(row["Frequency Input"]), my_encoder(row["FCC Callsign"]), my_encoder(row["Agency/Category"]), my_encoder(row["Description"]), my_encoder(row["Alpha Tag"]), my_encoder(row["PL Tone"]), my_encoder(row["Mode"]), my_encoder(row["Class Station Code"]), my_encoder(row["Tag"]), my_encoder(country), my_encoder(state_terr), my_encoder(county)]

                            #Print the outline to the master file
                            citd_writer.writerow(outline)
                    
                    #If the row has a shit character, send the whole row to be decoded and replace the character
                    except UnicodeDecodeError:
                        new_row = my_row_encoder(row)
                        outline = [new_row[0], new_row[1], new_row[2], new_row[3], new_row[4], new_row[5], new_row[6], new_row[7], new_row[8], new_row[9], my_encoder(country), my_encoder(state_terr), my_encoder(county)]

                        #Print the outline to the master file
                        citd_writer.writerow(outline)

                    county_read_file.close()
                    county = ""
                    state_terr = ""
                    country = ""

            citd_master.close()

#Function to kick off either the sid or tg combine functions
def sid_kicker():
    #Parse the county files first
    files = glob.glob("H:\\Radio_Scanner Info\\SDR and Scanners\\Scanner Downloads\\SID\\*.csv")

    #Open the master tg file to write to
    with open ("H:\\Radio_Scanner Info\\SDR and Scanners\\Scanner Downloads\\tg_master.csv", "a+", newline='', encoding='utf-8') as tg_master:
        csv_tg = csv.writer(tg_master)

        #Open the master sid file to write to
        with open ("H:\\Radio_Scanner Info\\SDR and Scanners\\Scanner Downloads\\sid_master.csv", "a+", newline='', encoding='utf-8') as sid_master:
            csv_sid = csv.writer(sid_master)

            #Call the correct function based on the file type
            for file in files:
                if "_tg.csv" in file:
                    print("Trying file: ", file)
                    tg_combine(file, csv_tg)

                if "_site.csv" in file:
                    print("Trying file: ", file)
                    sid_combine(file, csv_sid)

#Function to parse through and combine the SID (trunk system) files
def sid_combine(input_file, csv_sid):
    #Get the info from the saved file name
        name = input_file.split("\\")[5]

        try:
            country = name.split("-")[0]
        except:
            pass
        try:
            state_terr = name.split("-")[1]
        except:
            pass
        try:
            county = name.split("-")[2].replace(".csv", "")
        except:
            pass

        #Read the contents of the file and set it to write
        with open (input_file, "r", encoding='utf-8') as sid_read_file:
            csid_reader = csv.DictReader(sid_read_file)
            #Since there are gross unicode characters, we have to sanitize them first before we can try and output them
            try:
                for row in csid_reader:
                    outline = [my_encoder(row["Site Dec"]), my_encoder(row["Site Hex"]), my_encoder(row["Description"]), my_encoder(row["County Name"]), my_encoder(row["Lat"]), my_encoder(row["Lon"]), my_encoder(row["Range"]), my_encoder(row["Frequencies"]), my_encoder(country), my_encoder(state_terr), my_encoder(county)]

                    #Print the outline to the master file
                    csv_sid.writerow(outline)
            
            #If the row has a shit character, send the whole row to be decoded and replace the character
            except UnicodeDecodeError:
                new_row = sid_row_encoder(row)
                outline = [new_row[0], new_row[1], new_row[2], new_row[3], new_row[4], new_row[5], new_row[6], new_row[7], my_encoder(country), my_encoder(state_terr), my_encoder(county)]

                #Print the outline to the master file
                csv_sid.writerow(outline)

            county = ""
            state_terr = ""
            country = ""

#Function to parse through and combine the TG (talk group) files
def tg_combine(input_file, csv_tg):
    #Get the info from the saved file name
    name = input_file.split("\\")[5]

    try:
        country = name.split("-")[0]
    except:
        pass
    try:
        state_terr = name.split("-")[1]
    except:
        pass
    try:
        county = name.split("-")[2].replace(".csv", "")
    except:
        pass

    #Read the contents of the file and set it to write
    with open (input_file, "r", encoding='utf-8') as tg_read_file:
        tg_reader = csv.DictReader(tg_read_file)
        #Since there are gross unicode characters, we have to sanitize them first before we can try and output them
        try:
            for row in tg_reader:
                outline = [my_encoder(row["Decimal"]), my_encoder(row["Hex"]), my_encoder(row["Tag"]), my_encoder(row["Mode"]), my_encoder(row["Description"]), my_encoder(row["Tag"]), my_encoder(row["Category"]), my_encoder(country), my_encoder(state_terr), my_encoder(county)]

                #Print the outline to the master file
                csv_tg.writerow(outline)
        
        #If the row has a shit character, send the whole row to be decoded and replace the character
        except UnicodeDecodeError:
            new_row = tg_row_encoder(row)
            outline = [new_row[0], new_row[1], new_row[2], new_row[3], new_row[4], new_row[5], new_row[6], my_encoder(country), my_encoder(state_terr), my_encoder(county)]

            #Print the outline to the master file
            csv_tg.writerow(outline)

        county = ""
        state_terr = ""
        country = ""

#Decoder to replace gross unicode characters with "" in a single value
def my_encoder(input):
    #encode() method
    strencode = input.encode("ascii", "ignore")
    
    #decode() method
    strdecode = strencode.decode()
    return strdecode

#Decoder to replace gross unicode characters with "" in a row
def my_row_encoder(row):
    #encode() method
    strencode1 = row["Frequency Output"].encode("ascii", "ignore")
    strencode2 = row["Frequency Input"].encode("ascii", "ignore")
    strencode3 = row["FCC Callsign"].encode("ascii", "ignore")
    strencode4 = row["Agency/Category"].encode("ascii", "ignore")
    strencode5 = row["Description"].encode("ascii", "ignore")
    strencode6 = row["Alpha Tag"].encode("ascii", "ignore")
    strencode7 = row["PL Tone"].encode("ascii", "ignore")
    strencode8 = row["Mode"].encode("ascii", "ignore")
    strencode9 = row["Class Station Code"].encode("ascii", "ignore")
    strencode10 = row["Tag"].encode("ascii", "ignore")
    
    #decode() method
    strdecode1 = strencode1.decode()
    strdecode2 = strencode2.decode()
    strdecode3 = strencode3.decode()
    strdecode4 = strencode4.decode()
    strdecode5 = strencode5.decode()
    strdecode6 = strencode6.decode()
    strdecode7 = strencode7.decode()
    strdecode8 = strencode8.decode()
    strdecode9 = strencode9.decode()
    strdecode10 = strencode10.decode()

    new_row = [strdecode1, strdecode2, strdecode3, strdecode4, strdecode5, strdecode6, strdecode7, strdecode8, strdecode9, strdecode10]

    return new_row

#Decoder to replace gross unicode characters with "" in a row for tg files
def tg_row_encoder(row):
    #encode() method
    strencode1 = row["Decimal"].encode("ascii", "ignore")
    strencode2 = row["Hex"].encode("ascii", "ignore")
    strencode3 = row["Alpha Tag"].encode("ascii", "ignore")
    strencode4 = row["Mode"].encode("ascii", "ignore")
    strencode5 = row["Description"].encode("ascii", "ignore")
    strencode6 = row["Tag"].encode("ascii", "ignore")
    strencode7 = row["Category"].encode("ascii", "ignore")

    #decode() method
    strdecode1 = strencode1.decode()
    strdecode2 = strencode2.decode()
    strdecode3 = strencode3.decode()
    strdecode4 = strencode4.decode()
    strdecode5 = strencode5.decode()
    strdecode6 = strencode6.decode()
    strdecode7 = strencode7.decode()

    new_row = [strdecode1, strdecode2, strdecode3, strdecode4, strdecode5, strdecode6, strdecode7]

    return new_row

#Decoder to replace gross unicode characters with "" in a row for tg files
def sid_row_encoder(row):
    #encode() method
    strencode1 = row["Site Dec"].encode("ascii", "ignore")
    strencode2 = row["Site Hex"].encode("ascii", "ignore")
    strencode3 = row["Description"].encode("ascii", "ignore")
    strencode4 = row["County Name"].encode("ascii", "ignore")
    strencode5 = row["Lat"].encode("ascii", "ignore")
    strencode6 = row["Lon"].encode("ascii", "ignore")
    strencode7 = row["Range"].encode("ascii", "ignore")
    strencode8 = row["Frequencies"].encode("ascii", "ignore")

    #decode() method
    strdecode1 = strencode1.decode()
    strdecode2 = strencode2.decode()
    strdecode3 = strencode3.decode()
    strdecode4 = strencode4.decode()
    strdecode5 = strencode5.decode()
    strdecode6 = strencode6.decode()
    strdecode7 = strencode7.decode()
    strdecode8 = strencode7.decode()

    new_row = [strdecode1, strdecode2, strdecode3, strdecode4, strdecode5, strdecode6, strdecode7, strdecode8]

    return new_row

### THE THING ###
if __name__ == '__main__':
    try:
        #Combine the CTID files
        #ctid_combine()

        #Combine the SID and TG files
        sid_kicker()

    except KeyboardInterrupt:
        quit()
