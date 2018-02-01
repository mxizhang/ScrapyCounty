# -*- coding: utf-8 -*-
# -*- author: mxiz -*-
import time
from gspread import *
import csv
from zillow_function import findzillow
import httplib2
import random
import os
import subprocess
import mercer_convert
from Tkinter import *
import njlispendens
from apiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials

MRS_ADDS = 'https://docs.google.com/spreadsheets/d/1v5sNJuIiLGwU6fH9Kpfr9XRxQCxrf7bx_PR_1fNA_6Q/edit#gid=0'
ESS_ADDS = 'https://docs.google.com/spreadsheets/d/1isOSOsyvGFTuCZwuqEEkmou0uxWm9AVCrNx_V0_JDmc/edit#gid=0'
BGN_ADDS = 'https://docs.google.com/spreadsheets/d/1aZBeaENA0xjxqpmKYNDrjIM4c_zy-MhHuLaunmPLv98/edit#gid=0'
HTD_ADDS = 'https://docs.google.com/spreadsheets/d/1kjiHt_daqvIueDw6qD7wk75mTFo0_ubRUFCnHNn4J8E/edit#gid=0'
MIS_ADDS = 'https://docs.google.com/spreadsheets/d/1W-6ngztdGnx-N2-YA8v7dtOgw39OYi9cauYtMa4t-lw/edit#gid=0'
UNI_ADDS = 'https://docs.google.com/spreadsheets/d/1koChyqS8UbXCoWV662YY8zVXT57lR4snW6j5aMrU1Rw/edit#gid=0'
MEC_ADDS = 'https://docs.google.com/spreadsheets/d/1c2AiIahiFZFA37FCa5SJOcsWDXJQxa3qwmHw0rlB7eY/edit#gid=0'
MON_ADDS = 'https://docs.google.com/spreadsheets/d/1RHMczsQ6mpajEZT0gYcJqCXz3FR5SSZepxXZnGTXmy4/edit#gid=0'
PSC_ADDS = 'https://docs.google.com/spreadsheets/d/1zlClRl91bAcBtG1zA5NlyOHqUoV1wYHfnzyl_mof1qw/edit#gid=0'
HDS_ADDS = 'https://docs.google.com/spreadsheets/d/1QEZFHVAlLpKRsUOB0Gfai7C9h7fcasWIuuuUVAwDIm0/edit#gid=0'
BLT_ADDS = 'https://docs.google.com/spreadsheets/d/1zs2fKbSWRFKMH2qSxcHhMhD7ntI952w4ihPJ9lzNbEg/edit#gid=0'
KEY = 'flipnj-4f3fbac03d23.json'

