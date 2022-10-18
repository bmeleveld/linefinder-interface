# Coherence Grabber
# Author: Larry Donahue
# Edited: Bobby Eleveld
# This program aims to scrape coherence data generated by fscan in order to provide data for the Linefinder Interface located at https://github.com/donahuel/linefinder-interface to use.
# This program is intended for use on the LIGO clusters, and lives there.

import os
import subprocess

def scrape(dType, frame):
        #Define root directory to scrape data from by timeframe:
        rootdir = "/home/pulsar/public_html/fscan/H1/" + frame + "/H1Fscan_coherence/H1Fscan_coherence"
        
        #put scraped files in different directories depending on type of files scraped (plots/text files)
        if dType == ".png":
                fType == "plots"
        elif dType == ".txt":
                fType == "data"
        else: 
                print("Invalid Data Type")
        
        #List of files that will eventually be pushed to new directory:
        filecount = 0

        #For loop that runs through directory:
        for subdir, dirs, files in os.walk(rootdir): #Walk through (almost) every directory/subdirectory within the root directory
                print("Current directory: " + subdir)
                #This check allows us to bypass the first folder in the directory, comparisonFscans, and prevents us from getting caught up in the beginning of the directory when
                #making directories in our data folder:
                if subdir == rootdir + "/comparisonFscans" or subdir == rootdir:
                        pass
                else:
                        #Creates directory within data folder for certain weeks
                        if subdir.split("/")[9] != "comparisonFscans": #This check eliminates an empty comparisonFscans directory
                                subprocess.call(["mkdir", "-p", "/home/robertminghui.eleveld/" + fType + "/" + frame + "/" + subdir.split("/")[9]])
                        for file in files:
                                #If statement here filters out all files we know don't contain coherence data we want.
                                #A note: The gravitational wave channel (H1_GDS-CALIB_STRAIN) contains none of these files, so we can run this program through it with little cost.
                                if len(subdir.split("/")) >= 11: #Check to prevent bounds error on our split lists
                                        if subdir.split("/")[10] != "H1_GDS-CALIB_STRAIN":
                                                #Creates directory within weekly directory for certain channels
                                                subprocess.call(["mkdir", "-p", "/home/robertminghui.eleveld/" + fType + "/" + frame + "/" + subdir.split("/")[9] + "/" + subdir.split("/")[10]])
                                        if file.endswith(dType) and file.split("_")[4] == "coherence": #The plot and text files have identical names with the exception of their ending.
                                                #Copies file to appropriate directory
                                                subprocess.call(["rsync", os.path.join(subdir,file), "/home/robertminghui.eleveld/" + fType + "/" + frame + "/" + subdir.split("/")[9] + "/" + subdir.split("/")[10]])
                                                filecount = filecount + 1
        return filecount

print("Coherence Grabber opened. Starting data scrape.")
gate = True
dType = ""
frame = ""
while gate: #Get data folder (weekly/monthly) to run on
        userInput = input("Run on weekly (W) or monthly (M) directory? (W/M): ")
        if userInput.lower() == "w":
                gate = False
                frame = "weekly"
        elif userInput.lower() == "m":
                gate = False
                frame = "monthly"
        else:
                print("Invalid character.")
gate = True
while gate: #Get data type (plots/text files) to get
        userInput = input("Get plots (P) or .txt (T) files? (P/T): ")
        if userInput.lower() == "p":
                gate = False
                dType = ".png"
        elif userInput.lower() == "t":
                gate = False
                dType = ".txt"
        else:
                print("Invalid character.")
numfiles = scrape(dType, frame)
print("Scraped and copied " + str(numfiles) + " coherence files.")
