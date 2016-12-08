import urllib2
import requests
import subprocess

FILENAME_PDF = "sale.pdf"
FILENAME_CSV = "sale.xlsx"
BAKE = "bakerrec.py"

def hunterdon_save():
    download_file("http://www.co.hunterdon.nj.us/sheriff/SALES/sales.pdf")
    convert_to_xlsx()
    bake()

def download_file(download_url):
    response = urllib2.urlopen(download_url)
    file = open(FILENAME_PDF, 'wb')
    file.write(response.read())
    file.close()

def convert_to_xlsx():
	files = {'f': (FILENAME_PDF, open(FILENAME_PDF, 'rb'))}
	response = requests.post("https://pdftables.com/api?key=f46oilu9b3vs&format=xlsx-single", files=files)
	response.raise_for_status() # ensure we notice bad responses
	with open(FILENAME_CSV, "wb") as f:
	    f.write(response.content)
	f.close()

def bake():
    subprocess.call("bake " + BAKE + " " + FILENAME_CSV, shell=True)


hunterdon_save()