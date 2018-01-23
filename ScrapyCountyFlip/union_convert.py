from gspread import *
from zillow_function import findzillow
import httplib2
from Tkinter import *
from apiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials

UNI_ADDS = 'https://docs.google.com/spreadsheets/d/1koChyqS8UbXCoWV662YY8zVXT57lR4snW6j5aMrU1Rw/edit#gid=0'
KEY = 'flipnj-4f3fbac03d23.json'
union = {'name': 'Union', 'csv': 'union_items.csv', 'add': UNI_ADDS}

def main():
	global county_info, service
	service = get_google_service()
	spreadsheetID = UNI_ADDS.split('/')[5]
	worksheet_all_name = find_sheetname(spreadsheetID, 77541267)
	worksheet_all = get_gspread(UNI_ADDS, worksheet_all_name)

	for i in range(7, 76):
		address = worksheet_all.cell(i, 3).value
		#print address
		zipcode = address.split(' ')[-1]
		town = address.split(' ')[-3]
		street = " ".join(address.split(' ')[0:-3])
		print "[%s/%s/%s]" % (street, town, zipcode)
		worksheet_all.update_cell(i, 4, town)
		worksheet_all.update_cell(i, 5, zipcode)


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

main()