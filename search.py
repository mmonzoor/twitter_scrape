import sys
import requests
from urllib import parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import argparse

url = "https://twitter.com/search-advanced/"
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(executable_path='/home/massi/chromedriver', chrome_options=chrome_options)
driver.get(url)
driver.get_screenshot_as_file('shot.png')


def search_values(dict_namespace):
	# fields = {
	# 	"ands": None,
	# 	"phrase": None,
	# 	"ors": None,
	# 	"nots": None,
	# 	"tag": None,
	# 	"ref": None,
	# 	"geo": None,
	# 	"since": None,
	# 	"until": None
	# }

	# fields.update(kwargs)
	for key,value in dict_namespace.items():
		if value != None:			
			print("{} = {}".format(key,value))
			element = driver.find_element(By.XPATH, "//*[input/@name='{}']".format(key))
			print(element)
			element.send_keys(value)

def submit_search(dict_namespace):
		
	search_values(dict_namespace)
	driver.get_screenshot_as_file('shot.png')
	driver.find_element(By.XPATH, "//button[@class='EdgeButton EdgeButton--primary submit']").click()
	driver.get_screenshot_as_file('shot1.png')
	driver.quit()
def main():
	q = argparse.ArgumentParser(description="processing parameters")
	q.add_argument('-a', '--ands', help='query words')
	q.add_argument('-p', '--phrase', help='exact phrase')
	q.add_argument('-o', '--ors', help='any of these words')
	q.add_argument('-n', '--nots', help='none of these words')
	q.add_argument('-t', '--tag', help='twitter tags')
	q.add_argument('-r', '--ref', help='from accounts')
	q.add_argument('-g', '--geo', help='near geographical location')
	q.add_argument('-ds', '--since', help='since this date')
	q.add_argument('-du', '--until', help='until this date')

	args = q.parse_args()

	if len(sys.argv) < 1:
		raise Exception("Need at least 1 parameter to be passed!")
	elif len(sys.argv) > 9:
		raise Exception("Too many arguments passed, please use -h to view available parameters")
	else:
		print( 'I am on the else statement!')
		print(vars(args))
		main_dict = vars(args)
		print(main_dict)
		search_values(main_dict)


if __name__ == '__main__':
	main()