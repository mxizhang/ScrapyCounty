import requests
from lxml import html
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults, ZillowError

ZIL_KEY = 'X1-ZWz1fe5w83qcjv_70ucn'

def findzillow(address, zipcode):
	zillow_data = ZillowWrapper(ZIL_KEY)
	if zipcode == '':
		#print "No Zipcode"
		address = address.replace(' ', '+')
		url_search = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=' + ZIL_KEY +'&address=' + address + '&citystatezip=NJ'
		#print url_search
		tree = html.fromstring(requests.get(url_search).content)
		zpid = tree.xpath('//zpid/text()')
		prices = tree.xpath('//amount/text()')
		link = tree.xpath('//homedetails/text()')
		zipcode = tree.xpath('//zipcode/text()')
		try:
			zillow = [zpid[0], prices[0], link[0], zipcode[0]]
			return zillow
		except IndexError as err:
			print ("Index expecption!")
			return ['', '', '', '']
	try:
		deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
		result = GetDeepSearchResults(deep_search_response)
		zid = result.zillow_id
		#print zid
		url = 'http://www.zillow.com/webservice/GetZestimate.htm?zws-id=' + ZIL_KEY +'&zpid=' + zid
		#print url
		page = requests.get(url)
		tree = html.fromstring(page.content)
		prices = tree.xpath('//amount/text()')
		link = tree.xpath('//homedetails/text()')
		zillow = [zid, prices[0], link[0], zipcode[0]]
		return zillow

	except ZillowError as err:
		print ("No Zillow Found!")
		return ['', '', '', '']
	except IndexError as err:
		print ("Index expecption!")
		return ['', '', '', '']
'''
address = "6 WERTSVILLE ROAD EAST AMWELL NJ"
z = findzillow(address, '')
print z
if z[2] == '':
	print "=="
else:
	print "y"
'''