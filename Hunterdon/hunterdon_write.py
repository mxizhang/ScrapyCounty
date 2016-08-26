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
import zillow_functions
import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

'''
User Messages:
1. Type in Google SpreadSheets address as SS_ADDRESS.
2. Save credential (.json file) as KEY_CRE.
'''
SS_ADDRESS = "https://docs.google.com/spreadsheets/d/1XOkErm0Oah2zSx2rcJoV0OAGQx8DL-C--iOfZIhXXRs/edit#gid=0"
KEY_CRE = 'My Project-f09bdc10eb52.json'

SHEETID = 740199223
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_CRE, scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_url(SS_ADDRESS)


SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
credentials_g = ServiceAccountCredentials.from_json_keyfile_name(KEY_CRE, SCOPES)
http = credentials_g.authorize(httplib2.Http())
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

spreadsheetId = '1XOkErm0Oah2zSx2rcJoV0OAGQx8DL-C--iOfZIhXXRs'

with open("data-sale-bakerrec-.csv","rb") as csvfile:
	filereader = csv.reader(csvfile)
	data = list(filereader)
	row_count = len(data)

requests = []
requests.append({
    'insertDimension': {
        "range": {"sheetId": SHEETID, "dimension": 1, "startIndex": 5, "endIndex": 1 + row_count/7},
        "inheritFromBefore": False,
    }
})
batchUpdateRequest = {'requests': requests}

worksheet = sh.get_worksheet(5)
val = worksheet.acell('B6').value
if val is not "":
	service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body=batchUpdateRequest).execute()

start = 6
for line in data[1:]:
	#print line
	if line[0] is not "":
		try:
			caseno = str(int(round(float(line[0]))))
			print caseno
			cell = worksheet.find(caseno)
			date = worksheet.cell(cell.row, 1).value
			asset = worksheet.cell(cell.row, 9).value
			address = worksheet.cell(cell.row, 6).value
			town = ""

			print str(cell.row) + "/" + str(cell.col) + ": " + str(cell.value)
			requests = []
			requests.append({
			    'cutPaste': {
				    "source": {
					    "sheetId": SHEETID,
						"startRowIndex": cell.row - 1,
						"endRowIndex": cell.row,
				    },
				    "destination": {
					  	"sheetId": SHEETID,
					  	"rowIndex": start - 1,
						"columnIndex": 0,
				  },
					"pasteType": "PASTE_NORMAL",
			    }
			})

			batchUpdateRequest = {'requests': requests}

			service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body=batchUpdateRequest).execute()
			if asset is not line[47]:
				worksheet.update_cell(start, 9, asset + "\nNew: " + line[47]) #upset
			worksheet.update_cell(start, 1, date + "->" + line[38]) #date
			worksheet.update_cell(start, 18, line[63])
			

		except gspread.CellNotFound as err:
			print ("CellNotFound!")
		
			worksheet.update_cell(start, 1, line[38]) #date
			#worksheet.update_cell(start, 2, line[1]) #shf no
			worksheet.update_cell(start, 2, line[0]) #case
			address = line[55]
			city = line[71]
			town = " ".join(city.split()[2:])
			worksheet.update_cell(start, 6, line[55] + "\n" + town + " NJ") #add
			#worksheet.update_cell(start, 7, town) #city
			worksheet.update_cell(start, 18, line[63]) #status
			worksheet.update_cell(start, 9, line[47]) #upset

		#worksheet.update_cell(start, 4, "PLF: " + line[0] + "\n" + "DEF: " + line[7])
		#worksheet.update_cell(start, 5, line[5]) #att
		except ValueError as err:
			continue

		zillow = zillow_functions.findzillow(address, town)
		print zillow
		#worksheet.update_cell(start, 7, "\n".join(zillow[3][:]) + "\n" + town)
		#worksheet.update_cell(start, 14, "\n".join(zillow[0][:])) #zillowID
		worksheet.update_cell(start, 14, "\n".join(zillow[1][:])) #zestimate
		add = worksheet.cell(start, 6).value
		#worksheet.update_cell(start, 6, "\n".join(zillow[2][:])+ ", " + add)
		start=start+1
