from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  #크롬업데이트로 인해 추가
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import time
import csv

base_url = "https://www.mbn.co.kr/pages/news/index.html" # MBN 뉴스

driver = webdriver.Chrome(ChromeDriverManager().install()) #크롬업데이트로 인해 수정
driver.get(base_url)

html = driver.page_source
soup = bs(html, 'html.parser')

root = soup.find("div", {"class":"list_news"})
items = root.find_all("li")

for item in items:
    # data = item.find("li") 
    link = item.find("a")
    # print(link.get('href'))
    link_url = "https:" + link.get('href')
    
    driver.get(link_url)

    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')

    title = detail_soup.find("div", {"class" : "box01"}) #<h1> 만 뽑기 어려움 
    # wirtes = detail_soup.find("div", {"class" : "name"}) #기자가 택스트 내에 들어가 있어서 영역을 어떻게 잡아야 할지 모르겠음

    print(title.text)
    # print(wirtes.text)
    
    contents = detail_soup.find("div" , {"class" : "detail"}) 
    print(contents.text)
