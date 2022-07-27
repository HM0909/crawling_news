from crawl_manager import *
from bs4 import BeautifulSoup as bs

BASE_URL = "https://www.hani.co.kr" #한겨레 뉴스

class HaniCrawlManager(CrawlManager):
    def __init__(self, driver):
        self.driver = driver
       
    # 기사 목록
    def list(self):     
        self.driver.get(BASE_URL)
        
        html = self.driver.page_source
        soup = bs(html, 'html.parser')
        root = soup.find("div", {"class":"type1"})
        items = root.find_all("div", {"class":"main-top"})
        datas = []
        
        for item in items:
            data = item.find("h4", {"class":"article-title"}) 
            link = data.find("a")
            link_url = link.get('href')
            
            datas.append( BASE_URL + link_url)
    
        return datas
           
    # 상세 내용
    def detail(self, url):
        detail_url = url

        self.driver.get(detail_url)
        detail_html = self.driver.page_source 
        detail_soup = bs(detail_html, 'html.parser')
        
        title = detail_soup.find("span", {"class" : "title"}).text #제목
        
        writer = ""
        
        if detail_soup.find("div", {"class" : "name"}) != None:
            writer = detail_soup.find("div", {"class" : "name"}).text #작성자
        
        section = detail_soup.find("div" , {"class" : "article-text-font-size"})
        content = section.find("div" , {"class" : "text"}).text #본문
        
        
        all_date =detail_soup.find("p" , {"class" : "date-time"})
        dates =all_date.find_all("span")
        
        if len(dates) > 1:
            reg_date = dates[1].text  # 수정일
    
        else:
            reg_date = dates[0].text  # 입력일

                
        return [title, detail_url, writer, reg_date, content]
