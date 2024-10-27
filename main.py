import os;
import selenium.webdriver as webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from input import readCategoryUrl
from crawl import postCrawling

# https://tuoitre.vn/kinh-doanh.htm

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
edge_driver_path = os.path.join(os.getcwd(), 'msedgedriver.exe')

edge_service = Service(edge_driver_path)
edge_options = Options()
edge_options.add_argument(f'user-agent={user_agent}')
edge_options.add_experimental_option("detach", True)

url = readCategoryUrl("Input Category URL: ")
print(url)

browser = webdriver.Edge(service=edge_service, options=edge_options)
browser.get(url)

postCrawling(browser, 1)

# browser.close()