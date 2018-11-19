#!/usr/bin/env python3

import signal
import pathlib
import shutil
import sqlite3

from picotui.screen import *
from picotui.widgets import *
from picotui.context import Context

from img_display import W3MImageDisplayer

def load_database():
    global figures, types, mfrs, years, heights, colors, stands, ffigures
    
    conn = sqlite3.connect('./ActionFigures.sqlite')
    c = conn.cursor()
    c.execute('SELECT * FROM ActionFigures')
    
    figures = list(c.fetchall())
    figures.sort(key=lambda x:x[1])

    types = list(set([figures[i][2] for i in range(0,len(figures))]))
    types.sort()
    types.insert(0, ('All',))

    mfrs = list(set([figures[i][5] for i in range(0,len(figures))]))
    mfrs.sort()
    mfrs.insert(0, ('All',))

    years = list(set([figures[i][7] for i in range(0,len(figures))]))
    years.sort()
    years.insert(0, ('All',))

    heights = list(set([figures[i][9] for i in range(0,len(figures))]))
    heights.sort()
    heights.insert(0, ('All',))

    colors = list(set([figures[i][10] for i in range(0,len(figures))]))
    colors.sort()
    colors.insert(0, ('All',))

    stands = list(set([figures[i][12] for i in range(0,len(figures))]))
    stands.sort()
    stands.insert(0, ('All',))
    
    ffigures = figures[:]

def screen_redraw(s, allow_cursor=False):
    s.attr_color(C_WHITE, C_BLUE)
    s.cls()
    s.attr_reset()
    d.redraw()

def screen_resize(s):
    d = create_dialogs()
    screen_redraw(s)

def main_loop():
    while 1:
        key = d.get_input()
        
        if key == KEY_ESC:
            #image_display.clear(cwidth/1.98, 2, 92, 34)
            sys.exit()
        if figure_list.focus == True:
            if key == KEY_LEFT:
                img_view = (img_view-1 if img_view >= 1 else len(img_views)-1)
                draw_image()
            elif key == KEY_RIGHT:
                img_view = (img_view+1 if img_view < len(img_views)-1 else 0)
                draw_image()
            else:
                res = d.handle_input(key)
                if res is not None and res is not True:
                    return res
        else:            
            res = d.handle_input(key)
            if res is not None and res is not True:
                return res

def ax(x):
    return int(x / 80 * Screen.screen_size()[0])
#    return x

def ay(y):
    return int(y / 24 * Screen.screen_size()[1])
#    return y

