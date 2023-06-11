#!/usr/bin/python3
# encoding: utf-8

import webcolors
from colorthief import ColorThief
from PIL import Image

im = Image.open("test.jpg")
n, color = max(im.getcolors(im.size[0]*im.size[1]))
print (color)

color_thief = ColorThief('./test.jpg')
dominant_color = color_thief.get_color(quality=1)

def get_color_name(rgb_triplet):
    min_colours = {}
    for key, name in webcolors.css21_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - rgb_triplet[0]) ** 2
        gd = (g_c - rgb_triplet[1]) ** 2
        bd = (b_c - rgb_triplet[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

print (get_color_name(dominant_color))
