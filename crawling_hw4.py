from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  #크롬업데이트로 인해 추가
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import time
import csv

base_url = "https://www.hankyung.com/" #한국경제 뉴스

driver = webdriver.Chrome(ChromeDriverManager().install()) #크롬업데이트로 인해 수정
driver.get(base_url)

html = driver.page_source
soup = bs(html, 'html.parser')

root = soup.find("div", {"class":"main-top-major"})
items = root.find_all("li")

for item in items:
    # data = item.find("h2", {"class":"news-tit"}) 
    link = item.find("a")
    link_url = link.get('href')
    
    driver.get(link_url)

    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')

    title = detail_soup.find("h1", {"class" : "title"})
    wirtes = detail_soup.find("div", {"class" : "author"})

    print(title.text)
    print(wirtes.text.strip()) # 기자 두명 붙일 수 있나?
    
    section = detail_soup.find("div" , {"class" : "articlebody ga-view"})
    # contents_head = section.find("div" , {"class" : "summary editoropinions"})
    # contents_main = section.find("p" , {"class" : "txt"}) 
    # full_content = ""
    print(section.text)