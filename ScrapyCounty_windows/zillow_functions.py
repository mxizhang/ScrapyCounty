
import requests
from lxml import html
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults, ZillowError

def findzillow(address, township):
	#zillow_data = ZillowWrapper("X1-ZWz1fe5w83qcjv_70ucn")
	#address = "45 RIDGE ROAD"
	#address = "+".join(address.split())
	#city = "TOWNSHIP OF EAST AMWELL"
	try:
		if township == "":
			address = "+".join(address.split()[:-1])
			url = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=X1-ZWz1fe5w83qcjv_70ucn&address=' + address + '&citystatezip=NJ'
		else:
			address = "+".join(address.split())
			township = "+".join(township.split())
			url = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=X1-ZWz1fe5w83qcjv_70ucn&address=' + address + '&citystatezip='+ township + '+NJ'
		print url
		page = requests.get(url)
		tree = html.fromstring(page.content)

		zpid = tree.xpath('//zpid/text()')

		#This will create a list of prices
		prices = tree.xpath('//amount/text()')
		link = tree.xpath('//homedetails/text()')
		zipcode = tree.xpath('//zipcode/text()')
		zillow = [zpid, prices[0], link, zipcode]
		return zillow

	except IndexError as err:
		print ("Index expecption!")
		return ['','','','']
	'''
	try:
		deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
		result = GetDeepSearchResults(deep_search_response)
		print(result.zillow_id)
		print(result.zestimate_amount)
	except pyzillow.pyzillowerrors.ZillowError as err:
		#print ("No Zillow Found!")
		zestimate = 0
	'''

def find_zillow_by_zip(address, zip):
	zillow_data = ZillowWrapper("X1-ZWz1fe5w83qcjv_70ucn")
	try:
		deep_search_response = zillow_data.get_deep_search_results(address, zip)
		result = GetDeepSearchResults(deep_search_response)
		zid = result.zillow_id
		#print zid
		url = 'http://www.zillow.com/webservice/GetZestimate.htm?zws-id=X1-ZWz1fe5w83qcjv_70ucn&zpid=' + zid
		print url
		page = requests.get(url)
		tree = html.fromstring(page.content)
		prices = tree.xpath('//amount/text()')
		zillow = [zid, prices[0]]
		return zillow
		

	except ZillowError as err:
		print ("No Zillow Found!")
		return ['','']
	except IndexError as err:
		print ("Index expecption!")
		return ['','']



'''
address = "6 WERTSVILLE ROAD EAST AMWELL NJ"
zipcode = address.split(" ")[-1:]
print zipcode
if zipcode[0].isdigit():
	print "IS DIGIT"
	z = find_zillow_by_zip(address, zipcode)
else:
	t = ""
	z = findzillow(address, t)
print z[1]
'''