morris = {'name': 'Morris', 'csv': 'morris_items.csv', 'add': MRS_ADDS}
essex = {'name': 'Essex', 'csv': 'essex_items.csv', 'add': ESS_ADDS}
bergen = {'name': 'Bergen', 'csv': 'bergen_items.csv', 'add': BGN_ADDS}
hunterdon = {'name': 'Hunterdon', 'csv': 'hunterdon_items.csv', 'add': HTD_ADDS}
union = {'name': 'Union', 'csv': 'union_items.csv', 'add': UNI_ADDS}
mercer = {'name': 'Mercer', 'csv': 'mercer_items.csv', 'add': MEC_ADDS}
middlesex = {'name': 'Middlesex', 'csv': 'middlesex_items.csv', 'add': MIS_ADDS}
monmouth = {'name': 'Monmouth', 'csv': 'monmouth_items.csv', 'add': MON_ADDS}
passaic = {'name': 'Passaic', 'csv': 'passaic_items.csv', 'add': PSC_ADDS}
hudson = {'name': 'Hudson', 'csv': 'hudson_items.csv', 'add': HDS_ADDS}
burlington = {'name': 'Burlington', 'csv': 'burlington_items.csv', 'add': BLT_ADDS}
'''
result = service.spreadsheets().values().get(
    spreadsheetId=spreadsheetID, range='C6', valueRenderOption='FORMULA').execute()
print result['values'][0][0]
'''
COUNTY = [morris, essex, bergen, hunterdon, union, mercer, middlesex, monmouth, passaic, hudson, burlington]
'''
0             1       2      3        4    5   6    7      8    9
sale_date,sheriff_no,upset,att_ph,case_no,plf, att,address,dfd,schd_data
1      2            3           6          7         10       11        12       13
date, SHERIFF'S #, ADDRESS, Judegment,	NEW UPSET, PLF/DEF, ATTY/FIRM, DOCKET#, Zillow
'''
'''
### Match spreadsheet tab function:
	return county_info with 'old' tab and 'all' tab
'''
def match(num, tab_name):
	# Get credentials
	# Get Google Sheets official API
	global county_info, service
	county = COUNTY[num]
	SS_ADDRESS = county['add']
	spreadsheetID = SS_ADDRESS.split('/')[5]
	service = get_google_service()
	try: 
		worksheet_old = get_gspread(SS_ADDRESS, tab_name)
		worksheet_old_id = find_sheetId(spreadsheetID, tab_name)
		worksheet_all_name = find_sheetname(spreadsheetID, 0)
		worksheet_all = get_gspread(SS_ADDRESS, worksheet_all_name)
		worksheet_old_info = {'name': tab_name, 'id': worksheet_old_id, 'gspread': worksheet_old}
		worksheet_all_info = {'name': worksheet_all_name, 'id': 0, 'gspread': worksheet_all}
		county_info = {'county': county, 'worksheet_old_info': worksheet_old_info, 
						'worksheet_all_info': worksheet_all_info }
		return county_info
	except exceptions.WorksheetNotFound as err: 
		print "Please enter a valid tab name in sheet.\nAnd make sure it's not today's date."
		#tkMessageBox.showinfo("Error: Invalid Tab Name <%s>" % tab_name, "Please enter a valid tab name in sheet.")
		quit()


'''
### Normal Mode:
	
'''
def normal_mode(num, tab_name):
	county_info = match(num, tab_name)
	spreadsheetID = county_info['county']['add'].split('/')[5]
	
	### scrapy New Items ###
	if num == 3 or num == 5:
		pass
	else:
		scrapy(num, county_info['county'])
	### New Sheet ###
	worksheet_new_name = new_sheet(spreadsheetID)
	#tkMessageBox.showinfo("Congrats", "New Sheet! \nPlease wait for reading & writing data.")
	### Read Write ###
	read_and_write(county_info, worksheet_new_name)
	print "-----------------------------------------------------------"
	print "\t\tNew Sheet is ready! Please wait for backup process "
	print "-----------------------------------------------------------"
	#print "Finished Read & Write"
	#tkMessageBox.showinfo("Congrats", "Finished! \nPlease wait until back-up process done.")

	#print "Finished Read & Write"
	#tkMessageBox.showinfo("Congrats", "Finished! \nPlease wait until back-up process done.")
	
	### Back Up ###
	back_up(county_info)
	'''
	print "-----------------------------------------------------------"
	print "\t\tBackup Done! Wait for NJlispendens"
	print "-----------------------------------------------------------"
	'''
	### NJLispenden ###
	njlispendens.njlis_pic(num)
	
	print "-----------------------------------------------------------"
	print "\t\tAll Done! Exit anytime."
	print "-----------------------------------------------------------"
	

def back_up(county_info):
	worksheet_old = county_info['worksheet_old_info']['gspread']
	worksheet_all = county_info['worksheet_all_info']['gspread']
	spreadsheetID = county_info['county']['add'].split('/')[5]
	print "Backing Up ..."
	startrow = 6
	caseno = worksheet_old.cell(startrow, 2).value
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
			print "%s at %s is updated." % (caseno, cell.row)
			requests.append({
			    'deleteDimension': {
				    "range": {
					    "sheetId": 0, "dimension": 'ROWS', "startIndex": cell.row, "endIndex": cell.row + 1,
				    },
			    }
			})
		except CellNotFound as err:
			print "Not Found in Sheet_All!"

		requests.append({
		    'copyPaste': {
			    "source": {
				    "sheetId": county_info['worksheet_old_info']['id'], "startRowIndex": startrow - 1, "endRowIndex": startrow,
			    },
			    "destination": {
			    	"sheetId": 0, "startRowIndex": 5, "endRowIndex": 6,
			  },
				"pasteType": "PASTE_NORMAL",
		    }
		})
		startrow = startrow + 1
		caseno = worksheet_old.cell(startrow, 2).value
		batchUpdateRequest = {'requests': requests}
		service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetID, body=batchUpdateRequest).execute()
	#tkMessageBox.showinfo("Done!", "Back-up process is done.\n You can exit anytime.")

