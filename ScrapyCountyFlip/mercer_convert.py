from openpyxl import load_workbook
import csv
import datetime
def main():
	wb = load_workbook(filename='Mercer_lisp\sheriff_foreclosuresales_l.xlsx')
	ws = wb['Sheet1'] # ws is now an IterableWorksheet

	list_all = []
	list_all.append(['sale_date', 'sheriff_no', 'upset', 'att_ph', 'case_no', 'plf', 'att', 'address', 'dfd', 'schd_data'])
	item = [0 for x in range(10)]
	l = list(ws.rows)
	flag = False

	def next_weekday(d, weekday):  # 0 = Monday, 1=Tuesday, 2=Wednesday...
	    days_ahead = weekday - d.weekday()
	    if days_ahead <= 0:  # Target day already happened this week
	        days_ahead += 7
	    return d + datetime.timedelta(days_ahead)

	we = next_weekday(datetime.datetime.today(), 2)
	WE = we.strftime('%m/%d/%Y')

	for index, row in enumerate(l):
		if row[0].value == "Original Sale Date:":
			ori_date = row[1].value # original sale date
			file_no = row[3].value #file no
			case_no = row[4].value.split(' ')[-1] #court no

		elif row[0].value == "Current Sale Date:":
			if row[1].value == WE:
				flag = True
				item = [0 for x in range(10)]
				item[9] = ori_date # original sale date
				item[1] = file_no #file no
				item[4] = case_no #court no
				#print item
			else: 
				flag = False
				continue
			item[0] = row[1].value #current date
			if row[3].value == None: #plf
				item[5] = row[4].value
			else:
				item[5] = row[3].value
			if row[5].value == None:
				item[2] = row[6].value #asset
			else:
				item[2] = row[5].value
			
		elif row[2].value == "Defendant":
			if row[3].value == None:
				item[8] = row[4].value
			else:
				item[8] = row[3].value
		
		elif row[2].value == "Attorney":
			if row[3].value == None:
				item[6] = row[4].value
			else:
				item[6] = row[3].value
		

		elif row[2].value == "Location:":
			#print index, row[2].value

			if l[index+1][3].value != None and l[index+1][2].value == None:
				item[7] = row[3].value + ' ' + l[index+1][3].value
			else:
				item[7] = row[3].value
			if flag:
				print item
				list_all.append(item)
				item = [0 for x in range(10)]

		elif row[3].value == "Location:":
			item[7] = row[4].value
			if flag:
				print item
				list_all.append(item)
				item = [0 for x in range(10)]

	'''
	count = 0
	for line in list_all:
		print count
		print len(line), line
		count = count + 1
	'''
	with open("mercer_items.csv", "wb") as f:
	    writer = csv.writer(f)
	    writer.writerows(list_all)
	    
if __name__ == "__main__":
    main()