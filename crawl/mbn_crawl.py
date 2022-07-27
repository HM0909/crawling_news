from crawl_manager import *
from bs4 import BeautifulSoup as bs

BASE_URL = "https://www.mbn.co.kr/pages/news/index.html" # MBN 뉴스

class MbnCrawlManager(CrawlManager):
    def __init__(self, driver):
        self.driver = driver
         
          
     # 기사 목록
    def list(self):     
        self.driver.get(BASE_URL)
        
        html = self.driver.page_source
        soup = bs(html, 'html.parser')
        root = soup.find("div", {"class":"list_news"})
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
        if detail_url.find("http") < 0 and  detail_url.find("https"):
            detail_url = "https:" + detail_url
        
        self.driver.get(detail_url)
        detail_html = self.driver.page_source 
        detail_soup = bs(detail_html, 'html.parser')
        
        title_head = detail_soup.find("div", {"class" : "box01"})
        title = title_head.find("h1").text #제목
        
        writer = ""
        
        if detail_soup.find("span", {"class" : "report"}) != None:
            writer = detail_soup.find("span", {"class" : "report"}).text #작성자
        
        content = detail_soup.find("div" , {"class" : "detail"}).text #본문
        
        all_date =detail_soup.find("span" , {"class" : "time"})
        dates =all_date.find_all("span")
        
        if len(dates) > 1:
            reg_date = dates[1].text  # 수정일
        else:
            reg_date = dates[0].text  # 입력일

        return [title, detail_url, writer, reg_date, content]