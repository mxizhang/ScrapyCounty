# ScrapyCounty
Implemented with Python 2.7 by Xi Zhang for Noah Luk at LNH Holding LLC

## Overview:
    Collecting sales data from <http://salesweb.civilview.com/>
    Counties supported:
    - Morris
    - Essex
    - Bergen
    - Middlesex coming soon.

## Installation:
pip <https://pip.pypa.io/en/stable/installing/>
### Part 1:
- Scrapy <http://scrapy.org/>
	Install:  $ pip install scrapy
- Selenium <https://pypi.python.org/pypi/selenium>
	Install: $ pip install selenium
- PhantomJS <http://phantomjs.org/>
	Install: $ sudo pkg install phantomjs

### Part 2:
- gspread [Google Spreadsheets Python API <https://github.com/burnash/gspread>]
	Install: $ pip install gspread
- Obtain OAuth2 credentials from Google Developers Console
	[http://gspread.readthedocs.io/en/latest/oauth2.html]
- pyzillow <https://pypi.python.org/pypi/pyzillow/0.5.5>
	Install: $ pip install pyzillow
- Obtain zillow's API 
  <http://www.zillow.com/howto/api/APIOverview.htm>

## Run:
### Part 1:
1. Open Shell
2. cd ScrapyCounty/
- scrapy crawl morris -o morris_items.csv
- scrapy crawl essex -o essex_items.csv
- scrapy crawl bergen -o bergen_items.csv

### Part 2:
1. Open google_sps.py
2. Command + B
