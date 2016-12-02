# -*- coding: utf-8 -*-
# -*- author: mxiz -*-
'''
Before Start:
https://pip.pypa.io/en/stable/installing/
1. Scrapy [http://scrapy.org/]
	Install:  $ pip install scrapy
2. Selenium [https://pypi.python.org/pypi/selenium]
	Install: $ pip install selenium
3. PhantomJS
	Install: $ sudo pkg install phantomjs
    [Tip for Windows:
        Change the following code as:
        self.driver = webdriver.PhantomJS(executable_path=your_phantomJS_path)]
'''
from scrapy import Spider
from selenium import webdriver
from ScrapyCountyFlip.items import Item
import datetime

def next_weekday(d, weekday):  # 0 = Monday, 1=Tuesday, 2=Wednesday...
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

class MiddlesexSpider(Spider):
    name = "middlesex"
    allowed_domains = ["middlesexcountynj.gov"]
    start_urls = ["http://www.middlesexcountynj.gov/Government/Departments/PSH/Pages/Foreclosures.aspx"]

    def __init__(self):
    	self.driver = webdriver.PhantomJS(executable_path="C:/phantomjs-2.1.1-windows/bin/phantomjs.exe")

    def parse(self, response):
		self.driver.get(response.url)
		self.driver.get_screenshot_as_file('sc.png')
		while True:
			try:
				self.driver.find_element_by_xpath('//div[@class="mobile-only more"]/a').click()
			except:
				break

		#self.driver.get_screenshot_as_file('sc1.png')
		#self.driver.find_element_by_xpath('//div[@class="mobile-only more"]/a').click()
		#self.driver.get_screenshot_as_file('sc1.png')

		we = next_weekday(datetime.datetime.today(), 2)
		WE = "%02d/%02d/%02d" % (we.month, we.day, we.year)
		for i in range(1, 1000):
			try:
				date = self.driver.find_element_by_xpath('//table[1]/tbody/tr[%s]/td[3]' % i).text
				print date + ': ' + WE
				if date != WE:
					continue
				else:
					item = Item()
					item['sheriff_no'] = self.driver.find_element_by_xpath('//table[1]/tbody/tr[%s]/td[1]' % i).text
					item['sale_date'] = self.driver.find_element_by_xpath('//table[1]/tbody/tr[%s]/td[3]' % i).text
					item['case_no'] = self.driver.find_element_by_xpath('//table[1]/tbody/tr[%s]/td[2]' % i).text
					item['address'] = self.driver.find_element_by_xpath('//table[1]/tbody/tr[%s]/td[7]' % i).text
					item['upset'] = self.driver.find_element_by_xpath('//table[1]/tbody/tr[%s]/td[10]' % i).text

					item['att'] = self.driver.find_element_by_xpath('//table[1]/tbody/tr[%s]/td[5]' % i).text
					item['dfd'] = self.driver.find_element_by_xpath('//table[1]/tbody/tr[%s]/td[6]' % i).text
					item['plf'] = self.driver.find_element_by_xpath('//table[1]/tbody/tr[%s]/td[4]' % i).text

					#item['zipcode'] = self.driver.find_element_by_xpath('//table[1]/tbody/tr[%s]/td[9]' % i).text
					yield item
			except:
				break
		self.driver.close()
