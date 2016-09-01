import subprocess
from oauth2client.service_account import ServiceAccountCredentials
import morris_write
import essex_write
import hunterdon_write
import hunterdon_save
import bergen_write

MRS_ADDS = 'https://docs.google.com/spreadsheets/d/1XOkErm0Oah2zSx2rcJoV0OAGQx8DL-C--iOfZIhXXRs/edit#gid=0'
ESS_ADDS = 'https://docs.google.com/spreadsheets/d/1XOkErm0Oah2zSx2rcJoV0OAGQx8DL-C--iOfZIhXXRs/edit#gid=1826898806'
BGN_ADDS = 'https://docs.google.com/spreadsheets/d/1XOkErm0Oah2zSx2rcJoV0OAGQx8DL-C--iOfZIhXXRs/edit#gid=1623951483'
HTD_ADDS = 'https://docs.google.com/spreadsheets/d/1E4QyRyH2aS_XqeDkWkeZPDZn74gj9l1m1LU5GcZoMfE/edit#gid=558163237'
KEY = 'My Project-f09bdc10eb52.json'

def main():
    print "Welcome to Scrapy County, choose county:"
    print "Morris (M)"
    print "Essex (E)"
    print "Bergen (B)"
    print "Hunterdon (H)"
    num = raw_input("your choice?")
    if num == 'M':
        morris(MRS_ADDS, KEY)
    elif num == 'E':
        essex(ESS_ADDS, KEY)
    elif num == 'B':
        bergen(BGN_ADDS, KEY)
    elif num == 'H':
        print "Please enter current Sheet ID: "
        id = raw_input("Sheet ID is: ")
        print "Please enter current Sheet ID: "
        name = raw_input("Sheet Name is: ")
        hunterdon(HTD_ADDS, KEY, id, name)
    else:
        print "NOT FOUND! "

def morris(address, key):
    print "Morris County is called."
    subprocess.call("scrapy crawl morris -o morris_items.csv", shell=True)
    morris_write.morris_write(address, key)
def bergen(address, key):
    print "Bergen County is called."
    subprocess.call("scrapy crawl bergen -o bergen_items.csv", shell=True)
    bergen_write.bergen_write(address, key)
def essex(address, key):
    print "Essex County is called."
    subprocess.call("scrapy crawl essex -o essex_items.csv", shell=True)
    essex_write.essex_write(address, key)
def hunterdon(address, key, id, name):
    #hunterdon_save.hunterdon_save()
    hunterdon_write.hunterdon_write(address, key, id, name)


if __name__ == "__main__":
    main()