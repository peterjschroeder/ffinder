from bs4 import BeautifulSoup
import urllib
import csv
import glob
import os
import os.path
import re
import subprocess
import sys

csv = open('archive.csv', 'w')

csv.write ("Name\tType\tSeries\tSubseries\tManufacturer\tManufacturerNum\tYear Released\tUPC\tHeight\tAccessories\tAge Range\tGenres\tImage\n")

for filename in glob.iglob('item.aspx?itemID=*'):
    try:
        data = urllib.urlopen(filename)
        soup = BeautifulSoup(data, "lxml")
        text = soup.findAll("meta")

        name = soup.find("b").text
        try:
            year = soup.find("th", { "class" : "huge" }).text.strip()
        except:
            year = "Unknown"
        try:
            manufacturer = soup.find("th", text="Manufacturer").parent.find('td').text
        except:
            manufacturer = "Unknown"
        try:
            series = soup.find("th", text="Line").parent.find('td').text
        except:
            series = "Unknown"
        try:
            subseries = soup.find("th", text="Assortment").parent.find('td').text
        except:
            subseries = "Unknown"
        try:
            type = soup.find("th", text="Item type").parent.find('td').text
        except:
            type = "Unknown"
        try:
            size = soup.find("th", text="Figure Size").parent.find('td').text
        except:
            size = "Unknown"
        try:
            accessories = soup.find("th", text="Accessories").parent.find('td').text
        except:
            accessories = "Unknown"
        try:
            upc = soup.find('img', {'src' : re.compile(r'(.*upc.*)$')}).get('src').replace("upca.aspx?upc=", "")
        except:
            upc = "Unknown"
        try:
            genres = soup.find("th", text="Line").parent.find('a').get('href')
        except:
            genres = "Unknown"
        try:
            image = soup.find("meta",  property="og:image").get("content", None)
        except:
            image = ""

        csv.write (name+"\t"+type+"\t"+series+"\t"+subseries+"\t"+manufacturer+"\tUnknown\t"+year+"\t"+upc+"\t"+size+"\t"+accessories+"\tUnknown\t"+"http://figure-archive.net/"+genres+"\t"+image+"\n")
    except:
        continue

csv.close()
