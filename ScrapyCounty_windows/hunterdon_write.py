# -*- coding: utf-8 -*-
# -*- author: mxiz -*-
'''
Python 2.7
Before Start:
1. gspread [Google Spreadsheets Python API https://github.com/burnash/gspread]
	Install: $ pip install gspread
2. Obtain OAuth2 credentials from Google Developers Console
	[http://gspread.readthedocs.io/en/latest/oauth2.html]
3. httplib2
	Install: pip install httplib2
4. Google API client
	[https://developers.google.com/api-client-library/python/start/installation]
5. Share with @client
'''
import time
import gspread
import csv
import zillow_functions
import httplib2
import random
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

def hunterdon_write(SS_ADDRESS, key, old_id, sheetname):
	# Get credentials
	scope_gs = ['https://spreadsheets.google.com/feeds']
	credentials_gs = ServiceAccountCredentials.from_json_keyfile_name(key, scope_gs)
	gc = gspread.authorize(credentials_gs)
	sh = gc.open_by_url(SS_ADDRESS)
	worksheet_all = sh.get_worksheet(0)
	sh = gc.open_by_url(SS_ADDRESS)
	worksheet_old = sh.worksheet(sheetname)

	# Get Google Sheets official API
	scope_gl = 'https://www.googleapis.com/auth/spreadsheets'
	credentials_gl = ServiceAccountCredentials.from_json_keyfile_name(key, scope_gl)
	http = credentials_gl.authorize(httplib2.Http())
	discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
	service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

	spreadsheetID = SS_ADDRESS.split('/')[5]
	print spreadsheetID
	#sheetID = SS_ADDRESS.split('/')[6].split('=')[-1:][0]
	'''
	### back up ###
	'''
	print "Backing Up ..."
	startrow = 6
	caseno = worksheet_old.cell(startrow, 3).value
	while caseno is not "":
		requests = []
		requests.append({
		    'insertDimension': {
		        "range": {"sheetId": 0, "dimension": 1, "startIndex": 5, "endIndex": 6},
		        "inheritFromBefore": False,
		    }
		})

		try:
			cell = worksheet_all.find(caseno)
			print caseno + "at: " + cell.value + "is deleted."
			requests.append({
			    'deleteDimension': {
				    "range": {
					    "sheetId": 0, "dimension": 'ROWS', "startIndex": cell.row,"endIndex": cell.row + 1,
				    },
			    }
			})
		except gspread.CellNotFound as err:
			print "Not Found in Sheet_All!"


		requests.append({
		    'copyPaste': {
			    "source": {
				    "sheetId": old_id, "startRowIndex": startrow - 1, "endRowIndex": startrow,
			    },
			    "destination": {
			    	"sheetId": 0, "startRowIndex": 5, "endRowIndex": 6,
			  },
				"pasteType": "PASTE_NORMAL",
		    }
		})
		batchUpdateRequest = {'requests': requests}
		service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetID, body=batchUpdateRequest).execute()
		startrow = startrow + 1
		caseno = worksheet_old.cell(startrow, 3).value
		#print str(startrow) + " not null: " + str(caseno)

	'''
	### New Sheet ###
	'''

	print "Creating new sheet ..."
	requests = []
	new_no = random.randrange(1, 99999999)
	title = time.strftime("%d/%m/%Y")
	requests.append({
	    'addSheet': {
		    "properties": { "sheetId": new_no, "title": title,
		},
	    }
	})
	requests.append({
	    'copyPaste': {
		    "source": {
			    "sheetId": 0, "startRowIndex": 0, "endRowIndex": 4,
		    },
		    "destination": {
		    	"sheetId": new_no, "startRowIndex": 0, "endRowIndex": 4,
			},
			"pasteType": "PASTE_NORMAL",
	    }
	})
	batchUpdateRequest = {'requests': requests}
	service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetID, body=batchUpdateRequest).execute()

	sh = gc.open_by_url(SS_ADDRESS)
	worksheet_new = sh.worksheet(title)

	'''
	### Read Data ###
	'''
	print "Reading Data ..."
	with open("data-sale-bakerrec-.csv","rb") as csvfile:
		filereader = csv.reader(csvfile)
		data = list(filereader)
		row_count = len(data)

	print "--------------------------------------------------"
	print "Hunterdon County has " + str(row_count/8) + " items!"
	print "--------------------------------------------------"

	start = 6
	for index, line in enumerate(data[1:], start=0): 
		#print line
		if line[0] is not "":
			try:
				caseno = str(int(round(float(line[0]))))
				print caseno
				cell = worksheet_all.find(caseno)
				date = worksheet_all.cell(cell.row, 1).value
				address = worksheet_all.cell(cell.row, 6).value
				town = ""


				print str(cell.row) + "/" + str(cell.col) + ": " + str(cell.value)
				requests = []
				requests.append({
				    'copyPaste': {
					    "source": {
						    "sheetId": 0, "startRowIndex": cell.row - 1, "endRowIndex": cell.row,
					    },
					    "destination": {
						  	"sheetId": new_no, "startRowIndex": start - 1, "endRowIndex": start,
					  },
						"pasteType": "PASTE_NORMAL",
				    }
				})

				batchUpdateRequest = {'requests': requests}

				service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetID, body=batchUpdateRequest).execute()
				worksheet_new.update_cell(start, 9, line[47]) #upset
				worksheet_new.update_cell(start, 1, date + "->" + line[38]) #date
				worksheet_new.update_cell(start, 16, line[63]) #status
				

			except gspread.CellNotFound as err:
				print ("CellNotFound!")

				worksheet_new.update_cell(start, 1, line[38]) #date
				worksheet_new.update_cell(start, 3, line[0]) #case
				address = line[55]
				city = line[62]
				town = " ".join(city.split()[2:])
				worksheet_new.update_cell(start, 6, line[55] + "\n" + town + " NJ") #add
				#worksheet.update_cell(start, 7, town) #city
				worksheet_new.update_cell(start, 9, line[47]) #upset
				worksheet_new.update_cell(start, 5, line[70]) #firm

				worksheet_new.update_cell(start, 16, data[index+3][1]) #status
				worksheet_new.update_cell(start, 4, data[index+5][1]) #plantiff
				#worksheet_new.update_cell(start, 18, data[index+6][1]) #defe

			except ValueError as err:
				continue

			#zillow = zillow_functions.findzillow(address, town)
			#print zillow
			#worksheet.update_cell(start, 7, "\n".join(zillow[3][:]) + "\n" + town)
			#worksheet.update_cell(start, 14, "\n".join(zillow[0][:])) #zillowID
			zipcode = address.split(" ")[-1:]
			print zipcode
			if zipcode[0].isdigit():
				#print "IS DIGIT"
				zillow = zillow_functions.find_zillow_by_zip(address, zipcode)
			else:
				zillow = zillow_functions.findzillow(address, town)
			print zillow
			worksheet_new.update_cell(start, 12, zillow[1]) #zestimate
			#add = worksheet_new.cell(start, 6).value
			#worksheet.update_cell(start, 6, "\n".join(zillow[2][:])+ ", " + add)
			start=start+1
