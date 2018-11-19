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

def get_genres(g):
    with open(g, 'r') as f:
        try:
            soup = BeautifulSoup(open(g), "lxml")
            
            try:
                origin = soup.find("th", text="Origin").parent.find('td').text+", "
            except:
                origin = ""

            try:
                genres = soup.find("th", text="Genre").parent.find('td').text
            except:
                genres = ""
        except:
            genres = ""
    
        return(origin+genres).title()

csv = open('archive.csv', 'w')

csv.write ("ID\tName\tType\tSeries\tSubseries\tManufacturer\tManufacturerNum\tYear Released\tUPC\tHeight\tColor\tAccessories\tStand\tAge Range\tGenres\tImage\n")

for filename in glob.iglob('item.aspx?itemID=*'):
    try:
        soup = BeautifulSoup(open(filename), "lxml")
        text = soup.findAll("meta")

        id = filename.replace("item.aspx?itemID=", "")

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
            g = soup.find("th", text="Line").parent.find('a').get('href')
            genres = get_genres(g)
        except:
            genres = "Unknown"
        try:
            image = soup.find("meta",  property="og:image").get("content", None)
        except:
            image = ""

        csv.write (id+"\t"+name+"\t"+type+"\t"+series+"\t"+subseries+"\t"+manufacturer+"\tUnknown\t"+year+"\t"+upc+"\t"+size+"\tUnknown\t"+accessories+"\tUnknown\tUnknown\t"+genres+"\t"+image+"\n")
    except:
        continue

csv.close()
