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
Run : 
scrapy crawl morris -o morris_items.csv
'''
import scrapy
from scrapy import Spider
from selenium import webdriver
from morris.items import EssexItem
import time


class EssexSpider(Spider):
    name = "essex"
    allowed_domains = ["civilview.com"]
    start_urls = ["http://salesweb.civilview.com/Default.aspx"]

    def __init__(self):
    	self.driver = webdriver.PhantomJS()

    def parse(self, response):
        self.driver.get(response.url)
        el = self.driver.find_element_by_xpath('//a[@href="Default.aspx?id=00860"]')
        el.click()
        time.sleep(1)
        
        results = self.driver.find_elements_by_xpath('//a[text()="Details"]')
        #print len(results)
        
        for i in range(2, len(results) + 1):
            result = self.driver.find_element_by_xpath("//table/tbody/tr[%s]/td[1]/a" % i)
            result.click()

            item = EssexItem()
            item['sheriff_no'] = self.driver.find_element_by_xpath('//table[@id="grdSalesData"]/tbody/tr[1]/td[2]').text
            item['sale_date'] = self.driver.find_element_by_xpath('//table[@id="grdSalesData"]/tbody/tr[3]/td[2]').text
            item['case_no'] = self.driver.find_element_by_xpath('//table[@id="grdSalesData"]/tbody/tr[2]/td[2]').text
            item['address'] = self.driver.find_element_by_xpath('//table[@id="grdSalesData"]/tbody/tr[6]/td[2]').text
            item['upset'] = self.driver.find_element_by_xpath('//table[@id="grdSalesData"]/tbody/tr[8]/td[2]').text

            item['att'] = self.driver.find_element_by_xpath('//table[@id="grdSalesData"]/tbody/tr[9]/td[2]').text
            item['att_ph'] = self.driver.find_element_by_xpath('//table[@id="grdSalesData"]/tbody/tr[10]/td[2]').text
            item['dfd'] = self.driver.find_element_by_xpath('//table[@id="grdSalesData"]/tbody/tr[5]/td[2]').text
            item['plf'] = self.driver.find_element_by_xpath('//table[@id="grdSalesData"]/tbody/tr[4]/td[2]').text

            item['schd_data'] = self.driver.find_element_by_xpath('//table[@id="grdStatusHistory"]/tbody/tr[2]/td[2]').text
            yield item
            self.driver.back()
            #time.sleep(0.5)
            ###Uncomment above if loading error happens
        
        self.driver.close()
