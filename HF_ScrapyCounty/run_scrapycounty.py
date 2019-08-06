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
import normal_mode
import manual_mode
'''
COUNTY = [essex, union, middlesex]
'''
START = 0

def main():
    print "-----------------------------------------"
    print "         Welcome to Scrapy County!"
    print "Choose county:"
    print "              -- Essex (1)"
    print "              -- MiddleSex (2)"
    print "              -- Union (3)"
    print "-----------------------------------------"
    num = raw_input("your choice? ")
    mode = raw_input("Do you wanna run it on Normal(N) mode or Manual(M) mode? ")
    tab_name = raw_input('Old Tab Name?')
    if mode.upper() == 'M':
        new_tab = raw_input('New Tab Name?')
        start_row = raw_input('Restarting from which row?')

        manual_mode.manual_mode(int(num)-1, tab_name, new_tab, int(start_row))
    else:
        normal_mode.normal_mode(int(num)-1, tab_name)

if __name__ == "__main__":
    main()  