import os
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "PostmanRuntime/7.42.0",
    "Accept": "*/*",
    "Postman-Token": "1b0977a9-3cb2-4695-83bf-5cfe4fe74e0f",
    "Host": "batdongsan.com.vn",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
    }

apiUrl = 'https://batdongsan.com.vn/nha-dat-ban-quan-1'
response = requests.get(apiUrl, headers=headers)

# print(response.content)

if (response.status_code == 200):
    document = response.text
    soup = BeautifulSoup(document, 'html.parser')
    print(soup.prettify())
else:
    print("Failed!")
