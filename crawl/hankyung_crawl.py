from crawl_manager import *
from bs4 import BeautifulSoup as bs

BASE_URL = "https://www.hankyung.com/" #한국경제 뉴스

class HankyungCrawlManager(CrawlManager):
    def __init__(self, driver):
        self.driver = driver
    
    
    # 기사 목록
    def list(self):     
        self.driver.get(BASE_URL)
        
        html = self.driver.page_source
        soup = bs(html, 'html.parser')
        root = soup.find("div", {"class":"main-top-major"})
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
        
        title = self.get_writer(detail_soup.find("h1", {"class" : "headline"}).text) #제목
        
        writer = ""
        if detail_soup.find("div", {"class" : "author"}) != None:            
            writer = self.get_writer(detail_soup.find("div", {"class" : "author"}).text) #작성자 #공백 없이 추출하고 싶음
            
        content = ""
        if detail_soup.find("div" , {"id" : "articletxt"}) != None:
            content = detail_soup.find("div" , {"id" : "articletxt"}).text #본문
        
        
        all_date =detail_soup.find("div" , {"class" : "datetime"})
        dates =all_date.find_all("span")
        
        if len(dates) > 1:
            reg_date = dates[1].text  # 수정일
        else:
            reg_date = dates[0].text  # 입력일

        return [title, detail_url, writer, reg_date, content]
    
             
    # 텍스트 리플레스 #**        
    def get_writer(self, writer):
        writer = writer.replace('\n', '')
        writer = writer.replace(" ", "")
        writer = writer.replace("·", " ")
        
        return writer