def read_and_write(county_info, worksheet_new_name, start=6):
	county = county_info['county']
	filename = county['csv']
	SS_ADDRESS = county['add']
	spreadsheetID = SS_ADDRESS.split('/')[5]

	print "Reading Data ..."
	with open(filename, "rb") as csvfile:
		filereader = csv.reader(csvfile)
		data = list(filereader)
		row_count = len(data)

	print "--------------------------------------------------"
	print county['name'] + " County has " + str(row_count-1) + " items!"
	print "--------------------------------------------------"

	worksheet_new = get_gspread(SS_ADDRESS, worksheet_new_name)
	worksheet_old = county_info['worksheet_old_info']['gspread']
	worksheet_all = county_info['worksheet_all_info']['gspread']
	for line in data[start-5:]:
		caseno = line[1]
		new_no = find_sheetId(spreadsheetID, worksheet_new_name)

		try:
			cell = worksheet_old.find(caseno)
			Found = True
			date = worksheet_old.cell(cell.row, 1).value
			address = worksheet_old.cell(cell.row, 3).value
			address = address.replace(',', ' ')
			address = address.replace('\n', ' ')
			print "Found in old " + str(cell.row) + "/" + str(cell.col) + ": " + str(cell.value)

			requests = []
			requests.append({
			    'copyPaste': {
				    "source": {
					    "sheetId": county_info['worksheet_old_info']['id'], "startRowIndex": cell.row - 1, "endRowIndex": cell.row, },
				    "destination": {
					  	"sheetId": new_no, "startRowIndex": start - 1, "endRowIndex": start, },
					"pasteType": "PASTE_NORMAL",
			    }
			})
			batchUpdateRequest = {'requests': requests}
			service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetID, body=batchUpdateRequest).execute()
			worksheet_new.update_cell(start, 6, line[2]) #upset
			if date != line[0]:
				worksheet_new.update_cell(start, 1, date + "->" + line[0]) #date
		
		except CellNotFound as err:
			try:
				cell = worksheet_all.find(caseno)
				Found = True
				date = worksheet_all.cell(cell.row, 1).value
				address = worksheet_all.cell(cell.row, 3).value
				address = address.replace(',', ' ')
				address = address.replace('\n', ' ')
				print "Found in all " + str(cell.row) + "/" + str(cell.col) + ": " + str(cell.value)

				requests = []
				requests.append({
				    'copyPaste': {
					    "source": {
						    "sheetId": 0, "startRowIndex": cell.row - 1, "endRowIndex": cell.row, },
					    "destination": {
						  	"sheetId": new_no, "startRowIndex": start - 1, "endRowIndex": start, },
						"pasteType": "PASTE_NORMAL",
				    }
				})
				batchUpdateRequest = {'requests': requests}
				service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetID, body=batchUpdateRequest).execute()
				worksheet_new.update_cell(start, 6, line[2]) #upset
				if date != line[0]:
					worksheet_new.update_cell(start, 1, date + "->" + line[0]) #date
			except CellNotFound as err:
				print ("New Item!")
				Found = False
				if line[0] == line[9] or line[9] == 0:
					worksheet_new.update_cell(start, 1, line[0]) #date
				else:
					worksheet_new.update_cell(start, 1, line[9] + '->' + line[0]) #date
				worksheet_new.update_cell(start, 2, line[1]) #shriff
				worksheet_new.update_cell(start, 12, line[4]) #case
				#worksheet_new.update_cell(start, 6, line[55]) #add
				address = line[7].replace('\n', ' ')
				worksheet_new.update_cell(start, 6, line[2]) #upset
				if line[3] == '':
					worksheet_new.update_cell(start, 11, line[6]) #att
				else:
					worksheet_new.update_cell(start, 11, line[6] + '\nPhone: ' + line[3]) #date
				#worksheet_new.update_cell(start, 16, line[1]) #status
				if county['name'] is "Burlington":
					worksheet_new.update_cell(start, 10, line[5])
					worksheet_new.update_cell(start, 14, line[8])
				else:
					worksheet_new.update_cell(start, 10, 'PLF: ' + line[5] + '\nDEF:' + line[8]) #plantiff

		zipcode = address.split(" ")[-1:][0]
		#print zipcode
		if zipcode.isdigit():
			#print "IS DIGIT"
			zillow = findzillow(address, zipcode)
		else:
			zillow = findzillow(address, '')
			if zillow[3] is not '':
				#print "!!!Address replaced"
				address = address + ' ' + zillow[3] 
		#print zillow
		worksheet_new.update_cell(start, 13, zillow[1]) #zestimate
		if zillow[2] == '' and Found:
			pass
		elif zillow[2] == '' and not Found:
			#print line
			worksheet_new.update_cell(start, 3, address) #add	
		else:
			requests = []
			requests.append({
			    'updateCells': {
				    "rows": { 
				    	"values": [{
				    		"userEnteredValue": {
				    			"formulaValue": '=HYPERLINK("' + zillow[2] + '","' + address + '")', }, }], },
				    "fields": "*",
				    "start": {
				    	"sheetId": new_no, "rowIndex": start - 1, "columnIndex": 2,},}
			})
			batchUpdateRequest = {'requests': requests}
			service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetID, body=batchUpdateRequest).execute()

		start=start+1
		print "%s out of %s is finished." % (start-6, row_count-1)

