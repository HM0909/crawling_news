from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  #크롬업데이트로 인해 추가
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import time
import csv

base_url = "https://www.donga.com/"

driver = webdriver.Chrome(ChromeDriverManager().install()) #크롬업데이트로 인해 수정
driver.get(base_url)

html = driver.page_source
soup = bs(html, 'html.parser')

root = soup.find("div", {"class":"scroll_start01_in"})
items = root.find_all("li", {"class":"list_item"})

for item in items:
    data = item.find("div", {"class":"cont_info"})
    link = item.find("a")
    link_url = link.get('href')
    
    driver.get(link_url)

    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')

    title = detail_soup.find("h1", {"class" : "title"})
    wirtes = detail_soup.find("span", {"class" : "report"})

    print(title.text)
    print(wirtes.text)

    section = detail_soup.find("div" , {"class" : "article_view"}) 
    contents = section.find("div" , {"class" : "article_txt"}) 
    full_content = ""
    
    for content in contents:
        full_content = full_content + contents.text
    
        print(content.text)
        print("")  #중간에 이상한 태그도 같이 뽑힘