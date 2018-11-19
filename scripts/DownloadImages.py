#!/usr/bin/python3
# encoding: utf-8

from bs4 import BeautifulSoup
import os
import re
import sys

soup = BeautifulSoup(open(sys.argv[1]), "lxml")
image = soup.find('img', {'src' : re.compile(r'(jpg)$')})
if not os.path.exists(sys.argv[2].replace(":", " -").replace("/", "-")+"/"+sys.argv[3].replace(":", " -").replace("/", "-")):
    os.makedirs(sys.argv[2].replace(":", " -").replace("/", "-")+"/"+sys.argv[3].replace(":", " -").replace("/", "-"))
urllib.urlretrieve(image["src"].replace("galleries", "https://www.figurerealm.com/galleries").replace("thumb_", ""), filename=sys.argv[2].replace(":", " -").replace("/", "-")+"/"+sys.argv[3].replace(":", " -").replace("/", "-")+"/"+sys.argv[4].replace("$:", "").replace(":", " -").replace('"', "'").replace("/", "-").replace("?", "").replace("**", "2").replace("***", "3")+".jpg")