def new_sheet(spreadsheetID):
	try:
		print "Creating new sheet ..."
		requests = []
		new_no = random.randrange(1, 99999999)
		worksheet_new_name = time.strftime("%m/%d/%Y")
		requests.append({
		    'addSheet': {
			    "properties": { "sheetId": new_no, "title": worksheet_new_name,
			}, }
		})
		# Copy Title
		requests.append({
		    'copyPaste': {
			    "source": {
				    "sheetId": 0, "startRowIndex": 0, "endRowIndex": 4,},
			    "destination": {
			    	"sheetId": new_no, "startRowIndex": 0, "endRowIndex": 4,},
				"pasteType": "PASTE_NORMAL", }
		})
		batchUpdateRequest = {'requests': requests}
		service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetID, body=batchUpdateRequest).execute()
		return worksheet_new_name

	except HttpError as err:
		print "Google Error. Already Exists"
		print "Please enter a valid tab name in sheet."
		#tkMessageBox.showinfo("Error: Existed Tab Name", "A existed Tab name.\nPlease delete today's tab name or run it another day.")
		quit()

def scrapy(num, county):
	countyname = county['name']
	filename = county['csv']
	try:
		os.remove(filename)
	except OSError:
		pass
	print "%s county is scraping..." % countyname
	subprocess.call("scrapy crawl %s -o %s" % (countyname.lower(), filename), shell=True)
	print "%s county done scraping" % countyname

def get_gspread(SS_ADDRESS, sheetname):
	scope_gs = ['https://spreadsheets.google.com/feeds']
	credentials_gs = ServiceAccountCredentials.from_json_keyfile_name(KEY, scope_gs)
	gc = authorize(credentials_gs)
	sh = gc.open_by_url(SS_ADDRESS)
	worksheet = sh.worksheet(sheetname)
	return worksheet

def get_google_service():
	scope_gl = 'https://www.googleapis.com/auth/spreadsheets'
	credentials_gl = ServiceAccountCredentials.from_json_keyfile_name(KEY, scope_gl)
	http = credentials_gl.authorize(httplib2.Http())
	discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
	service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
	return service

def find_sheetId(spreadsheetID, sheetname):
	service = get_google_service()
	result = service.spreadsheets().get(spreadsheetId=spreadsheetID).execute()
	for item in result['sheets']:
		if item['properties']['title'] == sheetname:
			return item['properties']['sheetId']
	return None

def find_sheetname(spreadsheetID, sheetId):
	service = get_google_service()
	result = service.spreadsheets().get(spreadsheetId=spreadsheetID).execute()
	for item in result['sheets']:
		if item['properties']['sheetId'] == sheetId:
			return item['properties']['title']
	return None


#normal_mode(4, '01/22/2018')
'''
c_info = match(5, '01/02/2018')
back_up(c_info)
print '???????? finished'
'''