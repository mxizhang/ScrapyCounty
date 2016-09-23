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
import njlis
from oauth2client.service_account import ServiceAccountCredentials
import morris_write
import middlesex_write
import essex_write
import hunterdon_write
import hunterdon_save
import bergen_write
'''
MRS_ADDS = 'https://docs.google.com/spreadsheets/d/1v5sNJuIiLGwU6fH9Kpfr9XRxQCxrf7bx_PR_1fNA_6Q/edit#gid=0'
ESS_ADDS = 'https://docs.google.com/spreadsheets/d/1isOSOsyvGFTuCZwuqEEkmou0uxWm9AVCrNx_V0_JDmc/edit#gid=0'
BGN_ADDS = 'https://docs.google.com/spreadsheets/d/1aZBeaENA0xjxqpmKYNDrjIM4c_zy-MhHuLaunmPLv98/edit#gid=0'
HTD_ADDS = 'https://docs.google.com/spreadsheets/d/1kjiHt_daqvIueDw6qD7wk75mTFo0_ubRUFCnHNn4J8E/edit#gid=0'
'''
MRS_ADDS = 'https://docs.google.com/spreadsheets/d/11yUTZJURYQ_BHs_6VE9vz87q_teXmzApLXs11ZjK66w/edit#gid=0'
ESS_ADDS = 'https://docs.google.com/spreadsheets/d/1em7oEKzfA3qbNcHdn8d892y0rJvxjF5UnUY7XK6Yyik/edit#gid=0'
BGN_ADDS = 'https://docs.google.com/spreadsheets/d/1YKFWXYVnh_70KFcur7d7SsK8ZxDU5l9l4AOr-40-lY4/edit#gid=0'
HTD_ADDS = 'https://docs.google.com/spreadsheets/d/1lDEWpOAHh6XwqpjRxSFUIpfVMqqv_F5--Lj6b3rUQXU/edit#gid=0'
MIS_ADDS = 'https://docs.google.com/spreadsheets/d/1i2ZxwelVsH2H4cRGwLKoSFooNN5qHDZWKTJKsmz51A0/edit#gid=0'
KEY = 'ScrapyCountyWindows.json'

def main():
    print "-----------------------------------------"
    print "         Welcome to Scrapy County!"
    print "Choose county:"
    print "              -- Morris (M)"
    print "              -- Essex (E)"
    print "              -- Bergen (B)"
    print "              -- Hunterdon (H)"
    print "              -- MiddleSex (S)"
    print "-----------------------------------------"
    num = raw_input("your choice?")
    if num.upper() == 'M':
        morris(MRS_ADDS, KEY)
    elif num.upper() == 'E':
        essex(ESS_ADDS, KEY)
    elif num.upper() == 'B':
        bergen(BGN_ADDS, KEY)
    elif num.upper() == 'H':
        print "Please enter current Sheet ID: "
        id = raw_input("Sheet ID is: ")
        print "Please enter current Sheet Name: (Make sure it's not today's date because it will generate a new tab with today's date.)"
        name = raw_input("Sheet Name is: ")
        print "Download .pdf ? (Y/N) "
        b = raw_input(": ")
        if b.upper() == 'Y':
            hunterdon_save.hunterdon_save()
        hunterdon_write.hunterdon_write(HTD_ADDS, KEY, id, name)
    elif num.upper() == 'S':
        middlesex(MIS_ADDS, KEY)
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
    njlis.morris_lis('morris_lisp')
def bergen(address, key):
    print "Bergen County is called."
    try:
        os.remove("bergen_items.csv")
    except OSError:
        pass
    subprocess.call("scrapy crawl bergen -o bergen_items.csv", shell=True)
    bergen_write.bergen_write(address, key)
    njlis.bergen_lis('bergen_lisp')
def essex(address, key):
    print "Essex County is called."
    try:
        os.remove("essex_items.csv")
    except OSError:
        pass
    subprocess.call("scrapy crawl essex -o essex_items.csv", shell=True)
    essex_write.essex_write(address, key)
    njlis.essex_lis('essex_lisp')

def middlesex(address, key):
    print "middlesex County is called."
    try:
        os.remove("middlesex_items.csv")
    except OSError:
        pass
    subprocess.call("scrapy crawl middlesex -o middlesex_items.csv", shell=True)
    middlesex_write.middlesex_write(address, key)
    njlis.middlesex_lis('middlesex_lisp')

if __name__ == "__main__":
    main()