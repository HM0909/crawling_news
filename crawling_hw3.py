from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  #크롬업데이트로 인해 추가
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import time
import csv

base_url = "https://news.jtbc.joins.com/section/list.aspx?scode=" #JTBC 뉴스

driver = webdriver.Chrome(ChromeDriverManager().install()) #크롬업데이트로 인해 수정
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

    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')

    title = detail_soup.find("div", {"class" : "title"})
    wirtes = detail_soup.find("dd", {"class" : "name"})

    print(title.text)
    print(wirtes.text)