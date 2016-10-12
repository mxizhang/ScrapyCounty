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
from oauth2client.service_account import ServiceAccountCredentials
import morris_write
import essex_write
import hunterdon_write
import hunterdon_save
import bergen_write

MRS_ADDS = 'https://docs.google.com/spreadsheets/d/1XOkErm0Oah2zSx2rcJoV0OAGQx8DL-C--iOfZIhXXRs/edit#gid=2117274665'
ESS_ADDS = 'https://docs.google.com/spreadsheets/d/1XOkErm0Oah2zSx2rcJoV0OAGQx8DL-C--iOfZIhXXRs/edit#gid=1826898806'
BGN_ADDS = 'https://docs.google.com/spreadsheets/d/1XOkErm0Oah2zSx2rcJoV0OAGQx8DL-C--iOfZIhXXRs/edit#gid=1623951483'
HTD_ADDS = 'https://docs.google.com/spreadsheets/d/1E4QyRyH2aS_XqeDkWkeZPDZn74gj9l1m1LU5GcZoMfE/edit#gid=558163237'
KEY = 'My Project-f09bdc10eb52.json'

def main():
    print "-----------------------------------------"
    print "         Welcome to Scrapy County!"
    print "Choose county:"
    print "              -- Morris (M)"
    print "              -- Essex (E)"
    print "              -- Bergen (B)"
    print "              -- Hunterdon (H)"
    print "-----------------------------------------"
    num = raw_input("your choice?")
    if num == 'M':
        morris(MRS_ADDS, KEY)
    elif num == 'E':
        essex(ESS_ADDS, KEY)
    elif num == 'B':
        bergen(BGN_ADDS, KEY)
    elif num == 'H':
        print "Please enter current Sheet ID: "
        id = raw_input("Sheet ID is: ")
        print "Please enter current Sheet Name: "
        name = raw_input("Sheet Name is: ")
        print "Download .pdf ? (Y/N) "
        b = raw_input(": ")
        if b == 'Y':
            hunterdon_save.hunterdon_save()
        elif b == 'N':
            pass
        
        hunterdon_write.hunterdon_write(HTD_ADDS, KEY, id, name)
    else:
        print "NOT FOUND! "

def morris(address, key):
    print "Morris County is called."
    try:
        os.remove("morris_items.csv")
    except OSError:
        pass
    subprocess.call("scrapy crawl morris -o morris_items.csv", shell=True)
    morris_write.morris_write(address, key)
def bergen(address, key):
    print "Bergen County is called."
    try:
        os.remove("bergen_items.csv")
    except OSError:
        pass
    subprocess.call("scrapy crawl bergen -o bergen_items.csv", shell=True)
    bergen_write.bergen_write(address, key)
def essex(address, key):
    print "Essex County is called."
    try:
        os.remove("essex_items.csv")
    except OSError:
        pass
    subprocess.call("scrapy crawl essex -o essex_items.csv", shell=True)
    essex_write.essex_write(address, key)


if __name__ == "__main__":
    main()