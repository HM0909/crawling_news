from crawl_manager import *
from bs4 import BeautifulSoup as bs

BASE_URL = "https://www.khan.co.kr/" # 경향신문 뉴스

class KhanCrawlManager(CrawlManager):
    def __init__(self, driver):
        self.driver = driver


    # 기사 목록
    def list(self):     
        self.driver.get(BASE_URL)
        
        html = self.driver.page_source
        soup = bs(html, 'html.parser')
        root = soup.find("ul", {"class":"sub-news-wrap scroll_start02_in"})
        items = root.find_all("li")
        datas = []
        
        for item in items:
            link = item.find("a")
            link_url = link.get('href')
                
            datas.append(link_url) 
        
        return datas
    

    # 상세 내용
    def detail(self, url):
        detail_url = url
        
        self.driver.get(detail_url)
        detail_html = self.driver.page_source 
        detail_soup = bs(detail_html, 'html.parser')

        title = detail_soup.find("h1", {"class":"headline"}).text #제목
        writer = detail_soup.find("span", {"class":"author"}).text #작성자
        content = detail_soup.find("div" , {"class" : "art_body"}).text #본문 
        
        all_date =detail_soup.find("div" , {"class" : "byline"})
        dates =all_date.find_all("em")
        
        if len(dates) > 1: 
            reg_date = dates[1].text  # 수정일
        else:
            reg_date = dates[0].text  # 입력일
       

        return [title, detail_url, writer, reg_date, content]