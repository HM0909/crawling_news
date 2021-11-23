from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  #크롬업데이트로 인해 추가
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import time
import csv

base_url = "https://www.ytn.co.kr/" # YTN 뉴스

driver = webdriver.Chrome(ChromeDriverManager().install()) #크롬업데이트로 인해 수정
driver.get(base_url)

html = driver.page_source
soup = bs(html, 'html.parser')

root = soup.find("div", {"class":"now01 YTN_CSA_bottomnews1"}) #윗줄, 아랫줄 같이 추출 가능할까?
items = root.find_all("ul")

for item in items:
    data = item.find("li")
    link = item.find("a")
    link_url = link.get('href')
    
    driver.get(link_url) #윗줄의 앞의 칸만 열림
    
    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')

    top = detail_soup.find("div", {"class":"top"})
    title = top.find("h3")

    # wirtes = detail_soup.find("span", {"class" : "report"}) #기자가 택스트 내에 들어가 있어서 영역을 어떻게 잡아야 할지 모르겠음

    print(title.text)
    # print(wirtes.text)

    # section = detail_soup.find("div" , {"class" : "article"}) 
    contents = detail_soup.find("div" , {"class" : "article"}) 
    full_content = ""
    
    for content in contents:
        full_content = full_content + contents.text
    
        print(content.text)
        print("")