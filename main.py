from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import *
import sqlite3 as db

class DataBase:
	conn = db.connect("water.db")
	cursor = conn.cursor()
	def __init__(self):
		pass

	def create(self):
		self.cursor.execute("create table if not exists water (name text PRIMARY KEY, qty text, brand text, price real, old_price real, unit_price real, multi_buy text, link text)")
		self.conn.commit()

	def insert(self, name, qty, brand, price, old_price, unit_price, multi_buy, link):
		param = (name, qty, brand, price, old_price, unit_price, multi_buy, link)
		self.cursor.execute('insert or replace into water values (?, ?, ?, ?, ?, ?, ?, ?)', param)
		self.conn.commit()
	
	def updateBrand(self, name, brand):
		self.cursor.execute('update water set brand = ? where name = ?', (brand, name))
		self.conn.commit()

	def updateMultiBuy(self, name, multi_buy):
		self.cursor.execute('update water set multi_buy = ? where name = ?', (multi_buy, name))
		self.conn.commit()

	def updateOldPrice(self, name, old):
		self.cursor.execute('update water set old_price = ? where name = ?', (old, name))
		self.conn.commit()


class WebCrawler:
	datab = DataBase()
	chrome_options = Options()
	# chrome_options.add_argument("--incognito")
	# chrome_options.add_argument("--window-size = 1920x1080")
	driver = webdriver.Chrome(chrome_options = chrome_options, executable_path = r'/usr/local/bin/chromedriver')

	url = "https://www.wholesaleclub.ca/search/1579471623493/page/~item/water/~selected/true/~sort/recommended/~filters/category:RCWC001006000000/category:RCWC001006008000"
	driver.get(url)
	time.sleep(2) 

	def __init__(self):
		#pass
		self.datab.create()

	def location(self):
		# province
		loc = self.driver.find_element_by_xpath('.//span[@class="select-wrapper"]/select[1]')
		loc.click()
		loc = self.driver.find_element_by_xpath('.//span[@class="select-wrapper"]/select[1]/option[8]')
		loc.click()
		loc.click()
		# city
		loc = self.driver.find_element_by_xpath('(.//span[@class="select-wrapper"])[2]/select[1]')
		loc.click()
		loc = self.driver.find_element_by_xpath('(.//span[@class="select-wrapper"])[2]/select[1]/option[19]')
		loc.click()
		loc.click()
		# store
		loc = self.driver.find_element_by_xpath('(.//span[@class="select-wrapper"])[3]/select[1]')
		loc.click()
		loc = self.driver.find_element_by_xpath('(.//span[@class="select-wrapper"])[3]/select[1]/option[2]')
		loc.click()
		loc.click()
		# click shop button
		loc = self.driver.find_element_by_xpath('.//span[@class="button-text"]')
		loc.click()

		time.sleep(2)

	def category(self): #called AISLE in website
		# loc = self.driver.find_element_by_css_selector('.panel-title.filter-title')
		# loc.click()

		# first AISLE
		loc = self.driver.find_element_by_xpath('.//button[@data-filter-name="Bottled Water"]')
		category = loc.text
		category = category[:category.index("(") - 1]
		loc.click()
		time.sleep(2)
		self.pageNum()
		self.fetchInfoWithCategory(category)
		
		#cancel filters
		loc = self.driver.find_element_by_xpath('.//button[@data-filter="category:RCWC001006008003"]')
		loc.click()
		time.sleep(2)

		loc = self.driver.find_element_by_css_selector('.panel-title.filter-title')
		loc.click()
		time.sleep(2)

		# second aisle
		loc = self.driver.find_element_by_xpath('.//button[@data-filter-name="Flavoured Water"]')
		category = loc.text
		category = category[:category.index("(") - 1]
		loc.click()
		time.sleep(2)
		self.pageNum()
		self.fetchInfoWithCategory(category)
		
		#cancel filters
		loc = self.driver.find_element_by_xpath('.//button[@data-filter="category:RCWC001006008002"]')
		loc.click()
		time.sleep(2)

		loc = self.driver.find_element_by_css_selector('.panel-title.filter-title')
		loc.click()
		time.sleep(2)

		# third aisle
		loc = self.driver.find_element_by_xpath('.//button[@data-filter-name="Sparkling Water"]')
		category = loc.text
		category = category[:category.index("(") - 1]
		loc.click()
		time.sleep(2)
		self.pageNum()
		self.fetchInfoWithCategory(category)
		
		#cancel filters
		loc = self.driver.find_element_by_xpath('.//button[@data-filter="category:RCWC001006008001"]')
		loc.click()
		time.sleep(2)

		loc = self.driver.find_element_by_css_selector('.panel-title.filter-title')
		loc.click()
		time.sleep(2)

		#fourth aisle
		loc = self.driver.find_element_by_xpath('.//button[@data-filter-name="Tonic Water"]')
		category = loc.text
		category = category[:category.index("(") - 1]
		loc.click()
		time.sleep(2)
		self.pageNum()
		self.fetchInfoWithCategory(category)
		
		#cancel filters
		loc = self.driver.find_element_by_xpath('.//button[@data-filter="category:RCWC001006008004"]')
		loc.click()
		time.sleep(2)
		
		# check promotion info
		self.promotion()

		#check brand info
		self.brand()


	def brand(self):
		loc = self.driver.find_element_by_xpath('.//h5[@data-target=".productBrand-filters"]')
		loc.click()

		for i in range(26): # 26 brands
			#if i != 11 and i != 17 and i != 22 and i != 23 and i != 24 and i != 25:
			time.sleep(2)
			brand = self.driver.find_element_by_xpath('.//label[@for="productBrand{}"]'.format(i+1))
			brand_text = brand.text
			brand.click()
			time.sleep(2)
			self.pageNum()
			self.fetchInfoWithBrand(brand_text)
			time.sleep(2)
			try:	
				brand = self.driver.find_element_by_xpath('.//label[@for="productBrand1"]')
				time.sleep(2)
				#webdriver.ActionChains(driver).move_to_element(brand).click(brand).perform()
				brand.click()
				time.sleep(2)
			except:
				print(i+1)
				print(brand_text)
				loc = self.driver.find_elements_by_xpath('.//div[@class="product-info"]')
		
				self.driver.get(self.url)
				time.sleep(2)
				loc = self.driver.find_element_by_xpath('.//h5[@data-target=".productBrand-filters"]')
				loc.click()

		self.datab.conn.close()

	def promotion(self):
		loc = self.driver.find_element_by_xpath('.//h5[@data-target=".promotions-filters"]')
		loc.click()
		loc = self.driver.find_element_by_xpath('.//label[@for="promotions1"]')
		promo = loc.text
		print(promo)
		loc.click()
		time.sleep(2)
		self.pageNum()
		self.fetchInfoWithMultiBuy(promo)
		#cancel then choose another promo filter
		loc = self.driver.find_element_by_xpath('.//label[@for="promotions1"]')
		loc.click()
		time.sleep(2)

		# another promotion type
		loc = self.driver.find_element_by_xpath('.//label[@for="promotions2"]')
		promo = loc.text
		print(promo)
		loc.click()
		time.sleep(2)
		self.pageNum()
		self.fetchInfoWithSale(promo)
		#cancel then choose another promo filter
		loc = self.driver.find_element_by_xpath('.//label[@for="promotions1"]')
		loc.click()
		time.sleep(2)

		#close filter section
		loc = self.driver.find_element_by_xpath('.//h5[@data-target=".promotions-filters"]')
		loc.click()

	
	def pageNum(self):
		# find once load how many items
		loc = self.driver.find_element_by_xpath('.//span[@class="range"]')
		hyphen = loc.text.find("-") + 1
		once_load = int(loc.text[hyphen:])
		# find total results
		loc = self.driver.find_element_by_xpath('.//span[@class="result-total"]')
		total = int(loc.text)

		# click "load more" until showed all
		if total > once_load:
			for i in range(total//once_load):
				self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				loc = self.driver.find_element_by_xpath('.//button[@class="btn-inline-link btn-show-more"]')
				loc.click()
				time.sleep(2)
	
	def fetchInfo(self):
		# finding all the products' info
		loc = self.driver.find_elements_by_xpath('.//div[@class="product-info"]')

		for p in loc:
			title_sec = p.find_element_by_xpath('.//div[@class="product-name-wrapper"]/a[1]')
			name = title_sec.text
			print(name)

			#links
			print(title_sec.get_attribute('href'))
			reg_price = p.find_element_by_xpath('.//span[@class="reg-price-text"]').text
			print(reg_price)
			try:
				old_price = p.find_element_by_xpath('.//span[@class="old-price-text"]').text
			except NoSuchElementException:
				print("No old price")

			#reg_qty = unit price
			qty = p.find_element_by_xpath('.//div[@class="qty"]/span[1]').text
			price_per_100ml = qty[(qty.index("$") + 1) : (qty.index("/") - 1)]
			print(price_per_100ml)

	def fetchInfoWithBrand(self, brand):
		# finding all the products' info
		loc = self.driver.find_elements_by_xpath('.//div[@class="product-info"]')

		for p in loc:
			title_sec = p.find_element_by_xpath('.//div[@class="product-name-wrapper"]/a[1]')
			name = title_sec.text
			print(name)
			print(brand)
			self.datab.updateBrand(name, brand)

	def fetchInfoWithMultiBuy(self, promo):
		loc = self.driver.find_elements_by_xpath('.//div[@class="product-page-hotspot"]')
		for p in loc:
			title_sec = p.find_element_by_xpath('.//div[@class="product-name-wrapper"]/a[1]')
			name = title_sec.text
			print(name)
			deal = p.find_element_by_xpath('.//span[@class="deal-type"]').text
			print(deal)
			self.datab.updateMultiBuy(name, deal)

	def fetchInfoWithSale(self, promo):
		loc = self.driver.find_elements_by_xpath('.//div[@class="product-info"]')

		for p in loc:
			title_sec = p.find_element_by_xpath('.//div[@class="product-name-wrapper"]/a[1]')
			name = title_sec.text
			print(name)

			reg_price = p.find_element_by_xpath('.//span[@class="reg-price-text"]').text
			print(reg_price)
			old_price = p.find_element_by_xpath('.//span[@class="old-price-text"]').text
			print(old_price)
			self.datab.updateOldPrice(name, old_price)


	def fetchInfoWithCategory(self, category):
		# finding all the products' info
		loc = self.driver.find_elements_by_xpath('.//div[@class="product-info"]')

		for p in loc:
			title_sec = p.find_element_by_xpath('.//div[@class="product-name-wrapper"]/a[1]')
			name = title_sec.text
			print(name)

			#links
			link = title_sec.get_attribute('href')
			reg_price = p.find_element_by_xpath('.//span[@class="reg-price-text"]').text
			print(reg_price)
			try:
				old_price = p.find_element_by_xpath('.//span[@class="old-price-text"]').text
			except NoSuchElementException:
				print("No old price")

			#reg_qty = unit price
			qty = p.find_element_by_xpath('.//div[@class="qty"]/span[1]').text
			price_per_100ml = qty[(qty.index("$") + 1) : (qty.index("/") - 1)]
			print(price_per_100ml)

			print(category)

			try:
				qty = name[(name.rindex("(") + 1) : (name.rindex(")"))]
			except:
				if name == "Evian  Spring Water, Natural":
					qty = "6x330mL"
				else:
					qty = None

			self.datab.insert(name, qty , None, reg_price, None, price_per_100ml, None, link)
			


water = WebCrawler()
water.location()
water.category()

#conn.commit()
#conn.close()

