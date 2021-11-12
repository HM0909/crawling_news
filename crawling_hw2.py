from selenium import webdriver
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import time
import csv

base_url = "https://www.hani.co.kr/"

driver = webdriver.Chrome(executable_path='C:\hm_py\chromedriver')
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
    
    section = detail_soup.find("div" , {"class" : "text"}) 
    contents = section.find_all("div")
    full_content = ""

    for content in contents:
        full_content = full_content + content.text
    print(content.text)
    print("")
    