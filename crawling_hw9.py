from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  #크롬업데이트로 인해 추가
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import time
import csv

base_url = "https://www.chosun.com/" # 조선일보 뉴스

driver = webdriver.Chrome(ChromeDriverManager().install()) #크롬업데이트로 인해 수정
driver.get(base_url)

html = driver.page_source
soup = bs(html, 'html.parser')

root = soup.find("div", {"class":"flex-chain__column flex-chain__column-1 | box--bg-undefined grid__col--sm-8 grid__col--md-8 grid__col--lg-8 box--margin-right-md"})

for item in root:
    data = item.find("div", {"class":"story-card-component story-card__headline-container | text--overflow-ellipsis text--left"})
    link = item.find("a")
    link_url = link.get('href')
    
    driver.get(base_url + link_url)

    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')

    title = detail_soup.find("h1", {"class":"article-header__headline | font--primary text--black"})
    wirtes = detail_soup.find("a", {"class":"article-byline__author | text--wrap-pre text--black text__link--underline"})

    print(title.text)
    print(wirtes.text)
    
    contents = detail_soup.find("section" , {"class" : "article-body"}) #기사별로 나눔 표시하고 싶음
    full_content = ""
    
    for content in contents:
        full_content = full_content + contents.text
    
        print(content.text)
        print("")