from selenium import webdriver
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import time
import csv

base_url = "https://www.mbn.co.kr/pages/news/index.html"

driver = webdriver.Chrome(executable_path='C:\hm_py\chromedriver')
driver.get(base_url)

html = driver.page_source
soup = bs(html, 'html.parser')

root = soup.find("div", {"class":"list_news"})
items = root.find_all("li")

for item in items:
#     # data = item.find("li") 
    link = item.find("a")
    # print(link.get('href'))
    link_url = "https:" + link.get('href')
    
    driver.get(link_url)

#     # detail_html = driver.page_source 
#     # detail_soup = bs(detail_html, 'html.parser')

#     # title = detail_soup.find("span", {"class" : "title"})
#     # wirtes = detail_soup.find("div", {"class" : "name"})

#     # print(title.text)
#     # print(wirtes.text[0:7])