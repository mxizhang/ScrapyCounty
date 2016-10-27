from openpyxl import load_workbook
import csv
wb = load_workbook(filename='sheriff_foreclosuresales_list.xlsx', read_only=True)
ws = wb['Sheet1'] # ws is now an IterableWorksheet

list_all = []
list_all.append(['ori sale date', 'file no', 'court no', 'cur sale date', 'plf', 'asset', 'def', 'att', 'address'])
item = []
l = list(ws.rows)


for index, row in enumerate(ws.rows):
	if row[0].value == "Original Sale Date:":
		item = []
		
		item.append(row[1].value) # original sale date
		item.append(row[3].value) #file no
		item.append(row[4].value.split(' ')[-1]) #court no

	elif row[0].value == "Current Sale Date:":

		item.append(row[1].value) #current date
		if row[3].value == None: #plf
			item.append(row[4].value)
		else:
			item.append(row[3].value)
		if row[5].value == None:
			item.append(row[6].value) #asset
		else:
			item.append(row[5].value)
		
	elif row[2].value == "Defendant":
		if row[3].value == None:
			item.append(row[4].value)
		else:
			item.append(row[3].value)
	
	elif row[2].value == "Attorney":
		if row[3].value == None:
			item.append(row[4].value)
		else:
			item.append(row[3].value)
	

	elif row[2].value == "Location:":
		#print index, row[2].value

		if l[index+1][3].value != None and l[index+1][2].value == None:
			item.append(row[3].value + ', ' + l[index+1][3].value)
		else:
			item.append(row[3].value)

		list_all.append(item)

	elif row[3].value == "Location:":
		item.append(row[4].value)
		list_all.append(item)

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
