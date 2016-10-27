import urllib2
import requests
import subprocess

FILENAME_PDF = "selection.pdf"
FILENAME_CSV = "selection.xml"
BAKE = "bakerrec.py"

def mercer_save():
    download_file("http://nj.gov/counties/mercer/pdfs/sheriff_foreclosuresales_list.pdf")
    convert_to_xlsx()
    #bake()

def download_file(download_url):
    response = urllib2.urlopen(download_url)
    file = open(FILENAME_PDF, 'wb')
    file.write(response.read())
    file.close()

def convert_to_xlsx():
	files = {'f': (FILENAME_PDF, open(FILENAME_PDF, 'rb'))}
	response = requests.post("https://pdftables.com/api?key=lhfxwj5qn8jg&format=xml", files=files)
	response.raise_for_status() # ensure we notice bad responses
	with open(FILENAME_CSV, "wb") as f:
	    f.write(response.content)
	f.close()

def bake():
    subprocess.call("bake " + BAKE + " " + FILENAME_CSV, shell=True)

def main():
    convert_to_xlsx()