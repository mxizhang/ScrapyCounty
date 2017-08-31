# -*- coding: utf-8 -*-
# -*- author: mxiz -*-
import os.path
from gspread import *
from zillow_function import findzillow
import tkMessageBox
import njlispendens
from apiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
from normal_mode import *

MRS_ADDS = 'https://docs.google.com/spreadsheets/d/1v5sNJuIiLGwU6fH9Kpfr9XRxQCxrf7bx_PR_1fNA_6Q/edit#gid=0'
ESS_ADDS = 'https://docs.google.com/spreadsheets/d/1isOSOsyvGFTuCZwuqEEkmou0uxWm9AVCrNx_V0_JDmc/edit#gid=0'
BGN_ADDS = 'https://docs.google.com/spreadsheets/d/1aZBeaENA0xjxqpmKYNDrjIM4c_zy-MhHuLaunmPLv98/edit#gid=0'
HTD_ADDS = 'https://docs.google.com/spreadsheets/d/1kjiHt_daqvIueDw6qD7wk75mTFo0_ubRUFCnHNn4J8E/edit#gid=0'
MIS_ADDS = 'https://docs.google.com/spreadsheets/d/1W-6ngztdGnx-N2-YA8v7dtOgw39OYi9cauYtMa4t-lw/edit#gid=0'
UNI_ADDS = 'https://docs.google.com/spreadsheets/d/1koChyqS8UbXCoWV662YY8zVXT57lR4snW6j5aMrU1Rw/edit#gid=0'
MEC_ADDS = 'https://docs.google.com/spreadsheets/d/1c2AiIahiFZFA37FCa5SJOcsWDXJQxa3qwmHw0rlB7eY/edit#gid=0'
MON_ADDS = 'https://docs.google.com/spreadsheets/d/1RHMczsQ6mpajEZT0gYcJqCXz3FR5SSZepxXZnGTXmy4/edit#gid=0'
PSC_ADDS = 'https://docs.google.com/spreadsheets/d/1zlClRl91bAcBtG1zA5NlyOHqUoV1wYHfnzyl_mof1qw/edit#gid=0'

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
'''
result = service.spreadsheets().values().get(
    spreadsheetId=spreadsheetID, range='C6', valueRenderOption='FORMULA').execute()
print result['values'][0][0]
'''
COUNTY = [morris, essex, bergen, hunterdon, union, mercer, middlesex, monmouth, passaic]
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
		njlispendens.njlis_pic(num)
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

#manual_mode(5, '02/18/2017', '02/27/2017', 48)