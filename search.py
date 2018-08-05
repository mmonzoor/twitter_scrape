import requests
from urllib import parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

url = "https://twitter.com/search-advanced/"
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(executable_path='/home/massi/chromedriver', chrome_options=chrome_options)
driver.get(url)
driver.get_screenshot_as_file('shot.png')


def search_values(**kwargs):
	fields = {
		"ands": None,
		"phrase": None,
		"ors": None,
		"nots": None,
		"tag": None,
		"ref": None,
		"geo": None,
		"since": None,
		"until": None
	}

	fields.update(kwargs)
	for key,value in kwargs.items():
		print("{} = {}".format(key,value))
		try:
			
			element = driver.find_element(By.XPATH, "//*[input/@name='{}']".format(key))
			element.send_keys(value)
		except TimeoutException:
			print("not loading in time!")

def submit_search(**kwargs):
		
	search_values(**kwargs)
	driver.get_screenshot_as_file('shot.png')
	driver.find_element(By.XPATH, "//button[@class='EdgeButton EdgeButton--primary submit']").click()
	driver.get_screenshot_as_file('shot1.png')
	driver.quit()

submit_search(tag="#gmo#chem", ref="kim")