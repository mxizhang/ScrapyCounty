# -*- coding: utf-8 -*-
# -*- author: mxiz -*-
'''
Python 2.7
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

Run example
scrapy crawl morris -o morris_items.csv
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


class EssexSpider(Spider):
    name = "essex"
    allowed_domains = ["civilview.com"]
    start_urls = ["http://salesweb.civilview.com/"]

    def __init__(self):
        '''
        !!! FOR WINDOWS USER
        '''
        #self.driver = webdriver.PhantomJS(executable_path="c:/phantomjs-2.1.1-windows/bin/phantomjs.exe")
        self.driver = webdriver.PhantomJS(executable_path="C:/phantomjs-2.1.1-windows/bin/phantomjs.exe")

    def parse(self, response):
        self.driver.get(response.url)
        el = self.driver.find_element_by_xpath('//a[@href="/Sales/SalesSearch?countyId=2"]')
        el.click()

        tu = next_weekday(datetime.datetime.today(), 1)
        TU = "%s/%s/%s" % (tu.month, tu.day, tu.year)

        for i in range(1, 1300):
            result = self.driver.find_element_by_xpath("//table/tbody/tr[%s]/td[1]/a" % i)
            date = self.driver.find_element_by_xpath("//table/tbody/tr[%s]/td[3]" % i).text
            if date != TU:
                continue
            else:
                result.click()
                item = Item()
                item['sheriff_no'] = self.driver.find_element_by_xpath(
                    '//table[1]/tbody/tr[1]/td[2]').text
                item['sale_date'] = self.driver.find_element_by_xpath(
                    '//table[1]/tbody/tr[3]/td[2]').text
                item['case_no'] = self.driver.find_element_by_xpath(
                    '//table[1]/tbody/tr[2]/td[2]').text
                item['address'] = self.driver.find_element_by_xpath(
                    '//table[1]/tbody/tr[6]/td[2]').text
                item['upset'] = self.driver.find_element_by_xpath(
                    '//table[1]/tbody/tr[8]/td[2]').text

                item['att'] = self.driver.find_element_by_xpath(
                    '//table[1]/tbody/tr[9]/td[2]').text
                item['att_ph'] = self.driver.find_element_by_xpath(
                    '//table[1]/tbody/tr[10]/td[2]').text
                item['dfd'] = self.driver.find_element_by_xpath(
                    '//table[1]/tbody/tr[5]/td[2]').text
                item['plf'] = self.driver.find_element_by_xpath(
                    '//table[1]/tbody/tr[4]/td[2]').text

                item['schd_data'] = self.driver.find_element_by_xpath(
                    '//table[2]/tbody/tr[1]/td[2]').text

                yield item
                self.driver.back()

        self.driver.close()