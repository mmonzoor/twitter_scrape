import argparse
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from urllib import parse
import requests
import time
import sys
print(sys.version)

base_url = "https://twitter.com/search?l=&"
# src=typd means it was typed in and can be incorrect whereas the sprv means that no this is what I want
# p = parse.parse_qs(r'"https://twitter.com/search?l=&q=%23chem%20near%3A%22Toronto%2C%20Ontario%22%20within%3A15mi&src=sprv"')
# print(p)
# print(type(p))

# u = parse.urlencode(p, doseq=True)
# print(u)


def search_values(dict_namespace):
	# add ref casee here,

    query = []
    for key, value in dict_namespace.items():

        if value != None and key == 'ands':
            item = '{}'.format(value)
        elif value != None and key == 'nots':
            item = "-"+"{}".format(value)
        elif value != None and key == 'tag':
            item = "#"+"{}".format(value)
        elif value != None and key == 'phrase':
            item = "{}".format(value)
        elif value != None and key == 'ors':
            item = value.replace(' ', ' OR ')
        elif value != None and key == 'since':
            item = '{}:{}'.format(key, value)
        elif value != None and key == 'until':
            item = '{}:{}'.format(key, value)
        elif value != None and key == 'geo':
            item = 'near:'+"{}".format(value)
        else:
        	continue
        query.append(item)

        print(query)

    query_string = " ".join(query)
    print(query_string)

    fields = {'q': [query_string], 'src': 'sprv'}
    print(fields)
    return fields


def submit_search(dict_namespace):

	fields = search_values(dict_namespace)
	web_query = base_url + parse.urlencode(fields, doseq=True)
	print(web_query)

	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--window-size=1920,1080")
	driver = webdriver.Chrome(
	    executable_path='/usr/bin/chromedriver', chrome_options=chrome_options)
	driver.get(web_query)
	driver.get_screenshot_as_file('shot.png')
	driver.find_element_by_xpath("//*['tweet js-stream-tweet']")
	for i in range(1, 50):
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		#time.sleep()
	html_source = driver.page_source
	#print(html_source)
	data = html_source.encode('utf-8')
	print(data)
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
        raise Exception(
            "Too many arguments passed, please use -h to view available parameters")
    else:
        print('I am on the else statement!')
        print(vars(args))
        main_dict = vars(args)
        print(main_dict)
        submit_search(main_dict)


if __name__ == '__main__':
    main()
