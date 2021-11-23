from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  #크롬업데이트로 인해 추가
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import time
import csv

base_url = "https://www.khan.co.kr/" # 경향신문 뉴스

driver = webdriver.Chrome(ChromeDriverManager().install()) #크롬업데이트로 인해 수정
driver.get(base_url)

html = driver.page_source
soup = bs(html, 'html.parser')

root = soup.find("ul", {"class":"sub-news-wrap scroll_start02_in"})
items = root.find_all("li")

for item in items:
    data = item.find("dt")
    link = item.find("a")
    link_url = link.get('href')
    
    driver.get(link_url)
        
    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')

    title = detail_soup.find("h1", {"class":"headline"})
    wirtes = detail_soup.find("span", {"class":"author"})

    print(title.text)
    print(wirtes.text)
    
    section = detail_soup.find("div" , {"class" : "art_body"}) 
    contents = detail_soup.find("p" , {"class" : "content_text"}) #본문 단락이 해당 태그로 되어 있어서 다 뽑아내고 싶음
    print(contents.text) 
    # full_content = ""
    
    # for content in contents:
    #     full_content = full_content + contents.text
    
    #     print(content.text)
    #     print("")