'''
import datetime
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

m = next_weekday(datetime.datetime.today(), 0) # 0 = Monday, 1=Tuesday, 2=Wednesday...
mon = "%s/%s/%s" % (m.month, m.day, m.year)
date = datetime.date(2016,11,7)
#DATE = "%s/%s/%s" % (date.month, date.day, date.year)
DATE = "11/7/2016"
print mon
print DATE
print mon == DATE

import time
import gspread
import csv
import httplib2
import random
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

SS_ADDRESS = "https://docs.google.com/spreadsheets/d/1em7oEKzfA3qbNcHdn8d892y0rJvxjF5UnUY7XK6Yyik/edit#gid=0"
KEY = 'ScrapyCountyWindows-86f453b644e3.json'
scope_gl = 'https://www.googleapis.com/auth/spreadsheets'
credentials_gl = ServiceAccountCredentials.from_json_keyfile_name(KEY, scope_gl)
http = credentials_gl.authorize(httplib2.Http())
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

spreadsheetID = SS_ADDRESS.split('/')[5]
print spreadsheetID

requests = []
s = '=HYPERLINK("https://www.youtube.com/","youtube")'
requests.append({
    'updateCells': {
	    "rows": { 
	    	"values": [{
	    		"userEnteredValue": {
	    			"formulaValue": "s",
	    		},
	    	}],
	    },
	    "fields": "*",
	    "start": {
	    	"sheetId": 0,
  			"rowIndex": 3,
  			"columnIndex": 3,
  		},
    }
})
batchUpdateRequest = {'requests': requests}
service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetID, body=batchUpdateRequest).execute()

result = service.spreadsheets().get(spreadsheetId=spreadsheetID).execute()
for item in result['sheets']:
	if item['properties']['title'] == "Sheet5":
		print item['properties']['sheetId']

from item_write import items_write

items_write(6, 'Sheet5')
'''
import urllib
content = urllib.urlopen('http://www.middlesexcountynj.gov/Government/Departments/PSH/Pages/Foreclosures.aspx').read()
print content