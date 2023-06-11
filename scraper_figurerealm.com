#!/usr/bin/python3
# encoding: utf-8

from bs4 import BeautifulSoup
import csv
import glob
import os
import os.path
import re
import subprocess
import sys

csv = open('realm.csv', 'w')
imgurls = open('imgurls.txt', 'w')

csv.write ("ID\tName\tType\tSeries\tSubseries\tManufacturer\tManufacturerNum\tYear Released\tUPC\tHeight\tColor\tAccessories\tStand\tAge Range\tGenres\n")

for filename in glob.iglob('actionfigure?action=actionfigure&id=*'):
    try:
        soup = BeautifulSoup(open(filename), "lxml")
        text = soup.findAll("meta")

        id = filename.replace("actionfigure?action=actionfigure&id=", "")
                    
        try:
            variation = " ("+soup.find("td", text="Variation:").nextSibling.text.replace(" / ", "/")+")"
        except:
            variation = ""
        try:
            name = soup.find("td", text="Name:").nextSibling.text+variation
        except:
            print ("ERROR")
        
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
            imgurls.write('wget "%s" -O %s.jpg\n' % (soup.find("meta",  property="og:image").get("content", None).replace("thumb_", ""), id))
            
            image = [x['src'] for x in soup.findAll('img', {'jq': 'userpic'})]
            
            for i in range(2, len(image)):
                imgurls.write('wget "http://www.figurerealm.com/%s" -O %s%s.jpg\n' % (image[i].replace("thumb_", ""), id, (".%s" % i if i > 0 else "")))
        except:
            pass

        csv.write (id+"\t"+name+"\t"+type+"\t"+series+"\t"+subseries+"\t"+manufacturer+"\t"+manufacturernum+"\t"+year+"\t"+upc+"\t"+size+"\t"+"Unknown"+"\t"+accessories+"\t"+"Unknown"+\t"+ages+"\t"+genres+"\n")
    except:
        continue

csv.close()
imgurls.close()
