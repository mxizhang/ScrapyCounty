# -*- coding: utf-8 -*-
# -*- author: mxiz -*-
'''
Python 2.7
Before Start:
1. gspread [Google Spreadsheets Python API https://github.com/burnash/gspread]
	Install: $ pip install gspread
2. Obtain OAuth2 credentials from Google Developers Console
	[http://gspread.readthedocs.io/en/latest/oauth2.html]
'''
import gspread
import csv
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('My Project-f09bdc10eb52.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1XOkErm0Oah2zSx2rcJoV0OAGQx8DL-C--iOfZIhXXRs/edit#gid=0")
#worksheet = sh.add_worksheet(title="Test", rows="100", cols="20")
worksheet = sh.get_worksheet(4)

csvfile = open("morris_items.csv","rb")
reader = csv.reader(csvfile)

start = 2
for line in reader:
	#print line

	worksheet.update_cell(start, 1, line[8] + " -> " + line[4]) #date
	worksheet.update_cell(start, 2, line[1]) #shf no
	worksheet.update_cell(start, 3, line[3]) #case
	worksheet.update_cell(start, 6, line[6]) #add
	worksheet.update_cell(start, 9, line[2]) #upset

	worksheet.update_cell(start, 4, "PLF: " + line[0] + "\n" + "DEF: " + line[7])
	worksheet.update_cell(start, 5, line[5]) #att
	start=start+1
'''
csvfile = open("essex_items.csv","rb")
reader = csv.reader(csvfile)

start = 2
for line in reader:
	#print line

	worksheet.update_cell(start, 1, line[9] + " -> " + line[0]) #date
	worksheet.update_cell(start, 2, line[1]) #shf no
	worksheet.update_cell(start, 3, line[4]) #case
	worksheet.update_cell(start, 6, line[7]) #add
	worksheet.update_cell(start, 9, line[2]) #upset

	worksheet.update_cell(start, 4, "PLF: " + line[5] + "\n" + "DEF: " + line[8])
	worksheet.update_cell(start, 5, line[6] + "\n" + "Phone: " + line[3] ) #att
	start=start+1
'''