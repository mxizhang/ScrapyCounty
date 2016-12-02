import requests
from lxml import html

ZIL_KEY = 'X1-ZWz1fe5w83qcjv_70ucn'

def findzillow(address, zipcode):
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
	else:
		url_search = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=' + ZIL_KEY +'&address=' + address + '&citystatezip=' + zipcode
		#print url_search
		'''
		deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
		result = GetDeepSearchResults(deep_search_response)
		zpid = [result.zillow_id]
		#print zpid
		url = 'http://www.zillow.com/webservice/GetZestimate.htm?zws-id=' + ZIL_KEY +'&zpid=' + zid
		print url
		'''
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
'''
address = "159 GREGORY AVE WEST ORANGE NJ 07052"
z = findzillow(address, '07052')
print z
'''