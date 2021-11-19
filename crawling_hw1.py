from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  #크롬업데이트로 인해 추가
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import time
import csv

base_url = "https://news.naver.com/"

driver = webdriver.Chrome(ChromeDriverManager().install()) #크롬업데이트로 인해 수정
driver.get(base_url)

html = driver.page_source
soup = bs(html, 'html.parser')

root = soup.find("ul", {"class":"hdline_article_list"})
items = root.find_all("li")

for item in items:
    data = item.find("div", {"class":"hdline_article_tit"}) 
    link = data.find("a")
    link_url = link.get('href')
    
    driver.get(base_url + link_url)
    
    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')

    title = detail_soup.find("h3", {"class" : "tts_head"})
    wirtes = detail_soup.find("p", {"class" : "b_text"})

    print(title.text)
    print(wirtes.text.strip()) #[9:] 
    
    # 막힘
    section = detail_soup.find("div", {"class" : "_article_body_contents article_body_contents"})
    contents = section.get("br")
    full_content = ""
                        
    for content in contents:
        all_content = full_content + content.text
        print(all_content)
        print("")
        
    