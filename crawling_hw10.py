from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  #크롬업데이트로 인해 추가
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import time
import csv

base_url = "http://www.kmib.co.kr/news/index.asp" # 국민일보 뉴스

driver = webdriver.Chrome(ChromeDriverManager().install()) #크롬업데이트로 인해 수정
driver.get(base_url)

html = driver.page_source
soup = bs(html, 'html.parser')

root = soup.find("div", {"class":"con"})
items = root.find("dl")

for item in root:
    data = item.find("dd", {"class":"rel_lst"}) #
    link = item.find("a")
    link_url = link.get('href')
    
    driver.get(link_url) # 왜 안 넘어가지!!!!