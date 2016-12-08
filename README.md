# ScrapyCounty
Implemented with Python 2.7 by Xi Zhang for Noah Luk at LNH Holding LLC

## Overview:
    Collecting sales data from <http://salesweb.civilview.com/>
    Counties supported:
    - Morris
    - Essex
    - Bergen
    - Hunterdon  <http://www.co.hunterdon.nj.us/sheriff/SALES/sold.pdf>
    - Middlesex  <http://www.middlesexcountynj.gov/Government/Departments/PSH/Pages/Foreclosures.aspx>
    - Mercer
    - Union
    - Monmouth and Passaic comming soon

## Installation:
Check pip:
 - pip is already installed if you're using Python 2 >=2.7.9 or Python 3 >=3.4 downloaded from python.org, but you'll need to upgrade ir.<pip install -U pip>
 - Download pip <https://pip.pypa.io/en/stable/installing/>

### Part 1: (For scrapy crawler)
- Scrapy <http://scrapy.org/>
	>Install:  $ pip install scrapy
	
	Windows x32:
	$ pip install pypiwin32
	
	
	On Windows with Error:
	 	** make sure the development packages of libxml2 and libxslt are installed **

	1) download lxml & twisted wheel from here: http://www.lfd.uci.edu/~gohlke/pythonlibs/

	3) pip install C:\Users\Home\Downloads\lxml- ......... .whl
	

- Selenium <https://pypi.python.org/pypi/selenium>
	>Install: $ pip install selenium

- PhantomJS <http://phantomjs.org/>
	>Install: $ sudo pkg install phantomjs

    	Tip for Windows:
        	Change path for PhantomJS first
		Recommand path:
			C:/phantomjs-2.1.1-windows/bin/phantomjs.exe

### Part 2:
- gspread (Google Spreadsheets Python API <https://github.com/burnash/gspread>)
	>Install: $ pip install gspread

- Obtain OAuth2 credentials from Google Developers Console
	[http://gspread.readthedocs.io/en/latest/oauth2.html]

	>pip install PyOpenSSL

	>pip install --upgrade oauth2client
	
	>pip install --upgrade google-api-python-client

- Obtain zillow's official API :
  	<http://www.zillow.com/howto/api/APIOverview.htm>

	* Attention: 1000 max search properties.

- Obtain PDF to Excel API:
	<https://pdftables.com/pdf-to-excel-api>
	* Replace line 22 in hunterdon_save.py
	* Attention: 50 max free convert. Pay for more.

- httplib2
 	>Install: pip install httplib2

- Openpyxl
	>Install: pip install openpyxl

## Before run:
	* Make sure change spreadsheets address
	* Make sure share spreadsheets with client in credentials

## Run:
	python scrapycounty.py
