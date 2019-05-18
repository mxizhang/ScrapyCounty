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
from HF_ScrapyCounty.items import Item
from datetime import datetime, timedelta
import time


def next_weekday(d, weekday):  # 0 = Monday, 1=Tuesday, 2=Wednesday...
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


class MorrisSpider(Spider):
    name = "morris"
    allowed_domains = ["civilview.com"]
    start_urls = ["http://salesweb.civilview.com/"]

    def __init__(self):
        '''
        !!! FOR WINDOWS USER
        '''
        #self.driver = webdriver.PhantomJS(executable_path="c:/phantomjs-2.1.1-windows/bin/phantomjs.exe")
        self.driver = webdriver.PhantomJS()

    def parse(self, response):
        self.driver.get(response.url)
        el = self.driver.find_element_by_xpath('//a[@href="/Sales/SalesSearch?countyId=9"]')
        el.click()

        now = datetime.now()
        #n = "%s/%s/%s" % (now.month, now.day, now.year)
        #N = time.strptime(n, "%m/%d/%Y")
        std = now + timedelta(days=180)
        STD = "%s/%s/%s" % (std.month, std.day, std.year)
        #std = time.strptime(STD, "%m/%d/%Y")
        '''
        th = next_weekday(datetime.datetime.today(), 3)
        TH = "%s/%s/%s" % (th.month, th.day, th.year)
        '''
        for i in range(1, 500):
            result = self.driver.find_element_by_xpath("//table/tbody/tr[%s]/td[1]/a" % i)
            date = self.driver.find_element_by_xpath("//table/tbody/tr[%s]/td[3]" % i).text

            if date > STD:
                break
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
                upset = self.driver.find_element_by_xpath(
                    '//table[1]/tbody/tr[8]/td[2]').text

                item['att'] = self.driver.find_element_by_xpath(
                    '//table[1]/tbody/tr[9]/td[2]').text
                item['dfd'] = self.driver.find_element_by_xpath(
                    '//table[1]/tbody/tr[5]/td[2]').text
                item['plf'] = self.driver.find_element_by_xpath(
                    '//table[1]/tbody/tr[4]/td[2]').text

                item['schd_data'] = self.driver.find_element_by_xpath(
                    '//table[2]/tbody/tr[1]/td[2]').text

                if float(upset.split("$")[-1].replace(',', '')) <= 150000:
                    item['upset'] = upset
                    #print "!!"+upset
                    yield item
                self.driver.back()

        self.driver.close()
