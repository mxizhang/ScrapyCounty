# -*- coding: utf-8 -*-
# -*- author: mxiz -*-
'''
Python 2.7
To use ScrapyCounty crawler:
1. CHECK PIP: If not, download here -> [https://pip.pypa.io/en/stable/installing/] 
2. Scrapy [http://scrapy.org/]
    Install:  $ pip install scrapy
3. Selenium [https://pypi.python.org/pypi/selenium]
    Install: $ pip install selenium
4. PhantomJS
    Install: $ sudo pkg install phantomjs
    [Tip for Windows:
        Change path for PhantomJS first]

To upload to spreadsheet:
1. gspread [Google Spreadsheets Python API https://github.com/burnash/gspread]
    Install: $ pip install gspread
2. Obtain OAuth2 credentials from Google Developers Console
    [http://gspread.readthedocs.io/en/latest/oauth2.html]
3. httplib2
    Install: pip install httplib2
4. Google API client
    [https://developers.google.com/api-client-library/python/start/installation]
5. Before run it, make sure already shared googlesheet with @client
'''
import subprocess
import os
import njlispendens
from oauth2client.service_account import ServiceAccountCredentials
import hunterdon_save
import item_write
'''
COUNTY = [morris, essex, bergen, hunterdon, union, mercer, middlesex]
'''

def main():
    print "-----------------------------------------"
    print "         Welcome to Scrapy County!"
    print "Choose county:"
    print "              -- Morris (M)"
    print "              -- Mercer (C)"
    print "              -- Essex (E)"
    print "              -- Bergen (B)"
    print "              -- Hunterdon (H)"
    print "              -- MiddleSex (S)"
    print "              -- Union (U)"
    print "-----------------------------------------"
    num = raw_input("your choice?")
    name = raw_input('Old Tab Name?')
    if num.upper() == 'M':
        morris(0, name)
    elif num.upper() == 'C':
        mercer(5, name)
    elif num.upper() == 'E':
        essex(1, name)
    elif num.upper() == 'B':
        bergen(2, name)
    elif num.upper() == 'H':
        print "Download .pdf ? (Y/N) "
        b = raw_input(": ")
        if b.upper() == 'Y': 
            hunterdon_save.hunterdon_save()
        item_write.item_write(3, name)
        njlis.hunterdon_lis('hunterdon_lisp')
    elif num.upper() == 'S':
        middlesex(6, name)
    elif num.upper() == 'U':
        union(4, name)
    else:
        print "NOT FOUND! "

def mercer(number, name):
    print "Mercer County is called."
    print "!!! Step 1: Download sheriff_foreclosuresales_list.pdf from http://nj.gov/counties/mercer/pdfs/sheriff_foreclosuresales_list.pdf"
    print "!!! Step 2: Open http://www.pdftoexcel.com/"
    print "!!! Step 3: Upload sheriff_foreclosuresales_list.pdf and download .xlsx"
    print "!!! Step 4: Open sheriff_foreclosuresales_list.xlsx and Delete first two blank rows"
    print "!!! Step 5: Save as sheriff_foreclosuresales_list.xlsx in ScrapyCounty_windows folder"
    print "Please type Y to continue"
    num = raw_input("")
    if num.upper() == 'Y':
        subprocess.call("python mercer_convert.py", shell=True)
        item_write.item_write(number, name)
        njlispendens.njlis_pic(number)

def morris(number, name):
    print "Morris County is called."
    try:
        os.remove("morris_items.csv")
    except OSError:
        pass
    subprocess.call("scrapy crawl morris -o morris_items.csv", shell=True)
    item_write.item_write(number, name)
    njlispendens.njlis_pic(number)

def bergen(number, name):
    print "Bergen County is called."
    try:
        os.remove("bergen_items.csv")
    except OSError:
        pass
    subprocess.call("scrapy crawl bergen -o bergen_items.csv", shell=True)
    item_write.item_write(number, name)
    njlispendens.njlis_pic(number)

def essex(number, name):
    print "Essex County is called."
    
    try:
        os.remove("essex_items.csv")
    except OSError:
        pass
    subprocess.call("scrapy crawl essex -o essex_items.csv", shell=True)
    
    item_write.item_write(number, name)
    njlispendens.njlis_pic(number)

def middlesex(number, name):
    print "middlesex County is called."
    try:
        os.remove("middlesex_items.csv")
    except OSError:
        pass
    subprocess.call("scrapy crawl middlesex -o middlesex_items.csv", shell=True)
    item_write.item_write(number, name)
    njlispendens.njlis_pic(number)

def union(number, name):
    print "Union County is called."
    
    try:
        os.remove("union_items.csv")
    except OSError:
        pass
    subprocess.call("scrapy crawl union -o union_items.csv", shell=True)
    item_write.item_write(number, name)
    njlispendens.njlis_pic(number)


if __name__ == "__main__":
    main()