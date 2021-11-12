from selenium import webdriver
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import time
import csv

base_url = "https://news.jtbc.joins.com/section/list.aspx?scode="

driver = webdriver.Chrome(executable_path='C:\hm_py\chromedriver')
driver.get(base_url)

html = driver.page_source
soup = bs(html, 'html.parser')

root = soup.find("div", {"class":"news_area bd"})
items = root.find_all("li")

for item in items:
    data = item.find("dt", {"class":"title_cr"}) 
    link = data.find("a")
    link_url = link.get('href')
    
    driver.get("https://news.jtbc.joins.com" + link_url)
    # https://news.jtbc.joins.com/html/619/NB12030619.html