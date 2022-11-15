# FreqRunner
Automated SDR scanner script for scanning of police and other radio frequencies based on current location

This README will be updated continuously as this project is still under heavy development. For issue tracking and current development progress, check out the ISSUE_TRACKING.txt file. Note - This is NOT the place to post issues! An actual issue tracker will be created once this project is officially released.


The basis of this project is to create a robust police/emergency scanner that will work in place of a Uniden (or the like). This is an experimental project and aims to provide the same functionality in a Raspberry Pi but at a fraction of the cost. 



------------------------------------------------------------
# CONSIDERATIONS:

1: OP25 is the primary Radio Scanner software being used. For additional information, see https://github.com/boatbod/op25

2: A GPS module is used for location tracking which then will update the config OP25 uses for scanning. As you/your car moves, FreqRunner will update the location, and then use its DB of trunking systems and local police channels to scan through the ones in your area. 

3: The internal frequency and TRS lists that FreqRunner use are all pulled from RadioReference and are kept up to date weekly. As these lists and files are massive, they are not kept here on this GitHub page. They will be posted on another site once this is released for download and instructions.

4: The web console is used from OP25 to show the user what is going on. In the intended use case, the Raspberry Pi (3b+) is running in a car (tucked away somewhere) and the interface is pulled up by the user on a smartphone or tablet for vieweing. There will be a setup video posted once this project is released as well for use case ideas.

5: As of this writing, we are migrating away from using the legacy rx.py in OP25 and will be automating all of the config files to use multi_rx.py. This is due to the fact that all updates and feature additions are being done to multi_rx.py in OP25 by BoatBod. (See their GitHub page for more details)

6: All GPS data and channel switching are based off of Counties! There is support for a number of non-US lcations as well, but they will be coming out at in later releases.

7: This intended to be a fully offline system! In the world of emergency prepardness, we want our tools to work when we need them most. If we had this rely on the internet and in an emergency it was not available, well... shit. So, all the files for scan freqs and location data are stored locally to the rPi so no internet connection is needed! Routine updates should be done however to get the newest version of OP25 and update the scanner listings. Instructions on how to do this will be published once this project is fully released.

8: This is intended to be a plug and play, leave it and forget it solution! The idea is to connect the rPi in your car (hand held one coming in the future), and each time you start your car, the pi will power up, auto log in, and auto-start the scanner. That way it is running all the time. All you have to do is switch to  the audio source for output, and bring up the dashboard if desired to see who is talking and what is going on. An always-available scanner that you can count on is the way to go and this is an attempt at making that happen. Instructions on setting up FreqRunner, including the rPi setup and requirements, will be posted once this project is officially released.



------------------------------------------------------------
# HELPFUL LINKS:

Adhoc WiFi Hotspot: https://www.tomshardware.com/how-to/raspberry-pi-access-point



------------------------------------------------------------
This entire project is meant to be an open-source scanner for those with a little programming knowledge, and those who want information but don't want to pay the hefty price tag for a police scanner. Obviously this program cannot (yet) do everything that those can.
