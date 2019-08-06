# -*- coding: utf-8 -*-
# -*- author: mxiz -*-
import os.path
from gspread import *
from normal_mode import *

ESS_ADDS = 'https://docs.google.com/spreadsheets/d/11-NTooLrJf9NdzT_mdNECmXNi8oDZQnB-FMoy510Hx0/edit#gid=0'
MIS_ADDS = 'https://docs.google.com/spreadsheets/d/19R_7CYe1m07S6e3ZPpH5UphZE-lDEp2P0Fi-j7DSmO0/edit#gid=0'
UNI_ADDS = 'https://docs.google.com/spreadsheets/d/1Ut4Kcz2zd8VNw-J1SQOhe1yD4HC86J9JZA3oy-Lm2a4/edit#gid=0'
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
def manual_mode(num, old_tab_name, worksheet_new_name, startrow):
	county_info = match(num, old_tab_name)
	county = county_info['county']
	filename = county['csv']
	### check .csv file ###
	if os.path.isfile(filename):
		pass
	else:
		print "Error!!!!!"
		print "Not found .csv file.\nPlease run in normal mode first."
		#tkMessageBox.showerror("Error!", "Not found .csv file.\nPlease run in normal mode first.")


	if startrow is not 0:

		### write manully ###
		try:
			print "--------------------------------------------------"
			print county['name'] + " County starts from NO. " + str(startrow-5) + " item!"
			read_and_write(county_info, worksheet_new_name, startrow)
		except:
			print "--------------------------------------------------"
			print "\t\tNetwork problem. please try again."
			print "--------------------------------------------------"
			#tkMessageBox.showerror("Error!", "Network Problem.\nPlease run it again.")
			quit()
	#tkMessageBox.showinfo("Congrats", "Finished! \nPlease wait until back-up process done.")
	### Back Up ###
	back_up(county_info)
	'''
	print "-----------------------------------------------------------"
	print "\t\tBackup Done! Wait for NJlispendens"
	print "-----------------------------------------------------------"
	'''

	### NJLispenden ###
	
	print "-----------------------------------------------------------"
	print "\t\tAll Done! Exit anytime."
	print "-----------------------------------------------------------"

#manual_mode(4, '01/22/2018', '01/24/2018', 160)