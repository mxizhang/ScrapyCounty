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

Run : 
scrapy crawl morris -o morris_items.csv
'''
from scrapy import Spider
from selenium import webdriver
from morris.items import MorrisItem
import time

DATE = "7/28/2016"

class MorrisSpider(Spider):
    name = "morris"
    allowed_domains = ["civilview.com"]
    start_urls = ["http://salesweb.civilview.com/Default.aspx"]
    #headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36"}

    def __init__(self):
    	#driver open
        self.driver = webdriver.PhantomJS()

    def parse(self, response):
        self.driver.get(response.url)
        #Find morris item [id = 00890]
        el = self.driver.find_element_by_xpath('//a[@href="Default.aspx?id=00890"]')
        el.click()
        time.sleep(1)
        
        results = self.driver.find_elements_by_xpath('//a[text()="Details"]')
        #print len(results)
        ###Uncomment above to print NO. for all properties in morris
        
        for i in range(2, len(results) + 1):
            result = self.driver.find_element_by_xpath("//table/tbody/tr[%s]/td[1]/a" % i)
            date = self.driver.find_element_by_xpath("//table/tbody/tr[%s]/td[3]" % i).text
            if date == DATE:
            	break;
            result.click()

            item = MorrisItem()
            item['sheriff_no'] = self.driver.find_element_by_xpath('//table[@id="grdSalesData"]/tbody/tr[1]/td[2]').text
            item['sale_date'] = self.driver.find_element_by_xpath('//table[@id="grdSalesData"]/tbody/tr[3]/td[2]').text
            item['case_no'] = self.driver.find_element_by_xpath('//table[@id="grdSalesData"]/tbody/tr[2]/td[2]').text
            item['address'] = self.driver.find_element_by_xpath('//table[@id="grdSalesData"]/tbody/tr[6]/td[2]').text
            item['upset'] = self.driver.find_element_by_xpath('//table[@id="grdSalesData"]/tbody/tr[8]/td[2]').text

            item['att'] = self.driver.find_element_by_xpath('//table[@id="grdSalesData"]/tbody/tr[9]/td[2]').text
            item['dfd'] = self.driver.find_element_by_xpath('//table[@id="grdSalesData"]/tbody/tr[5]/td[2]').text
            item['plf'] = self.driver.find_element_by_xpath('//table[@id="grdSalesData"]/tbody/tr[4]/td[2]').text

            item['schd_data'] = self.driver.find_element_by_xpath('//table[@id="grdStatusHistory"]/tbody/tr[2]/td[2]').text
            yield item
            self.driver.back()
        
        self.driver.close()
