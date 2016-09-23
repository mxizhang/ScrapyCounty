# -*- coding: utf-8 -*-
# -*- author: mxiz -*-
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import csv
import httplib2
import zillow_functions
from apiclient import discovery

def middlesex_write(SS_ADDRESS, key):

	scope_gs = ['https://spreadsheets.google.com/feeds']
	credentials_gs = ServiceAccountCredentials.from_json_keyfile_name(key, scope_gs)
	gc = gspread.authorize(credentials_gs)
	sh = gc.open_by_url(SS_ADDRESS)
	'''
	*** ***
	'''
	worksheet = sh.get_worksheet(0)

	scope_gl = 'https://www.googleapis.com/auth/spreadsheets'
	credentials_gl = ServiceAccountCredentials.from_json_keyfile_name(key, scope_gl)
	http = credentials_gl.authorize(httplib2.Http())
	discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
	service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

	spreadsheetID = SS_ADDRESS.split('/')[5]
	sheetID = SS_ADDRESS.split('/')[6].split('=')[-1:][0]
	print spreadsheetID + " & " + sheetID

	with open("middlesex_items.csv","rb") as csvfile:
		filereader = csv.reader(csvfile)
		data = list(filereader)
		row_count = len(data)

	print "------------------------------------------"
	print "Middlesex County has " + str(row_count) + " items!"
	print "------------------------------------------"

	requests = []
	requests.append({
	    'insertDimension': {
	        "range": {"sheetId": sheetID, "dimension": 1, "startIndex": 5, "endIndex": 5 + row_count},
	        "inheritFromBefore": False,
	    }
	})
	batchUpdateRequest = {'requests': requests}
	service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetID, body=batchUpdateRequest).execute()

	start = 6
	for line in data[1:]:
		#print line
		if line[0] is not "":
			try:
				caseno = line[3]
				print caseno
				cell = worksheet.find(caseno)
				#date = worksheet.cell(cell.row, 1).value
				worksheet.update_cell(cell.row, 1, line[5]) #date
				worksheet.update_cell(start, 9, line[2]) #upset
				address = worksheet.cell(cell.row, 6).value

				print str(cell.row) + "/" + str(cell.col) + ": " + str(cell.value)
				requests = []
				requests.append({
				    'cutPaste': {
					    "source": {
						    "sheetId": sheetID,
							"startRowIndex": cell.row - 1,
							"endRowIndex": cell.row,
					    },
					    "destination": {
						  	"sheetId": sheetID,
						  	"rowIndex": start - 1,
							"columnIndex": 0,
					  },
						"pasteType": "PASTE_NORMAL",
				    }
				})
				requests.append({
				    'deleteDimension': {
				        "range": {"sheetId": sheetID, "dimension": 1, "startIndex": cell.row - 1, "endIndex": cell.row},
				    }
				})

				batchUpdateRequest = {'requests': requests}
				service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetID, body=batchUpdateRequest).execute()
				
			except gspread.CellNotFound as err:
				print ("CellNotFound!")
			
				worksheet.update_cell(start, 1, line[5]) #date
				worksheet.update_cell(start, 2, line[1]) #shf no
				worksheet.update_cell(start, 3, line[3]) #case
				worksheet.update_cell(start, 4, "PLF: " + line[0] + "\n" + "DEF: " + line[8])
				worksheet.update_cell(start, 5, line[6]) #att
				worksheet.update_cell(start, 6, line[7]) #add
				worksheet.update_cell(start, 9, line[2]) #upset
				address = line[7]

			except ValueError as err:
				print "ValueError"
				continue

			zip = address.split(' ')[-1:]
			zillow = zillow_functions.find_zillow_by_zip(address, zip)
			print zillow
			worksheet.update_cell(start, 14, zillow[1])#zestimate
			start = start + 1
