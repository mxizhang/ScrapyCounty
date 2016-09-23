# -*- coding: utf-8 -*-
# -*- author: mxiz -*-
'''
Python 2.7
Before Start:
1. Scrapy [http://scrapy.org/]
    Install:  $ pip install scrapy
2. Selenium [https://pypi.python.org/pypi/selenium]
    Install: $ pip install selenium
3. PhantomJS
    Install: $ sudo pkg install phantomjs
    [Tip for Windows:
        Change the following code as:
        self.driver = webdriver.PhantomJS(executable_path=your_phantomJS_path)]
Run : 
scrapy crawl bergen -o bergen_items.csv
'''
from scrapy import Spider
from selenium import webdriver
from morris.items import BergenItem
import time

DATE = []

class BergenSpider(Spider):
    name = "bergen"
    allowed_domains = ["civilview.com"]
    start_urls = ["http://salesweb.civilview.com/"]

    def __init__(self):
    	self.driver = webdriver.PhantomJS(executable_path="C:/phantomjs-2.1.1-windows/bin/phantomjs.exe")

    def parse(self, response):
        self.driver.get(response.url)
        el = self.driver.find_element_by_xpath('//a[@href="/Sales/SalesSearch?countyId=9"]')
        el.click()
        time.sleep(1)
        
        #results = self.driver.find_elements_by_xpath('//a[text()="Details"]')
        #print len(results)
        i = 1
        while len(DATE) < 2:
            result = self.driver.find_element_by_xpath("//table/tbody/tr[%s]/td[1]/a" % i)
            date = self.driver.find_element_by_xpath("//table/tbody/tr[%s]/td[3]" % i).text
            if date not in DATE:
                DATE.append(date)
            result.click()

            item = BergenItem()
            xpath = '//table[1]/tbody/'
            item['sheriff_no'] = self.driver.find_element_by_xpath(xpath + 'tr[1]/td[2]').text
            item['sale_date'] = self.driver.find_element_by_xpath(xpath + 'tr[3]/td[2]').text
            item['case_no'] = self.driver.find_element_by_xpath(xpath + 'tr[2]/td[2]').text
            item['address'] = self.driver.find_element_by_xpath(xpath + 'tr[6]/td[2]').text
            item['upset'] = self.driver.find_element_by_xpath(xpath + 'tr[8]/td[2]').text
            item['att'] = self.driver.find_element_by_xpath(xpath + 'tr[9]/td[2]').text
            item['dfd'] = self.driver.find_element_by_xpath(xpath + 'tr[5]/td[2]').text
            item['plf'] = self.driver.find_element_by_xpath(xpath + 'tr[4]/td[2]').text
            item['schd_data'] = self.driver.find_element_by_xpath('//table[2]/tbody/tr[1]/td[2]').text
            yield item
            self.driver.back()
            i = i + 1
            #time.sleep(0.5)
            ###Uncomment above if loading error happens
        print DATE
        self.driver.close()