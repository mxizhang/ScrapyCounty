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

ESS_ADDS = 'https://docs.google.com/spreadsheets/d/1isOSOsyvGFTuCZwuqEEkmou0uxWm9AVCrNx_V0_JDmc/edit#gid=0'
MIS_ADDS = 'https://docs.google.com/spreadsheets/d/1W-6ngztdGnx-N2-YA8v7dtOgw39OYi9cauYtMa4t-lw/edit#gid=0'
UNI_ADDS = 'https://docs.google.com/spreadsheets/d/1koChyqS8UbXCoWV662YY8zVXT57lR4snW6j5aMrU1Rw/edit#gid=0'
KEY = 'Project havingfun-e21e4cd12c11.json'

essex = {'name': 'Essex', 'csv': 'essex_items.csv', 'add': ESS_ADDS}
union = {'name': 'Union', 'csv': 'union_items.csv', 'add': UNI_ADDS}
middlesex = {'name': 'Middlesex', 'csv': 'middlesex_items.csv', 'add': MIS_ADDS}
'''
result = service.spreadsheets().values().get(
    spreadsheetId=spreadsheetID, range='C6', valueRenderOption='FORMULA').execute()
print result['values'][0][0]
'''
COUNTY = [essex, union, middlesex]
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