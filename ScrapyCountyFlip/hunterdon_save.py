import urllib2
import requests
from openpyxl import load_workbook
import csv

FILENAME_PDF = "sale.pdf"
FILENAME_CSV = "sale.xlsx"

def hunterdon_save():
    download_file("http://www.co.hunterdon.nj.us/sheriff/SALES/sales.pdf")
    convert_to_xlsx()
    csv_read()

def download_file(download_url):
    response = urllib2.urlopen(download_url)
    file = open(FILENAME_PDF, 'wb')
    file.write(response.read())
    file.close()

def convert_to_xlsx():
    try:
        files = {'f': (FILENAME_PDF, open(FILENAME_PDF, 'rb'))}
        response = requests.post("https://pdftables.com/api?key=lhfxwj5qn8jg&format=xlsx-single", files=files) # $50 for 2500 pdfs
        response.raise_for_status() # ensure we notice bad responses
        with open(FILENAME_CSV, "wb") as f:
            f.write(response.content)
        f.close()
    except IOError as e:
        print "Error: File does not appear to exist."

def csv_read():
    wb = load_workbook(filename='sale.xlsx', read_only=True)
    ws = wb['PDFTables.com'] # ws is now an IterableWorksheet

    list_all = []
    list_all.append(['sale_date', 'sheriff_no', 'upset', 'att_ph', 'case_no', 'plf', 'att', 'address', 'dfd', 'schd_data'])
    item = [0 for x in range(10)]
    l = list(ws.rows)
    num = 0
    for index, row in enumerate(l):
        if row[0].value == 'Case #':
            #print 'Case: ' + str(l[index+1][0].value) + '/Date: ' + l[index+1][1].value + '/Asset: ' + str(l[index+1][4].value) + '/Address: ' + l[index+1][5].value
            item = [0 for x in range(10)]
            item[0] = l[index+1][1].value #Date
            item[1] = str(l[index+1][0].value) #Caseno
            if l[index][5].value == 'JUDGEMENT':
                item[2] = l[index+1][5].value #asset
                num = 5
            elif l[index][4].value == 'JUDGEMENT':
                item[2] = l[index+1][4].value #asset
                num = 4
            else:
                item[2] = l[index+1][3].value 
                num = 3
            #print l[index+1][num+1].value
            if l[index+1][num+2].value == None:
                item[7] = str(l[index+1][num+1].value) #address
            else:
                item[7] = str(l[index+1][num+1].value) + l[index+1][num+2].value #address
            #print 'case#: '+ item[1] + '/asset: ' + l[index+1][num].value  
        elif row[num+1].value == 'City':
            city = l[index+1][num+1].value.split(' ')
            for index in range(len(city)):
                if city[index] == 'OF':
                    #print item[7]
                    #print " ".join(city[index+1:])
                    item[7] = item[7] + " " + " ".join(city[index+1:])
        elif row[0].value == 'Plaintiff':
            item[5] = l[index+1][0].value
        elif row[0].value == 'Defendant':
            item[8] = l[index+1][0].value
        elif row[num+1].value == 'FIRM':
            item[6] = l[index+1][num+1].value
        elif row[num+1].value == 'TELEPHONE':
            item[3] = l[index+1][num+1].value
            print item
            list_all.append(item)

    with open("hunterdon_items.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(list_all)
