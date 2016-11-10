from openpyxl import load_workbook
import csv
wb = load_workbook(filename='sale.xlsx', read_only=True)
ws = wb['PDFTables.com'] # ws is now an IterableWorksheet

list_all = []
list_all.append(['sale_date', 'sheriff_no', 'upset', 'att_ph', 'case_no', 'plf', 'att', 'address', 'dfd', 'schd_data'])
item = [0 for x in range(10)]
l = list(ws.rows)
for index, row in enumerate(l):
	if row[0].value == 'Case #':
		print 'Case: ' + str(l[index+1][0].value) + '/Date: ' + l[index+1][1].value + '/Asset: ' + str(l[index+1][4].value) + '/Address: ' + l[index+1][5].value
		item = [0 for x in range(10)]
		item[0] = l[index+1][1].value #Date
		item[1] = str(l[index+1][0].value) #Caseno
		if l[index+1][4].value == None:
			item[2] = l[index+1][3].value #asset
		else:
			item[2] = l[index+1][4].value 
		item[7] = l[index+1][5].value #address
	elif row[5].value == 'City':
		city = l[index+1][5].value.split(' ')
		for index in range(len(city)):
			if city[index] == 'OF':
				#print city[index+1:]
				#print " ".join(city[index+1:])
				item[7] = item[7] + " " + " ".join(city[index+1:])
	elif row[0].value == 'Plaintiff':
		item[5] = l[index+1][0].value
	elif row[0].value == 'Defendant':
		item[8] = l[index+1][0].value
	elif row[5].value == 'FIRM':
		item[6] = l[index+1][5].value
	elif row[5].value == 'TELEPHONE':
		item[3] = l[index+1][5].value
		print item
		list_all.append(item)

with open("hunterdon_items.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(list_all)