def create_dialogs():
    global cwidth, cheight, d, figure_list, draw_image
    cwidth, cheight = Screen.screen_size()
    img_views = ["front", "side-left", "side-right", "back", "bfront", "bback"]
    img_view = 0
    load_database()

    d = Dialog(0, 0, ax(80), ay(24), fcolor=C_WHITE, bcolor=C_BLUE)

    # Filters
    d.add(1, 1, WFrame(ax(40)-2, 5))
    
    d.add(2, 2, "Type:")
    filters_types = WDropDown(ax(23)-16, ["%s" % items for items in types], dropdown_h=int(cheight/4))
    d.add(16, 2, filters_types)
     
    d.add(2, 3, "Manufacturer:")
    filters_mfrs = WDropDown(ax(23)-16, ["%s" % items for items in mfrs], dropdown_h=int(cheight/4))
    d.add(16, 3, filters_mfrs)
        
    d.add(2, 4, "Year Released:")
    filters_years = WDropDown(ax(23)-16, ["%s" % items for items in years], dropdown_h=int(cheight/4))
    d.add(16, 4, filters_years)

    d.add(ax(24), 2, "Height:")
    filters_heights = WDropDown(ax(16)-9, ["%s" % items for items in heights], dropdown_h=int(cheight/4))
    d.add(ax(24)+7, 2, filters_heights)

    d.add(ax(24), 3, "Color:")
    filters_colors = WDropDown(ax(16)-9, ["%s" % items for items in colors], dropdown_h=int(cheight/4))
    d.add(ax(24)+7, 3, filters_colors)
    
    d.add(ax(24), 4, "Stand:")
    filters_stands = WDropDown(ax(16)-9, ["%s" % items for items in stands], dropdown_h=int(cheight/4))
    d.add(ax(24)+7, 4, filters_stands)

    def filters_changed(w):
        ffigures.clear()

        for i in range(0, len(figures)):
            if ((filters_types.items[filters_types.choice] == "All" or figures[i][2] == filters_types.items[filters_types.choice]) and
            (filters_mfrs.items[filters_mfrs.choice] == "All" or figures[i][5] == filters_mfrs.items[filters_mfrs.choice]) and 
            (filters_years.items[filters_years.choice] == "All" or figures[i][7] == filters_years.items[filters_years.choice]) and
            (filters_heights.items[filters_heights.choice] == "All" or figures[i][9] == filters_heights.items[filters_heights.choice]) and
            (filters_colors.items[filters_colors.choice] == "All" or figures[i][10] == filters_colors.items[filters_colors.choice]) and
            (filters_stands.items[filters_stands.choice] == "All" or figures[i][12] == filters_stands.items[filters_stands.choice])):
                ffigures.append(figures[i])

        # Temporary Fallback entry until filtering of filters is done  
        if not ffigures:
            ffigures.append(["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""])
                
        figure_list.top_line = 0
        figure_list.cur_line = 0
        figure_list.row = 0
        figure_list.items = ["%s" % items[1] for items in ffigures] 
        figure_list.set_lines(figure_list.items)
        figure_list.redraw()
        figure_list.signal("changed")

    filters_types.on("changed", filters_changed)
    filters_mfrs.on("changed", filters_changed)
    filters_years.on("changed", filters_changed)
    filters_heights.on("changed", filters_changed)
        
    # List box 
    d.add(1, 7, WFrame(ax(40)-2, ay(24)-8, "Action Figures"))
    figure_list = WListBox(ax(40)-4, ay(24)-10, ["%s" % items[1] for items in ffigures], scolor=C_MAGENTA)
    d.add(2, 8, figure_list)
 
    def flist_changed(w):
        fdetails_name.t = w.items[w.cur_line]
        fdetails_name.redraw()
        fdetails_type.t = ffigures[w.cur_line][2]
        fdetails_type.redraw()
        fdetails_series.t = ffigures[w.cur_line][3]
        fdetails_series.redraw()
        fdetails_subseries.t = ffigures[w.cur_line][4]
        fdetails_subseries.redraw()
        fdetails_mfr.t = ffigures[w.cur_line][5]
        fdetails_mfr.redraw()
        fdetails_mfrnum.t = ffigures[w.cur_line][6]
        fdetails_mfrnum.redraw()
        fdetails_year.t = ffigures[w.cur_line][7]
        fdetails_year.redraw()
        fdetails_upc.t = ffigures[w.cur_line][8]
        fdetails_upc.redraw()
        fdetails_height.t = ffigures[w.cur_line][9]
        fdetails_height.redraw()
        fdetails_color.t = ffigures[w.cur_line][10]
        fdetails_color.redraw()
        fdetails_acc.t = ffigures[w.cur_line][11]
        fdetails_acc.redraw()
        fdetails_stand.t = ffigures[w.cur_line][12]
        fdetails_stand.redraw()
        fdetails_age.t = ffigures[w.cur_line][13]
        fdetails_age.redraw()
        fdetails_genres.t = ffigures[w.cur_line][14]
        fdetails_genres.redraw()
        
        draw_image()
    figure_list.on("changed", flist_changed)

    # Image box
    d.add(ax(40), 1, WFillbox(ax(40), ay(24)-19))
        
    def draw_image():
        global image_display
        
        if "rxvt-unicode" in os.environ['TERM']:
            # Temporary for testing
            # image = "images/front/%s.jpg" % ffigures[figure_list.cur_line][0]
            image = "/home/peter/Downloads/+Backup/Figure Realm/%s/%s.jpg" % (img_views[img_view], ffigures[figure_list.cur_line][0])

            # Temporary until all watermarked images are replaced
            if not pathlib.Path(image).is_file():
                image = "/home/peter/Downloads/+Backup/Figure Realm/%s/%s (Watermarked).jpg" % (img_views[img_view], ffigures[figure_list.cur_line][0])
 
            try:
                image_display.quit()
            except:
                pass
        
            try:
                image_display = W3MImageDisplayer()
                image_display.initialize()
                image_display.clear(ax(41), 2, ax(38), ay(24)-21)
            
                if pathlib.Path(image).is_file():
                    image_display.draw(image, ax(41), 2, ax(38), ay(23)-21, scale_h=True)
            except:
                pass
        else:
            pass

    # Details
    d.add(ax(40), ay(24)-17, WFillbox(ax(40), 16))
   
    d.add(ax(41), ay(24)-16, "Name:")
    fdetails_name = WLabel("", w=ax(38)-6)
    d.add(ax(41)+6, ay(24)-16, fdetails_name)
    
    d.add(ax(41), ay(24)-15, "Type:")
    fdetails_type = WLabel("", w=ax(38)-6)
    d.add(ax(41)+6, ay(24)-15, fdetails_type)
    
    d.add(ax(41), ay(24)-14, "Series:")
    fdetails_series = WLabel("", w=ax(38)-8)
    d.add(ax(41)+8, ay(24)-14, fdetails_series)
    
    d.add(ax(41), ay(24)-13, "Subseries:")
    fdetails_subseries = WLabel("", w=ax(38)-11)
    d.add(ax(41)+11, ay(24)-13, fdetails_subseries)
    
    d.add(ax(41), ay(24)-12, "Manufacturer:")
    fdetails_mfr = WLabel("", w=ax(38)-14)
    d.add(ax(41)+14, ay(24)-12, fdetails_mfr)
    
    d.add(ax(41), ay(24)-11, "Manufacturer #:")
    fdetails_mfrnum = WLabel("", w=ax(38)-16)
    d.add(ax(41)+16, ay(24)-11, fdetails_mfrnum)
    
    d.add(ax(41), ay(24)-10, "Year Released:")
    fdetails_year = WLabel("", w=ax(38)-15)
    d.add(ax(41)+15, ay(24)-10, fdetails_year)
    
    d.add(ax(41), ay(24)-9, "UPC:")
    fdetails_upc = WLabel("", w=ax(38)-5)
    d.add(ax(41)+5, ay(24)-9, fdetails_upc)
    
    d.add(ax(41), ay(24)-8, "Height:")
    fdetails_height = WLabel("", w=ax(38)-8)
    d.add(ax(41)+8, ay(24)-8, fdetails_height)
    
    d.add(ax(41), ay(24)-7, "Color:")
    fdetails_color = WLabel("", w=ax(38)-7)
    d.add(ax(41)+7, ay(24)-7, fdetails_color)
    
    d.add(ax(41), ay(24)-6, "Accessories:")
    fdetails_acc = WLabel("", w=ax(38)-13)
    d.add(ax(41)+13, ay(24)-6, fdetails_acc)
    
    d.add(ax(41), ay(24)-5, "Stand:")
    fdetails_stand = WLabel("", w=ax(38)-7)
    d.add(ax(41)+7, ay(24)-5, fdetails_stand)
    
    d.add(ax(41), ay(24)-4, "Age Range:")
    fdetails_age = WLabel("", w=ax(38)-11)
    d.add(ax(41)+11, ay(24)-4, fdetails_age)
    
    d.add(ax(41), ay(24)-3, "Genres:")
    fdetails_genres = WLabel("", w=ax(38)-8)
    d.add(ax(41)+8, ay(24)-3, fdetails_genres)

    return d

with Context():
    d = create_dialogs()

    screen_redraw(Screen)
    Screen.set_screen_redraw(screen_redraw)
    Screen.set_screen_resize(screen_resize)

    figure_list.signal("changed")

    res = main_loop()

