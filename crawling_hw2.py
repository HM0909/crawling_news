from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  #크롬업데이트로 인해 추가
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import time
import csv

base_url = "https://www.hani.co.kr/" #한겨레 뉴스

driver = webdriver.Chrome(ChromeDriverManager().install()) #크롬업데이트로 인해 수정
driver.get(base_url)

html = driver.page_source
soup = bs(html, 'html.parser')

root = soup.find("div", {"class":"main-top01"})
items = root.find_all("div", {"class":"article-area"})

for item in items:
    data = item.find("h4", {"class":"article-title"}) 
    link = data.find("a")
    link_url = link.get('href')
    
    # print(base_url+ link_url)
    driver.get(base_url+ link_url)
    
    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')

    title = detail_soup.find("span", {"class" : "title"})
    wirtes = detail_soup.find("div", {"class" : "name"})

    print(title.text)
    print(wirtes.text[0:7])
    
    section = detail_soup.find("div" , {"class" : "article-text-font-size"}) 
    contents = section.find("div" , {"class" : "text"}) 
    # print(contents.text)
    full_content = ""  # 각 단락별 구분하기 쉽게 = 삽입하고 싶음

    for content in contents:
        full_content = full_content + content.text
    
        print(contents.text)
        print("")