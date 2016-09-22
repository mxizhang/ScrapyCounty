import csv
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def essex_lis(foldername):
	try:
	    os.makedirs('./' + foldername)
	except OSError:
	    pass
	driver = webdriver.PhantomJS()
	driver.get("https://njlispendens.com/properties")

	print "#################Logging In################"
	user = driver.find_element_by_name("amember_login")
	user.send_keys("Flipping_gr0up")
	pasw = driver.find_element_by_name("amember_pass")
	pasw.send_keys("Flipping_gr0up")

	driver.find_element_by_xpath("/html/body/table/tbody/tr[3]/td[2]/form[1]/table/tbody/tr[4]/td/input").click()

	print driver.title

	print "#################Reading Data################"
	with open("essex_items.csv","rb") as csvfile:
		filereader = csv.reader(csvfile)
		data = list(filereader)

	for index, line in enumerate(data[1:], start=0):
		caseno = line[4]
		address = line[7]
		zip = address.split(' ')[-1:][0]
		street = address.split(' ')[0] + " " + address.split(' ')[1]

		street_input = driver.find_element_by_name("Address")
		zip_input = driver.find_element_by_name("Zip_Code")

		street_input.clear()
		zip_input.clear()

		street_input.send_keys(street)
		if zip.isdigit():
			print "NO: " + str(zip) + " + " + str(street)
			zip_input.send_keys(zip)
		else:
			print str(zip) + " + " + str(street)


		driver.find_element_by_name("submit").click()

		driver.get_screenshot_as_file('essex/' + caseno + '.png');
		driver.back()