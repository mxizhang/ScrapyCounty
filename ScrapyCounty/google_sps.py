# -*- coding: utf-8 -*-
# -*- author: mxiz -*-
'''
Python 2.7
Before Start:
1. gspread [Google Spreadsheets Python API https://github.com/burnash/gspread]
	Install: $ pip install gspread
2. Obtain OAuth2 credentials from Google Developers Console
	[http://gspread.readthedocs.io/en/latest/oauth2.html]
3. pyzillow
	Install: $ pip install pyzillow
'''
import gspread
import csv
import pyzillow
from oauth2client.service_account import ServiceAccountCredentials
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults

# Data Entry for Morris County 
# input number as sheet number
def morrisentry(number):
	worksheet = sh.get_worksheet(number)
	csvfile = open("morris_items.csv","rb")
	reader = csv.reader(csvfile)
	start = 2
	for line in reader:
		#print line
		if line[0] is not "":
			# Get Address and corresponding Zipcode for Zestimate purpose
			address = line[6]
			address.replace("\n", " ")
			zipcode = address[-5:]

			try:
				deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
				result = GetDeepSearchResults(deep_search_response)
				zestimate = result.zestimate_amount
			except pyzillow.pyzillowerrors.ZillowError as err:
				#print ("No Zillow Found!")
				zestimate = 0
			# Update spreadsheets
			worksheet.update_cell(start, 1, line[8] + "->" + line[4]) #date
			worksheet.update_cell(start, 2, line[1]) #shf no
			worksheet.update_cell(start, 3, line[3]) #case
			worksheet.update_cell(start, 4, "PLF: " + line[0] + "\n" + "DEF: " + line[7])
			worksheet.update_cell(start, 5, line[5]) #att
			worksheet.update_cell(start, 6, line[6]) #add
			worksheet.update_cell(start, 9, line[2]) #upset
			worksheet.update_cell(start, 14, zestimate) #zillow
			start=start+1


def essexentry(number):
	worksheet = sh.get_worksheet(number)
	csvfile = open("essex_items.csv","rb")
	reader = csv.reader(csvfile)
	start = 2
	for line in reader:
		#print line
		if line[0] is not "":
			address = line[7]
			address.replace("\n", " ")
			zipcode = address[-5:]

			try:
				deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
				result = GetDeepSearchResults(deep_search_response)
				zestimate = result.zestimate_amount
			except pyzillow.pyzillowerrors.ZillowError as err:
				#print ("No Zillow Found!")
				zestimate = 0

			worksheet.update_cell(start, 1, line[9] + " -> " + line[0]) #date
			worksheet.update_cell(start, 2, line[1]) #shf no
			worksheet.update_cell(start, 3, line[4]) #case
			worksheet.update_cell(start, 6, address) #add
			worksheet.update_cell(start, 9, line[2]) #upset

			worksheet.update_cell(start, 4, "PLF: " + line[5] + "\n" + "DEF: " + line[8])
			worksheet.update_cell(start, 5, line[6] + "\n" + "Phone: " + line[3] ) #att
			worksheet.update_cell(start, 14, zestimate) #zillow
			start=start+1


def bergenentry(number):
	worksheet = sh.get_worksheet(number)
	csvfile = open("bergen_items.csv","rb")
	reader = csv.reader(csvfile)
	start = 2
	for line in reader:
		#print line
		if line[0] is not "":
			address = line[6]
			address.replace("\n", " ")
			zipcode = address[-5:]

			try:
				deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
				result = GetDeepSearchResults(deep_search_response)
				zestimate = result.zestimate_amount
			except pyzillow.pyzillowerrors.ZillowError as err:
				#print ("No Zillow Found!")
				zestimate = 0

			worksheet.update_cell(start, 1, line[8] + "->" + line[4]) #date
			worksheet.update_cell(start, 2, line[1]) #shf no
			worksheet.update_cell(start, 3, line[3]) #case
			worksheet.update_cell(start, 4, "PLF: " + line[0] + "\n" + "DEF: " + line[7])
			worksheet.update_cell(start, 5, line[5]) #att
			worksheet.update_cell(start, 6, address) #add
			worksheet.update_cell(start, 9, line[2]) #upset
			worksheet.update_cell(start, 14, zestimate) #zillow
			start=start+1

'''
Main function starts below
'''
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('My Project-f09bdc10eb52.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1XOkErm0Oah2zSx2rcJoV0OAGQx8DL-C--iOfZIhXXRs/edit#gid=0")
zillow_data = ZillowWrapper("X1-ZWz1fe5w83qcjv_70ucn")

#morrisentry(0)
#essexentry(1)
bergenentry(2)