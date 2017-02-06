# -*- coding: utf-8 -*-
# -*- author: mxiz -*-
import csv
import os
import zillow_function
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

morris = {'name': 'Morris', 'csv': 'morris_items.csv'}
essex = {'name': 'Essex', 'csv': 'essex_items.csv'}
bergen = {'name': 'Bergen', 'csv': 'bergen_items.csv'}
hunterdon = {'name': 'Hunterdon', 'csv': 'hunterdon_items.csv'}
union = {'name': 'Union', 'csv': 'union_items.csv'}
mercer = {'name': 'Mercer', 'csv': 'mercer_items.csv'}
middlesex = {'name': 'Middlesex', 'csv': 'middlesex_items.csv'}
monmouth = {'name' : 'Monmouth', 'csv': 'monmouth_items.csv'}
passaic = {'name' : 'Passaic', 'csv': 'passaic_items.csv'}
hudson = {'name': 'Hudson', 'csv': 'hudson_items.csv'}

COUNTY = [morris, essex, bergen, hunterdon, union, mercer, middlesex, monmouth, passaic, hudson]

def njlis():
	driver = webdriver.PhantomJS(executable_path="C:/phantomjs-2.1.1-windows/bin/phantomjs.exe")
	driver.get("https://njlispendens.com/properties")

	print "#################Logging In################"
	user = driver.find_element_by_name("amember_login")
	user.send_keys("Flipping_gr0up")
	pasw = driver.find_element_by_name("amember_pass")
	pasw.send_keys("Flipping_gr0up")

	driver.find_element_by_xpath("/html/body/table/tbody/tr[3]/td[2]/form[1]/table/tbody/tr[4]/td/input").click()

	print driver.title
	if driver.find_element_by_name("amember_login"):
		print "Error!!! --- Disabled account for njlispendens"
		driver.quit()
		return None
		pass
	else:
		return driver

def njlis_pic(num):
	foldername = COUNTY[num]['name'] + "_lisp"
	try:
	    os.makedirs('./' + COUNTY[num]['name'] + "_lisp")
	except OSError:
	    pass

	driver = njlis()
	if driver is None:
		pass
	else:

		print "#################Reading Data################"
		with open(COUNTY[num]['csv'], "rb") as csvfile:
			filereader = csv.reader(csvfile)
			data = list(filereader)

		for index, line in enumerate(data[1:], start=0):
			caseno = line[1]
			address = line[7].split('\n')[0]
			zip = line[7].split('\n')[-1:][0].split(' ')[-1:][0]
			if address is not "":
				try:
					street = address.split(' ')[0] + " " + address.split(' ')[1]
				except IndexError:
					street = address.split(' ')[0]

			street_input = driver.find_element_by_name("Address")
			zip_input = driver.find_element_by_name("Zip_Code")

			street_input.clear()
			zip_input.clear()

			street_input.send_keys(street)
			if zip.isdigit():
				print "Case: " + caseno + ": " + str(zip) + " + " + str(street)
				zip_input.send_keys(zip)
			else:
				print str(zip) + " + " + str(street)

			try:
				driver.find_element_by_name("submit").click()
				driver.get_screenshot_as_file(foldername + '/' + caseno + '.png');
				driver.back()
			except NoSuchElementException as e:
				driver.get_screenshot_as_file(foldername + '/' + caseno + '_ERROR.png');
				print "No Such Element Exception"
				driver.back()
				continue
		driver.quit()

