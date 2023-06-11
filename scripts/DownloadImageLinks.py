#!/usr/bin/python3
# encoding: utf-8

from bs4 import BeautifulSoup
import csv
import os
import re
import sys

f = open('afigures.csv')
csv_f = csv.reader(f)

with open("test.txt", "a") as myfile:
    for row in csv_f:
        data = urllib.urlopen(row[0])
        soup = BeautifulSoup(data, "lxml")
        image = soup.find('img', {'src' : re.compile(r'(jpg)$')})
        print (image["src"].replace("galleries", "https://www.figurerealm.com/galleries").replace("thumb_", ""))
        myfile.write(image["src"].replace("galleries", "https://www.figurerealm.com/galleries").replace("thumb_", "")+"\n")
