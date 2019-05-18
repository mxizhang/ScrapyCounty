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
from HF_ScrapyCounty.items import Item
import datetime

def next_weekday(d, weekday):  # 0 = Monday, 1=Tuesday, 2=Wednesday...
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def init_phantomjs_driver(*args, **kwargs):

    headers = { 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Connection': 'keep-alive'
    }

    for key, value in headers.iteritems():
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value

    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'

    driver =  webdriver.PhantomJS(*args, **kwargs)
    driver.set_window_size(1600, 1200)

    return driver

class MiddlesexSpider(Spider):
    name = "middlesex"
    allowed_domains = ["middlesexcountynj.gov"]
    start_urls = ["http://www.middlesexcountynj.gov/Government/Departments/PSH/Pages/Foreclosures.aspx"]

    def __init__(self):
    	self.driver = init_phantomjs_driver()

    def parse(self, response):
		count = 1
		self.driver.get(response.url)
		self.driver.get_screenshot_as_file('sc.png')
		ul = self.driver.find_elements_by_xpath('//*[@id="SheriffForclosuresWP"]/div/div[1]/div/ul/li')
		for each in ul:
			count = count + 1
		#self.driver.get_screenshot_as_file('sc1.png')
		#self.driver.find_element_by_xpath('//div[@class="mobile-only more"]/a').click()
		#self.driver.get_screenshot_as_file('sc1.png')
		#print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" + str(count)
		we = next_weekday(datetime.datetime.today(), 2)
		WE = "%02d/%02d/%02d" % (we.month, we.day, we.year)
		for j in range(2, count+1):
			for i in range(1, 41):
				try:
					date = self.driver.find_element_by_xpath('//*[@id="SheriffForclosuresWP"]/div/table/tbody/tr[%s]/td[3]' % i).text
					print date + ': ' + WE
					
					if date != WE:
						continue
					else:
						item = Item()
						item['sheriff_no'] = self.driver.find_element_by_xpath('//*[@id="SheriffForclosuresWP"]/div/table/tbody/tr[%s]/td[1]' % i).text
						item['sale_date'] = self.driver.find_element_by_xpath('//*[@id="SheriffForclosuresWP"]/div/table/tbody/tr[%s]/td[3]' % i).text
						item['case_no'] = self.driver.find_element_by_xpath('//*[@id="SheriffForclosuresWP"]/div/table/tbody/tr[%s]/td[2]' % i).text
						item['address'] = self.driver.find_element_by_xpath('//*[@id="SheriffForclosuresWP"]/div/table/tbody/tr[%s]/td[7]/a' % i).text
						item['upset'] = self.driver.find_element_by_xpath('//*[@id="SheriffForclosuresWP"]/div/table/tbody/tr[%s]/td[10]' % i).text
						item['att'] = self.driver.find_element_by_xpath('//*[@id="SheriffForclosuresWP"]/div/table/tbody/tr[%s]/td[5]' % i).text
						item['dfd'] = self.driver.find_element_by_xpath('//*[@id="SheriffForclosuresWP"]/div/table/tbody/tr[%s]/td[6]' % i).text
						item['plf'] = self.driver.find_element_by_xpath('//*[@id="SheriffForclosuresWP"]/div/table/tbody/tr[%s]/td[4]' % i).text
						#item['zipcode'] = self.driver.find_element_by_xpath('//table[1]/tbody/tr[%s]/td[9]' % i).text
						yield item
				except:
					break
			self.driver.find_element_by_xpath('//*[@id="SheriffForclosuresWP"]/div/div[1]/div/ul/li[%s]/a' % j).click()
		self.driver.close()
