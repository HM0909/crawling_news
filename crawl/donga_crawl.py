from crawl_manager import *
from bs4 import BeautifulSoup as bs

BASE_URL = "https://www.donga.com/" #동아일보 뉴스

class DongaCrawlManager(CrawlManager):
    def __init__(self, driver):
        self.driver = driver
   
   
    # 기사 목록
    def list(self):     
        self.driver.get(BASE_URL)
    
        html = self.driver.page_source
        soup = bs(html, 'html.parser')
        root = soup.find("div", {"class":"mainnews_cont"})
        items = root.find_all("h3", {"class":"tit"})
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
    
        title = detail_soup.find("h1", {"class" : "title"}).text #제목
        
        writer = ""
        if detail_soup.find("div", {"class" : "report"}) != None:
            writer = detail_soup.find("div", {"class" : "report"}).text #작성자
        
        content = detail_soup.find("div" , {"class" : "article_txt"}).text #본문 #본문이 각각 다른 div로 되어 있음
        
        dates = detail_soup.find_all("span", {"class" : "date01"})
        
        if len(dates) > 1:
            reg_date = dates[1].text  # 수정일
        else:
            reg_date = dates[0].text  # 입력일

        pos = reg_date.find(" ")
        
        if pos > 0:
            reg_date = reg_date[pos:]
            
        return [title, detail_url, writer, reg_date.strip(), content]