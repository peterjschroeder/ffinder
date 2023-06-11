from bs4 import BeautifulSoup
import urllib
import csv
import glob
import os
import os.path
import re
import subprocess
import sys

with open("output.csv", 'w') as g:
    with open('genres.csv', 'r') as f:
        for line in f:
            try:
                data = urllib.urlopen(line)
                soup = BeautifulSoup(data, "lxml")

                try:
                    origin = soup.find("th", text="Origin").parent.find('td').text+", "
                except:
                    origin = ""
                    
                try:
                    genres = soup.find("th", text="Genre").parent.find('td').text+"\n"
                except:
                    genres = "\n"
            except:
                genres = "\n"
                        
            g.write(origin+genres)
