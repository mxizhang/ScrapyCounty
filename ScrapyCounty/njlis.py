# -*- coding: utf-8 -*-
# -*- author: mxiz -*-
import csv
import os
import zillow_functions
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

def njlis():
	driver = webdriver.PhantomJS(executable_path="C:/Users/flipp/phantomjs-2.1.1-windows/bin/phantomjs.exe")
	driver.get("https://njlispendens.com/properties")

	print "#################Logging In################"
	user = driver.find_element_by_name("amember_login")
	user.send_keys("Flipping_gr0up")
	pasw = driver.find_element_by_name("amember_pass")
	pasw.send_keys("Flipping_gr0up")

	driver.find_element_by_xpath("/html/body/table/tbody/tr[3]/td[2]/form[1]/table/tbody/tr[4]/td/input").click()

	print driver.title
	return driver


def essex_lis(foldername):
	try:
	    os.makedirs('./' + foldername)
	except OSError:
	    pass

	driver = njlis()

	print "#################Reading Data################"
	with open("essex_items.csv","rb") as csvfile:
		filereader = csv.reader(csvfile)
		data = list(filereader)

	for index, line in enumerate(data[1:], start=0):
		caseno = line[4]
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

def mercer_lis(foldername):
	try:
	    os.makedirs('./' + foldername)
	except OSError:
	    pass

	driver = njlis()
	
	print "#################Reading Data################"
	with open("mercer_items.csv","rb") as csvfile:
		filereader = csv.reader(csvfile)
		data = list(filereader)

	for index, line in enumerate(data[1:], start=0):
		caseno = line[2]
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
			print "NO: " + str(zip) + " + " + str(street)
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

def morris_lis(foldername):
	try:
	    os.makedirs('./' + foldername)
	except OSError:
	    pass

	driver = njlis()
	
	print "#################Reading Data################"
	with open("morris_items.csv","rb") as csvfile:
		filereader = csv.reader(csvfile)
		data = list(filereader)

	for index, line in enumerate(data[1:], start=0):
		caseno = line[3]
		address = line[6].split('\n')[0]
		zip = line[6].split('\n')[-1:][0].split(' ')[-1:][0]
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
			print "NO: " + str(zip) + " + " + str(street)
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

def bergen_lis(foldername):
	try:
	    os.makedirs('./' + foldername)
	except OSError:
	    pass

	driver = njlis()
	
	print "#################Reading Data################"
	with open("bergen_items.csv","rb") as csvfile:
		filereader = csv.reader(csvfile)
		data = list(filereader)

	for index, line in enumerate(data[1:], start=0):
		caseno = line[3]
		address = line[6].split('\n')[0]
		zip = line[6].split('\n')[-1:][0].split(' ')[-1:][0]
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
			print "NO: " + str(zip) + " + " + str(street)
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

def hunterdon_lis(foldername):
	try:
	    os.makedirs('./' + foldername)
	except OSError:
	    pass

	driver = njlis()
	
	print "#################Reading Data################"
	with open("data-sale-bakerrec-.csv","rb") as csvfile:
		filereader = csv.reader(csvfile)
		data = list(filereader)

	for index, line in enumerate(data[1:], start=0): 
		#print line
		if line[0] is not "":
			try:
				caseno = str(int(round(float(line[0]))))
				address = line[55]
				city = line[62]
				town = " ".join(city.split()[2:])
				zillow = zillow_functions.findzillow(address, town)
				zip = zillow[3]
				#print zip + "zip + " + address
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
					print "NO: " + str(zip) + " + " + str(street)
					zip_input.send_keys(zip)
				else:
					print str(zip) + " + " + str(street)

				driver.find_element_by_name("submit").click()

				driver.get_screenshot_as_file(foldername + '/' + caseno + '.png');
				driver.back()
			except ValueError:
				break
	driver.quit()


def middlesex_lis(foldername):
	try:
	    os.makedirs('./' + foldername)
	except OSError:
	    pass

	driver = njlis()
	
	print "#################Reading Data################"
	with open("middlesex_items.csv","rb") as csvfile:
		filereader = csv.reader(csvfile)
		data = list(filereader)

	for index, line in enumerate(data[1:], start=0):
		caseno = line[3]
		address = line[7].split('\n')[0]
		zip = line[7].split('\n')[-1:][0].split(' ')[-1:][0]
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


def union_lis(foldername):
	try:
	    os.makedirs('./' + foldername)
	except OSError:
	    pass

	driver = njlis()
	
	print "#################Reading Data################"
	with open("union_items.csv","rb") as csvfile:
		filereader = csv.reader(csvfile)
		data = list(filereader)

	for index, line in enumerate(data[1:], start=0):
		caseno = line[3]
		address = line[6].split('\n')[0]
		zip = line[6].split('\n')[-1:][0].split(' ')[-1:][0]
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
			print "NO: " + str(zip) + " + " + str(street)
			zip_input.send_keys(zip)
		else:
			print str(zip) + " + " + str(street)

		#time.sleep(0.5)
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
