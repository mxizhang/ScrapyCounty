
import requests
from lxml import html
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults

def findzillow(address, township):
	zillow_data = ZillowWrapper("X1-ZWz1fe5w83qcjv_70ucn")
	#address = "45 RIDGE ROAD"
	address = "+".join(address.split())
	#city = "TOWNSHIP OF EAST AMWELL"
	township = "+".join(township.split())
	url = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=X1-ZWz1fe5w83qcjv_70ucn&address=' + address + '&citystatezip='+ township + '+NJ'
	#print (url)
	page = requests.get(url)
	tree = html.fromstring(page.content)

	zpid = tree.xpath('//zpid/text()')

	#This will create a list of prices
	prices = tree.xpath('//amount/text()')
	link = tree.xpath('//homedetails/text()')
	zipcode = tree.xpath('//zipcode/text()')
	zillow = [zpid, prices, link, zipcode]
	return zillow
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
