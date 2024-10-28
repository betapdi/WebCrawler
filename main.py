import os;
import selenium.webdriver as webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from input import readCategoryUrl, readNumberofPost
from crawl import postCrawling
import time

# https://tuoitre.vn/kinh-doanh.htm
# https://tuoitre.vn/the-gioi.htm
# https://tuoitre.vn/giao-duc.htm
# https://tuoitre.vn/chu-doanh-nghiep-lap-bat-chong-nang-noi-gi-ve-viec-hieu-truong-ke-khai-gia-bat-gap-3-lan-20241025142325469.htm

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
edge_driver_path = os.path.join(os.getcwd(), 'msedgedriver.exe')

edge_service = Service(edge_driver_path)
edge_options = Options()
edge_options.add_argument(f'user-agent={user_agent}')
edge_options.add_experimental_option("detach", True)

url1 = readCategoryUrl("Input Category URL 1: ")
url2 = readCategoryUrl("Input Category URL 2: ")
url3 = readCategoryUrl("Input Category URL 3: ")
num = readNumberofPost("Input number of posts you want to crawl in each category: ")
# print(url, num)

browser = webdriver.Edge(service=edge_service, options=edge_options)
browser.get(url1)
browser.maximize_window()
time.sleep(2)

postCrawling(browser, num)

browser.get(url2)
postCrawling(browser, num)

browser.get(url3)
postCrawling(browser, num)

browser.close()