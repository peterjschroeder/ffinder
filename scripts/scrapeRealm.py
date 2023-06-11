from bs4 import BeautifulSoup
import urllib
import csv
import glob
import os
import os.path
import re
import subprocess
import sys

csv = open('realm.csv', 'w')

csv.write ("ID\tName\tType\tSeries\tSubseries\tManufacturer\tManufacturerNum\tYear Released\tUPC\tHeight\tAccessories\tAge Range\tGenres\tImage\n")

for filename in glob.iglob('actionfigure?action=actionfigure&id=*'):
    try:
        data = urllib.urlopen(filename)
        soup = BeautifulSoup(data, "lxml")
        text = soup.findAll("meta")

        id = filename.replace("actionfigure?action=actionfigure&id=", "")
        
        try:
            variation = " ("+soup.find("td", text="Variation:").nextSibling.text.replace(" / ", "/")+")"
        except:
            variation = ""
        try:
            name = soup.find("td", text="Name:").nextSibling.text+variation
        except:
            print "ERROR: "+filename+"\n"
        
        type = "Unknown"
        
        try:
            year = soup.find("td", text="Year Released:").nextSibling.text
        except:
            year = "Unknown"
        try:
            manufacturer = soup.find("td", text="Manufacturer:").nextSibling.text
        except:
            manufacturer = "Unknown"
        try:
            manufacturernum = soup.find("td", text="Manufacturer #:").nextSibling.text
        except:
            manufacturernum = "Unknown"
        try:
            series = soup.find("td", text="Series:").nextSibling.text
        except:
            series = "Unknown"
        try:
            subseries = soup.find("td", text="Subseries:").nextSibling.text
        except:
            subseries = "Unknown"
        try:
            size = soup.find("td", text="Height:").nextSibling.text
        except:
            size = "Unknown"

        accessories = "Unknown"
        
        try:
            ages = soup.find("td", text="Age Range:").nextSibling.text
        except:
            ages = "Unknown"
        try:
            upc = soup.find("td", text="UPC:").nextSibling.text
        except:
            upc = "Unknown"
        try:
            genres = soup.find("td", text="Genres:").nextSibling.text
        except:
            genres = "Unknown"
        try:
            image = soup.find("meta",  property="og:image").get("content", None).replace("thumb_", "")
        except:
            image = ""

        csv.write (id+"\t"+name+"\t"+type+"\t"+series+"\t"+subseries+"\t"+manufacturer+"\t"+manufacturernum+"\t"+year+"\t"+upc+"\t"+size+"\t"+accessories+"\t"+ages+"\t"+genres+"\t"+image+"\n")
    except:
        continue

csv.close()
